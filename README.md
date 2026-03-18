**Auto Doc Generator Project Overview**
======================================

### **Project Title**
Auto Doc Generator

### **Project Goal**
The Auto Doc Generator is a software tool designed to help developers automatically generate documentation for their projects. The primary objective is to reduce the time and effort required to create and maintain project documentation, increasing productivity and improving overall project quality.

### **Core Logic & Principles**
The Auto Doc Generator operates on a layered plugin-factory pipeline architecture. The process begins with configuration, where settings are loaded from a YAML file, and structure settings are defined. The preprocessor then splits the raw repository code into chunks, which are compressed and prepared for processing. The LLM (Large Language Model) wrapper interacts with the model, utilizing the API key and regenerating models as needed. The factory generates documentation parts, which are then post-processed, sorted, and ordered. Finally, the manager orchestrates the entire process, saving the final README.md file or cache.

The system uses a combination of natural language processing (NLP) and machine learning algorithms to generate high-quality documentation. The LLM wrapper plays a crucial role in this process, as it enables the system to leverage the power of large language models to generate human-like text.

### **Key Features**

* Automatic generation of project documentation
* Support for multiple programming languages
* Customizable configuration and settings
* Integration with large language models (LLMs) for high-quality text generation
* Plugin-factory architecture for easy extension and customization
* Post-processing and sorting of generated documentation

### **Dependencies**
The Auto Doc Generator depends on the following libraries and tools:

* YAML library for configuration file parsing
* LLM library (e.g., OpenAI, Groq) for text generation
* Plugin-factory library for framework implementation
* Logging library (e.g., Pydantic) for logging and error handling
* Progress UI library (e.g., ConsoleGtiHubProgress) for console/CI feedback

