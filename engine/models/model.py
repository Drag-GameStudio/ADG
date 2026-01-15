from ..config.config import BASE_SYSTEM_TEXT, API_KEY, MODELS_NAME
import random

class History:
    def __init__(self, system_prompt: str = BASE_SYSTEM_TEXT):
        self.history = []
        if system_prompt is not None:
            self.add_to_history("system", system_prompt)

    def add_to_history(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content
        })


class ParentModel():
    def __init__(self, api_key=API_KEY, history: History = History()):
        self.history = history
        self.api_key = api_key

        self.current_model_index = 0
        models_copy = MODELS_NAME.copy()
        random.shuffle(models_copy)
        self.regen_models_name = models_copy


class Model(ParentModel):

    def generate_answer(self, with_history: bool = True, prompt: str = None) -> str:
        return "answer"
    
    def get_answer_without_history(self, prompt: list[dict[str, str]]) -> str:
        return self.generate_answer(with_history=False, prompt=prompt)

    def get_answer(self, prompt: str) -> str:
        self.history.add_to_history("user", prompt)
        model_answer = self.generate_answer()
        self.history.add_to_history("assistant", model_answer)
        return model_answer
    
class AsyncModel(ParentModel):

    async def generate_answer(self, with_history: bool = True, prompt: str = None) -> str:
        return "answer"
    
    async def get_answer_without_history(self, prompt: list[dict[str, str]]) -> str:
        return await self.generate_answer(with_history=False, prompt=prompt)

    async def get_answer(self, prompt: str) -> str:
        self.history.add_to_history("user", prompt)
        model_answer = await self.generate_answer()
        self.history.add_to_history("assistant", model_answer)
        return model_answer


