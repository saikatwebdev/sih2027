from src.world.state import (
    WorldState,
    PersonState,
    ObjectState
)


class WorldModelBuilder:

    def build(self, yolo_data):
        world = WorldState(
            frame_id=yolo_data["frame_id"],
            timestamp=yolo_data["timestamp"]
        )

        for detection in yolo_data.get("objects", []):
            object_id = detection["id"]
            object_type = detection["class"]
            confidence = detection["confidence"]

            center = detection.get(
                "center",
                [0, 0]
            )

            bbox = detection.get(
                "bbox",
                []
            )

            if object_type == "person":
                person = PersonState(
                    person_id=object_id,
                    position=center,
                    bbox=bbox,
                    activity=detection.get(
                        "activity",
                        "UNKNOWN"
                    ),
                    confidence=confidence
                )

                world.people[object_id] = person

                continue

            grid = detection.get("grid")

            if grid:
                grid_cell = (
                    f"R{grid['row']}"
                    f"C{grid['column']}"
                )
            else:
                grid_cell = None

            object_state = ObjectState(
                object_id=object_id,
                object_type=object_type,
                position_2d=center,
                grid_cell=grid_cell,
                state=detection.get(
                    "state",
                    "UNKNOWN"
                ),
                confidence=confidence
            )

            world.objects[object_id] = object_state

        return world