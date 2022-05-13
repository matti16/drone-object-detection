import numpy as np
import colorsys
import cv2


COLORS = 5

class Video:
    def __init__(self, video_addr=0) -> None:
        self.video = cv2.VideoCapture(video_addr)

    def read(self):
        return self.video.read()

    @staticmethod
    def hue_to_rgb(hue):
        (r, g, b) = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        r, g, b = int(255 * r), int(255 * g), int(255 * b)
        return (r, g, b)

    def draw_boxes(self, boxes, classes, image, boxes_ids):
        for i, box in enumerate(boxes):
            color = self.hue_to_rgb(boxes_ids[i] / COLORS)
            start_point = (int(box[0]), int(box[1]))
            end_point = (int(box[2]), int(box[3]))
            center = (int(np.mean([box[0], box[2]])), int(np.mean([box[1], box[3]])))
            cv2.rectangle(image, start_point, end_point, color, 2)
            cv2.putText(
                image,
                f"{boxes_ids[i]} - {classes[i]}",
                (int(box[0]), int(box[1] - 5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                1,
                lineType=cv2.LINE_AA,
            )
            cv2.circle(image, center, 3, color=color, thickness=cv2.FILLED)

        return image

    @staticmethod
    def crop_image_box(frame, box, size=86):
        img = frame[box[1]:box[3], box[0]:box[2]]
        img = cv2.resize(img, (size, size))
        return img

    def draw_speeds(
        self, image, center, color, velocity_forward, velocity_up, velocity_yaw
    ):
        up_arrow = (center[0], center[1] - velocity_up)
        cv2.arrowedLine(image, center, up_arrow, color)

        right_arrow = (center[0] + velocity_yaw, center[1])
        cv2.arrowedLine(image, center, right_arrow, color)

        speed_rect_start = (center[0] - 10, center[1] - velocity_forward)
        cv2.rectangle(image, speed_rect_start, center, color, cv2.FILLED)
