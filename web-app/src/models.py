from pydantic import BaseModel


class Trip(BaseModel):
    vehicle_id: str
    trip_id: str
    start_time: str
    end_time: str
    target_class: str
    steps: list


class TripImage(BaseModel):
    data: str
    filename: str
    vehicle_id: str
    trip_id: str

