## Executive Navigation Tree
- 📂 **Installation & Setup**
  - [Install Workflow](#install_workflow)
  - [Install Scripts](#install-scripts)
  - [Project Metadata](#project-metadata)
  - [Package‑Initialisation](#package‑initialisation)
  - [Config Reader Overview](#config_reader_overview)
  - [Project Config Settings](#project_config_settings)
  - [Config Builder](#config_builder)
  - [Read Config Function](#read_config_function)
  - [Config‑Constants](#config‑constants)
  - [Config‑Helper‑Function](#config‑helper‑function)
  - [Config‑Environment‑Setup](#config‑environment‑setup)

- ⚙️ **Configuration & Management**
  - [Manager Usage](#manager_usage)
  - [Manager Class Overview](#manager-class-overview)
  - [Manager Methods](#manager-methods)
  - [Factory Entry Point](#factory‑entry‑point)
  - [Factory Package Overview](#factory-package-overview)
  - [Base‑Module](#base-module)
  - [Doc Factory](#doc-factory)
  - [Built‑In‑Modules](#built‑in‑modules)
  - [Integration Flow](#integration‑flow)
  - [Integration Points](#integration-points)

- 🧩 **Core Models**
  - [Model Exception](#model‑exception)
  - [Model Base Classes](#model‑base‑classes)
  - [GPT Model Implementation](#gpt‑model‑implementation)

- 📄 **Documentation Generation**
  - [Run File Overview](#run_file_overview)
  - [Gen Doc Function](#gen_doc_function)
  - [Execution Flow](#execution_flow)
  - [Generate Descriptions](#generate_descriptions)
  - [Postprocess Overview](#postprocess_overview)
  - [Spliter](#spliter)
  - [Data Splitting](#data-splitting)
  - [Write Docs By Parts](#write-docs-by-parts)
  - [Async Write Docs By Parts](#async-write-docs-by-parts)
  - [Gen Doc Parts](#gen-doc-parts)
  - [Async Gen Doc Parts](#async-gen-doc-parts)

- 📦 **Compression Utilities**
  - [Compress](#compress)
  - [Compress And Compare](#compress_and_compare)
  - [Async Compress](#async_compress)
  - [Compress To One](#compress_to_one)

- 📈 **Logging & Progress**
  - [Logging Subsystem](#logging-subsystem)
  - [Progress Subsystem](#progress-subsystem)

- 🧪 **Assumptions & Limitations**
  - [Assumptions‑Limitations](#assumptions-limitations)

- 🔧 **Miscellaneous**
  - [Autodocconfig Options](#autodocconfig_options')
  - [Code Mix Component](#code-mix-component)

 

<a name='install_workflow'></a>
Explain how install workflow with install.ps1 and install.sh scripts for install you should use links `irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex` for PowerShell and `curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash` for Linux‑based systems and also you have to add secret variable to GitHub Action `GROCK_API_KEY` with your API key from Grock docs https://grockdocs.com to make it work.

<a name='manager_usage'></a>

**How to use the `Manager` class**

The `Manager` class is instantiated with the following parameters (as shown in the provided context):

| Parameter | Type / Description | How it is passed |
|-----------|--------------------|-----------------|
| `project_path` | `str` – Path to the root of the project | Positional argument |
| `project_settings` | `ProjectSettings` object – Settings for the project | Positional argument |
| `pcs` | `ProjectConfigSettings` object – Configuration settings | Positional argument |
| `sync_model` | `GPTModel` instance – Synchronous GPT model | Named argument |
| `async_model` | `AsyncGPTModel` instance – Asynchronous GPT model | Named argument |
| `ignore_files` | `list[str]` – List of file patterns to ignore | Named argument |
| `progress_bar` | `BaseProgress` subclass instance – Progress UI | Named argument |
| `language` | `str` – Language code (e.g., `"en"` for English) | Named argument |

---

### Full example of usage

```python
from autodocgenerator.manage import Manager
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.preprocessor.settings import ProjectSettings
from .config_reader import Config, read_config, ProjectConfigSettings

# 1. Load configuration (as done in the context)
with open("autodocconfig.yml", "r", encoding="utf-8") as file:
    config_data = file.read()
config: Config = read_config(config_data)

# 2. Retrieve required objects from the config
project_settings: ProjectSettings = config.get_project_settings()
pcs: ProjectConfigSettings = config.pcs
ignore_list: list[str] = config.ignore_files

# 3. Create GPT model instances
sync_model = GPTModel(API_KEY, use_random=False)
async_model = AsyncGPTModel(API_KEY)

# 4. Instantiate the Manager
manager = Manager(
    project_path=".",                # path to the current project
    project_settings=project_settings,
    pcs=pcs,
    sync_model=sync_model,
    async_model=async_model,
    ignore_files=ignore_list,
    progress_bar=ConsoleGtiHubProgress(),
    language="en"
)

# 5. Use the manager to generate documentation (example sequence)
manager.generate_code_file()
manager.generate_global_info_file(use_async=False, max_symbols=8000)
manager.generete_doc_parts(use_async=False, max_symbols=5000)

# (Further steps such as factory generation, cache clearing, etc. can follow
# the pattern shown in the original `gen_doc` function.)
```

<a name='autodocconfig_options'> </a>
The **autodocconfig.yml** file is a YAML document that can contain the following top‑level keys, as shown in the repository’s example:

- **project_name** – string, the name of the project (e.g., `"Auto Doc Generator"`).  
- **language** – string, language code for the documentation (e.g., `"en"`).  
- **ignore_files** – optional list of glob patterns to exclude from processing (e.g., `"*.pyc"`, `"__pycache__"`).  
- **project_settings** – mapping with configuration for the generator itself:  
  - **save_logs** – boolean, whether to keep generation logs.  
  - **log_level** – integer, verbosity level (e.g., `2`).  
- **project_additional_info** – mapping for arbitrary additional metadata; any key/value pair can be added (e.g., `global idea: "This project was created to help developers..."`).  
- **custom_descriptions** – list of strings, each describing a custom documentation request that will be processed by the generator.  

These keys are read by `autodocgenerator.auto_runner.config_reader.read_config` and used to build the generation configuration. No other options are defined in the provided context.

 

**<a name="package‑initialisation"></a># autodocgenerator package initialisation**

```python
# autodocgenerator/__init__.py
print("ADG")
from .ui.logging import BaseLogger, BaseLoggerTemplate, InfoLog, ErrorLog, WarningLog

logger = BaseLogger()
logger.set_logger(BaseLoggerTemplate())
```

### Responsibility
This module is the *entry point* for the **autodocgenerator** package.  
Its sole purpose is to bootstrap a **global logger** that can be used by every sub‑module (engine, factory, pre‑processor, UI, etc.) without the need to instantiate a logger repeatedly.

### Interaction with the rest of the system
* **ui.logging** – imports the concrete logging classes (`BaseLogger`, `BaseLoggerTemplate`, …) which implement a thin wrapper around **Rich**‑styled console output.
* All other modules import `autodocgenerator.logger` (e.g. `from autodocgenerator import logger`) and call `logger.info(...)`, `logger.error(...)`, etc. This centralises log configuration and guarantees a consistent format across the whole application.

### Key objects & flow
1. **`BaseLogger()`** – creates a logger instance with default settings (level, handlers).
2. **`BaseLoggerTemplate()`** – provides the concrete Rich‑styled formatter and handler configuration.
3. `logger.set_logger(BaseLoggerTemplate())` – binds the template to the logger, finalising the output pipeline.
4. The `print("ADG")` statement is a harmless side‑effect used during development to confirm that the package has been imported correctly.

### Assumptions
* The **ui.logging** module is importable and its classes conform to the expected interface (`set_logger` accepts a template instance).
* No additional configuration (e.g., log file path) is required at import time; defaults are sufficient for normal operation.

### Inputs / Outputs
* **Input:** None – the module runs automatically on import.
* **Output:** A configured `logger` object available as `autodocgenerator.logger`; console output of the string *“ADG”* the first time the package is imported.

### Side effects
* Writes “ADG” to STDOUT on first import (can be silenced by removing the `print` line).
* Registers a global logger that influences the logging behaviour of every downstream component.

<a name="config_reader_overview"></a>**Config Reader – autodocgenerator.auto_runner.config_reader**  
Loads *autodocconfig.yml*, transforms YAML into a runnable **Config** object and a tiny **ProjectConfigSettings** holder.  
The module is imported by **run_file.py**; no external calls are required.

<a name="project_config_settings"></a>**ProjectConfigSettings**  
- Attributes: `save_logs` (bool), `log_level` (int).  
- `load_settings(data)` copies any key/value from the supplied dict onto the instance via `setattr`.  
Used by the manager to control logging and other runtime flags.

<a name="config_builder"></a>**Config class**  
- Holds defaults: `ignore_files`, `language`, `project_name`, `project_additional_info`, `custom_modules`, and a `pcs` instance.  
- Fluent setters (`set_language`, `set_pcs`, …) return `self` for chaining.  
- `get_project_settings()` creates a **ProjectSettings** object and injects any extra info.  
- `get_doc_factory()` builds two **DocFactory** instances – one for user‑defined `custom_modules`, another for built‑in intro modules (`IntroLinks`, optional `IntroText`).  

<a name="read_config_function"></a>**read_config(file_data)**  
1. `yaml.safe_load` → dict.  
2. Populates ignore patterns, language, name, additional info.  
3. Instantiates `ProjectConfigSettings` and applies `project_settings` section.  
4. Adds custom description modules via `CustomModule`.  
5. Returns a fully‑populated **Config**.  
*Inputs*: raw YAML string. *Outputs*: `Config` object. No side‑effects besides object creation.

<a name="run_file_overview"></a>**Run File – autodocgenerator.auto_runner.run_file**  
Entry‑point script (`python -m autodocgenerator.auto_runner.run_file`).  

<a name="gen_doc_function"></a>**gen_doc(...)**  
- Instantiates synchronous (`GPTModel`) and asynchronous (`AsyncGPTModel`) LLM wrappers using the global `API_KEY`.  
- Creates a **Manager** with project path, settings, `pcs`, ignore list, a console progress bar (`ConsoleGtiHubProgress`), and language.  
- Calls the manager’s pipeline:  
  1. `generate_code_file`  
  2. `generate_global_info_file` (sync, 8 k symbols)  
  3. `generete_doc_parts` (sync, 5 k symbols)  
  4. `factory_generate_doc` for both factories (custom + intro)  
  5. `clear_cache`  
- Returns the final assembled document via `read_file_by_file_key("output_doc")`.  

<a name="execution_flow"></a>**Execution Flow ( __main__ )**  
1. Reads *autodocconfig.yml*.  
2. Calls `read_config` → `Config`.  
3. Extracts `project_settings` and both factories.  
4. Invokes `gen_doc` with those objects and the current directory.  
5. Stores the generated documentation in `output_doc`.  

**Assumptions** – YAML follows the expected schema; `API_KEY` is defined; all imported factories and UI components conform to their interfaces. No external files are written until the manager’s `clear_cache` step.

## <a name="config‑constants"></a>Prompt‑Template Constants  
The module defines a collection of multi‑line string constants (`BASE_SYSTEM_TEXT`, `BASE_PART_COMPLITE_TEXT`, `BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`, `BASE_SETTINGS_PROMPT`).  
These are **static prompt templates** used by the AutoDoc engine to instruct the LLM at various stages:

* **BASE_SYSTEM_TEXT** – Global instruction for incremental snippet analysis.  
* **BASE_PART_COMPLITE_TEXT** – Guidelines for generating concise documentation of a code fragment.  
* **BASE_INTRODACTION_CREATE_TEXT** – Rules for building the “Executive Navigation Tree”.  
* **BASE_INTRO_CREATE** – Template for a high‑level project overview.  
* **BASE_SETTINGS_PROMPT** – Prompt that turns the system into a persistent project knowledge base.

All templates are referenced by the **PromptManager** (or similar) to build the messages sent to the language model, ensuring consistent behavior across processing phases.

---

## <a name="config‑helper‑function"></a>Helper Function `get_BASE_COMPRESS_TEXT`  
```python
def get_BASE_COMPRESS_TEXT(start, power):
    return f""" … """
```
* **Purpose** – Dynamically creates a compression‑prompt that adapts to the size of an incoming code snippet (`start`) and a scaling factor (`power`).  
* **Interaction** – Called by the **CompressionEngine** right before a large snippet is sent to the LLM, providing a concise analysis request and a strict usage‑example skeleton.  
* **Inputs** – `start` (approx. character count of the snippet) and `power` (division factor controlling the allowed summary length).  
* **Output** – A formatted prompt string containing placeholders for analysis, summary length, and an example code block.

---

## <a name="config‑environment‑setup"></a>Environment Loading & Global Settings  
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise Exception("API_KEY is not set in environment variables.")

MODELS_NAME = ["openai/gpt-oss-120b", "llama-3.3-70b-versatile", "openai/gpt-oss-safeguard-20b"]
```
* **Responsibility** – Loads the `.env` file, extracts the required `API_KEY`, and aborts early if it is missing, guaranteeing that the LLM client can authenticate.  
* **`MODELS_NAME`** – Provides a default list of model identifiers the engine may select from when generating prompts.  
* **Interaction** – These globals are imported by the **LLMClient** and **ModelSelector** components, which rely on `API_KEY` for authentication and `MODELS_NAME` for model resolution.

---

### Summary
`config.py` centralises all static prompts, the dynamic compression‑prompt builder, and essential runtime configuration (environment variables and default model list). It serves as the *single source of truth* for textual instructions and credentials, enabling other engine modules (PromptManager, CompressionEngine, LLMClient) to operate without hard‑coded strings or duplicated logic. This separation keeps the core processing code clean and makes updates to prompts or credentials straightforward.

## <a name="model‑exception"></a>Exception `ModelExhaustedException`  
```python
class ModelExhaustedException(Exception):
    """Raised when no model in the rotation list is usable."""
```
* **Role** – Signals that every model in `regen_models_name` has failed, forcing the caller to abort or retry with a new configuration.  
* **Used by** – `GPTModel` and `AsyncGPTModel` during the retry loop.

---

## <a name="model‑base‑classes"></a>Core hierarchy (`model.py`)  

| Class | Responsibility | Key members |
|-------|----------------|-------------|
| **History** | Holds the chat history sent to the LLM. Initialized with `BASE_SYSTEM_TEXT` (global system prompt). | `history` list, `add_to_history()` |
| **ParentModel** | Supplies shared configuration: API key, history container, model‑list shuffling, and current‑model index. | `api_key`, `history`, `current_model_index`, `regen_models_name` |
| **Model** (sync) | Implements thin wrappers around `generate_answer()`. Provides `get_answer()` (records user → assistant exchange) and a no‑history shortcut. | `generate_answer()` (placeholder), `get_answer*()` |
| **AsyncModel** (async) | Same contract as `Model` but with `async` methods. | `generate_answer()`, `get_answer*()` (awaited) |

*Assumptions*: `BASE_SYSTEM_TEXT`, `API_KEY`, and `MODELS_NAME` are defined in `config.config`. The history starts with the system prompt unless overridden.

---

## <a name="gpt‑model‑implementation"></a>Concrete providers (`gpt_model.py`)  

* **`GPTModel`** – Synchronous wrapper around the Groq client.  
  * Initializes `self.client = Groq(api_key=self.api_key)` and a `BaseLogger`.  
  * `generate_answer()` builds the message payload (history or explicit `prompt`), then iterates over `regen_models_name` trying each model until a successful `chat.completions.create` call. On failure it logs a warning, advances the index (wrap‑around), and retries. When a model succeeds it returns `chat_completion.choices[0].message.content` and logs the result.

* **`AsyncGPTModel`** – Asynchronous counterpart using `AsyncGroq`.  
  * Same retry logic, but `await`‑ed and logs “Generating answer asynchronously…”.

Both raise **`ModelExhaustedException`** if the rotation list becomes empty.

*Side effects*: Mutates `self.history` (via parent methods), updates `self.current_model_index`, writes log entries via `BaseLogger`.

---

## <a name="factory‑entry‑point"></a>Factory package (`factory/__init__.py`)  

The file is currently empty; it exists to make `autodocgenerator.factory` a Python package. Future factory functions (e.g., `create_model()`) can be added here to encapsulate the selection of `GPTModel` vs. `AsyncGPTModel` based on runtime configuration.

<a name="factory-package-overview"></a>
## 📦 autodocgenerator.factory – Overview  

The **factory** package glues together *document‑generation modules* and the language model.  
`__init__.py` is intentionally empty – it only marks the directory as a Python package.  In the future it will expose helper functions (e.g. `create_model()`) that decide whether to instantiate `GPTModel` or `AsyncGPTModel` based on runtime settings.

<a name="base-module"></a>
## 🧩 BaseModule (abstract)  

*Location:* `factory/base_factory.py`  

- Defines the contract for every generation step.  
- Sub‑classes must implement `generate(info: dict, model: Model) → str`.  
- No state is required; the base `__init__` is a placeholder.

<a name="doc-factory"></a>
## 🏗️ DocFactory  

*Location:* `factory/base_factory.py`  

- **Constructor** `DocFactory(*modules)` stores a list of `BaseModule` instances.  
- **Method** `generate_doc(info, model, progress)` orchestrates:  

  1. Creates a sub‑task in `BaseProgress` sized to the number of modules.  
  2. Calls each module’s `generate`, concatenates results (`output += … + "\n\n"`).  
  3. Logs module activity via `BaseLogger` (`InfoLog`).  
  4. Advances the progress bar and finally removes the sub‑task.  

- Returns the full documentation string.  
- Side‑effects: progress UI updates, log entries.

<a name="built‑in‑modules"></a>
## 📄 Built‑in Modules  

| Module | Purpose | Key Call |
|--------|---------|----------|
| `modules.intro.IntroLinks` | Extracts HTML links from `info["full_data"]` and asks the model for a linked introduction. | `get_links_intro(…)` |
| `modules.intro.IntroText` | Generates a textual introduction from `info["global_data"]`. | `get_introdaction(…)` |
| `modules.general_modules.CustomModule` | Produces a custom description defined at instantiation (`discription`). | `generete_custom_discription(split_data(...), model, …)` |

All modules inherit `BaseModule`, receive the same `info` dictionary and a `Model` instance, and return a markdown‑compatible string.

<a name="integration‑flow"></a>
## 🔄 Integration Flow  

1. **Configuration** builds a list of desired modules (e.g., `IntroLinks()`, `CustomModule("API overview")`).  
2. `DocFactory` is instantiated with that list.  
3. The main application supplies `info` (parsed code, language, etc.), a concrete `Model`, and a `BaseProgress` UI object.  
4. `DocFactory.generate_doc` returns the assembled documentation, while progress and logging keep the user informed.

---  

*Assumptions*: `info` contains keys used by modules (`code_mix`, `full_data`, `global_data`, `language`).  
*Outputs*: a single markdown string.  
*Side‑effects*: UI progress updates, logging to the configured sink.  

Future additions to `factory/__init__.py` will expose convenience constructors that hide the module‑selection logic from callers.

<a name="manager-class-overview"></a>
## Manager – Central Orchestrator for Documentation Generation  

The **`Manager`** class glues together all preprocessing, LLM‑model, factory and UI components of **AutoDocGenerator**.  
It owns a per‑project cache folder (`.auto_doc_cache`) where intermediate artefacts are stored:

| key | filename |
|-----|----------|
| `code_mix` | `code_mix.txt` – raw repository dump |
| `global_info` | `global_info.md` – compressed project summary |
| `logs` | `report.txt` – run‑time log file |
| `output_doc` | `output_doc.md` – final markdown document |

### Core responsibilities  

* Initialise logging (`BaseLogger` → `FileLoggerTemplate`) and a progress UI (`BaseProgress`).  
* Provide thin helpers (`read_file_by_file_key`, `get_file_path`) for cache I/O.  
* Drive the three generation stages:
  1. **Code mix** – `generate_code_file()` builds a plain‑text representation of the repository using `preprocessor.code_mix.CodeMix`.  
  2. **Global info** – `generate_global_info_file()` (placeholder implementation) would compress the code mix via `spliter` + `compressor`.  
  3. **Doc parts** – `generete_doc_parts()` splits the mixed code and global info into chunks and feeds them to either a synchronous (`gen_doc_parts`) or asynchronous (`async_gen_doc_parts`) LLM model, producing a first draft (`output_doc.md`).  
* Post‑process the draft with a **factory** (`factory_generate_doc`). The supplied `DocFactory` aggregates custom modules (e.g., `IntroText`, `IntroLinks`, `CustomModule`) and calls `DocFactory.generate_doc(info, sync_model, progress_bar)`. The factory result is prepended to the existing document.  
* Clean up cache artefacts (`clear_cache`) respecting the `save_logs` flag from `ProjectConfigSettings`.

<a name="manager-methods"></a>
## Key Methods  

| Method | What it does | Important I/O / side‑effects |
|--------|--------------|------------------------------|
| `__init__` | Stores configuration, creates cache folder, wires logger and progress bar. | Writes a log file path; creates `CACHE_FOLDER_NAME` if missing. |
| `read_file_by_file_key` | Reads a cached file by logical key. | Returns UTF‑8 string content. |
| `get_file_path` | Resolves the absolute path for a cached file. | Pure path construction. |
| `generate_code_file` | Instantiates `CodeMix`, writes repository dump to cache. | Updates progress bar; logs start/completion. |
| `generate_global_info_file` | (stub) reads code mix, would compress it, writes placeholder `"ss"` to cache. | Updates progress bar; logs start/completion. |
| `generete_doc_parts` | Calls either `gen_doc_parts` or `async_gen_doc_parts` to produce a draft. | Writes `output_doc.md`; logs steps; updates progress. |
| `factory_generate_doc` | Loads cached artefacts, builds an `info` dict, runs the provided `DocFactory`. Prepends factory output to the draft. | Writes updated `output_doc.md`; logs module list and input sizes; updates progress. |
| `clear_cache` | Removes the log file unless `pcs.save_logs` is `True`. | File‑system side‑effect. |

<a name="integration-points"></a>
## Interaction with Other Sub‑systems  

* **Pre‑processor** – `CodeMix`, `split_data`, `gen_doc_parts`, `async_gen_doc_parts` (all under `autodocgenerator.preprocessor`).  
* **LLM Engine** – `Model` / `AsyncModel` instances supplied at construction; passed transparently to compression and doc‑part generators.  
* **Factory** – Concrete factories live in `autodocgenerator.factory`; `factory_generate_doc` supplies them with the unified `info` dict and the synchronous model.  
* **UI** – `BaseProgress` (and subclasses) receives `update_task()` calls after each major step; `BaseLogger` writes human‑readable logs to the cache.  

<a name="assumptions-limitations"></a>
## Assumptions & Limitations  

* The cache directory must be writable; otherwise initialization fails.  
* `generate_global_info_file` currently writes a dummy string – real implementation should invoke the commented‑out compression pipeline.  
* `generete_doc_parts` expects the supplied model to implement the same interface as `gen_doc_parts`/`async_gen_doc_parts`.  
* All file reads/writes are performed synchronously; large projects may benefit from streaming I/O in future revisions.  

---  

*This documentation covers the final orchestration layer (`Manager`) of the AutoDocGenerator pipeline. It is intended for developers extending the generation workflow, adding new factory modules, or swapping model back‑ends.*

<a name="code-mix-component"></a>
## `CodeMix` – Repository → Text Mixer  

**Responsibility**  
`CodeMix` walks a source‑tree, filters unwanted files/folders, and writes a single UTF‑8 document that first lists the directory hierarchy and then embeds every included file wrapped in `<file path="…">` tags. The output is later consumed by the pre‑processor (`Manager.generate_code_file`) to feed the LLM pipeline.

**Key API**  

| Member / Method | Purpose | I/O & Side‑effects |
|-----------------|---------|--------------------|
| `__init__(root_dir=".", ignore_patterns=None)` | Resolve the repository root and store ignore patterns. Instantiates a lightweight `BaseLogger`. | Creates `Path` objects; no FS writes. |
| `should_ignore(path: Path) -> bool` | Returns *True* if *path* matches any pattern in `ignore_patterns` (glob, basename, or any part). | Pure calculation; uses `fnmatch`. |
| `build_repo_content(output_file="repomix-output.txt")` | Generates the mixed file: writes a “Repository Structure” tree, a separator, then each file’s content. Logs ignored entries via `InfoLog`. | Writes (or overwrites) `output_file`; may raise if directory not writable. Errors while reading a file are captured and written as a line in the output. |

**Interaction with the System**  

* **Manager** – Calls `CodeMix(root_dir, ignore_patterns).build_repo_content(cache_path)` to obtain the repository dump before compression or doc‑part generation.  
* **Logging UI** – Uses `BaseLogger` (from `autodocgenerator.ui.logging`) to emit human‑readable messages that appear in the per‑run cache folder.  
* **LLM factories** – The generated file becomes the `code_mix_file` artefact loaded later by `Manager.factory_generate_doc`.  

**Assumptions & Limitations**  

* The supplied `root_dir` must exist and be readable; the process aborts on permission errors.  
* `ignore_patterns` are interpreted as Unix‑style glob strings; complex regexes are not supported.  
* File reading is performed synchronously with `errors="ignore"` – binary or badly‑encoded files will be silently corrupted.  
* The placeholder newline sequence `"\n\n\n"` after each file is intentional for later parsing but could be refined.  

**Typical Usage**  

```python
from autodocgenerator.preprocessor.code_mix import CodeMix, ignore_list

mix = CodeMix(root_dir="my_project", ignore_patterns=ignore_list)
mix.build_repo_content("codemix.txt")   # creates the mixed repository snapshot
```

The resulting `codemix.txt` is the canonical input for the rest of the AutoDocGenerator pipeline.

<a name="overview"></a>
## Overview  
`compressor.py` provides the **text‑compression & summarisation** stage of the AutoDocGenerator pipeline.  
It feeds raw code snippets (or any repository content) to a LLM model, asks the model to shrink the input according to a configurable *compress power*, and aggregates the results so that later stages receive a single, concise representation of the whole project.

<a name="dependencies"></a>
## Dependencies & Interaction  
* **Models** – `Model` / `AsyncModel` from `engine.models.gpt_model` are used to call `get_answer_without_history`.  
* **ProjectSettings** – supplies the *system prompt* (`project_settings.prompt`).  
* **Configuration** – `get_BASE_COMPRESS_TEXT` builds the LLM instruction that encodes the desired compression level.  
* **Progress UI** – `BaseProgress` visualises work; each public routine creates a sub‑task, updates it per element, and removes it on completion.  

<a name="compress"></a>
## `compress`  
```python
compress(data: str, project_settings, model, compress_power) -> str
```  
Creates a three‑part prompt (system‑prompt, compression instruction, user data) and returns the model’s compressed answer.

**Assumptions** – `compress_power` is a positive int; `model` implements the synchronous API.

<a name="compress_and_compare"></a>
## `compress_and_compare`  
*Batch version* for a list of strings.  
* Splits the input list into chunks of size `compress_power`.  
* Calls `compress` for each element, concatenating results per chunk.  
* Returns a list whose length ≈ `len(data) / compress_power`.  

Side‑effect: updates the supplied `progress_bar`.

<a name="async_compress"></a>
## `async_compress` & `async_compress_and_compare`  
Asynchronous counterparts that respect a semaphore (max 4 concurrent calls).  
`async_compress` builds the same prompt as `compress` but awaits `model.get_answer_without_history`.  
`async_compress_and_compare` launches all tasks, gathers results, then re‑chunks them exactly like `compress_and_compare`.

<a name="compress_to_one"></a>
## `compress_to_one`  
Iteratively reduces a list of fragments to a **single compressed document**:  

1. While more than one chunk exists, call either the async or sync batch compressor with a dynamic `compress_power` (downgraded to 2 when the list is short).  
2. Increment an internal iteration counter (useful for logging).  

Returns the final string.

<a name="generate_descriptions"></a>
## `generate_describtions_for_code`  
Takes the fully‑compressed code, asks the model to produce **developer‑facing documentation** per fragment.  
The system prompt enforces a strict format (components, parameters, usage example) and forbids hallucination.  
Outputs a list of markdown‑formatted descriptions, one per input element, while driving the progress UI.  

---  

**Key Assumptions**  
* All model objects are already authenticated and reachable.  
* `project_settings.prompt` is a valid system instruction.  
* `compress_power` ≤ length of `data` unless the fallback to 2 is applied.  

**Outputs**  
* Strings (compressed text or generated documentation).  
* Progress bar side‑effects for CLI feedback.  

<a name="postprocess_overview"></a>## Post‑processing Helpers (`postprocess.py`)  

**Responsibility** – After the LLM has generated raw markdown, this module extracts navigation data (section titles, HTML anchors) and creates short introductory texts that link to those sections. It does **not** modify the documentation content itself; it only builds auxiliary strings used by the final renderer.  

**Interactions**  
* **LLM models** – `Model` (or its subclasses) from `engine.models.model` is called via `get_answer_without_history` to ask the model to write an introduction that lists provided links.  
* **Configuration** – `BASE_INTRODACTION_CREATE_TEXT` and `BASE_INTRO_CREATE` supply the system prompts that enforce language and style.  
* **Logging UI** – `BaseLogger` + `InfoLog` produce console feedback; no state is mutated outside the logger.  

### Key Functions  

| Function | Purpose | Important I/O | Side‑effects |
|----------|---------|---------------|--------------|
| `generate_markdown_anchor(header: str) -> str` | Normalises a heading into a Git‑Hub‑style markdown anchor (`#my‑title`). | `header` – raw heading text. Returns anchor string prefixed with `#`. | None. |
| `get_all_topics(data: str) -> tuple[list[str], list[str]]` | Scans a markdown document for level‑2 headings (`## …`) and returns both the raw titles and their generated anchors. | `data` – full markdown. Returns `(titles, anchors)`. | None. |
| `get_all_html_links(data: str) -> list[str]` | Finds custom HTML anchors (`<a name="…">`) inside the doc, extracts the name, and returns a list of `#name` links (max length 25). | `data` – full markdown. Returns list of link strings. | Logs extraction progress via `BaseLogger`. |
| `get_links_intro(links: list[str], model: Model, language: str = "en") -> str` | Sends the list of links to the LLM with a system prompt (`BASE_INTRODACTION_CREATE_TEXT`) and receives a short introductory paragraph that references them. | `links` – list of `#…` strings. Returns generated intro text. | Logs start/completion; makes a synchronous LLM call. |
| `get_introdaction(global_data: str, model: Model, language: str = "en") -> str` | Similar to `get_links_intro` but creates a full‑document introduction based on the entire compressed markdown (`global_data`). | `global_data` – whole doc. Returns intro paragraph. | Logs via `BaseLogger`; synchronous LLM call. |
| `generete_custom_discription(splited_data: str, model: Model, custom_description: str, language: str = "en") -> str` | Iterates over pre‑split fragments, asking the model to produce a custom description (title + `<a name='…'>` anchor) respecting strict “no‑hallucination” rules. Stops at the first fragment that yields a non‑empty answer. | `splited_data` – iterable of fragments, `custom_description` – user‑requested topic. Returns the description or empty string. | Logs through `BaseLogger`; may perform several LLM calls. |

**Assumptions**  
* The input markdown follows the convention of `## ` headings and optional `<a name="…">` tags.  
* `model` implements the synchronous `get_answer_without_history` API and is already authenticated.  
* Language code (`en`, `ru`, …) is supported by the LLM.  

---

<a name="projectsettings"></a>## Project Settings (`settings.py`)  

**Responsibility** – Holds static project metadata used to build the system prompt for the LLM. It aggregates a base prompt (`BASE_SETTINGS_PROMPT`) with the project name and any key/value pairs supplied by the caller.  

**Key API**  
* `ProjectSettings(project_name: str)` – ctor stores the name.  
* `add_info(key, value)` – registers additional metadata.  
* `prompt` (property) – concatenates `BASE_SETTINGS_PROMPT`, the project name, and each `key: value` line into a single string ready for insertion into LLM prompts.  

**Assumptions & Side‑effects**  
* `BASE_SETTINGS_PROMPT` is a valid multi‑line instruction.  
* No I/O; purely in‑memory string assembly.  

---

<a name="spliter"></a>## Split‑Data Stub (`spliter.py`)  

Only the beginning of the file is shown; the core function `split_data(data: str, max_symbols: int) -> list[str]` is intended to break a large markdown string into smaller chunks that respect a token/character limit (`max_symbols`).  

**Typical Interaction**  
* Called by the compression pipeline (see the *compress* section of the global documentation) to produce a list of fragments that are later fed to the LLM.  
* Uses `BASE_PART_COMPLITE_TEXT` as part of the prompt for each fragment, and `BaseProgress` to visualise progress.  

**Assumptions**  
* `data` contains the full documentation text.  
* `max_symbols` is a positive integer smaller than the total length; the function will ensure no fragment exceeds it.  

---  

**Overall Role in the System**  

These three modules sit at the *post‑compression* stage: `spliter` prepares size‑limited fragments, `settings` supplies the contextual prompt, and `postprocess` extracts navigation anchors and asks the LLM to generate concise introductions and custom descriptions. Together they turn a raw, compressed markdown blob into a navigable, developer‑friendly documentation set ready for final rendering.

<a name="data-splitting"></a>## Data‑splitting Adjustments  

The loop normalises the raw *splited_by_files* list so that no fragment exceeds **1.5 × max_symbols**.  
* Over‑length chunks are cut in half and re‑inserted.  
* Afterwards a second pass packs the normalised pieces into **split_objects**, each respecting **1.25 × max_symbols**.  

**Inputs** – `splited_by_files` (list of strings), `max_symbols` (int).  
**Outputs** – `split_objects` (list of size‑limited fragments) used by the documentation‑generation pipeline.  
**Side‑effects** – logs progress via `BaseLogger`.  

---  

<a name="write-docs-by-parts"></a>## `write_docs_by_parts`  

Generates documentation for a single markdown fragment synchronously.  

* Builds an LLM **prompt**:  
  1. System message fixing the response language.  
  2. System message containing `BASE_PART_COMPLITE_TEXT` (the “write‑part” instruction).  
  3. Optional system message with the previous part’s output (`prev_info`).  
  4. User message with the current `part`.  
* Calls `model.get_answer_without_history`.  
* Strips surrounding markdown fences (``` … ```) and returns the clean text.  

**Parameters**  
- `part: str` – fragment to document.  
- `model: Model` – synchronous LLM wrapper.  
- `global_info: str` – (currently unused, reserved for future context).  
- `prev_info: str | None` – tail of the previous generation to keep continuity.  
- `language: str` – target language (default “en”).  

**Returns** – generated markdown string.  

---  

<a name="async-write-docs-by-parts"></a>## `async_write_docs_by_parts`  

Async counterpart of the above. It receives an `AsyncModel`, runs the same prompt logic inside an `async with semaphore` block, optionally calls `update_progress`, and returns the cleaned answer.  

---  

<a name="gen-doc-parts"></a>## `gen_doc_parts`  

Orchestrates *full* documentation creation in a synchronous pipeline.  

1. Calls `split_data(full_code_mix, max_symbols)` to obtain size‑limited fragments.  
2. Iterates over fragments, invoking `write_docs_by_parts`.  
3. Concatenates results, keeping the last 3 000 characters as context for the next call (`result = result[-3000:]`).  
4. Updates a `BaseProgress` sub‑task after each fragment.  

**Outputs** – a single markdown string containing the whole generated documentation.  

---  

<a name="async-gen-doc-parts"></a>## `async_gen_doc_parts`  

Async version of `gen_doc_parts`.  

* Splits the input, creates a semaphore (default 4 concurrent calls) and a progress sub‑task.  
* Fires off `async_write_docs_by_parts` for every fragment, gathers results with `asyncio.gather`, and joins them.  

Both generators feed the **post‑compression** stage of the system, turning chunked code into a navigable, developer‑friendly documentation set ready for final rendering.

<a name="logging-subsystem"></a>
## Logging subsystem – runtime diagnostics and persistence  

The **logging** module defines a tiny hierarchy of log objects (`BaseLog`, `ErrorLog`, `WarningLog`, `InfoLog`) that know how to format themselves with a timestamp and severity tag.  
`BaseLoggerTemplate` implements the filtering logic (`log_level` < 0 → all, otherwise only logs with `level ≤ log_level`) and a generic `log()` that prints to stdout.  
`FileLoggerTemplate` overrides `log()` to append the formatted text to a user‑specified file, enabling persistent build‑time diagnostics.  

`BaseLogger` is a **singleton façade** used throughout the generator pipeline. The generator creates a single `BaseLogger` instance, injects a concrete template via `set_logger()`, and calls `log()` wherever status messages are needed. The façade forwards calls to the configured template’s `global_log()`, guaranteeing a single point of control for all log output.  

*Assumptions*: callers provide a `BaseLog` subclass instance; `log_level` is an integer where higher values represent more detailed logs.  
*Side‑effects*: writing to stdout or appending to a file; no mutation of log objects after creation.

<a name="progress-subsystem"></a>
## Progress subsystem – visual feedback for long‑running steps  

`BaseProgress` declares the abstract API (`create_new_subtask`, `update_task`, `remove_subtask`).  
`LibProgress` implements this API using **Rich**’s `Progress` widget: it creates a base “General progress” task, spawns optional sub‑tasks, and advances the appropriate task on each `update_task()` call. Removing a sub‑task simply discards the reference, letting Rich finish the base task.  

`ConsoleGtiHubProgress` is a fallback that prints simple textual updates to the console. It uses the helper `ConsoleTask` to track current progress and emit percentage‑based messages.  

The generator injects one of these concrete progress objects into its orchestration layer, allowing the same orchestration code to drive either rich terminal UI or plain console output without modification.

<a name="install-scripts"></a>
## Install scripts – bootstrap for CI workflow  

`install.ps1` (PowerShell) and `install.sh` (Bash) create the `.github/workflows` directory, write a reusable GitHub Actions workflow (`autodoc.yml`), and generate `autodocconfig.yml` containing the current folder name as `project_name` and a fixed language (`en`).  

Both scripts are idempotent (they use `-Force` / `mkdir -p`), and they output a short success message. The generated workflow file is later used by the CI system to invoke the **AutoDoc** generator, while the config file supplies project‑specific metadata required by the generator at runtime.  

<a name="project-metadata"></a>
## Project metadata (pyproject.toml)

This **pyproject.toml** is the canonical source of truth for the *AutoDoc* generator package.  
It supplies the CI‑generated workflow and the runtime config with the information the
generator needs to resolve templates, locate source files and embed project‑specific
metadata (name, version, authors, license, etc.) into the produced documentation.

### Core responsibilities
* Declares the package name **`autodocgenerator`**, version **`0.7.9`**, description and
  licensing – values later interpolated into the generated `README` and docs.
* Lists all runtime dependencies (e.g. `pyyaml`, `pydantic`, `openai`) that the
  **AutoDoc** engine imports when the CI workflow runs.
* Defines the **build‑system** (`poetry-core`) so the CI job can `pip install .`
  before invoking the generator.

### Interaction with other components
* The **workflow‑creation script** (the part that uses `-Force` / `mkdir -p`) copies this
  file into the repository’s root; the CI runner reads it to install exact versions,
  guaranteeing reproducible documentation builds.
* The **config generator** reads the `[project]` fields to fill placeholders in the
  `autodoc_config.yml` that the generator consumes at runtime.

### Assumptions & side‑effects
* Assumes Python 3.11 – 3.12 (as declared by `requires-python`).  
* The presence of this file triggers Poetry to resolve and lock the dependency graph;
  missing entries will cause the CI step to fail.  
* No runtime side‑effects beyond package installation; it is purely declarative.

---  
*Success*: The script reports “✅ Workflow and config generated” after writing this file,
signalling that the CI pipeline can now safely invoke the **AutoDoc** generator.

