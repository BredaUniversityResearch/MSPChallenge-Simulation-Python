from pydantic import BaseModel
from typing import Dict
from ETextState import ETextState  # Ensure this enum is defined
from ETextSize import ETextSize    # Ensure this enum is defined

class LayerTextInfoObject(BaseModel):
    property_per_state: Dict[ETextState, str]
    text_color: str
    text_size: ETextSize
    zoom_cutoff: float
    x: float
    y: float
    z: float
