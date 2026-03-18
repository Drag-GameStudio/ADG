from .preprocessor.spliter import split_data, gen_doc_parts
from .preprocessor.compressor import compress_to_one
from .engine.models.model import Model
import os
from .preprocessor.code_mix import CodeMix
from .factory.base_factory import DocFactory
from .ui.progress_base import BaseProgress
from .ui.logging import BaseLogger, InfoLog, ErrorLog, WarningLog, FileLoggerTemplate
from .postprocessor.sorting import get_order, split_text_by_anchors
from .config.config import Config
from .schema.doc_schema import DocContent, DocHeadSchema, DocInfoSchema


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
                 llm_model: Model,
                 progress_bar: BaseProgress = BaseProgress()):
        
    
        self.doc_info = DocInfoSchema()
        self.config = config

        self.project_directory = project_directory
        self.progress_bar = progress_bar

        self.llm_model = llm_model

        self.logger = BaseLogger()
        self.logger.set_logger(FileLoggerTemplate(self.get_file_path("logs"), log_level=self.config.pbc.log_level))

        cache_path = os.path.join(self.project_directory, self.CACHE_FOLDER_NAME)

        if not os.path.isdir(cache_path):
            os.mkdir(cache_path)

    def read_file_by_file_key(self, file_key: str):
        try:
            with open(self.get_file_path(file_key), "r", encoding="utf-8") as file:
                data = file.read()
        except:
            data = None
        return data

    def get_file_path(self, file_key: str):
        return os.path.join(self.project_directory, self.CACHE_FOLDER_NAME, self.FILE_NAMES[file_key]) 

    def generate_code_file(self):
        self.logger.log(InfoLog("Starting code mix generation..."))
        cm = CodeMix(self.project_directory, self.config.ignore_files)
        code_mix = cm.build_repo_content()

        self.logger.log(InfoLog("Code mix generation completed."))
        self.doc_info.code_mix = code_mix
        self.progress_bar.update_task()

    def generate_global_info(self, compress_power: int = 4, max_symbols: int = 10000):
        full_code_mix = self.doc_info.code_mix
        data = split_data(full_code_mix, max_symbols)

        global_result = compress_to_one(data, self.llm_model, self.config.get_project_settings(), compress_power=compress_power, progress_bar=self.progress_bar)
        self.doc_info.global_info = global_result

        with open(self.get_file_path("global_info"), "w", encoding="utf-8") as file:
            file.write(global_result)

        self.progress_bar.update_task()

    def generete_doc_parts(self, max_symbols=5_000, with_global_file: bool = False):
        full_code_mix = self.doc_info.code_mix
        global_file = self.doc_info.global_info if with_global_file else None

        global_file = self.read_file_by_file_key("global_info")

        self.logger.log(InfoLog("Starting synchronous documentation generation by parts..."))
        result = gen_doc_parts(full_code_mix,
                                max_symbols, self.llm_model, self.config.get_project_settings(),
                                self.config.language, self.progress_bar, global_info=global_file)
        
        with open(self.get_file_path("output_doc"), "w", encoding="utf-8") as file:
            file.write(result)
        result = split_text_by_anchors(result)
        
        for el in result:
            self.doc_info.doc.add_parts(el, DocContent(content=result[el]))


        self.logger.log(InfoLog("Documentation generation by parts completed."))
        self.progress_bar.update_task()

    def factory_generate_doc(self, doc_factory: DocFactory, to_start: bool = False): #TODO rewrite to new arc
        curr_doc = self.doc_info.doc.get_full_doc()
        code_mix = self.doc_info.code_mix
        global_info = self.doc_info.global_info


        info = {
            "language": self.config.language,
            "full_data": curr_doc,
            "code_mix": code_mix,
            "global_info": global_info
        }

        self.logger.log(InfoLog(f"""Starting factory documentation generation \n
                                {" ".join([type(module).__name__ for module in doc_factory.modules])} \n
                                Input params: {" ".join([f"{key}" for key, value in info.items()])}
                                """))

        result = doc_factory.generate_doc(info, self.llm_model, self.progress_bar)
        self.logger.log(InfoLog("Factory documentation generation completed."))
        if to_start:
            self.doc_info.doc = result + self.doc_info.doc
        else:
            self.doc_info.doc = self.doc_info.doc + result

        self.progress_bar.update_task()

    def order_doc(self):
        result = get_order(self.llm_model, self.doc_info.doc.content_orders)
        self.doc_info.doc.content_orders = result

    def clear_cache(self):
        if not self.config.pbc.save_logs:
            os.remove(self.get_file_path("logs"))
    
    def save(self) -> None:
        with open(self.get_file_path("output_doc"), "w", encoding="utf-8") as file:
            file.write(self.doc_info.doc.get_full_doc())