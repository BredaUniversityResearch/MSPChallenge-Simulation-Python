from pydantic import BaseModel

class RequestTokenResult(BaseModel):
    api_access_token: str
    api_refresh_token: str
