from pydantic import BaseModel
from typing import Optional

# C# records are immutable data classes.
# Pydantic provides immutability by setting model_config = {"frozen": True} (if needed).

class SetMonthRequest(BaseModel):
    game_session_token: str
    month: int
    
    class Config:
        frozen = True  # Makes the model immutable, similar to a C# record