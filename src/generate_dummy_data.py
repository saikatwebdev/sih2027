# from src import yolo_reader
import json 
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

HMR_DIR = BASE_DIR / "data" / "hmr"
YOLO_DIR = BASE_DIR / "data" / "yolo"

HMR_DIR.mkdir(parents=True, exist_ok=True)
YOLO_DIR.mkdir(parents=True, exist_ok=True)

frames = [
    {
        "frame": 1,
        "time": 0.0,
        "activity": "IDLE",
        "person_position": [0.0, 0.0, 0.0],
        "right_wrist": [0.3, 0.9, 0.0],
        "object_grid": [4, 7],
        "object_state": "STATIONARY"
    },

    {
        "frame": 2,
        "time": 0.1,
        "activity": "WALKING",
        "person_position": [0.4, 0.0, 0.5],
        "right_wrist": [0.7, 0.9, 0.5],
        "object_grid": [4, 7],
        "object_state": "STATIONARY"
    },

    {
        "frame": 3,
        "time": 0.2,
        "activity": "REACHING",
        "person_position": [0.8, 0.0, 1.0],
        "right_wrist": [1.2, 0.9, 1.2],
        "object_grid": [4, 7],
        "object_state": "STATIONARY"
    },

    {
        "frame": 4,
        "time": 0.3,
        "activity": "GRABBING",
        "person_position": [1.0, 0.0, 1.2],
        "right_wrist": [1.5, 0.7, 1.4],
        "object_grid": [4, 7],
        "object_state": "HELD"
    },

    {
        "frame": 5,
        "time": 0.4,
        "activity": "MOVING_OBJECT",
        "person_position": [1.2, 0.0, 1.5],
        "right_wrist": [1.7, 0.7, 1.7],
        "object_grid": [4, 7],
        "object_state": "HELD"
    },

    {
        "frame": 6,
        "time": 0.5,
        "activity": "PLACING",
        "person_position": [1.5, 0.0, 2.0],
        "right_wrist": [2.0, 0.7, 2.2],
        "object_grid": [5, 8],
        "object_state": "PLACED"
    },

    {
        "frame": 7,
        "time": 0.6,
        "activity": "IDLE",
        "person_position": [1.6, 0.0, 2.1],
        "right_wrist": [1.9, 0.9, 2.1],
        "object_grid": [5, 8],
        "object_state": "STATIONARY"
    }
]


def create_hmr(frame):
    x, y, z = frame["person_position"]

    hmr = {
        "frame_id": frame["frame"],
        "timestamp": frame["time"],

        "person": {
            "id": "person_01",

            "root": [x, y, z],

            "joints": {
                "pelvis": [x, 1.0, z],

                "left_shoulder": [
                    x - 0.2,
                    1.5,
                    z
                ],

                "right_shoulder": [
                    x + 0.2,
                    1.5,
                    z
                ],

                "left_elbow": [
                    x - 0.3,
                    1.2,
                    z
                ],

                "right_elbow": [
                    x + 0.3,
                    1.2,
                    z
                ],

                "left_wrist": [
                    x - 0.3,
                    0.9,
                    z
                ],

                "right_wrist": frame["right_wrist"]
            },
            "activity":frame["activity"],
            "confidence": 0.95
        }
    }

    return hmr


def create_yolo(frame):
    row, column = frame["object_grid"]

    yolo = {
        "frame_id": frame["frame"],
        "timestamp": frame["time"],

        "objects": [
            {
                "id": "object_01",

                "class": "tool",

                "bbox": [
                    1000,
                    450,
                    120,
                    150
                ],

                "center": [
                    1060,
                    525
                ],

                "confidence": 0.95,

                "grid": {
                    "row": row,
                    "column": column
                },

                "state": frame["object_state"]
            }
        ]
    }

    return yolo



for frame in frames :
    hmr = create_hmr(frame)
    yolo = create_yolo(frame)

    hmr_path = HMR_DIR /f"frame_{frame['frame']:03d}.json"
    yolo_path = YOLO_DIR / f"frame_{frame['frame']:03d}.json"

    with open(hmr_path, "w") as f:
        json.dump(hmr, f, indent=2)

    with open(yolo_path, "w") as f:
        json.dump(yolo, f, indent=2)


print("Dummy dataset generated.")    


