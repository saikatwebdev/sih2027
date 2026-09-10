import json
import time
from pathlib import Path

from src.input.hmr_reader import HMRReader
from src.input.yolo_reader import YOLOReader

from src.validation.validator import JSONValidator

from src.temporal.buffer import TemporalBuffer

from src.fusion.engine import FusionEngine

from src.events.detector import EventDetector

from src.state_machine.machine import (
    DigitalTwinStateMachine
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

HMR_DIR = BASE_DIR / "data" / "hmr"
YOLO_DIR = BASE_DIR / "data" / "yolo"

HMR_SCHEMA = BASE_DIR / "schemas" / "hmr_schema.json"
YOLO_SCHEMA = BASE_DIR / "schemas" / "yolo_schema.json"


# ============================================================
# COMPONENTS
# ============================================================

hmr_reader = HMRReader(HMR_DIR)

yolo_reader = YOLOReader(YOLO_DIR)


hmr_validator = JSONValidator(
    HMR_SCHEMA
)

yolo_validator = JSONValidator(
    YOLO_SCHEMA
)


hmr_buffer = TemporalBuffer(
    max_size=5
)

yolo_buffer = TemporalBuffer(
    max_size=5
)


fusion = FusionEngine()

event_detector = EventDetector()

state_machine = DigitalTwinStateMachine()


# ============================================================
# CONFIGURATION
# ============================================================

START_FRAME = 1

END_FRAME = 7

FRAME_DELAY = 0.5


# ============================================================
# OUTPUT FUNCTION
# ============================================================

def create_output(
    world,
    events,
    state_machine
):

    expected = (
        state_machine.get_expected_next()
    )

    return {

        "schema_version": "1.0",

        "frame": {
            "id": world.frame_id,
            "timestamp": world.timestamp
        },

        "people": [

            {
                "id": person.person_id,

                "activity": person.activity,

                "position": person.position,

                "joints": person.joints,

                "confidence": person.confidence
            }

            for person
            in world.people.values()
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

            for obj
            in world.objects.values()
        ],

        "events": events,

        "digital_twin": {

            "current_state":
                state_machine.current_state.value,

            "previous_state":
                (
                    state_machine.previous_state.value
                    if state_machine.previous_state
                    else None
                ),

            "expected_next_state":
                (
                    expected.value
                    if expected
                    else None
                )
        }
    }


# ============================================================
# MAIN LOOP
# ============================================================

def main():

    print()
    print("=" * 60)
    print("DIGITAL TWIN SIMULATOR")
    print("=" * 60)
    print()

    for frame_id in range(
        START_FRAME,
        END_FRAME + 1
    ):

        print()
        print("-" * 60)
        print(f"PROCESSING FRAME {frame_id}")
        print("-" * 60)


        # ----------------------------------------------------
        # 1. READ HMR
        # ----------------------------------------------------

        try:

            hmr = hmr_reader.read_frame(
                frame_id
            )

        except FileNotFoundError:

            print(
                f"[ERROR] HMR frame {frame_id} "
                "not found."
            )

            continue


        # ----------------------------------------------------
        # 2. READ YOLO
        # ----------------------------------------------------

        try:

            yolo = yolo_reader.read_frame(
                frame_id
            )

        except FileNotFoundError:

            print(
                f"[ERROR] YOLO frame {frame_id} "
                "not found."
            )

            continue


        # ----------------------------------------------------
        # 3. VALIDATE HMR
        # ----------------------------------------------------

        if not hmr_validator.validate(hmr):

            print(
                "[WARNING] Invalid HMR data. "
                "Skipping frame."
            )

            continue


        # ----------------------------------------------------
        # 4. VALIDATE YOLO
        # ----------------------------------------------------

        if not yolo_validator.validate(yolo):

            print(
                "[WARNING] Invalid YOLO data. "
                "Skipping frame."
            )

            continue


        # ----------------------------------------------------
        # 5. ADD TO TEMPORAL BUFFERS
        # ----------------------------------------------------

        hmr_buffer.add(hmr)

        yolo_buffer.add(yolo)


        # ----------------------------------------------------
        # 6. FUSE DATA
        # ----------------------------------------------------

        world = fusion.fuse(

            hmr_buffer.latest(),

            yolo_buffer.latest()
        )


        # ----------------------------------------------------
        # 7. DETECT EVENTS
        # ----------------------------------------------------

        events = event_detector.detect(
            world
        )


        # ----------------------------------------------------
        # 8. UPDATE STATE MACHINE
        # ----------------------------------------------------

        state_machine.update(
            world,
            events
        )


        # ----------------------------------------------------
        # 9. CREATE DIGITAL TWIN OUTPUT
        # ----------------------------------------------------

        output = create_output(

            world,

            events,

            state_machine
        )


        # ----------------------------------------------------
        # 10. DISPLAY OUTPUT
        # ----------------------------------------------------

        print(
            json.dumps(
                output,
                indent=2
            )
        )


        # ----------------------------------------------------
        # 11. SIMULATE REAL-TIME DELAY
        # ----------------------------------------------------

        time.sleep(
            FRAME_DELAY
        )


    print()
    print("=" * 60)
    print("SIMULATION FINISHED")
    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()