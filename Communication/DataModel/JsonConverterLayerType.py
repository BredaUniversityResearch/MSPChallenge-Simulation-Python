"""
In Python, Pydantic and FastAPI handle JSON conversion automatically. However, we need a custom Pydantic JSON validator 
to handle both lists and dictionaries for EntityTypeValues.

"""

from pydantic import BaseModel, field_validator
from typing import List, Dict, Union
import json

from EntityTypeValues import EntityTypeValues  

class LayerTypeConverter(BaseModel):
    layer_type: Union[Dict[int, EntityTypeValues], List[EntityTypeValues]]

    @field_validator("layer_type", mode="before")
    @classmethod
    def convert_layer_type(cls, value):
        """Convert JSON input into the correct format."""
        if isinstance(value, list):  # If it's a List, convert it to Dict
            return {i: v for i, v in enumerate(value)}  # Convert list to {index: EntityTypeValues}
        elif isinstance(value, dict):  # If it's already a Dict, return it as is
            return value
        else:
            raise ValueError(f"Unexpected JSON format for layer_type: {json.dumps(value)}")

