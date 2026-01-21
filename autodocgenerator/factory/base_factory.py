from abc import ABC, abstractmethod
from ..engine.models.model import Model, AsyncModel
from ..ui.progress_base import BaseProgress

class BaseModule(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def generate(self, info: dict, model: Model):
        ...




class DocFactory:
    def __init__(self, *modules):
        self.modules: list[BaseModule] = modules

    def generate_doc(self, info: dict, model: Model, progress: BaseProgress):
        output = ""
        progress.create_new_subtask("Generate parts", len(self.modules))
        for module in self.modules:
            module_result = module.generate(info, model)
            output += module_result + "\n\n"
            progress.update_task()
        progress.remove_subtask()

        return output

if __name__ == "__main__":
    DocFactory(BaseModule(), BaseModule())