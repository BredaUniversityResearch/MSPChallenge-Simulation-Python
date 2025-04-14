from pydantic import BaseModel

# C# records are immutable data classes.
# Pydantic provides immutability by setting model_config = {"frozen": True} (if needed).

class GameSessionInfo(BaseModel):
    id: int
    name: str
    region: str
    config_version: int
    config_version_message: str
    config_file_name: str
    config_file_description: str
    config_file_metadata_date_modified: str
    config_file_metadata_model_hash: str
    config_file_metadata_editor_version: str
    config_file_metadata_config_version: str
    server_version: str

    class Config:
        frozen = True  # Makes the model immutable, similar to a C# record