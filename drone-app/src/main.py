import sys
from tkinter import Tk
from app import Application

from detection import Detector
from controller import FlightController
from video import Video
from tracker import EuclideanDistTracker
from api_client import ApiClient
from config import BLACK, BASE_API_URL, API_TOKEN, DATA_LOG_PATH, DATA_UPLOADED_PATH


def main():
    detector = Detector()
    controller = FlightController()
    video = Video()
    tracker = EuclideanDistTracker()

    window = Tk()
    window.title("Tello Drone")
    window.geometry("1600x850") 
    window.configure(background=BLACK)
    app = Application(window, detector, video, controller, tracker, api_client)
    app.mainloop()


if __name__=='__main__':
    if sys.argv[1] == "upload":
        api_client = ApiClient(BASE_API_URL, API_TOKEN)
        api_client.upload_trips(DATA_LOG_PATH, DATA_UPLOADED_PATH)
    else:
        main()