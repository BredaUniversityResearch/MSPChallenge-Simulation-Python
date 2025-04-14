from enum import Enum
from pydantic import BaseModel
from typing import Optional
from EInputFieldContentType import EInputFieldContentType  # Import the corresponding enum

class ContentValidation(str, Enum):
    NONE = "None"
    SHIPPING_WIDTH = "ShippingWidth"
    NUMBER_CABLES = "NumberCables"
    PIT_EXTRACTION_DEPTH = "PitExtractionDepth"

class LayerInfoPropertiesObject(BaseModel):
    property_name: str
    enabled: bool
    editable: bool
    display_name: str
    sprite_name: str
    default_value: str
    policy_type: str
    update_visuals: bool
    update_text: bool
    update_calculation: bool
    content_type: EInputFieldContentType  # Imported enum
    content_validation: ContentValidation
    unit: str
