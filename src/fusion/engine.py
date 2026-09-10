from src.world.state import (
    WorldState,
    PersonState,
    ObjectState
)


class FusionEngine:

    def fuse(
        self,
        hmr_data,
        yolo_data
    ):

        frame_id = hmr_data["frame_id"]

        timestamp = hmr_data["timestamp"]


        world = WorldState(

            frame_id=frame_id,

            timestamp=timestamp
        )


        # ====================================================
        # PERSON
        # ====================================================

        person = hmr_data["person"]


        person_state = PersonState(

            person_id=person["id"],

            position=person["root"],

            joints=person["joints"],

            activity=person.get(
                "activity",
                "UNKNOWN"
            ),

            confidence=person[
                "confidence"
            ]
        )


        world.people[
            person["id"]
        ] = person_state


        # ====================================================
        # OBJECTS
        # ====================================================

        for obj in yolo_data["objects"]:

            grid = obj["grid"]


            grid_cell = (
                f"R{grid['row']}"
                f"C{grid['column']}"
            )


            object_state = ObjectState(

                object_id=obj["id"],

                object_type=obj["class"],

                position_2d=obj["center"],

                grid_cell=grid_cell,

                state=obj.get(
                    "state",
                    "UNKNOWN"
                ),

                confidence=obj[
                    "confidence"
                ]
            )


            world.objects[
                obj["id"]
            ] = object_state


        return world