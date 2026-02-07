import yaml
from autodocgenerator.factory.modules.general_modules import CustomModule, CustomModuleWithOutContext
from ..config.config import Config, ProjectBuildConfig


class StructureSettings:
    include_intro_links = True
    include_order = True
    use_global_file = True
    max_doc_part_size = 5_000
    include_intro_text = True

    def load_settings(self, data: dict[str, any]):
        for key, el in data.items():
            setattr(self, key, el)


def read_config(file_data: str) -> tuple[Config, list[CustomModule], StructureSettings]:
    data = yaml.safe_load(file_data)
    config : Config = Config()

    ignore_files = data.get("ignore_files", [])
    language = data.get("language", "en")

    project_name = data.get("project_name")
    project_additional_info = data.get("project_additional_info", {})

    project_settings = data.get("build_settings", {})
    pcs = ProjectBuildConfig()
    pcs.load_settings(project_settings)
    
    config.set_language(language).set_project_name(project_name).set_pcs(pcs)

    for pattern in ignore_files:
        config.add_ignore_file(pattern)

    for key in project_additional_info:
        config.add_project_additional_info(key, project_additional_info[key])

    custom_discriptions = data.get("custom_descriptions", [])

    custom_modules = [CustomModuleWithOutContext(custom_discription[1:])  if custom_discription[0] == "%" else CustomModule(custom_discription) for custom_discription in custom_discriptions]

    structure_settings = data.get("structure_settings", {})
    structure_settings_object = StructureSettings()
    structure_settings_object.load_settings(structure_settings)

    return config, custom_modules, structure_settings_object