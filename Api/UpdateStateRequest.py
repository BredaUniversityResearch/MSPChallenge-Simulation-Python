from pydantic import BaseModel
from Api.GameSessionInfo import GameSessionInfo
from typing import Optional
from Api.ApiToken import ApiToken  # ✅


# C# records are immutable data classes.
# Pydantic provides immutability by setting model_config = {"frozen": True} (if needed).

class UpdateStateRequest(BaseModel):
    game_session_api: str
    game_session_token: str
    game_state: str
    required_simulations: str
    api_access_token: ApiToken
    api_access_renew_token: ApiToken
    month: int
    game_session_info: Optional[GameSessionInfo] = None