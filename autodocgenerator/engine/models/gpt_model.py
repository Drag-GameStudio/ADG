from .model import Model, AsyncModel, GROQ_API_KEYS, History
from groq import Groq, AsyncGroq
from ..exceptions import ModelExhaustedException
from ...ui.logging import BaseLogger, InfoLog, ErrorLog, WarningLog
from openai import OpenAI


class AsyncGPTModel(AsyncModel):
    ...

class GPT4oModel(Model):
    def __init__(self, api_key=GROQ_API_KEYS, history = History(), 
                 models_list: list[str] = ["openai/gpt-4o", "openai/gpt-4.1", "openai/gpt-5"], 
                 use_random: bool = True):
        super().__init__(api_key, history, models_list, use_random)

        self.client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=self.api_keys[self.current_key_index],
        )
        self.logger = BaseLogger()


    def generate_answer(self, with_history: bool = True, prompt: list[dict[str, str]] |  None = None) -> str:
        self.logger.log(InfoLog("Generating answer..."))
        if with_history:
            messages = self.history.history
        elif prompt is not None:
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
                    messages=messages, #type: ignore
                    temperature=0.3,
                    top_p=1.0,
                    max_tokens=16384,
                    model=model_name
                )
                break
            except Exception as e:
                print(e)
                self.logger.log(WarningLog(f"Model {model_name} failed with error: {str(e)}. Trying next model..."))
                self.current_key_index = 0 if self.current_key_index + 1 >= len(self.api_keys) else self.current_key_index + 1
                if self.current_key_index == 0:
                    self.current_model_index = 0 if self.current_model_index + 1 >= len(self.regen_models_name) else self.current_model_index + 1
                    
                self.client = OpenAI(
                    base_url="https://models.github.ai/inference",
                    api_key=self.api_keys[self.current_key_index],
                )



        result = chat_completion.choices[0].message.content
        self.logger.log(InfoLog(f"Generated answer with model {model_name}."))
        self.logger.log(InfoLog(f"Answer: {result}", level=2))
        if result is None:
            return ""
        
        return result

class GPTModel(Model):
    def __init__(self, api_key=GROQ_API_KEYS, history = History(), 
                 models_list: list[str] = ["openai/gpt-oss-120b",  "llama-3.3-70b-versatile",  "openai/gpt-oss-safeguard-20b"], 
                 use_random: bool = True):
        super().__init__(api_key, history, models_list, use_random)
        self.client = Groq(api_key=self.api_keys[self.current_key_index])
        self.logger = BaseLogger()


    def generate_answer(self, with_history: bool = True, prompt: list[dict[str, str]] |  None = None) -> str:
        self.logger.log(InfoLog("Generating answer..."))
        if with_history:
            messages = self.history.history
        elif prompt is not None:
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
                    messages=messages, #type: ignore
                    model=model_name,

                )
                break
            except Exception as e:
                print(e)
                self.logger.log(WarningLog(f"Model {model_name} failed with error: {str(e)}. Trying next model..."))
                self.current_key_index = 0 if self.current_key_index + 1 >= len(self.api_keys) else self.current_key_index + 1
                if self.current_key_index == 0:
                    self.current_model_index = 0 if self.current_model_index + 1 >= len(self.regen_models_name) else self.current_model_index + 1
                    
                self.client = Groq(api_key=self.api_keys[self.current_key_index])




        result = chat_completion.choices[0].message.content
        self.logger.log(InfoLog(f"Generated answer with model {model_name}."))
        self.logger.log(InfoLog(f"Answer: {result}", level=2))
        if result is None:
            return ""
        
        return result