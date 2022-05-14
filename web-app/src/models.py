from datetime import datetime
from pydantic import BaseModel


class Trip(BaseModel):
    vechicle_id: str
    trip_id: str
    start_time: datetime
    end_time: datetime
    target_class: str
    steps: list


class TripImage(BaseModel):
    data: str
    filename: str
    vehicle_id: str
    trip_id: str

