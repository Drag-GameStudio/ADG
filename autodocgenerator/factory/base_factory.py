from abc import ABC, abstractmethod
from ..engine.models.model import Model, AsyncModel
from ..ui.progress_base import BaseProgress
from ..ui.logging import BaseLogger, InfoLog, ErrorLog, WarningLog
from ..schema.doc_schema import DocContent, DocHeadSchema
from ..postprocessor.sorting import split_text_by_anchors

class BaseModule(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def generate(self, info: dict, model: Model):
        ...


class DocFactory:
    def __init__(self, *modules, with_splited: bool = True):
        self.modules: list[BaseModule] = modules # type: ignore
        self.logger = BaseLogger()
        self.with_splited = with_splited

    def generate_doc(self, info: dict, model: Model, progress: BaseProgress) -> DocHeadSchema:
        doc_head = DocHeadSchema()
        progress.create_new_subtask("Generate parts", len(self.modules))
        for i, module in enumerate(self.modules):
            module_result = module.generate(info, model)
            if self.with_splited:
                splited_result = split_text_by_anchors(module_result)
                for el in splited_result:
                    doc_head.add_parts(el, DocContent(content=splited_result[el]))
            else:
                task_name = f"{module.__class__.__name__}_{i}"
                doc_head.add_parts(task_name, DocContent(content=module_result))

            self.logger.log(InfoLog(f"Module {module.__class__.__name__} generated its part of the documentation."))
            self.logger.log(InfoLog(f"Module Output: {module_result}", level=2))
            progress.update_task()
        progress.remove_subtask()

        return doc_head

