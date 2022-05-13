from fastapi import FastAPI, File, UploadFile, Form
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from models import Trip
import boto3
import json

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
def post_trip(body: Trip):
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(
        TableName=DYNAMO_DB_TABLE, 
        Item={
            'VehicleId': {'S': body.vechicle_id},
            'TripId': {'S': body.vechicle_id},
            'StartTime': {'S': body.start_time},
            'EndTime': {'S': body.end_time},
            'Steps': {'S': json.dumps(body.steps)},
        }
    )


@app.post(f"{BASE_PATH}/trip_img")
def post_trip_img(
        img: UploadFile = File(...), 
        vehicle_id: str = Form(...), 
        trip_id: str = Form(...)
    ):
    s3_path = f"trips_images/{vehicle_id}/{trip_id}/{img.filename}"
    contents = await img.read() 

    client = boto3.client('s3')
    client.put_object(Body=contents, Bucket=S3_BUCKET, Key=s3_path)

    return {"bucket": S3_BUCKET, "key": s3_path}


handler = Mangum(app)