import re
from ..engine.models.model import Model
from ..ui.logging import BaseLogger, InfoLog, WarningLog, ErrorLog

def extract_links_from_start(chunks):
    links = []
    pattern = r'^<a name=["\']?(.*?)["\']?></a>'
    
    for chunk in chunks:
        match = re.search(pattern, chunk.strip())
        if match:
            anchor_name = match.group(1)
            if len(anchor_name) > 5:
                links.append("#" + anchor_name)
                
    return links


def split_text_by_anchors(text: str) -> dict[str, str]:
    pattern = r'(?=<a name=["\']?[^"\'>\s]{6,200}["\']?></a>)'
    chunks = re.split(pattern, text)
    result_chanks = [chunk.strip() for chunk in chunks if chunk.strip()]
    all_links = extract_links_from_start(result_chanks)

    start_link_index = text.find("<a name")
    if start_link_index > 10:
        result_chanks.pop(0)
    result = {}

    if len(all_links) != len(result_chanks):
        raise Exception("Somthing with anchors")

    for i in range(len(all_links)):
        result[all_links[i]] = result_chanks[i]
    return result


def get_order(model: Model, chanks: list[str]) -> list:
    logger = BaseLogger()
    logger.log(InfoLog("Start ordering"))
    logger.log(InfoLog(f"chanks name: {chanks}", level=1))


    prompt = [ #TODO tranport promt to prompts
        {
            "role": "user",
            "content": f"""Sort the following titles semantically (group related topics together). 
                        Return ONLY a comma-separated list of the sorted titles. 
                        Do not include any introductory text, explanations, or concluding remarks.
                        leave # in title.
                        do not skip any title
                        Titles:
                        {chanks}
            """
        }
    ]
    result = model.get_answer_without_history(prompt)
    new_result = list(map(lambda x: x.strip(), result.split(",")))
    logger.log(InfoLog(f"End ordering result list {new_result}"))

    
        
    return new_result


if __name__ == "__main__":
    with open(r"C:\Users\huina\Python Projects\Impotant projects\AutoDocGenerateGimini\README.md", "r", encoding="utf-8") as file:
        data = file.read()

    print(split_text_by_anchors(data))


