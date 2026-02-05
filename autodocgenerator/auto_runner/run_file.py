from autodocgenerator.manage import Manager
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.general_modules import CustomModule, CustomModuleWithOutContext
from autodocgenerator.factory.modules.intro import IntroLinks
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.auto_runner.config_reader import Config, read_config, StructureSettings
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.engine.config.config import API_KEY


def gen_doc(project_path: str, 
            config: Config, 
            custom_modules: list[CustomModule | CustomModuleWithOutContext], 
            structure_settings: StructureSettings) -> str:
    
    sync_model = GPTModel(API_KEY, use_random=False)
    async_model = AsyncGPTModel(API_KEY)
    
    manager = Manager(
        project_path, 
        config=config,
        sync_model=sync_model,
        async_model=async_model,
        progress_bar=ConsoleGtiHubProgress(), 
    )


    manager.generate_code_file()
    if config.pbc.use_global_file:
        manager.generate_global_info(compress_power=4)
        
    manager.generete_doc_parts(max_symbols=structure_settings.max_doc_part_size, with_global_file=config.pbc.use_global_file)
    manager.factory_generate_doc(DocFactory(*custom_modules))
    if structure_settings.include_order:
        manager.order_doc()
    
    if structure_settings.include_intro_links:
        manager.factory_generate_doc(DocFactory(IntroLinks()))
    manager.clear_cache()

    return manager.read_file_by_file_key("output_doc")

if __name__ == "__main__":
    with open("autodocconfig.yml", "r", encoding="utf-8") as file:
        config_data = file.read()
    config, custom_modules, structure_settings = read_config(config_data)

    output_doc = gen_doc(
        ".",
        config,
        custom_modules,
        structure_settings
    )

    



