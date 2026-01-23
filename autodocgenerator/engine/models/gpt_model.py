from .model import Model, AsyncModel, API_KEY, History
from groq import Groq, AsyncGroq
from ..exceptions import ModelExhaustedException

class AsyncGPTModel(AsyncModel):
    def __init__(self, api_key=API_KEY, history = History()):
        super().__init__(api_key, history)
        self.client = AsyncGroq(api_key=self.api_key)

    async def generate_answer(self, with_history: bool = True, prompt: str = None) -> str:
        
        if with_history:
            messages = self.history.history
        else:
            messages = prompt
        
        chat_completion = None
        
        while True:
            if len(self.regen_models_name) <= 0:
                raise ModelExhaustedException("No models available for use.")
            
            model_name = self.regen_models_name[self.current_model_index]
            try:
                chat_completion = await self.client.chat.completions.create(
                    messages=messages,
                    model=model_name,
                )
                break
            except Exception as e:
                print(e)
                self.current_model_index = 0 if self.current_model_index + 1 >= len(self.regen_models_name) else self.current_model_index + 1
                    


        return chat_completion.choices[0].message.content

class GPTModel(Model):
    def __init__(self, api_key=API_KEY, history = History()):
        super().__init__(api_key, history)
        self.client = Groq(api_key=self.api_key)

    def generate_answer(self, with_history: bool = True, prompt: str = None) -> str:
        
        if with_history:
            messages = self.history.history
        else:
            messages = prompt
        
        chat_completion = None

        while True:
            if len(self.regen_models_name) <= 0:
                raise ModelExhaustedException("No models available for use.")
            
            model_name = self.regen_models_name[self.current_model_index]
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model=model_name,

                )
                break
            except Exception as e:
                print(e)
                self.current_model_index = 0 if self.current_model_index + 1 >= len(self.regen_models_name) else self.current_model_index + 1


        return chat_completion.choices[0].message.content