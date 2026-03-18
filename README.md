# Auto‑Doc Generator  
*A layered, factory‑based, LLM‑driven Markdown documentation pipeline for any codebase.*

---

## 1. Project Title  
**Auto‑Doc Generator – Layered + Factory + LLM‑Driven**

---

## 2. Project Goal  
To automatically produce a complete, readable README (or other Markdown artifacts) from the source code of a repository.  
The tool parses the code, chunks it to stay within token limits, sends those fragments to a large‑language model (Groq or OpenAI), formats the generated text with reusable modules, and stitches the result into a single cohesive document. The solution is CI‑friendly and can be invoked from a local CLI or a GitHub Action.

---

## 3. Core Logic & Principles  

### 3.1 Pipeline Overview  

| Phase | Action | Key Components |
|-------|--------|----------------|
| **Configuration** | Read `autodocconfig.yml` → `Config`, `StructureSettings`, custom‑module lists | `auto_runner/config_reader.py` |
| **Entry Point** | `run_file.__main__` calls `gen_doc(project_path, …)` | `auto_runner/run_file.py` |
| **Repository Walk** | Scan files, split code into manageable chunks | `manage.py` (preprocessor `spliter.py`, `compressor.py`) |
| **LLM Interaction** | Submit chunks to `GPTModel` (rotating keys, history, logging) | `engine/models/gpt_model.py`, `engine/config/config.py` |
| **Doc Construction** | Each `BaseModule` (e.g., `IntroText`, `CustomModule`) processes LLM output → Markdown section | `factory/base_factory.py`, `factory/modules/*` |
| **Post‑processing** | Optional re‑ordering, anchor extraction, intro sections, cache clearance | `postprocessor/*` |
| **Persistence** | Write `README.md`, logs, and cache | `Manager.save()` in `manage.py` |

The pipeline is fully **layered** – each stage exposes a small, single‑purpose interface – and uses a **factory pattern** to iterate over a configurable list of doc modules.

### 3.2 LLM Wrapper  

`GPTModel` (synchronous) / `AsyncGPTModel` (async) manage a pool of API keys and models.  
* **Model rotation** – `ModelExhaustedException` is raised only when all configured keys/models are exhausted.  
* **History tracking** – keeps the last 3 k characters of context for subsequent prompts.  
* **Prompt assembly** – pulls constants such as `BASE_SYSTEM_TEXT`, `BASE_INTRO_CREATE`, etc., from `engine/config/config.py`.

### 3.3 Pre‑processing  

* **Splitting** – `split_data` respects a user‑defined `max_symbols` threshold and applies heuristics to stay below token limits.  
* **Compression** – `compressor.py` can reduce large files into concise prompts before they hit the LLM.  
* **Discovery** – `settings.py` controls file patterns to ignore, language, and metadata extraction.

### 3.4 Post‑processing  

* **Sorting & Ordering** – `postprocessor.sorting` places sections in a logical sequence.  
* **Anchor Extraction** – creates internal links for easy navigation.  
* **Intro Generation** – optional introductory text or global sections.

### 3.5 Logging & UI  

* **Singleton Logger** – `BaseLogger` funnels all logs, with optional file output via `FileLoggerTemplate`.  
* **Progress Feedback** – `ConsoleGitHubProgress` shows real‑time status during CI runs, while `LibProgress` (Rich) can be used locally.

---

## 4. Key Features  

* **Zero‑setup Documentation** – a single `autodocconfig.yml` configures patterns, languages, and module order.  
* **Modular Architecture** – add or replace `BaseModule` implementations without touching core logic.  
* **LLM Flexibility** – supports Groq, OpenAI, or any future LLM via the `gpt_model.py` abstraction.  
* **Token‑Aware Chunking** – automatically splits files to stay within token limits while preserving context.  
* **Post‑processing Pipeline** – reorder, add anchors, and create global intros automatically.  
* **CI‑Ready** – bundled GitHub workflows, progress output for GitHub Actions.  
* **Cache & History Management** – avoids redundant API calls and keeps conversational context.  
* **Extensible Prompt System** – all AI instructions live in `engine/config/config.py`; modify tone or formatting with minimal code changes.  
* **Exception Handling** – graceful fallback when API limits or key exhaustion occurs.  

---

## 5. Dependencies  

| Library / Tool | Purpose |
|----------------|---------|
| **Python 3.10+** | Core runtime |
| **rich** | Optional console progress UI |
| **pydantic** | Schema validation (`DocContent`, `DocInfoSchema`, etc.) |
| **groq / openai SDK** | LLM client (client choice determined by `GPTModel` implementation) |
| **PyYAML** | Read `autodocconfig.yml` |
| **GitHub Actions** | CI workflows (see `.github/workflows/*`) |
| **logging** | Standard Python logger (wrapped by `BaseLogger`) |

> *All third‑party dependencies are listed in `requirements.txt` and are installable via `pip install -r requirements.txt`.*

---

**Auto‑Doc Generator** delivers a maintainable, plug‑and‑play solution that turns raw source into polished, AI‑generated documentation while keeping the developer in full control of prompts, module composition, and CI integration.
## Executive Navigation Tree

