## Executive Navigation Tree
- ⚙️ Configuration
  - [configuration-loading-logic](#configuration-loading-logic)
  - [projectconfigsettings-structure](#projectconfigsettings-structure)
  - [config-builder-methods](#config-builder-methods)
  - [read_config-function-flow](#read_config-function-flow)
  - [environment-variable-loading](#environment-variable-loading)
  - [project‑settings‑builder](#project‑settings‑builder)
  - [installation‑scripts‑workflow‑generation](#installation‑scripts‑workflow‑generation)
  - [project‑metadata‑pyproject‑toml](#project‑metadata‑pyproject‑toml)

- 🤖 Model Management
  - [model-name-registry](#model-name-registry)
  - [base-text-generators](#base-text-generators)
  - [model-rotation-initialisation](#model-rotation-initialisation)
  - [synchronous-model-interface](#synchronous-model-interface)
  - [asynchronous-model-interface](#asynchronous-model-interface)

- 📊 Data Processing
  - [module‑interactions](#module‑interactions)
  - [data‑flow‑summary](#data‑flow‑summary)
  - [history-management](#history-management)
  - [semantic-section-sorting](#semantic-section-sorting)

- 🌐 HTML
  - [html-link-extractor](#html-link-extractor)

- 📦 Packaging
  - [repository‑content‑packer](#repository‑content‑packer)
  - [compressor‑pipeline](#compressor‑pipeline)
  - [split‑and‑doc‑generation](#split‑and‑doc‑generation)

- 🪵 Logging
  - [logging‑hierarchy](#logging‑hierarchy)
  - [logger‑template‑selection](#logger‑template‑selection)
  - [singleton‑logger‑facade](#singleton‑logger‑facade)
  - [progress‑abstraction](#progress‑abstraction)

- ❓ Misc
  - […](#…)

 

<a href="autodocconfig.yml"></a>To install the project, run the appropriate script for your platform:  

- **Windows (PowerShell)**:  
  ```powershell
  irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
  ```  

- **Linux/macOS (bash)**:  
  ```bash
  curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
  ```  

Additionally, add a secret variable named **`GROCK_API_KEY`** to your GitHub Actions workflow, containing your API key from the Grock documentation (https://grockdocs.com). This secret is required for the documentation generation step to work.

<a href="autodocgenerator/auto_runner/run_file.py"></a>
To use the **Manager** class you must provide the following parameters when creating an instance:

| Parameter | Description |
|-----------|-------------|
| `project_path` | Root directory of the project you want to document. |
| `project_settings` | An instance of **ProjectSettings** (obtained from the config). |
| `pcs` | An instance of **ProjectConfigSettings** (also from the config). |
| `sync_model` | A synchronous **GPTModel** object (e.g., `GPTModel(API_KEY, use_random=False)`). |
| `async_model` | An asynchronous **AsyncGPTModel** object (e.g., `AsyncGPTModel(API_KEY)`). |
| `ignore_files` | List of file names / paths that should be excluded from processing. |
| `progress_bar` | An implementation of a progress UI, such as **ConsoleGtiHubProgress()**. |
| `language` | Language code for the generated documentation (e.g., `"en"`). |

### Full example of usage

```python
from autodocgenerator.manage import Manager
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.preprocessor.settings import ProjectSettings
from autodocgenerator.auto_runner.config_reader import Config, read_config

# 1. Load configuration (example uses a YAML file)
with open("autodocconfig.yml", "r", encoding="utf-8") as file:
    config_data = file.read()
config: Config = read_config(config_data)

# 2. Extract required objects from the config
project_settings: ProjectSettings = config.get_project_settings()
project_config_settings = config.pcs          # ProjectConfigSettings instance
ignore_list = config.ignore_files             # List of files to ignore

# 3. Create GPT model instances
sync_model = GPTModel(API_KEY, use_random=False)
async_model = AsyncGPTModel(API_KEY)

# 4. Instantiate the Manager with all required arguments
manager = Manager(
    project_path=".",                 # current directory or any project root
    project_settings=project_settings,
    pcs=project_config_settings,
    sync_model=sync_model,
    async_model=async_model,
    ignore_files=ignore_list,
    progress_bar=ConsoleGtiHubProgress(),
    language="en"
)

# 5. Run the documentation generation workflow
manager.generate_code_file()
manager.generate_global_info_file(use_async=False, max_symbols=8000)
manager.generete_doc_parts(use_async=False, max_symbols=10000)
# … add any additional Manager method calls as needed …
manager.clear_cache()

# 6. Retrieve the final document
final_doc = manager.read_file_by_file_key("output_doc")
print(final_doc)
```

This example demonstrates the complete setup: loading configuration, creating model instances, constructing the **Manager**, invoking its processing methods, and finally retrieving the generated documentation.

<a href="autodocconfig.yml"></a>
The **autodocconfig.yml** file defines the configuration for the documentation generator. The available top‑level keys are:

- **project_name** – a string with the name of the project.  
- **language** – language code (e.g., `"en"`).  
- **project_settings** – a map of settings for the generator:
  - **save_logs** – boolean, whether to save generation logs.  
  - **log_level** – integer, logging verbosity (e.g., `2`).  
- **project_additional_info** – a map of arbitrary key/value pairs that will be added to the generated documentation (e.g., `"global idea"`).  
- **custom_descriptions** – a list of strings, each describing a custom module or documentation section to be included.  
- **ignore_files** – (optional) a list of glob patterns for files/directories that should be excluded from processing.  

When writing the file, use standard YAML syntax, for example:

```yaml
project_name: "My Project"
language: "en"
project_settings:
  save_logs: true
  log_level: 2
project_additional_info:
  global idea: "Brief description of the project"
custom_descriptions:
  - "First custom description"
  - "Second custom description"
ignore_files:
  - "*.tmp"
  - "tests/"
```

These keys are read by `autodocgenerator.auto_runner.config_reader.read_config` and applied during documentation generation.

 

<a name="configuration-loading-logic"></a>  
## Configuration Loading Logic  

The module parses **autodocconfig.yml**, turning raw YAML into a fully‑featured `Config` object used by the auto‑doc runner.  

<a name="projectconfigsettings-structure"></a>  
## `ProjectConfigSettings` Structure  

- Attributes `save_logs` and `log_level` default to `False`/`-1`.  
- `load_settings(data: dict)` iterates over the supplied dictionary and sets matching attributes via `setattr`, allowing any future setting to be added without code changes.  

<a name="config-builder-methods"></a>  
## `Config` Builder Methods  

| Method | Purpose | Returns |
|--------|---------|---------|
| `set_language(str)` | Override default language (`en`). | `self` |
| `set_pcs(ProjectConfigSettings)` | Attach processed project‑level settings. | `self` |
| `set_project_name(str)` | Store human‑readable project name. | `self` |
| `add_project_additional_info(key, value)` | Populate free‑form metadata for `ProjectSettings`. | `self` |
| `add_ignore_file(pattern)` | Extend the default ignore list for file scanning. | `self` |
| `add_custom_module(CustomModule)` | Register a user‑provided description that will become a custom doc module. | `self` |
| `get_project_settings()` | Build a `ProjectSettings` instance, injecting additional info. | `ProjectSettings` |
| `get_doc_factory()` | Assemble the primary documentation factory and an optional intro factory. | `(DocFactory, DocFactory)` |

<a name="read_config-function-flow"></a>  
## `read_config(file_data: str) → Config` Flow  

1. **YAML Deserialization** – `yaml.safe_load` converts the file string into a dict.  
2. **Base Config Instantiation** – a fresh `Config` object is created.  
3. **Core Fields** – `ignore_files`, `language`, `project_name`, and `project_additional_info` are extracted and applied via the builder methods.  
4. **Project Settings** – a `ProjectConfigSettings` instance receives `project_settings` and is attached with `set_pcs`.  
5. **Custom Descriptions** – each entry in `custom_descriptions` becomes a `CustomModule` added to `custom_modules`.  
6. **Return** – the fully‑populated `Config` ready for consumption by the runner.  

**Data Flow:** Input = raw YAML string; Output = configured `Config` object; Side‑effects = none (pure transformation). The function assumes well‑formed YAML and that any unknown keys are harmlessly ignored by the builder pattern.

<a name="environment-variable-loading"></a>
## Environment Variable Loading  

The module imports **os** and **dotenv**, invokes `load_dotenv()` and extracts `API_KEY` from the process environment. If the key is missing, an exception aborts execution, ensuring that downstream model classes always have a valid credential.

<a name="model-name-registry"></a>
## Model Name Registry  

`MODELS_NAME` is a constant list of three model identifiers. It is referenced by the GPT model factories to populate the `regen_models_name` rotation pool, enabling automatic fallback when a model fails.

<a name="base-text-generators"></a>
## Base Text Generators  

`get_BASE_COMPRESS_TEXT(start, power)` builds a formatted multi‑line string that describes a compression‑style documentation request. The returned template embeds the `start` and `int(start/power)` values, allowing callers to customise the length constraints dynamically.

<a name="module‑interactions"></a>
## Module Interactions  

- The environment loader supplies `API_KEY` to **autodocgenerator.engine.models.gpt_model** via the default argument of its constructors.  
- `MODELS_NAME` is consumed by the model classes to initialise the fallback model queue.  
- `get_BASE_COMPRESS_TEXT` is used by higher‑level documentation generators to produce concise summaries before emitting usage examples.

<a name="data‑flow‑summary"></a>
## Data‑Flow Summary  

**Inputs:** OS environment, integer parameters `start` and `power`.  
**Outputs:** `API_KEY` (global variable), `MODELS_NAME` list, and a formatted string from `get_BASE_COMPRESS_TEXT`.  
**Side‑effects:** Loading of `.env` file; raising an exception on missing API key; no mutation of external state beyond these globals.

<a name="history-management"></a>
## History Management  

`History` builds a per‑session message log.  
- **Constructor** (`system_prompt`) seeds the log with a *system* entry containing `BASE_SYSTEM_TEXT`.  
- **add_to_history(role, content)** appends a dict `{"role":…, "content":…}` to `self.history`.  
The object is injected into every model instance, enabling prompt stitching for chat‑style APIs.

<a name="model-rotation-initialisation"></a>
## Model Rotation Initialisation  

`ParentModel.__init__(api_key=API_KEY, history=History(), use_random=True)`  
1. Stores the supplied `api_key` and `history`.  
2. Copies `MODELS_NAME` (list of model identifiers) to `models_copy`.  
3. If `use_random` is true, shuffles the copy, producing a **fallback queue** saved as `self.regen_models_name`.  
This queue drives automatic model fallback when a request fails.

<a name="synchronous-model-interface"></a>
## Synchronous Model Interface  

`Model` inherits `ParentModel` and provides:  
- `generate_answer(... )` → placeholder `"answer"` (real implementation overridden elsewhere).  
- `get_answer(prompt)` records the user prompt, calls `generate_answer`, stores the assistant reply, and returns it.  
- `get_answer_without_history(prompt)` bypasses history.

<a name="asynchronous-model-interface"></a>
## Asynchronous Model Interface  

`AsyncModel` mirrors `Model` with `async` methods: `generate_answer`, `get_answer`, and `get_answer_without_history`, preserving the same history handling but allowing non‑blocking calls.

**Data Flow**  
- **Inputs:** `BASE_SYSTEM_TEXT`, environment‑provided `API_KEY`, `MODELS_NAME`, optional `start`/`power` from callers.  
- **Outputs:** `self.history` (populated log), `self.regen_models_name` (shuffled fallback list), and generated answer strings.  
- **Side‑effects:** Global env load via `config.config`; no external mutation beyond the created globals.

<a name="html-link-extractor"></a>
## HTML Link Extraction Utility (`custom_intro.py`)

**Responsibility** – Scans generated markdown for `<a name="…"></a>` anchors, builds a list of fragment identifiers, and uses a `Model` to synth‑esize introductions that reference those links.  

**Key Functions**  
- `get_all_html_links(data: str) → list[str]` – regex‑searches `data`, logs progress, returns `["#anchor"]` entries.  
- `get_links_intro(links, model, language="en") → str` – builds a three‑message system/user prompt (`BASE_INTRODACTION_CREATE_TEXT`), calls `model.get_answer_without_history`, returns the generated intro.  
- `get_introdaction(global_data, model, language="en") → str` – similar prompt but uses `BASE_INTRO_CREATE`.  
- `generete_custom_discription(splited_data, model, custom_description, language="en") → str` – iterates over code chunks, asks the model to produce a title/link pair respecting strict “no‑invent” rules; stops on the first non‑empty result.  

**Interactions** – Relies on `Model` (synchronous) for LLM calls; logging through `BaseLogger`. No external state is mutated besides the returned strings.  

**Data Flow**  
- **Input:** raw markdown (`data`), list of links, optional language.  
- **Output:** list of anchor hashes, generated introductory text, or a formatted title/link string.  
- **Side‑effects:** console‑level logs; model‑side history is bypassed (`get_answer_without_history`).  

---

<a name="semantic-section-sorting"></a>
## Semantic Section Sorting (`sorting.py`)

**Responsibility** – Parses a document split by HTML anchors, validates one‑to‑one anchor‑chunk mapping, then asks the LLM to return a comma‑separated ordering of titles.  

**Core Logic**  
1. `split_text_by_anchors(text)` – regex split on `<a name…></a>`, builds `dict[anchor → chunk]`. Returns `None` if counts mismatch.  
2. `get_order(model, chanks)` – logs start, sends a user prompt asking for semantic ordering, receives CSV, reassembles ordered text using the original chunk map.  

**Interactions** – Consumes a `Model` instance for the ordering request; uses `BaseLogger` for traceability.  

**Data Flow**  
- **Input:** full documentation string, `Model`.  
- **Output:** concatenated text ordered per LLM suggestion.  
- **Side‑effects:** logs at levels 0‑2; no file I/O.  

---

<a name="repository‑content‑packer"></a>
## Repository Content Packager (`code_mix.py`)

**Responsibility** – Walks a source tree, filters paths by `ignore_patterns`, and writes a single text file containing a tree view followed by the raw content of each non‑ignored file.  

**Main Class** – `CodeMix`  
- `should_ignore(path)` – resolves relative path, checks against glob patterns (`fnmatch`).  
- `build_repo_content(output_file)` – writes “Repository Structure” header, iterates `Path.rglob("*")` to emit indented tree lines, then writes each file wrapped in `<file path="…">` tags. Errors are captured inline.  

**Interactions** – Uses `BaseLogger` for per‑file logs; no external services.  

**Data Flow**  
- **Input:** root directory, optional ignore list.  
- **Output:** `output_file` (e.g., `codemix.txt`) containing a printable repository map and source snippets.  
- **Side‑effects:** filesystem write, console logging, possible read‑error messages embedded in output.

<a name="compressor‑pipeline"></a>
## Compressor Pipeline (`compressor.py`)

**Responsibility** – Reduces raw markdown/code chunks by prompting an LLM with a project‑specific system prompt and a size‑controlled compress prompt. Provides synchronous (`compress`, `compress_and_compare`) and asynchronous (`async_compress`, `async_compress_and_compare`, `compress_to_one`) workflows that batch‑merge *compress_power* chunks and report progress via `BaseProgress`.

**Interactions** – Calls `model.get_answer_without_history` (or its async counterpart) for every chunk; logs through `BaseLogger`. No external state is altered except the returned concatenated strings.

**Data Flow**  
- *Input*: `data` (str or list of str), `ProjectSettings`, `Model`, numeric `compress_power`.  
- *Output*: compressed string (single or list) ready for downstream comparison.  
- *Side‑effects*: progress‑bar updates, console logs.



<a name="project‑settings‑builder"></a>
## Project Settings Builder (`settings.py`)

**Responsibility** – Holds minimal project metadata and assembles the system prompt used by the compressor and other pre‑processors.

**Key API**  
- `ProjectSettings(project_name)` – creates container.  
- `add_info(key, value)` – injects arbitrary key/value pairs.  
- `prompt` property – concatenates `BASE_SETTINGS_PROMPT` with project name and all added entries, yielding the final system prompt string.

**Interactions** – Consumed by `compressor.py` and other modules; pure data object, no I/O.



<a name="split‑and‑doc‑generation"></a>
## Split & Documentation Generation (`spliter.py`)

**Responsibility** – Breaks a large source dump into size‑bounded parts (`split_data`) and drives LLM‑based documentation creation per part, both synchronously (`write_docs_by_parts`, `gen_doc_parts`) and asynchronously (`async_write_docs_by_parts`, `async_gen_doc_parts`).

**Technical Flow**  
1. `split_data` → iteratively halves oversized sections, then packs lines into chunks ≤ `max_symbols`.  
2. `write_docs_by_parts` → builds a multi‑role prompt (`BASE_PART_COMPLITE_TEXT` + optional prior part) and strips surrounding markdown fences.  
3. `gen_doc_parts` → iterates over split chunks, concatenates results, trims the tail for context reuse, and updates a `BaseProgress` sub‑task.  
4. Async equivalents use a semaphore (max 4 concurrent calls) and `await` the model.

**Data Flow**  
- *Input*: full code‑mix string, `max_symbols`, `Model`/`AsyncModel`, optional `global_info`, language tag.  
- *Output*: single assembled documentation string.  
- *Side‑effects*: progress‑bar manipulation, detailed logs (`InfoLog`) at levels 0‑2.

<a name="logging‑hierarchy"></a>
## Logging hierarchy and formatting  

`BaseLog` stores a raw message and a numeric severity. Sub‑classes (`ErrorLog`, `WarningLog`, `InfoLog`) prepend a timestamp (`[YYYY‑MM‑DD HH:MM:SS]`) and a level tag (`[ERROR]`, `[WARNING]`, `[INFO]`). The `format()` method returns the final string for output.

<a name="logger‑template‑selection"></a>
## Logger template selection  

`BaseLoggerTemplate` implements a configurable `log_level`. Its `global_log()` forwards a log entry to `log()` only when the entry’s level is ≤ the configured threshold (or when the threshold is negative, meaning “log everything”). `FileLoggerTemplate` overrides `log()` to append formatted lines to a file, while the base implementation writes to stdout.

<a name="singleton‑logger‑facade"></a>
## Singleton logger façade  

`BaseLogger.__new__` enforces a single shared instance (`BaseLogger.instance`). The façade holds a `logger_template` set via `set_logger()`. Calls to `log()` are delegated to the template’s `global_log()`, allowing the rest of the codebase to log without caring about the concrete sink.

<a name="progress‑abstraction"></a>
## Progress abstraction – rich vs console  

`BaseProgress` defines the public API (`create_new_subtask`, `update_task`, `remove_subtask`).  
- `LibProgress` wraps **rich.progress.Progress**, creating a base task (“General progress”) and optional sub‑tasks. `update_task()` advances the current sub‑task if present, otherwise the base task.  
- `ConsoleGtiHubProgress` mimics the same API with plain `print()` statements via `ConsoleTask`, useful when `rich` is unavailable.

<a name="installation‑scripts‑workflow‑generation"></a>
## Installation scripts – workflow file generation  

`install.ps1` (PowerShell) and `install.sh` (Bash) both create `.github/workflows/autodoc.yml` and `autodocconfig.yml`. They ensure the target directory exists, write a minimal GitHub Actions workflow that references the reusable workflow in the `Drag-GameStudio/ADG` repository, and inject the current project name into the config file. The scripts finish with a green‑colored success message.

<a name="project‑metadata‑pyproject‑toml"></a>
## Project metadata in **pyproject.toml**  

The `[project]` table declares the package name (`autodocgenerator`), version, description, author, license, and required Python version (`>=3.11,<4.0`). `dependencies` list all runtime libraries (e.g., `rich`, `openai`, `google‑genai`). The `[build‑system]` section pins Poetry as the build backend. This file is the single source of truth for packaging and dependency resolution.

