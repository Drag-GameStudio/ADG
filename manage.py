from preprocessor.spliter import split_data, gen_doc_parts, async_gen_doc_parts
from preprocessor.compressor import compress_to_one
from preprocessor.postprocess import get_introdaction, get_all_html_links, get_links_intro
from engine.models.gpt_model import AsyncGPTModel
import os
from preprocessor.code_mix import CodeMix
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
import asyncio
from factory.base_factory import DocFactory
from factory.modules.intro import IntroLinks, IntroText
from ui.progress_base import BaseProgress, LibProgress


class Manager:
    CACHE_FOLDER_NAME = ".auto_doc_cache"

    FILE_NAMES = {
        "code_mix": "code_mix.txt",
        "global_info": "global_info.md",
        "output_doc": "output_doc.md"
    }


    def __init__(self, project_directory: str, ignore_files: list = [], language: str = "en", progress_bar: BaseProgress = BaseProgress()):
        self.project_directory = project_directory
        self.ignore_files = ignore_files
        self.progress_bar = progress_bar
        self.language = language

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
        result = compress_to_one(splited_data, 2, progress_bar=self.progress_bar, use_async=use_async)
        with open(self.get_file_path("global_info"), "w", encoding="utf-8") as file:
            file.write(result)

        self.progress_bar.update_task()
        

    def generete_doc_parts(self, max_symbols=5_000, use_async: bool = False):
        global_info = self.read_file_by_file_key("global_info")
        full_code_mix = self.read_file_by_file_key("code_mix")

        if use_async:
            result = asyncio.run(async_gen_doc_parts(full_code_mix, global_info, max_symbols, self.language, self.progress_bar))
        else:
            result = gen_doc_parts(full_code_mix, global_info, max_symbols, self.language, self.progress_bar)

        with open(self.get_file_path("output_doc"), "w", encoding="utf-8") as file:
            file.write(result)
        
        self.progress_bar.update_task()


    def factory_generate_doc_intro(self, doc_factory: DocFactory):
        global_info = self.read_file_by_file_key("global_info")
        curr_doc =  self.read_file_by_file_key("output_doc")

        info = {
            "language": self.language,
            "global_data": global_info,
            "full_data": curr_doc
        }
        result = doc_factory.generate_doc(info)

        new_data = f"{result} \n\n{curr_doc}"

        with open(self.get_file_path("output_doc"), "w", encoding="utf-8") as file:
            file.write(new_data)

        self.progress_bar.update_task()
        

        


if __name__ == "__main__":
    ignore_list = [
        "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db", "data",
        "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore", ".ruff_cache", ".auto_doc_cache",
        "*.pyc", "__pycache__", ".git", ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles", ".mypy_cache"
    ]



    with Progress(
        SpinnerColumn(),          
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),               
        TaskProgressColumn(),     
    ) as progress:
        manager = Manager(r"C:\Users\huina\Python Projects\Impotant projects\AutoDocGenerateGimini", ignore_list, progress_bar=LibProgress(progress), language="en")

        manager.generate_code_file()
        manager.generate_global_info_file(use_async=True, max_symbols=7000)
        manager.generete_doc_parts(use_async=True, max_symbols=5000)
        manager.factory_generate_doc_intro(
            DocFactory(
                IntroLinks(),
                IntroText(),
            )
        )