Note: The specific dependencies may vary depending on the implementation and the chosen LLM backend.
## Executive Navigation Tree
* 📂 Core Engine
  * [Structure Settings](#structure-settings)
  * [Read Config](#read-config)
  * [Project Build Config](#project-build-config)
  * [Config Class](#config-class)
  * [Project Settings](#project-settings)
  * [AutoDoc Config Structure and Options](#autodocconfig-structure-and-options)
  * [Gen Doc Function](#gen-doc-function)
  * [DocFactory](#docfactory)
  * [Spliter Function](#spliter-function)
  * [HTML Link Extraction](#html-link-extraction)
  * [Link Intro Generation](#link-intro-generation)
* ⚙️ Content Management
  * [Global Introduction](#global-introduction)
  * [Custom Description](#custom-description)
  * [Content Description](#CONTENT_DESCRIPTION)
  * [Anchor Sorting](#anchor-sorting)
  * [Repo Content Packer](#repo-content-packer)
  * [Compressor Pipeline](#compressor-pipeline)
* 📈 Model Management
  * [Intro Modules](#intro-modules)
  * [Base Module](#basemodule)
  * [Custom Module](#custommodule)
  * [Manager](#manager)
  * [Manager Class Usage](#manager-class-usage)
  * [History](#history)
  * [GPT Model](#gptmodel)
  * [Model Base](#modelbase)
  * [Async GPT Model](#asyncgptmodel)
  * [Model Exhausted Exception](#model-exhausted-exception)
* 📦 Setup and Installation
  * [Install Workflow Setup](#install-workflow-setup)
<a name="structure-settings"></a>
## StructureSettings – Runtime Documentation Controls  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `include_intro_links` | bool | Toggle inclusion of link section | Default **True** |
| `include_order` | bool | Enable ordered sections generation | Default **True** |
| `use_global_file` | bool | Pull global project info into each part | Default **True** |
| `max_doc_part_size` | int | Max symbols per LLM chunk | Default **5 000** |
| `include_intro_text` | bool | Add textual introduction block | Default **True** |
| `load_settings` | method(dict) | Mutates attributes from YAML dict | Overwrites any defaults |

> **Assumption**: No validation is performed; keys must match attribute names exactly.

---
<a name="read-config"></a>
## read_config – YAML‑Driven Construction Pipeline  

**Purpose** – Parses a raw YAML string, builds the three core runtime objects, and returns them as a tuple.

### Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_data` | `str` | Raw YAML content | Must be UTF‑8 |
| Return `(Config, list[BaseModule], StructureSettings)` | tuple | Central configuration, custom module list, runtime flags | All objects are newly instantiated |

### Logic Flow  

1. `yaml.safe_load` → `data` dict.  
2. Instantiate `Config()` → `config`.  
3. Extract `ignore_files`, `language`, `project_name`, `project_additional_info`.  
4. Build `ProjectBuildConfig()` → `pcs`; `pcs.load_settings(project_settings)`.  
5. Chain setters on `config`: `set_language`, `set_project_name`, `set_pcs`.  
6. Populate `config.ignore_files` & `project_additional_info` via loops.  
7. Build `custom_modules` list:  
   - If description starts with “%” → `CustomModuleWithOutContext(desc[1:])`  
   - Else → `CustomModule(desc)`.  
8. Load `structure_settings` dict into `StructureSettings()` via `load_settings`.  
9. Return the assembled tuple.

### Visible Interactions  

- Imports `CustomModule*` from `factory.modules.general_modules`.  
- Relies on `Config` and `ProjectBuildConfig` from `..config.config`.  

---
<a name="project-build-config"></a>
## ProjectBuildConfig – Build‑Time Flags Container  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `save_logs` | bool | Persist log files | Default **False** |
| `log_level` | int | Verbosity selector | Default **-1** |
| `load_settings` | method(dict) | Apply arbitrary key/value pairs | Direct `setattr` without validation |

---
<a name="config-class"></a>
## Config – Global Project Settings Object  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `ignore_files` | `list[str]` | File‑pattern exclusion list | Pre‑populated with common artefacts |
| `language` | `str` | Documentation language | Default **“en”** |
| `project_name` | `str` | Identifier for output | Empty until set |
| `project_additional_info` | `dict` | Arbitrary key/value metadata | Populated by `add_project_additional_info` |
| `pbc` | `ProjectBuildConfig` | Build‑time flags | Instantiated in `__init__` |
| Setter methods (`set_language`, `set_pcs`, `set_project_name`) | fluent | Enable chaining | Return `self` |
| `add_project_additional_info`, `add_ignore_file` | mutators | Extend internal collections | Return `self` |
| `get_project_settings` | method → `ProjectSettings` | Convert stored metadata into a `ProjectSettings` instance | Calls `ProjectSettings(self.project_name)` then populates via `add_info` |

> **Note**: No I/O occurs; all state remains in‑memory.

---
<a name="project-settings"></a>
## `settings.py` – Project Settings Builder  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `ProjectSettings` | `class` | Holds per‑project metadata used in prompts. | `prompt` property concatenates `BASE_SETTINGS_PROMPT`, the project name, and any key/value pairs added via `add_info`. |

**Logic Flow**  
1. `__init__` stores `project_name` and an empty dict `info`.  
2. `add_info(key, value)` inserts arbitrary metadata.  
3. `prompt` (property) builds a string:  
   - Starts with constant `BASE_SETTINGS_PROMPT`.  
   - Appends “Project Name: …”.  
   - Iterates over `self.info` and adds “`key: value`”.
<a name="autodocconfig-structure-and-options"></a>
The autodocconfig.yml file has several available options. 
The main sections are: 
- project_name: used to specify the name of the project, for example "Auto Doc Generator".
- language: used to specify the language of the project, for example "en".
- ignore_files: a list of files and directories to be ignored, such as python bytecode, cache, environments, databases, logs, version control, and miscellaneous files.
- build_settings: contains two options: 
  - save_logs: a boolean value to specify whether to save logs or not, by default it is set to false.
  - log_level: an integer value to specify the log level, for example 2.
- structure_settings: contains several options: 
  - include_intro_links: a boolean value to specify whether to include intro links or not, by default it is set to true.
  - include_intro_text: a boolean value to specify whether to include intro text or not, by default it is set to true.
  - include_order: a boolean value to specify whether to include order or not, by default it is set to true.
  - use_global_file: a boolean value to specify whether to use a global file or not, by default it is set to true.
  - max_doc_part_size: an integer value to specify the maximum size of a document part, for example 5000.
- project_additional_info: contains additional information about the project, such as a global idea.
- custom_descriptions: a list of custom descriptions, for example how to install workflow, how to write autodocconfig.yml file, and how to use Manager class.
<a name="gen-doc-function"></a>
## gen_doc – End‑to‑End Documentation Generation Routine  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_path` | `str` | Root directory of source code | Passed to `Manager` |
| `config` | `Config` | Global configuration object | Produced by `read_config` |
| `custom_modules` | `list[BaseModule]` | User‑defined documentation fragments | Injected into `DocFactory` |
| `structure_settings` | `StructureSettings` | Runtime flags controlling pipeline steps | Drives conditional calls |
| Return | `str` | Fully assembled markdown document | Obtained via `manager.doc_info.doc.get_full_doc()` |

### Step‑by‑Step Execution  

1. Instantiate `GPTModel(API_KEY, use_random=False)` → `sync_model`.  
2. Build `Manager(project_path, config=config, llm_model=sync_model, progress_bar=ConsoleGtiHubProgress())`.  
3. `manager.generate_code_file()` – extracts source files.  
4. *(Optional global info generation is commented out.)*  
5. `manager.generete_doc_parts(max_symbols=structure_settings.max_doc_part_size, with_global_file=structure_settings.use_global_file)`.  
6. `manager.factory_generate_doc(DocFactory(*custom_modules))` – merges custom parts.  
7. If `structure_settings.include_order`: `manager.order_doc()`.  
8. Assemble optional intro modules based on flags, then `manager.factory_generate_doc(..., to_start=True)`.  
9. `manager.clear_cache()` – removes temporary artefacts.  
10. `manager.save()` – writes final markdown to configured target.  
11. Return the full document string.

### Inter‑Component Calls  

- Uses `ConsoleGtiHubProgress` for UI feedback.  
- Leverages `DocFactory` to wrap `custom_modules` and intro modules.  
- Relies on `Manager`’s public API; internal details are abstracted.

---
<a name="docfactory"></a>
## `DocFactory` – Orchestrates Module Execution and Fragment Assembly  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `modules` | `list[BaseModule]` | Ordered collection of plug‑ins to run | Supplied via `*modules` ctor argument |
| `with_splited` | `bool` | Controls post‑processing of each fragment | When `True`, `split_text_by_anchors` is applied |
| `logger` | `BaseLogger` | Central logging facility | Emits `InfoLog` entries |
| `progress` | `BaseProgress` | UI progress tracker passed to `generate_doc` | Creates sub‑task “Generate parts” |
| `generate_doc` | `method` | Returns `DocHeadSchema` containing all assembled parts | Iterates modules, logs, updates progress |

**Logic Flow**  
1. Initialise `DocHeadSchema`.  
2. `progress.create_new_subtask("Generate parts", len(modules))`.  
3. For each `module`:  
   - Call `module.generate(info, model) → str`.  
   - If `with_splited`, split result by anchors → dict; add each piece via `doc_head.add_parts(key, DocContent(content=piece))`.  
   - Else, add whole result under `task_name`.  
   - Log success and raw output (`level=2`).  
   - `progress.update_task()`.  
4. After loop, `progress.remove_subtask()` and return `doc_head`.
<a name="spliter-function"></a>
## `spliter.py` – Repository Chunk Splitter  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `split_data` | `def(data: str, max_symbols: int) → list[str]` | Breaks a large markdown string into size‑limited pieces for LLM consumption. | Splits on the sentinel `

## Auto Doc Generator – Technical Documentation
### Overview of the System

The Auto Doc Generator is a system designed to help developers automatically generate documentation for their projects. It utilizes a layered plugin-factory pipeline to process code, generate documentation, and provide a final output in Markdown format.

### Architecture

The system consists of several components:

* **Config**: Handles configuration settings, including YAML files, structure settings, and custom base modules.
* **Preprocessor**: Responsible for processing code, including splitting, compressing, and preparing it for the LLM wrapper.
* **LLM Wrapper**: Interfaces with the language model, handling tasks such as getting answers without history.
* **Factory**: Generates documentation parts, including intro links, intro text, and custom modules.
* **Post-processor**: Handles tasks such as sorting, anchor splitting, and ordering.
* **Manager**: Orchestrates all steps, including saving the final README.md file and caching.

### Key Entry Points

* `run_file.__main__`: The main entry point for the system, which can be triggered via CLI or GitHub Action.
* `Manager.generate_*` methods: These methods are used to generate documentation for code files, global information, doc parts, factory generation, and ordering.

### Terminal Points

* Cache files (`.auto_doc_cache/*`): The system caches generated documentation to improve performance.
* Final Markdown output (`README.md` or configured target): The final output of the system is a Markdown file containing the generated documentation.

### Shared State & Key Context

* **`BaseLogger`**: A singleton logger that can be accessed anywhere in the system.
* **`progress`**: An instance of `BaseProgress` subclass that tracks sub-task count.
* **`model`**: An opaque LLM client that only requires the `get_answer_without_history` method.
* **`ProjectSettings.prompt`**: A static system message injected into every LLM call.
* **`prev_fragment`**: The last ~3k characters of the previous output, kept to preserve continuity.
* **`global_info`**: Optional cross-file context added to the system prompt when supplied.

### Functional Flow

The system's functional flow can be broken down into the following steps:

1. **Data Splitting**: The system splits the input code into size-limited pieces for LLM consumption.
2. **Documentation Generation**: The system generates documentation for each piece using the LLM wrapper.
3. **Post-processing**: The system sorts, splits, and orders the generated documentation.
4. **Output**: The final output is a Markdown file containing the generated documentation.

### Technical Logic Flow

The technical logic flow of the system can be broken down into the following steps:

1. `gen_doc_parts` calls `split_data` to split the input code into pieces.
2. `gen_doc_parts` iterates over each piece and calls `write_docs_by_parts` to generate documentation.
3. `write_docs_by_parts` assembles a prompt and calls the LLM wrapper to get an answer.
4. `write_docs_by_parts` processes the answer and returns the generated documentation.
5. `gen_doc_parts` combines the generated documentation and returns the final output.

### Data Contract

The data contract of the system can be summarized in the following table:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `data` | `str` | Input code | Split into pieces for LLM consumption |
| `max_symbols` | `int` | Configuration | Determines the size of each piece |
| `model` | `Model` | LLM client | Interfaces with the language model |
| `project_settings` | `ProjectSettings` | Configuration | Holds per-project metadata |
| `language` | `str` | Configuration | Determines the language used for documentation |
| `global_info` | `str` | Optional context | Added to the system prompt when supplied |

### Component Responsibilities

* **`gen_doc_parts`**: Coordinates the splitting of input code, generation of documentation, and combination of output.
* **`split_data`**: Splits the input code into size-limited pieces for LLM consumption.
* **`write_docs_by_parts`**: Generates documentation for each piece using the LLM wrapper.
* **`Model`**: Interfaces with the language model, handling tasks such as getting answers without history.
* **`ProjectSettings`**: Holds per-project metadata used in prompts.

### Visible Interactions

The system interacts with the following external components:

* **Language Model**: The system uses the language model to generate documentation.
* **Configuration Files**: The system reads configuration files to determine settings such as the size of each piece.
* **Input Code**: The system takes input code as input and generates documentation for it.

### Critical Constraints

* **No generic headers**: The system does not use generic headers such as "Overview" or "Introduction".
* **Specific functionality**: The system uses headers that describe specific functionality, such as "Documentation Generation" or "LLM Wrapper".

## Documentation for Code Fragments

### Component Overview

The code fragments provided are part of the **Auto Doc Generator** project, which aims to help developers generate documentation for their projects. The fragments are divided into three main sections:

1. **Logging**: This section includes classes for logging purposes, such as `BaseLog`, `ErrorLog`, `WarningLog`, and `InfoLog`. These classes are used to format log messages with timestamps and log levels.
2. **Progress Tracking**: This section includes classes for tracking progress, such as `BaseProgress`, `LibProgress`, and `ConsoleGtiHubProgress`. These classes are used to display progress bars and update task status.
3. **Installation Script**: This section includes an installation script written in PowerShell, which creates a directory for workflows, generates a workflow file, and creates a configuration file for the **Auto Doc Generator** project.

### Technical Logic Flow

The technical logic flow of the code fragments can be broken down as follows:

1. **Logging**:
  * The `BaseLog` class is initialized with a message and a log level.
  * The `format` method is used to format the log message with a timestamp and log level.
  * The `ErrorLog`, `WarningLog`, and `InfoLog` classes inherit from `BaseLog` and override the `format` method to include specific log levels.
2. **Progress Tracking**:
  * The `BaseProgress` class is initialized with no arguments.
  * The `create_new_subtask` method is used to create a new subtask.
  * The `update_task` method is used to update the task status.
  * The `remove_subtask` method is used to remove a subtask.
  * The `LibProgress` and `ConsoleGtiHubProgress` classes inherit from `BaseProgress` and implement the progress tracking logic.
3. **Installation Script**:
  * The script creates a directory for workflows if it does not exist.
  * The script generates a workflow file using a here-string.
  * The script creates a configuration file for the **Auto Doc Generator** project.

### Data Contract

The data contract of the code fragments can be summarized as follows:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `log_message` | `str` | Log message | The message to be logged. |
| `log_level` | `int` | Log level | The level of the log message (e.g., error, warning, info). |
| `task_name` | `str` | Task name | The name of the task being tracked. |
| `total_len` | `int` | Total length | The total length of the task. |
| `current_len` | `int` | Current length | The current length of the task. |
| `percent` | `float` | Percentage | The percentage completion of the task. |

### Component Responsibilities

* **Logging**: The logging classes are responsible for formatting log messages with timestamps and log levels.
* **Progress Tracking**: The progress tracking classes are responsible for displaying progress bars and updating task status.
* **Installation Script**: The installation script is responsible for creating a directory for workflows, generating a workflow file, and creating a configuration file for the **Auto Doc Generator** project.

### Visible Interactions

The code fragments interact with the following external components:

* **File System**: The installation script interacts with the file system to create directories and files.
* **Workflow Engine**: The workflow file generated by the installation script interacts with a workflow engine to execute the workflow.
* **Configuration File**: The configuration file generated by the installation script interacts with the **Auto Doc Generator** project to provide configuration settings.

### Critical Constraints

* **No Generic Headers**: The logging classes do not use generic headers such as "Overview" or "Introduction".
* **Specific Functionality**: The logging classes use headers that describe specific functionality, such as "Error Log" or "Info Log".
* **Progress Tracking**: The progress tracking classes use specific methods to create and update tasks, such as `create_new_subtask` and `update_task`.

## Architecture: **Auto Doc Generator** – Layered + Task-pipeline
### Project Structure

The **Auto Doc Generator** project is structured as a layered task-pipeline. The pipeline consists of several layers, each with its own responsibility:

1. **Config Layer**: Responsible for loading and storing configuration settings.
2. **Preprocessor Layer**: Responsible for preprocessing the input code.
3. **LLM Wrapper Layer**: Responsible for interacting with the Large Language Model (LLM).
4. **Factory Layer**: Responsible for generating documentation parts.
5. **Post-processor Layer**: Responsible for post-processing the generated documentation.
6. **Manager Layer**: Responsible for orchestrating the entire pipeline.

### Component Responsibilities

* **Config**: Responsible for loading and storing configuration settings.
* **Preprocessor**: Responsible for preprocessing the input code.
* **LLM Wrapper**: Responsible for interacting with the LLM.
* **Factory**: Responsible for generating documentation parts.
* **Post-processor**: Responsible for post-processing the generated documentation.
* **Manager**: Responsible for orchestrating the entire pipeline.

### Visible Interactions

The **Auto Doc Generator** project interacts with the following external components:

* **File System**: The project reads and writes files to the file system.
* **LLM**: The project interacts with the LLM to generate documentation.
* **Configuration File**: The project reads configuration settings from a file.

### Technical Logic Flow

The technical logic flow of the **Auto Doc Generator** project is as follows:

1. The **Manager** layer orchestrates the pipeline.
2. The **Config** layer loads configuration settings.
3. The **Preprocessor** layer preprocesses the input code.
4. The **LLM Wrapper** layer interacts with the LLM to generate documentation parts.
5. The **Factory** layer generates documentation parts.
6. The **Post-processor** layer post-processes the generated documentation.
7. The **Manager** layer saves the final documentation.

### Data Contract

The data contract of the **Auto Doc Generator** project is as follows:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `config` | `dict` | Configuration settings | Loaded from configuration file. |
| `input_code` | `str` | Input code | Preprocessed by the preprocessor layer. |
| `llm_output` | `str` | LLM output | Generated by the LLM wrapper layer. |
| `documentation_parts` | `list` | Documentation parts | Generated by the factory layer. |
| `final_documentation` | `str` | Final documentation | Saved by the manager layer. |

### Shared State & Key Context

The shared state and key context of the **Auto Doc Generator** project are as follows:

* **Config**: Configuration settings loaded from file.
* **Input Code**: Input code preprocessed by the preprocessor layer.
* **LLM Output**: LLM output generated by the LLM wrapper layer.
* **Documentation Parts**: Documentation parts generated by the factory layer.
* **Final Documentation**: Final documentation saved by the manager layer.

### Quick Edit Reference

The quick edit reference for the **Auto Doc Generator** project is as follows:

| Aspect | Location | Effect |
| --- | --- | --- |
| Config settings | `autodocconfig.yml` | Changes configuration settings. |
| Input code | `input_code` | Changes input code. |
| LLM output | `llm_output` | Changes LLM output. |
| Documentation parts | `documentation_parts` | Changes documentation parts. |
| Final documentation | `final_documentation` | Changes final documentation. |

### Installation Script

The installation script for the **Auto Doc Generator** project is as follows:

```bash
#!/bin/bash

# Create directory for workflows if it doesn't exist
mkdir -p .github/workflows

# Create workflow file
cat <<EOF > .github/workflows/autodoc.yml
name: AutoDoc
on: [workflow_dispatch]
jobs:
  run:
    permissions:
      contents: write
    uses: Drag-GameStudio/ADG/.github/workflows/reuseble_agd.yml@main
    secrets:
      GROCK_API_KEY: \${{ secrets.GROCK_API_KEY }}
EOF

# Create configuration file
cat <<EOF > autodocconfig.yml
project_name: "$(basename "$PWD")"
language: "en"

# ... other configuration settings ...
EOF
```

### pyproject.toml

The `pyproject.toml` file for the **Auto Doc Generator** project is as follows:

```toml
[project]
name = "autodocgenerator"
version = "0.9.3.1"
description = "This Project helps you to create docs for your projects"
authors = [
    {name = "dima-on", email = "sinica911@gmail.com"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11,<4.0"

dependencies = [
    # ... dependencies ...
]

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"
```
<a name="html-link-extraction"></a>
## HTML Link Extraction (`get_all_html_links`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Input markdown/HTML source | Expected to contain `<a name="…"></a>` anchors |
| `links` | `list[str]` | Output collection | Each entry prefixed with “#” |
| `logger` | `BaseLogger` | Logging side‑effect | Emits two `InfoLog` messages |
| `pattern` | `str` | Regex pattern | `r'<a name=["\']?(.*?)["\']?></a>'` |

**Logic Flow**  
1. Instantiate `BaseLogger`.  
2. Compile regex and iterate over all matches in `data`.  
3. For each match, extract the anchor name; if its length > 5, prepend “#” and append to `links`.  
4. Log count and list, then return `links`.

---
<a name="link-intro-generation"></a>
## Link‑Based Introduction Generation (`get_links_intro`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `links` | `list[str]` | Input anchor list | Produced by `get_all_html_links` |
| `model` | `Model` (LLM wrapper) | Generates text | Only `get_answer_without_history` is used |
| `language` | `str` | System‑language hint | Default “en” |
| `prompt` | `list[dict]` | LLM request payload | Contains two system messages and one user message |
| `intro_links` | `str` | LLM output | Raw response from the model |

**Logic Flow**  
1. Log start via `BaseLogger`.  
2. Build `prompt`:
   - System message sets language.  
   - System message injects `BASE_INTRODACTION_CREATE_LINKS`.  
   - User message supplies the stringified `links`.  
3. Call `model.get_answer_without_history(prompt=prompt)`.  
4. Log completion and raw result, then return it.

**Interaction** – Relies on `BASE_INTRODACTION_CREATE_LINKS` from `engine.config.config` and the LLM client.

---
<a name="global-introduction"></a>
## Global Introduction Generation (`get_introdaction`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `global_data` | `str` | Input aggregated documentation | Typically the compressed global info |
| `model` | `Model` | LLM client | Same method as above |
| `language` | `str` | Language hint | Default “en” |
| `prompt` | `list[dict]` | LLM payload | Uses `BASE_INTRO_CREATE` system message |
| `intro` | `str` | Output | Direct LLM answer |

**Logic Flow**  
1. Assemble a three‑message `prompt` (language system, intro system, user with `global_data`).  
2. Invoke `model.get_answer_without_history`.  
3. Return the raw `intro`.

---
<a name="custom-description"></a>
## Custom Description Generation (`generete_custom_discription` & `generete_custom_discription_without`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `splited_data` | `str` (iterable) | Chunked source pieces | Used only in the first variant |
| `custom_description` | `str` | Task description for LLM | Same for both variants |
| `model` | `Model` | LLM client | Calls `get_answer_without_history` |
| `language` | `str` | Language hint | Default “en” |
| `result` / `intro` | `str` | LLM response | May be empty if “!noinfo” appears |

**`generete_custom_discription`**  
- Loops over `splited_data`, building a detailed system prompt that includes the chunk (`sp_data`) and `BASE_CUSTOM_DISCRIPTIONS`.  
- Calls the model; if the result contains “!noinfo” or “No information found” early, the loop continues; otherwise it breaks and returns the first satisfactory `result`.

**`generete_custom_discription_without`**  
- Constructs a single prompt with strict formatting rules (single `
<a name="CONTENT_DESCRIPTION"></a>` tag, no filenames, extensions, URLs, etc.).  
- Sends to the model and returns the raw answer.

**Side Effects** – Both functions log via `BaseLogger` (only the first logs implicitly through the model’s internal logger). No filesystem I/O occurs.
<a name="anchor-sorting"></a>
## Anchor‑Based Chunk Extraction & Ordering (`extract_links_from_start`, `split_text_by_anchors`, `get_order`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `chunks` / `text` | `list[str]` / `str` | Input raw markdown sections | Expected to contain HTML‑style anchors (`<a name="…"></a>`) |
| `links` | `list[str]` | Collected anchor IDs (prefixed with `#`) | Only anchors whose name length > 5 are kept |
| `result_chanks` | `list[str]` | Sanitized text pieces split on anchors | Stripped of surrounding whitespace |
| `chanks` | `dict[str, str]` | Mapping **anchor → chunk** | Keys are `#anchor_name` |
| `model` | `Model` | LLM wrapper used in `get_order` | Only `get_answer_without_history` is called |
| `logger` | `BaseLogger` | Logging facility | Emits `InfoLog` messages at various verbosity levels |
| `prompt` | `list[dict]` | Payload for the LLM | Single *user* message requesting a semantic sort |
| `new_result` | `list[str]` | Ordered list of anchors returned by the model | Produced by splitting the comma‑separated response |

**Functional Role**  
These utilities prepare the generated markdown for final assembly: they **detect** top‑level anchors, **segment** the document into anchor‑scoped chunks, and **ask** an LLM to return a semantically‑sorted ordering of those anchors.

**Visible Inter‑Component Interactions**  
- `split_text_by_anchors` calls `extract_links_from_start` to validate that each chunk begins with a proper anchor.  
- `get_order` receives the `chanks` dict, logs its content, builds a prompt, and forwards it to the shared `Model` instance.  
- No filesystem I/O occurs; all data flows in‑memory.

**Logic Flow**  
1. **`extract_links_from_start`** iterates over supplied `chunks`, matches `^<a name=["']?(.*?)["']?</a>`; if the captured name length > 5, `"#"+name` is appended to `links`.  
2. **`split_text_by_anchors`** splits `text` on a look‑ahead regex that locates any valid anchor (`(?=<a name=["']?[^"\'>\s]{6,200}["']?</a>)`).  
   - Trims empty pieces, builds `result_chanks`.  
   - Calls `extract_links_from_start`; raises `Exception("Somthing with anchors")` if counts differ.  
   - Constructs `result` dict mapping each anchor to its corresponding chunk.  
3. **`get_order`** logs start, chunk names, and full dict.  
   - Constructs `prompt` with a single user message: *“Sort the following titles …”* and injects the list of anchor keys.  
   - Calls `model.get_answer_without_history(prompt)`.  
   - Splits the comma‑separated answer, strips whitespace, logs the ordered list, and returns it.

> **Assumption** – The LLM is expected to keep the leading `#` in each title and return a plain CSV list; any deviation will propagate as‑is.

---
<a name="repo-content-packer"></a>
## Repository Content Packing (`CodeMix`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `root_dir` | `str` / `Path` | Base directory of the repository | Resolved to an absolute path at init |
| `ignore_patterns` | `list[str]` | Glob patterns for files/folders to skip | Supplied by caller or defaults to `[]` |
| `logger` | `BaseLogger` | Central logging instance | Emits `InfoLog` for each ignored path |
| `path` (in loops) | `Path` | Traversed filesystem entry | Obtained via `root_dir.rglob("*")` |
| `relative_path` | `Path` | Path relative to `root_dir` | Used for display and `<file>` tags |
| `content` | `list[str]` | Accumulator for the final markdown payload | Joined with newline separators |

**Functional Role**  
`CodeMix` **captures** the structural layout and raw source of a repository, producing a single markdown‑formatted string that downstream components (pre‑processor → LLM) can ingest.

**Visible Inter‑Component Interactions**  
- Relies on `BaseLogger` for visibility of ignored entries.  
- No external services; all operations are local filesystem reads.

**Logic Flow**  
1. **Initialization** stores `root_dir` (resolved) and `ignore_patterns`; creates a `BaseLogger`.  
2. **`should_ignore`** converts a `Path` to a relative string, then checks the path against each glob pattern via `fnmatch`. Returns `True` if any pattern matches the full path, its basename, or any path part.  
3. **`build_repo_content`**  
   - Starts `content` with “Repository Structure:”.  
   - First pass: walks the tree, logs ignored entries, and appends an indented line for each directory/file (`name/` for dirs).  
   - Inserts a visual separator (`"\n" + "="*20 + "\n"`).  
   - Second pass: for each non‑ignored file, adds `<file path="relative_path">`, reads its text (`read_text` with UTF‑8, ignoring errors), appends the raw content, and adds a newline marker (`"\n"`). Exceptions during reading are captured as inline error messages.  
   - Returns the concatenated string via `"\n".join(content)`.

> **Side Effect** – The method produces a large in‑memory string; callers should manage memory for very large repositories.

These two modules constitute the final pre‑LLM preparation stage before the **Global Introduction Generation** step (`get_introdaction`).
<a name="compressor-pipeline"></a>
## `compressor.py` – Data Compression Pipeline  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `compress` | `def(data: str, project_settings: ProjectSettings, model: Model, compress_power: int) → str` | Sends a single chunk to the LLM for size reduction. | Builds a three‑message prompt (`system` with project prompt, `system` with compression instruction, `user` with raw data). |
| `compress_and_compare` | `def(data: list[str], model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) → list[str]` | Groups *compress_power* chunks, compresses each group, and tracks progress. | Returns a list whose length ≈ `ceil(len(data)/compress_power)`. |
| `compress_to_one` | `def(data: list[str], model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) → str` | Iteratively reduces the list until a single compressed document remains. | Uses `compress_and_compare` in a loop; `count_of_iter` records iteration count. |

**Logic Flow**  
1. `compress` assembles `prompt` (system + system + user) and calls `model.get_answer_without_history`.  
2. `compress_and_compare` creates a sub‑task (`progress_bar.create_new_subtask`) sized to `len(data)`. For each element `el` it:  
   - Determines bucket `curr_index = i // compress_power`.  
   - Appends the compressed result + newline to that bucket.  
   - Updates progress (`progress_bar.update_task`).  
3. After the loop the sub‑task is removed; the bucket list is returned.  
4. `compress_to_one` repeatedly calls `compress_and_compare` with an adjusted `compress_power` (fallback = 2 when remaining items are few) until only one element remains, then returns it.  

> **Assumption** – `model.get_answer_without_history` returns plain text; no validation is performed here.
<a name="intro-modules"></a>
## `IntroLinks` & `IntroText` – Automatic Introduction Builders  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `IntroLinks.generate` | `method` | Extracts HTML links via `get_all_html_links` and formats them with `get_links_intro` | Uses `info["full_data"]` and language |
| `IntroText.generate` | `method` | Produces a textual intro from `info["global_info"]` via `get_introdaction` | Passes `model` and language |

**Interactions**  
- Both depend on `Model` for LLM‑driven phrasing.  
- No file‑system or network calls beyond the imported helper utilities.
<a name="basemodule"></a>
## `BaseModule` – Abstract Blueprint for Documentation Generators  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseModule` | `ABC` | Base class for all plug‑in modules that produce a doc fragment | Defines abstract `generate(info: dict, model: Model)` |
| `generate` | `method` | Must return a **str** containing the module’s raw markdown output | Called by `DocFactory` |

> **Assumption** – Concrete modules implement their own logic; `BaseModule` itself never produces output.
<a name="custommodule"></a>
## `CustomModule` & `CustomModuleWithOutContext` – User‑Defined Description Generators  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `discription` | `str` | Prompt text supplied by developer | Stored on init |
| `generate` | `method` | Calls `generete_custom_discription` (or `*_without`) with split code and language | Returns raw markdown fragment |

**Visible Interactions**  
- Imports `split_data` to chunk `info["code_mix"]`.  
- Calls `generete_custom_discription` / `generete_custom_discription_without` from `postprocessor.custom_intro`.  
- Relies on `Model` only for LLM invocation inside those helpers.
<a name="manager"></a>
## `Manager` – Coordination Hub for the Documentation Pipeline  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `CACHE_FOLDER_NAME` | `str` | Fixed sub‑directory for temporary artefacts | “`.auto_doc_cache`” |
| `FILE_NAMES` | `dict[str,str]` | Mapping of logical file keys to cache filenames | `code_mix`, `global_info`, `logs`, `output_doc` |
| `doc_info` | `DocInfoSchema` | Holds mutable documentation state (code mix, global info, `DocHeadSchema`) | Instantiated in `__init__` |
| `config` | `Config` | Global configuration object supplied by caller | Provides language, ignore list, logging level |
| `llm_model` | `Model` | LLM client used for all generation steps | Only `get_answer_without_history` is required |
| `progress_bar` | `BaseProgress` | UI progress tracker (default `BaseProgress()`) | Sub‑tasks created/removed per method |
| `logger` | `BaseLogger` | Central logger writing to `report.txt` | Configured with `FileLoggerTemplate` |
| `generate_code_file` | `method` | Produces a **code‑mix** string via `CodeMix.build_repo_content()` and stores it in `doc_info.code_mix` | Updates progress after completion |
| `generate_global_info` | `method` | Splits the code‑mix, compresses it to a single markdown block using `compress_to_one`, writes to cache, and updates `doc_info.global_info` | Takes `compress_power` & `max_symbols` parameters |
| `generete_doc_parts` | `method` | Drives the *part‑wise* LLM documentation flow (`gen_doc_parts`), splits final output by anchors, populates `doc_info.doc` with `DocContent` fragments | Persists raw result to `output_doc` |
| `factory_generate_doc` | `method` | Invokes a supplied `DocFactory` with assembled `info` dict, merges its `DocHeadSchema` result with existing doc parts, logs the operation | `to_start` flag controls prepend vs. append |
| `order_doc` | `method` | Requests ordering of sections via `get_order` and writes back to `doc_info.doc.content_orders` | No‑op if `result` is `None` |
| `clear_cache` | `method` | Removes the log file when `config.pbc.save_logs` is falsy | Does **not** delete other cache artefacts |
| `save` | `method` | Writes the fully assembled markdown document (`doc_info.doc.get_full_doc()`) to `output_doc.md` | Overwrites existing file |

> **Critical Logic** – All file‑system paths are resolved through `get_file_path`, which prefixes the project root, the cache folder, and the appropriate filename from `FILE_NAMES`. If the cache directory does not exist, `__init__` creates it.

### Execution Flow (per method)

1. **`__init__`** – Sets up state, configures logger, ensures cache folder exists.  
2. **`generate_code_file`** –  
   - Logs start.  
   - Instantiates `CodeMix(project_directory, config.ignore_files)`.  
   - Calls `build_repo_content()` → stores in `doc_info.code_mix`.  
   - Logs completion, updates progress.  
3. **`generate_global_info`** –  
   - Splits `doc_info.code_mix` via `split_data`.  
   - Calls `compress_to_one(..., compress_power, progress_bar)`.  
   - Persists result to cache and `doc_info.global_info`.  
   - Updates progress.  
4. **`generete_doc_parts`** –  
   - Retrieves optional global file.  
   - Calls `gen_doc_parts(full_code_mix, max_symbols, llm_model, config.get_project_settings(), config.language, progress_bar, global_info)`.  
   - Writes raw output to cache, splits by anchors, populates `doc_info.doc` with `DocContent`.  
   - Logs finish, updates progress.  
5. **`factory_generate_doc`** –  
   - Builds `info` dict (language, current doc, code mix, global info).  
   - Logs module list and parameters.  
   - Executes `doc_factory.generate_doc(info, llm_model, progress_bar)`.  
   - Merges returned `DocHeadSchema` with existing `doc_info.doc` based on `to_start`.  
   - Updates progress.  
6. **`order_doc`** –  
   - Calls `get_order(llm_model, doc_info.doc.content_orders)` and stores ordering back.  
7. **`clear_cache`** – Conditionally removes the log file.  
8. **`save`** – Writes the final assembled markdown to `output_doc.md`.  

All interactions are confined to the imported modules; no external network or file I/O occurs beyond the designated cache directory.
<a name="manager-class-usage"></a>
The Manager class is used to manage the documentation generation process. To use the Manager class, you need to create an instance of it, passing in the project path, config, llm_model, and progress_bar as parameters. 

Here is an example of how to create a Manager instance:
```python
manager = Manager(
    project_path, 
    config=config,
    llm_model=sync_model,
    progress_bar=ConsoleGtiHubProgress(), 
)
```
The Manager class has several methods available:

* `generate_code_file()`: This method generates the code file.
```python
manager.generate_code_file()
```
* `factory_generate_doc()`: This method generates the documentation using the provided DocFactory.
```python
manager.factory_generate_doc(DocFactory(*custom_modules))
```
* `order_doc()`: This method orders the documentation.
```python
manager.order_doc()
```
* `save()`: This method saves the generated documentation.
```python
manager.save()
```
* `clear_cache()`: This method clears the cache.
```python
manager.clear_cache()
```
The Manager class also has a `doc_info` attribute, which has `global_info` and `doc` attributes. The `global_info` attribute can be used to set the global information, and the `doc` attribute has a `get_full_doc()` method to get the full documentation.
```python
manager.doc_info.global_info = gdata
res = split_text_by_anchors(data)
for el in res:
    manager.doc_info.doc.add_parts(el, DocContent(content=res[el]))
print(manager.doc_info.doc.get_full_doc())
```
<a name="history"></a>
## `History` – System Prompt & Message Buffer  

| Field | Type | Role |
|-------|------|------|
| `history` | `list[dict[str,str]]` | Ordered message list for LLM calls |
| `system_prompt` (init) | `str` | Default system message (`BASE_SYSTEM_TEXT`) |

**Behavior** – On init, inserts a `system` role entry if a prompt is provided; `add_to_history` appends arbitrary role/content pairs.

---
<a name="gptmodel"></a>
## `GPTModel` – Synchronous Groq LLM Wrapper  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `str` | Authentication token | Defaults to `API_KEY` from config |
| `history` | `History` | Message buffer for system/user/assistant turns | Initialized with `BASE_SYSTEM_TEXT` |
| `models_list` | `list[str]` | Candidate model identifiers | Shuffled if `use_random=True` |
| `client` | `Groq` | Groq SDK client used for `chat.completions.create` | Created with `api_key` |
| `logger` | `BaseLogger` | Central logger for info/warning/error | Instantiated per object |
| `regen_models_name` | `list[str]` | Runtime‑mutable pool of models to try | Populated from `models_list` |
| `current_model_index` | `int` | Index of model currently being attempted | Starts at `0` |

**Responsibility** – Executes a single LLM call, iterating over `regen_models_name` until a model succeeds or the pool is exhausted, logging each step.

**Visible Interactions** –  
- Calls `self.client.chat.completions.create(messages=…, model=model_name)`.  
- Emits `InfoLog`, `WarningLog`, `ErrorLog` via `BaseLogger`.  
- Raises `ModelExhaustedException` when the pool is empty.

**Logic Flow**  
1. Select `messages` from `self.history.history` (or supplied `prompt`).  
2. Loop:  
   a. If `regen_models_name` empty → log error → raise `ModelExhaustedException`.  
   b. Pick `model_name = regen_models_name[current_model_index]`.  
   c. Attempt `client.chat.completions.create`. On success break.  
   d. On exception: log warning, advance `current_model_index` (wrap to `0`).  
3. Extract `result = chat_completion.choices[0].message.content`.  
4. Log generated answer and return it (empty string if `None`).

---
<a name="modelbase"></a>
## `Model` – Concrete Implementation of `ParentModel`  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `generate_answer` | `method` | Placeholder returning static `"answer"` | Overridden in subclasses |
| `get_answer_without_history` | `method` | Calls `generate_answer(with_history=False)` | Returns `str` |
| `get_answer` | `method` | Adds user prompt to `history`, calls `generate_answer`, stores assistant reply | Returns `str` |

**Responsibility** – Provides synchronous API (`get_answer`, `get_answer_without_history`) built on the abstract `ParentModel`.  

**Interactions** – Relies on `self.history` for context and on subclass overrides for actual LLM calls.

---
<a name="asyncgptmodel"></a>
## `AsyncGPTModel` – Async Stub  

| Entity | Type | Role |
|--------|------|------|
| `AsyncGPTModel` | subclass of `AsyncModel` | Declared but contains no implementation (`...`) |

> **Critical Note** – No functional code is present; attempts to use this class will raise `NotImplementedError` from abstract methods.
<a name="model-exhausted-exception"></a>
## ModelExhaustedException – LLM Availability Signal  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `ModelExhaustedException` | `Exception` subclass | Raised when no LLM model is selectable from a provided pool | No additional attributes; inherits default `Exception` behaviour |

> **Information not present in the provided fragment.**
<a name="install-workflow-setup"></a>

**Installation Workflow Overview**

1. **PowerShell (Windows)**
   - Execute the remote script directly from the repository using the following command in an elevated PowerShell console:  
     ```powershell
     irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
     ```
   - This command downloads the `install.ps1` script and pipes it to the PowerShell interpreter for immediate execution.

2. **Bash (Linux/macOS)**
   - Run the installation script on any Unix‑like system with a single line:  
     ```bash
     curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
     ```
   - The script is fetched via `curl` and executed by `bash`, handling all required setup steps automatically.

3. **GitHub Actions Integration**
   - To enable the workflow in CI/CD, add a secret named `GROCK_API_KEY` to the repository’s GitHub Actions secrets.
   - Obtain your API key from the Grock documentation site (https://grockdocs.com) and store it securely under the secret name.
   - The workflow can then reference `${{ secrets.GROCK_API_KEY }}` wherever the key is needed, ensuring that the key is never exposed in the codebase.

**Key Points**

- Use the exact commands shown above; they pull the latest installer directly from the source repository.
- Ensure you have appropriate permissions (administrator on Windows, sudo or equivalent on Unix) when running the scripts.
- The `GROCK_API_KEY` secret is mandatory for any steps that interact with Grock services; without it, the workflow will fail.
