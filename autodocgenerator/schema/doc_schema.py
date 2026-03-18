from pydantic import BaseModel, Field
import random
from ..postprocessor.embedding import Embedding
from typing import Any

class DocContent(BaseModel):
    content: str
    embedding_vector: list | None = None

    def init_embedding(self, embedding_model: Embedding):
        self.embedding_vector = embedding_model.get_vector(self.content)

class DocHeadSchema(BaseModel):
    content_orders: list[str] = []
    parts: dict[str, DocContent] = {}

    def add_parts(self, name, content: DocContent):
        iter_c = 0
        while name in self.content_orders:
            name = f"{name}_{iter_c}"
            iter_c += 1

        self.content_orders.append(name)
        self.parts[name] = content

    def get_full_doc(self, split_el: str = "\n") -> str:
        output_doc: str = ""
        for el in self.content_orders:
            output_doc += self.parts[el].content + split_el

        return output_doc
    
    def __add__(self, other: "DocHeadSchema") -> "DocHeadSchema":
        if not isinstance(other, DocHeadSchema):
            return NotImplemented
        
        for el in other.content_orders:
            self.add_parts(el, other.parts[el])
        return self

class DocInfoSchema(BaseModel):
    global_info: str = ""
    code_mix: str = ""
    doc: DocHeadSchema = Field(default_factory=DocHeadSchema)

