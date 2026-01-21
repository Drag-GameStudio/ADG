from ..base_factory import BaseModule
from ...engine.models.model import Model
from ...preprocessor.postprocess import generete_custom_discription
from ...preprocessor.spliter import split_data

class CustomModule(BaseModule):

    def __init__(self, discription: str):
        super().__init__()
        self.discription = discription  

    def generate(self, info: dict, model: Model):
        result = generete_custom_discription(split_data(info.get("code_mix"), max_symbols=7000), model, self.discription, info.get("language"))
        return result