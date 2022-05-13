from djitellopy import Tello
import time

from config import (
    TARGET_SIZE_PERC,
    VERTICAL_SHIFT,
    MAX_SPEED_FORWARD,
    MAX_SPEED_UP,
    MAX_SPEED_YAW,
    MIN_MOV_TIME,
)


class Velocities:
    def __init__(self, velocity_forward, velocity_up, velocity_yaw):
        self.velocity_forward = velocity_forward 
        self.velocity_up = velocity_up 
        self.velocity_yaw = velocity_yaw


class Step:
    def __init__(self, frame, boxes, classes, velocities, target_idx):
        self.frame = frame 
        self.boxes = boxes 
        self.classes = classes 
        self.velocities = velocities 
        self.target_idx = target_idx


class FlightController:
    def __init__(
        self, target_size_perc=TARGET_SIZE_PERC, vertical_shift=VERTICAL_SHIFT
    ) -> None:
        self.target_size_perc = target_size_perc
        self.vertical_shift = vertical_shift
        self.tello = Tello()

    def connect(self):
        self.tello.connect()
        self.tello.streamon()
        self.frame_read = self.tello.get_frame_read()

    def takeoff(self):
        try:
            self.tello.takeoff()
        except Exception as e:
            print(f"Error taking off: {e}")

    def tear_down(self):
        self.tello.end()

    def stop(self):
        self.tello.send_rc_control(0, 0, 0, 0)

    def move_direction(self, direction, speed=50):
        velocities = {
            "right": (0, 0, 0, speed),
            "left": (0, 0, 0, -speed),
            "up": (0, 0, speed, 0),
            "down": (0, 0, -speed, 0),
            "fwd": (0, speed, 0, 0),
            "bck": (0, -speed, 0, 0),
        }
        velocities = velocities[direction.lower()]
        self.tello.send_rc_control(*velocities)

    def step(self, target_box=None, frame=None) -> Step:
        if frame is None:
            frame = self.frame_read.frame
        
        velocities = None
        if target_box is not None:
            velocities = self.compute_speeds(frame, target_box)
        
        # First rotate, then go forward
        if velocities:
            if not velocities.velocity_yaw == 0:
                self.tello.send_rc_control(0, 0, 0, velocities.velocity_yaw)
                time.sleep(MIN_MOV_TIME)
            
            self.tello.send_rc_control(0, velocities.velocity_forward, velocities.velocity_up, 0)
            time.sleep(MIN_MOV_TIME)
        
        return velocities


    @staticmethod
    def calculate_velocity(frame_size, center_of_object, max_speed):
        center_of_frame = int(frame_size / 2)
        distance = center_of_object - center_of_frame
        return int(max_speed * (distance / frame_size)) * 2

    def compute_speeds(self, frame, target_bbox):
        frame_shape = frame.shape
        velocity_forward = velocity_up = velocity_yaw = 0
        target_size = (
            (frame_shape[0] ** 2 + frame_shape[1] ** 2) ** 0.5
        ) * self.target_size_perc

        start_x, start_y = int(target_bbox[0]), int(target_bbox[1])
        end_x, end_y = int(target_bbox[2]), int(target_bbox[3])

        target_center_x = int((start_x + end_x) / 2)
        target_center_y = int((start_y + end_y) / 2)
        current_size = (((start_x - end_x) ** 2) + ((start_y - end_y) ** 2)) ** 0.5

        delta_size_perc = (target_size - current_size) / target_size
        velocity_forward = int(delta_size_perc * MAX_SPEED_FORWARD)

        velocity_up = self.calculate_velocity(
            frame_shape[0], target_center_y + self.vertical_shift, MAX_SPEED_UP * -1
        )
        velocity_yaw = self.calculate_velocity(
            frame_shape[1], target_center_x, MAX_SPEED_YAW
        )
        return Velocities(velocity_forward, velocity_up, velocity_yaw)
