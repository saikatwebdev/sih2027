"""YOLO detection data reader module."""
import json
from pathlib import Path


class YOLOReader:

    def __init__(self, directory):
        self.directory = Path(directory)

    def read_frame(self, frame_id):

        filename = self.directory / f"frame_{frame_id:03d}.json"

        with open(filename, "r") as file:
            return json.load(file)