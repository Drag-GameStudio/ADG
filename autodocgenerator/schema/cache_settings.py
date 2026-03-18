from pydantic import BaseModel

class CacheSettings(BaseModel):
    last_commit: str = ""