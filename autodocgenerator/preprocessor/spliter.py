from ..engine.models.gpt_model import GPTModel, AsyncGPTModel, AsyncModel, Model
from ..engine.config.config import BASE_PART_COMPLITE_TEXT
import asyncio
from ..ui.progress_base import BaseProgress


def split_data(data: str, max_symbols: int) -> list[str]:

    split_objects = []

    splited_by_files = data.split("</file>")
    

    while True:
        have_to_change = False
        for i, el in enumerate(splited_by_files):
            if len(el) > max_symbols * 1.5:
                splited_by_files.insert(i+1, el[i][int(max_symbols / 2):])
                splited_by_files[i] = el[i][:int(max_symbols / 2)]
                have_to_change = True

        if have_to_change == False:
            break

            


    curr_index = 0
    for el in splited_by_files:
        if len(split_objects) - 1 < curr_index:
            split_objects.append("")

        if len(split_objects[curr_index]) + len(el) > max_symbols * 1.25:
            curr_index += 1
            split_objects.append(el)
            continue

        split_objects[curr_index] += "\n" + el

    return split_objects

def write_docs_by_parts(part: str, model: Model, global_info: str, prev_info: str = None, language: str = "en"):
    prompt = [
            {
                "role": "system",
                "content": f"For the following task use language {language}"
            },
            {
                "role": "system",
                "content": BASE_PART_COMPLITE_TEXT
            },
            {
                "role": "system",
                "content": global_info
            },
            {
                "role": "user",
                "content": part
            }
    ]

    if prev_info is not None:
        prompt.append({
                "role": "system",
                "content": f"it is last part of documentation that you have write before{prev_info}"
            })

    prompt.append({
                "role": "user",
                "content": part
            })
    
    answer: str = model.get_answer_without_history(prompt=prompt)
    temp_answer = answer.removeprefix("```")
    if answer == temp_answer:
        return answer

    answer = temp_answer.removesuffix("```")
    return answer

async def async_write_docs_by_parts(part: str, async_model: AsyncModel, global_info: str, semaphore, prev_info: str = None, language: str = "en", update_progress = None):

    async with semaphore:

        prompt = [
            {
                "role": "system",
                "content": f"For the following task use language {language}"
            },
            {
                "role": "system",
                "content": BASE_PART_COMPLITE_TEXT
            },
            {
                "role": "system",
                "content": global_info
            },
            {
                "role": "user",
                "content": part
            }
        ]

        if prev_info is not None:
            prompt.append({
                    "role": "system",
                    "content": f"it is last part of documentation that you have write before{prev_info}"
                })

        prompt.append({
                    "role": "user",
                    "content": part
                })
        answer: str = await async_model.get_answer_without_history(prompt=prompt)

        if update_progress is not None:
            update_progress()


        temp_answer = answer.removeprefix("```")
        if answer == temp_answer:
            return answer

        answer = temp_answer.removesuffix("```")
        return answer


def gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar: BaseProgress):
    splited_data = split_data(full_code_mix, max_symbols)
    result = None

    progress_bar.create_new_subtask(f"Generete doc parts", total=len(splited_data))
    
    all_result = ""
    model = GPTModel()
    for el in splited_data:
        result = write_docs_by_parts(el, model, global_info, result, language)
        all_result += result
        all_result += "\n\n"

        result = result[len(result) - 3000:]
        progress_bar.update_task()
    
    progress_bar.remove_subtask()

    return all_result

async def async_gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar: BaseProgress):
    splited_data = split_data(full_code_mix, max_symbols)
    progress_bar.create_new_subtask(f"Generete doc parts (async)", len(splited_data))

    semaphore = asyncio.Semaphore(4)
    async_gpt_model = AsyncGPTModel()

    tasks = []
    for el in splited_data:
        tasks.append(async_write_docs_by_parts(part=el, async_model=async_gpt_model, global_info=global_info, semaphore=semaphore, language=language, update_progress=lambda: progress_bar.update_task()))

    gen_parts = await asyncio.gather(*tasks)
    result = ""
    for el in gen_parts:
        result += el
        result += "\n\n"

    progress_bar.remove_subtask()


    return result