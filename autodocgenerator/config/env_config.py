from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict, BaseSettings
from typing import List, Any

class EnvConfig(BaseSettings):
    models_api_keys: str | List[str] = Field(..., alias="MODELS_API_KEYS")
    
    type_of_model: str = Field("git", alias="TYPE_OF_MODEL")
    
    google_embedding_api_key: str = Field("", alias="GOOGLE_EMBEDDING_API_KEY")
    github_event_name: str = Field("", alias="GITHUB_EVENT_NAME")
    output_github_file: str = Field("", alias="GITHUB_OUTPUT")

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore",
        env_file_encoding="utf-8",
        populate_by_name=True
    )

    @field_validator("models_api_keys", mode="before")
    @classmethod
    def split_keys(cls, v):
        if isinstance(v, str):
            keys = [k.strip() for k in v.split(",") if k.strip()]
            if not keys:
                raise ValueError("API_KEY is not set in environment variables.")
            return keys
        return v

    @field_validator("type_of_model")
    @classmethod
    def to_lower(cls, v):
        return v.lower()


env_config = EnvConfig()
print(env_config)