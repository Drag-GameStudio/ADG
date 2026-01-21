from .preprocessor.spliter import split_data, gen_doc_parts, async_gen_doc_parts
from .preprocessor.compressor import compress_to_one, generate_discribtions_for_code
from .preprocessor.postprocess import get_introdaction, get_all_html_links, get_links_intro
from .engine.models.gpt_model import AsyncGPTModel, GPTModel
from .engine.models.model import Model, AsyncModel
import os
from .preprocessor.code_mix import CodeMix
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
import asyncio
from .factory.base_factory import DocFactory
from .factory.modules.intro import IntroLinks, IntroText
from .factory.modules.general_modules import CustomModule
from .ui.progress_base import BaseProgress, LibProgress
from .preprocessor.settings import ProjectSettings


class Manager:
    CACHE_FOLDER_NAME = ".auto_doc_cache"

    FILE_NAMES = {
        "code_mix": "code_mix.txt",
        "global_info": "global_info.md",
        "output_doc": "output_doc.md"
    }


    def __init__(self, project_directory: str, project_settings: ProjectSettings,
                 sync_model: Model = None, async_model: AsyncModel = None,
                  ignore_files: list = [], language: str = "en", 
                  progress_bar: BaseProgress = BaseProgress()):
        self.project_directory = project_directory
        self.ignore_files = ignore_files
        self.progress_bar = progress_bar
        self.language = language
        self.project_settings = project_settings

        self.sync_model = sync_model
        self.async_model = async_model

        cache_path = os.path.join(self.project_directory, self.CACHE_FOLDER_NAME)

        if not os.path.isdir(cache_path):
            os.mkdir(cache_path)

    def read_file_by_file_key(self, file_key: str):
        with open(self.get_file_path(file_key), "r", encoding="utf-8") as file:
            data = file.read()
        return data

    def get_file_path(self, file_key: str):
        return os.path.join(self.project_directory, self.CACHE_FOLDER_NAME, self.FILE_NAMES.get(file_key))

    def generate_code_file(self):
        cm = CodeMix(self.project_directory, self.ignore_files)
        cm.build_repo_content(self.get_file_path("code_mix"))
        self.progress_bar.update_task()

    def generate_global_info_file(self, max_symbols=10_000, use_async: bool = False):
        full_code_mix = self.read_file_by_file_key("code_mix")

        splited_data = split_data(full_code_mix, max_symbols)
        curr_model = self.async_model if use_async else self.sync_model
        result = compress_to_one(splited_data, curr_model, self.project_settings, 2, progress_bar=self.progress_bar, use_async=use_async)
        with open(self.get_file_path("global_info"), "w", encoding="utf-8") as file:
            file.write(result)

        self.progress_bar.update_task()
        

    def generete_doc_parts(self, max_symbols=5_000, use_async: bool = False):
        global_info = self.read_file_by_file_key("global_info")
        full_code_mix = self.read_file_by_file_key("code_mix")

        if use_async:
            result = asyncio.run(async_gen_doc_parts(full_code_mix, global_info, max_symbols, self.async_model, self.language, self.progress_bar))
        else:
            result = gen_doc_parts(full_code_mix, global_info, max_symbols, self.sync_model, self.language, self.progress_bar)

        with open(self.get_file_path("output_doc"), "w", encoding="utf-8") as file:
            file.write(result)
        
        self.progress_bar.update_task()

    def factory_generate_doc(self, doc_factory: DocFactory):
        global_info = self.read_file_by_file_key("global_info")
        curr_doc = self.read_file_by_file_key("output_doc")
        code_mix = self.read_file_by_file_key("code_mix")

        info = {
            "language": self.language,
            "global_data": global_info,
            "full_data": curr_doc,
            "code_mix": code_mix
        }
        result = doc_factory.generate_doc(info, self.sync_model, self.progress_bar)

        new_data = f"{result} \n\n{curr_doc}"

        with open(self.get_file_path("output_doc"), "w", encoding="utf-8") as file:
            file.write(new_data)

        self.progress_bar.update_task()
        

        
from .engine.config.config import API_KEY

if __name__ == "__main__":
    ignore_list = [
        "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db", "data",
        "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore", ".ruff_cache", ".auto_doc_cache",
        "*.pyc", "__pycache__", ".git", ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles", ".mypy_cache"
    ]

    sync_model = GPTModel(API_KEY)
    async_model = AsyncGPTModel(API_KEY)

    with Progress(
        SpinnerColumn(),          
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),               
        TaskProgressColumn(),     
    ) as progress:
        project_settings = ProjectSettings("Auto Doc Generator")
        project_settings.add_info(
            "global idea",
            """This project was created to help developers make documentations for them projects"""
        )
        manager = Manager(r"C:\Users\sinic\OneDrive\Документы\GitHub\ADG", 
                        project_settings,
                        sync_model=sync_model,
                        async_model=async_model,
                        ignore_files=ignore_list, 
                        progress_bar=LibProgress(progress), 
                        language="en")

        # manager.generate_code_file()
        # manager.generate_global_info_file(use_async=True, max_symbols=5000)
        # manager.generete_doc_parts(use_async=True, max_symbols=4000)
        # manager.factory_generate_doc(
        #     DocFactory(
        #         CustomModule("how to use Manager class what parameters i need to give. give full example of usege"),
        #         CustomModule("how to use Module and create your own module. give full example of usege ")
        #     )
        # )
        
        manager.factory_generate_doc(
            DocFactory(
                IntroLinks(),
                # IntroText(),
            )
        )



