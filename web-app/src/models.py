from datetime import datetime
from pydantic import BaseModel


class Trip(BaseModel):
    vechicle_id: str
    trip_id: str
    start_time: datetime
    end_time: datetime
    target_label: str
    steps: list
