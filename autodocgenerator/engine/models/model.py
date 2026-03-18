from ..config.config import BASE_SYSTEM_TEXT, GROQ_API_KEYS
import random
from typing import Union, Any, Coroutine
from abc import abstractmethod, ABC

class History:
    def __init__(self, system_prompt: str = BASE_SYSTEM_TEXT):
        self.history: list[dict[str, str]] = []
        if system_prompt is not None:
            self.add_to_history("system", system_prompt)

    def add_to_history(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content
        })


class ParentModel(ABC):
    def __init__(self, api_key=GROQ_API_KEYS, history: History = History(), 
                 models_list: list[str] = ["openai/gpt-oss-120b",  "llama-3.3-70b-versatile",  "openai/gpt-oss-safeguard-20b"],
                 use_random: bool = True):
        self.history = history
        self.api_keys = api_key

        self.current_model_index = 0
        self.current_key_index = 0

        
        models_list = models_list.copy()
        if use_random:
            random.shuffle(models_list)
        self.regen_models_name = models_list

    @abstractmethod
    def generate_answer(self, with_history: bool = True, prompt: list[dict[str, str]] | None = None) -> Union[str, Coroutine[Any, Any, str]]:
        return ""
    
    @abstractmethod
    def get_answer_without_history(self, prompt: list[dict[str, str]]) -> Union[str, Coroutine[Any, Any, str]]:
        return ""
    
    @abstractmethod
    def get_answer(self, prompt: str) -> Union[str, Coroutine[Any, Any, str]]:
        return ""



class Model(ParentModel):

    def generate_answer(self, with_history: bool = True, prompt: list[dict[str, str]]  |  None = None) -> str:
        return "answer"
    
    def get_answer_without_history(self, prompt: list[dict[str, str]]) -> str:
        return self.generate_answer(with_history=False, prompt=prompt)

    def get_answer(self, prompt: str) -> str:
        self.history.add_to_history("user", prompt)
        model_answer = self.generate_answer()
        self.history.add_to_history("assistant", model_answer)
        return model_answer
    
class AsyncModel(ParentModel):

    async def generate_answer(self, with_history: bool = True, prompt: list[dict[str, str]] | None = None) -> str:
        return "answer"
    
    async def get_answer_without_history(self, prompt: list[dict[str, str]]) -> str:
        return await self.generate_answer(with_history=False, prompt=prompt)

    async def get_answer(self, prompt: str) -> str:
        self.history.add_to_history("user", prompt)
        model_answer = await self.generate_answer()
        self.history.add_to_history("assistant", model_answer)
        return model_answer


