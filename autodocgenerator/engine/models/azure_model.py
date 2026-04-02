from .model import Model, AsyncModel,  History
from ..exceptions import ModelExhaustedException
from ...ui.logging import BaseLogger, InfoLog, ErrorLog, WarningLog
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, ChatRequestMessage
from azure.core.credentials import AzureKeyCredential
import re


class AzureModel(Model):
    def __init__(self, api_key, history = History(), 
                 models_list: list[str] = ["deepseek/DeepSeek-V3-0324"], 
                 use_random: bool = True):
        super().__init__(api_key, history, models_list, use_random)
        self.client = ChatCompletionsClient(
            endpoint="https://models.github.ai/inference",
            credential=AzureKeyCredential(self.api_keys[self.current_key_index]),
        )
        self.logger = BaseLogger()

    def _clean_deepseek_response(self, text: str) -> str:
        """Удаляет блок <think>...</think> и лишние пробелы."""
        cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        return cleaned_text.strip()

    def _parse_prompt(self, data: list[dict[str, str]]) -> list[UserMessage | SystemMessage]:
        result: list[UserMessage | SystemMessage] = []
        for el in data:
            if el["role"] == "system":
                result.append(SystemMessage(el["content"]))
                continue

            if el["role"] == "user":
                result.append(UserMessage(el["content"]))
                continue

        return result


    def generate_answer(self, with_history: bool = True, prompt: list[dict[str, str]] |  None = None) -> str:
        self.logger.log(InfoLog("Generating answer..."))
        if with_history:
            messages = self.history.history
        elif prompt is not None:
            messages = prompt
        
        chat_completion = None
        model_name = None
        
        parse_messages: list[UserMessage | SystemMessage] = self._parse_prompt(messages)
        while True:
            if len(self.regen_models_name) <= 0:
                self.logger.log(ErrorLog("No models available for use."))
                raise ModelExhaustedException("No models available for use.")
            
            model_name = self.regen_models_name[self.current_model_index]
            try:
                response = self.client.complete(
                    messages=parse_messages, #type: ignore
                    temperature=0.2,
                    top_p=1.0,
                    max_tokens=10000,
                    model=model_name
                )

                break
            except Exception as e:
                print(e)
                self.logger.log(WarningLog(f"Model {model_name} failed with error: {str(e)}. Trying next model..."))
                self.current_key_index = 0 if self.current_key_index + 1 >= len(self.api_keys) else self.current_key_index + 1
                if self.current_key_index == 0:
                    self.current_model_index = 0 if self.current_model_index + 1 >= len(self.regen_models_name) else self.current_model_index + 1
                    
                self.client = ChatCompletionsClient(
                    endpoint="https://models.github.ai/inference",
                    credential=AzureKeyCredential(self.api_keys[self.current_key_index]),
                )




        result = self._clean_deepseek_response(response.choices[0].message.content)
        self.logger.log(InfoLog(f"Generated answer with model {model_name}."))
        self.logger.log(InfoLog(f"Answer: {result}", level=2))
        if result is None:
            return ""
        
        return result