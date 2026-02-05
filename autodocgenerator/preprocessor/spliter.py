from ..engine.models.gpt_model import GPTModel, AsyncGPTModel, AsyncModel, Model
from ..engine.config.config import BASE_PART_COMPLITE_TEXT
import asyncio
from ..ui.progress_base import BaseProgress
from ..ui.logging import BaseLogger, InfoLog, ErrorLog, WarningLog
from .settings import ProjectSettings


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

def write_docs_by_parts(part: str, model: Model, project_settings: ProjectSettings, prev_info: str = None, language: str = "en", global_info: str = None):
    logger = BaseLogger()
    logger.log(InfoLog("Generating documentation for a part..."))
    prompt = [
            {
                "role": "system",
                "content": f"For the following task use language {language}"
            },
            {
                "role": "system",
                "content": f"global project info: {project_settings.prompt}"
            },
            {
                "role": "system",
                "content": BASE_PART_COMPLITE_TEXT
            }
    ]

    if global_info is not None:
        prompt.append({
            "role": "system",
            "content": f"global relations in project: {global_info}"
        })

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




def gen_doc_parts(full_code_mix, max_symbols, model: Model, project_settings: ProjectSettings,  language, progress_bar: BaseProgress, global_info = None):
    splited_data = split_data(full_code_mix, max_symbols)
    result = None
    logger = BaseLogger()
    logger.log(InfoLog("Starting documentation generation by parts..."))

    progress_bar.create_new_subtask(f"Generete doc parts", total_len=len(splited_data))
    
    all_result = ""
    for i, el in enumerate(splited_data):
        result = write_docs_by_parts(el, model, project_settings, result, language, global_info=global_info)
        all_result += result
        all_result += "\n\n"

        result = result[len(result) - 3000:]
        progress_bar.update_task()
    
    progress_bar.remove_subtask()
    logger.log(InfoLog(f"""Documentation generation by parts completed.\n
                       Total documentation length: {len(all_result)}"""))
    logger.log(InfoLog(f"Documentation: {all_result}", level=2))
    return all_result
