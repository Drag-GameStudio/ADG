from autodocgenerator.manage import Manager
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.intro import IntroLinks, IntroText
from autodocgenerator.ui.progress_base import BaseProgress, LibProgress, ConsoleGtiHubProgress
from autodocgenerator.preprocessor.settings import ProjectSettings
from .config_reader import Config, read_config, ProjectConfigSettings
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.engine.config.config import API_KEY
from autodocgenerator.ui.logging import BaseLogger, InfoLog, ErrorLog, WarningLog, FileLoggerTemplate
import os


def gen_doc(project_settings: ProjectSettings, pcs: ProjectConfigSettings, ignore_list: list[str], project_path: str, doc_factory: DocFactory, intro_factory: DocFactory, language: str = "en"):
    
    sync_model = GPTModel(API_KEY, use_random=False)
    async_model = AsyncGPTModel(API_KEY)
    
    manager = Manager(
        project_path, 
        project_settings,
        pcs, 
        sync_model=sync_model,
        async_model=async_model,
        ignore_files=ignore_list, 
        progress_bar=ConsoleGtiHubProgress(), 
        language=language)


    manager.generate_code_file()
    manager.generate_global_info_file(use_async=False, max_symbols=8000)
    manager.generete_doc_parts(use_async=False, max_symbols=6000)
    manager.factory_generate_doc(doc_factory)
    manager.order_doc()
    manager.factory_generate_doc(intro_factory)
    manager.clear_cache()

    return manager.read_file_by_file_key("output_doc")

if __name__ == "__main__":
    with open("autodocconfig.yml", "r", encoding="utf-8") as file:
        config_data = file.read()
    config: Config = read_config(config_data)

    project_settings = config.get_project_settings()
    doc_factory, intro_factory = config.get_doc_factory()

    output_doc = gen_doc(
        project_settings,
        config.pcs,
        config.ignore_files,
        ".",
        doc_factory,
        intro_factory,
        language=config.language
    )

    



