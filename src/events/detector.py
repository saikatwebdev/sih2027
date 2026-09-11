class EventDetector:

    def __init__(self):
        self.previous_objects = {}

    def detect(self, world):
        events = []

        current_objects = set(world.objects.keys())

        for object_id, obj in world.objects.items():
            previous = self.previous_objects.get(object_id)

            if previous is None:
                self.previous_objects[object_id] = {
                    "grid_cell": obj.grid_cell,
                    "position": obj.position_2d,
                    "state": obj.state
                }

                events.append({
                    "type": "OBJECT_DETECTED",
                    "object_id": object_id,
                    "grid_cell": obj.grid_cell
                })

                continue

            previous_grid = previous["grid_cell"]
            previous_position = previous["position"]
            previous_state = previous["state"]

            if previous_grid != obj.grid_cell:
                events.append({
                    "type": "OBJECT_MOVED",
                    "object_id": object_id,
                    "from": previous_grid,
                    "to": obj.grid_cell
                })

            if previous_position != obj.position_2d:
                events.append({
                    "type": "OBJECT_POSITION_CHANGED",
                    "object_id": object_id,
                    "from": previous_position,
                    "to": obj.position_2d
                })

            if previous_state != obj.state:
                events.append({
                    "type": "OBJECT_STATE_CHANGED",
                    "object_id": object_id,
                    "from": previous_state,
                    "to": obj.state
                })

            self.previous_objects[object_id] = {
                "grid_cell": obj.grid_cell,
                "position": obj.position_2d,
                "state": obj.state
            }

        previous_ids = set(self.previous_objects.keys())

        for object_id in previous_ids - current_objects:
            events.append({
                "type": "OBJECT_LOST",
                "object_id": object_id
            })

            del self.previous_objects[object_id]

        return events