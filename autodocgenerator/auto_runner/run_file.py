from autodocgenerator.manage import Manager, split_text_by_anchors, DocContent
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.general_modules import CustomModule, CustomModuleWithOutContext
from autodocgenerator.factory.modules.intro import IntroLinks, IntroText, BaseModule
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.auto_runner.config_reader import Config, read_config, StructureSettings
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.engine.config.config import API_KEYS


def gen_doc(project_path: str, 
            config: Config, 
            custom_modules: list[BaseModule], 
            structure_settings: StructureSettings) -> str:
    
    sync_model = GPTModel(API_KEYS, use_random=False)
    
    manager = Manager(
        project_path, 
        config=config,
        llm_model=sync_model,
        progress_bar=ConsoleGtiHubProgress(), 
    )
  

    
    manager.generate_code_file()
    if structure_settings.use_global_file:
        manager.generate_global_info(compress_power=4)
    
    manager.generete_doc_parts(max_symbols=structure_settings.max_doc_part_size, with_global_file=structure_settings.use_global_file)
   

    manager.factory_generate_doc(DocFactory(*custom_modules))
    if structure_settings.include_order:
        manager.order_doc()
    
    additionals_modules: list[BaseModule] = []

    if structure_settings.include_intro_text:
        additionals_modules.append(IntroText())

    if structure_settings.include_intro_links:
        additionals_modules.append(IntroLinks())

    
    manager.factory_generate_doc(DocFactory(*additionals_modules, with_splited=False), to_start=True)
    manager.clear_cache()

    manager.save()
    return manager.doc_info.doc.get_full_doc()

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

    



