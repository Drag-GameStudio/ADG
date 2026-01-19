from ..base_factory import BaseModule
from ...preprocessor.postprocess import get_all_html_links, get_links_intro, get_introdaction


class IntroLinks(BaseModule):
    def generate(self, info: dict):
        links = get_all_html_links(info.get("full_data"))
        intro_links = get_links_intro(links, info.get("language"))

        return intro_links


class IntroText(BaseModule):
    def generate(self, info: dict):
        intro = get_introdaction(info.get("global_data"), info.get("language"))
        return intro