- 📖 **Introduction**
  - [get-introdaction](#get-introdaction)
  - [get-links-intro](#get-links-intro)
  - [intro-modules](#intro-modules)
  - [welcome-message](#welcome-message)

- 🔧 **Utilities**
  - [logging](#logging)
  - [logging-component](#logging-component)
  - [logging-initialization](#logging-initialization)
  - [imports](#imports)

- 📦 **Modules**
  - [base-module](#base-module)
  - [custom-module](#custom-module)
  - [custom-module-without](#custom-module-without)
  - [module-model](#module-model)
  - [module-run_file](#module-run_file)
  - [module-exceptions](#module-exceptions)
  - [module-conclusion](#module-conclusion)

- ⚙️ **Configuration**
  - [module-config](#module-config)
  - [module-config_reader](#module-config_reader)
  - [project-settings-class](#project-settings-class)
  - [autodocconfig-options](#autodocconfig-options)

- 📦 **Manager**
  - [manager](#manager)
  - [manager-class-usage](#manager-class-usage)
  - [manager-init](#manager-init)

- 🔩 **Components**
  - [component-gptmodel](#component-gptmodel)
  - [component-model](#component-model)
  - [progress-component](#progress-component)

- 📄 **Documentation Generation**
  - [get-all-html-links](#get-all-html-links)
  - [data-contract](#data-contract)
  - [data-contract-gptmodel](#data-contract-gptmodel)
  - [code-mix-class](#code-mix-class)
  - [code-mix-generation](#code-mix-generation)
  - [code-splitting](#code-splitting)
  - [compressor-functions](#compressor-functions)
  - [compressor-module](#compressor-module)
  - [compression-flow](#compression-flow)
  - [reassembly](#reassembly)
  - [CONTENT_DESCRIPTION](#CONTENT_DESCRIPTION)
  - [doc-factory](#doc-factory)
  - [doc-schemas](#doc-schemas)
  - [generete-custom-discription](#generete-custom-discription)
  - [generete-custom-discription-without](#generete-custom-discription-without)
  - [gen-doc-parts](#gen-doc-parts)
  - [global-info-generation](#global-info-generation)
  - [parts-generation](#parts-generation)
  - [write-docs](#write-docs)
  - [factory-generate](#factory-generate)

- 🔗 **Cross‑module Interaction**
  - [cross-module-interactions](#cross-module-interactions)
  - [inter-module-communication](#inter-module-communication)
  - [interactions](#interactions)

- 📁 **Anchor & Path**
  - [anchor-extraction](#anchor-extraction)
  - [anchor-splitting](#anchor-splitting)
  - [file-paths](#file-paths)

- 🛠️ **Exception & Cache**
  - [exception-handling](#exception-handling)
  - [cache-clear](#cache-clear)

- 📑 **Summary & Misc**
  - [conclusion](#conclusion)
  - [edge-cases](#edge-cases)
  - [overall-summary](#overall-summary)
  - [summary](#summary)
  - [example-flow](#example-flow)
  - [limitations](#limitations)
  - [observations](#observations)
  - [ignore-list](#ignore-list)
  - [ordering](#ordering)

- 📚 **General**
  - [project-metadata](#project-metadata)
<a name="get-all-html-links"></a>
### `get_all_html_links(data: str) → list[str]`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Markdown source | Input document to search for `<a name>` anchors. |
| `links` | `list[str]` | Result | Returns `[#anchor]` for each anchor with >5 chars. |
| `logger` | `BaseLogger` | Logger | Logs extraction steps. |
| `pattern` | `re.Pattern` | Anchor regex | Matches `<a name="...">` or `<a name='...'>`. |

**Logic Flow**  
1. Compile regex `r'<a name=["\']?(.*?)["\']?>`.  
2. Iterate over all matches; extract `anchor_name`.  
3. If `len(anchor_name)>5`, prepend `#` and append to `links`.  
4. Log number of links and list.  

> **Result** – Returns a list of markdown anchor links that will be used in table‑of‑contents sections.  

---
<a name="get-introdaction"></a>
### `get_introdaction(global_data: str, model: Model, language: str = "en") → str`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `global_data` | `str` | Raw project description | Supplied by the calling pipeline. |
| `model` | `Model` | LLM wrapper | Calls `get_answer_without_history`. |
| `language` | `str` | Target language | Included in system instruction. |

**Logic Flow**  
1. Compose a 3‑message prompt using `BASE_INTRO_CREATE`.  
2. Pass to LLM and return the resulting intro text.  

> **Result** – The top‑level introduction for the README.  

---
<a name="get-links-intro"></a>
### `get_links_intro(links: list[str], model: Model, language: str = "en") → str`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `links` | `list[str]` | Anchor list | Obtained from `get_all_html_links`. |
| `model` | `Model` | LLM wrapper | Calls `get_answer_without_history`. |
| `language` | `str` | Target language | Sent as a system instruction. |
| `prompt` | `list[dict]` | LLM prompt | Contains system messages and `BASE_INTRODACTION_CREATE_LINKS`. |

**Logic Flow**  
1. Build a 3‑message prompt: language instruction, `BASE_INTRODACTION_CREATE_LINKS`, and the `links` string.  
2. Invoke `model.get_answer_without_history`.  
3. Return the generated introductory section.  

> **Result** – A Markdown fragment that introduces the generated documentation with clickable links.  

---
<a name="intro-modules"></a>  
## Intro Modules – Automated Introduction Sections

```python
class IntroLinks(BaseModule):
    def generate(self, info: dict, model: Model):
        links = get_all_html_links(info.get("full_data"))
        return get_links_intro(links, model, info.get("language"))
```

```python
class IntroText(BaseModule):
    def generate(self, info: dict, model: Model):
        return get_introdaction(info.get("global_info"), model, info.get("language"))
```

* **Purpose** – Build introductory material from the repository’s metadata.  
  * `IntroLinks` collects all external URLs and asks the model to format a “Links” section.  
  * `IntroText` synthesizes a high‑level introduction based on `global_info`.  
* **Shared Mechanism** – Both rely on `postprocessor.custom_intro` functions and the same `model`.  

| Module | Input Key | Prompt Type | Output |
|--------|-----------|-------------|--------|
| `IntroLinks` | `full_data` | Link list | Markdown list of links |
| `IntroText` | `global_info` | Overview prompt | Markdown intro |

> **Note** – The modules are pure‑function; no side‑effects beyond returning strings.  
> **Error Handling** – Any exception in the underlying LLM call propagates to `DocFactory`; `ModelExhaustedException` is surfaced at the top level.  

---
<a name="welcome-message"></a>  
## Welcome Message Display

The module executes a single helper, `_print_welcome`, that renders an ASCII banner and a status line when the package is imported.

```python
def _print_welcome():
    ...
    print(ascii_logo)
    print(f"{CYAN}ADG Library{RESET} | {BOLD}Status:{RESET} Ready to work V0.0.1")
    print(f"{'—' * 35}\n")
```

The routine uses ANSI escape sequences to colour the output. It is **immediately invoked** at import time, so any consumer of the library will see the banner in the console.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BLUE` | str | Colour escape for banner | `"\033[94m"` |
| `BOLD` | str | Bold text escape | `"\033[1m"` |
| `CYAN` | str | Colour escape for library name | `"\033[96m"` |
| `RESET` | str | Reset formatting | `"\033[0m"` |
| `ascii_logo` | str | Multi‑line ASCII art | displayed on import |
| `_print_welcome()` | function | Side‑effect: prints banner | executed automatically |

> **Notice**: The function is not exported; it is a private helper for visual feedback only.

---
<a name="logging"></a>
## Logging Strategy

- `BaseLogger` is instantiated locally in each function; it is a *singleton* under the hood, guaranteeing a single output stream.  
- `InfoLog` objects carry a `level` integer; higher levels produce quieter logs.  
- All major stages emit a message, including lengths of generated text.

---
<a name="logging-component"></a>
## Logging Component – `autodocgenerator/ui/logging.py`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseLog` | Abstract class | Base for log objects | Stores `message`, `level`; generates timestamped prefix |
| `ErrorLog`, `WarningLog`, `InfoLog` | Sub‑classes | Emit formatted strings with severity tags | Override `format()` |
| `BaseLoggerTemplate` | Logger abstraction | Holds `log_level`; routes messages through `global_log` | `log()` writes directly (e.g., console) |
| `FileLoggerTemplate` | Concrete template | Appends formatted logs to a file | Uses `file_path` |
| `BaseLogger` | Singleton | Central logger instance | `set_logger()` attaches a concrete template; `log()` delegates to the template |

> **Implementation Detail** – `BaseLogger.__new__` guarantees a single shared instance across the project.

---
<a name="logging-initialization"></a>  
## Logger Initialization

After printing the banner, the module sets up the global logger that the rest of the package relies on.

```python
from .ui.logging import BaseLogger, BaseLoggerTemplate, InfoLog, ErrorLog, WarningLog

logger = BaseLogger()
logger.set_logger(BaseLoggerTemplate())
```

The `BaseLogger` is a singleton that aggregates log handlers. `BaseLoggerTemplate` defines the output format and default level. The `logger` instance becomes available to any sub‑module that imports it from `autodocgenerator`.

| Symbol | Scope | Effect |
|--------|-------|--------|
| `BaseLogger` | Module | Singleton logger class |
| `BaseLoggerTemplate` | Module | Log handler configuration |
| `logger` | Module | Global logger instance |

> **Assumption**: The `ui.logging` module implements a standard logger that accepts a template via `set_logger`. No other configuration is performed in this file.

---
<a name="base-module"></a>  
## BaseModule – Contract for Documentation Builders

```python
class BaseModule(ABC):
    @abstractmethod
    def generate(self, info: dict, model: Model):
        ...
```

* **Role** – Declares the interface a concrete module must implement.  
* **Parameters** – `info` is a dictionary of repo‑wide data; `model` is a `Model` instance that talks to Groq/Chat‑GPT.  
* **Output** – A Markdown string produced by the module.

---
<a name="custom-module"></a>  
## CustomModule – Context‑Rich Description

```python
class CustomModule(BaseModule):
    def generate(self, info: dict, model: Model):
        return generete_custom_discription(
            split_data(info.get("code_mix"), max_symbols=5000),
            model,
            self.discription,
            info.get("language"))
```

* **Goal** – Produce a documentation segment that incorporates a code snippet limited to `5 000` symbols.  
* **Dependencies** – `split_data` (preprocessor), `generete_custom_discription` (postprocessor).  
* **Data Flow**  
  1. `info["code_mix"]` → split to a manageable chunk.  
  2. Chunk + user `discription` + language sent to the model.  
  3. Result returned as Markdown.  

---
<a name="custom-module-without"></a>  
## CustomModuleWithOutContext – Self‑Contained Descriptions

```python
class CustomModuleWithOutContext(BaseModule):
    def generate(self, info: dict, model: Model):
        return generete_custom_discription_without(
            model, self.discription, info.get("language"))
```

* **Use‑case** – Generates a section that does **not** depend on any source fragment.  
* **Inputs** – Only `model`, static `discription`, and language.  
* **Output** – Plain Markdown paragraph.  

---
<a name="install-script"></a>
## Install PowerShell Script – `install.ps1`

| Step | Action | Outcome |
|------|--------|---------|
| Create `.github/workflows` dir | `New-Item -ItemType Directory -Force` | Directory ready for workflow file |
| Write workflow YAML | Here‑string `@' … '@` piped to `Out-File` | Generates `autodoc.yml` that calls reusable workflow |
| Generate `autodocconfig.yml` | Here‑string with current folder name and settings | Provides ignore patterns, build and structure flags |

> **Notice** – The script uses PowerShell variable interpolation and `Out-File -Encoding utf8` to ensure proper Unicode handling.

---
<a name="installer-shell-script"></a>  
## Installer Shell Script

**Purpose**  
Creates the CI workflow and initial configuration for the Auto‑Doc Generator.  
The script is run in the project root; it writes a GitHub Actions workflow
(`.github/workflows/autodoc.yml`) that re‑uses a shared reusable workflow
and an `autodocconfig.yml` file that stores project‑specific settings.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `mkdir -p .github/workflows` | command | Ensure the workflow directory exists | No side‑effects beyond directory creation |
| `autodoc.yml` | YAML file | Defines the GitHub Actions job | Uses `GROCK_API_KEY` secret |
| `autodocconfig.yml` | YAML file | Holds project metadata and ignore patterns | Generated using shell `basename` and heredoc |
| `echo "✅ Done!"` | console output | Feedback to the user | Non‑blocking |

**Processing Flow**

1. **Create Workflow Directory**  
   ```bash
   mkdir -p .github/workflows
   ```
   Ensures the directory for GitHub Actions files exists.

2. **Write `autodoc.yml`**  
   The file declares a dispatchable workflow that invokes a reusable
   workflow stored at `Drag‑GameStudio/ADG/.github/workflows/reuseble_agd.yml@main`.
   It passes the `GROCK_API_KEY` secret and grants write permission for
   repository contents.

3. **Write `autodocconfig.yml`**  
   Populates project metadata (`project_name`, `language`) and several
   sections:
   * `ignore_files` – glob patterns for files to exclude.
   * `build_settings` – logging options.
   * `structure_settings` – toggles for generated sections.
   The content is output via a here‑document, with the first `$` escaped
   (`\$`) so the key can be rendered correctly in GitHub secrets.

4. **Final Notification**  
   `echo "✅ Done! …"` confirms success.

> **Critical Assumption**  
> The script expects to be executed in the repository root where a
> GitHub Actions workflow can be committed and a `autodocconfig.yml`
> can be placed.
<a name="install-workflow-with-scripts"></a>  

To set up the application you can run one of two bootstrap scripts directly from the repository.  
- **On Windows with PowerShell** execute:  

  ```powershell
  irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
  ```  

  The script pulls the latest installation package, configures required environment variables, and starts the service.  

- **On Linux‑based systems** run the shell script:  

  ```bash
  curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
  ```  

  This performs the same sequence of download, setup, and launch steps in a POSIX environment.  

If you intend to run the installer within a CI pipeline such as GitHub Actions, create a secret named **GROCK_API_KEY** in the repository’s secret store. The value must be the API key obtained from the Grock interface at https://grockdocs.com. The installer will automatically consume this secret to authenticate with the Grock service during deployment.
<a name="manager"></a>
## Manager – Repository‑level Orchestration

**Purpose** –  
The `Manager` class is the central coordination hub for the Auto‑Doc Generator pipeline.  
It loads and persists intermediate artefacts, triggers LLM‑based transformations, and accumulates final Markdown output.

---
<a name="manager-class-usage"></a>

**Manager class**

| Method | Purpose |
|--------|---------|
| `generate_code_file()` | Scans the project folder and creates a cache of Python source files for later use. |
| `generate_global_info(compress_power: int)` | Builds a compressed global information file if requested. |
| `generete_doc_parts(max_symbols: int, with_global_file: bool)` | Splits the cached code into document parts respecting the maximum symbol count. |
| `factory_generate_doc(factory, to_start: bool = False, with_splited: bool = True)` | Uses a `DocFactory` instance to create documentation pieces, optionally inserting them at the beginning and controlling whether the result is split into multiple sections. |
| `order_doc()` | Reorders the generated documentation sections according to a predefined sequence. |
| `clear_cache()` | Deletes temporary files and data used during the generation cycle. |
| `save()` | Persists the final documentation object to disk. |
| `doc_info.doc.get_full_doc()` | Retrieves the complete assembled documentation text. |

**Typical usage**

```python
from autodocgenerator.manage import Manager
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.general_modules import CustomModule
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.auto_runner.config_reader import read_config
from autodocgenerator.engine.models.gpt_model import GPTModel
from autodocgenerator.engine.config.config import API_KEYS

# Load configuration data from a file (context provided in the project)
with open("autodocconfig.yml", "r", encoding="utf-8") as f:
    cfg_data = f.read()
config_obj, custom_mods, struct_opts = read_config(cfg_data)

# Prepare the language model and progress indicator
llm = GPTModel(API_KEYS, use_random=False)

# Create Manager
mgr = Manager(
    project_path=".",          # root of the target project
    config=config_obj,
    llm_model=llm,
    progress_bar=ConsoleGtiHubProgress()
)

# Execute the documentation pipeline
mgr.generate_code_file()

if struct_opts.use_global_file:
    mgr.generate_global_info(compress_power=4)

mgr.generete_doc_parts(
    max_symbols=struct_opts.max_doc_part_size,
    with_global_file=struct_opts.use_global_file
)

mgr.factory_generate_doc(DocFactory(*custom_mods))

if struct_opts.include_order:
    mgr.order_doc()

additional_modules = []
if struct_opts.include_intro_text:
    additional_modules.append(IntroText())
if struct_opts.include_intro_links:
    additional_modules.append(IntroLinks())

mgr.factory_generate_doc(
    DocFactory(*additional_modules, with_splited=False),
    to_start=True
)

mgr.clear_cache()
mgr.save()

# Retrieve the finished documentation
full_text = mgr.doc_info.doc.get_full_doc()
```

This sequence demonstrates how to instantiate the manager, run all generation steps, and obtain the final documentation string.
<a name="manager-init"></a>
### `__init__` – Construction & Cache Preparation

| Parameter | Type | Role | Notes |
|-----------|------|------|-------|
| `project_directory` | `str` | Root of target repository | Path used for all cache files |
| `config` | `Config` | Parsed `autodocconfig.yml` | Provides `pbc.log_level`, `ignore_files`, `language` etc. |
| `llm_model` | `Model` | LLM client | Handles key rotation, request history |
| `progress_bar` | `BaseProgress` | UI progress | Default instance if not supplied |

**Steps**

1. Initialise a new `DocInfoSchema` container.  
2. Store `config`, `project_directory`, `llm_model`, `progress_bar`.  
3. Initialise a singleton `BaseLogger` and attach a `FileLoggerTemplate` to a log file under the cache folder.  
4. Create a `.auto_doc_cache` folder if it does not exist.

> **Note** – No network traffic is performed during construction.

---
<a name="module-config"></a>
## Related Configuration

`autodocgenerator.engine.exceptions.ModelExhaustedException` is the only exception that propagates outside this module, signaling to `Manager` that the pipeline must terminate gracefully.

The `API_KEYS` list is sourced from `autodocgenerator.config.config` and typically contains Groq API keys.  

---

*The documentation above is a self‑contained, factual representation of the `gpt_model.py` and `model.py` fragments, aligned with the Auto‑Doc Generator’s pipeline and strictly based on the provided source.*
<a name="module-config_reader"></a>  
## Config Reader – Settings Loader

The `autodocgenerator.auto_runner.config_reader` module is responsible for translating the YAML configuration file (`autodocconfig.yml`) into runtime objects that drive the documentation pipeline.

### StructureSettings

| Property | Type | Default | Notes |
|----------|------|---------|-------|
| `include_intro_links` | `bool` | `True` | Whether to inject the `IntroLinks` module during the doc build. |
| `include_order` | `bool` | `True` | Enables post‑processing re‑ordering. |
| `use_global_file` | `bool` | `True` | Controls generation of a global‑information file. |
| `max_doc_part_size` | `int` | `5_000` | Maximum token count per chunk. |
| `include_intro_text` | `bool` | `True` | Controls injection of a descriptive intro section. |

`StructureSettings` exposes a `load_settings(dict)` method that dynamically overwrites defaults from a user‑supplied dictionary.

> **Assumption**: The module does not expose any public API beyond the `read_config` function and the `StructureSettings` class.

### read_config

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_data` | `str` | YAML source | Raw file contents. |
| `Config` | `autodocgenerator.config.config.Config` | Holds project‑wide settings. | Instantiated and populated. |
| `ProjectBuildConfig` | `ProjectBuildConfig` | Holds build‑specific toggles. | Loaded from `build_settings`. |
| `CustomModule` / `CustomModuleWithOutContext` | `BaseModule` subclasses | Custom LLM prompts. | Created from `custom_descriptions`. |
| `StructureSettings` | `StructureSettings` | Layout flags. | Instantiated and overwritten. |

The function returns a tuple of:

```python
(config: Config, custom_modules: list[BaseModule], structure_settings: StructureSettings)
```

Internally it:

1. Parses `file_data` with `yaml.safe_load`.  
2. Constructs a `Config` and populates ignore patterns, language, project metadata.  
3. Builds a `ProjectBuildConfig` from `build_settings`.  
4. Creates `CustomModule` instances based on the `%` marker logic.  
5. Loads any supplied `structure_settings`.

> **Missing**: No public functions are exposed beyond `read_config`.

---
<a name="module-conclusion"></a>  
## Module Summary

* Executes a banner on import.
* Instantiates and configures a global logger for the project.
* Exposes the `logger` instance for downstream components.

Information not present in the provided fragment: there are no public functions or classes beyond the internal banner routine; the module does not expose any API beyond the logger.
<a name="module-exceptions"></a>  
## Engine Exceptions – LLM Availability Guard

`autodocgenerator.engine.exceptions.ModelExhaustedException` signals that all configured Groq/ChatGPT models have been exhausted, and no further requests can be made. This exception propagates up to the caller, typically resulting in a graceful termination of the documentation pipeline.

---

### Summary

These modules collectively translate a YAML configuration into runtime objects, orchestrate the document generation pipeline via `Manager` and `DocFactory`, and expose a clean API for the rest of the system to consume. The design relies on explicit data contracts and avoids hidden state, ensuring that each component can be unit‑tested in isolation.
<a name="module-model"></a>
## Supporting Module – `model.py`

**History Class**  
```python
class History:
    def __init__(self, system_prompt: str = BASE_SYSTEM_TEXT):
        self.history: list[dict[str, str]] = []
        if system_prompt is not None:
            self.add_to_history("system", system_prompt)
    ...
```
- Initializes with the default system prompt.
- Provides `add_to_history(role, content)` for appending messages.

**Abstract Base**  
`ParentModel` abstracts key rotation and history management.  
- `self.api_keys` holds the list of API keys.
- `self.regen_models_name` holds the shuffled list of model identifiers.
- `generate_answer`, `get_answer_without_history`, `get_answer` are abstract and implemented by concrete subclasses.

**Synchronous Implementation**  
`GPTModel` implements the actual HTTP request to Groq:

```python
chat_completion = self.client.chat.completions.create(
    messages=messages,
    model=model_name,
)
```
- The request is wrapped in a `while True` loop that continues until a success or all models are exhausted.  
- On failure, it logs a warning, updates indices, and re‑instantiates the Groq client with a new key.  
- `ModelExhaustedException` is raised when the model pool is empty.

> **Side Effect** – All logs (`InfoLog`, `WarningLog`, `ErrorLog`) are routed through `BaseLogger`, ensuring uniform traceability across the system.  

---
<a name="module-run_file"></a>  
## Run File – Orchestration Entry Point

`autodocgenerator.auto_runner.run_file` contains the primary driver that ties together all layers of the Auto‑Doc Generator. The core public method is `gen_doc`.

### gen_doc

| Parameter | Type | Role | Notes |
|-----------|------|------|-------|
| `project_path` | `str` | Root of the repository | Target for content discovery. |
| `config` | `Config` | Project configuration | From `config_reader`. |
| `custom_modules` | `list[BaseModule]` | Custom sections to inject | Provided by `read_config`. |
| `structure_settings` | `StructureSettings` | Layout toggles | Also from `read_config`. |

#### Flow

1. **LLM Preparation**  
   ```python
   sync_model = GPTModel(API_KEYS, use_random=False)
   ```

2. **Manager Instantiation**  
   ```python
   manager = Manager(
       project_path,
       config=config,
       llm_model=sync_model,
       progress_bar=ConsoleGtiHubProgress(),
   )
   ```

3. **Repository Walk**  
   - `manager.generate_code_file()` – splits the codebase into manageable chunks.

4. **Global Section (Optional)**  
   ```python
   if structure_settings.use_global_file:
       manager.generate_global_info(compress_power=4)
   ```

5. **Document Parts Generation**  
   ```python
   manager.generete_doc_parts(
       max_symbols=structure_settings.max_doc_part_size,
       with_global_file=structure_settings.use_global_file
   )
   ```

6. **Custom Module Injection**  
   ```python
   manager.factory_generate_doc(DocFactory(*custom_modules))
   ```

7. **Re‑ordering (Optional)**  
   ```python
   if structure_settings.include_order:
       manager.order_doc()
   ```

8. **Intro Modules** (conditioned on flags)  
   ```python
   additionals_modules = []
   if structure_settings.include_intro_text:
       additionals_modules.append(IntroText())
   if structure_settings.include_intro_links:
       additionals_modules.append(IntroLinks())
   manager.factory_generate_doc(DocFactory(*additionals_modules, with_splited=False), to_start=True)
   ```

9. **Cleanup & Persist**  
   ```python
   manager.clear_cache()
   manager.save()
   ```

10. **Return Value** – the assembled markdown string:
    ```python
    return manager.doc_info.doc.get_full_doc()
    ```

> **Return**: `str` – the complete README content.

The `__main__` block simply loads `autodocconfig.yml`, parses it with `read_config`, and calls `gen_doc` on the current directory.

### Key Interactions

| Component | Interaction | Outcome |
|-----------|-------------|---------|
| `Manager` | `generate_code_file` → `generate_global_info` | Pre‑processing pipeline that creates a cached, compressed representation of the code. |
| `DocFactory` | `factory_generate_doc` | Instantiates and processes each `BaseModule`, which in turn calls `GPTModel.generate_answer`. |
| `GPTModel` | LLM requests | Generates Markdown for each code chunk or module. |
| `ConsoleGtiHubProgress` | Progress callbacks | UI feedback during long operations. |
| `CustomModule` | Prompt injection | Allows users to embed arbitrary LLM prompts. |

### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_path` | `str` | Input | Directory to scan. |
| `config.ignore_files` | `list[str]` | Filters | Files/directories excluded from the scan. |
| `config.language` | `str` | LLM context | Determines language of prompts. |
| `config.project_name` | `str` | Metadata | Populated into global information. |
| `structure_settings.max_doc_part_size` | `int` | Chunk size limit | Token cap for each LLM call. |
| `manager.doc_info.doc` | `DocContent` | Resulting document | Exposed via `get_full_doc()` |

---
<a name="project-metadata"></a>  
## Project Metadata (`pyproject.toml`)

**Purpose**  
Defines packaging metadata, runtime dependencies, and the build system
configuration for the Auto‑Doc Generator.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `[project]` | section | PEP 621 metadata | Includes `name`, `version`, `authors`, `license`, `readme`, `requires‑python` |
| `dependencies` | list | Runtime requirements | Uses pinned versions for stability |
| `[build-system]` | section | Build backend | Uses `poetry‑core` to build a wheel |

**Key Parameters**

| Parameter | Value | Effect |
|-----------|-------|--------|
| `name` | `autodocgenerator` | Package name used in PyPI |
| `version` | `1.0.3.3` | Semantic versioning tag |
| `requires-python` | `>=3.11,<4.0` | Ensures compatibility with Python 3.11+ |
| `license.text` | `MIT` | Open‑source license |
| `readme` | `README.md` | Primary long‑description source |
| `dependencies` | extensive list | Includes `rich`, `pyyaml`, `pydantic`, `groq`, etc. |
| `build-system.requires` | `poetry‑core>=2.0.0` | Specifies backend required to build the project |

> **Side Effect**  
> The `pyproject.toml` is consumed by Poetry (or compatible tools) during
> installation or packaging, automatically pulling the specified
> dependencies and ensuring the runtime environment matches the
> configuration.
<a name="project-settings-class"></a>
## `ProjectSettings` (preprocessor.settings)

**Core Responsibility**  
Holds a per‑project prompt template used by compression and other LLM interactions. Allows arbitrary key/value metadata to be inserted into the prompt.

| Method | Role | Notes |
|---|---|---|
| `__init__(project_name)` | Initializes with project name; starts empty `info` dict. | |
| `add_info(key, value)` | Stores custom metadata. | |
| `prompt` (property) | Builds a composite prompt string: base template + project name + all `info` key/value pairs. | Uses `BASE_SETTINGS_PROMPT` constant from `engine.config.config`. |

---
<a name="component-gptmodel"></a>
## GPTModel: LLM Request Handler

**Role**  
Acts as the bridge between the Auto‑Doc Generator pipeline and an external Groq‑powered language model.  
- Manages a rotating pool of API keys and model names.  
- Provides a synchronous API (`generate_answer`) used by `DocFactory` and higher‑level orchestrators.  
- Emits detailed logs via `BaseLogger`.  

**Key Interactions**  

| Called By | Outcome |
|-----------|---------|
| `DocFactory.factory_generate_doc` | LLM generates Markdown for a code chunk or module. |
| `Manager.generate_global_info` | Requests auxiliary documentation pieces (e.g., project overview). |
| `ConsoleGitHubProgress` | Uses the logs generated by `GPTModel` for UI feedback (implicit through `BaseLogger`). |

---
<a name="component-model"></a>
## Model Hierarchy & History Context

| Class | Base | Purpose |
|-------|------|---------|
| `History` | – | Stores a list of `{role, content}` objects representing the conversation. |
| `ParentModel` | `ABC` | Holds common state: `api_keys`, `history`, shuffling of `models_list`. |
| `Model` | `ParentModel` | Synchronous implementation of the LLM interface. |
| `AsyncModel` | `ParentModel` | Asynchronous counterpart (currently unimplemented). |
| `AsyncGPTModel` | `AsyncModel` | Stub for future async support. |

> **Critical Logic**  
> 1. **Constructor** – Shuffles `models_list` if `use_random=True`, initializes indices.  
> 2. **generate_answer** – Attempts to call `client.chat.completions.create`.  
> 3. **Error Recovery** – On exception, rotates to the next API key and/or model until the pool is exhausted.  
> 4. **Result Handling** – Extracts `choices[0].message.content`, logs success, returns empty string if `None`.  

---
<a name="progress-component"></a>
## Progress Interface – `autodocgenerator/ui/progress_base.py`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseProgress` | Interface | Defines progress API | Methods are no‑ops or placeholders |
| `LibProgress` | Rich‑based implementation | Uses `rich.progress.Progress` to show a main task and optional subtasks | `create_new_subtask()`, `update_task()`, `remove_subtask()` |
| `ConsoleTask` | Simple console helper | Prints percentage of a single task | Not thread‑safe, used by GitHub progress |
| `ConsoleGtiHubProgress` | GitHub‑friendly wrapper | Falls back to console output when Rich is absent | Delegates to `ConsoleTask` instances |

> **Key Logic Flow** – `update_task()` checks for an active subtask; if none, it advances the base task, otherwise advances the current sub‑task.

---
<a name="data-contract"></a>
## Data Contract

| Entity | Type | Role | Notes |
|---|---|---|---|
| `data` (in `compress`) | `str` | Input text to be compressed. | Raw Markdown, code snippets, or other free text. |
| `project_settings` | `ProjectSettings` | Provides contextual prompt information. | Includes `BASE_SETTINGS_PROMPT` and user‑defined metadata. |
| `model` | `Model` | LLM wrapper exposing `get_answer_without_history`. | Must be an instance of `engine.models.gpt_model.GPTModel` or compatible. |
| `compress_power` | `int` | Compression granularity hint. | Influences prompt construction and bucket size in higher‑level functions. |
| `progress_bar` | `BaseProgress` | UI feedback. | Default constructed instance if omitted. |

---
<a name="data-contract-gptmodel"></a>
## Data Contract for GPTModel

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `list[str]` | Credentials for Groq client | Default: `API_KEYS` from `config.config`. |
| `history` | `History` | Conversation history | Contains the system prompt on initialization. |
| `models_list` | `list[str]` | Candidate LLM models | Defaults include `gpt-oss-120b`, `llama‑3.3‑70b‑versatile`, `gpt-oss-safeguard‑20b`. |
| `use_random` | `bool` | Shuffle model list | True by default. |
| `client` | `Groq` | Active Groq client instance | Re‑instantiated when key changes. |
| `messages` | `list[dict[str,str]]` | Chat messages | Either `history.history` or provided `prompt`. |
| `regen_models_name` | `list[str]` | Remaining models to try | Updated during error handling. |
| `current_model_index` | `int` | Index in `regen_models_name` | Rotated after a failed request. |
| `current_key_index` | `int` | Index in `api_keys` | Rotated after a failed request. |
| `result` | `str` | LLM response | Returned to caller; logged at level 2. |

---
<a name="code-mix-class"></a>  
## Repository Content Packing – `CodeMix`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `root_dir` | Path | Base directory for traversal | Default `.` resolved to absolute path. |
| `ignore_patterns` | list[str] | Patterns to skip | Used by `should_ignore`. |
| `logger` | `BaseLogger` | Logging helper | Emits ignored‑file messages. |
| `should_ignore(path)` | method | Determines if a file/directory should be excluded | Uses `fnmatch` against path parts and basename. |
| `build_repo_content()` | method | Generates a Markdown representation of the repository | Returns a single string. |

### Logic Flow  

1. Append a header **“Repository Structure:”**.  
2. Walk the file tree (`rglob("*")`).  
3. For each path:
   - Skip if `should_ignore(path)` is `True` (log at level 1).  
   - Calculate depth and indentation; add a line with either `<dir_name>/` or file name.  
4. Append a separator of equal signs.  
5. Walk again, this time adding file contents:
   - For each file not ignored, write `<file path="relative_path">` marker, file text (UTF‑8, ignore errors), then a newline.  
   - Catch read errors and include an error message line.  
6. Return the joined string.

> **Result** – A consolidated Markdown block describing the repository layout and all source file contents.
<a name="code-mix-generation"></a>
### `generate_code_file`

| Action | Description | Dependencies |
|--------|-------------|--------------|
| Calls `CodeMix(project_directory, config.ignore_files)` | Builds a flattened source string | `preprocessor.code_mix.CodeMix` |
| Stores result in `self.doc_info.code_mix` | Centralised repository of raw code | `DocInfoSchema.code_mix` |
| Updates progress | Signals step completion | `BaseProgress.update_task()` |

> **Side‑effect** – Emits an `InfoLog` entry for start/finish.

---
<a name="code-splitting"></a>
## Code Splitting & Chunking Logic

```python
while True:
    have_to_change = False
    for i, el in enumerate(splited_by_files):
        if len(el) > max_symbols * 1.5:
            splited_by_files.insert(i+1, el[i][int(max_symbols / 2):])
            splited_by_files[i] = el[i][:int(max_symbols / 2)]
            have_to_change = True

    if have_to_change == False:
        break
```

- **Purpose** – Iteratively bisects any source fragment that exceeds *1.5 ×* the maximum allowed symbol count (`max_symbols`).  
- **Behaviour** – The loop terminates once every element in `splited_by_files` is below the threshold.  
- **Side‑effects** – Mutates `splited_by_files` in‑place and records progress via `BaseLogger`.  
- **Edge** – If an element is exactly at the threshold it is **not** split, ensuring minimal churn.
<a name="compressor-functions"></a>
## Key Functions

| Function | Purpose | Parameters | Returns | Notes |
|---|---|---|---|---|
| `compress(data: str, project_settings: ProjectSettings, model: Model, compress_power) -> str` | Sends a single text block to an LLM for compression using a dynamic prompt. | `data`: text to compress <br>`project_settings`: contextual prompts<br>`model`: LLM interface (`Model`) <br>`compress_power`: numeric hint for prompt length | Compressed text string returned by the LLM | Uses `get_BASE_COMPRESS_TEXT(len(data), compress_power)` to prepend token‑limit instructions. |
| `compress_and_compare(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) -> list` | Aggregates multiple items into compressed buckets of size `compress_power`. | `data`: list of strings to compress <br>`model`, `project_settings`: as above <br>`compress_power`: how many items per bucket <br>`progress_bar`: progress feedback | List of compressed strings; each element represents a bucket | Logs progress via `BaseProgress`. |
| `compress_to_one(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) -> str` | Iteratively merges the list returned by `compress_and_compare` until a single string remains. | Same as `compress_and_compare` | Final single compressed document | Uses a loop that halves the list size; `new_compress_power` is reduced to `2` when the remaining list is smaller than `compress_power+1`. |

---
<a name="compressor-module"></a>
## Compressor Module – `autodocgenerator.preprocessor.compressor`

**Core Responsibility**  
The `compressor` module condenses raw source‑code or documentation fragments into a smaller representation suitable for LLM‑based processing. It orchestrates one‑to‑many compression passes, progressively merging chunks until a single compressed document remains.

---
<a name="compression-flow"></a>
## Compression Logic Flow

1. **Prompt Construction**  
   - System messages: project‑specific prompt (`project_settings.prompt`) and a size‑aware compression directive (`get_BASE_COMPRESS_TEXT`).  
   - User message: the raw `data` string.

2. **LLM Invocation**  
   - `model.get_answer_without_history(prompt)` is called synchronously; the response is a compressed string.

3. **Batch Compression**  
   - `compress_and_compare` groups incoming items (`data` list) into buckets of `compress_power`.  
   - Each bucket’s aggregated content is compressed via `compress`, appended with a newline.

4. **Recursive Reduction**  
   - `compress_to_one` repeatedly calls `compress_and_compare`, reducing the list size until a single string is produced.  
   - When the remaining list length is below `compress_power + 1`, the bucket size is lowered to `2` to ensure convergence.

5. **Result**  
   - A single Markdown string that encapsulates the entire repository or documentation section, ready for further post‑processing or file output.

---
<a name="reassembly"></a>
## Re‑assembly into Fixed‑Size Parts

```python
curr_index = 0
for el in splited_by_files:
    if len(split_objects) - 1 < curr_index:
        split_objects.append("")

    if len(split_objects[curr_index]) + len(el) > max_symbols * 1.25:
        curr_index += 1
        split_objects.append(el)
        continue

    split_objects[curr_index] += "\n" + el
```

- **Goal** – Concatenate split fragments into `split_objects` such that each accumulated string stays within *1.25 ×* `max_symbols`.  
- **Result** – Returns a list of strings, each a “clean” chunk ready for LLM consumption.  
- **Logging** – `BaseLogger` reports the final chunk count.
<a name="CONTENT_DESCRIPTION"></a>` tag and contain no file paths, extensions, or generic terms.  
2. Send to the LLM.  
3. Return the raw answer.  

> **Result** – A formatted, tag‑prefixed description suitable for insertion into documentation sections.  

---
<a name="doc-factory"></a>  
## DocFactory – Orchestrating Module Execution

```python
class DocFactory:
    def generate_doc(self, info: dict, model: Model, progress: BaseProgress) -> DocHeadSchema:
```

* **Purpose** – Sequentially runs each `BaseModule`, splits the result on anchor markers, and aggregates `DocHeadSchema`.  
* **Workflow**  
  1. Create a sub‑task counter in `progress`.  
  2. For every module, call `module.generate(info, model)`.  
  3. If `with_splited` is `True`, split the returned string using `split_text_by_anchors` and add each fragment to `doc_head` with its key.  
  4. Log at level 1 (module finished) and level 2 (raw output).  
  5. Increment progress, remove sub‑task after all modules finish.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `info` | `dict` | Repository metadata | Provided by `Manager`; keys: `code_mix`, `full_data`, `global_info`, `language`, … |
| `model` | `Model` | LLM wrapper | Handles key rotation, history, and HTTP calls. |
| `progress` | `BaseProgress` | UI progress | Tracks sub‑task count and updates. |
| `doc_head` | `DocHeadSchema` | Result container | Holds named `DocContent` entries. |

---
<a name="doc-schemas"></a>
## Documentation Data Structures

```python
class DocContent(BaseModel):
    content: str
```

- Holds a raw markdown fragment.

```python
class DocHeadSchema(BaseModel):
    content_orders: list[str] = []
    parts: dict[str, DocContent] = {}

    def add_parts(self, name, content: DocContent):
        ...

    def get_full_doc(self, split_el: str = "\n") -> str:
        ...
    def __add__(self, other: "DocHeadSchema") -> "DocHeadSchema":
        ...
```

- **Ordering** – `content_orders` preserves insertion order for deterministic rendering.  
- **Merging** – `__add__` concatenates two schemas, ensuring no key clashes by renaming.  

```python
class DocInfoSchema(BaseModel):
    global_info: str = ""
    code_mix: str = ""
    doc: DocHeadSchema = Field(default_factory=DocHeadSchema)
```

- Aggregates the global metadata, source mix, and generated documentation.

> > **Warning** – All schemas derive from *pydantic* and are serialisable via `dict()`. No custom validation beyond field types.
<a name="generete-custom-discription"></a>
### `generete_custom_discription(splited_data: str, model: Model, custom_description: str, language: str = "en") → str`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `splited_data` | `str` | Iterable of code snippets | The function iterates over it, treating each element as a chunk (likely intended to be a list). |
| `model` | `Model` | LLM wrapper | `get_answer_without_history`. |
| `custom_description` | `str` | Prompt text | Task description for the LLM. |
| `language` | `str` | Target language | System instruction. |
| `result` | `str` | Accumulated answer | Returned when a valid response is found. |

**Logic Flow**  
1. Loop over `splited_data`.  
2. For each `sp_data`, build a prompt with context, `BASE_CUSTOM_DISCRIPTIONS`, and the task.  
3. Query the LLM.  
4. If the answer does **not** contain `!noinfo` or “No information found”, or if `!noinfo` occurs past 30 chars, break the loop.  
5. Return the first satisfactory `result`.  

> **Result** – A concise description generated for the supplied custom task, or an empty string if no info is available.  

---
<a name="generete-custom-discription-without"></a>
### `generete_custom_discription_without(model: Model, custom_description: str, language: str = "en") → str`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | LLM wrapper | Calls `get_answer_without_history`. |
| `custom_description` | `str` | Prompt text | Task description for the LLM. |
| `language` | `str` | Target language | System instruction. |

**Logic Flow**  
1. Construct a prompt that includes a strict rule block: the answer must begin with a single `
<a name="gen-doc-parts"></a>
## `gen_doc_parts` – Orchestrator

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `full_code_mix` | `str` | All source text | Input to be split. |
| `max_symbols` | `int` | Size threshold | Determines chunk boundaries. |
| `model` | `Model` | LLM wrapper | Same contract as above. |
| `project_settings` | `ProjectSettings` | Configuration holder | Provides `prompt`. |
| `language` | `str` | Target language | |
| `progress_bar` | `BaseProgress` | UI feedback | Can be a concrete implementation. |
| `global_info` | `str | None` | Repository‑wide metadata | |

### Workflow

1. **Split** – `split_data(full_code_mix, max_symbols)` produces a list of chunks.  
2. **Progress** – `create_new_subtask` tracks number of chunks.  
3. **Iterate** – For every chunk:
   * Call `write_docs_by_parts`.
   * Append result to `all_result`.
   * Keep only the last 3 k characters of the current result for context in the next call (`result = result[len(result) - 3000:]`).  
   * Update progress.
4. **Finalize** – Remove subtask, log total length, and return `all_result`.

### Edge Cases

| Scenario | Current Behaviour | Notes |
|----------|-------------------|-------|
| `split_data` returns empty list | No iterations; `all_result` is empty | No docs produced. |
| `model.get_answer_without_history` throws | Exception propagates | No retry logic in this layer. |
| `progress_bar` is a stub | Silent execution | Progress not displayed. |
<a name="global-info-generation"></a>
### `generate_global_info`

| Parameter | Default | Role |
|-----------|---------|------|
| `compress_power` | `4` | Compression aggressiveness |
| `max_symbols` | `10000` | Token‑size of initial chunk |

**Flow**

1. `split_data(full_code_mix, max_symbols)` – chunk the code mix.  
2. `compress_to_one` – feeds chunks to `llm_model` with project settings; returns a single‑string global doc fragment.  
3. Persist fragment to `global_info.md`.  
4. Store in `self.doc_info.global_info`.  
5. Log and advance progress.

> **Note** – `compress_power` controls how many top‑level sections the compressor keeps.  

---
<a name="parts-generation"></a>
### `generete_doc_parts`

| Parameter | Default | Role |
|-----------|---------|------|
| `max_symbols` | `5_000` | Max chunk size for part generation |
| `with_global_file` | `False` | Whether to prepend global content |

**Sequence**

1. Read the cached `global_info` file (ignores passed `with_global_file`).  
2. Call `gen_doc_parts` with:  
   * `full_code_mix`  
   * `max_symbols`  
   * `llm_model`  
   * project settings from `config`  
   * language from `config`  
   * progress bar  
   * `global_info` payload.  
3. Persist raw output to `output_doc.md`.  
4. Split output into sections by anchors (`split_text_by_anchors`).  
5. Store each section into `self.doc_info.doc` (`DocContent`).  

> **Output** – The fully stitched Markdown string, later refined by post‑processors.

---
<a name="write-docs"></a>
## `write_docs_by_parts` – One‑Chunk LLM Pass

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | Raw code fragment | Must be a single chunk from `gen_doc_parts`. |
| `model` | `Model` | LLM wrapper | Exposes `get_answer_without_history`. |
| `project_settings` | `ProjectSettings` | Configuration holder | Supplies `prompt` and other constants. |
| `prev_info` | `str | None` | Last LLM output | Used as context for the following chunk. |
| `language` | `str` | Target language | e.g., `"en"`. |
| `global_info` | `str | None` | Repository‑wide metadata | Injected into system messages. |

### Prompt Assembly

1. **System messages** – three entries:
   * Language directive (`"For the following task use language {language}"`).
   * Global project metadata (`project_settings.prompt`).
   * Pre‑defined completion template (`BASE_PART_COMPLITE_TEXT`).
2. **Optional system messages** – appended when `global_info` or `prev_info` exist.
3. **User message** – the actual `part` of source code.

> > **Important** – The LLM receives *no history*; each chunk is independent except for `prev_info`, which is supplied as a system prompt.

### Response Handling

```python
answer: str = model.get_answer_without_history(prompt=prompt)
temp_answer = answer.removeprefix("```")
```

- Removes leading triple backticks that some LLMs prepend.  
- If the response is identical to `temp_answer`, the function returns it directly.  
- Otherwise, trailing ``` fences are stripped and the cleaned string is returned.
<a name="factory-generate"></a>
### `factory_generate_doc`

| Parameter | Type | Role |
|-----------|------|------|
| `doc_factory` | `DocFactory` | Provides a list of `BaseModule` instances |
| `to_start` | `bool` | Determines whether to prepend or append generated content |

**Workflow**

1. Compose a context dictionary:

```python
info = {
    "language": config.language,
    "full_data": curr_doc,           # existing markdown
    "code_mix": self.doc_info.code_mix,
    "global_info": self.doc_info.global_info
}
```

2. Log the module names and input keys.  
3. Invoke `doc_factory.generate_doc(info, llm_model, progress_bar)`.  
4. Merge `result` with `self.doc_info.doc` either at start or end.  
5. Increment progress.

> **Key point** – `DocFactory` internally iterates over its `BaseModule` children, each of which calls the LLM via `generete_custom_discription` or similar functions.

---

<a name="order"></a>
### `order_doc`

| Action | Description |
|--------|-------------|
| Calls `get_order` | Reorders `self.doc_info.doc.content_orders` according to LLM‑generated suggestions. |

> **Result** – Final section ordering is stored in `doc_info.doc`.

---
<a name="cross-module-interactions"></a>  
## Cross‑Module Interactions

* **`sorting.py`** imports `Model` from `engine.models.model` and logging classes from `ui.logging`.  
* **`extract_links_from_start`** and **`split_text_by_anchors`** work together to convert a raw Markdown document into an anchor‑based mapping.  
* **`get_order`** relies on a `Model` implementation that implements `get_answer_without_history`; no internal state is mutated.  
* **`CodeMix`** uses `fnmatch` for ignore logic and logs via `BaseLogger`; it is independent of any LLM components.  
* All modules expose purely functional logic; any persistence or higher‑level orchestration occurs elsewhere in the Auto‑Doc Generator pipeline.
<a name="inter-module-communication"></a>
## Cross‑Module Interactions

| Component | Interaction |
|---|---|
| `compress` → `engine.models.model.Model` | Calls `get_answer_without_history(prompt)` to obtain LLM output. |
| `compress` → `engine.config.config.get_BASE_COMPRESS_TEXT` | Generates a system instruction based on input length and compression power. |
| `compress_and_compare` → `BaseProgress` | Creates a sub‑task and updates it per iteration. |
| `compress_to_one` → `compress_and_compare` | Re‑uses it to progressively merge data. |
| `ProjectSettings` → `compress` / `compress_and_compare` | Supplies `project_settings.prompt` for system messages. |

> **Note** – All imports are explicit; no implicit external library usage beyond those declared.

---
<a name="interactions"></a>
### Cross‑Module Interactions  

* Uses `BASE_INTRODACTION_CREATE_LINKS`, `BASE_INTRO_CREATE`, `BASE_CUSTOM_DISCRIPTIONS` from `engine.config.config`.  
* Relies on `GPTModel` (subclass of `Model`) to perform LLM calls.  
* Logs via `BaseLogger`/`InfoLog`; no error handling is performed—exceptions bubble to the caller.  
* Functions are pure helpers; no state is held within the module.  

---

<a name="notes"></a>
### Observations  

* `generete_custom_discription` iterates over a `str`, which likely is an unintended bug if a list of strings is expected.  
* All functions return raw LLM responses; downstream code is responsible for formatting and integration.  
* Logging verbosity can be adjusted through `InfoLog` level parameter.  

---
<a name="ignore-list"></a>  
## Default Ignore List

| Pattern | Effect |
|---------|--------|
| `*.pyo`, `*.pyd`, `*.pdb`, `*.pkl`, `*.log`, `*.sqlite3`, `*.db` | Binary and log files |
| `venv`, `env`, `.venv`, `.env`, `.vscode`, `.idea`, `*.iml`, `.gitignore`, `.ruff_cache` | Virtual environments, IDE files, caching |
| `*.pyc`, `__pycache__`, `.git`, `.coverage`, `htmlcov`, `migrations`, `*.md`, `static`, `staticfiles`, `.mypy_cache` | Compiled Python, CI artifacts, markdown, static assets, type‑check cache |

> **Usage** – Passed to `CodeMix` constructor to exclude unwanted files from the generated content.
<a name="ordering"></a>  
## Semantic Ordering via LLM

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | LLM wrapper | Must expose `get_answer_without_history`. |
| `chanks` | list[str] | Section titles to reorder | Passed directly into the prompt. |
| `logger` | `BaseLogger` | Logging helper | Records start/end of ordering. |
| `prompt` | list[dict] | Messages sent to the LLM | Contains a user role prompt that instructs the model to return a comma‑separated list. |
| `result` | str | Raw LLM output | Returned by `get_answer_without_history`. |
| `new_result` | list[str] | Cleaned, ordered titles | Result of splitting and trimming `result`. |

### Logic Flow  

1. Log the start of ordering and the titles to process.  
2. Build a single user message asking the LLM to sort the titles semantically, keeping `#` prefixes and not adding explanatory text.  
3. Call `model.get_answer_without_history(prompt)`.  
4. Split the returned string on commas, strip whitespace, and store in `new_result`.  
5. Log the final list and return it.

> **Result** – A list of titles in a LLM‑determined semantic order.
<a name="anchor-extraction"></a>  
## Anchor Extraction Logic

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `extract_links_from_start(chunks)` | function | Parses a list of Markdown‑section strings for a leading `<a name="..."></a>` tag. | Returns a list of anchor links (prefixed with `#`) and a boolean indicating whether the first chunk should be discarded. |
| `links` | list[str] | Collected anchor names | Each anchor name longer than 5 characters is considered valid. |
| `have_to_del_first` | bool | Flag for removal of the first chunk | If any chunk lacks a valid anchor, the first chunk is marked for deletion. |

### Logic Flow  

1. Iterate over `chunks`.  
2. For each `chunk`, strip whitespace and search for the regex pattern `^<a name=["\']?(.*?)["\']?>`.  
3. If a match is found and the captured name exceeds five characters, append `#<name>` to `links`.  
4. If no match exists for a chunk, set `have_to_del_first` to `True`.  
5. Return `(links, have_to_del_first)`.

> **Result** – A tuple used by `split_text_by_anchors` to identify and manage anchor boundaries.
<a name="anchor-splitting"></a>  
## Text Splitting by Anchors

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `text` | str | Raw README content | Expected to contain `<a name="..."></a>` anchors. |
| `chunks` | list[str] | Sub‑strings separated by the anchor regex | Derived via `re.split`. |
| `result_chanks` | list[str] | Cleaned, non‑empty chunks | Trims whitespace. |
| `all_links, have_to_del_first` | tuple | Result from `extract_links_from_start` | Determines if the first chunk must be removed. |
| `result` | dict[str, str] | Mapping of anchor link → section text | Returned by the function. |

### Logic Flow  

1. Split `text` at every anchor point using `(?=<a name=...)` (look‑ahead).  
2. Trim whitespace from each resulting chunk.  
3. Invoke `extract_links_from_start` on the cleaned chunks.  
4. Detect if the overall file starts with an anchor or the first chunk should be dropped; if so, `pop(0)`.  
5. Verify that the number of links matches the number of remaining chunks; otherwise raise an exception.  
6. Build a dictionary mapping each `#anchor` to its corresponding section text and return it.

> **Result** – A deterministic mapping of anchors to their associated Markdown sections.
<a name="file-paths"></a>
### File Path Helpers

| Method | Purpose | Notes |
|--------|---------|-------|
| `get_file_path(file_key)` | Resolve absolute cache file path | Uses `FILE_NAMES` mapping |
| `read_file_by_file_key(file_key)` | Load cached content | Returns `None` on failure |

---
<a name="cache-clear"></a>
### `clear_cache`

If the configuration flag `pbc.save_logs` is `False`, the method deletes the cached log file.

---

<a name="save"></a>
### `save`

Writes the fully assembled documentation (`self.doc_info.doc.get_full_doc()`) to `output_doc.md` in the cache directory.

---
<a name="exception-handling"></a>
### Error Handling

* `read_file_by_file_key` swallows all exceptions and returns `None`.  
* All LLM calls inside other methods propagate `ModelExhaustedException` if no key remains.  
* No explicit `try/except` around network or file operations beyond the minimal wrapper, keeping responsibility at the caller level.

---
<a name="conclusion"></a>
## Summary of Manager Responsibilities

1. **Cache Management** – Creates and cleans `.auto_doc_cache`.  
2. **Source Aggregation** – Produces a single `code_mix` string from the repo.  
3. **Global Compression** – Condenses the entire code mix into one Markdown snippet.  
4. **Chunked Generation** – Breaks the mix into manageable parts, queries the LLM, stitches results.  
5. **Factory‑based Expansion** – Allows plug‑in modules to add or modify sections.  
6. **Ordering & Persistence** – Orders sections and writes the final `README.md`.  

All interactions are strictly local or via the provided `Model` and `DocFactory` interfaces; no external services are invoked outside of the LLM wrapper.
<a name="edge-cases"></a>
## Edge Cases & Error Handling

| Scenario | Current Behavior | Potential Issue |
|---|---|---|
| `data` contains more than `compress_power` items | Processed in multiple passes | None |
| LLM returns empty string | `compress` returns an empty string | Missing documentation content |
| `progress_bar` is the base class (no UI) | Operations run silently | UI feedback unavailable |
| `model.get_answer_without_history` raises an exception | Propagates upwards | No retry logic implemented |

---
<a name="imports"></a>
## `autodocgenerator.postprocessor.custom_intro` – Module Overview  

This module provides helper utilities for enriching the generated Markdown with hyperlinks, introductory text, and custom‑section descriptions.  All LLM interactions are delegated to a `Model` instance passed in as an argument.  Logging is performed via the singleton `BaseLogger`.  

---
<a name="overall-summary"></a>
## Summary

This fragment delivers a **logging singleton** and **progress reporting** utilities, together with a **PowerShell bootstrapper** that scaffolds GitHub Actions and configuration files for the Auto‑Doc Generator. All classes are lightweight, rely only on the standard library (plus `rich` for CLI progress), and expose a consistent API for the rest of the pipeline.
<a name="summary"></a>
## Summary

The provided fragment implements the **chunk‑based documentation pipeline**:

1. **Chunking** – Splits raw source into size‑bounded parts, ensuring no individual chunk exceeds a token‑like limit.  
2. **LLM Pass** – Each part is sent to a configured GPT model (`Model`) with a rich system prompt derived from `ProjectSettings` and optional contextual messages.  
3. **Aggregation** – Results are concatenated, trimmed, and returned as a single markdown string.  
4. **Schema** – Generated fragments are wrapped in `DocHeadSchema`/`DocInfoSchema` for later assembly.

All interactions are pure except for logger and progress updates, keeping the core logic deterministic and testable.
<a name="example-flow"></a>
## Example Call Sequence

```python
# Inside Manager.generate_doc_parts
gpt = GPTModel()
answer = gpt.generate_answer(
    with_history=True,
    prompt=[{"role":"user","content":"Explain this function"}]
)
```

1. `generate_answer` pulls the current conversation history.  
2. Iterates over `regen_models_name` and `api_keys`.  
3. On success, returns Markdown string; on total exhaustion, propagates `ModelExhaustedException`.  

---
<a name="limitations"></a>
## Constraints & Observations

- **Async Support** – `AsyncGPTModel` is a placeholder; the asynchronous logic remains unimplemented.  
- **Error Handling** – Generic `Exception` is caught; specific Groq errors are not distinguished.  
- **Logging Level** – `Answer: {result}` is logged at level 2; consumers can tune verbosity via `BaseLogger`.  

---
<a name="observations"></a>  
## Observations & Edge Cases

* `extract_links_from_start` assumes the anchor appears at the start of a chunk; any deviation may lead to `have_to_del_first` being `True`.  
* `split_text_by_anchors` raises a generic `Exception` if anchor–chunk counts mismatch. No recovery strategy is included.  
* `get_order` expects the LLM to honor the instruction “leave # in title”; malformed output will be included as‑is.  
* `CodeMix.build_repo_content` writes a literal newline `"\n\n"` after each file block; if a file contains this pattern, duplication may occur.  
* All logging levels are set to `level=1` or default; higher granularity is not provided in the snippets.  

---
<a name="autodocconfig-options"></a>  
The file defines several top‑level keys:

* **project_name** – the title of the documentation set.  
* **language** – the language to use for generated text.  

* **ignore_files** – a list of glob patterns that will be skipped by the generator. Typical values include cache directories, byte‑code, virtual env folders, database files, logs, git artefacts, IDE folders and markdown files.  

* **build_settings** – controls the build process:  
  * **save_logs** – Boolean to keep or discard the log file.  
  * **log_level** – numeric verbosity (e.g., 2).  

* **structure_settings** – governs the layout of the output:  
  * **include_intro_links** – add hyperlinks to the introduction.  
  * **include_intro_text** – add explanatory introductory text.  
  * **include_order** – maintain a defined order for sections.  
  * **use_global_file** – whether to pull content from a shared file.  
  * **max_doc_part_size** – maximum character count per document chunk (here 5000).  

* **project_additional_info** – free‑form fields, such as a project “global idea” description.  

* **custom_descriptions** – a list of template strings that can contain placeholders and are inserted into the final documentation. The example items illustrate installing the generator, describing configuration options, and using the Manager class.
