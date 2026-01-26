from .preprocessor.spliter import split_data, gen_doc_parts, async_gen_doc_parts
from .preprocessor.compressor import compress_to_one, generate_discribtions_for_code
from .postprocessor.custom_intro import get_introdaction, get_all_html_links, get_links_intro
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
from .ui.logging import BaseLogger, BaseLoggerTemplate, InfoLog, ErrorLog, WarningLog, FileLoggerTemplate
from .preprocessor.settings import ProjectSettings
from .auto_runner.config_reader import ProjectConfigSettings
from .postprocessor.sorting import get_order, split_text_by_anchors
from .config.config import Config


class Manager:
    CACHE_FOLDER_NAME = ".auto_doc_cache"

    FILE_NAMES = {
        "code_mix": "code_mix.txt",
        "global_info": "global_info.md",
        "logs": "report.txt",
        "output_doc": "output_doc.md"
    }


    def __init__(self, project_directory: str, 
                 config: Config, 
                 sync_model: Model = None, 
                 async_model: AsyncModel = None, 
                 progress_bar: BaseProgress = BaseProgress()):
        
        self.config = config

        self.project_directory = project_directory
        self.progress_bar = progress_bar

        self.sync_model = sync_model
        self.async_model = async_model

        self.logger = BaseLogger()
        self.logger.set_logger(FileLoggerTemplate(self.get_file_path("logs"), log_level=self.config.pcs.log_level))

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
        self.logger.log(InfoLog("Starting code mix generation..."))
        cm = CodeMix(self.project_directory, self.config.ignore_files)
        cm.build_repo_content(self.get_file_path("code_mix"))

        self.logger.log(InfoLog("Code mix generation completed."))
        self.progress_bar.update_task()


    def generete_doc_parts(self, max_symbols=5_000):


        full_code_mix = self.read_file_by_file_key("code_mix")

        self.logger.log(InfoLog("Starting synchronous documentation generation by parts..."))
        result = gen_doc_parts(full_code_mix,
                                max_symbols, self.sync_model, 
                                self.config.language, self.progress_bar)
            
        self.logger.log(InfoLog("Documentation generation by parts completed."))

        with open(self.get_file_path("output_doc"), "w", encoding="utf-8") as file:
            file.write(result)
        
        self.progress_bar.update_task()

    def factory_generate_doc(self, doc_factory: DocFactory):
        curr_doc = self.read_file_by_file_key("output_doc")
        code_mix = self.read_file_by_file_key("code_mix")

        info = {
            "language": self.config.language,
            "full_data": curr_doc,
            "code_mix": code_mix
        }

        self.logger.log(InfoLog(f"""Starting factory documentation generation \n
                                {" ".join([type(module).__name__ for module in doc_factory.modules])} \n
                                Input params: {" ".join([f"{key}: {len(value)} chars" for key, value in info.items()])}
                                """))

        result = doc_factory.generate_doc(info, self.sync_model, self.progress_bar)
        self.logger.log(InfoLog("Factory documentation generation completed."))
        new_data = f"{result} \n\n{curr_doc}"

        with open(self.get_file_path("output_doc"), "w", encoding="utf-8") as file:
            file.write(new_data)

        self.progress_bar.update_task()

    def order_doc(self):
        curr_doc = self.read_file_by_file_key("output_doc")
        result = split_text_by_anchors(curr_doc)
        if result is None:
            return
        result = get_order(self.sync_model, result)

        with open(self.get_file_path("output_doc"), "w", encoding="utf-8") as file:
            file.write(result)

    def clear_cache(self):
        if not self.config.pcs.save_logs:
            os.remove(self.get_file_path("logs"))
        