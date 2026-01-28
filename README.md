## Executive Navigation Tree
- 📦 Installation & Setup
  - [Install Workflow Powershell Unix](#install-workflow-powershell-unix)
  - [Install Scripts Behaviour](#install‑scripts‑behaviour)
- 📄 Documentation Generation
  - [Autodocfile Structure](#autodocfile-structure)
  - [Doc Factory](#doc-factory)
  - [Gen Doc Function](#gen-doc-function)
  - [Write Docs By Parts](#write-docs-by-parts)
  - [Async Write Docs By Parts](#async-write-docs-by-parts)
  - [Gen Doc Parts](#gen-doc-parts)
  - [Async Gen Doc Parts](#async-gen-doc-parts)
  - [Generate Descriptions](#generate-descriptions)
  - [Intro Links](#intro-links)
  - [Intro Text](#intro-text)
- 🛠️ Module & Manager Architecture
  - [Manager Class Usage](#manager-class-usage)
  - [Manager Core](#manager-core)
  - [Module Initializer](#module-initializer)
  - [Base Module](#base-module)
  - [Custom Module](#custom-module)
  - [Custom Module NoCtx](#custom-module-noctx)
  - [Custom Intro Processor](#custom-intro-processor)
  - [Code Mix Class](#code-mix-class)
  - [Logging Module Structure](#logging‑module‑structure)
  - [Progress Module Structure](#progress‑module‑structure)
- 📊 Metadata & Configuration
  - [Visible Interactions](#visible-interactions)
  - [Logic Flow](#logic-flow)
  - [Metadata Logic Flow](#metadata-logic-flow)
  - [Metadata Functional Role](#metadata-functional-role)
  - [Metadata Visible Interactions](#metadata-visible-interactions)
  - [Metadata Data Contract](#metadata-data-contract)
  - [Get Order](#get-order)
  - [Data Contract](#data-contract)
  - [Structure Settings](#structure-settings)
  - [Project Settings](#project-settings)
  - [Project Metadata Definition](#project-metadata-definition)
  - [CONTENT_DESCRIPTION](#CONTENT_DESCRIPTION)
  - [Read Config Function](#read-config-function)
- 🔧 Processing & Compression
  - [Extract Links From Start](#extract-links-from-start)
  - [Split Text By Anchors](#split-text-by-anchors)
  - [Split Data](#split-data)
  - [Split Data Loop Adjustments](#split-data-loop-adjustments)
  - [Split Data Chunk Assembly](#split-data-chunk-assembly)
  - [Compress](#compress)
  - [Compress And Compare](#compress-and-compare)
  - [Async Compress](#async-compress)
  - [Async Compress And Compare](#async-compress-and-compare)
  - [Compress To One](#compress-to-one)
- 🤖 AI Model Integration
  - [Async GPT Model](#async-gpt-model)
  - [GPT Model](#gpt-model)
  - [Model Base](#model-base)

 

<a name="install-workflow-powershell-unix"></a>
To set up the automated installation for both Windows PowerShell and Unix‑like shells, follow these steps in your GitHub Actions workflow:

### 1. PowerShell bootstrap (Windows agents)  
Use **Invoke‑RestMethod** (`irm`) to download the PowerShell bootstrap script directly from the repository and execute it in the same pipeline:

```yaml
- name: Run PowerShell installer
  if: runner.os == 'Windows'
  shell: pwsh
  run: |
    irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/installer.ps1 | iex
```

* `irm` fetches the script content.  
* The pipeline pipes the content to `iex` (Invoke‑Expression) so the script runs immediately without writing a temporary file.

### 2. Shell bootstrap (Linux/macOS agents)  
Use **curl** to fetch the Unix shell bootstrap script and pipe it to `bash`:

```yaml
- name: Run Unix installer
  if: runner.os != 'Windows'
  run: |
    curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/installer.sh | bash
```

* `-sSL` makes curl silent, follows redirects, and ensures TLS is used.  
* The script is streamed directly into `bash` for execution.

### 3. Add required secret for the installer  
The installer expects an API key to be provided via a secret environment variable. Define a secret named **GROCK_API_KEY** in the repository settings (Settings → Secrets → Actions) with the key you obtained from the Grock documentation.

```yaml
env:
  GROCK_API_KEY: ${{ secrets.GROCK_API_KEY }}
```

### 4. Complete workflow example  

```yaml
name: Install ADG

on:
  push:
    branches: [ main ]

jobs:
  install:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ windows-latest, ubuntu-latest, macos-latest ]

    steps:
      - uses: actions/checkout@v3

      # Provide the API key to all steps
      - name: Set API key
        env:
          GROCK_API_KEY: ${{ secrets.GROCK_API_KEY }}

      # Windows PowerShell installer
      - name: Run PowerShell installer
        if: runner.os == 'Windows'
        shell: pwsh
        run: |
          irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/installer.ps1 | iex

      # Linux/macOS shell installer
      - name: Run Unix installer
        if: runner.os != 'Windows'
        run: |
          curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/installer.sh | bash
```

**Key points to remember**

* Use the appropriate command (`irm` + `iex` for PowerShell, `curl` + `bash` for Unix) to pull and execute the remote bootstrap script in one step.  
* Protect the API key by storing it as a secret (`GROCK_API_KEY`) and referencing it via `${{ secrets.GROCK_API_KEY }}`.  
* The workflow runs on all major runner OSes, selecting the correct installer automatically. 
<a name="install‑scripts‑behaviour"></a>
## Installation Scripts (`install.ps1` / `install.sh`)  

| Script | Action | Result |
|--------|--------|--------|
| `install.ps1` | Creates `.github/workflows` directory; writes a GitHub Actions workflow YAML (`autodoc.yml`); writes `autodocconfig.yml` containing current folder name and language `"en"` | PowerShell‑based setup for Windows |
| `install.sh` | Same as above using Bash; uses `mkdir -p`; writes the workflow YAML with escaped `${{…}}`; creates `autodocconfig.yml` with `project_name` derived from `pwd` | Cross‑platform (Linux/macOS) setup |

Both scripts end with a success message printed to the console. 
<a name="autodocfile-structure"></a>
The autodoc configuration file is a YAML document with the following top‑level keys and sub‑options:

**project_name** – a string that defines the name of the project.

**language** – a string indicating the language for generated documentation (e.g., “en”).

**build_settings** – a map containing:
- **save_logs** – boolean, whether to keep generation logs.
- **log_level** – integer, level of detail for logging.

**structure_settings** – a map that controls documentation layout:
- **include_intro_links** – boolean, include introductory hyperlinks.
- **include_order** – boolean, preserve the order of sections.
- **max_doc_part_size** – integer, maximum size (in characters) for each documentation part.

**project_additional_info** – a map for extra project metadata, for example:
- **global idea** – a descriptive string about the project’s purpose.

**custom_descriptions** – a list of strings, each providing custom prompts or explanations that will be incorporated into the generated documentation.

When writing the file, use proper YAML indentation, include the keys above, and set values according to the desired behavior. No other options are shown in the provided context. 
<a name="doc-factory"></a>
## `DocFactory` – Orchestrator of Module Pipeline  

**Responsibility** – Executes a sequence of `BaseModule` instances, concatenates their outputs, logs progress, and updates a `BaseProgress` sub‑task.  

**Logic Flow**  
1. `__init__(*modules)` stores modules list and creates `BaseLogger`.  
2. `generate_doc(info, model, progress)`  
   - Calls `progress.create_new_subtask` with module count.  
   - Iterates over `self.modules`:  
     • `module.generate(info, model)` → `module_result`.  
     • Appends `module_result` and two newlines to `output`.  
     • Logs module completion (`InfoLog`).  
     • Logs raw module output at level 2.  
     • Calls `progress.update_task()`.  
   - After loop, `progress.remove_subtask()`.  
   - Returns the aggregated `output`.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `modules` | `list[BaseModule]` | Generation steps | Provided at construction |
| `logger` | `BaseLogger` | Central logger | Uses `InfoLog`/`ErrorLog` etc. |
| `info` | `dict` | Shared context for all modules | Passed unchanged |
| `model` | `Model` | LLM interface for modules | Same instance reused |
| `progress` | `BaseProgress` | Progress UI controller | Must support sub‑task API |
| Return | `str` | Full documentation string | Newlines separate parts |

--- 
<a name="gen-doc-function"></a>
## `gen_doc` – Orchestrator of Documentation Generation  

**Responsibility** – Creates the AI models, configures a `Manager`, drives the full generation cycle, and returns the final markdown document.  

**Logic Flow**  
1. Instantiate `GPTModel` (sync) and `AsyncGPTModel` (async) with `API_KEY`.  
2. Initialise `Manager` with `project_path`, the `Config`, both models, and a `ConsoleGtiHubProgress` bar.  
3. Sequential calls on `manager`:  
   - `generate_code_file()` – extracts source files.  
   - `generete_doc_parts(max_symbols=structure_settings.max_doc_part_size)` – splits docs.  
   - `factory_generate_doc(DocFactory(*custom_modules))` – applies custom modules.  
   - Conditional `order_doc()` if `include_order` is true.  
   - Conditional `factory_generate_doc(DocFactory(IntroLinks()))` if `include_intro_links` is true.  
   - `clear_cache()` – removes temporary artefacts.  
4. Retrieve the assembled output via `manager.read_file_by_file_key("output_doc")`.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_path` | `str` | Filesystem root of the target project | Passed unchanged to `Manager`. |
| `config` | `Config` | Global configuration (language, ignores, etc.) | Produced by `read_config`. |
| `custom_modules` | `list[CustomModule]` | Extension points for description generation | May be empty. |
| `structure_settings` | `StructureSettings` | Controls chunk size & optional sections | Influences `generete_doc_parts` and ordering. |
| Return value | `str` | Final assembled documentation | Read from manager’s internal cache. |

> **Warning** – The function assumes `API_KEY` is defined in `autodocgenerator.engine.config.config`; missing or invalid keys will raise at model construction time. 
<a name="write-docs-by-parts"></a>
## write_docs_by_parts Interaction  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | Code fragment to document | Supplied by caller |
| `model` | `Model` | LLM interface | Provides `get_answer_without_history` |
| `project_settings` | `ProjectSettings` | Holds `prompt` for global context | Inserted into system messages |
| `prev_info` | `str | None` | Prior generated doc snippet | May be included in prompt |
| `language` | `str` | Desired output language | Defaults `"en"` |
| Return | `str` | Generated documentation snippet | Stripped of surrounding markdown fences if present |

The function builds a prompt (system messages + optional previous info + user part), calls the model, trims leading/trailing ``````` fences, logs the result, and returns the cleaned answer. 
<a name="async-write-docs-by-parts"></a>
## async_write_docs_by_parts Async Generation  

Mirrors `write_docs_by_parts` but **awaits** `async_model.get_answer_without_history` within a semaphore‑protected block. It also accepts an optional `update_progress` callback invoked after the LLM call. 
<a name="gen-doc-parts"></a>
## gen_doc_parts Orchestration  

| Entity | Type | Role |
|--------|------|------|
| `full_code_mix` | `str` | Whole source to split |
| `max_symbols` | `int` | Size limit for chunks |
| `model` | `Model` | Synchronous LLM |
| `project_settings` | `ProjectSettings` | Global prompt |
| `language` | `str` | Output language |
| `progress_bar` | `BaseProgress` | Visual progress tracking |
| Return | `str` | Concatenated documentation |

Calls `split_data`, iterates over each chunk, invokes `write_docs_by_parts`, appends results, trims the tail to keep a 3000‑character context window, updates the progress bar, and finally returns the aggregated documentation. 
<a name="async-gen-doc-parts"></a>
## async_gen_doc_parts Asynchronous Orchestration  

Functions identically to `gen_doc_parts` but creates tasks that run `async_write_docs_by_parts` concurrently (semaphore limit = 4) and gathers their results. Progress updates are performed via the supplied `update_progress` lambda. The final concatenated documentation is returned. 
<a name="generate-descriptions"></a>
## `generate_discribtions_for_code` – LLM‑Driven Doc Generation  

**Role** – Sends each code snippet to a model with a strict “no‑hallucination” prompt, collects the responses.

| Entity | Type | Role | Notes |
|--------|------|------|------- |
| `data` | `list[str]` | Input | Code snippets. |
| `model` | `Model` | Input | Must support `get_answer_without_history`. |
| `project_settings` | `ProjectSettings` | — | Not used directly. |
| `progress_bar` | `BaseProgress` | Internal | Per‑snippet progress. |
| `describtions` | `list[str]` | Output | Model‑generated documentation strings. |

**Flow**  
1. Create sub‑task sized to `len(data)`.  
2. For each snippet, build a prompt that forces the model to produce a self‑contained description.  
3. Call `model.get_answer_without_history`.  
4. Append the answer to `describtions`.  
5. Update progress, remove sub‑task, return the list. 
<a name="manager-core"></a>
## `Manager` – Core Coordination Component  

**Responsibility** – Orchestrates the end‑to‑end documentation pipeline: prepares cache, reads/writes intermediate files, drives code‑mix creation, part‑wise generation, factory‑based enrichment, and final ordering.  

**Visible Interactions**  
- Imports preprocessing utilities (`split_data`, `gen_doc_parts`, `CodeMix`), post‑processing helpers (`get_introdaction`, `get_all_html_links`, `get_links_intro`), model abstractions (`Model`, `AsyncModel`), and UI logging/progress classes.  
- Persists files under `self.CACHE_FOLDER_NAME` using paths from `self.FILE_NAMES`.  
- Delegates heavy work to external functions (`gen_doc_parts`, `DocFactory.generate_doc`, `split_text_by_anchors`, `get_order`).  

**Logic Flow**  
1. **`__init__(project_directory, config, sync_model=None, async_model=None, progress_bar=BaseProgress())`**  
   - Stores arguments, creates a logger with file target `logs`.  
   - Ensures cache directory exists (`.auto_doc_cache`).  

2. **`read_file_by_file_key(file_key)`** → opens `self.get_file_path(file_key)` and returns its UTF‑8 content.  

3. **`get_file_path(file_key)`** → builds `os.path.join(project_directory, CACHE_FOLDER_NAME, FILE_NAMES[file_key])`.  

4. **`generate_code_file()`** →  
   - Instantiates `CodeMix` with `project_directory` and `config.ignore_files`.  
   - Calls `cm.build_repo_content` to write the code mix to `code_mix.txt`.  

5. **`generete_doc_parts(max_symbols=5_000)`** →  
   - Reads full code mix, logs start, invokes `gen_doc_parts(full_code_mix, max_symbols, sync_model, config.get_project_settings(), config.language, progress_bar)`.  
   - Writes the returned markdown to `output_doc.md`.  

6. **`factory_generate_doc(doc_factory)`** →  
   - Reads current doc and code mix, builds `info` dict (`language`, `full_data`, `code_mix`).  
   - Calls `doc_factory.generate_doc(info, sync_model, progress_bar)`.  
   - Prepends the new fragment to existing doc and writes back.  

7. **`order_doc()`** →  
   - Splits current doc by anchors via `split_text_by_anchors`, orders sections with `get_order`, and rewrites the file.  

8. **`clear_cache()`** → deletes `logs` file when `config.pbc.save_logs` is `False`.  

**Data Contract**  

| Method | Input(s) | Output | Side Effects |
|--------|----------|--------|--------------|
| `__init__` | `project_directory: str`, `config: Config`, optional models, `progress_bar` | `Manager` instance | Creates cache folder, sets up logger |
| `read_file_by_file_key` | `file_key: str` (key in `FILE_NAMES`) | `str` file content | None |
| `get_file_path` | `file_key: str` | `str` absolute path | None |
| `generate_code_file` | – | – | Writes `code_mix.txt` |
| `generete_doc_parts` | `max_symbols: int` | – | Writes `output_doc.md` |
| `factory_generate_doc` | `doc_factory: DocFactory` | – | Updates `output_doc.md` |
| `order_doc` | – | – | Rewrites `output_doc.md` |
| `clear_cache` | – | – | May delete `report.txt` |

> **Warning** – All file operations assume the referenced keys exist in `FILE_NAMES`; missing keys raise `KeyError`. 
<a name="module-initializer"></a>
## Package Initializer – Logger Bootstrap

**Functional role**  
The `autodocgenerator/__init__.py` module bootstraps the **AutoDocGenerator** package by:

1. Emitting a simple runtime banner (`print("ADG")`).
2. Importing the core logging classes from `autodocgenerator.ui.logging`.
3. Instantiating a global `logger` object (`BaseLogger`).
4. Attaching a concrete logging template (`BaseLoggerTemplate`) to the logger.

This makes a ready‑to‑use `logger` available to every submodule that imports `autodocgenerator`. 
<a name="base-module"></a>
## `BaseModule` – Abstract Generation Unit  

**Responsibility** – Serves as the contract for all documentation modules; subclasses must implement `generate(info: dict, model: Model)`.  

**Logic Flow**  
1. Inherits from `ABC`.  
2. Defines abstract `generate`.  
3. Provides a no‑op `__init__`.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `info` | `dict` | Input data for generation | Expected keys are module‑specific |
| `model` | `Model` | LLM wrapper used by modules | Imported from `engine.models.model` |
| Return | `str` | Generated documentation fragment | Must be a string |

--- 
<a name="custom-module"></a>
## `CustomModule` – Context‑Aware Description Generator  

**Responsibility** – Produces a custom description using the code mix (split to ≤ 5000 symbols) and language.  

**Logic Flow**  
1. Stores `discription` (sic) on init.  
2. `generate(info, model)` →  
   - Calls `split_data(info.get("code_mix"), max_symbols=5000)`.  
   - Passes result, `model`, stored `discription`, and `info.get("language")` to `generete_custom_discription`.  
   - Returns the obtained string.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `discription` | `str` | Template text for generation | Set via constructor |
| `info["code_mix"]` | `str` | Source code fragment | May be absent → `None` |
| `info["language"]` | `str` | Target language for output | Optional |
| Return | `str` | Generated custom description | From `generete_custom_discription` |

--- 
<a name="custom-module-noctx"></a>
## `CustomModuleWithOutContext` – Context‑Free Description Generator  

**Responsibility** – Generates a description without processing any code context.  

**Logic Flow**  
1. Stores `discription` on init.  
2. `generate(info, model)` → calls `generete_custom_discription_without(model, self.discription, info.get("language"))` and returns its result.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `discription` | `str` | Fixed template | Constructor argument |
| `info["language"]` | `str` | Desired language | Optional |
| Return | `str` | Description string | From `generete_custom_discription_without` |

--- 
<a name="custom-intro-processor"></a>
## Custom Intro Processor Functions  

**Responsibility** – Generates enriched introductory sections and HTML link lists for the documentation pipeline. It extracts anchors, prompts a *Model* to create link‑based intros, full introductions, and optional custom descriptions. 
<a name="code-mix-class"></a>
## `CodeMix` – Repository Content Packager

**Responsibility** – Walks a directory tree, writes a textual representation of its structure and the raw content of each non‑ignored file to an output file.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `root_dir` | `Path` | Input | Base directory (resolved). |
| `ignore_patterns` | `list[str]` | Input | Glob patterns for files/dirs to skip. |
| `logger` | `BaseLogger` | Internal | Logs actions at configurable levels. |
| `should_ignore(path)` | `bool` | Output | True if `path` matches any ignore pattern. |
| `build_repo_content(output_file)` | `None` | Side‑effect | Writes structure + file bodies to *output_file*. |

**Logic Flow**  
1. `should_ignore` computes a relative path, then checks glob matches against the full path, basename, and any path component.  
2. `build_repo_content` opens `output_file`.  
3. First pass: writes “Repository Structure” with indentation proportional to depth, skipping ignored entries.  
4. Writes a separator line.  
5. Second pass: for each non‑ignored file, writes `<file path="…">` header, the file’s text (read with UTF‑8, errors ignored), and a blank line; errors are recorded in the output.  

**Interaction** – Relies solely on the standard library (`os`, `pathlib`, `fnmatch`) and the internal `BaseLogger`. No external services are invoked. 
<a name="logging‑module‑structure"></a>
## `logging.py` Classes and Flow  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseLog` | class | Holds raw `message` and numeric `level`; provides default `format()` | `level` defaults 0 |
| `ErrorLog` / `WarningLog` / `InfoLog` | subclasses of `BaseLog` | Override `format()` to prepend timestamp & severity | Use `_log_prefix` property |
| `BaseLoggerTemplate` | class | Routes a `BaseLog` to an output; respects `log_level` filter | `global_log()` checks filter |
| `FileLoggerTemplate` | subclass of `BaseLoggerTemplate` | Writes formatted logs to a file path | Overrides `log()` |
| `BaseLogger` | singleton class | Central façade exposing `set_logger()` and `log()` | Stores a single `logger_template` instance |

**Logic flow**  
1. A log object (e.g., `ErrorLog("msg")`) is instantiated → `_log_prefix` builds `"[YYYY‑MM‑DD HH:MM:SS]"`.  
2. `BaseLogger().set_logger(logger_template)` injects a concrete template (`BaseLoggerTemplate` or `FileLoggerTemplate`).  
3. `BaseLogger().log(log_obj)` forwards to `logger_template.global_log`.  
4. `global_log` checks `self.log_level`; if `-1` or `log_level >= log.level`, it calls `log()` of the template, which either prints or appends to file. 
<a name="progress‑module‑structure"></a>
## `progress_base.py` Classes and Flow  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseProgress` | abstract class | Defines progress‑related API (`create_new_subtask`, `update_task`, `remove_subtask`) | Methods are placeholders |
| `LibProgress` | subclass of `BaseProgress` | Wraps **rich** `Progress`; tracks a base task and optional sub‑task | `update_task()` advances the appropriate task |
| `ConsoleTask` | helper class | Prints simple textual progress updates | `progress()` increments and prints percent |
| `ConsoleGtiHubProgress` | subclass of `BaseProgress` | Uses `ConsoleTask` for both general and sub‑tasks | `gen_task` created for overall progress |

**Logic flow**  
1. `LibProgress.__init__` creates a rich base task (`total` defaults 4).  
2. `create_new_subtask(name, total_len)` registers a sub‑task and stores its ID.  
3. `update_task()` advances the sub‑task if present; otherwise advances the base task.  
4. `remove_subtask()` clears the sub‑task reference.  
5. `ConsoleGtiHubProgress` mirrors this behavior with `ConsoleTask` objects, printing textual percentages. 
<a name="intro-links"></a>
## `IntroLinks` – HTML Link Intro Builder  

**Responsibility** – Extracts HTML links from `full_data` and formats an introductory block using the model.  

**Logic Flow**  
1. `generate(info, model)` →  
   - `links = get_all_html_links(info.get("full_data"))`.  
   - `intro_links = get_links_intro(links, model, info.get("language"))`.  
   - Returns `intro_links`.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `info["full_data"]` | `Any` | Raw data containing HTML links | Passed to `get_all_html_links` |
| `info["language"]` | `str` | Output language | Optional |
| Return | `str` | Intro text with links | From `get_links_intro` |

--- 
<a name="intro-text"></a>
## `IntroText` – General Introduction Generator  

**Responsibility** – Generates a textual introduction from `global_data` via the model.  

**Logic Flow**  
1. `generate(info, model)` →  
   - `intro = get_introdaction(info.get("global_data"), model, info.get("language"))`.  
   - Returns `intro`.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `info["global_data"]` | `Any` | Source content for intro | Consumed by `get_introdaction` |
| `info["language"]` | `str` | Desired language | Optional |
| Return | `str` | Introduction paragraph | From `get_introdaction` |

> **Warning** – All modules assume required keys exist in `info`; missing keys will cause `None` to be passed to downstream functions, which may raise errors if not handled. 
<a name="visible-interactions"></a>
## External Interactions  

- Imports **`GPTModel`**, **`Model`** (model abstractions).  
- Uses UI logging classes **`BaseLogger`**, **`InfoLog`** for progress reporting.  
- Relies on configuration constants **`BASE_INTRODACTION_CREATE_LINKS`**, **`BASE_INTRO_CREATE`**, **`BASE_CUSTOM_DISCRIPTIONS`**.  
- No file I/O is performed here; all persistence is handled upstream/downstream. 
<a name="logic-flow"></a>
## Execution Flow  

1. **`get_all_html_links(data)`** – Scans *data* with regex `<a name=["']?(.*?)["']?</a>`; collects anchors longer than 5 chars, prefixes “#”. Logs start/completion.  
2. **`get_links_intro(links, model, language)`** – Builds a system‑prompt using `BASE_INTRODACTION_CREATE_LINKS`, adds the *links* list, calls `model.get_answer_without_history`, returns the generated intro.  
3. **`get_introdaction(global_data, model, language)`** – Similar prompt flow with `BASE_INTRO_CREATE`; returns plain introduction text.  
4. **`generete_custom_discription(splited_data, model, custom_description, language)`** – Iterates over *splited_data*, constructs a detailed system prompt (technical analyst + `BASE_CUSTOM_DISCRIPTIONS`), stops when the model returns a substantive answer (absence of “!noinfo”/“No information found”). Returns the first valid result.  
5. **`generete_custom_discription_without(model, custom_description, language)`** – Sends a single prompt that enforces a mandatory ` 
<a name="metadata-logic-flow"></a>
## Logic Flow  

1. Build tool opens `pyproject.toml`.  
2. Parses `[project]` section → extracts metadata fields.  
3. Parses `[build-system]` → ensures `poetry-core` is available.  
4. Emits a `ProjectMetadata` object; downstream steps use it to construct distribution files. 
<a name="metadata-functional-role"></a>
## Functional Role  

The fragment declares **static package metadata** and **dependency constraints** for the **Auto Doc Generator** project. It serves as the single source of truth for packaging, installation, and build‑time resolution of required libraries. 
<a name="metadata-visible-interactions"></a>
## Visible Interactions  

1. **Build backend** (`poetry.core.masonry.api`) reads the file to generate `pyproject‑metadata` and wheel/sdist artifacts.  
2. **Dependency resolvers** (pip, poetry) consume the `dependencies` list to install required packages.  
3. **IDE tooling** may display the metadata (name, version, authors) for user reference. 
<a name="metadata-data-contract"></a>
## Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| Input file | **toml** | Source of configuration | Must be present at project root |
| Output artifact | **wheel / sdist** | Packaged distribution | Contains metadata derived from this fragment |
| Side effects | **none at runtime** | Build‑time only | No code execution, only static analysis |

This documentation isolates the `pyproject.toml` fragment, adhering strictly to the provided content without external inference. 
<a name="get-order"></a>
## `get_order` – Semantic Title Sorting

**Responsibility** – Sends the list of anchor titles to a *Model* for semantic ordering, then assembles the ordered markdown.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | Input | Must implement `get_answer_without_history`. |
| `chanks` | `dict[str, str]` | Input | Anchor → content mapping from `split_text_by_anchors`. |
| `result` | `str` | Internal | Raw comma‑separated answer from model. |
| `new_result` | `list[str]` | Internal | Stripped title list. |
| `order_output` | `str` | Output | Concatenated content in the model’s order. |

**Logic Flow**  
1. Log start and inputs.  
2. Build `prompt` requesting a **comma‑separated** list of titles (anchors kept).  
3. Call `model.get_answer_without_history(prompt)`.  
   - *If the model lacks this method, an `AttributeError` is raised.*  
4. Split and strip the answer → `new_result`.  
5. Iterate `new_result`, append `chanks[el]` to `order_output` with a trailing newline, logging each addition.  
6. Return the assembled string. 
<a name="data-contract"></a>
## Data Contract  

| Function | Input(s) | Output | Side Effects |
|----------|----------|--------|--------------|
| `get_all_html_links` | `data: str` | `list[str]` of “#anchor” links | Logs extraction |
| `get_links_intro` | `links: list[str]`, `model: Model`, `language: str` | `str` intro with links | Logs generation |
| `get_introdaction` | `global_data: str`, `model: Model`, `language: str` | `str` full intro | None |
| `generete_custom_discription` | `splited_data: str`, `model: Model`, `custom_description: str`, `language: str` | `str` description (or empty) | Logs each attempt |
| `generete_custom_discription_without` | `model: Model`, `custom_description: str`, `language: str` | `str` description with mandatory tag | None |

> **⚠️ Warning** – All prompts assume the provided *Model* implements `get_answer_without_history`. If the model is absent or mis‑configured, the functions will raise an `AttributeError`. 
<a name="structure-settings"></a>
## `StructureSettings` – Runtime Documentation Layout Settings  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `include_intro_links` | `bool` | Toggle insertion of intro‑links section | Defaults `True` |
| `include_order` | `bool` | Toggle automatic ordering of generated parts | Defaults `True` |
| `max_doc_part_size` | `int` | Maximum symbols per documentation chunk | Default `5 000` |
| `load_settings` | method | Populates attributes from a dict | **Assumption** – keys match attribute names exactly |

> **Assumption** – No validation is performed; unknown keys become new attributes. 
<a name="project-settings"></a>
## `ProjectSettings` – Project‑Specific Prompt Builder  

**Role** – Holds a project name and arbitrary key/value pairs, exposing a `prompt` property that concatenates the base settings prompt with those values.

| Entity | Type | Role | Notes |
|--------|------|------|------- |
| `project_name` | `str` | Input | Identifier for the project. |
| `info` | `dict` | Internal | Arbitrary metadata added via `add_info`. |
| `add_info(key, value)` | `method` | Mutator | Stores `key: value` in `info`. |
| `prompt` | `property` | Output | `BASE_SETTINGS_PR` + project name + all `info` entries. |

**Flow**  
1. `add_info` inserts a key/value pair.  
2. `prompt` starts with `BASE_SETTINGS_PROMPT`, appends “Project Name: …”, then each stored pair as `key: value`.  

> **Note:** All components rely solely on the standard library and the internal `engine` and `ui` packages; no external services are invoked beyond the supplied `Model` implementations. 
<a name="project-metadata-definition"></a>
## `pyproject.toml` Project Metadata  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `name` | string | Package identifier | `"autodocgenerator"` |
| `version` | string | Semantic version | `"0.9.0.1"` |
| `description` | string | One‑line summary | Helps create docs for projects |
| `authors` | list of tables | Author contact info | `{name, email}` |
| `license` | table | SPDX‑compatible licensing | `text = "MIT"` |
| `readme` | string | Path to long description | `"README.md"` |
| `requires-python` | string | Python version constraint | `">=3.11,<4.0"` |
| `dependencies` | list of strings | Runtime requirements | 44 packages listed |
| `build-system.requires` | list of strings | Build‑time requirements | `["poetry-core>=2.0.0"]` |
| `build-system.build-backend` | string | Build backend entry point | `"poetry.core.masonry.api"` |

> **Assumption:** The file is processed by **PEP 621**‑compatible tools (e.g., *poetry*). No other runtime logic is present. 
<a name="CONTENT_DESCRIPTION"></a>` tag and strict lexical rules; returns the model’s raw answer. 
<a name="read-config-function"></a>
## `read_config` – YAML Configuration Loader  

**Responsibility** – Parses a YAML string, builds a **`Config`** object, instantiates custom description modules, and prepares a **`StructureSettings`** instance for the generation pipeline.  

**Logic Flow**  
1. `yaml.safe_load` → `data` dict.  
2. Extract `ignore_files`, `language`, `project_name`, `project_additional_info`, `build_settings`, `custom_descriptions`, `structure_settings`.  
3. Initialise `Config()` → `pcs = ProjectBuildConfig()`; `pcs.load_settings(build_settings)`.  
4. Chain setters: `set_language`, `set_project_name`, `set_pcs`.  
5. Append each ignore pattern via `config.add_ignore_file`.  
6. Populate additional info with `config.add_project_additional_info`.  
7. Build `custom_modules` list: entries starting with **`%`** become `CustomModuleWithOutContext(custom_desc[1:])`; otherwise `CustomModule(custom_desc)`.  
8. Load structure settings into a fresh `StructureSettings` object.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_data` | `str` | Raw YAML content | Must be UTF‑8 valid |
| `config` | `Config` | Central project configuration | Populated via setters |
| `custom_modules` | `list[CustomModule]` | User‑supplied description hooks | Context‑aware vs. context‑less |
| `structure_settings_object` | `StructureSettings` | Controls doc chunking & ordering | Loaded from `structure_settings` dict |
| Return value | `tuple[Config, list[CustomModule], StructureSettings]` | Combined runtime configuration | Order fixed as shown | 
<a name="extract-links-from-start"></a>
## `extract_links_from_start` – Anchor Extraction

**Responsibility** – Scans a list of markdown *chunks* and returns a list of anchor links (`#anchor`) whose name length > 5.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `chunks` | `list[str]` | Input | Raw markdown sections. |
| `links` | `list[str]` | Output | Collected `#`‑prefixed anchors. |

> **Assumption** – Each chunk may start with an HTML `<a name="…"></a>` tag. 
<a name="split-text-by-anchors"></a>
## `split_text_by_anchors` – Chunk Partitioning

**Responsibility** – Splits a markdown *text* at anchor tags, validates a 1:1 mapping, and builds a dict `{anchor: chunk}`.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `text` | `str` | Input | Full markdown document. |
| `result_chanks` | `list[str]` | Internal | Trimmed, non‑empty pieces. |
| `all_links` | `list[str]` | Internal | Output of `extract_links_from_start`. |
| `result` | `dict[str, str]` | Output | Mapping anchor → chunk; `None` if lengths differ. |

**Logic Flow**  
1. Regex `(?=<a name=…)` creates split points.  
2. Whitespace‑trim each piece.  
3. Call `extract_links_from_start` → `all_links`.  
4. If `len(all_links) != len(result_chanks)` → `return None`.  
5. Populate `result` by index. 
<a name="split-data"></a>
## `split_data` – Input Chunking for Symbol‑Limited Processing  

**Role** – Divides a raw documentation string into smaller fragments that do not exceed a given symbol count, preparing the text for downstream model calls that have size limits.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Input | Complete documentation text to be partitioned. |
| `max_symbols` | `int` | Input | Maximum number of characters allowed per output fragment. |
| `split_objects` | `list[str]` | Internal | Accumulates the generated fragments; initially empty. |
| `splited_by_files` | `list[str]` | Internal | Result of `data.split(...)`; the delimiter is not visible in the fragment. |
| `BASE_PART_COMPLITE_TEXT` | `str` (import) | External | Constant from the engine config; purpose not evident in the shown code. |
| `ProjectSettings`, `BaseProgress`, `BaseLogger`, … | *imports* | External | Imported but not referenced in the visible fragment. |

> **Note:** The delimiter used in `data.split(...)` and any subsequent processing steps are omitted from the provided snippet; therefore, the full transformation logic cannot be described.

**Flow**  
1. **Initialize** `split_objects` as an empty list.  
2. **Split** the input string `data` using an unspecified delimiter (`data.split("…")`) and store the resulting list in `splited_by_files`.  
3. *(Further processing – e.g., chunk size enforcement, aggregation into `split_objects` – is not present in the supplied fragment and therefore not documented.)*  

**Visible Interactions**  
- Relies solely on Python's built‑in `str.split` method; no external APIs or custom classes are invoked within the visible portion.  
- Imports from the engine and UI layers are present but unused in the excerpt, indicating that additional functionality may be added later in the function.  

> **Critical Assumption:** Without the remainder of the function, the exact mechanism for respecting `max_symbols` and how the fragments are returned remains undefined.  

---  

*End of `split_data` documentation.* 
<a name="split-data-loop-adjustments"></a>
## split_data Loop Adjustments  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `splited_by_files` | `list[str]` | Source fragments after initial split | Populated before this fragment |
| `max_symbols` | `int` | Size threshold | Used with multipliers `1.5` and `1.25` |
| `have_to_change` | `bool` | Loop‑control flag | Starts `False`, set `True` when a slice is re‑partitioned |
| `i`, `el` | `int`, `str` | Iterator values | `enumerate(splited_by_files)` |

**Logic flow**  
1. Enter an indefinite `while` loop.  
2. Iterate over `splited_by_files`.  
3. If a segment length exceeds `max_symbols * 1.5`, insert a new slice at `i+1` containing the right half (`el[i][int(max_symbols/2):]`) and truncate the original to the left half (`el[i][:int(max_symbols/2)]`).  
4. Set `have_to_change` = `True`.  
5. After the `for` loop, break when no segment required further splitting.

> **Assumption:** `el[i]` indexing is safe because `el` is a string; the code relies on Python slicing semantics. 
<a name="split-data-chunk-assembly"></a>
## split_data Chunk Assembly  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `split_objects` | `list[str]` | Accumulator for final parts | Initialized earlier as `[]` |
| `curr_index` | `int` | Current output bucket index | Starts `0` |
| `el` (loop variable) | `str` | Current piece from `splited_by_files` | Processed sequentially |

**Logic flow**  
1. Ensure `split_objects` has an entry for `curr_index`; append empty string if missing.  
2. If adding `el` would make the current bucket exceed `max_symbols * 1.25`, increment `curr_index`, start a new bucket with `el`, and continue.  
3. Otherwise, append `"\n"+el` to the existing bucket.  

The loop yields `split_objects`, a list of strings each respecting the size heuristic. 
<a name="compress"></a>
## `compress` – Text Chunk Compression  

**Role** – Sends a single text fragment to a language model with a project‑specific system prompt and a base compression prompt, then returns the model’s raw answer.

| Entity | Type | Role | Notes |
|--------|------|------|------- |
| `data` | `str` | Input | Text to compress. |
| `project_settings` | `ProjectSettings` | Input | Provides the system prompt via its `prompt` property. |
| `model` | `Model` | Input | Must implement `get_answer_without_history`. |
| `compress_power` | `int` | Input | Determines the compression strength. |
| `prompt` | `list[dict]` | Internal | System and user messages built for the model. |
| `answer` | `str` | Output | Raw response from `model.get_answer_without_history`. |

**Flow**  
1. Assemble `prompt` with three messages: project settings, base‑compression text (`get_BASE_COMPRESS_TEXT(10000, compress_power)`), and the target `data`.  
2. Call `model.get_answer_without_history(prompt=prompt)`.  
3. Return the obtained answer. 
<a name="compress-and-compare"></a>
## `compress_and_compare` – Batch Compression & Comparison  

**Role** – Groups input strings into bundles of size `compress_power`, compresses each via `compress`, and returns a list where each element contains the concatenated compressed results of a bundle.

| Entity | Type | Role | Notes |
|--------|------|------|------- |
| `data` | `list[str]` | Input | Source strings to compress. |
| `model` | `Model` | Input | Used by `compress`. |
| `project_settings` | `ProjectSettings` | Input | Passed to `compress`. |
| `compress_power` | `int` | Input | Bundle size (default 4). |
| `progress_bar` | `BaseProgress` | Internal | Updates progress per item. |
| `compress_and_compare_data` | `list[str]` | Output | List sized ⌈len(data)/compress_power⌉. |

**Flow**  
1. Allocate a result list sized for the number of bundles.  
2. Create a sub‑task for progress.  
3. Iterate over `data`; compute `curr_index = i // compress_power`.  
4. Append `compress(el, …)` plus newline to the corresponding slot.  
5. Update progress after each element.  
6. Remove the sub‑task and return the list. 
<a name="async-compress"></a>
## `async_compress` – Async Single‑Item Compression  

**Role** – Async counterpart of `compress`; respects a semaphore to limit concurrent model calls and reports progress.

| Entity | Type | Role | Notes |
|--------|------|------|------- |
| `data` | `str` | Input | Text to compress. |
| `project_settings` | `ProjectSettings` | Input | Provides system prompt. |
| `model` | `AsyncModel` | Input | Async `get_answer_without_history`. |
| `compress_power` | `int` | Input | Compression strength. |
| `semaphore` | `asyncio.Semaphore` | Input | Limits parallel calls. |
| `progress_bar` | `BaseProgress` | Input | Updates after each call. |
| `answer` | `str` | Output | Model’s response. |

**Flow**  
1. Acquire `semaphore`.  
2. Build the same three‑message `prompt` as `compress`.  
3. Await `model.get_answer_without_history(prompt=prompt)`.  
4. Increment progress, release semaphore, return answer. 
<a name="async-compress-and-compare"></a>
## `async_compress_and_compare` – Parallel Batch Compression  

**Role** – Dispatches `async_compress` for each element, runs up to four concurrent tasks, and merges results into bundles of size `compress_power`.

| Entity | Type | Role | Notes |
|--------|------|------|------- |
| `data` | `list[str]` | Input | Items to compress. |
| `model` | `AsyncModel` | Input | Async model. |
| `project_settings` | `ProjectSettings` | Input | System prompt source. |
| `compress_power` | `int` | Input | Bundle size (default 4). |
| `progress_bar` | `BaseProgress` | Internal | Tracks overall progress. |
| `compressed_elements` | `list[str]` | Internal | Individual async results. |
| `final_data` | `list[str]` | Output | Concatenated bundles. |

**Flow**  
1. Create a semaphore of 4 permits.  
6. Queue a task for each element via `async_compress`.  
2. Await `asyncio.gather(*tasks)`.  
3. Slice the flat list into chunks of `compress_power` and join with newlines. 
<a name="compress-to-one"></a>
## `compress_to_one` – Recursive Full‑Project Compression  

**Role** – Repeatedly compresses a list until a single string remains; optionally uses async processing.

| Entity | Type | Role | Notes |
|--------|------|------|------- |
| `data` | `list[str]` | Input | Initial fragments. |
| `model` | `Model` | Input | Model for sync or async calls. |
| `project_settings` | `ProjectSettings` | Input | Prompt source. |
| `compress_power` | `int` | Input | Max items per iteration. |
| `use_async` | `bool` | Input | Selects async path. |
| `progress_bar` | `BaseProgress` | Internal | Progress for each iteration. |
| `count_of_iter` | `int` | Internal | Iteration counter. |
| `data` (final) | `str` | Output | Final compressed document. |

**Flow**  
Loop while `len(data) > 1`:  
  • Adjust `compress_power` to 2 when list is smaller than `compress_power+1`.  
  • Call either `async_compress_and_compare` (via `asyncio.run`) or `compress_and_compare`.  
  • Increment iteration counter.  
Return the sole remaining element. 
<a name="async-gpt-model"></a>
## `AsyncGPTModel` – Asynchronous LLM Wrapper  

**Responsibility** – Implements `AsyncModel` for Groq’s async client, handling model rotation, history management, and logging.  

**Logic Flow**  
1. `__init__` → calls `ParentModel.__init__` → shuffles `MODELS_NAME` into `regen_models_name`.  
2. Instantiates `AsyncGroq` client with `api_key`.  
3. `generate_answer` logs start, selects `messages` from `self.history.history` (or a single `prompt`).  
4. Loops until a model succeeds:  
   - Picks `model_name` from `regen_models_name[self.current_model_index]`.  
   - Calls `await self.client.chat.completions.create(messages=messages, model=model_name)`.  
   - On exception logs a warning and advances `current_model_index` (wrap‑around).  
5. On success extracts `chat_completion.choices[0].message.content`, logs result, returns it.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `str` | Authentication token | Defaults to `API_KEY` from config |
| `history` | `History` | Message buffer for context | Provided to `ParentModel` |
| `use_random` | `bool` | Enables random model order | Shuffles `MODELS_NAME` |
| `messages` | `list[dict]` | Payload sent to Groq | Derived from `history` or `prompt` |
| `model_name` | `str` | Current LLM identifier | Rotated on failure |
| `chat_completion` | `AsyncGroq` response | Raw API result | Must contain `choices[0].message.content` |
| Return | `str` | Generated answer | Logged at level 2 |

> **Warning** – If `regen_models_name` becomes empty, `ModelExhaustedException` is raised; ensure at least one model is configured.

--- 
<a name="gpt-model"></a>
## `GPTModel` – Synchronous LLM Wrapper  

**Responsibility** – Mirrors `AsyncGPTModel` for the synchronous Groq client, providing the same rotation and logging logic.  

**Logic Flow**  
1. `__init__` → inherits `ParentModel` setup, creates `Groq` client.  
2. `generate_answer` follows the identical loop as the async version, using `self.client.chat.completions.create`.  
3. Logs success and returns the extracted content.  

**Data Contract** – Same as `AsyncGPTModel` with the only difference being a **synchronous** `client` (`Groq`).  

--- 
<a name="model-base"></a>
## `Model` / `AsyncModel` – Shared Foundations  

**Responsibility** – Provide history handling (`get_answer`, `get_answer_without_history`) and expose `generate_answer` placeholders overridden by subclasses.  

**Visible Interactions**  
- Both subclasses call `self.history.add_to_history` to record *user* and *assistant* turns.  
- They rely on `BASE_SYSTEM_TEXT`, `API_KEY`, and `MODELS_NAME` imported from `autodocgenerator.engine.config.config`.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `history` | `History` | Stores system, user, and assistant messages | Initialized with `BASE_SYSTEM_TEXT` |
| `api_key` | `str` | API credential | Default from config |
| `regen_models_name` | `list[str]` | Rotated list of model identifiers | Shuffled when `use_random=True` |
| `current_model_index` | `int` | Pointer to the next model to try | Reset on each call cycle |
| Return of `get_answer` | `str` | Answer from underlying `generate_answer` | Also updates history |

> **Note** – Base implementations of `generate_answer` return the literal string `"answer"`; real behavior is supplied by `GPTModel` and `AsyncGPTModel`. 
