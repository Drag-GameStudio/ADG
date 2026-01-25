import re
from .custom_intro import get_all_html_links
from ..engine.models.model import Model
from ..ui.logging import BaseLogger, InfoLog, WarningLog, ErrorLog

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
    logger = BaseLogger()
    logger.log(InfoLog("Start ordering"))
    logger.log(InfoLog(f"chanks name: {list(chanks.keys())}", level=1))
    logger.log(InfoLog(f"chanks: {chanks}", level=2))


    prompt = [
        {
            "role": "user",
            "content": f"""Sort the following titles semantically (group related topics together). 
                        Return ONLY a comma-separated list of the sorted titles. 
                        Do not include any introductory text, explanations, or concluding remarks.
                        You can delete somthing strange like #[^>]* or empty
                        Titles:
                        {list(chanks.keys())}
            """
        }
    ]
    result = model.get_answer_without_history(prompt)
    result = map(lambda x: x.strip(),result.split(","))
    logger.log(InfoLog(f"End ordering result list {list(result)}"))

    order_output = ""
    print("tressafafasfasfasfsafas")
    print(result)
    print(len(result))
    for el in result:
        print(el)
        order_output += f"{chanks.get(el)} \n"
        logger.log(InfoLog(f"Add to {chanks.get(el)}", level=2))
        
    return order_output



