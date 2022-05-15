from fastapi import FastAPI, File, UploadFile, Form
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from models import Trip, TripImage
import boto3
import json
import base64
from decimal import Decimal

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
            'Steps': {'L': json.loads(json.dumps(trip.steps, default=str), parse_float=Decimal)},
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

@app.get(BASE_PATH + "/trip/{vechicle_id}/{trip_id}")
def get_trip(vechicle_id: str, trip_id: str) -> Trip:
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        Key={
            'VehicleId': {
                'S': vechicle_id,
            },
            'TripId': {
                'S': trip_id,
            },
        },
        TableName=DYNAMO_DB_TABLE,
    )
    print(response)
    return Trip(
        vehicle_id=response["Item"]["VehicleId"]["S"],
        trip_id=response["Item"]["TripId"]["S"],
        start_time=response["Item"]["TargetClass"]["S"],
        end_time=response["Item"]["StartTime"]["S"],
        target_class=response["Item"]["EndTime"]["S"],
        steps=response["Item"]["Steps"].values()[0]
    )


handler = Mangum(app)