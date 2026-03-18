**Project Title:** Auto Doc Generator - Orchestrated Pipeline

**Project Goal:** 
The Auto Doc Generator project aims to automate the process of creating project documentation by leveraging Large Language Models (LLMs) for source code analysis and post-processing the output. This innovative approach streamlines the documentation process, reducing manual effort and enhancing overall efficiency. By automating project documentation, this software solves the problem of tedious and time-consuming manual documentation, allowing developers to focus on core development tasks.

**Core Logic & Principles:**
The Auto Doc Generator operates on a layered architecture, comprising multiple components that work in harmony to produce high-quality documentation. The pipeline is orchestrated by the `Manager` component, which holds shared state and configuration. The process begins with the `CodeMix` component, which preprocesses source code into a unified string. This output is then fed into the `DocFactory` component, which utilizes LLMs to generate documentation. The `Embedding` component wraps the generated documentation parts with vector embeddings, while the `Config` component stores global settings and cache metadata. The project employs various technologies, including LLMs, vector embeddings, and caching mechanisms, to ensure efficient and accurate documentation generation.

**Key Features:**
* Automated project documentation generation
* Utilization of Large Language Models (LLMs) for source code analysis
* Post-processing of LLM output for enhanced documentation quality
* Vector embedding for document parts
* Caching mechanism for intermediate artifacts
* Support for multiple entry points and terminal points
* Layered architecture with clear component boundaries

