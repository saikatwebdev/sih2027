from enum import Enum


class TwinState(Enum):

    IDLE = "IDLE"

    APPROACHING_RACK = (
        "APPROACHING_RACK"
    )

    REACHING_FOR_OBJECT = (
        "REACHING_FOR_OBJECT"
    )

    OBJECT_GRABBED = (
        "OBJECT_GRABBED"
    )

    MOVING_OBJECT = (
        "MOVING_OBJECT"
    )

    OBJECT_PLACED = (
        "OBJECT_PLACED"
    )

    TASK_COMPLETE = (
        "TASK_COMPLETE"
    )


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

        self.current_state = (
            TwinState.IDLE
        )

        self.previous_state = None


    def can_transition(
        self,
        new_state
    ):

        return new_state in (
            VALID_TRANSITIONS.get(
                self.current_state,
                set()
            )
        )


    def transition(
        self,
        new_state
    ):

        if not self.can_transition(
            new_state
        ):

            print(
                f"[INVALID TRANSITION] "
                f"{self.current_state.value} "
                f"-> "
                f"{new_state.value}"
            )

            return False


        self.previous_state = (
            self.current_state
        )

        self.current_state = new_state

        print(
            f"[STATE] "
            f"{self.previous_state.value} "
            f"-> "
            f"{self.current_state.value}"
        )

        return True


    def update(
        self,
        world,
        events
    ):

        person = next(
            iter(world.people.values()),
            None
        )


        if person is None:

            return self.current_state


        activity = person.activity


        object_moved = any(

            event["type"]
            == "OBJECT_MOVED"

            for event in events
        )


        # ====================================================
        # STATE LOGIC
        # ====================================================

        if (
            self.current_state
            == TwinState.IDLE
        ):

            if activity == "WALKING":

                self.transition(
                    TwinState.APPROACHING_RACK
                )


        elif (
            self.current_state
            == TwinState.APPROACHING_RACK
        ):

            if activity == "REACHING":

                self.transition(
                    TwinState.REACHING_FOR_OBJECT
                )


        elif (
            self.current_state
            == TwinState.REACHING_FOR_OBJECT
        ):

            if activity == "GRABBING":

                self.transition(
                    TwinState.OBJECT_GRABBED
                )


        elif (
            self.current_state
            == TwinState.OBJECT_GRABBED
        ):

            if activity == "MOVING_OBJECT":

                self.transition(
                    TwinState.MOVING_OBJECT
                )


        elif (
            self.current_state
            == TwinState.MOVING_OBJECT
        ):

            if activity == "PLACING":

                self.transition(
                    TwinState.OBJECT_PLACED
                )


        elif (
            self.current_state
            == TwinState.OBJECT_PLACED
        ):

            if activity == "IDLE":

                self.transition(
                    TwinState.TASK_COMPLETE
                )


        return self.current_state


    def get_expected_next(self):

        expected = {

            TwinState.IDLE:
                TwinState.APPROACHING_RACK,

            TwinState.APPROACHING_RACK:
                TwinState.REACHING_FOR_OBJECT,

            TwinState.REACHING_FOR_OBJECT:
                TwinState.OBJECT_GRABBED,

            TwinState.OBJECT_GRABBED:
                TwinState.MOVING_OBJECT,

            TwinState.MOVING_OBJECT:
                TwinState.OBJECT_PLACED,

            TwinState.OBJECT_PLACED:
                TwinState.TASK_COMPLETE,

            TwinState.TASK_COMPLETE:
                None
        }

        return expected[
            self.current_state
        ]