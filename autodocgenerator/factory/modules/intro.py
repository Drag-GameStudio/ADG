from ...engine.models.model import Model
from ..base_factory import BaseModule
from ...postprocessor.custom_intro import get_all_html_links, get_links_intro, get_introdaction


class IntroLinks(BaseModule):
    def generate(self, info: dict, model: Model):
        links = get_all_html_links(info.get("full_data"))
        print(links)
        intro_links = get_links_intro(links, model, info.get("language"))

        return intro_links


class IntroText(BaseModule):
    def generate(self, info: dict, model: Model):
        intro = get_introdaction(info.get("global_data"), model, info.get("language"))
        return intro
