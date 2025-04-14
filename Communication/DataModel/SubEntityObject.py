from pydantic import BaseModel
from typing import List, Dict
from GeometryObject import GeometryObject  # Ensure this is defined

class SubEntityObject(BaseModel):
    id: int
    geometry: List[List[float]]
    subtractive: List[GeometryObject]
    active: int
    persistent: int
    mspid: str
    country: int = -1
    type: str
    data: Dict[str, str]
