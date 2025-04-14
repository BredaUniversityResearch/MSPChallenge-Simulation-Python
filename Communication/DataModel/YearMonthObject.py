from pydantic import BaseModel

class YearMonthObject(BaseModel):
    year: int = 0
    month_of_year: int
