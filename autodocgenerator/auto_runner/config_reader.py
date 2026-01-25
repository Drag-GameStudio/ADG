import yaml
from autodocgenerator.factory.modules.general_modules import CustomModule
from autodocgenerator.preprocessor.settings import ProjectSettings
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.intro import IntroLinks, IntroText

class ProjectConfigSettings:
    save_logs = False
    log_level = -1
    def load_settings(self, data: dict[str, any]):
        for key, el in data.items():
            setattr(self, key, el)



class Config:
    def __init__(self):
        self.ignore_files: list[str] = [    "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db", "data",
        "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore", ".ruff_cache", ".auto_doc_cache",
        "*.pyc", "__pycache__", ".git", ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles", ".mypy_cache"
    ]
        self.language: str = "en"
        self.project_name: str = ""
        self.project_additional_info: dict = {}
        self.custom_modules: list[CustomModule] = []
        self.pcs: ProjectConfigSettings = ProjectConfigSettings()

    def set_language(self, language: str):
        self.language = language
        return self
    
    def set_pcs(self, pcs: ProjectConfigSettings):
        self.pcs = pcs
        return self
    
    def set_project_name(self, name: str):
        self.project_name = name
        return self
    
    def add_project_additional_info(self, key: str, value: str):
        self.project_additional_info[key] = value
        return self
    
    def add_ignore_file(self, pattern: str):
        self.ignore_files.append(pattern)
        return self
    
    def add_custom_module(self, custom_module: CustomModule):
        self.custom_modules.append(custom_module)
        return self
    
    def get_project_settings(self):
        settings = ProjectSettings(self.project_name)
        for key in self.project_additional_info:
            settings.add_info(key, self.project_additional_info[key])
        return settings

    def get_doc_factory(self):
        docFactory = DocFactory(*self.custom_modules)
        return docFactory, DocFactory(
            IntroLinks(),
            # IntroText(),
        )

def read_config(file_data: str) -> Config:
    data = yaml.safe_load(file_data)

    config : Config = Config()

    ignore_files = data.get("ignore_files", [])
    language = data.get("language", "en")

    project_name = data.get("project_name")
    project_additional_info = data.get("project_additional_info", {})

    project_settings = data.get("project_settings", {})
    pcs = ProjectConfigSettings()
    pcs.load_settings(project_settings)
    
    config.set_language(language).set_project_name(project_name).set_pcs(pcs)

    for pattern in ignore_files:
        config.add_ignore_file(pattern)

    for key in project_additional_info:
        config.add_project_additional_info(key, project_additional_info[key])

    custom_discriptions = data.get("custom_descriptions", [])


    for custom_discription in custom_discriptions:
        config.add_custom_module(CustomModule(custom_discription))

    return config