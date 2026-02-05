from ..engine.models.gpt_model import GPTModel, AsyncGPTModel, Model, AsyncModel
from ..engine.config.config import get_BASE_COMPRESS_TEXT
import math
import asyncio
from ..ui.progress_base import BaseProgress
from .settings import ProjectSettings




def compress(data: str, project_settings: ProjectSettings, model: Model, compress_power) -> str:
    prompt = [
        {
            "role": "system",
            "content": project_settings.prompt
        },
        {
            "role": "system",
            "content": get_BASE_COMPRESS_TEXT(len(data), compress_power)
        },
        {
            "role": "user",
            "content": data
        }
    ]
    answer = model.get_answer_without_history(prompt=prompt)

    return answer


def compress_and_compare(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) -> list:
    compress_and_compare_data = ["" for i in range(math.ceil(len(data) / compress_power))]
    progress_bar.create_new_subtask(f"Compare all files", len(data))
    for i, el in enumerate(data):
        curr_index = i // compress_power
        compress_and_compare_data[curr_index] += compress(el, project_settings, model, compress_power) + "\n"
        progress_bar.update_task()

    progress_bar.remove_subtask()

    return compress_and_compare_data



def compress_to_one(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()):
    count_of_iter = 0

    while len(data) > 1:
        new_compress_power = compress_power
        if (len(data) < compress_power + 1):
            new_compress_power = 2
        
        data = compress_and_compare(data, model, project_settings, new_compress_power, progress_bar=progress_bar)

        count_of_iter += 1


    return data[0]







