from pydantic import BaseModel

class GeometryParameterObject(BaseModel):
    meta_name: str
    display_name: str
    sprite_name: str
    update_visuals: int
    