## Executive Navigation Tree
* 📂 Project Overview
  * [AutoDoc Generator Project](#autodoc-generator-project)
  * [Project Description](#project-description)
  * [Intro Links](#intro-links)
  * [Intro Text](#intro-text)
* ⚙️ Installation and Setup
  * [Installation Workflow Description](#installation-workflow-description)
  * [Installation Scripts](#installation-scripts)
  * [Windows Installation Script](#windows-installation-script)
  * [Linux Installation Script](#linux-installation-script)
* 📄 Core Engine
  * [Project Metadata](#project-metadata)
  * [Dependencies](#dependencies)
  * [Build System](#build-system)
  * [Package Initialization and Logger Setup](#package-initialization-and-logger-setup)
* 📊 Logging and Progress Tracking
  * [Logging Component](#logging-component)
  * [Log Classes](#log-classes)
  * [Logger Classes](#logger-classes)
  * [Progress Tracking Component](#progress-tracking-component)
  * [Progress Classes](#progress-classes)
* 📈 Configuration and Management
  * [Config Reader Read Config](#config-reader-read-config)
  * [Run File Gen Doc](#run-file-gen-doc)
  * [AutoDoc Configuration Options](#autodoc-configuration-options)
  * [Manager Class Usage and Methods](#manager-class-usage-and-methods)
  * [Manager Factory](#manager-factory)
  * [Manager Orchestration](#manager-orchestration)
  * [Manager Read File](#manager-read-file)
  * [Manager Generate Code](#manager-generate-code)
  * [Manager Gen Parts](#manager-gen-parts)
  * [Manager Order](#manager-order)
  * [Manager Clear](#manager-clear)
* 📁 Modules and Functionality
  * [Base Module](#base-module)
  * [Custom Module](#custom-module)
  * [Custom Module No Context](#custom-module-no-context)
  * [Doc Factory](#doc-factory)
  * [GPT Model](#gpt-model)
  * [Async GPT Model](#async-gpt-model)
* 📊 Data Processing
  * [Data Splitting Mechanism](#data-splitting-mechanism)
  * [Split Data Function](#split-data-function)
  * [Write Docs by Parts Function](#write-docs-by-parts-function)
  * [Async Write Docs by Parts Function](#async-write-docs-by-parts-function)
  * [Gen Doc Parts Function](#gen-doc-parts-function)
  * [Async Gen Doc Parts Function](#async-gen-doc-parts-function)
* 📈 Module Functionalities
  * [Sorting Module Functionality](#sorting-module-functionality)
  * [Code Mix Module Functionality](#code-mix-module-functionality)
  * [Compressor Module Functionality](#compressor-module-functionality)
* 📊 Interactions and Logic
  * [Visible Interactions](#visible-interactions)
  * [Visible Interactions 1](#visible-interactions-1)
  * [Visible Interactions 2](#visible-interactions-2)
  * [Visible Interactions 3](#visible-interactions-3)
  * [Visible Interactions 4](#visible-interactions-4)
  * [Visible Interactions 5](#visible-interactions-5)
  * [Technical Logic Flow](#technical-logic-flow)
  * [Technical Logic Flow 1](#technical-logic-flow-1)
  * [Technical Logic Flow 2](#technical-logic-flow-2)
  * [Technical Logic Flow 3](#technical-logic-flow-3)
  * [Technical Logic Flow 4](#technical-logic-flow-4)
  * [Technical Logic Flow 5](#technical-logic-flow-5)
* 📄 Data Contract
  * [Data Contract](#data-contract)
  * [Data Contract 1](#data-contract-1)
  * [Data Contract 2](#data-contract-2)
  * [Data Contract 3](#data-contract-3)
  * [Data Contract 4](#data-contract-4)
  * [Data Contract 5](#data-contract-5)

 

<a name="autodoc-generator-project"></a> AutoDoc Generator Project
### 
<a name="project-description"></a> Project Description
The AutoDoc Generator project is designed to help developers generate documentation for their projects. The project includes various components, such as logging, progress tracking, and installation scripts.

### 
<a name="intro-links"></a>
## `IntroLinks` – HTML‑Link Intro Builder  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `generate` | `def` → `str` | Extracts links and builds intro | Calls `get_all_html_links` then `get_links_intro` |

**Logic Flow**  
1. Extract all HTML links from `info["full_data"]`.  
2. Pass links, `model`, and language to `get_links_intro`.  
3. Return the generated introductory text.

**Visible Interactions**  
- Depends on `get_all_html_links` and `get_links_intro` from `postprocessor.custom_intro`.  

--- 
<a name="intro-text"></a>
## `IntroText` – Global Data Intro Builder  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `generate` | `def` → `str` | Produces introductory paragraph from global data | Calls `get_introdaction` |

**Logic Flow**  
1. Retrieve `global_data` from `info`.  
2. Invoke `get_introdaction` with this data, `model`, and language.  
3. Return the resulting text.

**Visible Interactions**  
- Utilises `get_introdaction` from `postprocessor.custom_intro`. 
<a name="installation-workflow-description"></a>
The installation process utilizes two scripts: one for PowerShell and one for Linux-based systems. To install using PowerShell, the command `irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex` is used. This command downloads the `install.ps1` script from the specified repository and executes it directly in the PowerShell environment.

For Linux-based systems, the installation command is `curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash`. This command downloads the `install.sh` script from the repository and pipes it to the Bash shell for execution.

To complete the installation and make it functional, a secret variable named `GROCK_API_KEY` must be added to the GitHub Actions configuration. The value for this variable should be obtained from the GROCK documentation portal, found at https://grockdocs.com. This API key is necessary for integrating with GROCK services and must be kept secure to prevent unauthorized access.

Here is a rewritten version with precise steps:

1. **For Windows (PowerShell):**
   - Open PowerShell.
   - Execute the command: `irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex`
   - Follow any additional prompts from the script.

2. **For Linux-Based Systems:**
   - Open a terminal.
   - Execute the command: `curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash`
   - Follow any additional prompts from the script.

3. **Configuring GitHub Actions:**
   - Navigate to your repository on GitHub.
   - Go to the "Actions" tab and then click on "Workflows".
   - Find your workflow and click on the three dots next to it, then select "Edit".
   - In the workflow editor, click on the "Actions" tab on the left and scroll down to "Secrets".
   - Add a new secret named `GROCK_API_KEY`.
   - Paste your API key from GROCK into the value field for `GROCK_API_KEY`.
   - Save the changes to your workflow.

This process ensures that the necessary scripts are executed for installation and that the required API key is securely stored for use with GROCK services. 
<a name="installation-scripts"></a> Installation Scripts
The project includes installation scripts for Windows and Linux, which create the necessary files and directories for the project.

#### 
<a name="windows-installation-script"></a> Windows Installation Script
The Windows installation script is written in PowerShell and creates the `.github/workflows` directory and the `autodocconfig.yml` file.

#### 
<a name="linux-installation-script"></a> Linux Installation Script
The Linux installation script is written in Bash and creates the `.github/workflows` directory and the `autodocconfig.yml` file.

### 
<a name="project-metadata"></a> Project Metadata
The project metadata is defined in the `pyproject.toml` file. The key metadata points are:
* **Project Name:** `autodocgenerator`
* **Version:** `0.9.0.2`
* **Description:** `This Project helps you to create docs for your projects`
* **Authors:** `dima-on <sinica911@gmail.com>`
* **License:** `MIT`
* **Python Version:** `>=3.11,<4.0`

## 
<a name="dependencies"></a> Dependencies
The project dependencies are listed in the `pyproject.toml` file. The dependencies are:
| Dependency | Version |
| --- | --- |
| annotated-types | 0.7.0 |
| pyyaml | 6.0.3 |
| anyio | 4.12.1 |
| CacheControl | 0.14.4 |
| certifi | 2026.1.4 |
| charset-normalizer | 3.4.4 |
| cleo | 2.1.0 |
| colorama | 0.4.6 |
| crashtest | 0.4.1 |
| distlib | 0.4.0 |
| distro | 1.9.0 |
| dulwich | 0.25.2 |
| fastjsonschema | 2.21.2 |
| filelock | 3.20.3 |
| findpython | 0.7.1 |
| google-auth | 2.47.0 |
| google-genai | 1.56.0 |
| groq | 1.0.0 |
| h11 | 0.16.0 |
| httpcore | 1.0.9 |
| httpx | 0.28.1 |
| idna | 3.11 |
| installer | 0.7.0 |
| jaraco.classes | 3.4.0 |
| jaraco.context | 6.1.0 |
| jaraco.functools | 4.4.0 |
| jiter | 0.12.0 |
| keyring | 25.7.0 |
| markdown-it-py | 4.0.0 |
| mdurl | 0.1.2 |
| more-itertools | 10.8.0 |
| msgpack | 1.1.2 |
| openai | 2.14.0 |
| packaging | 25.0 |
| pbs-installer | 2026.1.14 |
| pkginfo | 1.12.1.2 |
| platformdirs | 4.5.1 |
| pyasn1 | 0.6.1 |
| pyasn1_modules | 0.4.2 |
| pydantic | 2.12.5 |
| pydantic_core | 2.41.5 |
| Pygments | 2.19.2 |
| pyproject_hooks | 1.2.0 |
| python-dotenv | 1.2.1 |
| pywin32-ctypes | 0.2.3 |
| RapidFuzz | 3.14.3 |
| requests | 2.32.5 |
| requests-toolbelt | 1.0.0 |
| rich | 14.2.0 |
| rich_progress | 0.4.0 |
| rsa | 4.9.1 |
| shellingham | 1.5.4 |
| sniffio | 1.3.1 |
| tenacity | 9.1.2 |
| tomlkit | 0.14.0 |
| tqdm | 4.67.1 |
| trove-classifiers | 2026.1.14.14 |
| typing_extensions | 4.15.0 |
| typing-inspection | 0.4.2 |
| urllib3 | 2.6.2 |
| virtualenv | 20.36.1 |
| websockets | 15.0.1 |
| zstandard | 0.25.0 |

## 
<a name="build-system"></a> Build System
The build system is defined in the `pyproject.toml` file. The build system is:
* **Requires:** `poetry-core>=2.0.0`
* **Build Backend:** `poetry.core.masonry.api` 
<a name="package-initialization-and-logger-setup"></a>
## Package Initialization and Logger Setup

**Functional Role**  
Initializes the `autodocgenerator` package and configures a global logger instance (`logger`) that other modules can use for structured logging.

**Visible Interactions**  
- Imports logging primitives from `autodocgenerator.ui.logging`.  
- Instantiates `BaseLogger` → creates an object capable of routing log messages.  
- Calls `BaseLogger.set_logger` with a `BaseLoggerTemplate` instance, selecting the concrete logging format/handler.  
- Emits a side‑effect `print("ADG")` to standard output when the package is first imported.

**Step‑by‑Step Logic Flow**  

1. **Execute top‑level `print`** – writes the literal string `ADG` to `stdout`.  
2. **Import statements** – bring `BaseLogger`, `BaseLoggerTemplate`, `InfoLog`, `ErrorLog`, `WarningLog` into the module namespace. No runtime side‑effects beyond standard import mechanics.  
3. **Instantiate logger** – `logger = BaseLogger()` creates a fresh logger object.  
4. **Configure logger** – `logger.set_logger(BaseLoggerTemplate())` attaches a default template (format/handler) to the logger, preparing it for subsequent use by other package components.

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `print("ADG")` | Side‑effect (stdout) | Simple visual cue confirming package import | No return value |
| `BaseLogger` | Class (import) | Core logging orchestrator | Imported from `.ui.logging` |
| `BaseLoggerTemplate` | Class (import) | Concrete logging template/handler | Imported from `.ui.logging` |
| `logger` | Instance of `BaseLogger` | Global logger used across the package | Created at import time |
| `logger.set_logger(...)` | Method call | Binds a `BaseLoggerTemplate` to `logger` | Must be called before any log emission |

> **Assumption** – The imported logging classes behave as typical logger factories; no further details are available in the provided fragment.  

**Implications for Consumers**  
Any module that does `from autodocgenerator import logger` will receive a ready‑to‑use logger already configured with the default template, eliminating the need for repetitive logger setup. The initial `print` may be removed or silenced in production if console noise is undesired. 
<a name="logging-component"></a> Logging Component
The logging component is responsible for handling log messages in the system. It includes several classes, including `BaseLog`, `ErrorLog`, `WarningLog`, and `InfoLog`, which represent different types of log messages.

#### 
<a name="log-classes"></a> Log Classes
The following log classes are available:
* `BaseLog`: The base class for all log messages.
* `ErrorLog`: Represents an error log message.
* `WarningLog`: Represents a warning log message.
* `InfoLog`: Represents an information log message.

#### 
<a name="logger-classes"></a> Logger Classes
The following logger classes are available:
* `BaseLoggerTemplate`: The base class for all loggers.
* `FileLoggerTemplate`: A logger that logs messages to a file.
* `BaseLogger`: A singleton logger that can be used to log messages.

### 
<a name="progress-tracking-component"></a> Progress Tracking Component
The progress tracking component is responsible for tracking the progress of tasks in the system. It includes several classes, including `BaseProgress`, `LibProgress`, `ConsoleTask`, and `ConsoleGtiHubProgress`, which represent different types of progress trackers.

#### 
<a name="progress-classes"></a> Progress Classes
The following progress classes are available:
* `BaseProgress`: The base class for all progress trackers.
* `LibProgress`: A progress tracker that uses the `rich.progress` library.
* `ConsoleTask`: A progress tracker that logs progress to the console.
* `ConsoleGtiHubProgress`: A progress tracker that logs progress to the console in a GitHub-style format.

### 
<a name="config-reader-read-config"></a>  
## `read_config` – YAML‑Based Configuration Loader  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_data` | `str` | Raw YAML content | Must be UTF‑8 decoded before call |
| `config` | `Config` | Central project configuration object | Populated via setters |
| `custom_modules` | `list[CustomModule]` | User‑defined documentation extensions | `%`‑prefixed entries become `CustomModuleWithOutContext` |
| `structure_settings_object` | `StructureSettings` | Controls documentation layout | Defaults are overridden by `structure_settings` key |

> **Assumption** – `yaml.safe_load` returns a dictionary matching the expected schema; no validation beyond key existence is performed.

**Logic Flow**  
1. Parse `file_data` with `yaml.safe_load`.  
2. Instantiate a fresh `Config`.  
3. Extract `ignore_files`, `language`, `project_name`, and `project_additional_info` from the dict, applying defaults where missing.  
4. Load build‑time options into a `ProjectBuildConfig` (`pcs`) and attach it to `config` via `set_pcs`.  
5. Populate `config.ignore_files` and additional info using `add_ignore_file` / `add_project_additional_info`.  
6. Build `custom_modules` list: each entry is a two‑element sequence; if the first element is `"%"` the second element is wrapped in `CustomModuleWithOutContext`, otherwise in `CustomModule`.  
7. Create a `StructureSettings` instance, overwrite its attributes with any supplied `structure_settings` dict.  
8. Return the triple `(config, custom_modules, structure_settings_object)`.

**Visible Interactions**  
- Relies on `CustomModule`, `CustomModuleWithOutContext` from `autodocgenerator.factory.modules.general_modules`.  
- Consumes `Config` and `ProjectBuildConfig` from `autodocgenerator.config.config`.  
- No side‑effects beyond object construction.

--- 
<a name="run-file-gen-doc"></a>  
## `gen_doc` – Orchestrator for Automated Documentation Generation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_path` | `str` | Root directory of target project | Passed to `Manager` |
| `config` | `Config` | Project‑wide settings | Supplied by `read_config` |
| `custom_modules` | `list[CustomModule\|CustomModuleWithOutContext]` | Extensible documentation hooks | Injected into `DocFactory` |
| `structure_settings` | `StructureSettings` | Layout directives (e.g., `max_doc_part_size`) | Controls ordering and intro links |
| Return value | `str` | Final assembled documentation | Retrieved via `Manager.read_file_by_file_key("output_doc")` |

> **Assumption** – `Manager` methods (`generate_code_file`, `generete_doc_parts`, `factory_generate_doc`, `order_doc`, `clear_cache`) perform I/O and caching internally; their signatures are not exposed here.

**Logic Flow**  
1. Initialise synchronous (`GPTModel`) and asynchronous (`AsyncGPTModel`) language‑model clients using the global `API_KEY`.  
2. Construct a `Manager` with the project path, configuration, both models, and a console progress bar (`ConsoleGtiHubProgress`).  
3. Invoke `manager.generate_code_file()` to collect source files.  
4. Split generated content into chunks respecting `structure_settings.max_doc_part_size` via `manager.generete_doc_parts`.  
5. Feed the `custom_modules` into a `DocFactory` and generate documentation (`manager.factory_generate_doc`).  
6. If `include_order` is true, reorder sections (`manager.order_doc`).  
7. If `include_intro_links` is true, prepend intro links using an `IntroLinks` factory instance.  
8. Flush temporary data (`manager.clear_cache`).  
9. Return the assembled document text.

**Visible Interactions**  
- Imports `DocFactory`, `IntroLinks`, `ConsoleGtiHubProgress`, `GPTModel`, `AsyncGPTModel`, and `API_KEY`.  
- Delegates all heavy lifting to `Manager`; this function solely wires components together.  

--- 
<a name="autodoc-configuration-options"></a>
The autodocconfig.yml file has several options available. The file is used to configure the Auto Doc Generator project. The available options include:
- project_name: This is used to specify the name of the project.
- language: This option is used to specify the language of the project.
- build_settings: This has two sub-options: 
  - save_logs: This is a boolean value that determines whether to save logs or not.
  - log_level: This is used to set the log level, with higher values indicating more detailed logging.
- structure_settings: This has three sub-options: 
  - include_intro_links: This is a boolean value that determines whether to include intro links or not.
  - include_order: This is a boolean value that determines whether to include order or not.
  - max_doc_part_size: This is used to set the maximum size of a documentation part.
- project_additional_info: This has one sub-option: 
  - global idea: This is used to provide a global idea or description of the project.
- custom_descriptions: This is a list of custom descriptions that can be used to provide additional information about the project. 
<a name="manager-class-usage-and-methods"></a>
The Manager class is used to manage the generation of documents. To use the Manager class, you need to create an instance of it, passing in the project path, config, sync model, async model, and progress bar. 

Here is an example of how to use the Manager class:
```python
manager = Manager(
    project_path, 
    config=config,
    sync_model=sync_model,
    async_model=async_model,
    progress_bar=ConsoleGtiHubProgress(), 
)
```
The Manager class has the following methods available:
- `generate_code_file()`: This method is used to generate the code file.
```python
manager.generate_code_file()
```
- `generete_doc_parts(max_symbols)`: This method is used to generate the doc parts. It takes one argument, `max_symbols`, which specifies the maximum number of symbols.
```python
manager.generete_doc_parts(max_symbols=structure_settings.max_doc_part_size)
```
- `factory_generate_doc(doc_factory)`: This method is used to generate the doc using a doc factory. It takes one argument, `doc_factory`, which is an instance of the DocFactory class.
```python
manager.factory_generate_doc(DocFactory(*custom_modules))
```
- `order_doc()`: This method is used to order the doc.
```python
manager.order_doc()
```
- `clear_cache()`: This method is used to clear the cache.
```python
manager.clear_cache()
```
- `read_file_by_file_key(key)`: This method is used to read a file by its key. It takes one argument, `key`, which specifies the key of the file to read.
```python
output_doc = manager.read_file_by_file_key("output_doc")
``` 
<a name="manager-factory"></a>
## `Manager.factory_generate_doc` – Modular Post‑Processing  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `doc_factory` | `DocFactory` | Container of `BaseModule` instances | Provides `modules` attribute |
| Return | `None` | Appends factory‑generated text to existing doc | Writes back to cache |

**Logic Flow**  
1. Load current output and code‑mix.  
2. Assemble `info` dict (`language`, `full_data`, `code_mix`).  
3. Log start with module list and input sizes.  
4. Call `doc_factory.generate_doc(info, sync_model, progress_bar)`.  
5. Prepend result to existing document, write file, log completion, update progress.  

**Visible Interactions** – Relies on `DocFactory` and its modules (e.g., `IntroLinks`, `CustomModule`).  

--- 
<a name="manager-orchestration"></a>
## `Manager` – Core Orchestration  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_directory` | `str` | Root path of the target project | Provided to ctor |
| `config` | `Config` | Runtime configuration (languages, logging, ignore rules) | Stored as `self.config` |
| `sync_model` / `async_model` | `Model` / `AsyncModel` | LLM interfaces for synchronous / asynchronous calls | Optional |
| `progress_bar` | `BaseProgress` | UI progress feedback | Defaults to a fresh instance |
| `logger` | `BaseLogger` | Centralised file logger | Writes to `logs` cache file |

**Logic Flow**  
1. Store ctor arguments, create a **FileLoggerTemplate** bound to `self.get_file_path("logs")`.  
2. Ensure a hidden cache directory ```.auto_doc_cache``` exists under `project_directory`.  

> **Note**: All side‑effects (directory creation, logger setup) occur in `__init__`.

--- 
<a name="manager-read-file"></a>
## `Manager.read_file_by_file_key` – Cached File Reader  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_key` | `str` | Identifier from `FILE_NAMES` | Maps to a concrete filename |
| Return | `str` | Full file contents | UTF‑8 read |

**Logic Flow**  
1. Resolve absolute path via `self.get_file_path(file_key)`.  
2. Open the file in read mode, return its text.  

**Visible Interactions** – Uses Python `open`, relies on the cache layout created by `__init__`.

--- 
<a name="manager-generate-code"></a>
## `Manager.generate_code_file` – Repository Code‑Mix Builder  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| None | – | Triggers `CodeMix` to produce a combined source dump | Output stored at ``code_mix.txt`` |

**Logic Flow**  
1. Log start (`InfoLog`).  
2. Instantiate `CodeMix(project_directory, config.ignore_files)`.  
3. Call `cm.build_repo_content(self.get_file_path("code_mix"))`.  
4. Log completion, advance `progress_bar`.  

**Visible Interactions** – Imports `CodeMix` (pre‑processor) and `InfoLog` (logging).  

--- 
<a name="manager-gen-parts"></a>
## `Manager.generete_doc_parts` – Synchronous Chunked Documentation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `max_symbols` | `int` | Upper bound per chunk (default 5 000) | Passed to `gen_doc_parts` |
| Return | `None` | Writes assembled markdown to ``output_doc.md`` | Side‑effect only |

**Logic Flow**  
1. Load full code‑mix via `read_file_by_file_key`.  
2. Log start, invoke `gen_doc_parts` with code, model, settings, language, and `progress_bar`.  
3. Write returned string to the output cache file.  
4. Log finish, update progress.  

**Visible Interactions** – Calls `gen_doc_parts` (pre‑processor) and `BaseLogger`.  

--- 
<a name="manager-order"></a>
## `Manager.order_doc` – Anchor‑Based Reordering  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| None | – | Splits document by ``<a name=...>`` anchors, reorders via LLM | Uses `split_text_by_anchors` then `get_order` |

**Logic Flow**  
1. Read current output.  
2. Split into anchor blocks; abort if `None`.  
3. Pass blocks to `get_order` with `sync_model`.  
4. Overwrite output file with ordered content.  

**Visible Interactions** – Imports `split_text_by_anchors` and `get_order` (post‑processor).  

--- 
<a name="manager-clear"></a>
## `Manager.clear_cache` – Conditional Log Cleanup  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| None | – | Removes ``report.txt`` unless `config.pbc.save_logs` is `True` | Uses `os.remove` |

**Logic Flow**  
1. Check `self.config.pbc.save_logs`.  
2. If falsy, delete the log file via its cached path.  

**Visible Interactions** – Direct filesystem operation; no external module calls.  

## Auto Doc Generator: Custom Introduction Module
### Overview of Custom Introduction Generation

The provided code snippet is part of the Auto Doc Generator project, specifically within the `custom_intro.py` file. This module is responsible for generating custom introductions for documentation, including extracting HTML links, creating introductions with links, and generating custom descriptions.

### Entity Relationship Table

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Input data for link extraction | String containing HTML links |
| `links` | `list[str]` | Extracted HTML links | List of anchor names |
| `model` | `Model` | Language model for introduction generation | Instance of `GPTModel` or other language models |
| `language` | `str` | Language for introduction generation | Default language is "en" |
| `global_data` | `str` | Input data for introduction generation | String containing global data |
| `custom_description` | `str` | Custom description for generation | String describing the task |

### Logic Flow

The custom introduction module follows this logic flow:

1. **Link Extraction**: The `get_all_html_links` function extracts HTML links from the input data using regular expressions.
2. **Introduction with Links**: The `get_links_intro` function generates an introduction with links using the extracted links and a language model.
3. **Introduction Generation**: The `get_introdaction` function generates an introduction based on the global data and language model.
4. **Custom Description Generation**: The `generete_custom_discription` and `generete_custom_discription_without` functions generate custom descriptions based on the input data and language model.

### Visible Interactions

The custom introduction module interacts with the following external components:

* `GPTModel`: A language model used for introduction generation.
* `BaseLogger`: A logging module used for logging events.
* `InfoLog`: A logging module used for logging information.

### Context Lock

The custom introduction module operates within the context of the Auto Doc Generator project, using only the provided code snippet and explicit global context. No external knowledge or assumptions are made.

### Technical Requirements

The custom introduction module requires the following technical components:

* Python 3.x
* `re` module for regular expressions
* `GPTModel` or other language models for introduction generation
* `BaseLogger` and `InfoLog` modules for logging

### Content Requirements

The custom introduction module generates content based on the input data and language model. The generated content includes introductions with links, custom descriptions, and other documentation-related text. The content is generated in a technical and professional tone, targeting developers who need to understand the documentation instantly.

## 
<a name="base-module"></a>
## `BaseModule` – Abstract Generation Primitive  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `generate` | `abstractmethod` | Produce a documentation fragment | Receives `info: dict` and a concrete `Model` instance |
| `__init__` | `def` | Base constructor (no state) | May be extended by subclasses |

> **Assumption:** Subclasses must implement `generate`; the base class provides no default behavior.

--- 
<a name="custom-module"></a>
## `CustomModule` – Context‑Aware Description Generator  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `discription` | `str` | User‑provided narrative seed | Stored on init |
| `generate` | `def` → `str` | Calls `generete_custom_discription` | Splits `info["code_mix"]` (max 5000 symbols) before passing to post‑processor |

**Logic Flow**  
1. Retrieve `code_mix` from `info`, split via `split_data`.  
2. Invoke `generete_custom_discription` with split code, `model`, stored description, and `info["language"]`.  
3. Return the produced string.

**Visible Interactions**  
- Imports `split_data` (pre‑processor) and `generete_custom_discription` (post‑processor).  

--- 
<a name="custom-module-no-context"></a>
## `CustomModuleWithOutContext` – Stand‑Alone Description Generator  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `discription` | `str` | Narrative seed | Stored on init |
| `generate` | `def` → `str` | Calls `generete_custom_discription_without` | No code context required |

**Logic Flow**  
1. Directly call `generete_custom_discription_without` with `model`, description, and language.  
2. Return the result.

**Visible Interactions**  
- Uses only the post‑processor `generete_custom_discription_without`.  

--- 
<a name="doc-factory"></a>
## `DocFactory` – Orchestrator of Module Pipeline  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `modules` | `list[BaseModule]` | Ordered collection of generation units | Supplied via `*modules` at instantiation |
| `logger` | `BaseLogger` | Centralised log sink | Instantiated internally |
| `generate_doc` | `def` → `str` | Executes each module, aggregates output | Accepts `info`, a `Model`, and a `BaseProgress` tracker |

**Logic Flow**  
1. Initialise progress sub‑task “Generate parts” with length `len(self.modules)`.  
2. Iterate `module` in `self.modules`:  
   a. Call `module.generate(info, model)`.  
   b. Append result plus double newline to `output`.  
   c. Log module completion (`InfoLog`) at default and level 2.  
   d. Advance progress via `progress.update_task()`.  
3. Remove the sub‑task and return the concatenated `output`.

**Visible Interactions**  
- Relies on `BaseModule` subclasses from `autodocgenerator.factory.modules`.  
- Uses `BaseProgress` for UI feedback.  
- Emits logs through `BaseLogger` (`InfoLog`).  

--- 
<a name="gpt-model"></a>  
## `GPTModel` – Synchronous Groq Model Wrapper  

| Entity | Type | Role | Notes |
|-------|------|------|------|
| `api_key` | `str` | API credential | Defaults to `API_KEY` |
| `history` | `History` | Message history | Inherited |
| `use_random` | `bool` | Randomize model order | Default `True` |
| `client` | `Groq` | Groq sync client | Instantiated in `__init__` |
| `logger` | `BaseLogger` | Log sink | Instantiated in `__init__` |
| `with_history` | `bool` | Include history flag | Default `True` |
| `prompt` | `str` | Optional prompt | Used when `with_history=False` |
| `generate_answer` | `def` → `str` | Returns model answer | May raise `ModelExhaustedException` |

**Logic Flow**  
1. Call parent `Model` constructor (stores API key, history, shuffles model list).  
6. In `generate_answer`, pick messages from history or the supplied prompt.  
5. Loop: select `model_name` from `regen_models_name`.  
6. Attempt `client.chat.completions.create(messages=…, model=model_name)`.  
7. On exception, log a warning and move to the next model index.  
9. If the list is exhausted, log an error and raise `ModelExhaustedException`.  
10. Return the first choice’s message content after logging.  

**Visible Interactions**  
- Extends `Model` from *engine/models/model.py*.  
- Uses `Groq` from the `groq` package.  
- Logs through `BaseLogger` with `InfoLog`, `ErrorLog`, `WarningLog`.  
- Raises `ModelExhaustedException` when no model remains. 
<a name="async-gpt-model"></a>  
## `AsyncGPTModel` – Asynchronous Groq Model Wrapper  

| Entity | Type | Role | Notes |
|-------|------|------|------|
| `api_key` | `str` | API credential | Defaults to module‑level `API_KEY` |
| `history` | `History` | Message history store | Initialized with system prompt |
| `use_random` | `bool` | Randomize model order | Default `True` |
| `client` | `AsyncGroq` | Groq async client | Created in `__init__` |
| `logger` | `BaseLogger` | Log sink | Created in `__init__` |
| `with_history` | `bool` | Flag to include history | Default `True` |
| `prompt` | `str` | Optional override prompt | Used when `with_history=False` |
| `generate_answer` | `async def` → `str` | Returns model answer | May raise `ModelExhaustedException` |

**Logic Flow**  
1. Initialise parent `AsyncModel` (stores `api_key`, `history`, shuffles `MODELS_NAME`).  
2. Create an `AsyncGroq` client with the supplied API key.  
3. In `generate_answer`, optionally use the stored history or a single prompt.  
4. Loop until a model succeeds: select the current model from `regen_models_name`.  
5. Call `await client.chat.completions.create(messages=…, model=model_name)`.  
6. On failure, log a warning and advance `current_model_index` (wrap to 0).  
7. If no models remain, log an error and raise `ModelExhaustedException`.  
8. Extract the answer from `chat_completion.choices[0].message.content`.  
9. Log the result at level 2 and return the string.  

**Visible Interactions**  
- Inherits from `AsyncModel` (defined in *engine/models/model.py*).  
- Uses `AsyncGroq` from the `groq` package.  
- Catches generic `Exception`; logs via `BaseLogger` with `InfoLog`, `ErrorLog`, `WarningLog`.  
- Propagates `ModelExhaustedException` from `autodocgenerator.exceptions`.  

--- 
<a name="data-splitting-mechanism"></a>
## Data Splitting Mechanism
The `split_data` function is responsible for dividing a large input string into smaller chunks based on a specified maximum symbol count.

### Function Signature
```python
def split_data(data: str, max_symbols: int) -> list[str]:
```
### Parameters
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `data` | str | Input | The input string to be split. |
| `max_symbols` | int | Input | The maximum number of symbols per chunk. |
| `split_objects` | list[str] | Output | The list of split strings. |

### Technical Logic Flow
1. The function takes in two parameters: `data` and `max_symbols`.
2. It initializes an empty list `split_objects` to store the split strings.
3. The input `data` is split into chunks based on the `max_symbols` limit.

### Visible Interactions
This function interacts with the `ProjectSettings` module indirectly through the import of other modules.

### Specific Component Responsibility
The `split_data` function is responsible for preprocessing the input data by splitting it into manageable chunks, which can then be processed by other components of the Auto Doc Generator system.

### Data Contract
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `data` | str | Input | The input string to be split. |
| `max_symbols` | int | Input | The maximum number of symbols per chunk. |
| `split_objects` | list[str] | Output | The list of split strings. |

Note: The implementation details of the `split_data` function are not fully provided in the given code snippet, so the technical logic flow and data contract are based on the available information.

## 
<a name="split-data-function"></a> Split Data Function
The `split_data` function is responsible for preprocessing the input data by splitting it into manageable chunks.

### 
<a name="write-docs-by-parts-function"></a> Write Docs By Parts Function
The `write_docs_by_parts` function generates documentation for a given part of the code.

### 
<a name="async-write-docs-by-parts-function"></a> Async Write Docs By Parts Function
The `async_write_docs_by_parts` function asynchronously generates documentation for a given part of the code.

### 
<a name="gen-doc-parts-function"></a> Gen Doc Parts Function
The `gen_doc_parts` function generates documentation for the given code by splitting it into parts.

### 
<a name="async-gen-doc-parts-function"></a> Async Gen Doc Parts Function
The `async_gen_doc_parts` function asynchronously generates documentation for the given code by splitting it into parts.

### 
<a name="sorting-module-functionality"></a> Sorting Module Functionality
The sorting module is responsible for ordering the documentation fragments based on their semantic meaning. It takes a dictionary of fragments as input, where each key is a unique identifier (anchor name) and the value is the corresponding fragment text.

### 
<a name="code-mix-module-functionality"></a> Code Mix Module Functionality
The code mix module is responsible for building the repository content by traversing the directory tree and writing the file contents to an output file.

### 
<a name="compressor-module-functionality"></a> Compressor Module Functionality
The compressor module is responsible for compressing input data using a provided model and project settings.

### 
<a name="visible-interactions"></a> Visible Interactions
The logging component interacts with the `BaseLogger` class to log messages. The progress tracking component interacts with the `BaseProgress` class to track progress. The installation scripts interact with the file system to create the necessary files and directories.

## 
<a name="visible-interactions-1"></a> Visible Interactions
The code mix module interacts with the following components:

* **Logger**: The code mix module uses the `BaseLogger` class to log information about the repository structure and file contents.

### 
<a name="visible-interactions-2"></a> Visible Interactions
This function interacts with the `Model` and `ProjectSettings` modules.

### 
<a name="visible-interactions-3"></a> Visible Interactions
This function interacts with the `AsyncModel` and `global_info` modules.

### 
<a name="visible-interactions-4"></a> Visible Interactions
This function interacts with the `Model`, `ProjectSettings`, and `BaseProgress` modules.

### 
<a name="visible-interactions-5"></a> Visible Interactions
This function interacts with the `AsyncModel`, `global_info`, and `BaseProgress` modules.

### 
<a name="technical-logic-flow"></a> Technical Logic Flow
1. The user runs the installation script to create the necessary files and directories.
2. The logging component is used to log messages in the system.
3. The progress tracking component is used to track the progress of tasks in the system.
4. The user can configure the logging and progress tracking components using the `autodocconfig.yml` file.

### 
<a name="technical-logic-flow-1"></a> Technical Logic Flow
The technical logic flow of the code mix module can be described as follows:

1. The `CodeMix` class initializes the root directory and ignore patterns.
2. The `should_ignore` method checks if a file or directory should be ignored based on the ignore patterns.
3. The `build_repo_content` method traverses the directory tree and writes the file contents to an output file.
4. The repository structure and file contents are written to the output file.

### 
<a name="technical-logic-flow-2"></a> Technical Logic Flow
1. The function takes in several parameters: `part`, `model`, `project_settings`, `prev_info`, and `language`.
2. It initializes a prompt for the model, including the language and project settings.
3. The function generates documentation for the given part using the model.

### 
<a name="technical-logic-flow-3"></a> Technical Logic Flow
1. The function takes in several parameters: `part`, `async_model`, `global_info`, `semaphore`, `prev_info`, `language`, and `update_progress`.
2. It initializes a prompt for the model, including the language and global information.
3. The function generates documentation for the given part using the async model.

### 
<a name="technical-logic-flow-4"></a> Technical Logic Flow
1. The function takes in several parameters: `full_code_mix`, `max_symbols`, `model`, `project_settings`, `language`, and `progress_bar`.
2. It splits the input code into parts based on the `max_symbols` limit.
3. The function generates documentation for each part using the `write_docs_by_parts` function.

### 
<a name="technical-logic-flow-5"></a> Technical Logic Flow
1. The function takes in several parameters: `full_code_mix`, `global_info`, `max_symbols`, `model`, `language`, and `progress_bar`.
2. It splits the input code into parts based on the `max_symbols` limit.
3. The function generates documentation for each part using the `async_write_docs_by_parts` function.

### 
<a name="data-contract"></a> Data Contract
The following data contract is available:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `log_message` | str | Input | The log message to be logged. |
| `log_level` | int | Input | The log level of the message. |
| `task_name` | str | Input | The name of the task. |
| `total_length` | int | Input | The total length of the task. |
| `progress` | int | Output | The progress of the task. |

### 
<a name="data-contract-1"></a> Data Contract
The data contract of the code mix module can be described in the following table:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `root_dir` | str | Input | The root directory of the repository. |
| `ignore_patterns` | list[str] | Input | A list of patterns to ignore when traversing the directory tree. |
| `output_file` | str | Output | The file path where the repository content will be written. |

### 
<a name="data-contract-2"></a> Data Contract
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `part` | str | Input | The part of the code to generate documentation for. |
| `model` | Model | Input | The model used to generate documentation. |
| `project_settings` | ProjectSettings | Input | The project settings used to generate documentation. |
| `prev_info` | str | Input | The previous documentation generated. |
| `language` | str | Input | The language used to generate documentation. |
| `answer` | str | Output | The generated documentation. |

## 
<a name="data-contract-3"></a> Data Contract
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `part` | str | Input | The part of the code to generate documentation for. |
| `async_model` | AsyncModel | Input | The async model used to generate documentation. |
| `global_info` | str | Input | The global information used to generate documentation. |
| `semaphore` | Semaphore | Input | The semaphore used to control the async process. |
| `prev_info` | str | Input | The previous documentation generated. |
| `language` | str | Input | The language used to generate documentation. |
| `update_progress` | Function | Input | The function used to update the progress. |
| `answer` | str | Output | The generated documentation. |

## 
<a name="data-contract-4"></a> Data Contract
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `full_code_mix` | str | Input | The input code to generate documentation for. |
| `max_symbols` | int | Input | The maximum number of symbols per chunk. |
| `model` | Model | Input | The model used to generate documentation. |
| `project_settings` | ProjectSettings | Input | The project settings used to generate documentation. |
| `language` | str | Input | The language used to generate documentation. |
| `progress_bar` | BaseProgress | Input | The progress bar used to track the progress. |
| `result` | str | Output | The generated documentation. |

## 
<a name="data-contract-5"></a> Data Contract
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `full_code_mix` | str | Input | The input code to generate documentation for. |
| `global_info` | str | Input | The global information used to generate documentation. |
| `max_symbols` | int | Input | The maximum number of symbols per chunk. |
| `model` | AsyncModel | Input | The async model used to generate documentation. |
| `language` | str | Input | The language used to generate documentation. |
| `progress_bar` | BaseProgress | Input | The progress bar used to track the progress. |
| `result` | str | Output | The generated documentation. |


