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


def split_text_by_anchors(text):
    pattern = r'(?=<a name=["\']?[^"\'>\s]{6,200}["\']?></a>)'
    chunks = re.split(pattern, text)
    result_chanks = [chunk.strip() for chunk in chunks if chunk.strip()]
    all_links = extract_links_from_start(result_chanks)
    result = {}

    if len(all_links) != len(result_chanks):
        return None

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
                        You can delete somthing strange like #[^>]* or empty.
                        Titles:
                        {list(chanks.keys())}
            """
        }
    ]
    result = model.get_answer_without_history(prompt)
    new_result = map(lambda x: x.strip(),result.split(","))
    logger.log(InfoLog(f"End ordering result list {list(new_result)}"))

    order_output = ""
    print("tressafafasfasfasfsafas")
    print(list(new_result))
    print(len(list(new_result)))
    for el in new_result:
        print(el, "EL: ...")
        order_output += f"{chanks.get(el)} \n"
        logger.log(InfoLog(f"Add to {chanks.get(el)}", level=2))
        
    return order_output


if __name__ == "__main__":
    with open(r"C:\Users\huina\Python Projects\Impotant projects\AutoDocGenerateGimini\README.md", "r", encoding="utf-8") as file:
        data = file.read()

    print(split_text_by_anchors(data))


