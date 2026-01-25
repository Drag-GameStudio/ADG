import re
from .custom_intro import get_all_html_links
from ..engine.models.model import Model
from ..engine.models.gpt_model import GPTModel
from ..engine.config.config import API_KEY

def split_text_by_anchors(text):
    pattern = r'(?=<a name=[^>]*></a>)'
    chunks = re.split(pattern, text)
    result_chanks = [chunk.strip() for chunk in chunks if chunk.strip()]
    all_links = get_all_html_links(text)
    result = {}

    for i in range(len(all_links)):
        result[all_links[i]] = result_chanks[i]
    return result


def get_order(model: Model, chanks: dict[str, str]):
    prompt = [
        {
            "role": "user",
            "content": f"""Sort the following titles semantically (group related topics together). 
                        Return ONLY a comma-separated list of the sorted titles. 
                        Do not include any introductory text, explanations, or concluding remarks.

                        Titles:
                        {list(chanks.keys())}
            """
        }
    ]
    result = model.get_answer_without_history(prompt)
    result = map(lambda x: x.strip(),result.split(","))

    order_output = ""
    for el in result:
        order_output += f"{chanks[el]} \n"
    return order_output

with open(r"C:\Users\huina\Python Projects\Impotant projects\AutoDocGenerateGimini\.auto_doc_cache\output_doc.md", "r", encoding="utf-8") as file:
    content  = file.read()

result = split_text_by_anchors(content)
sync_model = GPTModel(API_KEY, use_random=False)
print(get_order(sync_model, result))