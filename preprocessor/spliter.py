from engine.models.gpt_model import GPTModel
from engine.config.config import BASE_PART_COMPLITE_TEXT

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

def write_docs_by_parts(part: str, global_info: str, prev_info: str = None):
    if prev_info is None:
        prompt = [
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

    else:
        prompt = [
            {
                "role": "system",
                "content": BASE_PART_COMPLITE_TEXT
            },
            {
                "role": "system",
                "content": global_info
            },
            {
                "role": "system",
                "content": f"it is last part of documentation that you have write before{prev_info}"
            },
            {
                "role": "user",
                "content": part
            }
        ]
    answer: str = GPTModel().get_answer_without_history(prompt=prompt)
    temp_answer = answer.removeprefix("```")
    if answer == temp_answer:
        return answer

    answer = temp_answer.removesuffix("```")
    return answer

