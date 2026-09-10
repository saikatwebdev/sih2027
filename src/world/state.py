from dataclasses import dataclass, field


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

    people: dict = field(
        default_factory=dict
    )

    objects: dict = field(
        default_factory=dict
    )

    environment: dict = field(
        default_factory=dict
    )