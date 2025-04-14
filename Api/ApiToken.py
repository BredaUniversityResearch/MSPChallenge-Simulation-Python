from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, root_validator
import json


class ApiToken(BaseModel):
    token: str
    valid_until: datetime

    @root_validator(pre=True)
    def handle_stringified_json(cls, values):
        if isinstance(values, str):
            try:
                return json.loads(values)
            except json.JSONDecodeError as e:
                raise ValueError(f"Could not parse ApiToken from string: {e}")
        return values