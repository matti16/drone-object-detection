from tkinter import *
from PIL import ImageTk, Image
import cv2
from config import *
from controller import FlightController, Velocities
from trip import Trip

class Application(Frame):

    def __init__(self, master, detector, video, controller: FlightController, tracker, api_client):
        super(Application, self).__init__(master, background=BLACK)
        self.grid()

        self.detector = detector
        self.video = video
        self.controller = controller
        self.tracker = tracker
        self.api_client = api_client
        self.target_id = None
        self.target_class = None
        self.trip = None
        
        self.create_video_frame()
        self.create_targets_frame()
        
        self.control_frame = Frame(self, background=BLACK)
        self.control_frame.grid(column=0, row=0)
        self.create_control_buttons(offset_row=0, offset_col=0)
        self.create_move_arrows(offset_row=2, offset_col=0)
        self.velocity_label = Label(self.control_frame, text="No target", foreground=WHITE, background=BLACK)
        self.velocity_label.grid(column=1, row=6, padx=5, pady=(20, 10))

        self.controller_loop()


    def create_targets_frame(self):
        self.targets = {}
        self.target_label = Label(
            self, text="NO TARGET", width=30, background=BLACK, foreground=WHITE
        )
        self.target_label.grid(padx=10, pady=(20, 5), column=2, row=0, sticky='N')
        self.targets_frame = Frame(self, background=BLACK, width=250, height=460)
        self.targets_frame.grid(padx=10, pady=50, column=2, row=0, sticky='N')
        self.targets_frame.grid_propagate(0)


    def create_video_frame(self):
        self.video_frame = Frame(self, background=BLACK)
        self.video_frame.grid(padx=20, pady=20, column=1, row=0)
        self.video_label = Label(self.video_frame, borderwidth=5, background=BLUE)
        self.video_label.grid()

    def update_velocities_info(self, velocities: Velocities=None):
        if velocities:
            velocity_text = f"Up/Down: {velocities.velocity_up}\n"
            velocity_text += f"Fwd/Bck: {velocities.velocity_forward}\n"
            velocity_text += f"Yaw: {velocities.velocity_yaw}\n"
        else:
            velocity_text = "No target"
        self.velocity_label.configure(text=velocity_text)
    
    def create_move_arrows(self, offset_row, offset_col):
        self.arrow_btns = {}
        pos = [(0, 1), (1, 0), (1, 2), (2, 1), (3, 0), (3, 2)]
        subsample = [30, 30, 30, 30, 8, 8]
        for i, c in enumerate(["up", "left", "right", "down", "bck", "fwd"]):
            self.arrow_btns[c] = {}
            self.arrow_btns[c]["img"] = PhotoImage(
                master=self.control_frame, file=get_asset_path(c + "_arrow.png")
            ).subsample(subsample[i])
            
            self.arrow_btns[c]["btn"] = Button(
                self.control_frame, 
                text=c,
                image=self.arrow_btns[c]["img"], 
                background=BLACK
            )
            self.arrow_btns[c]["btn"].grid(
                row=pos[i][0]+offset_row, column=pos[i][1]+offset_col, padx=5
            )
            self.arrow_btns[c]["btn"].bind("<ButtonPress>", lambda ev, x=c: self.arrow_pressed(x))
            self.arrow_btns[c]["btn"].bind("<ButtonRelease>", self.arrow_released)

    
    def arrow_pressed(self, direction):
        self.select_target(None, stop=False)
        self.controller.move_direction(direction)
    

    def arrow_released(self, event):
        self.controller.stop()


    def create_control_buttons(self, offset_row, offset_col):
        self.btns = {}
        for i, s in enumerate(["start", "hold", "stop"]):
            self.btns[s] = {}
            self.btns[s]["img"] = PhotoImage(
                master=self.control_frame, file=get_asset_path(s + "_btn.png")
            ).subsample(25)
            
            self.btns[s]["btn"] = Button(
                self.control_frame, 
                text=s.upper(),
                image=self.btns[s]["img"], 
                background=BLACK
            )
            self.btns[s]["btn"].grid(column=i+offset_col, row=offset_row, padx=5)
            self.btns[s]["label"] = Label(self.control_frame, text=s, foreground=WHITE, background=BLACK)
            self.btns[s]["label"].grid(column=i+offset_col, row=offset_row+1, padx=5, pady=(0, 10))
        
        self.btns["start"]["btn"].configure(command=self.start_drone)
        self.btns["hold"]["btn"].configure(command=self.controller.stop)
        self.btns["stop"]["btn"].configure(command=self.controller.tello.land)

    def start_drone(self):
        self.controller.connect()
        self.controller.takeoff()


    def update_detected_targets(self, boxes, classes, frame, boxes_ids):
        for i, box in enumerate(boxes):
            box_id = boxes_ids[i]
            if box_id not in self.targets:
                self.targets[box_id] = {}
                # img = Video.crop_image_box(frame, box)
                # img = ImageTk.PhotoImage(Image.fromarray(img))
                # self.targets[box_id]["img"] = img
                self.targets[box_id]["btn"] = Button(
                    self.targets_frame, 
                    text=f"{classes[i]} {box_id}".upper(),
                    background=YELLOW,
                    command=lambda x=box_id,y=classes[i]:self.select_target(x, False, y)
                )
                self.targets[box_id]["btn"].grid(pady=5)
                self.targets[box_id]["class"] = classes[i]
        
        for i, b in self.targets.items():
            if not i in boxes_ids:
                if i == self.target_id:
                    self.select_target(None)
                    for j, b2 in self.targets.items():
                        if b2["class"] == b["class"] and j in boxes_ids and j != i:
                            self.select_target(j, False, b2["class"])
                            break
                b["btn"].destroy()
        self.targets = {k:v for k,v in self.targets.items() if k in boxes_ids}


    def select_target(self, target_id=None, stop=True, target_class=None):
        target_id = None if self.target_id == target_id else target_id
        if target_id:
            self.target_label.configure(text=f"TARGET: {self.targets[target_id]['class']} {target_id}".upper())
            self.video_label.configure(background=RED)
            self.trip = Trip(self.controller.tello, self.targets[target_id]['class'])
        else:
            self.target_label.configure(text=f"NO TARGET")
            self.video_label.configure(background=BLUE)
            if stop:
                self.controller.stop()
            if self.trip is not None:
                self.trip.end_trip()
                self.trip = None
            
        self.target_id = target_id
        self.target_class = target_class

    # function for video streaming
    def controller_loop(self):
        if not self.controller.tello.stream_on:
            img = PhotoImage(file=get_asset_path("background.png"))
        else:
            frame = self.controller.frame_read.frame
            boxes, classes = self.detector.predict(frame)
            boxes, boxes_ids = self.tracker.update(boxes)
            
            velocities = None
            if self.target_id and self.target_id in boxes_ids:
                target_box = boxes[boxes_ids.index(self.target_id)]
                velocities = self.controller.step(
                    target_box=target_box, frame=frame
                )
            
            self.update_velocities_info(velocities)

            frame = self.video.draw_boxes(boxes, classes, frame, boxes_ids)
            if self.trip is not None:
                self.trip.record_step(frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.update_detected_targets(boxes, classes, frame, boxes_ids)

        self.video_label.configure(image=img)
        self.video_label.image = img
        self.video_label.update()
        self.video_label.after(1, self.controller_loop) 


