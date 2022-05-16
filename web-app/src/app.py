from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from models import Trip, TripImage
import boto3
import base64

from config import BASE_PATH, S3_BUCKET
from services import save_trip_to_dynamo, get_trip_from_dynamo, get_trip_img_urls

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
    save_trip_to_dynamo(trip)
    return {"vehile_id": str(trip.vehicle_id), "trip_id": str(trip.trip_id)}


@app.post(f"{BASE_PATH}/trip_img")
def post_trip_img(trip_img: TripImage):
    s3_path = f"trips_images/{trip_img.vehicle_id}/{trip_img.trip_id}/{trip_img.filename}"
    data = base64.b64decode(trip_img.data)
    client = boto3.client('s3')
    client.put_object(Body=data, Bucket=S3_BUCKET, Key=s3_path)
    return {"bucket": S3_BUCKET, "key": s3_path}


@app.get(BASE_PATH + "/trip/{vehicle_id}/{trip_id}")
def get_trip(vehicle_id: str, trip_id: str) -> Trip:
    trip = get_trip_from_dynamo(vehicle_id, trip_id)
    trip = get_trip_img_urls(trip)
    return trip


handler = Mangum(app)