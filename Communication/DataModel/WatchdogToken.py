from pydantic import BaseModel

class WatchdogToken(BaseModel):
    watchdog_token: str
