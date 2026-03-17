from pydantic import BaseModel, Field

class DocContent(BaseModel):
    content: str

class DocHeadSchema(BaseModel):
    content_orders: list[str] = []
    parts: dict[str, DocContent] = {}

class DocInfoSchema(BaseModel):
    global_info: str | None = None
    code_mix: str | None = None
    doc: DocHeadSchema = Field(default_factory=DocHeadSchema)

