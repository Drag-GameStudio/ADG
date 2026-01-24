from .model import Model, AsyncModel, API_KEY, History
from groq import Groq, AsyncGroq
from ..exceptions import ModelExhaustedException
from ...ui.logging import BaseLogger, InfoLog, ErrorLog, WarningLog

class AsyncGPTModel(AsyncModel):
    def __init__(self, api_key=API_KEY, history = History(), use_random: bool = True):
        super().__init__(api_key, history, use_random)
        self.client = AsyncGroq(api_key=self.api_key)
        self.logger = BaseLogger()

    async def generate_answer(self, with_history: bool = True, prompt: str = None) -> str:
        
        self.logger.log(InfoLog("Generating answer asynchronously..."))

        if with_history:
            messages = self.history.history
        else:
            messages = prompt
        
        chat_completion = None
        model_name = None
        while True:
            if len(self.regen_models_name) <= 0:
                self.logger.log(ErrorLog("No models available for use."))
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
                self.logger.log(WarningLog(f"Model {model_name} failed with error: {str(e)}. Trying next model..."))
                self.current_model_index = 0 if self.current_model_index + 1 >= len(self.regen_models_name) else self.current_model_index + 1
                    


        result = chat_completion.choices[0].message.content
        self.logger.log(InfoLog(f"Generated answer with model {model_name}."))
        self.logger.log(InfoLog(f"Answer: {result}", level=2))

        return result

class GPTModel(Model):
    def __init__(self, api_key=API_KEY, history = History(), use_random: bool = True):
        super().__init__(api_key, history, use_random)
        self.client = Groq(api_key=self.api_key)
        self.logger = BaseLogger()


    def generate_answer(self, with_history: bool = True, prompt: str = None) -> str:
        self.logger.log(InfoLog("Generating answer..."))
        if with_history:
            messages = self.history.history
        else:
            messages = prompt
        
        chat_completion = None
        model_name = None

        while True:
            if len(self.regen_models_name) <= 0:
                self.logger.log(ErrorLog("No models available for use."))
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
                self.logger.log(WarningLog(f"Model {model_name} failed with error: {str(e)}. Trying next model..."))
                self.current_model_index = 0 if self.current_model_index + 1 >= len(self.regen_models_name) else self.current_model_index + 1


        result = chat_completion.choices[0].message.content
        self.logger.log(InfoLog(f"Generated answer with model {model_name}."))
        self.logger.log(InfoLog(f"Answer: {result}", level=2))
        return result