from tkinter import Tk
from app import Application

from detection import Detector
from controller import FlightController
from video import Video
from tracker import EuclideanDistTracker
from config import BLACK


def main():
    detector = Detector()
    controller = FlightController()
    video = Video()
    tracker = EuclideanDistTracker()

    window = Tk()
    window.title("Tello Drone")
    window.geometry("1600x850") 
    window.configure(background=BLACK)
    app = Application(window, detector, video, controller, tracker)
    app.mainloop()


if __name__=='__main__':
    main()