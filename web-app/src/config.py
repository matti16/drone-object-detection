import os

REGION = os.getenv("REGION", "eu-west-1")

BASE_PATH = "/api"

S3_BUCKET = os.environ["S3_BUCKET"]
DYNAMO_DB_TABLE = os.environ["DYNAMO_DB_TABLE"]