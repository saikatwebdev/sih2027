import json
from pathlib import Path

from jsonschema import validate
from jsonschema.exceptions import ValidationError


class JSONValidator:

    def __init__(self, schema_path):

        schema_path = Path(schema_path)

        with open(schema_path, "r") as file:
            self.schema = json.load(file)


    def validate(self, data):

        try:

            validate(
                instance=data,
                schema=self.schema
            )

            return True

        except ValidationError as error:

            print(
                f"[VALIDATION ERROR] {error.message}"
            )

            return False