from fastapi import FastAPI, File, UploadFile, Form
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from models import Trip, TripImage
import boto3
import json
import base64

from config import BASE_PATH, DYNAMO_DB_TABLE, S3_BUCKET


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

@app.post(f"{BASE_PATH}/trip")
def post_trip(trip: Trip):
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(
        TableName=DYNAMO_DB_TABLE, 
        Item={
            'VehicleId': {'S': str(trip.vehicle_id)},
            'TripId': {'S': str(trip.trip_id)},
            'TargetClass': {'S': str(trip.target_class)},
            'StartTime': {'S': str(trip.start_time)},
            'EndTime': {'S': str(trip.end_time)},
            'Steps': {'S': json.dumps(trip.steps, default=str)},
        }
    )
    return {"vehile_id": str(trip.vehicle_id), "trip_id": str(trip.trip_id)}


@app.post(f"{BASE_PATH}/trip_img")
async def post_trip_img(trip_img: TripImage):
    s3_path = f"trips_images/{trip_img.vehicle_id}/{trip_img.trip_id}/{trip_img.filename}"
    data = base64.b64decode(trip_img.data)
    client = boto3.client('s3')
    client.put_object(Body=data, Bucket=S3_BUCKET, Key=s3_path)
    return {"bucket": S3_BUCKET, "key": s3_path}


handler = Mangum(app)