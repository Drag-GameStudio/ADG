## Executive Navigation Tree

- 📁 **Configuration**
  - [#autodocconfig.yml](#autodocconfig.yml)
  - [#config-classes](#config-classes)
  - [#config-methods](#config-methods)
  - [#config-usage](#config-usage)
  - [#config-reader-component](#config-reader-component)
  - [#pyproject-configuration](#pyproject-configuration)

- ⚙️ **Generation**
  - [#autodocgenerator/auto_runner/run_file.py](#autodocgenerator/auto_runner/run_file.py)
  - [#async-doc-generation](#async-doc-generation)
  - [#sync-doc-generation](#sync-doc-generation)

- 📦 **Modules**
  - [#module-initialization](#module-initialization)
  - [#module-interactions](#module-interactions)

- 🔗 **Interactions**
  - [#interactions](#interactions)
  - [#runtime-interaction](#runtime-interaction)

- 📚 **Intro Modules**
  - [#intro-links-module](#intro-links-module)
  - [#intro-text-module](#intro-text-module)
  - [#custom-intro-module](#custom-intro-module)

- 📈 **Data Flow**
  - [#data-flow](#data-flow)
  - [#data-flow-diagram](#data-flow-diagram)

- 🧠 **Models**
  - [#asyncgptmodel-class](#asyncgptmodel-class)
  - [#gptmodel-class](#gptmodel-class)
  - [#model‑dependency](#model‑dependency)
  - [#model-exception-handling](#model-exception-handling)

- 🔧 **Pipeline**
  - [#pipeline-assembly](#pipeline-assembly)
  - [#sorting-module](#sorting-module)
  - [#compressor-module](#compressor-module)
  - [#spliter-module](#spliter-module)

- ⚠️ **Error & Logging**
  - [#error-handling-and-logging](#error-handling-and-logging)
  - [#base-log-classes](#base-log-classes)
  - [#logger-templates](#logger-templates)

- 📂 **Settings**
  - [#settings-module](#settings-module)

- 🌐 **External Dependencies**
  - [#external-dependencies](#external-dependencies)

- 📈 **Progress Interfaces**
  - [#progress-interfaces](#progress-interfaces)

- 📦 **Installation**
  - [#installation-scripts](#installation-scripts)

 

<a name="autodocconfig.yml"></a>
**Autodocconfig.yml Structure and Options**

The `autodocconfig.yml` file configures the AutoDocGenerator.  
The YAML structure supports the following top‑level keys:

| Key | Type | Description |
|-----|------|-------------|
| `project_name` | string | Name of the documented project. |
| `language` | string | Code language used for documentation (default: `en`). |
| `ignore_files` | list of strings | Glob patterns of files/folders to exclude from processing (e.g., `*.pyc`, `venv`, `.git`). |
| `project_settings` | mapping | Settings related to logging and caching: <br>`save_logs` (boolean) – whether to keep logs. <br>`log_level` (int) – verbosity level (default 1). |
| `project_additional_info` | mapping | Key‑value pairs of additional metadata that can be referenced inside documentation. |
| `custom_descriptions` | list of strings | Free‑form text blocks that appear in the generated documentation, useful for detailed explanations or usage instructions. |
| `custom_modules` | list (implied via `CustomModule` entries) | Each string is wrapped into a `CustomModule` and included in the doc generation pipeline. |

Example snippet:

```yaml
project_name: "Auto Doc Generator"
language: "en"
project_settings:
  save_logs: true
  log_level: 1
project_additional_info:
  global idea: "This project was created to help developers make documentations for them projects"
custom_descriptions:
  - "explain how install workflow with install.ps1 and install.sh scripts..."
  - "how to use Manager class what parameters i need to give..."
  - "explain how to write autodocconfig.yml file what options are available"
```

These options are parsed in `autodocgenerator/auto_runner/config_reader.py` and populate the `Config` object used during documentation generation. 
<a name="config-classes"></a>
## Config Classes
The Config Reader component defines two main classes: `ProjectConfigSettings` and `Config`.

### ProjectConfigSettings
This class stores project-specific settings, such as log level and save logs flag.

### Config
This class stores general configuration data, including language, project name, and custom modules. 
<a name="config-methods"></a>
## Config Methods
The `Config` class defines several methods for setting and getting configuration data.

### set_language
Sets the language for the configuration.

### set_pcs
Sets the project config settings for the configuration.

### set_project_name
Sets the project name for the configuration.

### add_project_additional_info
Adds additional information to the project configuration.

### add_ignore_file
Adds a file pattern to the ignore list.

### add_custom_module
Adds a custom module to the configuration.

### get_project_settings
Returns the project settings object.

### get_doc_factory
Returns the document factory object. 
<a name="config-usage"></a>
## Config Usage
The `Config` class is used in the `autodocgenerator/auto_runner/run_file.py` module to initialize the configuration data. The `read_config` function is used to parse the YAML configuration file and create a `Config` object. 
<a name="config-reader-component"></a>
## Config Reader Component
The Config Reader component is responsible for parsing configuration data from a YAML file.

### Interactions
This component interacts with the `autodocgenerator/auto_runner/run_file.py` module by providing the parsed configuration data.

### Technical Details
The Config Reader component uses the `yaml` library to load configuration data from a file. It defines two main classes: `ProjectConfigSettings` and `Config`. The `ProjectConfigSettings` class stores project-specific settings, such as log level and save logs flag. The `Config` class stores general configuration data, including language, project name, and custom modules.

### Data Flow
The data flow for this component is as follows:
1. **Input**: YAML configuration file data.
2. **Processing**: The `read_config` function parses the YAML data and creates a `Config` object.
3. **Output**: A `Config` object containing the parsed configuration data.
4. **Side Effects**: The parsed configuration data is used to initialize the `autodocgenerator/auto_runner/run_file.py` module. 
<a name="pyproject-configuration"></a>
## Project Metadata (`pyproject.toml`)

The `pyproject.toml` declares the `autodocgenerator` package:
- **Project** metadata (name, version, description, authors, license, README, Python requirement).  
- **Dependencies** list is comprehensive, including OpenAI, Rich, Pydantic, and a host of utility libraries.  
- **Build system** uses Poetry’s `poetry-core`.

This configuration drives packaging, dependency resolution, and compatibility checks for the library. 
<a name="autodocgenerator/auto_runner/run_file.py"></a><h1>Using the Manager Class</h1>  
The `Manager` class is instantiated with the following parameters (as shown in `run_file.py`):

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_path` | `str` | Path to the root of the project to document |
| `project_settings` | `ProjectSettings` | Settings loaded from the configuration (e.g., file patterns, language) |
| `pcs` | `ProjectConfigSettings` | Project‑specific configuration settings |
| `sync_model` | `GPTModel` | Synchronous GPT model instance (created with `API_KEY`, `use_random=False`) |
| `async_model` | `AsyncGPTModel` | Asynchronous GPT model instance (created with `API_KEY`) |
| `ignore_files` | `list[str]` | List of file paths to ignore during documentation |
| `progress_bar` | `BaseProgress` | Progress display implementation (`ConsoleGtiHubProgress()` in the example) |
| `language` | `str` | Target language for documentation (e.g., `"en"`) |

### Full example of usage

```python
# run_file.py
from autodocgenerator.manage import Manager
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.preprocessor.settings import ProjectSettings
from .config_reader import Config, read_config, ProjectConfigSettings
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.engine.config.config import API_KEY
from autodocgenerator.factory.base_factory import DocFactory

def gen_doc(project_settings: ProjectSettings,
            pcs: ProjectConfigSettings,
            ignore_list: list[str],
            project_path: str,
            doc_factory: DocFactory,
            intro_factory: DocFactory):
    
    # Create GPT models
    sync_model = GPTModel(API_KEY, use_random=False)
    async_model = AsyncGPTModel(API_KEY)
    
    # Instantiate Manager with all required arguments
    manager = Manager(
        project_path,
        project_settings,
        pcs,
        sync_model=sync_model,
        async_model=async_model,
        ignore_files=ignore_list,
        progress_bar=ConsoleGtiHubProgress(),
        language="en"
    )
    
    # Generate documentation
    manager.generate_code_file()
    manager.generate_global_info_file(use_async=False, max_symbols=8000)
    manager.generete_doc_parts(use_async=False, max_symbols=6000)
    manager.factory_generate_doc(doc_factory)
    manager.order_doc()
    manager.factory_generate_doc(intro_factory)
    manager.clear_cache()

    return manager.read_file_by_file_key("output_doc")

if __name__ == "__main__":
    with open("autodocconfig.yml", "r", encoding="utf-8") as file:
        config_data = file.read()
    config: Config = read_config(config_data)

    project_settings = config.get_project_settings()
    doc_factory, intro_factory = config.get_doc_factory()

    output_doc = gen_doc(
        project_settings,
        config.pcs,
        config.ignore_files,
        ".",           # current directory as project path
        doc_factory,
        intro_factory
    )
```

This example demonstrates creating the required GPT models, initializing the `Manager` with all necessary parameters, calling its methods to generate and order documentation, and finally retrieving the output. 
<a name="async-doc-generation"></a>
## Asynchronous Documentation Generation

`async_write_docs_by_parts(part: str, async_model: AsyncModel, global_info: str, semaphore, prev_info: str = None, language: str = "en", update_progress = None) → str`

- Mirrors the synchronous flow but operates within an `asyncio.Semaphore` limiting parallel LLM queries.  
- Calls `async_model.get_answer_without_history`, awaits result, updates progress, and returns cleaned text.

--- 
<a name="sync-doc-generation"></a>
## Synchronous Documentation Generation

`write_docs_by_parts(part_id: int, part: str, model: Model, prev_info: str = None, language: str = "en") → str`

1. **Prompt Construction** – Builds a two‑system‑role prompt containing:  
   * Language instruction (`language`),  
   * The global `BASE_PART_COMPLITE_TEXT` template,  
   * Optional context from `prev_info`.  
   * User role containing the source `part`.
2. **LLM Call** – Invokes `model.get_answer_without_history` with the prompt.  
3. **Post‑processing** – Strips Markdown fences (` ``` `) if present.  
4. **Return** – Cleaned documentation string.

Logging records total length and the raw answer.

--- 
<a name="module-initialization"></a>
## Module Initialization and Logger Provision

The **`autodocgenerator/__init__.py`** file acts as the package entry point.  
It prints a simple identifier (`"ADG"`), imports the public logging classes from `autodocgenerator.ui.logging`, creates a singleton `logger` instance of **`BaseLogger`**, and wires it to a **`BaseLoggerTemplate`** implementation. This makes a ready‑to‑use logger available to every submodule that imports `autodocgenerator`. 
<a name="module-interactions"></a>
## Factory Interaction
* Both `IntroLinks` and `IntroText` are instantiated and executed by a `DocFactory` instance.
* The `generate_doc` method of `DocFactory` iterates over its modules, invoking each `generate` method with a shared `info` dictionary and a synchronous `Model` instance.
* The resulting strings are concatenated to form the final documentation section.

--- 
<a name="interactions"></a>
## Interaction with the Rest of the System

| Component | Role | Data Flow |
|-----------|------|-----------|
| `Model` / `AsyncModel` | LLM backend | Receives prompt → returns Markdown description |
| `BASE_PART_COMPLITE_TEXT` | Prompt template | Pre‑prefixed to every user chunk |
| `BaseLogger` | Logging | Emits status messages for debugging |
| `BaseProgress` | UI progress | Tracks task completion across chunks |
| `engine.config` | Configuration | Supplies `max_symbols` and prompt constants |

The splitters feed into the compressor module, while the doc‑generation functions provide ready‑to‑use Markdown fragments that are later merged or written to disk by higher‑level orchestrators. 
<a name="intro-links-module"></a>
## IntroLinks Module
<blockquote>Responsible for extracting and formatting external HTML link references from a document.</blockquote>

### Class Overview
```python
class IntroLinks(BaseModule):
    def generate(self, info: dict, model: Model):
        …
```
* `BaseModule` provides the standard `generate` contract used by the `DocFactory`.
* The `generate` method receives a dictionary of contextual data and a `Model` instance.

### Core Logic
1. **Link Extraction**  
   `links = get_all_html_links(info.get("full_data"))`  
   Parses the raw document string (`full_data`) for any HTML anchor tags and returns a list of link objects.
2. **Link Presentation**  
   `intro_links = get_links_intro(links, model, info.get("language"))`  
   Uses the model (e.g., GPT) to produce a natural‑language summary of the collected links in the requested language.
3. **Return Value**  
   The formatted link summary string.

### Interaction with External Functions
| Function | Purpose | Source |
|----------|---------|--------|
| `get_all_html_links` | Scans markdown/HTML for `<a>` tags | `postprocessor/custom_intro.py` |
| `get_links_intro` | Generates a text summary of links using the supplied `Model` | `postprocessor/custom_intro.py` |

### Data Flow
| Stage | Input | Output | Side‑Effects |
|-------|-------|--------|--------------|
| 1 | `info["full_data"]` (str) | List of link dictionaries | None |
| 2 | `links`, `model`, `info["language"]` | Introductory link text (str) | None |
| 3 | Return | `intro_links` string | None |

--- 
<a name="intro-text-module"></a>
## IntroText Module
<blockquote>Responsible for generating a concise introduction paragraph for a module or file.</blockquote>

### Class Overview
```python
class IntroText(BaseModule):
    def generate(self, info: dict, model: Model):
        …
```
* Operates within the same factory framework as `IntroLinks`.

### Core Logic
1. **Base Introduction**  
   `intro = get_introdaction(info.get("global_data"), model, info.get("language"))`  
   Sends the global documentation snippet (`global_data`) to the language model to craft a brief intro in the target language.
2. **Return Value**  
   The resulting introductory paragraph.

### Interaction with External Functions
| Function | Purpose | Source |
|----------|---------|--------|
| `get_introdaction` | Uses the supplied `Model` to produce a generic introductory paragraph | `postprocessor/custom_intro.py` |

### Data Flow
| Stage | Input | Output | Side‑Effects |
|-------|-------|--------|--------------|
| 1 | `info["global_data"]` (str), `model`, `info["language"]` | Intro paragraph (str) | None |
| 2 | Return | `intro` string | None |

--- 
<a name="custom-intro-module"></a>  
## CustomIntro Module  
<blockquote>Collects links, creates intro snippets, and produces targeted descriptions using a language model.</blockquote>

### Core Functions  

| Function | Responsibility | Key Steps | Inputs | Outputs |
|----------|----------------|-----------|--------|---------|
| `get_all_html_links` | Scans markdown for `<a name="…">` anchors | Regex `'<a name=[\"']?(.*?)[\"']?</a>'` → `#anchor` list | `data: str` | `list[str]` of link identifiers |
| `get_links_intro` | Generates a summary of those links | Build system/user prompt (`BASE_INTRODACTION_CREATE_TEXT`) → `model.get_answer_without_history` | `links: list[str]`, `model: Model`, `language` | `str` intro with link context |
| `get_introdaction` | Produces a generic module intro | Prompt with `BASE_INTRO_CREATE` → `model.get_answer_without_history` | `global_data: str`, `model: Model`, `language` | `str` paragraph |
| `generete_custom_discription` | Creates a precise technical description for each data chunk | Iterates through `splited_data`; builds a strict instruction prompt; stops when a valid answer is found | `splited_data: str`, `model: Model`, `custom_description: str`, `language` | `str` description or `!noinfo` marker |

**Note:** `generete_custom_discription` contains a typo in the function name; callers should use the exact name.

### Interaction with External Modules  

* **Model** – All prompts are sent to a `Model` instance (e.g., `GPTModel`).  
* **Config** – Uses `BASE_INTRODACTION_CREATE_TEXT` and `BASE_INTRO_CREATE` constants for system messages.  
* **Logging** – `BaseLogger`/`InfoLog` track extraction and generation steps.  

### Data Flow Summary  

```text
raw markdown → get_all_html_links → link list → get_links_intro → intro string
global doc   → get_introdaction → module intro
section data → generete_custom_discription → concise description
```

--- 
<a name="runtime-interaction"></a>
## Runtime Interaction with Submodules

- **Import side‑effect**: Importing `autodocgenerator` triggers the logger setup, so downstream modules can call `autodocgenerator.logger.info(...)` without additional configuration.  
- **Dependency exposure**: The exported names (`BaseLogger`, `BaseLoggerTemplate`, `InfoLog`, `ErrorLog`, `WarningLog`) are re‑exported, allowing external code to subclass or customise the logging behavior while still sharing the same logger instance. 
<a name="data-flow"></a>
## Data Flow and Side Effects

1. **Input**: Import of the package (no external parameters).  
2. **Processing**: Instantiation of `BaseLogger`; template binding via `set_logger`.  
3. **Output**: A configured `logger` object available as `autodocgenerator.logger`.  
4. **Side Effects**: Console output of `"ADG"` and registration of logging handlers that affect any subsequent log calls across the codebase. 
<a name="data-flow-diagram"></a>
## Data Flow Summary

```
[Source Code Strings] → [compressor module] → (sync or async) →
  ├─ build prompts (project settings + base templates)
  ├─ send to Model → Model output
  └─ aggregate into chunks → [Final Compressed String]

[Code Snippets] → [generate_descriptions_for_code] → 
  ├─ build “Describe this code” prompt
  ├─ send to Model
  └─ collect Markdown descriptions

[Large Text] → [spliter.split_data] → list of manageable chunks
```

The resulting data can be fed into downstream components such as the `autodocgenerator.engine` pipeline or persisted to disk.

--- 
<a name="asyncgptmodel-class"></a>
## AsyncGPTModel Class
*Responsible for*  
Provides an asynchronous LLM wrapper that iteratively tries each model name in `regen_models_name`. It logs progress, handles failures by cycling through the list, and raises `ModelExhaustedException` when all attempts fail.

*Key methods*  
- `generate_answer(with_history=True, prompt=None)` –  
  * Builds the conversation payload from `self.history` or a supplied prompt.  
  * Enters a retry loop: picks the current model, calls `AsyncGroq.chat.completions.create`.  
  * On success returns the content of the first choice.  
  * On exception logs a warning, moves to the next model index, and retries.  

*Interactions*  
Relies on `BaseLogger` for `InfoLog`, `WarningLog`, and `ErrorLog`. Uses `ModelExhaustedException` to signal no remaining models. The `client` is an `AsyncGroq` instance initialized with `API_KEY`.

*Data flow*  
Inputs: `with_history`, optional `prompt`.  
Outputs: a string answer.  
Side‑effects: updates internal history, logs status, potentially raises an exception.

--- 
<a name="gptmodel-class"></a>
## GPTModel Class
*Responsible for*  
Synchronous counterpart to `AsyncGPTModel`, executing the same retry logic via `Groq`.

*Key methods*  
- `generate_answer(with_history=True, prompt=None)` – identical flow to the async version but uses `Groq.chat.completions.create`.  

*Interactions*  
Same logger and exception handling as `AsyncGPTModel`. Uses the shared `regen_models_name` list from `ParentModel`.

*Data flow*  
Same as the async class, but returns the answer synchronously.  

Both classes inherit `current_model_index` and `regen_models_name` from `ParentModel`, which randomizes the model order if `use_random=True`. 
<a name="model‑dependency"></a>
## Model Dependency
* Requires a concrete `Model` implementation (e.g., `GPTModel`) to perform natural‑language generation.
* The model object is passed directly to the helper functions; these functions internally manage retry logic, logging, and potential exception propagation (see `AsyncGPTModel`/`GPTModel` documentation).

--- 
<a name="pipeline-assembly"></a>
## Part‑by‑Part Pipeline

`gen_doc_parts(full_code_mix, global_info, max_symbols, model: Model, language, progress_bar: BaseProgress) → str`

- **Splitting** – Calls `split_data` to produce `splited_data`.  
- **Sub‑task** – Uses `progress_bar` to track per‑chunk progress.  
- **Iteration** – For each chunk:
  * Calls `write_docs_by_parts` with `prev_info` set to the last 3000 characters of the previous result (caching strategy).
  * Concatenates results, separated by two newlines.
  * Updates progress.
- **Result** – Full documentation string for the entire source.

---

`async_gen_doc_parts(full_code_mix, global_info, max_symbols, model: AsyncModel, language, progress_bar: BaseProgress) → str`

- Executes the same logic as `gen_doc_parts` but launches a separate coroutine per chunk, limited by a semaphore of 4.  
- Gathers results with `asyncio.gather`, stitches them, and reports aggregated length.

--- 
<a name="sorting-module"></a>  
## Sorting Module  
<blockquote>Organizes document sections by semantic title order using the model.</blockquote>

### Key Functions  

| Function | Responsibility | Flow |
|----------|----------------|------|
| `extract_links_from_start` | Pulls anchor names from the start of a chunk | Regex `^<a name=[\"']?(.*?)[\"']?</a>` → `#anchor` |
| `split_text_by_anchors` | Splits a document into chunks based on anchors | Regex split on look‑ahead `(?=<a name=…)`; validates link‑chunk count; returns `dict[anchor, chunk]` |
| `get_order` | Orders chunks according to model output | Sends title list to model; receives comma‑separated titles; concatenates corresponding chunks in that order |

### Interaction with Model and Logging  

* `get_order` logs start/end and passes a single user prompt that asks the model to sort titles.  
* Uses `Model.get_answer_without_history` for all LLM calls.  

### Data Flow  

```text
full_text → split_text_by_anchors → {anchor: chunk}
chunk_dict → get_order → ordered_text
```

--- 
<a name="compressor-module"></a>
## autodocgenerator.preprocessor.compressor

The *compressor* module orchestrates the chunking and compression of source‑code strings before they are fed to a language model. It supports both synchronous and asynchronous pathways, allowing multiple files to be compressed in parallel while preserving the overall order of the original payload.

### Key Responsibilities

| Function | Purpose |
|----------|---------|
| `compress` | Sends a single string to a *Model* and returns the model’s response. The prompt is built from a project‑specific template and a base compression text. |
| `compress_and_compare` | Aggregates a list of strings into “compare‑chunks” by iteratively compressing groups of *compress_power* elements. It updates a progress bar and returns a list of compressed strings. |
| `async_compress` | Asynchronously compresses a single string using a semaphore to throttle concurrency. |
| `async_compress_and_compare` | Parallelizes `async_compress` over a data list, then stitches the results back into chunks. |
| `compress_to_one` | Iteratively reduces a list of strings to a single compressed representation, toggling between sync and async pipelines. |
| `generate_descriptions_for_code` | Builds a detailed LLM prompt for each code snippet to obtain human‑readable documentation; collects all generated descriptions. |

### Interaction with the Rest of the System

* **Model**: All compression functions expect a `Model` or `AsyncModel` instance that implements `get_answer_without_history`. This interface is defined in `engine.models.gpt_model`.  
* **Project Settings**: `ProjectSettings` supplies the base prompt and any additional key/value metadata via its `prompt` property.  
* **Progress Reporting**: A `BaseProgress` instance tracks subtasks and updates. If none is supplied, the default `BaseProgress()` creates a no‑op logger.  
* **Logging**: The module currently does not emit logs itself; logging is handled in other parts of the pipeline.

### Detailed Flow

```text
compress(data, project_settings, model, power)
 └─ build 3‑role prompt
 └─ model.get_answer_without_history(prompt)
 └─ return answer

compress_and_compare(data, model, project_settings, power, progress)
 └─ create sub‑task (len(data))
 └─ for each element:
     • determine chunk index = i // power
     • accumulate compressed chunk string
     • update progress
 └─ finish sub‑task
 └─ return list of chunk strings
```

```text
async_compress(data, project_settings, async_model, power, semaphore, progress)
 └─ acquire semaphore
 └─ build prompt (identical to sync)
 └─ await async_model.get_answer_without_history(prompt)
 └─ progress.update_task()
 └─ return answer

async_compress_and_compare(data, async_model, project_settings, power, progress)
 └─ semaphore(4)
 └─ launch async_compress for each element
 └─ gather all responses
 └─ regroup into chunks of size `power`
 └─ finish sub‑task
 └─ return list of chunk strings
```

```text
compress_to_one(data, model, settings, power, use_async, progress)
 └─ loop until only one element remains:
     • if len(data) < power + 1 → new_power = 2
     • compress_and_compare (sync or async) → new data
     • increment iteration counter
 └─ return single string (data[0])
```

```text
generate_descriptions_for_code(data, model, settings, progress)
 └─ sub‑task for all code snippets
 └─ for each code snippet:
     • craft a “Describe this code” prompt (instructions + raw code)
     • answer = model.get_answer_without_history(prompt)
     • append to `describtions`
     • progress.update_task()
 └─ finish sub‑task
 └─ return list of description strings
```

### Important Notes

* `compress_power` defaults to 4 but is automatically reduced to 2 when the remaining list is too small.  
* All prompts are built from `BASE_SETTINGS_PROMPT` and a power‑dependent base compression string obtained via `get_BASE_COMPRESS_TEXT`.  
* The module intentionally ignores any I/O; it works purely on in‑memory strings. 
<a name="spliter-module"></a>
## Data Splitting Logic

`split_data(data: str, max_symbols: int) → list[str]`

- **Purpose** – Break a large source‑code string into chunks that respect the token budget of the LLM.  
- **Algorithm**  
  1. **Initial Split** – `data` is first split on a file‑boundary marker (e.g. `<|`) producing `splited_by_files`.  
  2. **Recursive Oversize Correction** – In a loop, any segment exceeding `max_symbols * 1.5` is bisected in half and re‑inserted next to the original.  
     ```text
     el[i][:max_symbols/2]  ──► new chunk
     el[i][max_symbols/2:]  ──► insert after
     ```
  3. **Re‑aggregation** – Chunks are concatenated until the combined length would exceed `max_symbols * 1.25`; at that point a new slot in `split_objects` is started.  
  4. **Result** – Returns a list of strings, each ≤ ~1.25×`max_symbols`, ready for compression or prompt building.

- **Side effects** – Logs each major step through `BaseLogger`.  
- **Assumptions** – `data` contains the `<|` delimiter; `max_symbols` is a conservative upper bound for LLM input size.

--- 
<a name="model-exception-handling"></a>
## Model Exception Handling
The `ModelExhaustedException` class is a custom exception that is raised when none of the models in the `MODELS_NAME` list are available for use.

### Exception Details
This exception is a subclass of the built-in `Exception` class, providing a specific error message when all models are exhausted.

### Interactions
The `ModelExhaustedException` class interacts with the rest of the system by being raised when the model availability check fails. This exception is likely handled by a try-except block in the main code, allowing for a graceful error handling mechanism.

### Technical Details
The `ModelExhaustedException` class has a docstring that provides a brief description of the exception. The `...` in the class definition is a placeholder for the actual implementation of the exception.

### Data Flow
The `ModelExhaustedException` class takes no inputs and produces no outputs. However, it has a side effect of interrupting the normal execution of the program when raised, allowing for error handling and potential recovery mechanisms to be implemented.

```python
# Real-world usage based on the code above
try:
    # Model availability check
    if not any(model_available(model) for model in MODELS_NAME):
        raise ModelExhaustedException("No models available for use.")
except ModelExhaustedException as e:
    print(f"Error: {e}")
``` 
None 
<a name="error-handling-and-logging"></a>  
## Error Handling & Logging  
Both modules rely on `BaseLogger` for status messages. Exceptions from the model or regex operations propagate upward; the caller (DocFactory) is responsible for catching and reacting. Logging levels: `0` – standard, `1` – verbose, `2` – detailed.  

--- 
<a name="base-log-classes"></a>
## Base Log Hierarchy

`BaseLog` is a lightweight log object that captures a message and a severity level.  
- **Constructor** stores the supplied message and integer level.  
- `_log_prefix` generates a UTC timestamp string (`[YYYY‑MM‑DD HH:MM:SS]`).  
- `format()` simply returns the message; overridden in subclasses.

Derived classes inject severity markers:
| Class | Format Output |
|------|---------------|
| `ErrorLog` | `"[timestamp] [ERROR] message"` |
| `WarningLog` | `"[timestamp] [WARNING] message"` |
| `InfoLog` | `"[timestamp] [INFO] message"` |

These classes are used throughout the project to create typed log entries that are later routed to a logger template.

--- 
<a name="logger-templates"></a>
## Logger Template System

`BaseLoggerTemplate` provides a pluggable interface for dispatching log messages.  
- `log()` writes the formatted entry to the chosen destination (console by default).  
- `global_log()` applies a global log level filter: if `log_level < 0` or `log_level >= entry.level`, the entry is forwarded to `log()`.

`FileLoggerTemplate` extends `BaseLoggerTemplate` to append each formatted line to a file specified at construction.  It overrides `log()` to open the file in append mode, ensuring atomic writes per entry.

`BaseLogger` is a **singleton** that holds a reference to a concrete `BaseLoggerTemplate`.  
- `set_logger()` swaps the underlying template.  
- `log()` forwards the `BaseLog` instance to the template’s `global_log()`.

This design decouples log generation from output, allowing console, file, or future transports without changing the code that creates logs.

--- 
<a name="settings-module"></a>
## autodocgenerator.preprocessor.settings

`ProjectSettings` centralises all project‑specific metadata that influences prompt generation. The class exposes a mutable `info` dictionary and exposes a read‑only `prompt` property that concatenates a global template with the current state.

### Responsibilities

* Store the project name and arbitrary key/value pairs.  
* Generate a prompt string that can be injected as the system role in subsequent LLM requests.

### Core API

| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__(project_name: str)` | Create a new settings instance. |
| `add_info(key, value)` | Store a custom piece of information. |
| `prompt` | Property that returns a single string:  
  * `BASE_SETTINGS_PROMPT` from configuration.  
  * `Project Name: …` line.  
  * One line per `info` entry in insertion order. |

### Interaction

The `prompt` property is consumed by `compress` and `generate_descriptions_for_code` to prepend project‑level context to every LLM request. 
<a name="external-dependencies"></a>
## External Dependencies

| Module | Purpose | Notes |
|--------|---------|-------|
| `engine.models.gpt_model` | Provides `Model`, `AsyncModel`, and concrete implementations. | Must expose `get_answer_without_history`. |
| `engine.config.config` | Supplies `BASE_SETTINGS_PROMPT`, `BASE_PART_COMPLITE_TEXT`, and `get_BASE_COMPRESS_TEXT`. | Text templates for prompts. |
| `ui.progress_base` | `BaseProgress` tracks asynchronous task progress. | Default instance is a no‑op stub. |
| `ui.logging` | Optional logging via `BaseLogger`, `InfoLog`, etc. | Not directly used in this snippet. |
| `asyncio`, `math`, `fnmatch`, `pathlib` | Standard library utilities. | `fnmatch` used in other modules for file filtering. |

--- 
<a name="progress-interfaces"></a>
## Progress Tracking Interface

`BaseProgress` declares abstract methods for sub‑task creation, updates, and removal.  
Concrete implementations:

- `LibProgress` wraps `rich.progress.Progress`.  
  - `create_new_subtask(name, total_len)` registers a sub‑task.  
  - `update_task()` advances the current sub‑task or the base task if none exists.  
  - `remove_subtask()` clears the current sub‑task reference.

- `ConsoleTask` is a simple progress printer that logs percentage completion to the console.

- `ConsoleGtiHubProgress` mixes both: it keeps a general `ConsoleTask` for overall progress and spawns a new `ConsoleTask` for specific subtasks when requested.

These classes enable flexible progress reporting across CLI and GitHub Actions environments.

--- 
<a name="installation-scripts"></a>
## GitHub Actions Bootstrap

Both `install.ps1` (PowerShell) and `install.sh` (Bash) automate the creation of a reusable GitHub workflow file (`autodoc.yml`) and a configuration file (`autodocconfig.yml`) in the current repository.

Key points:
- The workflow file references a reusable workflow from the `ADG` repository and injects the `GROCK_API_KEY` secret.  
- `autodocconfig.yml` records the repository’s base name as `project_name` and defaults the documentation language to `"en"`.  
- Scripts ensure directories exist and use here‑strings or `cat <<EOF` for file generation, handling shell variable expansion correctly.

These scripts are entry points for users who wish to integrate automatic documentation generation into their CI pipeline.

--- 
