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
            "content": get_BASE_COMPRESS_TEXT(10000, compress_power)
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

async def async_compress(data: str,  project_settings: ProjectSettings, model: AsyncModel, compress_power, semaphore, progress_bar: BaseProgress) -> str:
    
    async with semaphore:
        prompt = [
            {
                "role": "system",
                "content": project_settings.prompt
            },
            {
                "role": "system",
                "content": get_BASE_COMPRESS_TEXT(10000, compress_power)
            },
            {
                "role": "user",
                "content": data
            }
        ]
        answer = await model.get_answer_without_history(prompt=prompt)
        progress_bar.update_task()
        return answer

async def async_compress_and_compare(data: list, model: AsyncModel, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) -> list:
    semaphore = asyncio.Semaphore(4)
    tasks = []
    progress_bar.create_new_subtask(f"Compare all files (async)", len(data))

    for el in data:
        tasks.append(async_compress(el, project_settings, model, compress_power, semaphore, progress_bar))
    
    compressed_elements = await asyncio.gather(*tasks)
    
    final_data = []
    chunk_size = compress_power
    for i in range(0, len(compressed_elements), chunk_size):
        chunk = compressed_elements[i : i + chunk_size]
        final_data.append("\n".join(chunk) + "\n")
    
    progress_bar.remove_subtask()
        
    return final_data

def compress_to_one(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, use_async: bool = False, progress_bar: BaseProgress = BaseProgress()):
    count_of_iter = 0
    while len(data) > 1:
        new_compress_power = compress_power
        if (len(data) < compress_power + 1):
            new_compress_power = 2
        
        if use_async:
            data = asyncio.run(async_compress_and_compare(data, model, project_settings, new_compress_power, progress_bar=progress_bar))
        else:
            data = compress_and_compare(data, model, project_settings, new_compress_power, progress_bar=progress_bar)
        count_of_iter += 1


    return data[0]



def generate_discribtions_for_code(data: list, model: Model, project_settings: ProjectSettings, progress_bar: BaseProgress = BaseProgress()) -> list:
    describtions = []
    progress_bar.create_new_subtask("Generate describtions for code files", len(data))
    for code in data:
        prompt = [
            {
                "role": "system",
                "content": """### Instructions:
1. Identify Main Components: Determine what classes, functions, or modules are meant to be used by an external developer.
2. Description: Explain the purpose of each main component (e.g., "What is the Manager class for?").
3. Parameters & Types: Detail every parameter required for initialization and method calls, including their expected data types and default values.
4. Usage Example: Provide a COMPLETE, "copy-pasteable" code example showing:
   - Proper initialization.
   - Calling key methods.
   - Handling expected outputs or errors.

### Strict Rules:
- Base your guide ONLY on the provided code. 
- If the code is incomplete or a certain class/method is missing, do not hallucinate its logic—simply state that information is unavailable.
- Use Markdown for code blocks and bold text for parameter names.
- If no usable logic is found in the code, respond with an empty string ("")."""
            },
            {
                "role": "user",
                "content": f"CONTEXT: {code}"
            }
        ]
        answer = model.get_answer_without_history(prompt=prompt)
        describtions.append(answer)
        progress_bar.update_task()
    
    progress_bar.remove_subtask()
    return describtions




