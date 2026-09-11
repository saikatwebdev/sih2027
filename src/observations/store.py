import json
from pathlib import Path
from datetime import datetime


class ObservationStore:

    def __init__(
        self,
        observation_file="data/observations.json",
        anomaly_file="data/anomaly_observations.json"
    ):

        self.observation_file = Path(
            observation_file
        )

        self.anomaly_file = Path(
            anomaly_file
        )

        # ----------------------------------------------------
        # Create parent directories
        # ----------------------------------------------------

        self.observation_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.anomaly_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------------------
        # Create files if they don't exist
        # ----------------------------------------------------

        self._initialize_file(
            self.observation_file
        )

        self._initialize_file(
            self.anomaly_file
        )


    # ========================================================
    # INITIALIZE FILE
    # ========================================================

    def _initialize_file(self, filepath):

        if not filepath.exists():

            filepath.write_text(
                "[]",
                encoding="utf-8"
            )


    # ========================================================
    # LOAD JSON
    # ========================================================

    def _load(self, filepath):

        try:

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

                return []

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            return []


    # ========================================================
    # SAVE JSON
    # ========================================================

    def _save(self, filepath, data):

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )


    # ========================================================
    # STORE OBSERVATION
    # ========================================================

    def store_observation(self, observation):

        observation = observation.copy()

        observation["stored_at"] = (
            datetime.now().isoformat()
        )

        observations = self._load(
            self.observation_file
        )

        observations.append(
            observation
        )

        self._save(
            self.observation_file,
            observations
        )

        print(
            "[OBSERVATION STORED]"
        )


    # ========================================================
    # STORE ANOMALY
    # ========================================================

    def store_anomaly(self, observation):

        anomaly = observation.copy()

        anomaly["stored_at"] = (
            datetime.now().isoformat()
        )

        anomalies = self._load(
            self.anomaly_file
        )

        anomalies.append(
            anomaly
        )

        self._save(
            self.anomaly_file,
            anomalies
        )

        print(
            "[ANOMALY STORED]"
        )


    # ========================================================
    # STORE BOTH
    # ========================================================

    def store(
        self,
        observation,
        is_anomaly=False
    ):

        # Every observation goes here
        self.store_observation(
            observation
        )

        # Only deviations go here
        if is_anomaly:

            self.store_anomaly(
                observation
            )