**Auto Doc Generator – Project Overview**

---

### 1. Project Title  
**Auto Doc Generator**

---

### 2. Project Goal  

The purpose of *Auto Doc Generator* is to relieve developers from the repetitive, manual work of writing project documentation.  
Given a repository and a tiny `autodocconfig.yml` file, the tool automatically extracts source‑code, creates a concise high‑level summary, splits the material into LLM‑friendly chunks, asks a large language model to produce markdown fragments, and finally assembles a polished `README.md`.  
In short, it turns a raw codebase into a ready‑to‑publish documentation file with zero human‑written prose.

---

### 3. Core Logic & Principles  

| Phase | What Happens | Main Classes / Modules |
|-------|--------------|------------------------|
| **Configuration** | The CLI reads `autodocconfig.yml`. The parser builds a immutable `Config` object, a collection of `CustomModule` definitions, and a `StructureSettings` object that governs chunk size, ordering, and intro sections. | `autodocgenerator.auto_runner.config_reader`, `autodocgenerator.config.config.Config` |
| **Pre‑processing** | 1. **CodeMix** walks the repository, respects ignore patterns, and writes a single *repo‑mix* file that contains the directory tree and raw source. <br>2. **Compressor** sends the mix to the LLM (via `GPTModel` / `AsyncGPTModel`) and receives a compact project‑wide summary. <br>3. **Spliter** breaks the summary (or the raw mix) into chunks that respect the `max_symbols` limit configured by the user. | `preprocessor.code_mix`, `preprocessor.compressor`, `preprocessor.spliter` |
| **LLM Generation** | For every chunk a prompt is built from the global `ProjectSettings.prompt` (which already embeds language, project name, etc.) and the chunk’s content. The prompt is sent to the LLM wrapper; the response is a markdown fragment. Custom modules defined in the config are also processed at this stage, allowing users to inject bespoke sections that are still rendered by the LLM. | `engine.models.GPTModel`, `engine.models.AsyncGPTModel`, `DocFactory`, `CustomModule`, `CustomModuleWithOutContext` |
| **Post‑processing** | The generated fragments are concatenated into a temporary `output_doc.md`. Anchor tags (`<a name="…"></a>`) are extracted, then a second LLM call determines the semantically optimal ordering of those sections (or respects a user‑provided order). Static intro fragments (`IntroLinks`, `IntroText`) are prepended, and the final markdown is written to `README.md`. | `postprocessor.sorting`, `postprocessor.custom_intro`, `IntroLinks`, `IntroText` |
| **Orchestration & UI** | `Manager` coordinates every step, keeping an internal cache (`.auto_doc_cache`) that stores intermediate files (code mix, global summary, per‑chunk docs). A progress bar (`ConsoleGtiHubProgress`) and a global logger (`ui.logging`) give real‑time feedback, especially useful in CI pipelines. | `autodocgenerator.auto_runner.run_file`, `Manager`, `ConsoleGtiHubProgress`, `BaseLogger` |
| **Error handling** | If the list of LLM models is exhausted, a `ModelExhaustedException` bubbles up to the CLI, which exits with a clear message. Shared `History` and `ParentModel` objects allow fallback to alternative models without losing context. | `ModelExhaustedException`, `History`, `ParentModel` |

**Key Architectural Principles**

* **Pipeline‑first design** – each stage receives a well‑defined artifact, transforms it, and passes it downstream.  
* **Configuration‑driven** – all behaviour (ignore patterns, language, chunk size, custom sections) lives in a single YAML file; the code itself never hard‑codes project specifics.  
* **Stateless LLM wrappers** – `GPTModel` and `AsyncGPTModel` expose a single method (`get_answer_without_history`) that receives a prompt and returns a response, keeping the model layer thin and replaceable.  
* **Cache‑based intermediate storage** – the `.auto_doc_cache` directory guarantees that a failure in a later stage does not require re‑running the entire pipeline.  
* **Extensibility via Custom Modules** – users can drop a Python file that implements a `process` method; the factory will call it, letting the LLM enrich the custom text.  

---

### 4. Key Features  

- **One‑command generation** – `python -m autodocgenerator.auto_runner.run_file` launches the full pipeline.  
- **YAML‑based configuration** – `autodocconfig.yml` defines ignore patterns, project language, chunk size, ordering preferences, and custom modules.  
- **Automatic code extraction** – walks the repository, filters by patterns, and produces a unified source view (`code_mix.txt`).  
- **LLM‑powered summarisation** – compresses the entire codebase into a concise global description.  
- **Chunked processing** – splits large inputs into token‑safe pieces, guaranteeing that every LLM request stays within model limits.  
- **Customizable sections** – users can inject arbitrary prose (e.g., “Installation”, “Contribution Guidelines”) that the LLM formats automatically.  
- **Semantic re‑ordering** – after generation, anchors are extracted and a second LLM call decides the most logical section order.  
- **Progress reporting & logging** – console‑based progress bar and structured logs help debug and monitor CI runs.  
- **Cache persistence** – intermediate files (`code_mix.txt`, `global_info.md`, `report.txt`, `output_doc.md`) survive crashes, allowing a quick resume.  
- **Async support** – `AsyncGPTModel` enables concurrent LLM calls for large projects, reducing overall runtime.  
- **Graceful fallback** – if a model becomes unavailable, `ModelExhaustedException` triggers a clean shutdown with a helpful error message.  

---

### 5. Dependencies  

| Dependency | Purpose | Minimum Version |
|------------|---------|-----------------|
| **Python** | Runtime language | 3.9+ |
| **groq** (or any Groq‑compatible client) | Communicates with the Groq LLM endpoint | 0.1.0 |
| **PyYAML** | Parses `autodocconfig.yml` | 6.0 |
| **tqdm** (or similar) | Displays progress bars in the console | 4.65 |
| **rich** (optional) | Fancy logging/pretty console output | 13.0 |
| **aiohttp** (optional) | Asynchronous HTTP calls for `AsyncGPTModel` | 3.9 |
| **click** (or built‑in `argparse`) | CLI argument handling (if used) | 8.1 |
| **pathspec** | Advanced file‑ignore pattern matching (git‑style) | 0.11 |
| **pytest** (dev) | Test suite | 7.0 |
| **black / isort / flake8** (dev) | Code formatting and linting | – |

