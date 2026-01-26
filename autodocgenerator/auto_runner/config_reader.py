import yaml
from autodocgenerator.factory.modules.general_modules import CustomModule
from ..config.config import Config, ProjectConfigSettings



def read_config(file_data: str) -> tuple[Config, list[CustomModule]]:
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

    custom_modules = [CustomModule(custom_discription) for custom_discription in custom_discriptions]

    return config, custom_modules