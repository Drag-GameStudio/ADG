from ..engine.models.gpt_model import GPTModel, AsyncGPTModel, AsyncModel, Model
from ..engine.config.config import BASE_PART_COMPLITE_TEXT
import asyncio
from ..ui.progress_base import BaseProgress
from ..ui.logging import BaseLogger, InfoLog, ErrorLog, WarningLog


def split_data(data: str, max_symbols: int) -> list[str]:

    split_objects = []
    splited_by_files = data.split("</file>")
    
    logger = BaseLogger()
    logger.log(InfoLog("Starting data splitting..."))

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

    logger.log(InfoLog(f"Data split into {len(split_objects)} parts based on max symbols {max_symbols}."))

    return split_objects

def write_docs_by_parts(part: str, model: Model, prev_info: str = None, language: str = "en"):
    logger = BaseLogger()
    logger.log(InfoLog("Generating documentation for a part..."))
    prompt = [
            {
                "role": "system",
                "content": f"For the following task use language {language}"
            },
            {
                "role": "system",
                "content": BASE_PART_COMPLITE_TEXT
            }
    ]

    if prev_info is not None:
        prompt.append({
                "role": "system",
                "content": f"it is last part of documentation that you have write before {prev_info}"
            })

    prompt.append({
                "role": "user",
                "content": part
            })
    
    answer: str = model.get_answer_without_history(prompt=prompt)
    temp_answer = answer.removeprefix("```")
    logger.log(InfoLog("Documentation for part generated. total length: " + str(len(answer))))
    logger.log(InfoLog(f"Part Documentation: {answer}", level=2))
    if answer == temp_answer:
        return answer

    answer = temp_answer.removesuffix("```")
    return answer

async def async_write_docs_by_parts(part: str, async_model: AsyncModel, global_info: str, semaphore, prev_info: str = None, language: str = "en", update_progress = None):
    logger = BaseLogger()
    logger.log(InfoLog("Generating documentation for a part (async)..."))
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
                "role": "user",
                "content": part
            }
        ]

        if prev_info is not None:
            prompt.append({
                    "role": "system",
                    "content": f"it is last part of documentation that you have write before {prev_info}"
                })

        prompt.append({
                    "role": "user",
                    "content": part
                })
        answer: str = await async_model.get_answer_without_history(prompt=prompt)

        if update_progress is not None:
            update_progress()

        logger.log(InfoLog("Documentation for part generated. total length: " + str(len(answer))))
        logger.log(InfoLog(f"Part Documentation: {answer}", level=2))
        temp_answer = answer.removeprefix("```")
        if answer == temp_answer:
            return answer

        answer = temp_answer.removesuffix("```")
        return answer


def gen_doc_parts(full_code_mix, max_symbols, model: Model, language, progress_bar: BaseProgress):
    splited_data = split_data(full_code_mix, max_symbols)
    result = None
    logger = BaseLogger()
    logger.log(InfoLog("Starting documentation generation by parts..."))

    progress_bar.create_new_subtask(f"Generete doc parts", total_len=len(splited_data))
    
    all_result = ""
    for i, el in enumerate(splited_data):
        result = write_docs_by_parts(el, model, result, language)
        all_result += result
        all_result += "\n\n"

        result = result[len(result) - 3000:]
        progress_bar.update_task()
    
    progress_bar.remove_subtask()
    logger.log(InfoLog(f"""Documentation generation by parts completed.\n
                       Total documentation length: {len(all_result)}"""))
    logger.log(InfoLog(f"Documentation: {all_result}", level=2))
    return all_result

async def async_gen_doc_parts(full_code_mix, global_info, max_symbols, model: AsyncModel, language, progress_bar: BaseProgress):
    splited_data = split_data(full_code_mix, max_symbols)
    progress_bar.create_new_subtask(f"Generete doc parts (async)", len(splited_data))
    
    semaphore = asyncio.Semaphore(4)
    logger = BaseLogger()
    logger.log(InfoLog("Starting asynchronous documentation generation by parts..."))

    tasks = []
    for el in splited_data:
        tasks.append(async_write_docs_by_parts(part=el, async_model=model, global_info=global_info, semaphore=semaphore, language=language, update_progress=lambda: progress_bar.update_task()))

    gen_parts = await asyncio.gather(*tasks)
    result = ""
    for el in gen_parts:
        result += el
        result += "\n\n"

    progress_bar.remove_subtask()
    logger.log(InfoLog(f"""Asynchronous documentation generation by parts completed.\n
                       Total documentation length: {len(result)}"""))
    logger.log(InfoLog(f"Documentation: {result}", level=2))

    return result