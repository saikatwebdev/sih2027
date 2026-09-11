import json
import time
from pathlib import Path

from src.input.yolo_reader import YOLOReader
from src.validation.validator import JSONValidator
from src.validation.procedure_validator import ProcedureValidator
from src.temporal.buffer import TemporalBuffer
from src.world.builder import WorldModelBuilder
from src.events.detector import EventDetector
from src.state_machine.machine import DigitalTwinStateMachine, TwinState
from src.observations.store import ObservationStore


BASE_DIR = Path(__file__).resolve().parent.parent

YOLO_DIR = BASE_DIR / "data" / "yolo"
YOLO_SCHEMA = BASE_DIR / "schemas" / "yolo_schema.json"
OBSERVATION_FILE = BASE_DIR / "data" / "observations.json"
ANOMALY_FILE = BASE_DIR / "data" / "anomaly_observations.json"


yolo_reader = YOLOReader(YOLO_DIR)
yolo_validator = JSONValidator(YOLO_SCHEMA)
yolo_buffer = TemporalBuffer(max_size=5)

world_builder = WorldModelBuilder()
event_detector = EventDetector()

state_machine = DigitalTwinStateMachine()
procedure_validator = ProcedureValidator()

observation_store = ObservationStore(
    observation_file=OBSERVATION_FILE,
    anomaly_file=ANOMALY_FILE
)


START_FRAME = 1
END_FRAME = 7
FRAME_DELAY = 0.5


def create_output(world, events, state_machine, validation):
    expected = state_machine.get_expected_next()

    if isinstance(expected, str):
        expected_state = expected
    elif expected:
        expected_state = expected.value
    else:
        expected_state = None

    return {
        "schema_version": "1.0",
        "frame": {
            "id": world.frame_id,
            "timestamp": world.timestamp
        },
        "digital_twin": {
            "current_state": state_machine.current_state.value,
            "previous_state": (
                state_machine.previous_state.value
                if state_machine.previous_state
                else None
            ),
            "expected_next_state": expected_state,
            "validation": validation
        },
        "people": [
            {
                "id": person.person_id,
                "position": person.position,
                "bbox": person.bbox,
                "activity": person.activity,
                "confidence": person.confidence
            }
            for person in world.people.values()
        ],
        "objects": [
            {
                "id": obj.object_id,
                "type": obj.object_type,
                "position_2d": obj.position_2d,
                "grid_cell": obj.grid_cell,
                "state": obj.state,
                "confidence": obj.confidence
            }
            for obj in world.objects.values()
        ],
        "events": events,
        "environment": world.environment
    }


def create_observation(world, validation):
    return {
        "frame_id": world.frame_id,
        "timestamp": world.timestamp,
        "current_state": validation.get("current_state"),
        "expected": validation.get("expected"),
        "observed": validation.get("observed"),
        "status": validation.get("status"),
        "reason": validation.get("reason")
    }


def print_validation_result(validation):
    status = validation.get("status", "UNKNOWN")

    if status == "VALID":
        print(
            f"[VALID] Expected={validation.get('expected')} "
            f"Observed={validation.get('observed')}"
        )

    elif status == "DEVIATION":
        print(
            f"[DEVIATION] Expected={validation.get('expected')} "
            f"Observed={validation.get('observed')}"
        )
        print(f"[REASON] {validation.get('reason')}")

    elif status == "NO_TRANSITION":
        print(f"[NO TRANSITION] {validation.get('reason')}")

    elif status == "WARNING":
        print(f"[WARNING] {validation.get('reason')}")

    elif status == "ERROR":
        print(f"[ERROR] {validation.get('reason')}")


def process_frame(frame_id):
    print()
    print("-" * 60)
    print(f"PROCESSING FRAME {frame_id}")
    print("-" * 60)

    try:
        yolo = yolo_reader.read_frame(frame_id)
    except FileNotFoundError:
        print(f"[ERROR] YOLO frame {frame_id} not found.")
        return None

    if not yolo_validator.validate(yolo):
        print("[WARNING] Invalid YOLO data.")
        print("[FRAME SKIPPED]")
        return None

    yolo_buffer.add(yolo)

    latest_yolo = yolo_buffer.latest()

    world = world_builder.build(latest_yolo)

    events = event_detector.detect(world)

    world.current_state = (
        state_machine.get_current_state()
    )

    world.previous_state = (
        state_machine.previous_state.value
        if state_machine.previous_state
        else None
    )

    validation = procedure_validator.validate(
        world,
        state_machine
    )

    print_validation_result(validation)

    observation = create_observation(
        world,
        validation
    )

    is_anomaly = (
        validation.get("status") == "DEVIATION"
    )

    observation_store.store(
        observation,
        is_anomaly=is_anomaly
    )

    status = validation.get("status")

    if status == "VALID":
        observed_state = validation.get("observed")

        if observed_state:
            try:
                next_state = TwinState(observed_state)

                state_machine.transition(
                    next_state
                )

            except ValueError:
                print(
                    f"[ERROR] Unknown state: {observed_state}"
                )

    elif status == "DEVIATION":
        print("[PROCEDURE DEVIATION DETECTED]")

    elif status == "WARNING":
        print("[PROCEDURE WARNING]")

    elif status == "ERROR":
        print("[PROCEDURE ERROR]")

    output = create_output(
        world,
        events,
        state_machine,
        validation
    )

    print()
    print(json.dumps(output, indent=2))

    return output


def main():
    print()
    print("=" * 60)
    print("DIGITAL TWIN PROCEDURE VALIDATION SYSTEM")
    print("=" * 60)
    print()
    print("YOLO -> World Model -> State Machine -> Procedure Validator")
    print()

    for frame_id in range(
        START_FRAME,
        END_FRAME + 1
    ):
        process_frame(frame_id)
        time.sleep(FRAME_DELAY)

    print()
    print("=" * 60)
    print("SIMULATION FINISHED")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()