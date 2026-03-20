from pydantic import BaseModel, Field
from .doc_schema import DocInfoSchema

class CacheSettings(BaseModel):
    last_commit: str = ""
    doc: DocInfoSchema = Field(default_factory=DocInfoSchema)


class CheckGitStatusResultSchema(BaseModel):
    need_to_remake: bool
    remake_gl_file: bool