*All external libraries are listed in `requirements.txt` and are installed via `pip install -r requirements.txt`.*

---

**In summary**, *Auto Doc Generator* is a fully‑configurable, pipeline‑oriented Python tool that leverages LLMs (through the Groq API) to turn any code repository into a high‑quality `README.md`. Its modular design, clear separation of concerns, and rich extensibility make it suitable for both individual developers and automated CI/CD environments.

## Executive Navigation Tree
- 📂 Setup
  - [Install Workflow Setup](#install-workflow-setup)
- ⚙️ Configuration
  - [Structure Settings](#structure-settings)
  - [Config Reader Read Config](#config-reader-read-config)
  - [Config Classes](#config-classes)
  - [Projectsettings Module](#projectsettings-module)
  - [Project Metadata](#project-metadata)
  - [Autodoc Yaml Options](#autodoc-yaml-options)
- 📄 Documentation
  - [CONTENT DESCRIPTION](#CONTENT_DESCRIPTION)
  - [Codemix Repo Builder](#codemix-repo-builder)
  - [Docfactory](#docfactory)
  - [Run File Gen Doc](#run-file-gen-doc)
  - [Write Docs By Parts Function](#write-docs-by-parts-function)
  - [Gen Doc Parts Function](#gen-doc-parts-function)
- 📂 Modules
  - [Basemodule](#basemodule)
  - [Custom Modules](#custom-modules)
  - [Intro Modules](#intro-modules)
  - [Custom Intro Module](#custom-intro-module)
  - [Module Initializer](#module-initializer)
  - [Compressor Module](#compressor-module)
  - [Spliter Module](#spliter-module)
  - [Manager Class Operations](#manager-class-operations)
  - [Manager Orchestration Core](#manager-orchestration-core)
- ⚙️ Execution
  - [Module Execution](#module-execution)
  - [Visible Interactions](#visible-interactions)
  - [Technical Logic Flow](#technical-logic-flow)
  - [Function Print Welcome](#function-print-welcome)
- 🤖 Models
  - [Model Base](#model-base)
  - [GPTModel Sync](#gptmodel-sync)
  - [AsyncGPTModel Async](#asyncgptmodel-async)
- 📊 Data
  - [Data Contract](#data-contract)
  - [Sorting Anchor Extraction Ordering](#sorting-anchor-extraction-ordering)
  - [Split Data Function](#split-data-function)
- 🛠️ Logging & Progress
  - [Logging Infrastructure](#logging-infrastructure)
  - [Baseprogress Abstract](#baseprogress-abstract)
  - [Libprogress Rich](#libprogress-rich)
  - [Consolegtihubprogress CLI](#consolegtihubprogress-cli)

 

<a name="install-workflow-setup"></a>

**Overview**  
To set up the automated installation workflow you need to execute a PowerShell installer on Windows platforms and a Bash installer on Linux‑based platforms. The workflow also requires a secret named `GROCK_API_KEY` in the repository’s GitHub Actions settings, populated with the API key obtained from the Grock documentation site.

**Steps for Windows (PowerShell)**  

1. Open PowerShell with administrative privileges.  
2. Run the following one‑liner, which fetches the installer script directly from the repository and executes it in the current session:  

   ```powershell
   irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
   ```

   - `irm` (alias for `Invoke-RestMethod`) downloads the script.  
   - The pipeline (`|`) passes the script content to `iex` (`Invoke-Expression`) for immediate execution.  

3. Follow any prompts shown by the installer to complete the setup.

**Steps for Linux/macOS (Bash)**  

1. Open a terminal.  
2. Execute the following command, which streams the installer script from the repository into the Bash interpreter:  

   ```bash
   curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
   ```

   - `curl -sSL` silently follows redirects and outputs the script.  
   - The pipe sends the script to `bash` for execution.  

3. Respond to any interactive questions the script may ask.

**Adding the Required Secret to GitHub Actions**  

1. In your GitHub repository, navigate to **Settings → Secrets and variables → Actions**.  
2. Click **New repository secret**.  
3. Set the **Name** to `GROCK_API_KEY`.  
4. Retrieve your API key from the Grock documentation site at `https://grockdocs.com`.  
5. Paste the key into the **Value** field and save.  

**Result**  
With the installer executed on the appropriate platform and the `GROCK_API_KEY` secret stored, any GitHub Actions workflow that references this secret will be able to communicate with the Grock service and complete the automated deployment or build process. 
<a name="structure-settings"></a>
## `StructureSettings` – Configuration Container  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `include_intro_links` | bool | Toggle inclusion of link section | Default **True** |
| `include_order` | bool | Enable semantic re‑ordering of doc parts | Default **True** |
| `use_global_file` | bool | Generate a global summary file | Default **True** |
| `max_doc_part_size` | int | Max characters per LLM chunk | Default **5 000** |
| `include_intro_text` | bool | Add introductory text module | Default **True** |
| `load_settings` | method | Overwrites attributes from a dict | Mutates instance |

> **Note:** Only keys present in the supplied dict are altered; missing keys retain defaults. 
<a name="config-reader-read-config"></a>
## `read_config` – YAML Parser  

**Purpose:** Convert raw `autodocconfig.yml` content into three runtime objects: `Config`, a list of `CustomModule` instances, and a `StructureSettings` instance.  

**Logic Flow**
1. `yaml.safe_load` → Python dict `data`.  
2. Instantiate `Config()`.  
3. Extract `ignore_files`, `language`, `project_name`, `project_additional_info`.  
4. Build `ProjectBuildConfig` → `load_settings(project_settings)`.  
5. Populate `Config` via fluent setters (`set_language`, `set_project_name`, `set_pcs`).  
6. Append each ignore pattern to `Config.ignore_files`.  
7. Populate additional project info via `add_project_additional_info`.  
8. Translate `custom_descriptions` into module objects:  
   * Prefix “%” → `CustomModuleWithOutContext(custom[1:])`  
   * Otherwise → `CustomModule(custom)`.  
9. Create `StructureSettings()` and apply `load_settings(structure_settings)`.  
10. Return `(config, custom_modules, structure_settings_object)`.

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_data` | `str` | Raw YAML text | Must be UTF‑8 encoded |
| Return tuple | `(Config, list[CustomModule], StructureSettings)` | Packaged configuration | All objects are mutable after creation | 
<a name="config-classes"></a>
## `Config` & `ProjectBuildConfig` – Core Settings Objects  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `ProjectBuildConfig` | class | Holds build‑time flags (`save_logs`, `log_level`) | Loaded via `load_settings`. |
| `Config` | class | Aggregates ignore patterns, language, project name, additional info, and a `ProjectBuildConfig` instance | Provides fluent setters and `get_project_settings()` for downstream use. |

All interactions are strictly defined by the code; no external library behavior is assumed beyond `yaml.safe_load`. 
<a name="projectsettings-module"></a>
## `settings.py` – Project Prompt Builder  

**Responsibility** – Constructs the **system prompt** injected into every LLM call, aggregating static base prompt with project‑specific key/value pairs.  

### Interactions  
- Imported by `compressor.py` and `spliter.py`.  
- Uses constant `BASE_SETTINGS_PROMPT` from `engine.config`.  

### Logic Flow  
1. `ProjectSettings.__init__(project_name)` stores the name and an empty `info` dict.  
2. `add_info(key, value)` populates `info`.  
3. `prompt` property concatenates `BASE_SETTINGS_PROMPT`, the project name line, and each `info` entry as `"key: value"` lines.  

### Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_name` | `str` | Identifier of the target repository | Supplied by CLI config |
| `info` | `dict[str, str]` | Additional metadata (e.g., language, ignore patterns) | Filled via `add_info` |
| `prompt` | `str` (property) | Full system prompt for LLM | Combines base prompt and dynamic info |

--- 
<a name="project-metadata"></a>
## `pyproject.toml` – Project Metadata & Build Configuration  

**Responsibility** – Supplies **static declarative configuration** for the **Auto Doc Generator** package. The file is consumed by *Poetry*, *pip*, and runtime tools (e.g., `importlib.metadata`) to:

1. Register the distribution (`name`, `version`, `description`).  
2. Declare authorship, licensing, and the README target.  
3. Constrain the supported Python interpreter (`requires‑python`).  
4. List *runtime* dependencies required for code execution.  
5. Define the *build system* (`poetry‑core`) used to generate a wheel.

### Technical Logic Flow  

1. **Poetry** parses the TOML document → builds an internal `Project` model.  
2. The model populates `metadata` fields (used for `setup.cfg`‑like output).  
3. Dependency strings are resolved against the current Python environment → lock file (`poetry.lock`).  
4. During `pip install .` the same parser supplies the same values to `setuptools`‑compatible hooks.  
5. At runtime `importlib.metadata.metadata("autodocgenerator")` reads the generated `METADATA` file, which mirrors the entries defined here.

### Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `name` | `str` | Distribution identifier | `"autodocgenerator"` – must be unique on PyPI. |
| `version` | `str` | Semantic version | `"0.9.2.8"` – follows *PEP 440*. |
| `description` | `str` | Human‑readable short summary | Used by package indexes. |
| `authors` | `list[dict]` | Contributor contact data | Each dict contains `name` & `email`. |
| `license` | `dict` | SPDX‑compatible license info | `text = "MIT"`. |
| `readme` | `str` | Path to long description file | `"README.md"`. |
| `requires-python` | `str` | Interpreter constraint | `">=3.11,<4.0"`. |
| `dependencies` | `list[str]` | Runtime requirement specifications | Exact pins (e.g., `rich==14.2.0`). |
| `build-system.requires` | `list[str]` | Packages needed for building the wheel | `["poetry-core>=2.0.0"]`. |
| `build-system.build-backend` | `str` | Entry point for the build backend | `"poetry.core.masonry.api"` |

> **⚠️** No executable code lives in this file; it is **pure data**. Any change requires a new build/release to take effect.

### Visible Interactions  

- **Package managers** (`poetry`, `pip`) read the file to resolve the dependency graph.  
- **CI pipelines** may parse `dependencies` to cache wheels.  
- **Runtime introspection** (`importlib.metadata`) surfaces the declared metadata to the application (e.g., `__version__` helpers).  

*All other project modules reference this configuration indirectly via the packaging tools; the file itself holds no mutable state.* 
<a name="CONTENT_DESCRIPTION"></a>` tag; the raw answer is returned.

> **Assumption:** All `Model` instances correctly implement `get_answer_without_history`; any failure propagates as an exception.

### Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Markdown source containing anchors | Input to `get_all_html_links` |
| `links` | `list[str]` | Extracted `#anchor` strings | Output of `get_all_html_links`, input to `get_links_intro` |
| `model` | `Model` | LLM interface | Required for every generation function |
| `language` | `str` | Language code (default `"en"`) | Included in system prompt |
| `global_data` | `str` | Project‑wide summary | Input to `get_introdaction` |
| `splited_data` | `Iterable[str]` | Chunked source text | Input to `generete_custom_discription` |
| `custom_description` | `str` | User‑defined description request | Used by both custom description functions |
| `result` / `intro_*` | `str` | LLM‑generated markdown fragments | Written downstream by the `DocFactory` pipeline | 
<a name="autodoc-yaml-options"></a>
The YAML file starts with a top‑level key for the project name, for example:

```yaml
project_name: "Your Project Title"
```

Follow it with the programming language used:

```yaml
language: "en"
```

To exclude files and directories from documentation, list them under **ignore_files**:

```yaml
ignore_files:
  - "dist"
  - "*.pyc"
  - "__pycache__"
  - "venv"
  - ".git"
  - "*.md"
  # add any other patterns you want to skip
```

Control the generation process with **build_settings**. Available keys:

- **save_logs** – set to `true` to keep log files, `false` to discard them.
- **log_level** – numeric value (e.g., `1` for minimal, `2` for normal, `3` for verbose).

```yaml
build_settings:
  save_logs: false
  log_level: 2
```

Define the structure of the output using **structure_settings**. Options:

- **include_intro_links** – `true` to add navigation links at the start.
- **include_intro_text** – `true` to include introductory paragraph.
- **include_order** – `true` to keep sections in the order they appear in the source.
- **use_global_file** – `true` to place shared information in a single section.
- **max_doc_part_size** – maximum characters per generated part (e.g., `5000`).

```yaml
structure_settings:
  include_intro_links: true
  include_intro_text: true
  include_order: true
  use_global_file: true
  max_doc_part_size: 5000
```

Add any project‑wide description under **project_additional_info**:

```yaml
project_additional_info:
  global idea: "Brief description of the project's purpose."
```

Finally, provide custom prompts for the generator in **custom_descriptions**. Each entry is a free‑form string describing a documentation task:

```yaml
custom_descriptions:
  - "Explain how to install workflow with install scripts for Windows and Linux."
  - "Explain how to write this YAML file and list available options."
  - "Explain how to use the Manager class with code examples."
```

Combine all sections in a single YAML document, respecting proper indentation, to guide the documentation generator. 
<a name="basemodule"></a>
## `BaseModule` – Abstract LLM Module Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `generate` | `def(info: dict, model: Model) -> str` | Must return a **markdown fragment** produced by the supplied **LLM model**. | Abstract; concrete subclasses implement the call. |

> **Assumption:** All subclasses treat `info` as a key‑value bag supplied by the pipeline and use `model` for any LLM request.

--- 
<a name="custom-modules"></a>
## Custom Description Modules  

| Class | Purpose | LLM Entry Point |
|-------|---------|-----------------|
| `CustomModule` | Wraps a user‑provided **description** and processes the repository mix. | Calls `generete_custom_discription(split_data(...), model, self.discription, language)`. |
| `CustomModuleWithOutContext` | Same description but **without** code context. | Calls `generete_custom_discription_without(model, self.discription, language)`. |

Both receive `info` (expects keys `code_mix`, `language`) and forward the **model** to the post‑processor helpers, which issue the actual LLM request.

--- 
<a name="intro-modules"></a>
## Introductory Modules  

| Class | Purpose | LLM Entry Point |
|-------|---------|-----------------|
| `IntroLinks` | Extracts HTML links from `full_data` and generates a link block. | Calls `get_links_intro(links, model, language)`. |
| `IntroText` | Generates an introductory paragraph from `global_data`. | Calls `get_introdaction(global_data, model, language)`. |

Each module reads specific keys from `info` (`full_data`, `global_data`, `language`) and passes them with the shared `model` to post‑processor functions that perform the LLM interaction. 
<a name="custom-intro-module"></a>
## Custom Intro Module – Link & Description Generation  

**Purpose** – Produces markdown introductions and link lists for the documentation using LLM calls. All functions are pure utilities; they do not modify repository files directly.

### Visible Interactions  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseLogger` | class (ui) | Central logger used by every helper | Writes `InfoLog` entries |
| `Model` / `GPTModel` | class (engine) | LLM wrapper exposing `get_answer_without_history` | Passed explicitly to each generator |
| `get_all_html_links` | function | Scans a markdown string for `<a name="…"></a>` anchors and returns `#anchor` links | Uses regex `r'<a name=["']?(.*?)["']?</a>'` |
| `get_links_intro` | function | Sends a list of links to the LLM to create an introductory paragraph | Prompt composed of `BASE_INTRODACTION_CREATE_LINKS` |
| `get_introdaction` | function | Generates a project‑wide intro from `global_data` using `BASE_INTRO_CREATE` | Returns raw LLM text |
| `generete_custom_discription` | function | Iterates over split chunks, asks the LLM to describe a user‑provided topic until a non‑empty answer is obtained | Stops after first valid response |
| `generete_custom_discription_without` | function | Produces a description without any source context, enforcing a mandatory ` 
<a name="module-initializer"></a>
## `autodocgenerator.__init__` – Startup Banner & Global Logger

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `_print_welcome` | function | Emits a coloured ASCII banner and status line when the package is imported. | Uses inline ANSI escape codes; no external dependencies. |
| `BLUE`, `BOLD`, `CYAN`, `RESET` | local `str` | Colour/formatting tokens for the banner. | Defined inside the function; scoped to `_print_welcome`. |
| `ascii_logo` | local `str` | Multiline string containing the project logo. | Interpolated with colour tokens. |
| `logger` | `BaseLogger` instance | Centralised logger for the library. | Instantiated after the banner; configured with `BaseLoggerTemplate`. |
| `BaseLogger`, `BaseLoggerTemplate`, `InfoLog`, `ErrorLog`, `WarningLog` | imports | Logging utilities re‑exported at package level. | Imported from `autodocgenerator.ui.logging`. |

> **Critical assumption:** The banner is printed *every* time the package is imported; this side‑effect is intentional for user feedback. 
<a name="module-execution"></a>
### Immediate Execution & Exported Symbols
- After defining `_print_welcome`, the module **invokes** it (`_print_welcome()`), ensuring the banner appears on import.
- The module then **re‑exports** logging classes and creates a **module‑level logger**:
  ```python
  from .ui.logging import BaseLogger, BaseLoggerTemplate, InfoLog, ErrorLog, WarningLog
  logger = BaseLogger()
  logger.set_logger(BaseLoggerTemplate())
  ```
  This makes `logger` available to any sub‑module that imports `autodocgenerator`.

**Side‑effects:**  
- Terminal output on import.  
- Global `logger` instance ready for use throughout the package.  

> **Warning:** If the package is imported in a non‑interactive context (e.g., CI without a tty), the ANSI codes may appear as raw escape sequences. Adjust environment or suppress import side‑effects if undesirable. 
<a name="compressor-module"></a>
## `compressor.py` – LLM‑Based Text Compression  

**Responsibility** – Reduces raw code‑mix fragments to compact summaries using the configured **LLM model**.  

### Interactions  
- Receives `project_settings` (from `preprocessor.settings.ProjectSettings`).  
- Calls `model.get_answer_without_history` (wrapper from `engine.models`).  
- Updates a `BaseProgress` instance to report sub‑task progress.  

### Logic Flow  
1. **`compress`** builds a three‑message prompt: system prompt from `project_settings.prompt`, a dynamic system prompt from `get_BASE_COMPRESS_TEXT`, and the user payload `data`.  
2. Sends the prompt to `model.get_answer_without_history`; returns the LLM answer.  
3. **`compress_and_compare`** groups input `data` list into blocks of `compress_power`. For each element it calls `compress`, concatenates results per block, and updates the progress bar.  
4. **`compress_to_one`** repeatedly invokes `compress_and_compare` until a single compressed string remains, adjusting `compress_power` when the remaining list is short.  

### Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` / `list[str]` | Raw text or list of fragments to compress | Passed to `compress` / `compress_and_compare` |
| `project_settings` | `ProjectSettings` | Supplies system prompt and project metadata | Accessed via `.prompt` |
| `model` | `Model` | LLM interface (sync/async) | Uses `get_answer_without_history` |
| `compress_power` | `int` | Block size for grouping fragments | Default 4, may be reduced |
| `progress_bar` | `BaseProgress` | Visual progress reporter | Sub‑task created/updated/removed |
| Return | `str` | Fully compressed markdown | Output of `compress_to_one` |

> **Warning** – If `compress_and_compare` receives an empty list, it returns a list of empty strings; subsequent loops may produce an empty final result.

--- 
<a name="spliter-module"></a>
## `spliter.py` – Chunking for LLM Consumption  

**Responsibility** – Splits a large markdown string into size‑constrained chunks (`max_symbols`) suitable for LLM prompts.  

### Interactions  
- Consumes `ProjectSettings` for prompt construction (future steps not shown).  
- Uses `BaseProgress` and logging utilities for runtime visibility.  

### Logic Flow (present portion)  
1. `split_data(data, max_symbols)` initializes `split_objects`.  
2. **(Implementation truncated)** – The function will later divide `data` at logical boundaries while respecting `max_symbols`.  

### Data Contract (extracted)  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Full markdown to be chunked | May contain anchor tags |
| `max_symbols` | `int` | Upper token/character limit per chunk | Drives split granularity |
| Return | `list[str]` | Ordered list of chunk strings | Consumed by downstream doc generation |

> **Note** – Only the signature and initial variable setup are visible; further processing is not documented here. 
<a name="manager-class-operations"></a>
**Using the `Manager` class**

```python
from autodocgenerator.manage import Manager
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.general_modules import CustomModule, CustomModuleWithOutContext

# 1. Prepare required objects
project_path = "."                         # path to the root of the project
config = ...                               # an instance of Config (filled elsewhere)
sync_model = GPTModel(API_KEY, use_random=False)
async_model = AsyncGPTModel(API_KEY)
progress = ConsoleGtiHubProgress()

# 2. Create the manager
manager = Manager(
    project_path,
    config=config,
    sync_model=sync_model,
    async_model=async_model,
    progress_bar=progress,
)

# 3. Run the main generation steps
manager.generate_code_file()                         # scans the project and creates internal code representation
manager.generate_global_info(compress_power=4)       # optional: builds a global information file
manager.generete_doc_parts(                          # splits documentation into parts
    max_symbols=5000,                                 # maximum size of each part
    with_global_file=True
)

# 4. Apply custom documentation modules (if any)
custom_modules = [
    CustomModule("...description..."),
    CustomModuleWithOutContext("...description without context...")
]
manager.factory_generate_doc(DocFactory(*custom_modules))

# 5. Optional ordering of the generated documentation
manager.order_doc()

# 6. Add introductory modules (e.g., intro text, links)
from autodocgenerator.factory.modules.intro import IntroText, IntroLinks
intro_modules = [IntroText(), IntroLinks()]
manager.factory_generate_doc(DocFactory(*intro_modules))

# 7. Clean up temporary data
manager.clear_cache()

# 8. Retrieve the final documentation
output = manager.read_file_by_file_key("output_doc")
print(output)
```

**Key `Manager` methods**

| Method | Purpose |
|--------|---------|
| `generate_code_file()` | Scans the project directory, respects ignore patterns, and builds an internal representation of source files. |
| `generate_global_info(compress_power: int)` | Creates a global information file; `compress_power` controls the level of compression. |
| `generete_doc_parts(max_symbols: int, with_global_file: bool)` | Splits the documentation into chunks limited by `max_symbols`. If `with_global_file` is `True`, the global file is included in each part. |
| `factory_generate_doc(factory: DocFactory)` | Generates documentation using a `DocFactory` built from provided modules. |
| `order_doc()` | Reorders the generated sections according to the configured order logic. |
| `clear_cache()` | Removes temporary files and cached data after generation. |
| `read_file_by_file_key(key: str) -> str` | Returns the content of a generated file identified by `key` (e.g., `"output_doc"`). |

These examples show a typical workflow: instantiate `Manager`, run the generation pipeline, optionally add custom or introductory modules, and finally retrieve the assembled documentation. 
<a name="manager-orchestration-core"></a>
## Manager Class – Orchestration Core  

**Responsibility** – Central coordinator that drives the full documentation pipeline: code‑mix creation, global summary compression, chunked doc generation, factory‑based extensions, final ordering, and cache cleanup. 
<a name="visible-interactions"></a>
## Visible Interactions  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `CodeMix` | class (preprocessor) | Builds filtered repository mix file | Writes to `code_mix.txt` |
| `split_data` / `compress_to_one` | functions (preprocessor) | Split raw mix, compress to a single summary | Uses `self.sync_model` |
| `gen_doc_parts` | function (preprocessor) | Generates docs per chunk, optionally prepends global summary | Returns markdown string |
| `DocFactory` | class (factory) | Applies custom modules (`IntroLinks`, `IntroText`, `CustomModule`) to augment docs | Receives `info` dict |
| `split_text_by_anchors` / `get_order` | functions (postprocessor) | Extracts `<a name="…"></a>` anchors, asks LLM for semantic ordering | Returns reordered markdown |
| `BaseLogger` & `BaseProgress` | utilities (ui) | Log messages and update progress bars throughout steps | Config‑driven levels | 
<a name="technical-logic-flow"></a>
## Technical Logic Flow  

1. **Init** – stores `project_directory`, `Config`, models, logger, creates `.auto_doc_cache` if absent.  
2. `generate_code_file` → instantiate `CodeMix`, call `build_repo_content`, write `code_mix.txt`, log & update progress.  
3. `generate_global_info` → read `code_mix.txt`, split via `split_data`, compress with `compress_to_one` (sync LLM), write `global_info.md`.  
4. `generete_doc_parts` → read `code_mix.txt` (+ optional global), invoke `gen_doc_parts` (sync LLM) with language & settings, write `output_doc.md`.  
5. `factory_generate_doc` → load current doc & code mix, build `info` dict (`language`, `full_data`, `code_mix`), call `doc_factory.generate_doc`, prepend result to existing doc, write back.  
6. `order_doc` → split current doc by anchors, request ordering via `get_order`, overwrite `output_doc.md`.  
7. `clear_cache` → optionally delete `report.txt` based on `config.pbc.save_logs`. 
<a name="model-base"></a>
## `Model` Base – History & Model Rotation  

**Responsibility** – Supplies shared **history**, **API key**, and **model‑selection list** for both sync and async wrappers.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `str` | Auth token for Groq API | Defaults to global `API_KEY` |
| `history` | `History` | Stores system & user messages | Initialized with `BASE_SYSTEM_TEXT` |
| `regen_models_name` | `list[str]` | Candidate model identifiers | Shuffled if `use_random=True` |
| `current_model_index` | `int` | Index of model currently tried | Updated on failure |

**Logic Flow**  
1. `ParentModel.__init__` copies `MODELS_NAME`.  
2. If `use_random`, list is shuffled.  
3. `regen_models_name` holds the rotation order. 
<a name="gptmodel-sync"></a>
## `GPTModel` – Synchronous LLM Wrapper  

**Responsibility** – Sends a **single request** to Groq’s synchronous client and returns the generated text.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `client` | `Groq` | API client for sync calls | Created with `api_key` |
| `logger` | `BaseLogger` | Emits `InfoLog`/`ErrorLog`/`WarningLog` | Logs start, model used, answer |
| `prompt` (method arg) | `str` | User‑supplied message when `with_history=False` | Otherwise uses `history.history` |
| Return | `str` | LLM‑generated answer | Extracted from `chat_completion.choices[0].message.content` |

**Step‑by‑Step**  
1. Log start.  
2. Choose `messages` = history or `prompt`.  
3. Loop: pick `model_name` from `regen_models_name[current_model_index]`.  
4. Call `client.chat.completions.create(messages=model_name)`.  
5. On exception, log warning, advance index (wrap to 0).  
6. When a response arrives, log model and answer, then return content. 
<a name="asyncgptmodel-async"></a>
## `AsyncGPTModel` – Asynchronous LLM Wrapper  

**Responsibility** – Mirrors `GPTModel` but operates with **`await`** using Groq’s async client.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `client` | `AsyncGroq` | Async API client | Created with `api_key` |
| `logger` | `BaseLogger` | Same logging behavior as sync | |
| `prompt` | `str` | Optional override when `with_history=False` | |
| Return | `str` | Generated answer (awaited) | |

**Logic Flow** (identical to sync version, prefixed with `await`):  
- Log generation start.  
- Determine `messages`.  
- Loop through `regen_models_name` attempting async `chat.completions.create`.  
- On failure, log warning and rotate index.  
- Upon success, log model and answer, return the text.  

> **Assumption** – The code presumes `chat_completion.choices[0].message.content` is always present; no guard is added for empty choices.  

These three classes constitute the **LLM interaction layer** used throughout the Auto‑Doc Generator pipeline. 
<a name="data-contract"></a>
## Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_directory` | `str` | Root path of the target repo | Used for all file I/O |
| `config` | `Config` | Immutable settings (ignore patterns, language, logging) | Accessed via `config.get_project_settings()` |
| `sync_model` / `async_model` | `Model` / `AsyncModel` | LLM interface for all generation calls | Must implement `get_answer_without_history` |
| `full_code_mix` | `str` | Raw concatenated source files | Read from `code_mix.txt` |
| `global_result` | `str` | Compressed project summary | Written to `global_info.md` |
| `result` (doc parts) | `str` | Generated markdown fragments | Written to `output_doc.md` |
| `info` dict | `dict[str, str]` | Payload for factories (`language`, `full_data`, `code_mix`) | Size logged per key |

> **Assumption:** All imported functions/classes behave as documented in the project knowledge base; no external side effects are introduced beyond file writes and LLM calls. 
<a name="sorting-anchor-extraction-ordering"></a>
## Sorting – Anchor Extraction & Ordering  

**Responsibility** – Parses a markdown document for `<a name="…"></a>` anchors, builds a mapping of anchor → section text, and asks an LLM to return a semantically‑sorted list of titles.  

**Interactions** –  
- Receives raw markdown **text** from the **Manager** (post‑processor stage).  
- Uses the **Model** (`Model.get_answer_without_history`) to obtain ordering.  
- Returns a concatenated markdown string that the **DocFactory** writes to the final output file.  

**Logic Flow**  
1. `split_text_by_anchors(text)` → regex `(?=<a name=…)` splits the document at each anchor.  
2. `extract_links_from_start(chunks)` → extracts leading anchors (`#anchor`) from each chunk, discarding those ≤ 5 chars.  
3. Validates equal counts; otherwise returns `None`.  
4. Builds `result` dict mapping each `#anchor` to its chunk.  
5. `get_order(model, chanks)` logs start, composes a **user** prompt asking the LLM to “Sort the following titles semantically …”.  
6. Parses the comma‑separated response, reassembles ordered sections, logs each addition, and returns the ordered markdown.  

> **Warning** – If the number of detected anchors does not match the number of chunks, the function aborts and yields `None`, causing downstream steps to skip ordering.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `text` | `str` | Source markdown with anchors | Input to `split_text_by_anchors` |
| `chunks` | `list[str]` | Segments split at anchors | Produced internally |
| `all_links` | `list[str]` | `#anchor` identifiers | Must align with `chunks` |
| `chanks` | `dict[str,str]` | Anchor → section mapping | Output of `split_text_by_anchors` |
| `model` | `Model` | LLM interface | Provides ordering via `get_answer_without_history` |
| `order_output` | `str` | Ordered markdown document | Final return value of `get_order` | 
<a name="codemix-repo-builder"></a>
## CodeMix – Repository Content Builder  

**Responsibility** – Walks the project tree, respects ignore patterns, writes a structural tree followed by each file’s raw content into a single text file (`repomix-output.txt`).  

**Interactions** –  
- Consumes `root_dir` and `ignore_patterns` supplied by **config_reader**.  
- Emits the mixed repository file consumed later by **preprocessor.compressor**.  
- Logs progress via **BaseLogger** (`InfoLog`).  

**Logic Flow**  
1. `should_ignore(path)` → normalises `path` relative to `root_dir` and checks it against each `ignore_patterns` entry using `fnmatch`.  
2. `build_repo_content(output_file)` opens the output, writes a “Repository Structure” header.  
3. Iterates over `root_dir.rglob("*")` (sorted):  
   - If a directory, writes an indented line `dir/`.  
   - If a file and not ignored, writes `<file path="…">` tag, then the file’s raw UTF‑8 text, followed by two newlines.  
   - Errors during file read are captured and written as `Error reading …`.  
4. Logs each ignored path at level 1.  

> **Assumption** – All files are UTF‑8 decodable; unreadable files are recorded but do not halt execution.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `root_dir` | `str`/`Path` | Base directory of the project | Supplied by CLI |
| `ignore_patterns` | `list[str]` | Glob patterns to exclude | Defined in `ignore_list` |
| `output_file` | `str` | Destination mix file | Defaults to `repomix-output.txt` |
| `path` | `Path` | Current file/dir during walk | Processed by `should_ignore` |
| `logger` | `BaseLogger` | Central logging facility | Emits `InfoLog` messages |
| `result file` | `text file` | Structured repository dump | Input for subsequent compression stages | 
<a name="split-data-function"></a>
## `split_data` – Adaptive Chunk Rebalancing  

**Responsibility** – Re‑splits a list of raw file fragments (`splited_by_files`) into size‑controlled `split_objects` so that each chunk respects `max_symbols`.  

**Visible Interactions** – Uses `BaseLogger` for progress messages; no external state is mutated beyond returned list.  

**Logic Flow**  
1. Initialise `split_objects = []`.  
2. **Balancing loop** – while any fragment exceeds `1.5 × max_symbols` it is bisected at `max_symbols/2` and re‑inserted, setting `have_to_change`. Loop repeats until all fragments fit the limit.  
3. Iterate `splited_by_files`, appending each piece to the current chunk; if adding would exceed `1.25 × max_symbols`, start a new chunk.  
4. Log final count and return `split_objects`.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `splited_by_files` | `list[str]` | Raw fragments from previous step | May contain oversized entries |
| `max_symbols` | `int` | Upper bound for chunk size | Drives both balancing & chunk creation |
| Return | `list[str]` | Ordered chunks respecting limits | Consumed by `gen_doc_parts` |

> **Warning** – Over‑large fragments are split at a fixed half‑point; content boundaries (e.g., markdown headings) are not preserved. 
<a name="docfactory"></a>
## `DocFactory` – Generation Orchestrator  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `modules` | `list[BaseModule]` | Ordered collection of LLM‑driven processors. | Provided at construction (`*modules`). |
| `info` | `dict` | Shared data bag (e.g., `code_mix`, `language`). | Passed unchanged to each module. |
| `model` | `Model` | Synchronous LLM wrapper used by every module. | Same instance reused throughout the run. |
| `progress` | `BaseProgress` | Progress‑bar helper. | Creates a sub‑task named **“Generate parts”**. |
| `output` | `str` | Concatenated documentation fragments. | Each fragment appended with a double newline. |

**Logic Flow**  
1. Initialise sub‑task (`progress.create_new_subtask`).  
2. Iterate over `self.modules`.  
3. Call `module.generate(info, model)`.  
4. Append result to `output`.  
5. Log success via `BaseLogger`.  
6. Update progress (`progress.update_task`).  
7. After loop, remove sub‑task and return `output`.

**Visible Interactions** – Directly invokes each module’s `generate`; delegates LLM calls to those modules; writes logs; updates UI progress.

--- 
<a name="run-file-gen-doc"></a>
## `gen_doc` – Orchestrator Entry Point  

**Purpose:** Drive the full documentation pipeline using the objects produced by `read_config`.  

**Step‑by‑Step**
1. Initialise LLM wrappers: `GPTModel` (sync) and `AsyncGPTModel`.  
2. Instantiate `Manager` with project path, `Config`, models, and a `ConsoleGtiHubProgress` bar.  
3. `manager.generate_code_file()` – creates repo‑mix.  
4. If `structure_settings.use_global_file` → `manager.generate_global_info(compress_power=4)`.  
5. `manager.generete_doc_parts(max_symbols=..., with_global_file=...)` – chunk‑splits and LLM‑generates per part.  
6. `manager.factory_generate_doc(DocFactory(*custom_modules))` – runs user‑defined modules.  
7. If `include_order` → `manager.order_doc()` – semantic re‑ordering.  
8. Append optional intro modules (`IntroText`, `IntroLinks`) based on settings and invoke another `factory_generate_doc`.  
9. `manager.clear_cache()` – removes temporary artifacts.  
10. Return final markdown via `manager.read_file_by_file_key("output_doc")`.

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_path` | `str` | Root directory of the target repo | |
| `config` | `Config` | Global pipeline settings | Immutable after creation |
| `custom_modules` | `list[CustomModule|CustomModuleWithOutContext]` | User‑provided description handlers | Order preserved |
| `structure_settings` | `StructureSettings` | Feature toggles & limits | |
| Return | `str` | Fully assembled documentation markdown | Written to `output_doc` cache key | 
<a name="write-docs-by-parts-function"></a>
## `write_docs_by_parts` – LLM‑Driven Part Documentation  

**Responsibility** – Build a system‑user prompt, invoke the LLM (`model.get_answer_without_history`), and return cleaned markdown for a single chunk.  

**Visible Interactions** – Reads `project_settings.prompt`; optionally includes `global_info` and `prev_info`; logs via `BaseLogger`.  

**Logic Flow**  
1. Initialise logger.  
2. Assemble `prompt` list with three mandatory system messages (language, global project info, `BASE_PART_COMPLITE_TEXT`).  
3. Append optional system messages for `global_info` and `prev_info`.  
4. Append the user message containing the chunk `part`.  
5. Call `model.get_answer_without_history(prompt)`.  
6. Strip leading/trailing Markdown fences ````` ```.  
7. Return cleaned answer.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | Chunk to document | Produced by `split_data` |
| `model` | `Model` | LLM interface | Calls `get_answer_without_history` |
| `project_settings` | `ProjectSettings` | Supplies system prompt | Accessed via `.prompt` |
| `prev_info` | `str` |​ Previous part’s tail (optional) | Helps maintain continuity |
| `global_info` | `str` |​ Project‑wide relations (optional) | Injected as extra context |
| Return | `str` | Cleaned documentation fragment | May be empty if LLM returns only fences | 
<a name="gen-doc-parts-function"></a>
## `gen_doc_parts` – End‑to‑End Part Generation  

**Responsibility** – Split the full code‑mix, generate documentation for each chunk, and concatenate results.  

**Visible Interactions** – Calls `split_data`, `write_docs_by_parts`, updates a `BaseProgress` sub‑task, and logs.  

**Logic Flow**  
1. `splited_data = split_data(full_code_mix, max_symbols)`.  
2. Create a progress sub‑task sized to `len(splited_data)`.  
3. For each chunk `el`:  
   * `result = write_docs_by_parts(el, …, prev=result, …)`.  
   * Append `result` to `all_result`.  
   * Keep a 3000‑character tail of `result` for the next iteration (`prev_info`).  
   * Update progress.  
4. Remove sub‑task, log final length, and return `all_result`.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `full_code_mix` | `str` | Entire mixed repository content | Input to splitting |
| `max_symbols` | `int` | Chunk size limit | Propagates to `split_data` |
| `model` | `Model` | LLM wrapper | Shared across parts |
| `project_settings` | `ProjectSettings` | System prompt source | Passed unchanged |
| `language` | `str` | Output language for LLM | E.g., `"en"` |
| `progress_bar` | `BaseProgress` | Visual progress tracker | Sub‑task created/removed |
| Return | `str` | Full assembled documentation markdown | Written later to `output_doc.md` | 
<a name="logging-infrastructure"></a>
## Logging Infrastructure – `BaseLogger` & Log Types  

**Responsibility** – Provide a singleton logger that delegates to a configurable `BaseLoggerTemplate` (console or file).  

**Visible Interactions** – All functions above instantiate `BaseLogger()` and call `.log(InfoLog(...))`.  

**Components**  
* `BaseLog` – base class with `message`, `level`, and formatted output.  
* Sub‑classes `ErrorLog`, `WarningLog`, `InfoLog` prepend timestamp and severity.  
* `BaseLoggerTemplate` – filters by `log_level` and prints.  
* `FileLoggerTemplate` – writes to a file.  
* `BaseLogger` – singleton factory exposing `set_logger` and `log`.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `log_level` | `int` | Minimum severity to emit | `-1` disables filtering |
| `logger_template` | `BaseLoggerTemplate` | Destination for formatted logs | Set via `BaseLogger.set_logger` |
| Return | `None` | Side‑effect: printed or file‑written log line | — | 
<a name="baseprogress-abstract"></a>
## `BaseProgress` – Minimal Progress Interface  

**Responsibility** – Defines the contract used by the pipeline to report incremental work. It exposes three methods that concrete progress reporters must implement: `create_new_subtask(name, total_len)`, `update_task()`, and `remove_subtask()`.  

**Visible Interactions** – All manager‑level loops call `BaseProgress.create_new_subtask` before a batch of LLM requests, invoke `update_task` after each request, and finally `remove_subtask`. No state is stored in this class itself.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `name` | `str` | Sub‑task identifier | Human‑readable label |
| `total_len` | `int` | Expected iteration count | Drives progress bar limits |
| Return | `None` | Side‑effect only | Implementations update UI or console |

--- 
<a name="libprogress-rich"></a>
## `LibProgress` – Rich‑based UI Implementation  

**Responsibility** – Provides a visual progress bar using **rich.Progress** while preserving the abstract API.  

**Logic Flow**  
1. Constructor receives a `Progress` instance and creates a base task `"General progress"` with configurable total (default 4).  
2. `create_new_subtask` registers a new task and stores its handle in `_cur_sub_task`.  
3. `update_task` advances the current sub‑task if present; otherwise it advances the base task.  
4. `remove_subtask` discards the current sub‑task handle, causing subsequent updates to target the base task again.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `progress` | `rich.progress.Progress` | Rendering engine | Provided by caller |
| `total` | `int` | Base task length | Defaults to 4 |
| `_base_task` | `int` | Rich task ID for the base bar | Internal |
| `_cur_sub_task` | `int | None` | Active sub‑task ID | Cleared on removal |

> **⚠️** The class does **not** implement error handling for missing `Progress` objects; callers must ensure a valid instance.

--- 
<a name="consolegtihubprogress-cli"></a>
## `ConsoleGtiHubProgress` – Simple Console Task Reporter  

**Responsibility** – Supplies a lightweight, dependency‑free progress reporter that prints textual updates to stdout.  

**Logic Flow**  
1. Instantiation creates a permanent **General Progress** `ConsoleTask` (`gen_task`).  
2. `create_new_subtask` spawns a fresh `ConsoleTask` for the named sub‑operation, stored in `curr_task`.  
3. `update_task` calls `curr_task.progress()` if a sub‑task exists; otherwise it updates `gen_task`.  
4. `remove_subtask` clears `curr_task`, causing future updates to fall back to the general task.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `curr_task` | `ConsoleTask | None` | Active sub‑task reporter | Created on `create_new_subtask` |
| `gen_task` | `ConsoleTask` | Persistent general progress reporter | Initialized in `__init__` |
| Return | `None` | Side‑effect: printed progress line | Uses `print` |

**ConsoleTask** – Helper class that tracks `current_len`, computes percentage, and emits a formatted line on each `progress()` call.

---  

*All progress reporters conform to the `BaseProgress` contract, enabling the manager to switch UI implementations without code changes.* 
<a name="function-print-welcome"></a>
### `_print_welcome` – Logic Flow
1. Define ANSI colour/format strings (`BLUE`, `BOLD`, `CYAN`, `RESET`).  
2. Build `ascii_logo` with colour placeholders and the literal logo.  
3. Print `ascii_logo` to `stdout`.  
4. Print a status line: `"ADG Library | Status: Ready to work"` coloured with `CYAN`.  
5. Print a separator line (`'—' * 35`).  

The function has **no parameters**, **returns `None`**, and **produces side‑effects** (terminal output). 
