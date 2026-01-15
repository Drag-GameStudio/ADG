from engine.models.gpt_model import GPTModel, AsyncGPTModel, Model, AsyncModel
from engine.config.config import BASE_COMPRESS_TEXT, get_BASE_COMPRESS_TEXT
import math
import asyncio
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn


def compress(data: str, model: Model, compress_power) -> str:
    prompt = [
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


def compress_and_compare(data: list, compress_power: int = 4, progress_bar: Progress = None) -> list:
    compress_and_compare_data = ["" for i in range(math.ceil(len(data) / compress_power))]
    sub_task = progress_bar.add_task(f"[green]  compare all files", total=len(data))
    model = GPTModel()
    for i, el in enumerate(data):
        curr_index = i // compress_power
        compress_and_compare_data[curr_index] += compress(el, model, compress_power) + "\n"
        progress_bar.update(sub_task, advance=1)

    progress_bar.remove_task(sub_task)

    return compress_and_compare_data


async def async_compress(data: str, model: AsyncModel, compress_power, semaphore) -> str:
    
    async with semaphore:
        prompt = [
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
        return answer

async def async_compress_and_compare(data: list, compress_power: int = 4) -> list:
    semaphore = asyncio.Semaphore(4)
    model = AsyncGPTModel()
    tasks = []
    for el in data:
        tasks.append(async_compress(el, model, compress_power, semaphore))
    
    compressed_elements = await asyncio.gather(*tasks)
    
    final_data = []
    chunk_size = compress_power
    for i in range(0, len(compressed_elements), chunk_size):
        chunk = compressed_elements[i : i + chunk_size]
        final_data.append("\n".join(chunk) + "\n")
        
    return final_data

def compress_to_one(data: list, compress_power: int = 4, use_async: bool = False, progress_bar: Progress = None):
    count_of_iter = 0
    while len(data) > 1:
        new_compress_power = compress_power
        if (len(data) < compress_power + 1):
            new_compress_power = 2
        
        if use_async:
            data = asyncio.run(async_compress_and_compare(data, new_compress_power))
        else:
            data = compress_and_compare(data, new_compress_power, progress_bar=progress_bar)
        count_of_iter += 1


    return data[0]






