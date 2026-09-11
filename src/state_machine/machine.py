from enum import Enum


class TwinState(Enum):
    IDLE = "IDLE"
    APPROACHING_RACK = "APPROACHING_RACK"
    REACHING_FOR_OBJECT = "REACHING_FOR_OBJECT"
    OBJECT_GRABBED = "OBJECT_GRABBED"
    MOVING_OBJECT = "MOVING_OBJECT"
    OBJECT_PLACED = "OBJECT_PLACED"
    TASK_COMPLETE = "TASK_COMPLETE"


VALID_TRANSITIONS = {
    TwinState.IDLE: {
        TwinState.APPROACHING_RACK
    },

    TwinState.APPROACHING_RACK: {
        TwinState.REACHING_FOR_OBJECT
    },

    TwinState.REACHING_FOR_OBJECT: {
        TwinState.OBJECT_GRABBED
    },

    TwinState.OBJECT_GRABBED: {
        TwinState.MOVING_OBJECT
    },

    TwinState.MOVING_OBJECT: {
        TwinState.OBJECT_PLACED
    },

    TwinState.OBJECT_PLACED: {
        TwinState.TASK_COMPLETE
    },

    TwinState.TASK_COMPLETE: set()
}


class DigitalTwinStateMachine:

    def __init__(self):

        self.current_state = TwinState.IDLE
        self.previous_state = None

    def get_current_state(self):

        return self.current_state.value

    def get_expected_next(self):

        next_states = VALID_TRANSITIONS.get(
            self.current_state,
            set()
        )

        if not next_states:
            return None

        return next(iter(next_states)).value

    def transition(self, new_state):

        if new_state not in VALID_TRANSITIONS[self.current_state]:

            print(
                f"[INVALID TRANSITION] "
                f"{self.current_state.value} -> "
                f"{new_state.value}"
            )

            return False

        self.previous_state = self.current_state
        self.current_state = new_state

        print(
            f"[STATE] "
            f"{self.previous_state.value} -> "
            f"{self.current_state.value}"
        )

        return True