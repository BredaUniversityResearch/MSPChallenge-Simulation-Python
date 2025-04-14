from pydantic import BaseModel

class SimulationDefinition(BaseModel):
    name: str
    version: str

    class Config:
        frozen = True  # Makes the model immutable, similar to a C# record
