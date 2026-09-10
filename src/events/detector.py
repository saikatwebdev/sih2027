class EventDetector:

    def __init__(self):

        self.previous_objects = {}


    def detect(self, world):

        events = []


        for (
            object_id,
            obj
        ) in world.objects.items():

            previous = (
                self.previous_objects.get(
                    object_id
                )
            )


            # First time seeing object
            if previous is None:

                self.previous_objects[
                    object_id
                ] = obj.grid_cell

                continue


            # Object moved
            if previous != obj.grid_cell:

                events.append({

                    "type":
                        "OBJECT_MOVED",

                    "object_id":
                        object_id,

                    "from":
                        previous,

                    "to":
                        obj.grid_cell
                })


            # Save latest location

            self.previous_objects[
                object_id
            ] = obj.grid_cell


        return events