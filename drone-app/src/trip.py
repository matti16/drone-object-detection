import datetime
from config import VEHICLE_ID, DATA_LOG_PATH
import cv2
import json
import os
from pydantic import BaseModel


IMG_FREQ = 3


class Step(BaseModel):
    dt: datetime.datetime
    
    pitch: int
    roll: int
    yaw: int
        
    vgx: int 
    vgy: int 
    vgz: int

    agx: float
    agy: float
    agz: float

    h: int
    bat: int

    img_filename: str


class Trip:
    def __init__(self, tello, target_class, vechicle_id=VEHICLE_ID):
        self.counter = 0
        self.tello = tello
        self.vechicle_id = vechicle_id
        self.target_class = target_class
        self.start_time = datetime.datetime.utcnow()
        self.end_time = None
        self.steps = []
        self.trip_id = ''.join([c for c in str(self.start_time) if c.isdigit()])
        self.vechicle_path = f"{self.vechicle_id}/{self.trip_id}"
        self.base_path = f"{DATA_LOG_PATH}/{self.vechicle_path}"
        os.makedirs(self.base_path)

    def save_img(self):
        return self.counter % IMG_FREQ == 0

    
    def record_step(self, img):
        dt = datetime.datetime.utcnow()
        if self.save_img():
            date_str = ''.join([c for c in str(dt) if c.isdigit()])
            img_path = f"{self.base_path}/{date_str}.jpg"
            cv2.imwrite(img_path, img)
            img_filename = f"{date_str}.jpg"
        else:
            img_filename = ""
        
        step = Step(
            dt=dt,
            pitch=self.tello.get_state_field('pitch'),
            roll=self.tello.get_state_field('roll'),
            yaw=self.tello.get_state_field('yaw'),
            vgx=self.tello.get_state_field('vgx'),
            vgy=self.tello.get_state_field('vgy'),
            vgz=self.tello.get_state_field('vgz'),
            agx=self.tello.get_state_field('agx'),
            agy=self.tello.get_state_field('agy'),
            agz=self.tello.get_state_field('agz'),
            h=self.tello.get_state_field('h'),
            bat=self.tello.get_state_field('bat'),
            img_filename=img_filename
        )

        self.steps.append(step)
        self.counter += 1
    

    def end_trip(self):
        self.end_time = datetime.datetime.utcnow()
        json_trip = {
            "vehicle_id": str(self.vechicle_id),
            "trip_id": str(self.trip_id),
            "target_class": self.target_class,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "steps": [s.dict() for s in self.steps]
        }
        filename = f"{self.base_path}/trip.json"
        self.save_trip(filename, json_trip)


    def save_trip(self, filename, data):
        print(f"Saving trip at {filename}")
        with open(filename, "w") as f:
            json.dump(data, f, indent=4, default=str)
        


    