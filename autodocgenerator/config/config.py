from ..factory.modules.general_modules import CustomModule
from ..preprocessor.settings import ProjectSettings
from ..factory.base_factory import DocFactory
from ..factory.modules.intro import IntroLinks


class ProjectBuildConfig:
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
        self.pbc: ProjectBuildConfig = ProjectBuildConfig()

    def set_language(self, language: str):
        self.language = language
        return self
    
    def set_pcs(self, pcs: ProjectBuildConfig):
        self.pbc = pcs
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
    
    
    def get_project_settings(self):
        settings = ProjectSettings(self.project_name)
        for key in self.project_additional_info:
            settings.add_info(key, self.project_additional_info[key])
        return settings
