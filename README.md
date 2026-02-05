## Executive Navigation Tree
- 📘 Introduction
  - [Basic Introduction](#basic-introduction)
  - [Intro Text](#intro-text)
  - [Intro Links](#intro-links)
  - [Intro With Links](#intro-with-links)
  - [CONTENT DESCRIPTION](#CONTENT_DESCRIPTION)
- ⚙️ Setup & Configuration
  - [Install Workflow Setup](#install-workflow-setup)
  - [Autodoc Yml Structure](#autodoc-yml-structure)
  - [Read Config](#read-config)
- 🛠️ Core Functions
  - [_Print Welcome Function](#_print_welcome-function)
  - [Logger Initialization](#logger-initialization)
  - [Logging Infrastructure](#logging-infrastructure)
  - [Base Progress](#base-progress)
  - [Lib Progress](#lib-progress)
  - [Console Github Progress](#console-github-progress)
- 📦 Manager
  - [Manager Class](#manager-class)
  - [Manager Class Usage](#manager-class-usage)
- 🧩 Modules
  - [Base Module Abstract](#base-module-abstract)
  - [Custom Module](#custom-module)
  - [Custom Module Without Context](#custom-module-without-context)
  - [Docfactory Orchestrator](#docfactory-orchestrator)
- 🤖 Models
  - [Parent Model](#parent-model)
  - [Gpt Model](#gpt-model)
  - [Async Gpt Model](#async-gpt-model)
  - [Semantic Ordering Llm](#semantic-ordering-llm)
- 📡 Extraction & Processing
  - [Html Link Extraction](#html-link-extraction)
  - [Anchor Extraction Chunk Splitting](#anchor-extraction-chunk-splitting)
  - [Regex Pattern](#["\\\']?(.*?)["\\\']?)
- 📝 Documentation Generation
  - [Gen Doc](#gen-doc)
  - [Gen Doc Parts](#gen-doc-parts)
  - [Write Docs By Parts](#write-docs-by-parts)
  - [Custom Description Template](#custom-description-template)
  - [Custom Description Iterative](#custom-description-iterative)
- 📚 Repository & Mixing
  - [Repository Mixer](#repository-mixer)
- 📦 Compression
  - [Compressor Core Function](#compressor-core-function)
  - [Batch Compression Compare](#batch-compression-compare)
  - [Iterative Full Compression](#iterative-full-compression)
- 🔄 Data Loop
  - [Split Data Loop](#split-data-loop)

 

<a name="basic-introduction"></a>
## Basic Introduction Generation (`get_introdaction`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `global_data` | `str` | Input | Full documentation content. |
| `model` | `Model` | Input | LLM interface. |
| `language` | `str` | Input (default `"en"`) | Language hint. |
| `intro` | `str` | Output | Generated introduction. |

Builds a prompt with `BASE_INTRO_CREATE` and `global_data`, then returns the LLM answer. 
<a name="intro-text"></a>
## `IntroText` – Global Data Intro Builder
**Responsibility** – Generates a textual introduction from `global_data`.  
**Visible Interactions** – Calls `get_introdaction`.  
**Logic Flow** –  
1. `generate(info, model)` →  
   - `intro = get_introdaction(info.get("global_data"), model, info.get("language"))`.  
   - Return `intro`.  

> **Warning:** All modules assume the presence of specific keys (`code_mix`, `full_data`, `global_data`, `language`). Absence results in `None` being passed to downstream functions, which may raise runtime errors if those functions lack internal checks. 
<a name="intro-links"></a>
## `IntroLinks` – HTML Link Intro Builder
**Responsibility** – Extracts HTML links from `full_data` and builds an introductory paragraph.  
**Visible Interactions** – Calls `get_all_html_links`, `get_links_intro`.  
**Logic Flow** –  
1. `generate(info, model)` →  
   - `links = get_all_html_links(info.get("full_data"))`.  
   - `intro_links = get_links_intro(links, model, info.get("language"))`.  
   - Return `intro_links`. 
<a name="intro-with-links"></a>
## Introduction Generation with Links (`get_links_intro`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `links` | `list[str]` | Input | Anchor list from `get_all_html_links`. |
| `model` | `Model` | Input | Provides `get_answer_without_history`. |
| `language` | `str` | Input (default `"en"`) | Language hint for the LLM. |
| `intro_links` | `str` | Output | Generated introductory text. |
| `logger` | `BaseLogger` | Side‑effect | Logs start, completion, and result. |

Creates a prompt containing the language directive, `BASE_INTRODACTION_CREATE_LINKS`, and the stringified `links`. Calls `model.get_answer_without_history` and returns the LLM’s response. 
<a name="CONTENT_DESCRIPTION"></a>` tag with strict naming constraints, then returns the LLM’s response.

> **Warning** – All functions assume the provided `Model` instance implements `get_answer_without_history`. Missing methods will raise `AttributeError`. The logger must be operational; otherwise logging calls will fail. 
<a name="install-workflow-setup"></a>

**PowerShell installation (Windows)**  
Execute the following command in an elevated PowerShell window to fetch and execute the installation script directly from the repository:

```powershell
irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
```

- `irm` (Invoke‑WebRequest) downloads the script content.  
- The pipeline to `iex` (Invoke‑Expression) runs the script in the current session.

**Shell installation (Linux/macOS)**  
Run this one‑liner in a terminal to retrieve and execute the Linux installer:

```bash
curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
```

- `curl -sSL` silently follows redirects and outputs the script.  
- The output is piped to `bash` for immediate execution.

**GitHub Actions secret configuration**  
To enable the workflow to interact with the Grock service, add a secret named `GROCK_API_KEY` to the repository’s GitHub Actions secrets:

1. Navigate to the repository’s **Settings → Secrets and variables → Actions**.  
2. Click **New repository secret**.  
3. Enter **Name**: `GROCK_API_KEY`.  
4. Paste the API key obtained from the Grock documentation.  
5. Save the secret.

The workflow will automatically read `GROCK_API_KEY` from the environment, allowing authenticated calls to the Grock API during execution. 
<a name="autodoc-yml-structure"></a>
The configuration file is a YAML document that defines several top‑level sections:

**Project metadata**  
- `project_name`: a string that specifies the name of the project.  
- `language`: the language code (e.g., `"en"`).

**Files to ignore**  
- `ignore_files`: a list of directory or file names that should be excluded from documentation generation (e.g., `"dist"`).

**Build settings** (`build_settings` block)  
- `save_logs`: boolean, when `true` the generation process stores logs.  
- `log_level`: integer controlling verbosity (e.g., `2`).

**Structure settings** (`structure_settings` block)  
- `include_intro_links`: boolean, adds introductory links if `true`.  
- `include_order`: boolean, keeps the original order of sections when `true`.  
- `max_doc_part_size`: integer, maximum size (in characters) for each documentation part.

**Additional project information** (`project_additional_info` block)  
- Custom key/value pairs, such as `global idea`, provide free‑form description of the project’s purpose.

**Custom descriptions** (`custom_descriptions` block)  
- A list of strings that can contain special instructions or explanatory text. These strings are processed by the generator to enrich the final documentation (e.g., how to install the workflow, how to write the configuration file, how to use the Manager class).

When creating the file, follow standard YAML syntax: use indentation (two spaces) for nested sections, place lists under a dash (`-`), and ensure string values are quoted if they contain special characters. This structure enables the documentation generator to read all required options and produce the desired output. 
<a name="read-config"></a>
## `read_config` – YAML Configuration Parsing  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_data` | `str` | Raw YAML content | Passed by caller |
| `data` | `dict` | Parsed YAML tree | Result of `yaml.safe_load` |
| `config` | `Config` | Central project configuration | Instantiated locally |
| `ignore_files` | `list[str]` | Files/patterns to skip | Defaults from YAML or empty |
| `language` | `str` | Documentation language | Defaults to `"en"` |
| `project_name` | `str` | Identifier for the project | May be `None` |
| `project_additional_info` | `dict` | Arbitrary key‑value pairs | Empty dict if omitted |
| `pcs` | `ProjectBuildConfig` | Build‑time settings container | Populated via `load_settings` |
| `custom_modules` | `list[CustomModule|CustomModuleWithOutContext]` | User‑defined processing hooks | Constructed from `custom_descriptions` |
| `structure_settings_object` | `StructureSettings` | Runtime doc‑structure flags | Loaded from `structure_settings` |

**Logic Flow**  
1. Parse `file_data` with `yaml.safe_load`.  
2. Instantiate a fresh `Config`.  
3. Extract top‑level keys (`ignore_files`, `language`, `project_name`, `project_additional_info`, `build_settings`).  
4. Load build settings into a `ProjectBuildConfig` and attach to `config` via `set_pcs`.  
5. Populate ignore patterns and additional info on `config`.  
6. Build `custom_modules` list, choosing `CustomModuleWithOutContext` when a description starts with `"%"`.  
7. Initialise `StructureSettings`, apply any overrides from YAML.  
8. Return tuple `(config, custom_modules, structure_settings_object)`.

> **Assumption** – All expected YAML sections exist; missing sections yield defaults as coded. 
<a name="_print_welcome-function"></a>
## `_print_welcome` Function Execution  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BLUE`, `BOLD`, `CYAN`, `RESET` | `str` | ANSI colour codes | Used only within this function |
| `ascii_logo` | `str` | Formatted ASCII art | Combines colour codes for visual header |
| `print` (built‑in) | callable | Output side‑effect | Sends logo and status lines to **stdout** |

**Purpose** – Render a coloured ASCII banner and a one‑line status message when the package is imported.  

**Logic Flow**  
1. Define colour constants (`BLUE`, `BOLD`, `CYAN`, `RESET`).  
2. Build `ascii_logo` using an f‑string that inserts the colour constants.  
3. Print the logo, then a line showing *“ADG Library | Status: Ready to work”* with cyan text.  
4. Print a separator line (`'—' * 35`).  

> **Warning** – This function executes at import time, causing I/O side‑effects even if the consumer only needs the library’s API. 
<a name="logger-initialization"></a>
## Logger Initialization  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseLogger` | class | Core logger object | Instantiated as `logger` |
| `BaseLoggerTemplate` | class | Formatting/template provider | Passed to `logger.set_logger` |
| `InfoLog`, `ErrorLog`, `WarningLog` | classes | Log‑level helpers (imported but not used here) | Exported for downstream modules |

**Purpose** – Prepare a singleton‑style logger ready for use throughout the package.  

**Logic Flow**  
1. Import logger classes from `.ui.logging`.  
2. Create `logger = BaseLogger()`.  
3. Apply a default template via `logger.set_logger(BaseLoggerTemplate())`.  

**Interactions** – Subsequent modules import `logger` from this package; they rely on the pre‑configured template for consistent output formatting. No external configuration files are consulted in this fragment.  

---  

*All information is derived exclusively from the provided `autodocgenerator/__init__.py` source.* 
<a name="logging-infrastructure"></a>
## Logging Infrastructure – `BaseLog` Hierarchy & Singleton `BaseLogger`  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseLog` | class | Abstract | Stores `message` and `level`; provides `_log_prefix`. |
| `ErrorLog`, `WarningLog`, `InfoLog` | subclasses | Concrete | Override `format()` with severity tag. |
| `BaseLoggerTemplate` | class | Abstract logger | Holds `log_level`; routes via `global_log`. |
| `FileLoggerTemplate` | subclass | File‑output logger | Writes formatted logs to a file. |
| `BaseLogger` | singleton class | Proxy | Delegates `log()` to assigned `logger_template`. |

**Logic Flow**  
1. `BaseLogger.__new__` ensures a single instance.  
2. `set_logger()` injects a concrete `BaseLoggerTemplate`.  
3. `log()` forwards the `BaseLog` object to `logger_template.global_log`, which respects `log_level`.  

> **Assumption** – A logger template is set before any `BaseLogger.log` call; otherwise an `AttributeError` would occur. 
<a name="base-progress"></a>
## `BaseProgress` – Abstract Progress Interface  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseProgress` | class | Abstract base | Defines the progress API used by the documentation generator. |
| `create_new_subtask` | `method(name: str, total_len: int) → None` | Abstract | Intended to start a child progress track. |
| `update_task` | `method() → None` | Abstract | Advances either the current sub‑task or the base task. |
| `remove_subtask` | `method() → None` | Abstract | Clears the active sub‑task reference. |

**Component Responsibility**  
Provides a minimal contract that concrete progress reporters must implement, allowing the generator to switch between rich‑terminal, console, or other visual back‑ends without code changes.

**Visible Interactions**  
`LibProgress` and `ConsoleGtiHubProgress` inherit from it and are passed to higher‑level functions (e.g., `gen_doc_parts`) as the `progress_bar` argument.

**Technical Logic Flow**  
1. Instantiation does nothing (`__init__` is empty).  
2. Sub‑classes override the three abstract methods to manipulate their own state.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `name` | `str` | Input to `create_new_subtask` | Human‑readable identifier of the sub‑task. |
| `total_len` | `int` | Input to `create_new_subtask` | Expected number of `update_task` calls. |
| `current progress` | internal | Side‑effect | Updated via `update_task`; no external return. |

> **Assumption** – The base class is never used directly; calling its methods without a concrete implementation would raise `NotImplementedError`. 
<a name="lib-progress"></a>
## `LibProgress` – Rich‑Library Progress Implementation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `LibProgress` | class | Concrete `BaseProgress` | Wraps `rich.progress.Progress`. |
| `progress` | `Progress` | Dependency | Provided by the `rich` library. |
| `_base_task` | `int` | Internal | ID of the top‑level “General progress” task. |
| `_cur_sub_task` | `int | None` | Internal | ID of the active sub‑task, if any. |

**Component Responsibility**  
Renders hierarchical progress bars in terminals that support ANSI graphics, tracking overall and per‑chunk documentation generation.

**Visible Interactions**  
- `create_new_subtask(name, total_len)` registers a new rich task and stores its ID.  
- `update_task()` advances either `_cur_sub_task` or `_base_task`.  
- `remove_subtask()` discards the current sub‑task reference, leaving the base task alive.

**Technical Logic Flow**  
1. Constructor receives a `Progress` instance and creates the base task (`total` defaults to 4).  
2. `create_new_subtask` calls `self.progress.add_task(name, total=total_len)` and caches the ID.  
3. `update_task` checks `_cur_sub_task`; if set, updates it, otherwise updates the base task.  
4. `remove_subtask` simply null‑ifies `_cur_sub_task`.  

**Data Contract** – same as abstract plus the internal task IDs. 
<a name="console-github-progress"></a>
## `ConsoleGtiHubProgress` – Simple Console Fallback  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `ConsoleGtiHubProgress` | class | Concrete `BaseProgress` | Prints textual progress to stdout. |
| `gen_task` | `ConsoleTask` | Internal | Represents the overall “General Progress”. |
| `curr_task` | `ConsoleTask | None` | Internal | Active per‑chunk task. |

**Component Responsibility**  
Provides a lightweight, environment‑agnostic progress indicator when the rich library cannot be used (e.g., CI logs).

**Visible Interactions**  
- Mirrors the abstract API: `create_new_subtask`, `update_task`, `remove_subtask`.  
- Delegates actual printing to `ConsoleTask.progress()`.

**Technical Logic Flow**  
1. Instantiation creates a `ConsoleTask` named “General Progress” with 4 steps.  
2. `create_new_subtask` replaces `curr_task` with a new `ConsoleTask`.  
3. `update_task` calls `curr_task.progress()` if a sub‑task exists; otherwise updates `gen_task`.  
4. `remove_subtask` clears `curr_task`, causing subsequent updates to affect the general task again.  

**Data Contract** – identical to the abstract contract; progress is emitted via `print`.  

> **Warning** – This implementation does not persist state beyond the current process; restarting the script will reset all counters. 
<a name="manager-class"></a>
## `Manager` – Orchestrator for Documentation Pipeline  

**Responsibility** – Coordinates preprocessing, LLM‑driven generation, post‑processing and caching for a single project directory.  

**Visible Interactions** –  
- Imports from **preprocessor**, **postprocessor**, **engine.models**, **ui**, **factory**.  
- Uses `BaseProgress`/`LibProgress` for task updates, `BaseLogger` for log emission, `DocFactory` for modular doc assembly.  

**Logic Flow** –  
1. `__init__` stores paths, config, models, logger and ensures a cache folder exists.  
2. `read_file_by_file_key` → open cached file → return its contents.  
3. `get_file_path` → compose absolute path under `CACHE_FOLDER_NAME`.  
4. `generate_code_file` → instantiate `CodeMix`, build repository content into `code_mix.txt`, log start/finish, update progress.  
5. `generate_global_info` → read `code_mix.txt`, split via `split_data`, compress with `compress_to_one`, write `global_info.md`, update progress.  
6. `generete_doc_parts` → optionally read `global_info.md`, call `gen_doc_parts` with sync model & settings, write `output_doc.md`, update progress.  
7. `factory_generate_doc` → read current doc & code mix, build `info` dict, log module list & key sizes, invoke `doc_factory.generate_doc`, prepend result to existing doc, update progress.  
8. `order_doc` → split current doc by anchors, reorder sections via `get_order`, overwrite `output_doc.md`.  
9. `clear_cache` → delete log file if `save_logs` is false.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_directory` | `str` | Input | Root of the target code base. |
| `config` | `Config` | Input | Supplies `ignore_files`, `language`, `pbc.log_level`, `pbc.save_logs`, `get_project_settings()`. |
| `sync_model` / `async_model` | `Model` / `AsyncModel` | Input | LLM interface passed to preprocessors/post‑processors. |
| `progress_bar` | `BaseProgress` | Input/Side‑effect | Must implement `update_task()`. |
| `self.logger` | `BaseLogger` | Side‑effect | Writes to `report.txt` via `FileLoggerTemplate`. |
| Cached files (`code_mix.txt`, `global_info.md`, `output_doc.md`, `report.txt`) | on‑disk | Persistent storage | Created/overwritten by manager methods. |
| `info` (in `factory_generate_doc`) | `dict` | Input to `DocFactory.generate_doc` | Keys: `language`, `full_data`, `code_mix`. |
| Return values | `None` (except `read_file_by_file_key`) | Side‑effects | Methods write files or update progress; only `read_file_by_file_key` returns file contents. |

> **Warning** – The manager assumes all configured keys exist; missing files raise `FileNotFoundError`, and absent config attributes cause `AttributeError`. 
<a name="manager-class-usage"></a>!noinfo 
<a name="base-module-abstract"></a>
## `BaseModule` Abstract Interface
**Responsibility** – Defines the contract for all documentation generation modules.  
**Visible Interactions** – Sub‑classes inherit from this ABC and are invoked by `DocFactory`.  
**Logic Flow** –  
1. Constructor (`__init__`) does nothing (`pass`).  
2. Declares abstract `generate(info: dict, model: Model)` method. 
<a name="custom-module"></a>
## `CustomModule` – Context‑Aware Description Generator
**Responsibility** – Generates a custom description using the supplied `discription` and a code split.  
**Visible Interactions** – Calls `generete_custom_discription`, `split_data`.  
**Logic Flow** –  
1. Store `discription` at init.  
2. `generate(info, model)` →  
   - Retrieve `code_mix` via `info.get("code_mix")`.  
   - Split with `split_data(..., max_symbols=5000)`.  
   - Invoke `generete_custom_discription(split_result, model, self.discription, info.get("language"))`.  
   - Return the resulting string. 
<a name="custom-module-without-context"></a>
## `CustomModuleWithOutContext` – Description‑Only Generator
**Responsibility** – Produces a description without processing source code.  
**Visible Interactions** – Calls `generete_custom_discription_without`.  
**Logic Flow** –  
1. Store `discription`.  
2. `generate(info, model)` →  
   - Invoke `generete_custom_discription_without(model, self.discription, info.get("language"))`.  
   - Return the result. 
<a name="docfactory-orchestrator"></a>
## `DocFactory` Orchestrator
**Responsibility** – Executes a sequence of `BaseModule` instances, aggregates their outputs, and logs progress.  
**Visible Interactions** – Receives a list of module instances, a `Model`, a `BaseProgress` reporter, and uses `BaseLogger`.  
**Logic Flow** –  
1. Store `modules` tuple as list; instantiate `BaseLogger`.  
2. `generate_doc(info, model, progress)`  
   - Initialise `output = ""`.  
   - `progress.create_new_subtask("Generate parts", len(self.modules))`.  
   - Iterate `module` in `self.modules`:  
     - Call `module.generate(info, model)` → `module_result`.  
     - Append `module_result + "\n\n"` to `output`.  
     - Log informational messages with `InfoLog`.  
     - `progress.update_task()`.  
   - End loop → `progress.remove_subtask()`.  
   - Return aggregated `output`.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `info` | `dict` | Input data (code snippets, language, etc.) | Keys accessed via `info.get(...)` in modules. |
| `model` | `Model` | LLM interface used by modules | Passed unchanged to post‑processor calls. |
| `progress` | `BaseProgress` | Progress tracking object | Must implement `create_new_subtask`, `update_task`, `remove_subtask`. |
| `module_result` | `str` | Partial documentation fragment | Concatenated into final `output`. |
| `self.logger` | `BaseLogger` | Logging sink | Emits `InfoLog` entries. |

> **Note:** `DocFactory` does not perform any validation of `info` keys; missing keys may cause `None` to be passed downstream. 
<a name="parent-model"></a>
## `ParentModel` – Shared configuration & model rotation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `str` | API credential | Defaults to `API_KEY` from `autodocgenerator.engine.config.config` |
| `history` | `History` | Message buffer | Injected or created on‑demand |
| `use_random` | `bool` | Randomise model order | `True` enables `random.shuffle` |
| `regen_models_name` | `list[str]` | Rotation list | Copied from `MODELS_NAME` then shuffled if `use_random` |
| `current_model_index` | `int` | Cursor in `regen_models_name` | Starts at 0 |

> **Assumption** – `MODELS_NAME` and `API_KEY` are defined in the imported config module.  

The class stores credentials, a shared `History`, and prepares a shuffled list of model identifiers for fail‑over usage.

--- 
<a name="gpt-model"></a>
## `GPTModel` – Synchronous Groq client wrapper  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `client` | `Groq` | Sends sync chat requests | Instantiated with `self.api_key` |
| `logger` | `BaseLogger` | Emits runtime logs | Same log types as async variant |
| `generate_answer` | `def` | Returns LLM reply | Same signature as async version |

**Logic Flow** mirrors `AsyncGPTModel` but uses the synchronous `self.client.chat.completions.create` call and returns the extracted `result` directly.

Both wrappers expose the same public contract, differing only in async vs sync execution. 
<a name="async-gpt-model"></a>
## `AsyncGPTModel` – Asynchronous Groq client wrapper  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `client` | `AsyncGroq` | Sends async chat requests | Instantiated with `self.api_key` |
| `logger` | `BaseLogger` | Emits runtime logs | Uses `InfoLog`, `WarningLog`, `ErrorLog` |
| `generate_answer` | `async def` | Returns LLM reply | Parameters: `with_history: bool = True`, `prompt: str = None` |

**Logic Flow**  
1. Log start of generation.  
2. Select `messages` from `self.history.history` or the supplied `prompt`.  
3. Loop until a model succeeds:  
   - If `regen_models_name` empty → log error & raise `ModelExhaustedException`.  
   - Pick `model_name` from `regen_models_name[current_model_index]`.  
   - Call `await self.client.chat.completions.create(messages=messages, model=model_name)`.  
   - On exception → log warning, advance `current_model_index` (wrap‑around).  
4. Extract `result = chat_completion.choices[0].message.content`.  
5. Log the selected model and the answer (level 2).  
6. Return `result`.

**Interactions** – Relies on `AsyncGroq` for network I/O, `History` for context, and the shared logger. No file I/O.

--- 
<a name="semantic-ordering-llm"></a>
## Semantic Title Ordering (LLM Interaction)  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | Input | Must expose `get_answer_without_history`. |
| `chanks` | `dict[str,str]` | Input | Mapping from anchor links to text chunks. |
| `logger` | `BaseLogger` | Side‑effect | Emits `InfoLog` entries at various levels. |
| `prompt` | `list[dict]` | Local | Single user‑role message requesting a comma‑separated ordering. |
| `result` | `str` | Output (raw LLM reply) | Expected list of `#anchor` titles. |
| `new_result` | `list[str]` | Local | Stripped titles from `result`. |
| `order_output` | `str` | Return | Concatenated chunk texts in LLM‑provided order. |

**Logic Flow**  
1. Initialise `BaseLogger`; log start and input keys/values.  
2. Build `prompt` containing the titles (`list(chanks.keys())`).  
3. Call `model.get_answer_without_history(prompt)`; capture raw string.  
4. Split on commas, strip whitespace → `new_result`.  
5. Iterate `new_result`; for each anchor retrieve its chunk via `chanks.get(el)` and append to `order_output` (newline‑separated).  
6. Log each addition; return the assembled `order_output`.  

> **Warning** – If the model returns a malformed list (missing titles or extra commas), mismatches may lead to `None` values in the final output. 
<a name="html-link-extraction"></a>
## HTML Link Extraction (`get_all_html_links`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Input | Raw documentation text. |
| `links` | `list[str]` | Output | Anchor links prefixed with `#`. |
| `logger` | `BaseLogger` | Side‑effect | Logs progress at INFO level. |
| `pattern` | `str` | Internal | Regex `\<a name=["']?(.*?)["']?\>\</a\>` . |

The function scans `data` for `<a name=…></a>` anchors, captures the name when longer than five characters, prefixes it with `#`, logs the count and the list, then returns `links`. No file I/O occurs. 
<a name="anchor-extraction-chunk-splitting"></a>
## Anchor Extraction & Chunk Splitting  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `chunks` | `list[str]` | Input (raw HTML fragments) | Passed to **extract_links_from_start**. |
| `pattern` (in `extract_links_from_start`) | `str` | Constant | `r'^<a name=["\']?(.*?)["\']?></a>'` matches a leading anchor. |
| `anchor_name` | `str` | Local | Captured name; processed only if `len > 5`. |
| `links` | `list[str]` | Output (prefixed anchors) | Each stored as `#` + name. |
| `text` | `str` | Input (full doc) | Split by **split_text_by_anchors**. |
| `result_chanks` | `list[str]` | Output | Trimmed, non‑empty chunks after `re.split`. |
| `all_links` | `list[str]` | Output | Result of **extract_links_from_start** on the chunks. |
| `result` | `dict[str,str]` | Output | Mapping `#anchor → chunk`. Returns `None` on size mismatch. |

**Logic Flow**  
1. `extract_links_from_start` iterates `chunks`; regex anchors at start are captured.  
2. If an anchor’s name exceeds five characters, `"#"+name` is appended to `links`.  
3. `split_text_by_anchors` builds a look‑ahead pattern (`(?=<a name=…>)`) to split the full text into `chunks`.  
4. Whitespace‑trimmed chunks become `result_chanks`.  
5. `extract_links_from_start` processes these chunks; if the count of anchors ≠ chunks, the function aborts (`None`).  
6. Otherwise a dict `result` maps each `#anchor` to its associated chunk.  

> **Assumption** – No file I/O occurs; the functions only transform in‑memory strings. 
<a name="gen-doc"></a>
## `gen_doc` – End‑to‑End Documentation Generation Pipeline  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_path` | `str` | Root of the source project | Supplied by caller |
| `config` | `Config` | Project‑wide settings | From `read_config` |
| `custom_modules` | `list[...]` | Extension hooks for doc factories | Passed to `DocFactory` |
| `structure_settings` | `StructureSettings` | Controls ordering & intro links | Determines size & optional steps |
| `sync_model` / `async_model` | `GPTModel` / `AsyncGPTModel` | Language model back‑ends | Instantiated with global `API_KEY` |
| `manager` | `Manager` | Orchestrates parsing, generation, caching | Core engine object |
| Return value | `str` | Final assembled documentation | Read from manager’s output cache |

**Logic Flow**  
1. Create `GPTModel` and `AsyncGPTModel` using the shared `API_KEY`.  
2. Initialise `Manager` with `project_path`, `config`, both models, and a console progress bar.  
3. Invoke `manager.generate_code_file()` → extracts source code.  
4. Call `manager.generete_doc_parts(...)` → splits docs per `structure_settings.max_doc_part_size`.  
5. Run `manager.factory_generate_doc(DocFactory(*custom_modules))` → applies user‑defined modules.  
6. If `include_order` is true, `manager.order_doc()` reorders sections.  
7. If `include_intro_links` is true, generate intro links via `IntroLinks()` factory.  
8. Clear temporary caches with `manager.clear_cache()`.  
9. Return the assembled document read by `manager.read_file_by_file_key("output_doc")`.

**Interactions** – `gen_doc` ties together configuration (`Config`), custom processing (`CustomModule*`), the GPT backend, and the `Manager` orchestration. No external I/O occurs beyond the initial YAML read (handled elsewhere).  

> **Warning** – The function assumes `API_KEY` is defined in `autodocgenerator.engine.config.config`; absence raises an import error. 
<a name="gen-doc-parts"></a>
## `gen_doc_parts` – Orchestrated Multi‑Chunk Documentation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `full_code_mix` | `str` | Input | Complete source to be documented. |
| `max_symbols` | `int` | Input | Symbol limit passed to `split_data`. |
| `model` | `Model` | Input | Same contract as above. |
| `project_settings` | `ProjectSettings` | Input | Supplies global prompts. |
| `language` | `str` | Input | Target language for docs. |
| `progress_bar` | `BaseProgress` | Side‑effect | Tracks per‑chunk progress. |
| `global_info` | `str` / `None` | Optional | Extra project context. |
| `all_result` | `str` | Output | Concatenated documentation. |
| `logger` | `BaseLogger` | Side‑effect | Logs orchestration milestones. |

**Logic Flow**  
1. Split source via `split_data`.  
2. Create a sub‑task on `progress_bar` for the number of chunks.  
3. For each chunk `el`:  
   - Call `write_docs_by_parts` passing the previous result as `prev_info`.  
   - Append returned text and two newlines to `all_result`.  
   - Retain only the last 3000 characters of `result` for the next iteration (context window).  
   - Update progress bar.  
4. Remove sub‑task, log final length, and return `all_result`. 
<a name="write-docs-by-parts"></a>
## `write_docs_by_parts` – Per‑Chunk Documentation Generation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | Input | Text fragment to document. |
| `model` | `Model` | Input | Must implement `get_answer_without_history(prompt)`. |
| `project_settings` | `ProjectSettings` | Input | Provides `prompt` for system context. |
| `prev_info` | `str` / `None` | Optional | Previously generated doc fragment. |
| `language` | `str` | Input | Language code (default `"en"`). |
| `global_info` | `str` / `None` | Optional | Additional project‑wide context. |
| `answer` | `str` | Output | Raw LLM response, possibly wrapped in markdown fences. |
| `logger` | `BaseLogger` | Side‑effect | Logs generation steps. |

**Logic Flow**  
1. Initialise logger and base system prompts (language, global project info, static `BASE_PART_COMPLITE_TEXT`).  
2. Append optional `global_info` and `prev_info` prompts.  
3. Append user prompt containing `part`.  
4. Call `model.get_answer_without_history(prompt=prompt)`.  
5. Strip leading/trailing ````` fences if present and return cleaned text.  

> **Warning** – The function assumes the LLM returns a string; non‑string answers would raise a type error. 
<a name="custom-description-template"></a>
## Template‑Based Custom Description Generation (`generete_custom_discription_without`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | Input | LLM interface. |
| `custom_description` | `str` | Input | Desired description task. |
| `language` | `str` | Input (default `"en"`) | Language hint. |
| `result` | `str` | Output | LLM answer respecting strict tag rules. |

Constructs a prompt that enforces a single opening ` 
<a name="custom-description-iterative"></a>
## Iterative Custom Description Generation (`generete_custom_discription`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `splited_data` | `str` (iterable) | Input | Segments of documentation. |
| `model` | `Model` | Input | LLM interface. |
| `custom_description` | `str` | Input | Task description for the LLM. |
| `language` | `str` | Input (default `"en"`) | Language hint. |
| `result` | `str` | Output | First non‑error description. |

Iterates over `splited_data`, sending a prompt that includes the segment, `BASE_CUSTOM_DISCRIPTIONS`, and the task. Breaks when the LLM response does **not** contain `"!noinfo"` or `"No information found"` early in the text; otherwise continues. Returns the final `result`. 
<a name="repository-mixer"></a>
## Repository Structure Packing (CodeMix)  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `root_dir` | `Path` | Input | Base directory for scanning. |
| `ignore_patterns` | `list[str]` | Input | Glob patterns to exclude files/dirs. |
| `logger` | `BaseLogger` | Side‑effect | Logs ignored paths. |
| `should_ignore` | `method` | Local | Returns `True` if a path matches any ignore pattern. |
| `output_file` | `str` | Input | Destination text file for the mix. |
| `out` | file handle | Side‑effect | Receives repository tree and file contents. |

**Logic Flow**  
1. Resolve `root_dir`; instantiate `BaseLogger`.  
2. `should_ignore` converts a `Path` to a relative string, then checks against each glob pattern (full path, basename, and any path part).  
3. `build_repo_content` opens `output_file` for writing.  
4. First pass: iterate sorted `rglob("*")`; for each non‑ignored path write an indented tree line (`dir/` or `file`).  
5. Write a separator line (`"="*20`).  
6. Second pass: iterate again; for each non‑ignored **file**, write a `<file path="…">` tag, then the file’s text (read with UTF‑8, errors ignored). Errors are captured and written as plain text.  

> **Critical** – No network or external service calls; all operations are local filesystem reads/writes. 
<a name="compressor-core-function"></a>
## `compress` – Core LLM‑driven Compression  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Input | Raw source text to be compressed. |
| `project_settings` | `ProjectSettings` | Input | Supplies system prompt via its **`prompt`** property. |
| `model` | `Model` | Input | Must implement `get_answer_without_history(prompt)`. |
| `compress_power` | `int` | Input | Determines compression intensity; passed to helper text. |
| `prompt` | `list[dict]` | Local | System‑user message stack fed to the LLM. |
| `answer` | `str` | Output | LLM’s compressed response. |

**Logic Flow**  
1. Assemble a three‑message `prompt`: project‑level system prompt, a dynamically built “base compress” text (`get_BASE_COMPRESS_TEXT`), and the user‑provided `data`.  
2. Invoke `model.get_answer_without_history(prompt=prompt)`.  
3. Return the LLM’s reply unchanged.  

> **Assumption** – No file I/O; transformation occurs entirely in‑memory. 
<a name="batch-compression-compare"></a>
## `compress_and_compare` – Batch Compression with Progress  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | Input | Collection of text fragments. |
| `model` | `Model` | Input | Same requirements as above. |
| `project_settings` | `ProjectSettings` | Input | Shared prompt source. |
| `compress_power` | `int` | Input (default 4) | Max fragments per batch. |
| `progress_bar` | `BaseProgress` | Side‑effect | Visual sub‑task tracking. |
| `compress_and_compare_data` | `list[str]` | Local | Holds concatenated compressed batches. |

**Logic Flow**  
1. Initialise `compress_and_compare_data` sized to `ceil(len(data)/compress_power)`.  
2. Create a sub‑task on `progress_bar` for the full length of `data`.  
3. Iterate `data` with index `i`; compute batch index `curr_index = i // compress_power`.  
4. Call `compress` on each element, appending the result plus a newline to the appropriate batch slot.  
5. Update the progress bar after each element; finally remove the sub‑task.  
6. Return the list of batched compressed strings. 
<a name="iterative-full-compression"></a>
## `compress_to_one` – Recursive Full‑Document Collapse  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | Input/Output | Shrinks each iteration until a single string remains. |
| `model` | `Model` | Input | Same LLM contract. |
| `project_settings` | `ProjectSettings` | Input | Provides prompt context. |
| `compress_power` | `int` | Input (default 4) | Base batch size; may be reduced to 2 for small tails. |
| `progress_bar` | `BaseProgress` | Side‑effect | Propagated to inner calls. |
| `count_of_iter` | `int` | Local | Iteration counter (for potential logging). |

**Logic Flow**  
1. Loop while `len(data) > 1`.  
2. Adjust `new_compress_power`: if remaining items are fewer than `compress_power + 1`, set to 2 to avoid a final singleton batch.  
3. Replace `data` with the result of `compress_and_compare(data, …, new_compress_power, progress_bar)`.  
4. Increment `count_of_iter`.  
5. Once reduced to a single element, return `data[0]`.  

> **Warning** – The function assumes `compress_and_compare` always returns a non‑empty list; an empty return would raise an `IndexError`. 
<a name="split-data-loop"></a>
## `split_data` – Symbol‑Based Chunking Loop  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `splited_by_files` | `list[str]` | Local | Initial list of file‑level fragments (source not shown). |
| `max_symbols` | `int` | Input | Upper bound for symbols per chunk. |
| `split_objects` | `list[str]` | Local | Accumulates final chunks respecting `max_symbols`. |
| `logger` | `BaseLogger` | Side‑effect | Emits progress messages. |

**Logic Flow**  
1. Log start.  
2. **Refinement loop** – while any element exceeds `1.5 × max_symbols`, split it at `max_symbols/2` and insert the second half right after the original.  
3. **Packing loop** – iterate `splited_by_files`; create a new `split_objects` entry when adding the element would breach `1.25 × max_symbols`. Otherwise, concatenate with a newline.  
4. Log final chunk count and return `split_objects`.  

> **Assumption** – `splited_by_files` is pre‑populated; no I/O occurs here. 
