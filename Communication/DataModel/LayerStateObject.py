from pydantic import BaseModel

class LayerStateObject(BaseModel):
    state: str
    time: int
