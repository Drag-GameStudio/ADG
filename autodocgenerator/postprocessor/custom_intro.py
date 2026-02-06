from ..engine.models.gpt_model import GPTModel
from ..engine.models.model import Model 
from ..engine.config.config import BASE_INTRODACTION_CREATE_LINKS, BASE_INTRO_CREATE, BASE_CUSTOM_DISCRIPTIONS
from ..ui.logging import InfoLog, BaseLogger
import re



def get_all_html_links(data: str) -> list[str]:
    links = []
    
    logger = BaseLogger()
    logger.log(InfoLog("Extracting HTML links from documentation..."))

    pattern = r'<a name=["\']?(.*?)["\']?></a>'
    
    for match in re.finditer(pattern, data):
        anchor_name = match.group(1)
        
        if len(anchor_name) > 5:
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
            "content": BASE_INTRODACTION_CREATE_LINKS
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
                "content": f"Act as a precise Technical Analyst. You will be provided with specific code or documentation. Your task is to describe or extract information based ONLY on the provided context"
            },
            {
                "role": "system",
                "content": f"### Context: {sp_data}"
            },
            {
                "role": "system",
                "content": BASE_CUSTOM_DISCRIPTIONS
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

def generete_custom_discription_without(model: Model, custom_description: str, language: str = "en") -> str:
    prompt = [
         {
            "role": "system",
            "content": f"For the following task use language {language}"
        },
        {
            "role": "system",
            "content": f"Act as a precise Technical Analyst. You will be provided with specific code or documentation. Your task is to describe and rewrite the following text"
        },
        {
            "role": "system",
            "content": """Every response must start with exactly one <a name="CONTENT_DESCRIPTION"></a> tag. DO NOT CHANGE ANY LINKS IN PROMPT, The CONTENT_DESCRIPTION must be a short, hyphenated summary of the actual information you are providing (e.g., "user-authentication-logic" instead of "auth.yml"). STRICT RULES:

NO filenames or paths (e.g., forbidden: "autodocconfig.yml", "src/config").
NO file extensions (e.g., forbidden: ".yml", ".md").
NO generic terms (e.g., forbidden: "config", "settings", "run", "docs").
NO protocols (http/https).
This tag must appear ONLY ONCE at the very beginning. Never repeat it or use other links"""
        },
        {
            "role": "user",
            "content": f"### Task to discribe: {custom_description}"
        }
    ]

    result = model.get_answer_without_history(prompt=prompt)
    return result

