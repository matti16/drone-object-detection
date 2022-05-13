import sys
import os


VEHICLE_ID = 1

# Flight Controller
TARGET_SIZE_PERC = 0.7
VERTICAL_SHIFT = 25  # The camera of Tello drone is slightly inclined to down, increase this to adjust for it
MAX_SPEED_FORWARD = 100
MAX_SPEED_UP = 75
MAX_SPEED_YAW = 100
MIN_MOV_TIME = 0.15

# GUI
BLACK = "#212121"
WHITE = "#FAFAFA"
RED = "#FFB3BA"
GREEN = "#BAFFC9"
YELLOW = "#FFFFBA"
BLUE = "#BAE1FF"

APP_MUSIC = "the_imperial_march.mp3"

# Object Detection
THRESHOLD = 0.6
COCO_LABELS = [
    "__background__",
    "person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "traffic light",
    "fire hydrant",
    "N/A",
    "stop sign",
    "parking meter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "N/A",
    "backpack",
    "umbrella",
    "N/A",
    "N/A",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sports ball",
    "kite",
    "baseball bat",
    "baseball glove",
    "skateboard",
    "surfboard",
    "tennis racket",
    "bottle",
    "N/A",
    "wine glass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hot dog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "potted plant",
    "bed",
    "N/A",
    "dining table",
    "N/A",
    "N/A",
    "toilet",
    "N/A",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cell phone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "N/A",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddy bear",
    "hair drier",
    "toothbrush",
]


def get_base_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
    return base_path

def get_resources_path():
    return os.path.join(get_base_path(), "resources")


RESOURCES_PATH = get_resources_path()
DATA_LOG_PATH = os.path.join(get_base_path(), "data_log")


def get_asset_path(name):
    return os.path.join(RESOURCES_PATH, "assets", name)