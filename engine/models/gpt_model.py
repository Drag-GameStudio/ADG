from .model import Model, AsyncModel, API_KEY
from groq import Groq, AsyncGroq
from ..config.config import MODELS_NAME



class AsyncGPTModel(AsyncModel):
    def __init__(self, api_key=API_KEY):
        super().__init__(api_key)
        self.client = AsyncGroq(api_key=self.api_key)

    async def generate_answer(self, with_history: bool = True, prompt: str = None) -> str:
        
        if with_history:
            messages = self.history.history
        else:
            messages = prompt
        
        chat_completion = None

        for model_name in MODELS_NAME:
            try:
                chat_completion = await self.client.chat.completions.create(
                    messages=messages,
                    model=model_name
                )
                break
            except Exception as e:
                print(e)
                pass

        if chat_completion is None:
            raise Exception("all models do not work")

        return chat_completion.choices[0].message.content

class GPTModel(Model):
    def __init__(self, api_key=API_KEY):
        super().__init__(api_key)
        self.client = Groq(api_key=self.api_key)

    def generate_answer(self, with_history: bool = True, prompt: str = None) -> str:
        
        if with_history:
            messages = self.history.history
        else:
            messages = prompt
        
        chat_completion = None

        models_del = []

        for model_name in MODELS_NAME:
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model=model_name
                )
                break
            except Exception as e:
                print(e)
                models_del.append(model_name)
                pass

        for el in models_del:
            MODELS_NAME.remove(el)

        if chat_completion is None:
            raise Exception("all models do not work")

        return chat_completion.choices[0].message.content