class ProcedureValidator:

    def validate(self, world, state_machine):

        current_state = (
            state_machine.get_current_state()
        )

        expected_state = (
            state_machine.get_expected_next()
        )

        person = next(
            iter(world.people.values()),
            None
        )

        # ====================================================
        # NO PERSON
        # ====================================================

        if person is None:

            return {
                "status": "ERROR",
                "reason": "NO_PERSON_DETECTED",

                "current_state":
                    current_state,

                "expected":
                    expected_state,

                "observed":
                    None
            }


        observed_activity = person.activity


        # ====================================================
        # ACTIVITY -> PROCEDURE STATE
        # ====================================================

        activity_to_state = {

            "WALKING":
                "APPROACHING_RACK",

            "REACHING":
                "REACHING_FOR_OBJECT",

            "GRABBING":
                "OBJECT_GRABBED",

            "MOVING_OBJECT":
                "MOVING_OBJECT",

            "PLACING":
                "OBJECT_PLACED"
        }


        observed_state = (
            activity_to_state.get(
                observed_activity
            )
        )


        # ====================================================
        # SPECIAL CASE: IDLE
        # ====================================================
        #
        # IDLE does NOT automatically mean TASK_COMPLETE.
        #
        # IDLE at the beginning:
        #
        #       IDLE
        #        ↓
        #    WALKING
        #
        # IDLE after OBJECT_PLACED:
        #
        #       OBJECT_PLACED
        #             ↓
        #           IDLE
        #             ↓
        #       TASK_COMPLETE
        #
        # ====================================================

        if observed_activity == "IDLE":

            if (
                current_state == "OBJECT_PLACED"
                and expected_state == "TASK_COMPLETE"
            ):

                observed_state = "TASK_COMPLETE"

            else:

                return {
                    "status": "NO_TRANSITION",

                    "reason":
                        "IDLE_WITHOUT_COMPLETION",

                    "current_state":
                        current_state,

                    "expected":
                        expected_state,

                    "observed":
                        "IDLE"
                }


        # ====================================================
        # UNKNOWN ACTIVITY
        # ====================================================

        if observed_state is None:

            return {
                "status": "WARNING",

                "reason":
                    "UNKNOWN_ACTIVITY",

                "current_state":
                    current_state,

                "expected":
                    expected_state,

                "observed":
                    observed_activity
            }


        # ====================================================
        # EXPECTED STATE
        # ====================================================

        if expected_state == observed_state:

            return {
                "status": "VALID",

                "reason":
                    "EXPECTED_ACTIVITY",

                "current_state":
                    current_state,

                "expected":
                    expected_state,

                "observed":
                    observed_state
            }


        # ====================================================
        # PROCEDURE DEVIATION
        # ====================================================

        return {
            "status": "DEVIATION",

            "reason":
                "UNEXPECTED_ACTIVITY",

            "current_state":
                current_state,

            "expected":
                expected_state,

            "observed":
                observed_state
        }