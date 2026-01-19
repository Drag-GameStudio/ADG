from ..engine.models.gpt_model import GPTModel
from ..engine.config.config import BASE_INTRODACTION_CREATE_TEXT, BASE_INTRO_CREATE
import re
import unicodedata

def generate_markdown_anchor(header: str) -> str:
    anchor = header.lower()
    anchor = unicodedata.normalize('NFKC', anchor)
    anchor = anchor.replace(' ', '-')
    anchor = re.sub(r'[^a-z0-9\-_]', '', anchor)

    anchor = re.sub(r'-+', '-', anchor)
    anchor = anchor.strip('-')
    
    return f"#{anchor}"

def get_all_topics(data: str) -> list[str]:
    topics = []
    curr_shift_index = 0
    while True:
        curr_index = data.find("\n## ", curr_shift_index)
        if curr_index == -1:
            break
        
        curr_shift_index = data.find("\n", curr_index + 3)
        topics.append(data[curr_index + 4:curr_shift_index])

    links = [generate_markdown_anchor(el) for el in topics]
    return topics, links 

def get_all_html_links(data: str) -> list[str]:
    links = []
    curr_shift_index = 0
    while True:
        curr_index = data.find("<a name=", curr_shift_index)
        if curr_index == -1:
            break

        curr_shift_index = data.find("</a>", curr_index + 3)
        links.append(data[curr_index + 9:curr_shift_index - 2])

    return links



def get_links_intro(links: list[str], language: str = "en"):
    model = GPTModel()
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
    intro_links = model.get_answer_without_history(prompt=prompt)
    return intro_links

def get_introdaction(global_data: str, language: str = "en") -> str:
    model = GPTModel()
    

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

