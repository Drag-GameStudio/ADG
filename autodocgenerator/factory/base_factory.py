from abc import ABC, abstractmethod

class BaseModule(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def generate(self, info: dict):
        ...




class DocFactory:
    def __init__(self, *modules):
        self.modules: list[BaseModule] = modules

    def generate_doc(self, info: dict):
        output = ""
        for module in self.modules:
            module_result = module.generate(info)
            output += module_result + "\n\n"

        return output

if __name__ == "__main__":
    DocFactory(BaseModule(), BaseModule())