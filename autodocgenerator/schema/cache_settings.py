from pydantic import BaseModel, Field
from .doc_schema import DocInfoSchema

class CacheSettings(BaseModel):
    last_commit: str = ""
    doc: DocInfoSchema = Field(default_factory=DocInfoSchema)