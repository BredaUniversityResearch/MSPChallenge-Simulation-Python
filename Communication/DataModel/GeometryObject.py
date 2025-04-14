from pydantic import BaseModel
from typing import List, Optional

# ✅ C# properties convert to Pydantic fields using snake_case.

class GeometryObject(BaseModel):
    id: int
    geometry: List[List[float]]
    subtractive: Optional[List["GeometryObject"]] = None  # Recursive reference
    active: int
    persistent: int
    mspid: str

