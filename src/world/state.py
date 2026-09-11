from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PersonState:
    person_id: str
    position: list
    joints: dict
    activity: str
    confidence: float


@dataclass
class ObjectState:
    object_id: str
    object_type: str
    position_2d: list
    grid_cell: str
    state: str
    confidence: float


@dataclass
class WorldState:
    frame_id: int
    timestamp: float

    people: dict = field(default_factory=dict)
    objects: dict = field(default_factory=dict)
    environment: dict = field(default_factory=dict)

    current_state: Optional[str] = None
    previous_state: Optional[str] = None

    observations: list = field(default_factory=list)

    def to_dict(self):
        return {
            "frame_id": self.frame_id,
            "timestamp": self.timestamp,

            "current_state": self.current_state,
            "previous_state": self.previous_state,

            "people": {
                pid: {
                    "person_id": person.person_id,
                    "position": person.position,
                    "joints": person.joints,
                    "activity": person.activity,
                    "confidence": person.confidence
                }
                for pid, person in self.people.items()
            },

            "objects": {
                oid: {
                    "object_id": obj.object_id,
                    "object_type": obj.object_type,
                    "position_2d": obj.position_2d,
                    "grid_cell": obj.grid_cell,
                    "state": obj.state,
                    "confidence": obj.confidence
                }
                for oid, obj in self.objects.items()
            },

            "environment": self.environment,

            "observations": self.observations
        }