from pydantic import BaseModel

class KPI(BaseModel):
    name: str  # Name of the KPI
    month: int  # Month this KPI applies to
    value: float  # The value of this KPI
    type: str  # KPI category: 'ECOLOGY', 'ENERGY', 'SHIPPING', 'EXTERNAL'
    unit: str  # The unit of the KPI
    country: int = -1  # Country ID (-1 means no country associated)