**Dependencies:**
* Large Language Models (LLMs) APIs (e.g., OpenAI, GROQ)
* Vector embedding libraries
* Caching libraries
* Python 3.x (for script execution)
* Required libraries: `ui.logging`, `ui.progress_base`, `engine.models`
* Environment variables: `OPENAI_API_KEY`, `GROQ_API_KEY` (for LLM API access)
## Executive Navigation Tree
* 📂 Project Settings
  * [Project Settings Class](#project-settings-class)
  * [Project Settings Attributes](#project-settings-attributes)
  * [Project Settings Methods](#project-settings-methods)
  * [Project Info](#project-info)
  * [Project Metadata](#project-metadata)
  * [Project Overview](#project-overview)
* ⚙️ Installation and Configuration
  * [Installation Workflow Description](#installation-workflow-description)
  * [Install Script](#install-script)
  * [Current Code Base](#current-code-base)
  * [Config Class](#config-class)
  * [Autodoc Config Structure and Options](#autodocconfig-structure-and-options)
  * [Read Config](#read-config)
* 📄 Documentation Generation
  * [Data Contract](#data-contract)
  * [Doc Schema](#doc-schema)
  * [Code Example Doc Schema](#code-example-doc-schema)
  * [Gen Doc](#gen-doc)
  * [Gen Doc Parts Functionality](#gen-doc-parts-functionality)
  * [Gen Doc Parts Parameters](#gen-doc-parts-parameters)
  * [Gen Doc Parts Return Value](#gen-doc-parts-return-value)
  * [Code Example Gen Doc Parts](#code-example-gen-doc-parts)
  * [Write Docs by Parts Functionality](#write-docs-by-parts-functionality)
  * [Write Docs by Parts Parameters](#write-docs-by-parts-parameters)
  * [Write Docs by Parts Return Value](#write-docs-by-parts-return-value)
  * [Code Example Write Docs by Parts](#code-example-write-docs-by-parts)
* 📊 Code Examples and Utilities
  * [Autodoc Generator Project Documentation](#autodocgenerator-project-documentation)
  * [Code Example](#code-example)
  * [Code Example 2](#code-example-2)
  * [Code Example 3](#code-example-3)
  * [Code Example Split Data](#code-example-split-data)
  * [Code Example Logging](#code-example-logging)
  * [Code Example Progress Bar](#code-example-progress-bar)
* 📈 Git and Version Control
  * [Check Git Status](#check-git-status)
* 🤖 AI and Machine Learning
  * [GPT Model Class](#gpt-model-class)
  * [Manager Class](#manager-class)
  * [Manager Class Usage](#manager-class-usage)
* ⚖️ Compression and Data Processing
  * [Compressor Component](#compressor-component)
  * [Compress Function](#compress-function)
  * [Compress and Compare Function](#compress-and-compare-function)
  * [Compress to One Function](#compress-to-one-function)
  * [Split Data Function](#split-data-function)
  * [Split Data Parameters](#split-data-parameters)
  * [Split Data Return Value](#split-data-return-value)
  * [Split Data Functionality](#split-data-functionality)
* 📊 Technical Logic and Flow
  * [Technical Logic Flow](#technical-logic-flow)
  * [Functional Flow](#functional-flow)
  * [Component Logic](#component-logic)
  * [Key Context for Snippets](#key-context-for-snippets)
* 📝 Logging and Progress
  * [Logger Functionality](#logger-functionality)
  * [Progress Bar Functionality](#progress-bar-functionality)
<a name="project-settings-class"></a> Project Settings Class
The `ProjectSettings` class is used to store project-specific settings, including the prompt and other configuration.

###
<a name="project-settings-attributes"></a> Project Settings Attributes

* `project_name`: The name of the project
* `info`: A dictionary of additional project information

###
<a name="project-settings-methods"></a> Project Settings Methods

* `add_info(key, value)`: Adds a new key-value pair to the `info` dictionary
* `prompt`: Returns the project prompt, which includes the project name and additional information

###
<a name="project-info"></a> Project Info
Project Name: Auto Doc Generator 
Project Parameters: 
- global_idea: This project was created to help developers make documentations for them projects 
- target_audience: Developers
- tech_stack: Python, LLMs, Markdown

##
<a name="project-metadata"></a> Project Metadata
The project metadata is defined in the `pyproject.toml` file. 

### Project Information
* **Name:** autodocgenerator
* **Version:** 1.0.5.0
* **Description:** This Project helps you to create docs for your projects
* **Authors:** dima-on <sinica911@gmail.com>
* **License:** MIT
* **Readme:** README.md
* **Python Version:** >=3.11,<4.0

### Dependencies
The project dependencies are listed in the `dependencies` section of the `pyproject.toml` file. Some of the notable dependencies include:
* annotated-types
* pyyaml
* anyio
* CacheControl
* certifi
* charset-normalizer
* cleo
* colorama
* crashtest
* distlib
* distro
* dulwich
* fastjsonschema
* filelock
* findpython
* google-auth
* google-genai
* groq
* h11
* httpcore
* httpx
* idna
* installer
* jaraco.classes
* jaraco.context
* jaraco.functools
* jiter
* keyring
* markdown-it-py
* mdurl
* more-itertools
* msgpack
* openai
* packaging
* pbs-installer
* pkginfo
* platformdirs
* pyasn1
* pyasn1_modules
* pydantic
* pydantic_core
* Pygments
* pyproject_hooks
* python-dotenv
* pywin32-ctypes
* RapidFuzz
* requests
* requests-toolbelt
* rich
* rich_progress
* rsa
* shellingham
* sniffio
* tenacity
* tomlkit
* tqdm
* trove-classifiers
* typing_extensions
* typing-inspection
* urllib3
* virtualenv
* websockets
* zstandard
* numpy

### Build System
The build system is defined in the `build-system` section of the `pyproject.toml` file. 
* **Requires:** poetry-core>=2.0.0
* **Build Backend:** poetry.core.masonry.api

##
<a name="project-overview"></a> Project Overview
The AutoDocGenerator project is designed to automate the process of generating documentation for source code repositories. The project uses a layered architecture, with components responsible for pre-processing, engine, post-processing, and utility functions.

###
<a name="installation-workflow-description"></a>
The installation process utilizes two scripts, install.ps1 for PowerShell and install.sh for Linux-based systems, which are downloaded and executed directly from a GitHub repository. To install using PowerShell, the command `irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex` is used, while Linux-based systems rely on `curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash`. Additionally, to successfully implement this workflow within GitHub Actions, a secret variable named `GROCK_API_KEY` must be defined, containing the user's API key from the Grock documentation found at https://grockdocs.com. This API key is crucial for the installation process to function correctly, enabling the interaction with the Grock service as outlined in their documentation. 

Here is a step-by-step guide on how to accomplish this:

1. **For PowerShell Users:**
   - Open PowerShell.
   - Use the command `irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex` to download and execute the install script.

2. **For Linux-Based Systems:**
   - Open your terminal.
   - Run the command `curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash` to download and execute the installation script.

3. **Configuring GitHub Actions:**
   - Navigate to your GitHub repository.
   - Go to Settings > Actions > Secrets.
   - Click on "New repository secret".
   - Name the secret `GROCK_API_KEY`.
   - Enter your Grock API key as the value.
   - Click "Add secret" to save.

By following these steps and ensuring the `GROCK_API_KEY` secret is correctly set up in your GitHub repository, you will have successfully set up the installation workflow using the provided scripts and enabled integration with the Grock service.
<a name="install-script"></a> Install Script
The install script is defined in the `install.sh` file. 
### Script Functionality
The script creates the following files and directories:
* `.github/workflows/autodoc.yml`
* `autodocconfig.yml`

### Autodoc Configuration
The `autodocconfig.yml` file contains the following configuration settings:
* **Project Name:** The name of the project, which is set to the basename of the current working directory.
* **Language:** The language of the project, which is set to "en".
* **Ignore Files:** A list of files and directories to ignore, including:
	+ Python bytecode and cache files
	+ Environment and IDE settings files
	+ Database and binary data files
	+ Log and coverage report files
	+ Version control and asset files
	+ Miscellaneous files
* **Build Settings:**
	+ **Save Logs:** A boolean value indicating whether to save logs, which is set to `false`.
	+ **Log Level:** An integer value representing the log level, which is set to `2`.
* **Structure Settings:**
	+ **Include Intro Links:** A boolean value indicating whether to include intro links, which is set to `true`.
	+ **Include Intro Text:** A boolean value indicating whether to include intro text, which is set to `true`.
	+ **Include Order:** A boolean value indicating whether to include order, which is set to `true`.
	+ **Use Global File:** A boolean value indicating whether to use a global file, which is set to `true`.
	+ **Max Doc Part Size:** An integer value representing the maximum size of a doc part, which is set to `5000`.

##
<a name="current-code-base"></a> Current Code Base
The current code base includes the following files:
- `autodocgenerator/ui/logging.py`: This file contains classes for logging, including `BaseLog`, `ErrorLog`, `WarningLog`, `InfoLog`, `BaseLoggerTemplate`, `FileLoggerTemplate`, and `BaseLogger`.
- `autodocgenerator/ui/progress_base.py`: This file contains classes for progress bars, including `BaseProgress`, `LibProgress`, `ConsoleTask`, and `ConsoleGtiHubProgress`.
- `install.ps1`: This file is a PowerShell script that creates a directory and files for GitHub workflows and configurations.

##
<a name="config-class"></a>
## Config Class
The `Config` class is responsible for storing and managing the configuration settings for the Auto Doc Generator project.

### Parameters
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `ignore_files` | `list[str]` | Input | List of file patterns to ignore |
| `language` | `str` | Input | Language of the project |
| `project_name` | `str` | Input | Name of the project |
| `project_additional_info` | `dict` | Input | Additional information about the project |
| `pbc` | `ProjectBuildConfig` | Input | Project build configuration |

### Technical Logic Flow
1. Initialize the `Config` object with default values.
2. Set the language of the project using the `set_language` method.
3. Set the project name using the `set_project_name` method.
4. Add additional information about the project using the `add_project_additional_info` method.
5. Add file patterns to ignore using the `add_ignore_file` method.
6. Get the project settings using the `get_project_settings` method.

### Methods
* `set_language(language: str)`: Sets the language of the project.
* `set_pcs(pcs: ProjectBuildConfig)`: Sets the project build configuration.
* `set_project_name(name: str)`: Sets the name of the project.
* `add_project_additional_info(key: str, value: str)`: Adds additional information about the project.
* `add_ignore_file(pattern: str)`: Adds a file pattern to ignore.
* `get_project_settings()`: Gets the project settings.

### Code
```python
class Config:
    def __init__(self):
        self.ignore_files: list[str] = ["*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db", "data",
                                         "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore", ".ruff_cache", ".auto_doc_cache",
                                         "*.pyc", "__pycache__", ".git", ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles", ".mypy_cache"]
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
```
<a name="autodocconfig-structure-and-options"></a>
The autodocconfig.yml file has several options available for configuration. The main sections include:
- project_name: This is where the name of the project is specified.
- language: This option specifies the language of the project.
- ignore_files: This section allows specifying files or directories to be ignored during the documentation generation process. Examples of ignored files include:
  - "dist"
  - Python bytecode and cache files like "*.pyc", "*.pyo", "*.pyd", "__pycache__", ".ruff_cache", ".mypy_cache", ".auto_doc_cache"
  - Environment and IDE settings like "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml"
  - Databases and binary data like "*.sqlite3", "*.db", "*.pkl", "data"
  - Logs and coverage reports like "*.log", ".coverage", "htmlcov"
  - Version control and assets like ".git", ".gitignore", "migrations", "static", "staticfiles"
  - Miscellaneous files like "*.pdb", "*.md"
- build_settings: This section includes options for the build process:
  - save_logs: A boolean option to specify whether logs should be saved.
  - log_level: An option to set the level of logging, with a value of 2 in the provided example.
  - threshold_changes: An option to set a threshold for changes, with a value of 20000 in the provided example.
- structure_settings: This section includes options for customizing the structure of the generated documentation:
  - include_intro_links: A boolean option to include introduction links.
  - include_intro_text: A boolean option to include introduction text.
  - include_order: A boolean option to include order.
  - use_global_file: A boolean option to use a global file.
  - max_doc_part_size: An option to set the maximum size of a documentation part, with a value of 5000 in the provided example.
- project_additional_info: This section allows adding additional information about the project.
- custom_descriptions: This section allows adding custom descriptions for the project.
<a name="read-config"></a>
## Read Config
The `read_config` function is responsible for parsing the configuration file and returning the configuration objects. It takes a string containing the configuration data as input and returns a tuple of `Config`, `custom_modules`, and `structure_settings` objects.

### Parameters
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `file_data` | `str` | Input | Configuration file data |

### Technical Logic Flow
1. Load the configuration data from the input string using YAML.
2. Create a `Config` object and set its properties based on the configuration data.
3. Create a list of `custom_modules` based on the configuration data.
4. Create a `structure_settings` object and set its properties based on the configuration data.
5. Return the `config`, `custom_modules`, and `structure_settings` objects.

### Code
```python
def read_config(file_data: str) -> tuple[Config, list[BaseModule], StructureSettings]:
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

    custom_modules: list[BaseModule] = [CustomModuleWithOutContext(custom_discription[1:])  if custom_discription[0] == "%" else CustomModule(custom_discription) for custom_discription in custom_discriptions]

    structure_settings = data.get("structure_settings", {})
    structure_settings_object = StructureSettings()
    structure_settings_object.load_settings(structure_settings)

    return config, custom_modules, structure_settings_object
```
<a name="data-contract"></a> Data Contract
The data contract includes the following entities:
* **Log:** A log entry with a message and a level.
* **Task:** A task with a name and a total length.
* **Progress:** A progress bar with a current task and a total length.

##
<a name="doc-schema"></a> Doc Schema
The doc schema is defined using Pydantic models. The schema includes the following models:
* **`DocContent`**: Represents the content of a doc part, including the content and embedding vector.
* **`DocHeadSchema`**: Represents the schema of a doc head, including the content orders and parts.
* **`DocInfoSchema`**: Represents the schema of a doc info, including the global info, code mix, and doc.

###
<a name="code-example-doc-schema"></a> Code Example: Doc Schema
```python
from autodocgenerator.schema.doc_schema import DocContent, DocHeadSchema, DocInfoSchema

# Create a doc content object
doc_content = DocContent(content="This is a sample string.")

# Create a doc head schema object
doc_head_schema = DocHeadSchema()

# Add a part to the doc head schema
doc_head_schema.add_parts("part1", doc_content)

# Create a doc info schema object
doc_info_schema = DocInfoSchema(global_info="This is a sample global info.")

# Print the doc info schema
print(doc_info_schema)
```

##
<a name="gen-doc"></a>
## Gen Doc
The `gen_doc` function is responsible for generating the documentation for a project. It takes the project path, configuration, custom modules, and structure settings as input and returns the generated documentation as a string.

### Parameters
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `project_path` | `str` | Input | Project path |
| `config` | `Config` | Input | Configuration object |
| `custom_modules` | `list[BaseModule]` | Input | List of custom modules |
| `structure_settings` | `StructureSettings` | Input | Structure settings object |

### Technical Logic Flow
1. Create a `Manager` instance with the project path, configuration, and custom modules.
2. Check the git status using the `check_git_status` function. If the documentation should not be updated, return an empty string.
3. Generate the code file using the `generate_code_file` method of the `Manager` instance.
4. Generate the global information using the `generate_global_info` method of the `Manager` instance.
5. Generate the documentation parts using the `generete_doc_parts` method of the `Manager` instance.
6. Generate the documentation using the `factory_generate_doc` method of the `Manager` instance.
7. Create an embedding layer using the `create_embedding_layer` method of the `Manager` instance.
8. Save the documentation using the `save` method of the `Manager` instance.
9. Return the generated documentation as a string.

### Code
```python
def gen_doc(project_path: str, 
            config: Config, 
            custom_modules: list[BaseModule], 
            structure_settings: StructureSettings) -> str:
    
    sync_model = GPTModel(GROQ_API_KEYS, use_random=False)
    embedding_model = Embedding(GOOGLE_EMBEDDING_API_KEY)
    
    
    manager = Manager(
        project_path, 
        config=config,
        llm_model=sync_model,
        embedding_model=embedding_model,
        progress_bar=ConsoleGtiHubProgress(), 
    )

    should_change = check_git_status(manager)
    if not should_change:
        return ""
    

    
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
    manager.create_embedding_layer()
    manager.clear_cache()

    manager.save()
    return manager.doc_info.doc.get_full_doc()
```
<a name="gen-doc-parts-functionality"></a> Gen Doc Parts Functionality
###
<a name="gen-doc-parts-parameters"></a> Gen Doc Parts Parameters
The `gen_doc_parts` function takes the following parameters:
* `full_code_mix`: The full code mix string.
* `max_symbols`: The maximum number of symbols in each chunk.
* `model`: The language model used for generating documentation.
* `project_settings`: The project settings, including the prompt and other configuration.
* `language`: The language used for generating documentation.
* `progress_bar`: The progress bar object.
* `global_info`: The global information, if any.

###
<a name="gen-doc-parts-return-value"></a> Gen Doc Parts Return Value
The `gen_doc_parts` function returns the generated documentation as a string.

###
<a name="code-example-gen-doc-parts"></a> Code Example: Gen Doc Parts
```python
from autodocgenerator.preprocessor import gen_doc_parts

# Create a project settings object
project_settings = ProjectSettings("My Project")

# Create a language model object
model = Model()

# Preprocess the input data
full_code_mix = "This is a sample string."

# Create a progress bar object
progress_bar = BaseProgress()

# Generate documentation for the parts
documentation = gen_doc_parts(full_code_mix, max_symbols=10, model=model, project_settings=project_settings, language="en", progress_bar=progress_bar)

# Print the documentation
print(documentation)
```

##
<a name="write-docs-by-parts-functionality"></a> Write Docs by Parts Functionality
###
<a name="write-docs-by-parts-parameters"></a> Write Docs by Parts Parameters
The `write_docs_by_parts` function takes the following parameters:
* `part`: The string data to be used for generating documentation.
* `model`: The language model used for generating documentation.
* `project_settings`: The project settings, including the prompt and other configuration.
* `prev_info`: The previous documentation information, if any.
* `language`: The language used for generating documentation.
* `global_info`: The global information, if any.

###
<a name="write-docs-by-parts-return-value"></a> Write Docs by Parts Return Value
The `write_docs_by_parts` function returns the generated documentation as a string.

###
<a name="code-example-write-docs-by-parts"></a> Code Example: Write Docs by Parts
```python
from autodocgenerator.preprocessor import write_docs_by_parts

# Create a project settings object
project_settings = ProjectSettings("My Project")

# Create a language model object
model = Model()

# Preprocess the input data
part = "This is a sample string."

# Generate documentation for the part
documentation = write_docs_by_parts(part, model, project_settings)

# Print the documentation
print(documentation)
```

##
<a name="autodocgenerator-project-documentation"></a> AutoDocGenerator Project Documentation
###
<a name="code-example"></a> Code Example
```python
from autodocgenerator.preprocessor import compressor
from autodocgenerator.preprocessor import settings

# Create a project settings object
project_settings = settings.ProjectSettings("My Project")

# Create a language model object
model = Model()

# Preprocess the input data
data = "This is a sample string."

# Compress the preprocessed data
compressed_data = compressor.compress(data, project_settings, model, compress_power=4)

# Print the compressed data
print(compressed_data)
```

##
<a name="code-example-2"></a> Code Example
```python
from autodocgenerator.preprocessor import settings

# Create a project settings object
project_settings = settings.ProjectSettings("My Project")

# Add additional project information
project_settings.add_info("author", "John Doe")

# Print the project prompt
print(project_settings.prompt)
```

##
<a name="code-example-3"></a> Code Example
```python
from autodocgenerator.preprocessor import spliter

# Preprocess the input data
data = "This is a sample string."

# Split the preprocessed data into chunks
chunks = spliter.split_data(data, max_symbols=10)

# Print the chunks
print(chunks)
```

##
<a name="code-example-split-data"></a> Code Example: Split Data
```python
from autodocgenerator.preprocessor import split_data

# Preprocess the input data
data = "This is a sample string."

# Split the preprocessed data into chunks
chunks = split_data(data, max_symbols=10)

# Print the chunks
print(chunks)
```

##
<a name="code-example-logging"></a> Code Example: Logging
```python
from autodocgenerator.ui.logging import BaseLogger, InfoLog

# Create a logger
logger = BaseLogger()

# Create a log entry
log = InfoLog("This is a sample log message.")

# Log the message
logger.log(log)
```

##
<a name="code-example-progress-bar"></a> Code Example: Progress Bar
```python
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress

# Create a progress bar
progress = ConsoleGtiHubProgress()

# Create a new subtask
progress.create_new_subtask("Sample Task", 10)

# Update the task
progress.update_task()

# Remove the subtask
progress.remove_subtask()
```
<a name="check-git-status"></a>
## Check Git Status
The `check_git_status` function is responsible for determining whether the git repository has changed since the last documentation generation. It takes a `Manager` instance as input and returns a boolean indicating whether the documentation should be updated.

### Parameters
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `manager` | `Manager` | Input | Instance of the `Manager` class |
| `GITHUB_EVENT_NAME` | `str` | Global | GitHub event name |
| `cache_settings` | `CacheSettings` | Input | Cache settings object |

### Technical Logic Flow
1. Check if the GitHub event name is "workflow_dispatch". If so, return `True`.
2. Load the cache settings from the `.auto_doc_cache_file`.
3. Get the diff between the current commit and the last commit stored in the cache settings.
4. If the diff is greater than the threshold changes or the last commit is empty, update the cache settings and return `True`.
5. Otherwise, return `False`.

### Code
```python
def check_git_status(manager: Manager) -> bool:
    print("GIT EVENT:", GITHUB_EVENT_NAME)
    if GITHUB_EVENT_NAME == "workflow_dispatch":
        return True
    
    cache_settings = CacheSettings.model_validate_json(manager.read_file_by_file_key(".auto_doc_cache_file", is_outside=True))

    if len(get_diff_by_hash(cache_settings.last_commit)) > manager.config.pbc.threshold_changes or cache_settings.last_commit == "":
        cache_settings.last_commit = get_git_revision_hash()
        with open(manager.get_file_path(".auto_doc_cache_file", is_outside=True), "w", encoding="utf-8") as file:
            file.write(cache_settings.model_dump_json())
        return True
    
    return False
```
<a name="gpt-model-class"></a>
## GPT Model Class
The `GPTModel` class is responsible for generating answers using the GPT model.

### Parameters
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `api_key` | `str` | Input | API key for the GPT model |
| `history` | `History` | Input | History of previous conversations |
| `models_list` | `list[str]` | Input | List of available GPT models |
| `use_random` | `bool` | Input | Whether to use a random model |

### Technical Logic Flow
1. Initialize the `GPTModel` object with the API key, history, models list, and use random flag.
2. Set up the GPT client using the API key.
3. Generate an answer using the `generate_answer` method.

### Methods
* `generate_answer(with_history: bool = True, prompt: list[dict[str, str]] | None = None)`: Generates an answer using the GPT model.

### Code
```python
class GPTModel(Model):
    def __init__(self, api_key=GROQ_API_KEYS, history=History(), 
                 models_list: list[str] = ["openai/gpt-oss-120b",  "llama-3.3-70b-versatile",  "openai/gpt-oss-safeguard-20b"], 
                 use_random: bool = True):
        super().__init__(api_key, history, models_list, use_random)
        self.client = Groq(api_key=self.api_keys[self.current_key_index])
        self.logger = BaseLogger()

    def generate_answer(self, with_history: bool = True, prompt: list[dict[str, str]] | None = None) -> str:
        self.logger.log(InfoLog("Generating answer..."))
        if with_history:
            messages = self.history.history
        elif prompt is not None:
            messages = prompt
        
        chat_completion = None
        model_name = None

        while True:
            if len(self.regen_models_name) <= 0:
                self.logger.log(ErrorLog("No models available for use."))
                raise ModelExhaustedException("No models available for use.")
            
            model_name = self.regen_models_name[self.current_model_index]
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages, #type: ignore
                    model=model_name,

                )
                break
            except Exception as e:
                print(e)
                self.logger.log(WarningLog(f"Model {model_name} failed with error: {str(e)}. Trying next model..."))
                self.current_key_index = 0 if self.current_key_index + 1 >= len(self.api_keys) else self.current_key_index + 1
                if self.current_key_index == 0:
                    self.current_model_index = 0 if self.current_model_index + 1 >= len(self.regen_models_name) else self.current_model_index + 1
                    
                self.client = Groq(api_key=self.api_keys[self.current_key_index])

        result = chat_completion.choices[0].message.content
        self.logger.log(InfoLog(f"Generated answer with model {model_name}."))
        self.logger.log(InfoLog(f"Answer: {result}", level=2))
        if result is None:
            return ""
        
        return result
```

## Auto Doc Generator: Model and Factory Components
### Overview of Model Components

The **Model** components are responsible for generating answers using the GPT model. The `ParentModel` class serves as an abstract base class, defining the interface for models. The `Model` and `AsyncModel` classes implement the synchronous and asynchronous versions of the model, respectively.

### Model Contract

The model contract specifies the interface for models, which includes the following methods:

* `generate_answer`: generates an answer using the model
* `get_answer_without_history`: generates an answer without using the conversation history
* `get_answer`: generates an answer using the provided prompt

### Factory Components

The **Factory** components are responsible for generating documentation using the model. The `DocFactory` class serves as the main entry point for generating documentation. It takes a list of modules, each responsible for generating a specific part of the documentation.

### Factory Modules

The factory modules are responsible for generating specific parts of the documentation. The following modules are available:

* `CustomModule`: generates a custom description for the documentation
* `CustomModuleWithOutContext`: generates a custom description without using the context
* `IntroLinks`: generates an introduction to the links in the documentation
* `IntroText`: generates an introduction to the documentation

### Technical Logic Flow

The technical logic flow for the model and factory components is as follows:

1. The `DocFactory` class is initialized with a list of modules.
2. The `generate_doc` method is called, which generates the documentation using the modules.
3. Each module generates its part of the documentation using the `generate` method.
4. The `generate` method uses the model to generate an answer, which is then processed and added to the documentation.

### Data Contract

The data contract for the model and factory components specifies the input and output formats for the methods. The following table summarizes the data contract:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `info` | `dict` | Input | Dictionary containing information about the documentation |
| `model` | `Model` | Input | Model used to generate answers |
| `module_result` | `str` | Output | Result generated by a module |
| `doc_head` | `DocHeadSchema` | Output | Documentation head schema |

### Code Examples

The following code examples demonstrate how to use the model and factory components:
```python
# Initialize the DocFactory
factory = DocFactory(CustomModule("Custom description"))

# Generate the documentation
doc_head = factory.generate_doc({"code_mix": "code"}, Model())

# Print the documentation
print(doc_head.parts)
```
Note that this is a simplified example and you may need to add more modules and customize the factory to suit your specific use case.

## Manager Class Documentation
<a name="manager-class"></a>

The `Manager` class is responsible for orchestrating the pipeline, holding shared state and configuration. It provides methods for generating code files, global information, documentation parts, and ordering the documentation.

### Attributes
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `doc_info` | `DocInfoSchema` | Stores documentation information |  |
| `config` | `Config` | Stores configuration settings |  |
| `project_directory` | `str` | Project directory path |  |
| `llm_model` | `Model` | LLM model instance |  |
| `embedding_model` | `Embedding` | Embedding model instance |  |
| `logger` | `BaseLogger` | Logger instance |  |
| `progress_bar` | `BaseProgress` | Progress bar instance |  |

### Methods
#### `init_folder_system`
 Initializes the folder system by creating the cache directory if it does not exist.

#### `read_file_by_file_key`
 Reads a file by its key.

#### `get_file_path`
 Gets the file path by its key.

#### `generate_code_file`
 Generates the code file by building the repository content.

#### `generate_global_info`
 Generates global information by compressing the code mix.

#### `generete_doc_parts`
 Generates documentation parts by splitting the code mix and generating documentation for each part.

#### `factory_generate_doc`
 Generates documentation using a doc factory.

#### `create_embedding_layer`
 Creates an embedding layer for the documentation parts.

#### `order_doc`
 Orders the documentation parts.

#### `clear_cache`
 Clears the cache by removing the logs file if save logs is disabled.

#### `save`
 Saves the documentation to a file.

### Usage
To use the `Manager` class, create an instance and call the desired methods. For example:
```python
manager = Manager(project_directory, config, llm_model, embedding_model)
manager.generate_code_file()
manager.generate_global_info()
manager.generete_doc_parts()
manager.factory_generate_doc(doc_factory)
manager.create_embedding_layer()
manager.order_doc()
manager.save()
```
Note: This documentation is based on the provided code snippet and may not be comprehensive. Additional functionality and details may be present in the complete codebase.

## Custom Introduction and Embedding
### Overview of Introduction Generation

The introduction generation process involves multiple steps, including extracting HTML links from the documentation, generating an introduction with links, and creating a custom description.

#### Introduction Generation Process
1. **Extracting HTML Links**: The `get_all_html_links` function extracts HTML links from the documentation using a regular expression. It logs the number of extracted links and the links themselves.
2. **Generating Introduction with Links**: The `get_links_intro` function generates an introduction with links using a language model. It takes the extracted links, a language model, and a language as input and returns the generated introduction.
3. **Generating Custom Description**: The `generete_custom_discription` function generates a custom description using a language model. It takes the split data, a language model, a custom description, and a language as input and returns the generated description.

#### Embedding Process
The embedding process involves sorting vectors by distance.

#### Sorting Vectors
1. **Bubble Sort**: The `bubble_sort_by_dist` function sorts a list of vectors by distance using the bubble sort algorithm.
2. **Getting Vector Length**: The `get_len_btw_vectors` function calculates the length between two vectors using the Euclidean norm.
3. **Sorting Vectors**: The `sort_vectors` function sorts a dictionary of vectors by distance from a root vector.

### Embedding Class
The `Embedding` class encapsulates the embedding functionality.

#### Embedding Initialization
The `__init__` method initializes the embedding client with an API key.

#### Getting Vector
The `get_vector` method gets a vector for a given prompt using the Gemini embedding model.

### Usage
To use the introduction generation and embedding functionality, create an instance of the `Embedding` class and use its methods.

```python
embedding = Embedding(api_key)
vector = embedding.get_vector(prompt)
```

### Data Contract

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| links | list[str] | Input | Extracted HTML links |
| model | Model | Input | Language model |
| language | str | Input | Language for introduction generation |
| intro_links | str | Output | Generated introduction with links |
| custom_description | str | Input | Custom description for generation |
| root_vector | list | Input | Root vector for sorting |
| other | dict[str, Any] | Input | Dictionary of vectors for sorting |
| sorted_list | list[str] | Output | Sorted list of vector names |

### Technical Logic Flow

1. Extract HTML links from documentation using `get_all_html_links`.
2. Generate introduction with links using `get_links_intro`.
3. Generate custom description using `generete_custom_discription`.
4. Initialize embedding client with API key using `Embedding`.
5. Get vector for prompt using `get_vector`.
6. Sort vectors by distance using `sort_vectors`.

### Notes
* The introduction generation process uses a language model to generate text.
* The embedding process uses the Gemini embedding model to get vectors.
* The sorting process uses the bubble sort algorithm to sort vectors by distance.

## CodeMix and Sorting Components
The `CodeMix` and `Sorting` components are crucial parts of the AutoDocGenerator system. 

### CodeMix Component
The `CodeMix` component is responsible for preprocessing the source code, creating a unified string representation of the repository structure and code content. This is achieved through the `build_repo_content` method, which:
1. Iterates over all files in the repository, ignoring specified patterns.
2. Creates a structured representation of the repository, including file names and contents.
3. Returns the unified string representation.

The `CodeMix` class also includes an `should_ignore` method to determine whether a file should be ignored based on the provided patterns.

### Sorting Component
The `Sorting` component is responsible for sorting the code chunks semantically. This is achieved through the following methods:
1. `extract_links_from_start`: Extracts HTML links from the start of each chunk.
2. `split_text_by_anchors`: Splits the text into chunks based on anchor tags.
3. `get_order`: Uses a language model to sort the chunks semantically.

The `get_order` method takes a list of chunk names and a language model as input, and returns a sorted list of chunk names.

### Component Interactions
The `CodeMix` and `Sorting` components interact as follows:
1. The `CodeMix` component preprocesses the source code, creating a unified string representation.
2. The `Sorting` component takes the preprocessed string and splits it into chunks based on anchor tags.
3. The `Sorting` component uses a language model to sort the chunks semantically.

### Data Contract

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| repository_path | str | Input | Path to the repository |
| ignore_patterns | list[str] | Input | List of patterns to ignore |
| preprocessed_string | str | Output | Unified string representation of the repository |
| chunk_names | list[str] | Input | List of chunk names |
| language_model | Model | Input | Language model for semantic sorting |
| sorted_chunk_names | list[str] | Output | Sorted list of chunk names |

### Technical Logic Flow

1. Preprocess the source code using `CodeMix`.
2. Split the preprocessed string into chunks based on anchor tags using `Sorting`.
3. Sort the chunks semantically using `Sorting` and a language model.
4. Return the sorted list of chunk names.

### Notes
* The `CodeMix` component ignores files based on specified patterns.
* The `Sorting` component uses a language model to sort the chunks semantically.
* The components interact to create a sorted representation of the repository structure and code content. 

Here is the high-level code representation for this: 
```python
class CodeMix:
    def __init__(self, root_dir=".", ignore_patterns=None):
        # ...

    def build_repo_content(self):
        # ...

class Sorting:
    def extract_links_from_start(self, chunks):
        # ...

    def split_text_by_anchors(self, text):
        # ...

    def get_order(self, model, chunk_names):
        # ...

# Usage
code_mix = CodeMix(root_dir="path/to/repo", ignore_patterns=["*.pyc", "__pycache__"])
preprocessed_string = code_mix.build_repo_content()

sorting = Sorting()
chunk_names = sorting.split_text_by_anchors(preprocessed_string)
sorted_chunk_names = sorting.get_order(model, chunk_names)
```

##
<a name="manager-class-usage"></a>
The Manager class is used to manage the generation of documentation. It has several methods available for this purpose. 

To use the Manager class, you first need to create an instance of it, passing in the project path, config, llm model, embedding model, and progress bar as arguments. 

Here's an example of how to create a Manager instance:
```python
manager = Manager(
    project_path, 
    config=config,
    llm_model=sync_model,
    embedding_model=embedding_model,
    progress_bar=ConsoleGtiHubProgress(), 
)
```

The Manager class has several methods available, including:

- `generate_code_file()`: This method generates the code file.
```python
manager.generate_code_file()
```

- `generate_global_info(compress_power)`: This method generates the global info with the specified compress power.
```python
manager.generate_global_info(compress_power=4)
```

- `generete_doc_parts(max_symbols, with_global_file)`: This method generates the doc parts with the specified max symbols and with or without the global file.
```python
manager.generete_doc_parts(max_symbols=structure_settings.max_doc_part_size, with_global_file=structure_settings.use_global_file)
```

- `factory_generate_doc(DocFactory, to_start)`: This method generates the doc using the specified DocFactory and with the option to append to the start.
```python
manager.factory_generate_doc(DocFactory(*custom_modules))
```
or
```python
manager.factory_generate_doc(DocFactory(*additionals_modules, with_splited=False), to_start=True)
```

- `order_doc()`: This method orders the doc.
```python
manager.order_doc()
```

- `create_embedding_layer()`: This method creates the embedding layer.
```python
manager.create_embedding_layer()
```

- `clear_cache()`: This method clears the cache.
```python
manager.clear_cache()
```

- `save()`: This method saves the doc.
```python
manager.save()
```

- `get_file_path(file_name, is_outside)`: This method returns the file path for the specified file name and with the option to be outside the project path.
```python
manager.get_file_path(".auto_doc_cache_file", is_outside=True)
```

- `read_file_by_file_key(file_name, is_outside)`: This method reads the file by the file key with the option to be outside the project path.
```python
manager.read_file_by_file_key(".auto_doc_cache_file", is_outside=True)
```
<a name="compressor-component"></a> Compressor Component
The compressor component is responsible for compressing the preprocessed data into a unified string representation. This is achieved through the `compress` and `compress_and_compare` functions.

###
<a name="compress-function"></a> Compress Function
The `compress` function takes in the following parameters:
* `data`: The preprocessed string data to be compressed
* `project_settings`: The project settings, including the prompt and other configuration
* `model`: The language model used for compression
* `compress_power`: The power of compression, which determines the level of compression

The function creates a prompt for the language model, which includes the project settings and the data to be compressed. The prompt is then used to get an answer from the language model without history, and the answer is returned as the compressed string.

###
<a name="compress-and-compare-function"></a> Compress and Compare Function
The `compress_and_compare` function takes in the following parameters:
* `data`: The list of strings to be compressed and compared
* `model`: The language model used for compression and comparison
* `project_settings`: The project settings, including the prompt and other configuration
* `compress_power`: The power of compression, which determines the level of compression
* `progress_bar`: The progress bar used to track the progress of the compression and comparison process

The function iterates over the input data, compressing each string using the `compress` function and comparing the results. The compressed strings are then combined into a single list, and the progress bar is updated to reflect the progress of the process.

###
<a name="compress-to-one-function"></a> Compress to One Function
The `compress_to_one` function takes in the following parameters:
* `data`: The list of strings to be compressed
* `model`: The language model used for compression
* `project_settings`: The project settings, including the prompt and other configuration
* `compress_power`: The power of compression, which determines the level of compression
* `progress_bar`: The progress bar used to track the progress of the compression process

The function repeatedly applies the `compress_and_compare` function to the input data, reducing the number of strings in the list until only one string remains. The final compressed string is then returned.

###
<a name="split-data-function"></a> Split Data Function
The `split_data` function is used to split the preprocessed data into smaller chunks.

###
<a name="split-data-parameters"></a> Split Data Parameters
The `split_data` function takes the following parameters:
* `data`: The preprocessed string data to be split.
* `max_symbols`: The maximum number of symbols in each chunk.

###
<a name="split-data-return-value"></a> Split Data Return Value
The `split_data` function returns a list of strings, where each string is a chunk of the input data.

###
<a name="split-data-functionality"></a> Split Data Functionality
###
<a name="technical-logic-flow"></a> Technical Logic Flow
The technical logic flow includes the following steps:
1. Create a logger using the `BaseLogger` class.
2. Create a progress bar using the `BaseProgress` class.
3. Use the logger to log messages.
4. Use the progress bar to update the progress.

##
<a name="functional-flow"></a> Functional Flow
The functional flow of the project is as follows:
1. The `Manager` initializes the pipeline, creating a cache folder and setting up the configuration.
2. The `CodeMix` preprocesses the source code, producing a unified string.
3. The `DocFactory` generates documentation using LLMs, with optional post-processing.
4. The `Embedding` generates vector embeddings for doc parts.
5. The `Manager` saves the final documentation and schema.

###
<a name="component-logic"></a> Component Logic
The project consists of the following components:
* **`Manager`**: Orchestrates the pipeline, holding shared state and configuration.
* **`CodeMix`**: Preprocesses source code into a unified string.
* **`DocFactory`**: Generates documentation via LLMs and post-processing.
* **`Embedding`**: Wraps generated doc parts with vector embeddings.
* **`Config`**: Stores global settings and cache metadata.

###
<a name="key-context-for-snippets"></a> Key Context for Snippets
* **Shared State:** `Manager` instance holds `doc_info`, `config`, and `llm_model`.
* **Cache Folder:** `.auto_doc_cache` stores intermediate artifacts.
* **Entry Points:** `Manager.generate_code_file`, `Manager.generate_global_info`, `Manager.generate_doc_parts`, `Manager.factory_generate_doc`.
* **Terminal Points:** `Manager.save` writes final markdown and schema.

##
<a name="logger-functionality"></a> Logger Functionality
The logger functionality is implemented using the following classes:
- `BaseLog`: This class is the base class for all logs. It has a `message` attribute and a `level` attribute.
- `ErrorLog`, `WarningLog`, `InfoLog`: These classes inherit from `BaseLog` and override the `format` method to include the log level.
- `BaseLoggerTemplate`: This class is a template for loggers. It has a `log_level` attribute and methods for logging and global logging.
- `FileLoggerTemplate`: This class inherits from `BaseLoggerTemplate` and logs to a file.
- `BaseLogger`: This class is a singleton that provides a global logger.

##
<a name="progress-bar-functionality"></a> Progress Bar Functionality
The progress bar functionality is implemented using the following classes:
- `BaseProgress`: This class is the base class for progress bars. It has methods for creating new subtasks, updating tasks, and removing subtasks.
- `LibProgress`: This class inherits from `BaseProgress` and uses the `rich` library to create a progress bar.
- `ConsoleTask`: This class represents a task with a name and a total length. It has methods for starting the task and updating the progress.
- `ConsoleGtiHubProgress`: This class inherits from `BaseProgress` and uses `ConsoleTask` to create a progress bar.

##
