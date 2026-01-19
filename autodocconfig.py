from autodocgenerator.manage import Manager
from autodocgenerator.preprocessor.spliter import split_data, gen_doc_parts, async_gen_doc_parts
from autodocgenerator.preprocessor.compressor import compress_to_one
from autodocgenerator.preprocessor.postprocess import get_introdaction, get_all_html_links, get_links_intro
from autodocgenerator.engine.models.gpt_model import AsyncGPTModel
from autodocgenerator.preprocessor.code_mix import CodeMix
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.intro import IntroLinks, IntroText
from autodocgenerator.ui.progress_base import BaseProgress, LibProgress
from autodocgenerator.preprocessor.settings import ProjectSettings


def gen_doc(project_settings: ProjectSettings, ignore_list: list[str], project_path: str):
    

    with Progress(
        SpinnerColumn(),          
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),               
        TaskProgressColumn(),     
    ) as progress:

        
        manager = Manager(project_path, project_settings, ignore_list, progress_bar=LibProgress(progress), language="en")

        manager.generate_code_file()
        manager.generate_global_info_file(use_async=True, max_symbols=5000)
        manager.generete_doc_parts(use_async=True, max_symbols=4000)
        manager.factory_generate_doc_intro(
            DocFactory(
                IntroLinks(),
                IntroText(),
            )
        )

        return manager.read_file_by_file_key("output_doc")



project_settings = ProjectSettings("Auto Doc Generator")
project_settings.add_info(
    "global idea",
    """This project was created to help developers make documentations for them projects"""
)
ignore_list = [
        "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db", "data",
        "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore", ".ruff_cache", ".auto_doc_cache",
        "*.pyc", "__pycache__", ".git", ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles", ".mypy_cache"
    ]

result = gen_doc(project_path=".", project_settings=project_settings, ignore_list=ignore_list)
print(result[:1000])