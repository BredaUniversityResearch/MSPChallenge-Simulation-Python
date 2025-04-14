from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from LayerInfoPropertiesObject import LayerInfoPropertiesObject
from LayerTextInfoObject import LayerTextInfoObject
from EntityTypeValues import EntityTypeValues
from GeometryParameterObject import GeometryParameterObject
from ELayerKPICategory import ELayerKPICategory
from ELayerSpecialEntityType import ELayerSpecialEntityType

class LayerMeta(BaseModel):
    layer_type: Dict[int, EntityTypeValues]  # JSON automatically converts this

    """layer_id: int = 0
    layer_original_id: Optional[str] = None
    layer_depth: str = "0"
    layer_tags: List[str] = Field(default_factory=list)
    layer_name: str = "test_layer"
    layer_geotype: str = "polygon"
    layer_short: str = "Test Layer"
    layer_media: Optional[str] = None
    layer_group: str = ""
    layer_tooltip: str = ""
    layer_sub: str = ""
    layer_icon: str = ""
    layer_info_properties: List[LayerInfoPropertiesObject] = Field(default_factory=list)
    layer_text_info: Optional[LayerTextInfoObject] = None
    # The C# JsonConverterLayerType is not directly needed in Pydantic,
    # but if you need custom conversion you can add a validator.
    layer_type: Dict[int, EntityTypeValues] = Field(default_factory=dict)
    layer_dependencies: List[int] = Field(default_factory=list)
    layer_category: str = "Test Category"
    layer_subcategory: str = "aquaculture"
    layer_kpi_category: ELayerKPICategory = ELayerKPICategory.Miscellaneous
    layer_active: str = "1"
    layer_selectable: bool = True
    layer_editable: bool = True
    layer_toggleable: bool = True
    layer_active_on_start: bool = False
    layer_states: str = ""
    layer_geometry_parameters: List[GeometryParameterObject] = Field(default_factory=list)
    layer_raster: str = ""
    layer_editing_type: str = ""
    layer_special_entity_type: ELayerSpecialEntityType = ELayerSpecialEntityType.Default
    layer_green: int = 0
    layer_filecreationtime: int = -1
    layer_entity_value_max: Optional[float] = None"""
