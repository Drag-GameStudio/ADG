## Executive Navigation Tree
* 📂 Configuration
  * [AutoDoc Config](#autodocconfig.yml)
  * [Project Configuration](#project-configuration)
  * [Configuration Parsing](#configuration-parsing)
* ⚙️ AutoDoc Generator
  * [AutoDoc Generator Component](#autodoc-generator-component)
  * [AutoDoc Generator Architecture](#autodoc-generator-architecture)
  * [AutoDoc Generator Auto Runner](#autodocgenerator\\auto_runner\\run_file.py)
* 📄 Documentation
  * [Documentation Generation](#documentation-generation)
  * [Custom Introduction Generation](#custom-introduction-generation)
  * [Usage Example](#usage-example)
* 🤖 Technical Details
  * [Technical Details](#technical-details)
  * [GPT Model Implementation](#gpt-model-implementation)
  * [Data Flow](#data-flow)
  * [Model Exception Handling](#model-exception-handling)
* 📈 Utilities
  * [Compressor Module](#compressor-module)
  * [Logging Mechanism](#logging-mechanism)
  * [Logger Templates](#logger-templates)
  * [Progress Tracking](#progress-tracking)
  * [Manager Class](#manager-class)
* 📦 Installation
  * [Installation Scripts](#installation-scripts)

 

<a name='autodocconfig.yml'></a>
To install the workflow, you should use the following links: 
For PowerShell, use `irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex`. 
For Linux-based systems, use `curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash`. 
Additionally, you need to add a secret variable to your GitHub Action, `GROCK_API_KEY`, with your API key from Grock Docs (https://grockdocs.com) to make it work. 
<a name='autodocgenerator\auto_runner\run_file.py'></a>
To use the Manager class, you need to provide the following parameters: 
- project_path: the path to the project
- project_settings: an instance of ProjectSettings
- pcs: an instance of ProjectConfigSettings
- sync_model: an instance of GPTModel
- async_model: an instance of AsyncGPTModel
- ignore_files: a list of files to ignore
- progress_bar: an instance of a progress bar class (in this case, ConsoleGtiHubProgress)
- language: the language to use (in this case, "en")

Here is an example of usage:
```
sync_model = GPTModel(API_KEY, use_random=False)
async_model = AsyncGPTModel(API_KEY)

manager = Manager(
    project_path=".", 
    project_settings=project_settings,
    pcs=pcs, 
    sync_model=sync_model,
    async_model=async_model,
    ignore_files=ignore_list, 
    progress_bar=ConsoleGtiHubProgress(), 
    language="en"
)
```
You can then call various methods on the manager instance, such as:
```
manager.generate_code_file()
manager.generate_global_info_file(use_async=False, max_symbols=8000)
manager.generete_doc_parts(use_async=False, max_symbols=6000)
manager.factory_generate_doc(doc_factory)
manager.order_doc()
manager.factory_generate_doc(intro_factory)
```

<a name='autodocconfig.yml'> </a>
The autodocconfig.yml file has the following available options: 
- project_name: the name of the project
- language: the language of the project (default is "en")
- project_settings: 
  - save_logs: whether to save logs (default is False)
  - log_level: the level of logs (default is -1)
- project_additional_info: additional information about the project, where the key and value are both strings
- custom_descriptions: a list of custom descriptions, where each description is a string. 
These options are used to configure the Auto Doc Generator. 
<a name="autodoc-generator-component"></a>
## AutoDoc Generator Component
The AutoDoc Generator is a tool designed to automate the process of generating documentation for projects. 

### Component Responsibility
This component is responsible for creating and maintaining documentation for a given project, utilizing a configuration file (`autodocconfig.yml`) to guide the documentation generation process.

### Interactions
The AutoDoc Generator interacts with the project's repository, utilizing GitHub Actions to automate the documentation generation process. It also relies on the `autodocconfig.yml` file for configuration settings.

### Technical Details
Key functions and classes in this component include:
- `autodocgenerator.auto_runner.run_file`: The main entry point for the documentation generation process.
- `autodocgenerator.engine.config.config.py`: Handles configuration settings for the generator.
- `autodocgenerator.factory.base_factory.py`: Provides a base factory for creating documentation components.
- `autodocgenerator.ui.logging.py`: Offers logging functionality for the generator.

### Data Flow
The data flow for this component involves:
- **Input**: The `autodocconfig.yml` file, which provides configuration settings for the generator.
- **Processing**: The generator uses the configuration settings to create documentation for the project.
- **Output**: The generated documentation is saved as a Markdown file (`README.md`) in the project's repository.
- **Side Effects**: The generator also creates log files (`agd_report.txt`) to track any issues during the documentation generation process. 

### Configuration Settings
The `autodocconfig.yml` file contains the following configuration settings:
- `project_name`: The name of the project being documented.
- `language`: The language used for the documentation.
- `project_settings`: Additional settings for the project, such as log level and save logs.
- `custom_descriptions`: Custom descriptions for the project, including installation instructions and usage examples. 
<a name="autodoc-generator-architecture"></a>
## Autodoc Generator Architecture
The Autodoc generator is a complex system composed of multiple components. 

### 
<a name="configuration-parsing"></a>
## Configuration Parsing
The provided code snippet is responsible for parsing configuration files for the auto documentation generator.

### Config Class
The `Config` class is used to store configuration settings. It has the following properties:
- `ignore_files`: a list of file patterns to ignore
- `language`: the language used for documentation
- `project_name`: the name of the project being documented
- `project_additional_info`: additional information about the project
- `custom_modules`: a list of custom modules
- `pcs`: project configuration settings

The `Config` class also has methods to set these properties and to get project settings and a document factory.

### Reading Configuration
The `read_config` function reads configuration from a YAML file and returns a `Config` object. It parses the following settings:
- `ignore_files`
- `language`
- `project_name`
- `project_additional_info`
- `project_settings`
- `custom_descriptions`

### ProjectConfigSettings Class
The `ProjectConfigSettings` class is used to store project configuration settings. It has the following properties:
- `save_logs`: whether to save logs
- `log_level`: the log level

The `ProjectConfigSettings` class also has a method to load settings from a dictionary.

### Document Generation
The `gen_doc` function generates documentation for a project. It uses the following parameters:
- `project_settings`: project settings
- `pcs`: project configuration settings
- `ignore_list`: a list of files to ignore
- `project_path`: the path to the project
- `doc_factory`: a document factory
- `intro_factory`: an intro factory

The `gen_doc` function generates code files, global info files, and documentation parts, and then orders and generates the final documentation. 

### Main Function
The `main` function reads the configuration from the `autodocconfig.yml` file, generates documentation, and prints the output. 

### 
<a name="project-configuration"></a>
#### Project Configuration
The project configuration is defined in the `pyproject.toml` file. This file specifies the project's dependencies, version, and other metadata.

### 
<a name="installation-scripts"></a>
#### Installation Scripts
The installation scripts (`install.ps1`, `install.sh`) are used to set up the Autodoc generator. They create the necessary directories and files, including the `.github/workflows/autodoc.yml` file and the `autodocconfig.yml` file.

### 
<a name="documentation-generation"></a>
## Documentation Generation
The documentation generation module is responsible for generating documentation for a given code snippet. This module utilizes the `Model` and `AsyncModel` classes to generate documentation.

### Data Splitting
The `split_data` function splits the input data into smaller parts based on the `max_symbols` parameter. This is done to prevent excessive data from being processed at once.

### Documentation Generation by Parts
The `gen_doc_parts` function generates documentation for each part of the split data. It uses the `write_docs_by_parts` function to generate documentation for each part and then combines the results.

### Asynchronous Documentation Generation
The `async_gen_doc_parts` function generates documentation asynchronously using the `async_write_docs_by_parts` function. This allows for multiple parts to be processed concurrently, improving performance.

### Technical Details
The documentation generation module uses the following key functions and classes:
* `split_data`: Splits the input data into smaller parts based on the `max_symbols` parameter.
* `write_docs_by_parts`: Generates documentation for a single part of the split data.
* `gen_doc_parts`: Generates documentation for all parts of the split data.
* `async_write_docs_by_parts`: Generates documentation for a single part of the split data asynchronously.
* `async_gen_doc_parts`: Generates documentation for all parts of the split data asynchronously.

### Usage Example
```python
full_code_mix = "This is a sample code snippet."
global_info = "This is a sample global information."
max_symbols = 1000
model = Model()
language = "en"
progress_bar = BaseProgress()

result = gen_doc_parts(full_code_mix, global_info, max_symbols, model, language, progress_bar)
``` 
<a name="custom-introduction-generation"></a>
## Custom Introduction Generation
The custom introduction generation module is responsible for extracting HTML links from documentation, generating introductions with links, and creating custom descriptions.

### Functionality
The module consists of four main functions:
* `get_all_html_links`: Extracts HTML links from a given documentation string.
* `get_links_intro`: Generates an introduction with links using a provided model and language.
* `get_introdaction`: Creates an introduction based on global data, a model, and a language.
* `generete_custom_discription`: Generates a custom description for a given code or documentation snippet.

### Interactions
The custom introduction generation module interacts with the following components:
* `GPTModel`: For generating introductions and custom descriptions.
* `Model`: For generating introductions and custom descriptions.
* `BaseLogger`: For logging information and warnings.

### Data Flow
- **Input**: The module takes in documentation strings, models, languages, and custom description requests.
- **Output**: The module generates introductions with links, custom descriptions, and logs information and warnings.
- **Side Effects**: The module updates the log with information and warnings.

### Technical Details
The module uses regular expressions to extract HTML links from documentation strings. It also utilizes the `GPTModel` and `Model` classes to generate introductions and custom descriptions.

### Usage Example
```python
links = get_all_html_links(doc_string)
intro = get_links_intro(links, model, language="en")
custom_description = generete_custom_discription(code_snippet, model, custom_description_request)
``` 
<a name="usage-example"></a>
#### Usage Example
To use the Autodoc generator, simply run the installation script and follow the prompts. Once the Autodoc generator is set up, you can use it to generate documentation for your project. 

```python
# Create a new logger
logger = BaseLogger()

# Set the logger template
logger.set_logger(FileLoggerTemplate("log.txt"))

# Log a message
logger.log(InfoLog("This is an info message"))
``` 
<a name="technical-details"></a>
#### Technical Details
The Autodoc generator uses a variety of technologies, including Python, YAML, and Markdown. It also uses several libraries, including `pyyaml`, `anyio`, and `rich`. 

### 
<a name="gpt-model-implementation"></a>
## GPT Model Implementation
### Purpose
The GPT model implementation is designed to handle the generation of answers using the GPT model. It includes two classes: `AsyncGPTModel` and `GPTModel`, which inherit from `AsyncModel` and `Model` respectively.

### Technical Details
The `AsyncGPTModel` and `GPTModel` classes are defined in the `autodocgenerator\engine\models\gpt_model.py` file. They utilize the `Groq` and `AsyncGroq` clients to interact with the GPT model. The `logger` attribute is used to log information, warnings, and errors.

### Interactions
The GPT model implementation interacts with the `ModelExhaustedException` class to handle situations where no models are available for use. It also interacts with the `History` class to store and retrieve conversation history.

### Data Flow
- **Input**: The `generate_answer` method takes in `with_history` and `prompt` parameters.
- **Output**: The method returns the generated answer as a string.
- **Side Effects**: The method updates the conversation history and logs information, warnings, and errors.

### Usage Example
```python
gpt_model = AsyncGPTModel()
try:
    answer = await gpt_model.generate_answer(with_history=True, prompt="Hello, how are you?")
    print(answer)
except ModelExhaustedException as e:
    print(f"Error: {e}")
``` 
<a name="data-flow"></a>
#### Data Flow
The data flow of the Autodoc generator involves the following steps:
* The user runs the installation script to set up the Autodoc generator.
* The Autodoc generator reads the project's configuration from the `pyproject.toml` file.
* The Autodoc generator uses the `BaseLog` and `BaseLoggerTemplate` classes to handle logging.
* The Autodoc generator uses the `BaseProgress` class to track progress.
* The Autodoc generator generates documentation based on the project's configuration and code. 

### 
<a name="model-exception-handling"></a>
## Model Exception Handling
### Purpose
The `ModelExhaustedException` class is designed to handle situations where none of the models in the predefined list are available for use.

### Technical Details
This custom exception is defined in the `autodocgenerator\engine\exceptions.py` file. It inherits from the base `Exception` class, allowing it to be used as a specific error type in the code.

### Interactions
The `ModelExhaustedException` is expected to be raised when the code attempts to utilize a model from the `MODELS_NAME` list, but none are available. This could be due to various reasons such as the models being offline, not properly configured, or exceeding usage limits.

### Data Flow
- **Input**: The exception is triggered by the unavailability of models.
- **Output**: The exception is raised, indicating that no suitable model is available.
- **Side Effects**: The program's execution is halted until the exception is handled, potentially leading to a restart or alternative model selection.

### Usage Example
```python
try:
    # Attempt to use a model from the list
    for model_name in MODELS_NAME:
        # Model usage logic here
        pass
    # If no model is available, raise the exception
    raise ModelExhaustedException("No model is available for use.")
except ModelExhaustedException as e:
    # Handle the exception, e.g., log the error and notify the user
    print(f"Error: {e}")
``` 
<a name="compressor-module"></a>
## Compressor Module
The compressor module is responsible for compressing and comparing data using a provided model and project settings.

### Compressor Functions
The compressor module contains the following key functions:
* `compress`: Compresses a given string of data using a provided model and project settings.
* `compress_and_compare`: Compresses and compares a list of data using a provided model and project settings.
* `async_compress`: Asynchronously compresses a given string of data using a provided model and project settings.
* `async_compress_and_compare`: Asynchronously compresses and compares a list of data using a provided model and project settings.
* `compress_to_one`: Compresses a list of data to a single string using a provided model and project settings.
* `generate_discribtions_for_code`: Generates descriptions for a list of code using a provided model and project settings.

### Data Flow
- **Input**: The compressor module takes in data, models, project settings, and progress bars.
- **Output**: The compressor module generates compressed data, descriptions, and logs information and warnings.
- **Side Effects**: The compressor module updates the log with information and warnings.

### Technical Details
The compressor module uses the `GPTModel` and `AsyncModel` classes to compress and compare data. It also utilizes the `ProjectSettings` class to store project information and generate prompts for the model.

### Usage Example
```python
project_settings = ProjectSettings("My Project")
data = ["This is a test string", "This is another test string"]
compressed_data = compress_to_one(data, model, project_settings)
``` 
<a name="logging-mechanism"></a>
#### Logging Mechanism
The logging mechanism is handled by the `BaseLog` class and its subclasses (`ErrorLog`, `WarningLog`, `InfoLog`). These classes define the structure of log messages, including a timestamp and a message. 

### 
<a name="logger-templates"></a>
#### Logger Templates
The `BaseLoggerTemplate` class and its subclasses (`FileLoggerTemplate`) define how log messages are handled. The `BaseLogger` class is a singleton that provides a global logging interface.

### 
<a name="progress-tracking"></a>
#### Progress Tracking
The progress tracking mechanism is handled by the `BaseProgress` class and its subclasses (`LibProgress`, `ConsoleGtiHubProgress`). These classes define how progress is tracked and updated.

### 
<a name="manager-class"></a>
## Manager Class
### Purpose
The Manager class is responsible for orchestrating the documentation generation process, including code mixing, global information generation, documentation generation, and post-processing.

### Technical Details
The Manager class is defined in the `autodocgenerator\manage.py` file and utilizes various modules, such as `CodeMix`, `DocFactory`, and `ProjectSettings`, to perform its tasks. It also interacts with the `GPTModel` and `AsyncGPTModel` classes for documentation generation.

### Interactions
The Manager class interacts with the following components:

* `CodeMix`: for code mixing and generating the code mix file
* `DocFactory`: for generating documentation using the factory approach
* `GPTModel` and `AsyncGPTModel`: for documentation generation
* `ProjectSettings` and `ProjectConfigSettings`: for project configuration and settings

### Data Flow
- **Input**: The Manager class takes in project directory, project settings, and other parameters.
- **Output**: The Manager class generates various files, including the code mix file, global information file, and output documentation file.
- **Side Effects**: The Manager class updates the cache folder, logs information, warnings, and errors, and clears the cache if necessary.

### Usage Example
```python
manager = Manager(project_directory="/path/to/project", project_settings=ProjectSettings(), 
                  pcs=ProjectConfigSettings(), sync_model=GPTModel(), async_model=AsyncGPTModel())
manager.generate_code_file()
manager.generate_global_info_file()
manager.generete_doc_parts()
manager.factory_generate_doc(DocFactory())
manager.order_doc()
``` 
