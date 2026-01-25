from ..engine.models.gpt_model import GPTModel
from ..engine.models.model import Model 
from ..engine.config.config import BASE_INTRODACTION_CREATE_TEXT, BASE_INTRO_CREATE
from ..ui.logging import InfoLog, BaseLogger
import re



def get_all_html_links(data: str) -> list[str]:
    links = []
    
    logger = BaseLogger()
    logger.log(InfoLog("Extracting HTML links from documentation..."))

    pattern = r'<a name=["\']?(.*?)["\']?></a>'
    
    for match in re.finditer(pattern, data):
        anchor_name = match.group(1)
        
        links.append("#" + anchor_name)

    
    logger.log(InfoLog(f"Extracted {len(links)} HTML links from documentation."))
    logger.log(InfoLog(f"Links: {links}", level=1))
    return links

def get_links_intro(links: list[str], model: Model, language: str = "en"):
    logger = BaseLogger()

    prompt = [
        {
            "role": "system",
            "content": f"For the following task use language {language}"
        },
        {
            "role": "system",
            "content": BASE_INTRODACTION_CREATE_TEXT
        },
        {
            "role": "user",
            "content": str(links)
        }
    ]
    logger.log(InfoLog("Generating introduction with links..."))
    intro_links = model.get_answer_without_history(prompt=prompt)
    logger.log(InfoLog("Introduction with links generated."))
    logger.log(InfoLog(f"Introduction Links: {intro_links}", level=1))
    return intro_links

def get_introdaction(global_data: str, model: Model, language: str = "en") -> str:
    prompt = [
        {
            "role": "system",
            "content": f"For the following task use language {language}"
        },
        {
            "role": "system",
            "content": BASE_INTRO_CREATE
        },
        {
            "role": "user",
            "content": global_data
        }
    ]

    intro = model.get_answer_without_history(prompt=prompt)

    return intro

def generete_custom_discription(splited_data: str, model: Model, custom_description: str, language: str = "en") -> str:

    for sp_data in splited_data:

        prompt = [
            {
                "role": "system",
                "content": f"For the following task use language {language}"
            },
            {
                "role": "system",
                "content": f"Act as a precise Technical Analyst. You will be provided with specific code or documentation. Your task is to describe or extract information based ONLY on the provided context. And make title and link <a name='your_title'> </a> format"
            },
            {
                "role": "system",
                "content": f"### Context: {sp_data}"
            },
            {"role": "system",
            "content": """### Strict Rules:
                1. Use ONLY the provided Context to answer. 
                2. If the requested information is not explicitly mentioned in the Context, or if you don't know the answer based on the provided data, respond with an empty string ("") or simply say "No information found". 
                3. DO NOT use external knowledge or invent any logic that is not present in the text.
                4. Do not provide any introductory or concluding remarks. If there is no info, output must be empty.
                5. If you dont have any info about it return just !noinfo"""
            },
            {
                "role": "user",
                "content": f"### Task to discribe: {custom_description}"
            }
        ]

        result = model.get_answer_without_history(prompt=prompt)
        if (result.find("!noinfo") == -1 and result.find("No information found") == -1) or result.find("!noinfo") > 30:
            break
        result = ""
    return result