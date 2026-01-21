## Executive Navigation Tree
* 📂 Core Engine
  * [Manager Class Usage](#Manager_Class_Usage)
  * [AutoDoc Config](#autodocconfig)
  * [AutoDoc Generator](#autodocgenerator)
* ⚙️ Components
  * [GPT Model Component](#gpt_model_component)
  * [Compressor Component](#compressor-component)
  * [Post Process Module](#postprocess_module)
* 📄 Modules
  * [Settings Module](#settings_module)
  * [Splitter Module](#spliter_module)
  * [UI Module](#ui_module)
* 📊 Example Usage
  * [Example Usage DocFactory](#example_usage_DocFactory)

**Project Overview: Auto Doc Generator**

## **Project Title**
Auto Doc Generator

## **Project Goal**
The Auto Doc Generator project aims to assist developers in creating documentation for their software projects. It provides a customizable solution for generating high-quality documentation, leveraging the power of AI-powered GPT models to automate the process. The primary goal of this project is to simplify the documentation creation process, saving developers time and effort.

## **Core Logic & Principles**
The Auto Doc Generator project operates based on the following core logic and principles:

* The project architecture consists of multiple modules, including `engine.models`, `factory`, `manage`, `preprocessor`, and `ui`. These modules work together to provide a comprehensive documentation generation solution.
* The project utilizes a configuration file (`autodocconfig.yml`) to specify project settings, custom modules, and other details.
* The `Manager` class serves as the central component, orchestrating the documentation generation process. It initializes project settings, models, and progress bars to ensure a seamless experience.
* The `GPTModel` and `AsyncGPTModel` classes are used for text generation, enabling the creation of high-quality documentation.
* The project employs a document factory to generate documentation, allowing for customization and flexibility.
* The logic flow begins with reading the configuration file, creating project settings, and initializing the manager class. The manager then generates documentation by calling various methods, such as `generate_code_file`, `generate_global_info_file`, and `generate_doc_parts`.

## **Key Features**
The Auto Doc Generator project offers the following key features:

* Customizable documentation generation using a configuration file
* Support for multiple GPT models, including synchronous and asynchronous options
* Automatic text generation for code files and global information files
* Progress bar display for monitoring documentation generation progress
* Flexible document factory for generating customized documentation
* Post-processing capabilities for generated descriptions

## **Dependencies**
To run the Auto Doc Generator project, the following dependencies are required:

* `autodocgenerator` package
* `GPTModel` and `AsyncGPTModel` libraries
* `rich` library for progress bar display
* `pyyaml` library for configuration file parsing
* `python` 3.8 or later (recommended)

 

<a name='Manager Class Usage'> </a>
The Manager class is used in the autodocgenerator/auto_runner/run_file.py file. 

To use the Manager class, you need to provide the following parameters:
- project_path: the path to the project
- project_settings: an instance of the ProjectSettings class
- sync_model: an instance of the GPTModel class
- async_model: an instance of the AsyncGPTModel class
- ignore_files: a list of file patterns to ignore
- progress_bar: an instance of the LibProgress class
- language: the language to use

Here is an example of how to use the Manager class:
```python
sync_model = GPTModel(API_KEY)
async_model = AsyncGPTModel(API_KEY)
manager = Manager(
    project_path ".", 
    project_settings=project_settings, 
    sync_model=sync_model,
    async_model=async_model,
    ignore_files=ignore_list, 
    progress_bar=LibProgress(progress), 
    language="en"
)
```
You can then call various methods on the manager object, such as:
- generate_code_file()
- generate_global_info_file(use_async=False, max_symbols=8000)
- generete_doc_parts(use_async=False, max_symbols=4000)
- factory_generate_doc(doc_factory)
- read_file_by_file_key("output_doc") 

For example:
```python
manager.generate_code_file()
manager.generate_global_info_file(use_async=False, max_symbols=8000)
manager.generete_doc_parts(use_async=False, max_symbols=4000)
manager.factory_generate_doc(doc_factory)
manager.factory_generate_doc(intro_factory)
output_doc = manager.read_file_by_file_key("output_doc")
```

<a name='example_usage_DocFactory'> </a>
To create a DocFactory instance with different modules, you can pass various modules to its constructor. 

Here is an example:
```python
doc_factory = DocFactory(
    IntroLinks(),
    IntroText(),
    CustomModule("custom_description")
)
```
In this example, `DocFactory` is initialized with `IntroLinks`, `IntroText`, and a `CustomModule` instance. 

Another example:
```python
doc_factory = DocFactory(
    IntroLinks(),
    CustomModule("another_custom_description")
)
```
In this case, `DocFactory` is created with `IntroLinks` and another `CustomModule` instance.

The `autodocgenerator/auto_runner/config_reader.py` file provides more information about how `Config` class creates `DocFactory` instances with different modules:
```python
def get_doc_factory(self):
    docFactory = DocFactory(*self.custom_modules)
    return docFactory, DocFactory(
        IntroLinks(),
        IntroText(),
    )
```
It shows that `DocFactory` can be created with custom modules and with `IntroLinks` and `IntroText` modules.

Also, in the `autodocgenerator/auto_runner/run_file.py` file, there is an example of using `DocFactory` with `gen_doc` function:
```python
manager.factory_generate_doc(doc_factory)
manager.factory_generate_doc(intro_factory)
```
Here, `doc_factory` and `intro_factory` are `DocFactory` instances created with different modules.

<a name='autodocconfig'> </a>
To write an autodocconfig.yml file, the following options are available based on the provided context:

1. **project_name**: This option is used to specify the name of the project. 
   Example: `project_name: "Auto Doc Generator"`

2. **language**: This option is used to specify the language of the project. The default language is "en".
   Example: `language: "en"`

3. **project_additional_info**: This option is used to add additional information about the project.
   Example: 
   ```
   project_additional_info:
     global idea: "This project was created to help developers make documentations for them projects"
   ```

4. **ignore_files**: This option is used to specify files or patterns to be ignored.
   Example: 
   ```
   ignore_files:
     - "*.pyo"
     - "*.pyd"
     - "*.pdb"
   ```

5. **custom_descriptions**: This option is used to add custom descriptions for the project.
   Example: 
   ```
   custom_descriptions:
     - "how to use Manager class what parameters i need to give. give full example of usage"
     - "give me examples of usage for DocFactory with different modules"
   ```

Here's an example of what the autodocconfig.yml file might look like:
```
project_name: "Auto Doc Generator"
language: "en"

project_additional_info:
  global idea: "This project was created to help developers make documentations for them projects"

custom_descriptions:
  - "how to use Manager class what parameters i need to give. give full example of usage"
  - "give me examples of usage for DocFactory with different modules"
```

 

<a name="autodocgenerator_component"></a>
## Autodocgenerator Component
The Autodocgenerator component is a crucial part of the overall system, responsible for generating documentation for projects. This component interacts with other parts of the system, such as the CI/CD workflow and the autodocconfig.yml configuration file.

### Responsibility
The Autodocgenerator component is responsible for:
* Generating documentation for projects based on the autodocconfig.yml configuration file.
* Providing examples of usage for various classes and modules, such as the Manager class and DocFactory.
* Writing the autodocconfig.yml file and explaining the available options.

### Key Functions and Classes
* `auto_runner/run_file.py`: This script runs the documentation generation process.
* `factory/base_factory.py`: This module provides a base factory for generating documentation.
* `engine/models/gpt_model.py`: This module contains the GPT model used for generating documentation.
* `config/config.py`: This module contains the configuration for the Autodocgenerator component.

### Logic Flow
The Autodocgenerator component works as follows:
1. The CI/CD workflow triggers the documentation generation process.
2. The `auto_runner/run_file.py` script reads the autodocconfig.yml configuration file and starts the documentation generation process.
3. The Autodocgenerator component uses the GPT model and other modules to generate the documentation.
4. The generated documentation is written to the README.md file.

### Important Assumptions and Inputs
* The autodocconfig.yml configuration file is assumed to be present and correctly formatted.
* The API key and other secrets are assumed to be securely stored and passed to the Autodocgenerator component as environment variables.
* The input to the Autodocgenerator component is the autodocconfig.yml configuration file and the project code.

### Outputs and Side Effects
* The output of the Autodocgenerator component is the generated documentation written to the README.md file.
* The side effects of the Autodocgenerator component include the creation of the README.md file and the update of the GitHub repository.

<a name="autodocgenerator"></a>
## Autodocgenerator Component

The Autodocgenerator component is responsible for generating documentation for a given project. It uses the GPT model and other modules to generate the documentation.

### Responsibility

The responsibility of this component is to:

* Read the configuration file `autodocconfig.yml` and parse its contents
* Generate documentation for the project using the GPT model and other modules
* Write the generated documentation to the `README.md` file

### Interactions with Other Parts of the System

The Autodocgenerator component interacts with the following parts of the system:

* **Config Reader**: The Config Reader module reads the `autodocconfig.yml` configuration file and parses its contents.
* **GPT Model**: The GPT model is used to generate the documentation.
* **Manager**: The Manager module is responsible for managing the generation of the documentation.
* **Doc Factory**: The Doc Factory module is responsible for generating the documentation.

### Key Functions, Classes, and Logic Flows

The key functions, classes, and logic flows in this component are:

* **`Config` class**: This class represents the configuration of the Autodocgenerator component.
* **`read_config` function**: This function reads the `autodocconfig.yml` configuration file and returns a `Config` object.
* **`gen_doc` function**: This function generates the documentation for the project.
* **`Manager` class**: This class is responsible for managing the generation of the documentation.

### Important Assumptions, Inputs, Outputs, and Side Effects

The important assumptions, inputs, outputs, and side effects of this component are:

* **Assumptions**: The `autodocconfig.yml` configuration file is assumed to be present and correctly formatted.
* **Inputs**: The input to the Autodocgenerator component is the `autodocconfig.yml` configuration file and the project code.
* **Outputs**: The output of the Autodocgenerator component is the generated documentation written to the `README.md` file.
* **Side Effects**: The side effects of the Autodocgenerator component include the creation of the `README.md` file and the update of the GitHub repository.

### Usage

To use this component, simply run the `run_file.py` script. This will read the `autodocconfig.yml` configuration file, generate the documentation, and write it to the `README.md` file.

Example usage:
```bash
python run_file.py
```
This will generate the documentation for the project and write it to the `README.md` file.

<a name="gpt_model_component"></a>
## GPT Model Component

The GPT Model component is responsible for generating answers to user prompts using the GPT model. It interacts with the `model.py` file, which provides the base classes for the models, and the `config.py` file, which provides the configuration settings.

### Key Functions and Classes

* `AsyncGPTModel` and `GPTModel` classes: These classes inherit from `AsyncModel` and `Model` respectively, and provide the implementation for generating answers using the GPT model.
* `generate_answer` method: This method takes a prompt and generates an answer using the GPT model.
* `get_answer` method: This method adds the user prompt to the history and generates an answer using the GPT model.
* `History` class: This class is used to store the conversation history.

### Logic Flow

1. The `AsyncGPTModel` or `GPTModel` class is initialized with an API key and a history object.
2. The `generate_answer` method is called with a prompt and the `with_history` flag.
3. If `with_history` is True, the method uses the conversation history to generate an answer. Otherwise, it uses the provided prompt.
4. The method tries to generate an answer using the GPT model. If it fails, it tries the next model in the list.
5. If all models fail, it raises an exception.

### Important Assumptions and Inputs

* The API key is assumed to be valid and configured in the `config.py` file.
* The `MODELS_NAME` list is assumed to be configured in the `config.py` file.
* The `History` class is assumed to be initialized with a system prompt.
* The `generate_answer` method assumes that the prompt is a string or a list of dictionaries.

### Outputs and Side Effects

* The `generate_answer` method returns a string answer.
* The `get_answer` method adds the user prompt and the model answer to the conversation history.
* The `History` class stores the conversation history in memory. 

### Usage

To use the GPT Model component, create an instance of the `AsyncGPTModel` or `GPTModel` class and call the `generate_answer` or `get_answer` method. For example:
```python
gpt_model = GPTModel()
answer = gpt_model.get_answer("Hello, how are you?")
```
Note that the `AsyncGPTModel` class is asynchronous and should be used with the `await` keyword. For example:
```python
async def main():
    gpt_model = AsyncGPTModel()
    answer = await gpt_model.get_answer("Hello, how are you?")
```

<a name="autodocgenerator_documentation"></a>
## Autodocgenerator Documentation
The Autodocgenerator system is a tool for generating documentation for software projects. The code provided is a part of this system, responsible for generating specific parts of the documentation.

### Base Factory Module
The `BaseFactory` module, located in `autodocgenerator/factory/base_factory.py`, serves as the foundation for the documentation generation process. It defines the `BaseModule` abstract class, which specifies the `generate` method that must be implemented by all concrete module classes.

The `DocFactory` class is responsible for orchestrating the generation of documentation parts by multiple modules. It takes a variable number of `BaseModule` instances in its constructor and provides the `generate_doc` method, which iterates over the modules, calls their `generate` methods, and combines the results into a single output string.

### Module Implementations
Concrete module implementations, such as `CustomModule`, `IntroLinks`, and `IntroText`, are located in `autodocgenerator/factory/modules/general_modules.py` and `autodocgenerator/factory/modules/intro.py`. These modules inherit from `BaseModule` and provide their own implementations of the `generate` method, which generates specific parts of the documentation.

### Code Mix Preprocessor
The `CodeMix` class, defined in `autodocgenerator/preprocessor/code_mix.py`, is a preprocessor that extracts code from a repository and generates a mixed code file. It takes a root directory and ignore patterns as input and produces a file containing the repository structure and code.

### Key Functions and Logic Flows
* `DocFactory.generate_doc`: Generates documentation by iterating over modules and combining their outputs.
* `BaseModule.generate`: Abstract method that must be implemented by concrete module classes to generate specific parts of the documentation.
* `CodeMix.build_repo_content`: Extracts code from a repository and generates a mixed code file.

### Important Assumptions and Inputs
* The system assumes that the `info` dictionary passed to the `generate` method contains relevant data, such as `code_mix` and `language`.
* The `model` parameter passed to the `generate` method is an instance of `Model` or `AsyncModel`.
* The `progress` object passed to the `generate_doc` method is an instance of `BaseProgress`, which provides progress tracking functionality.

### Outputs and Side Effects
* The `generate_doc` method returns a string containing the generated documentation.
* The `build_repo_content` method generates a file containing the mixed code.
* The system may print error messages or progress updates to the console.

## <a name="compressor-component"></a>Compressor Component
The Compressor component is responsible for reducing the size of input data using a compression algorithm. It interacts with the Model component to generate compressed text and the Progress Bar component to display progress updates.

### Key Functions
* `compress(data, project_settings, model, compress_power)`: Compresses a single string of data using the provided model and compress power.
* `compress_and_compare(data, model, project_settings, compress_power, progress_bar)`: Compresses a list of data using the provided model and compress power, and compares the results.
* `async_compress(data, project_settings, model, compress_power, semaphore, progress_bar)`: Asynchronously compresses a single string of data using the provided model and compress power.
* `async_compress_and_compare(data, model, project_settings, compress_power, progress_bar)`: Asynchronously compresses a list of data using the provided model and compress power, and compares the results.
* `compress_to_one(data, model, project_settings, compress_power, use_async, progress_bar)`: Recursively compresses a list of data until only one element remains.
* `generate_discribtions_for_code(data, model, project_settings, progress_bar)`: Generates descriptions for a list of code files using the provided model and project settings.

### Logic Flow
1. The `compress` function takes in a string of data, project settings, a model, and a compress power, and returns the compressed text.
2. The `compress_and_compare` function takes in a list of data, a model, project settings, a compress power, and a progress bar, and returns a list of compressed and compared text.
3. The `async_compress` and `async_compress_and_compare` functions are asynchronous versions of the `compress` and `compress_and_compare` functions, respectively.
4. The `compress_to_one` function recursively compresses a list of data until only one element remains.
5. The `generate_discribtions_for_code` function generates descriptions for a list of code files using the provided model and project settings.

### Important Assumptions
* The input data is a string or a list of strings.
* The model is an instance of the `Model` or `AsyncModel` class.
* The project settings are an instance of the `ProjectSettings` class.
* The progress bar is an instance of the `BaseProgress` class.

### Inputs and Outputs
* `compress`: input - `data` (str), `project_settings` (ProjectSettings), `model` (Model), `compress_power` (int); output - `compressed_text` (str)
* `compress_and_compare`: input - `data` (list), `model` (Model), `project_settings` (ProjectSettings), `compress_power` (int), `progress_bar` (BaseProgress); output - `compressed_and_compared_text` (list)
* `async_compress`: input - `data` (str), `project_settings` (ProjectSettings), `model` (AsyncModel), `compress_power` (int), `semaphore` (asyncio.Semaphore), `progress_bar` (BaseProgress); output - `compressed_text` (str)
* `async_compress_and_compare`: input - `data` (list), `model` (AsyncModel), `project_settings` (ProjectSettings), `compress_power` (int), `progress_bar` (BaseProgress); output - `compressed_and_compared_text` (list)
* `compress_to_one`: input - `data` (list), `model` (Model), `project_settings` (ProjectSettings), `compress_power` (int), `use_async` (bool), `progress_bar` (BaseProgress); output - `compressed_text` (str)
* `generate_discribtions_for_code`: input - `data` (list), `model` (Model), `project_settings` (ProjectSettings), `progress_bar` (BaseProgress); output - `descriptions` (list)

### Side Effects
* The `compress` and `async_compress` functions may print error messages or progress updates to the console.
* The `compress_and_compare` and `async_compress_and_compare` functions may print error messages or progress updates to the console.
* The `compress_to_one` function may print error messages or progress updates to the console.
* The `generate_discribtions_for_code` function may print error messages or progress updates to the console.

<a name="postprocess_module"></a>
## Postprocess Module
The postprocess module is responsible for generating markdown anchors, extracting topics and links, and creating introductions and custom descriptions for the provided data.

### Functions
* `generate_markdown_anchor(header: str) -> str`: Generates a markdown anchor from the provided header.
* `get_all_topics(data: str) -> list[str]`: Extracts all topics from the provided data and returns them along with their corresponding links.
* `get_all_html_links(data: str) -> list[str]`: Extracts all HTML links from the provided data.
* `get_links_intro(links: list[str], model: Model, language: str = "en")`: Generates an introduction for the provided links using the given model and language.
* `get_introdaction(global_data: str, model: Model, language: str = "en") -> str`: Generates an introduction for the provided global data using the given model and language.
* `generete_custom_discription(splited_data: str, model: Model, custom_description: str, language: str = "en") -> str`: Generates a custom description for the provided data using the given model, custom description, and language.

### Interactions with Other Modules
The postprocess module interacts with the `settings` module through the `ProjectSettings` class, which is used to generate a prompt for the model. It also interacts with the `model` module through the `Model` class, which is used to generate answers without history.

### Key Logic Flows
1. The `generate_markdown_anchor` function generates a markdown anchor from the provided header by normalizing the text, replacing spaces with hyphens, and removing any non-alphanumeric characters.
2. The `get_all_topics` function extracts all topics from the provided data by finding all occurrences of "\n## " and extracting the text that follows.
3. The `get_links_intro` function generates an introduction for the provided links by creating a prompt for the model and getting the answer without history.
4. The `get_introdaction` function generates an introduction for the provided global data by creating a prompt for the model and getting the answer without history.
5. The `generete_custom_discription` function generates a custom description for the provided data by creating a prompt for the model and getting the answer without history.

### Important Assumptions
* The input data is a string or a list of strings.
* The model is an instance of the `Model` class.
* The language is a string that represents the language to be used for the task.

### Inputs and Outputs
* `generate_markdown_anchor`: input - `header` (str), output - `anchor` (str)
* `get_all_topics`: input - `data` (str), output - `topics` (list[str]), `links` (list[str])
* `get_all_html_links`: input - `data` (str), output - `links` (list[str])
* `get_links_intro`: input - `links` (list[str]), `model` (Model), `language` (str), output - `intro_links` (str)
* `get_introdaction`: input - `global_data` (str), `model` (Model), `language` (str), output - `intro` (str)
* `generete_custom_discription`: input - `splited_data` (str), `model` (Model), `custom_description` (str), `language` (str), output - `result` (str)

### Side Effects
* The `get_links_intro`, `get_introdaction`, and `generete_custom_discription` functions may print error messages or progress updates to the console. 

<a name="settings_module"></a>
## Settings Module
The settings module is responsible for representing project settings, including the project name and additional information.

### Classes
* `ProjectSettings`: Represents project settings, including the project name and additional information.

### Methods
* `__init__(project_name: str)`: Initializes the project settings with the given project name.
* `add_info(key, value)`: Adds additional information to the project settings.
* `prompt`: Generates a prompt for the model based on the project settings.

### Interactions with Other Modules
The settings module interacts with the `postprocess` module through the `ProjectSettings` class, which is used to generate a prompt for the model.

### Key Logic Flows
1. The `__init__` method initializes the project settings with the given project name.
2. The `add_info` method adds additional information to the project settings.
3. The `prompt` property generates a prompt for the model based on the project settings.

### Important Assumptions
* The project name is a string.
* The additional information is a dictionary of key-value pairs.

### Inputs and Outputs
* `__init__`: input - `project_name` (str)
* `add_info`: input - `key`, `value`
* `prompt`: output - `prompt` (str)

### Side Effects
* The `prompt` property may print error messages or progress updates to the console.

<a name="spliter_module"></a>
## Spliter Module
The spliter module is responsible for splitting the input data into smaller parts and generating documentation for each part using a model.

### Classes
* None

### Methods
* `split_data(data: str, max_symbols: int) -> list[str]`: Splits the input data into smaller parts based on the maximum number of symbols allowed.
* `write_docs_by_parts(part: str, model: Model, global_info: str, prev_info: str = None, language: str = "en")`: Generates documentation for a given part using a model.
* `async_write_docs_by_parts(part: str, async_model: AsyncModel, global_info: str, semaphore, prev_info: str = None, language: str = "en", update_progress = None)`: Asynchronously generates documentation for a given part using an asynchronous model.
* `gen_doc_parts(full_code_mix, global_info, max_symbols, model: Model, language, progress_bar: BaseProgress)`: Generates documentation for the input data by splitting it into smaller parts and using a model to generate documentation for each part.
* `async_gen_doc_parts(full_code_mix, global_info, max_symbols, model: AsyncModel, language, progress_bar: BaseProgress)`: Asynchronously generates documentation for the input data by splitting it into smaller parts and using an asynchronous model to generate documentation for each part.

### Interactions with Other Modules
The spliter module interacts with the `engine` module through the `Model` and `AsyncModel` classes, which are used to generate documentation for each part. It also interacts with the `ui` module through the `BaseProgress` class, which is used to display progress updates.

### Key Logic Flows
1. The `split_data` method splits the input data into smaller parts based on the maximum number of symbols allowed.
2. The `write_docs_by_parts` method generates documentation for a given part using a model.
3. The `gen_doc_parts` method generates documentation for the input data by splitting it into smaller parts and using a model to generate documentation for each part.
4. The `async_gen_doc_parts` method asynchronously generates documentation for the input data by splitting it into smaller parts and using an asynchronous model to generate documentation for each part.

### Important Assumptions
* The input data is a string.
* The model is an instance of the `Model` or `AsyncModel` class.
* The language is a string that represents the language to be used for the task.

### Inputs and Outputs
* `split_data`: input - `data` (str), `max_symbols` (int), output - `split_objects` (list[str])
* `write_docs_by_parts`: input - `part` (str), `model` (Model), `global_info` (str), `prev_info` (str), `language` (str), output - `answer` (str)
* `async_write_docs_by_parts`: input - `part` (str), `async_model` (AsyncModel), `global_info` (str), `semaphore`, `prev_info` (str), `language` (str), `update_progress`, output - `answer` (str)
* `gen_doc_parts`: input - `full_code_mix`, `global_info`, `max_symbols`, `model` (Model), `language`, `progress_bar` (BaseProgress), output - `all_result` (str)
* `async_gen_doc_parts`: input - `full_code_mix`, `global_info`, `max_symbols`, `model` (AsyncModel), `language`, `progress_bar` (BaseProgress), output - `result` (str)

### Side Effects
* The `write_docs_by_parts` and `async_write_docs_by_parts` methods may print error messages or progress updates to the console.
* The `gen_doc_parts` and `async_gen_doc_parts` methods may display progress updates using the `BaseProgress` class.

<a name="ui_module"></a>
## UI Module
The UI module is responsible for handling the user interface and progress updates for the autodocgenerator project. It provides a BaseProgress class that defines the interface for progress updates, and a LibProgress class that implements this interface using the rich.progress library.

### Key Classes and Methods
* `BaseProgress`: The base class for progress updates, defining the interface for creating new subtasks, updating tasks, and removing subtasks.
* `LibProgress`: A concrete implementation of the BaseProgress class, using the rich.progress library to display progress updates.
	+ `__init__`: Initializes the LibProgress object with a Progress object and a total number of tasks.
	+ `create_new_subtask`: Creates a new subtask with a given name and total length.
	+ `update_task`: Updates the current task or subtask.
	+ `remove_subtask`: Removes the current subtask.

### Interactions with Other Modules
The UI module interacts with the `engine` module through the `gen_doc_parts` and `async_gen_doc_parts` functions, which use the BaseProgress class to display progress updates.

### Important Assumptions
* The input data is a string.
* The model is an instance of the `Model` or `AsyncModel` class.
* The language is a string that represents the language to be used for the task.

### Inputs and Outputs
* `BaseProgress`: input - `name` (str), `total_len` (int), output - None
* `LibProgress`: input - `progress` (Progress), `total` (int), output - None

### Side Effects
* The `LibProgress` class may display progress updates to the console using the rich.progress library.

