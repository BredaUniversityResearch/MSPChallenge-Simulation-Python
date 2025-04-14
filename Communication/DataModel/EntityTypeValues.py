from pydantic import BaseModel
from ELinePatternType import ELinePatternType
from EApprovalType import EApprovalType
from typing import Optional

# ✅ C# properties convert to Pydantic fields using snake_case.

class EntityTypeValues(BaseModel):
    display_name: str
    display_polygon: bool
    polygon_color: Optional[str] = None
    polygon_pattern_name: Optional[str] = None
    inner_glow_enabled: bool
    inner_glow_radius: int
    inner_glow_iterations: int
    inner_glow_multiplier: float
    inner_glow_pixel_size: float
    display_lines: bool
    line_color: str
    line_width: float = 1.0  # ✅ Default value from C#
    line_icon: Optional[str] = None  
    line_pattern_type: ELinePatternType
    display_points: bool
    point_color: str
    point_size: float
    point_sprite_name: Optional[str] = None
    description: str
    capacity: int   # ✅ C# `long` → Python `int`
    investment_cost: float
    availability: int
    value: int
    media: Optional[str] = None
    approval: EApprovalType

