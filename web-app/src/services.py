import boto3
import json

from config import DYNAMO_DB_TABLE, S3_BUCKET
from models import Trip

def save_trip_to_dynamo(trip: Trip):
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


def get_trip_from_dynamo(vehicle_id, trip_id):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        Key={
            'VehicleId': {
                'S': vehicle_id,
            },
            'TripId': {
                'S': trip_id,
            },
        },
        TableName=DYNAMO_DB_TABLE,
    )
    return Trip(
        vehicle_id=response["Item"]["VehicleId"]["S"],
        trip_id=response["Item"]["TripId"]["S"],
        start_time=response["Item"]["StartTime"]["S"],
        end_time=response["Item"]["EndTime"]["S"],
        target_class=response["Item"]["TargetClass"]["S"],
        steps=json.loads(response["Item"]["Steps"]["S"])
    )

def get_trip_img_urls(trip: Trip) -> Trip:
    s3_client = boto3.client('s3')
    for s in trip.steps:
        if s["img_filename"]:
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': S3_BUCKET, 
                    'Key': f"trips_images/{trip.vehicle_id}/{trip.trip_id}/{s['img_filename']}"
                    },
                ExpiresIn=3600
            )
            s["img_url"] = presigned_url
    return trip