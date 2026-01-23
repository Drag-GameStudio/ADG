## Executive Navigation Tree
* 📂 Core Engine
  * [Installation Workflow](#installation_workflow)
  * [Config Module](#config_module)
  * [Constants](#constants)
  * [Environment Variables](#environment_variables)
  * [Functions](#functions)
  * [Project Configuration](#project-configuration)
  * [Dependencies](#dependencies)
  * [Build System](#build-system)
* 📊 Manager Class
  * [Manager Class Usage](#Manager_Class_Usage)
  * [Manager Class](#manager-class)
  * [Responsibilities](#responsibilities)
  * [Example Usage](#example-usage)
* 📈 Logic and Interactions
  * [Interactions](#interactions)
  * [Key Functions](#key_functions)
  * [Logic Flow](#logic_flow)
  * [Assumptions](#assumptions)
  * [Inputs and Outputs](#inputs_outputs)
  * [Side Effects](#side_effects)
* 📄 Model Components
  * [Model Component](#model_component)
  * [Code Description](#code-description)
  * [Inputs and Outputs](#inputs-and-outputs)

**Project Title**: Auto Doc Generator

**Project Goal**: The Auto Doc Generator project aims to assist developers in creating documentation for their projects. The primary objective is to automate the process of generating high-quality documentation, making it easier for developers to maintain and share their code. The project utilizes natural language processing (NLP) and machine learning (ML) to analyze the codebase and generate accurate, concise, and readable documentation.

**Core Logic & Principles**: The Auto Doc Generator project operates on the following core logic and principles:

* **Config Reader**: The project reads configuration settings from a YAML file (`autodocconfig.yml`), which stores project-specific settings, such as the project name, ignore files, and custom descriptions.
* **Document Factory**: The project creates document factories based on the custom descriptions provided in the configuration file. These factories are used to generate documentation for specific parts of the codebase.
* **Manager**: The Manager class is responsible for generating the documentation. It takes the project settings, ignore files, project path, and document factories as input and uses the GPT model to generate high-quality documentation.
* **GPT Model**: The project uses a GPT (Generative Pre-trained Transformer) model to analyze the codebase and generate documentation. The model is trained on a large corpus of text data and can generate human-like text based on the input it receives.
* **Progress Bar**: The project uses a progress bar to display the progress of the documentation generation process. This provides feedback to the user and helps them track the progress of the process.

**Key Features**:

* Automated documentation generation
* Support for multiple programming languages
* Customizable documentation templates
* Integration with popular development tools and platforms
* Progress bar to display the progress of the documentation generation process
* Support for generating documentation for specific parts of the codebase

**Dependencies**:

* YAML library for reading configuration files
* GPT model library for natural language processing and machine learning
* Progress bar library for displaying progress
* Python programming language for development and execution
* Various development tools and platforms for integration and support

Note: The dependencies listed above are not exhaustive and may vary depending on the specific requirements and implementation of the project.

 

<a name='installation_workflow'> </a>
To install the workflow, follow these steps:
1. For PowerShell, use the command: `irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex`
2. For Linux-based systems, use the command: `curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash`
3. Add a secret variable to your GitHub Action: `GROCK_API_KEY` with your API key from Grock Docs (`https://grockdocs.com`) to make the workflow work.

<a name='Manager Class Usage'> </a>
The Manager class is used in the autodocgenerator/auto_runner/run_file.py file. 

It takes the following parameters:
- project_path: the path to the project
- project_settings: an object of class ProjectSettings
- sync_model: an object of class GPTModel
- async_model: an object of class AsyncGPTModel
- ignore_files: a list of files to be ignored
- progress_bar: an object of class BaseProgress or its subclasses
- language: the language to be used

Here is an example of usage:
```python
manager = Manager(
        project_path, 
        project_settings, 
        sync_model=sync_model,
        async_model=async_model,
        ignore_files=ignore_list, 
        progress_bar=ConsoleGtiHubProgress(), 
        language="en")
``` 

You can then call methods on the manager object, such as:
```python
manager.generate_code_file()
manager.generate_global_info_file(use_async=False, max_symbols=8000)
manager.generete_doc_parts(use_async=False, max_symbols=8000)
manager.factory_generate_doc(doc_factory)
manager.factory_generate_doc(intro_factory)
``` 

Note: The classes and objects used in the example (such as ProjectSettings, GPTModel, AsyncGPTModel, BaseProgress, ConsoleGtiHubProgress) are defined in other parts of the codebase.

<a name='autodocconfig_yml_options'> </a>
The autodocconfig.yml file has the following options available:

* project_name: The name of the project.
* language: The language of the project, default is "en".
* project_additional_info: Additional information about the project, which is a dictionary of key-value pairs.
* ignore_files: A list of file patterns to be ignored.
* custom_descriptions: A list of custom descriptions.

Example of autodocconfig.yml file:
```
project_name: "Auto Doc Generator"
language: "en"
project_additional_info:
  global idea: "This project was created to help developers make documentations for them projects"
ignore_files:
  - "*.pyo"
  - "*.pyd"
  - "*.pdb"
  - "*.pkl"
  - "*.log"
  - "*.sqlite3"
  - "*.db"
  - "data"
  - "venv"
  - "env"
  - ".venv"
  - ".env"
  - ".vscode"
  - ".idea"
  - "*.iml"
  - ".gitignore"
  - ".ruff_cache"
  - ".auto_doc_cache"
  - "*.pyc"
  - "__pycache__"
  - ".git"
  - ".coverage"
  - "htmlcov"
  - "migrations"
  - "*.md"
  - "static"
  - "staticfiles"
  - ".mypy_cache"
custom_descriptions:
  - "explain how install workflow with install.ps1 and install.sh scripts for install you should use links irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex for powershell and curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash for linux based systems and also you have to add secret variable to git hub action GROCK_API_KEY with your api key from grock docs https://grockdocs.com to make it work"
  - "how to use Manager class what parameters i need to give. give full example of usage"
  - "explain how to write autodocconfig.yml file what options are available"
```

 

## <a name="overview"></a> Overview
The provided code snippet is part of the Auto Doc Generator (ADG) system, a tool designed to automate the generation of documentation for projects. This documentation focuses on the `autodocgenerator/auto_runner` module, which is responsible for reading the configuration file, generating documentation, and interacting with other components of the ADG system.

## <a name="responsibility"></a> Responsibility
The `autodocgenerator/auto_runner` module is responsible for:
* Reading the configuration file (`autodocconfig.yml`)
* Generating documentation based on the project settings and configuration
* Interacting with other components, such as the `Manager` class, to generate code files, global information files, and document parts

## <a name="interactions"></a> Interactions
This module interacts with the following components:
* `autodocgenerator/manage.py`: The `Manager` class, which is responsible for generating documentation
* `autodocgenerator/engine/models/gpt_model.py`: The `GPTModel` and `AsyncGPTModel` classes, which are used for generating documentation
* `autodocgenerator/factory/base_factory.py`: The `DocFactory` class, which is used to generate documentation
* `autodocgenerator/ui/progress_base.py`: The `ConsoleGtiHubProgress` class, which is used to display progress

## <a name="key_functions"></a> Key Functions
The key functions in this module are:
* `read_config(file_data: str) -> Config`: Reads the configuration file and returns a `Config` object
* `gen_doc(project_settings: ProjectSettings, ignore_list: list[str], project_path: str, doc_factory: DocFactory, intro_factory: DocFactory)`: Generates documentation based on the project settings and configuration

## <a name="logic_flow"></a> Logic Flow
The logic flow of this module is as follows:
1. Read the configuration file (`autodocconfig.yml`)
2. Create a `Config` object based on the configuration file
3. Create a `ProjectSettings` object based on the `Config` object
4. Create `DocFactory` objects based on the `Config` object
5. Generate documentation using the `Manager` class and the `GPTModel` and `AsyncGPTModel` classes
6. Display progress using the `ConsoleGtiHubProgress` class

## <a name="assumptions"></a> Assumptions
This module assumes that:
* The configuration file (`autodocconfig.yml`) is present and correctly formatted
* The `Manager` class and the `GPTModel` and `AsyncGPTModel` classes are implemented correctly
* The `DocFactory` class is implemented correctly

## <a name="inputs_outputs"></a> Inputs and Outputs
The inputs to this module are:
* The configuration file (`autodocconfig.yml`)
* The project path
* The `DocFactory` objects

The outputs of this module are:
* The generated documentation
* The progress displayed using the `ConsoleGtiHubProgress` class

## <a name="side_effects"></a> Side Effects
This module has the following side effects:
* Creates files and directories for the generated documentation
* Displays progress using the `ConsoleGtiHubProgress` class

## <a name="config_module"></a> Config Module
The `autodocgenerator/engine/config/config.py` module is responsible for storing and managing configuration constants and environment variables for the AutoDoc system.

## <a name="constants"></a> Constants
This module defines several constants, including:
* `BASE_SYSTEM_TEXT`: a string containing instructions for processing code snippets
* `BASE_PART_COMPLITE_TEXT`: a string containing instructions for documenting code snippets
* `BASE_INTRODACTION_CREATE_TEXT`: a string containing instructions for generating an executive navigation tree
* `BASE_INTRO_CREATE`: a string containing instructions for generating a project overview
* `BASE_SETTINGS_PROMPT`: a string containing instructions for processing project parameters
* `MODELS_NAME`: a list of model names used for generating documentation

## <a name="environment_variables"></a> Environment Variables
The module loads environment variables using the `load_dotenv` function from the `dotenv` library. It checks if the `API_KEY` environment variable is set and raises an exception if it is not.

## <a name="functions"></a> Functions
The module defines a single function, `get_BASE_COMPRESS_TEXT`, which returns a formatted string containing instructions for analyzing and summarizing a large code snippet.

## <a name="interactions"></a> Interactions
This module interacts with other parts of the system by providing configuration constants and environment variables to other modules. It also relies on the `dotenv` library to load environment variables.

## <a name="logic_flow"></a> Logic Flow
The logic flow of this module is as follows:
1. Load environment variables using `load_dotenv`.
2. Check if the `API_KEY` environment variable is set and raise an exception if it is not.
3. Define configuration constants and functions.

## <a name="assumptions"></a> Assumptions
This module assumes that the `API_KEY` environment variable is set in the `.env` file and that the `dotenv` library is installed.

## <a name="inputs_outputs"></a> Inputs and Outputs
The inputs to this module are the environment variables loaded using `load_dotenv`. The outputs are the configuration constants and functions defined in the module.

## <a name="side_effects"></a> Side Effects
This module has the side effect of raising an exception if the `API_KEY` environment variable is not set.

## <a name="model_component"></a> Model Component
### Responsibility
The Model component is responsible for generating answers to user prompts based on the provided context and history. It interacts with other parts of the system by receiving input from the user, processing it, and returning a generated answer.

### Key Functions and Classes
*   `History` class: Maintains a record of interactions between the user and the model, including system prompts and user input.
*   `ParentModel` class: Serves as the base class for models, initializing the API key, history, and model names.
*   `Model` class: Generates answers to user prompts with or without history.
*   `AsyncModel` class: Provides asynchronous versions of the `Model` class methods.

### Logic Flow
1.  The `History` class is initialized with a system prompt, which is added to the history.
2.  The `ParentModel` class is initialized with an API key and a history object.
3.  The `Model` or `AsyncModel` class is instantiated, and the `generate_answer` method is called with a user prompt.
4.  The `generate_answer` method adds the user prompt to the history, generates an answer, and adds the answer to the history.
5.  The generated answer is returned to the user.

### Important Assumptions and Inputs
*   The `API_KEY` environment variable is set.
*   The `MODELS_NAME` list is populated with available model names.
*   User input is provided as a string or a list of dictionaries.
*   The `language` parameter is specified for language-specific processing.

### Outputs and Side Effects
*   The generated answer is returned as a string.
*   The history is updated with the user prompt and the generated answer.
*   If the `API_KEY` environment variable is not set, an exception is raised.

### Interaction with Other Components
The Model component interacts with the following components:
*   `DocFactory`: Uses the `Model` class to generate documentation.
*   `BaseModule`: Subclasses of `BaseModule` use the `Model` class to generate specific parts of the documentation.
*   `Preprocessor`: The preprocessor component is responsible for splitting data, generating custom descriptions, and getting HTML links, which are used by the Model component.

### Overview of the Manager Class
<a name="manager-class"></a>

The `Manager` class is a central component of the automatic documentation generation system. It is responsible for managing the entire documentation generation process, from code mixing to document generation.

### Responsibilities
<a name="responsibilities"></a>

The `Manager` class has the following responsibilities:

* Managing the project directory and cache folder
* Generating code mix files
* Generating global information files
* Generating document parts
* Using the `DocFactory` to generate final documents

### Interaction with Other Components
<a name="interaction-with-other-components"></a>

The `Manager` class interacts with the following components:

* `CodeMix`: used to generate code mix files
* `DocFactory`: used to generate final documents
* `GPTModel` and `AsyncGPTModel`: used for language processing and document generation
* `ProjectSettings`: used to store project-specific settings and information

### Key Functions and Logic Flows
<a name="key-functions-and-logic-flows"></a>

The `Manager` class has the following key functions:

* `generate_code_file`: generates a code mix file using the `CodeMix` class
* `generate_global_info_file`: generates a global information file using the `GPTModel` or `AsyncGPTModel` class
* `generete_doc_parts`: generates document parts using the `GPTModel` or `AsyncGPTModel` class
* `factory_generate_doc`: uses the `DocFactory` to generate a final document

The logic flow of the `Manager` class is as follows:

1. Initialize the project directory and cache folder
2. Generate a code mix file using the `CodeMix` class
3. Generate a global information file using the `GPTModel` or `AsyncGPTModel` class
4. Generate document parts using the `GPTModel` or `AsyncGPTModel` class
5. Use the `DocFactory` to generate a final document

### Important Assumptions, Inputs, Outputs, and Side Effects
<a name="important-assumptions-inputs-outputs-and-side-effects"></a>

The `Manager` class assumes that the project directory and cache folder are properly set up. The inputs to the `Manager` class include the project directory, project settings, and language. The outputs of the `Manager` class include the generated document. The side effects of the `Manager` class include the creation of cache files and the updating of the project settings.

### Example Usage
<a name="example-usage"></a>

The `Manager` class can be used as follows:
```python
project_settings = ProjectSettings("Auto Doc Generator")
project_settings.add_info("global idea", "This project was created to help developers make documentations for them projects")

manager = Manager(r"C:\Users\sinic\OneDrive\Документы\GitHub\ADG", 
                 project_settings,
                 sync_model=GPTModel(API_KEY),
                 async_model=AsyncGPTModel(API_KEY),
                 ignore_files=ignore_list, 
                 progress_bar=LibProgress(progress), 
                 language="en")

manager.factory_generate_doc(DocFactory(IntroLinks()))
```

## Compressor Module Documentation
<a name="compressor-module-documentation"></a>

The compressor module is a crucial component of the automatic documentation generation system. It is responsible for compressing and comparing code files to generate high-quality documentation.

### Responsibilities
<a name="responsibilities"></a>

The compressor module has the following responsibilities:

* Compressing code files using a model-based approach
* Comparing compressed code files to generate documentation
* Providing a progress bar to track the compression and comparison process

### Interaction with Other Components
<a name="interaction-with-other-components"></a>

The compressor module interacts with the following components:

* `Model`: used to compress and compare code files
* `ProjectSettings`: used to store project-specific settings and information
* `BaseProgress`: used to display a progress bar

### Key Functions and Logic Flows
<a name="key-functions-and-logic-flows"></a>

The compressor module has the following key functions:

* `compress`: compresses a single code file using a model-based approach
* `compress_and_compare`: compresses and compares multiple code files to generate documentation
* `async_compress`: asynchronously compresses a single code file using a model-based approach
* `async_compress_and_compare`: asynchronously compresses and compares multiple code files to generate documentation

The logic flow of the compressor module is as follows:

1. Initialize the progress bar and project settings
2. Compress each code file using the `compress` function
3. Compare the compressed code files using the `compress_and_compare` function
4. Generate documentation based on the compressed and compared code files

### Important Assumptions, Inputs, Outputs, and Side Effects
<a name="important-assumptions-inputs-outputs-and-side-effects"></a>

The compressor module assumes that the project settings and model are properly configured. The inputs to the compressor module include the code files, project settings, and model. The outputs of the compressor module include the compressed and compared code files, as well as the generated documentation. The side effects of the compressor module include the creation of temporary files and the updating of the project settings.

### Example Usage
<a name="example-usage"></a>

The compressor module can be used as follows:
```python
project_settings = ProjectSettings("Auto Doc Generator")
model = Model()

code_files = ["file1.py", "file2.py", "file3.py"]
compressed_files = compress_and_compare(code_files, model, project_settings)

# Generate documentation based on the compressed files
documentation = generate_discribtions_for_code(compressed_files, model, project_settings)
```

## <a name="code-description"></a> Code Description
The provided code snippet is part of a larger system responsible for generating documentation for code files. This specific snippet focuses on the final stages of the documentation generation process.

### <a name="responsibility"></a> Responsibility
The code is responsible for compressing code files, comparing them, and generating documentation based on the compressed files.

### <a name="interactions"></a> Interactions
This component interacts with other parts of the system by:

* Receiving compressed files from the `compress_and_compare` function
* Passing the compressed files to the `generate_discribtions_for_code` function to generate documentation
* Utilizing the `model` and `project_settings` from the system configuration

### <a name="key-functions"></a> Key Functions
The key functions involved in this process are:

* `compress_and_compare`: Compresses code files and compares them
* `generate_discribtions_for_code`: Generates documentation based on the compressed files

### <a name="logic-flow"></a> Logic Flow
The logic flow of this component is as follows:

1. Compress code files using the `compress_and_compare` function
2. Generate documentation based on the compressed files using the `generate_discribtions_for_code` function

### <a name="assumptions"></a> Assumptions
This component assumes that:

* The `compress_and_compare` function returns a list of compressed files
* The `generate_discribtions_for_code` function takes in the compressed files, `model`, and `project_settings` as input

### <a name="inputs-outputs"></a> Inputs and Outputs
The inputs to this component are:

* `code_files`
* `model`
* `project_settings`

The output of this component is:

* `documentation`: The generated documentation for the code files

### <a name="side-effects"></a> Side Effects
This component has the following side effects:

* Generates documentation for the code files
* Updates the system configuration with the generated documentation

In the context of the entire system, this component plays a crucial role in generating high-quality documentation for code files, making it easier for developers to understand and maintain the codebase. 

```python
compressed_files = compress_and_compare(code_files, model, project_settings)
documentation = generate_discribtions_for_code(compressed_files, model, project_settings)
```

## <a name="project-configuration"></a> Project Configuration
The provided `pyproject.toml` file serves as the configuration file for the `autodocgenerator` project. It contains essential information about the project, including its name, version, description, authors, and license.

### <a name="dependencies"></a> Dependencies
The project relies on a wide range of dependencies, which are listed in the `dependencies` section. These dependencies include libraries for tasks such as:
* Data serialization and deserialization (e.g., `pyyaml`, `msgpack`)
* HTTP requests and web development (e.g., `httpx`, `requests`)
* Authentication and authorization (e.g., `google-auth`, `rsa`)
* Code analysis and documentation generation (e.g., `pydantic`, `Pygments`)
* Utility libraries for tasks such as caching, logging, and progress bars (e.g., `CacheControl`, `rich`, `tqdm`)

### <a name="build-system"></a> Build System
The `build-system` section specifies the requirements for building the project. It requires `poetry-core` version 2.0.0 or higher and uses the `poetry.core.masonry.api` build backend.

### <a name="assumptions-and-implications"></a> Assumptions and Implications
Based on the provided configuration file, it can be assumed that the `autodocgenerator` project is designed to generate documentation for other projects. The project's dependencies suggest that it may utilize various technologies, such as machine learning models (e.g., `google-genai`) and natural language processing (e.g., `openai`), to analyze and document code.

The implications of this configuration are that the project is likely to be complex, with multiple components and dependencies working together to achieve its goals. As a result, developers working on this project should be familiar with a range of technologies and libraries to effectively maintain and extend the project. 

### <a name="inputs-and-outputs"></a> Inputs and Outputs
The `pyproject.toml` file does not specify any direct inputs or outputs. However, as a configuration file, its contents serve as input for the project's build and development processes. The output of the project is likely to be generated documentation for other projects, which can take various forms, such as HTML files, PDF documents, or other formats. 

### <a name="side-effects"></a> Side Effects
The `pyproject.toml` file itself does not have any direct side effects. However, the project it configures may have side effects, such as generating documentation files, updating system configurations, or interacting with external services. 

In the context of the entire system, the `autodocgenerator` project plays a crucial role in generating high-quality documentation for code files, making it easier for developers to understand and maintain the codebase. 

```python
compressed_files = compress_and_compare(code_files, model, project_settings)
documentation = generate_discribtions_for_code(compressed_files, model, project_settings)
```

