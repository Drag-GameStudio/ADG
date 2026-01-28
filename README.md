## Executive Navigation Tree
- 📦 Installation & Workflow
  - [install-workflow-description](#install-workflow-description)
- ⚙️ Configuration
  - [autodocconfig-options](#autodocconfig-options)
  - [config-reader-yaml-parsing](#config-reader-yaml-parsing)
  - [project-build-config-model](#project-build-config-model)
  - [projectsettings](#projectsettings)
- 🏗️ Model & Architecture
  - [data-contract](#data-contract)
  - [logic-flow](#logic-flow)
  - [parent-model-hierarchy](#parent-model-hierarchy)
- 📂 Modules & Management
  - [basemodule-definition](#basemodule-definition)
  - [docfactory-implementation](#docfactory-implementation)
  - [custommodule-implementation](#custommodule-implementation)
  - [intro-modules-implementation](#intro-modules-implementation)
  - [manager-class](#manager-class)
  - [manager-class-usage](#manager-class-usage)
  - [module-init-logger-setup](#module-init-logger-setup)
- 📝 Document Generation
  - [asyncgptmodel-implementation](#asyncgptmodel-implementation)
  - [gptmodel-implementation](#gptmodel-implementation)
  - [document-generation-orchestrator](#document-generation-orchestrator)
  - [generate_descriptions_for_code](#generate_descriptions_for_code)
  - [gen_doc_parts](#gen_doc_parts)
  - [async_gen_doc_parts](#async_gen_doc_parts)
  - [write_docs_by_parts](#write_docs_by_parts)
  - [async_write_docs_by_parts](#async_write_docs_by_parts)
- 📄 Content & Descriptions
  - [CONTENT_DESCRIPTION](#CONTENT_DESCRIPTION)
  - [generete_custom_discription](#generete_custom_discription)
  - [generete_custom_discription_without](#generete_custom_discription_without)
- 🔗 Link & Text Processing
  - [extract_links_from_start](#extract_links_from_start)
  - [get_all_html_links](#get_all_html_links)
  - [RegexPattern](#["\\\']?(.*?)["\\\']?)
  - [get_introdaction](#get_introdaction)
  - [get_links_intro](#get_links_intro)
  - [split_text_by_anchors](#split_text_by_anchors)
  - [get_order](#get_order)
  - [split_data](#split_data)
- 🛠️ Utilities
  - [code_mix](#code_mix)
- 📦 Compression
  - [compress](#compress)
  - [compress_and_compare](#compress_and_compare)
  - [async_compress](#async_compress)
  - [async_compress_and_compare](#async_compress_and_compare)
  - [compress_to_one](#compress_to_one)
- ❓ Miscellaneous
  - [missing-fragment](#missing-fragment)

 

<a name="install-workflow-description"></a>
**Installation workflow overview**

1. **Windows PowerShell execution**  
   - Open a PowerShell terminal with administrative rights.  
   - Run the following one‑liner, which downloads the PowerShell installer script directly from the project's repository and executes it in the same session:  
     ```powershell
     irm <raw‑script‑url> | iex
     ```  
   - The command uses `Invoke‑WebRequest` (`irm`) to fetch the script content and pipes it to `iex` (Invoke‑Expression) for immediate execution.

2. **Linux/macOS shell execution**  
   - Open a terminal.  
   - Execute the following command to retrieve the shell installer script from the repository and run it with `bash`:  
     ```bash
     curl -sSL <raw‑script‑url> | bash
     ```  
   - `curl` fetches the script silently (`-s`) while following redirects (`-L`). The output is streamed to `bash` for execution.

3. **GitHub Actions secret configuration**  
   - In the GitHub repository, navigate to **Settings → Secrets and variables → Actions**.  
   - Add a new **secret** named `GROCK_API_KEY`.  
   - Paste the API key you obtained from the Grock documentation into the value field.  
   - Save the secret; the workflow will now have access to `GROCK_API_KEY` as an environment variable during runs.

4. **Workflow behavior**  
   - When the GitHub Action triggers, it will reference the `GROCK_API_KEY` secret to authenticate calls to the Grock service.  
   - The appropriate installer command (PowerShell on Windows runners, Bash on Linux/macOS runners) will be invoked, pulling the latest installer script from the repository and executing it automatically.  

**Key points to remember**  
- Use the raw file URL from the repository for both `irm` and `curl` commands.  
- Ensure the secret is correctly named and stored; GitHub masks its value in logs.  
- Run the commands in a clean environment to avoid conflicts with existing installations. 
<a name="autodocconfig-options"></a>
The configuration file uses a top‑level mapping with several sections:

**Project information**
- `project_name`: a short title for the documentation generator.
- `language`: the language code for the generated text (e.g., “en”).

**Build section**
- `save_logs`: set to `true` to keep generation logs, `false` to discard them.
- `log_level`: numeric level controlling verbosity (higher values give more detail).

**Structure section**
- `include_intro_links`: `true` adds navigation links at the beginning.
- `include_order`: `true` keeps the original order of the processed files.
- `max_doc_part_size`: maximum size of each documentation chunk, expressed as an integer.

**Additional information**
- `global idea`: a free‑form description that will be inserted into the documentation as a project overview.

**Custom descriptions**
- A list of strings that define extra prompts for the generator. Each item can contain placeholders and URLs for installation instructions or other guidance.

When creating the file, follow the YAML syntax shown above, using proper indentation for nested mappings and list items. Use boolean values (`true`/`false`) and integers where indicated. The custom description strings can be written on separate lines prefixed with a hyphen. 
<a name="config-reader-yaml-parsing"></a>
## Config Reader – YAML Parsing  

The **`read_config`** function deserialises a YAML string into three concrete objects used throughout the runner.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_data` | `str` | Raw YAML payload | Must be UTF‑8 encoded |
| `config` | `Config` | Global project configuration | Populated via `Config` setters |
| `custom_modules` | `list[CustomModule│CustomModuleWithOutContext]` | Extension points for documentation generators | Determined by leading “%” token |
| `structure_settings_object` | `StructureSettings` | Controls output segmentation and linking | Loads arbitrary keys from `structure_settings` dict |

**Logic flow**  
1. `yaml.safe_load` → `data` (dict).  
2. Instantiate `Config` & `ProjectBuildConfig`.  
3. Pull `ignore_files`, `language`, `project_name`, `project_additional_info`, `build_settings` from `data`.  
4. `pcs.load_settings(build_settings)`, then chain `config.set_language(...).set_project_name(...).set_pcs(pcs)`.  
5. Iterate `ignore_files` → `config.add_ignore_file`.  
6. Iterate `project_additional_info` → `config.add_project_additional_info`.  
7. Build `custom_modules` list: **`%`** prefix → `CustomModuleWithOutContext`, else `CustomModule`.  
8. Load `structure_settings` into a fresh `StructureSettings` via `load_settings`.  
9. Return `(config, custom_modules, structure_settings_object)`.

> **Deterministic**: No conditionals beyond data‑driven branches; identical input yields identical output.

--- 
<a name="project-build-config-model"></a>
## Project Build Config Model (`ProjectBuildConfig`)  

A simple container for build‑time flags.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `save_logs` | `bool` | Enable persistent logging | Default `False` |
| `log_level` | `int` | Verbosity selector | Default `-1` (unspecified) |
| `load_settings` | `method` | Populate attributes from dict | Direct `setattr` loop |

No methods beyond `load_settings`; the object is attached to `Config` via `set_pcs`. 
<a name="projectsettings"></a>
## `ProjectSettings` – Prompt Builder  

| Entity | Type | Role |
|--------|------|------|
| `project_name` | `str` | Identifier inserted into prompt |
| `info` | `dict` | Additional key‑value pairs |
| `prompt` (property) | `str` | Concatenation of `BASE_SETTINGS_PROMPT`, project name, and each `info` entry (each on its own line) |

**Logic**  
- `add_info` stores arbitrary metadata.  
- `prompt` assembles base prompt, project name, then iterates `self.info` to append `"{key}: {value}"` lines.  

> **Note**: All functions rely exclusively on the LLM interface (`get_answer_without_history`) and a progress‑bar abstraction; no file I/O occurs here. 
<a name="data-contract"></a>
### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `print("ADG")` | side‑effect (stdout) | Simple identification signal emitted at import time. | No return value; executed once per interpreter session. |
| `BaseLogger` | class (import) | Core logging facility used throughout the package. | Imported but not instantiated elsewhere in this file. |
| `BaseLoggerTemplate` | class (import) | Provides the default formatting/handler configuration for the logger. | Passed to `logger.set_logger`. |
| `logger` | `BaseLogger` instance | Shared logger instance exposed as a module‑level variable. | Other modules can `from autodocgenerator import logger`. |
| `InfoLog`, `ErrorLog`, `WarningLog` | classes (import) | Specialized log record types. | Imported for external use; not instantiated here. |

> **⚠️ Note** – The module does **not** perform file I/O, network calls, or alter global state beyond the stdout side‑effect and logger creation.

--- 
<a name="logic-flow"></a>
### Execution Flow (Step‑by‑Step)

1. **Import phase** – Python evaluates the file linearly.  
2. **`print` execution** – Immediately writes `"ADG"` to the console.  
3. **Symbol import** – Retrieves logger‑related classes from `autodocgenerator.ui.logging`.  
4. **Logger instantiation** – Calls `BaseLogger()` → creates a logger object.  
5. **Template binding** – Calls `logger.set_logger(BaseLoggerTemplate())` → attaches the default template to the logger.  
6. **Export** – The module’s namespace now contains the ready‑to‑use `logger` and the imported log‑type classes.

No additional functions or conditional branches are present; the module’s behavior is fully deterministic and repeatable on each import. 
<a name="parent-model-hierarchy"></a>
## Core Model Hierarchy (`ParentModel`, `Model`, `AsyncModel`)

**Responsibility** – Supplies shared state (API key, history, model rotation) for concrete generators.  
**Visible interactions** – Other modules import `Model`/`AsyncModel` via `gpt_model.py`; they receive a pre‑configured instance from the orchestrator.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `str` | Authentication token | Defaulted to `API_KEY` from config |
| `history` | `History` | Conversational buffer | Injected or created lazily |
| `use_random` | `bool` | Controls shuffling of `MODELS_NAME` | Randomised on each instantiation |
| `current_model_index` | `int` | Index of the active model | Starts at 0 |
| `regen_models_name` | `list[str]` | Rotation list of model identifiers | Shuffled when `use_random=True` |

**Logic flow**  
1. `ParentModel.__init__` stores `api_key` & `history`.  
2. Copies global `MODELS_NAME`; shuffles if `use_random`.  
3. Exposes `regen_models_name` & `current_model_index` for child classes.  

--- 
<a name="basemodule-definition"></a>
## Abstract Base Module (`BaseModule`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseModule` | `ABC` | Contract for all doc‑generation blocks | Requires `generate(info: dict, model: Model)` |
| `__init__` | `method` | No‑op constructor | Allows subclass‑specific init |
| `generate` | `abstractmethod` | Core payload generator | Must return a **string** fragment |

> **Assumption** – Sub‑classes provide concrete logic; the base class itself does not produce output.

--- 
<a name="docfactory-implementation"></a>
## Documentation Orchestrator (`DocFactory`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `modules` | `list[BaseModule]` | Ordered generators supplied at construction | Stored as‑is |
| `logger` | `BaseLogger` | Centralised logging | Uses `InfoLog` |
| `generate_doc` | `method` | Executes each module, aggregates results, updates progress | Returns the full markdown document |

**Logic flow**  
1. Initialise `output = ""`.  
2. Call `progress.create_new_subtask("Generate parts", len(self.modules))`.  
3. Iterate `module` in `self.modules`:  
   - `module_result = module.generate(info, model)`  
   - Append `module_result` and two newlines to `output`.  
   - Log module completion (`InfoLog`).  
   - Log raw module output at level 2.  
   - `progress.update_task()`.  
4. After loop, `progress.remove_subtask()` and return `output`.

> **Warning** – The `__main__` guard instantiates `BaseModule()` directly, which is abstract and would raise `TypeError` if executed.

--- 
<a name="custommodule-implementation"></a>
## Custom Content Modules (`CustomModule`, `CustomModuleWithOutContext`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `discription` | `str` | User‑provided header for the custom block | Set in ctor |
| `generate` (both) | `method` | Calls post‑processor to build a custom description | Returns a **string** |

**CustomModule** –  
1. Split `info["code_mix"]` into ≤ 5000‑symbol chunks via `split_data`.  
2. Invoke `generete_custom_discription` with the chunks, model, description, and language.  

**CustomModuleWithOutContext** –  
1. Directly call `generete_custom_discription_without` with model, description, and language (no code context).  

Both rely exclusively on the imported post‑processor functions; no side effects beyond the returned string.

--- 
<a name="intro-modules-implementation"></a>
## Intro Extraction Modules (`IntroLinks`, `IntroText`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `generate` | `method` | Produces introductory material | Returns a **string** |
| `links` / `intro` | `str` | Intermediate data from helpers | Obtained from `info` dict |

**IntroLinks** –  
1. `get_all_html_links(info["full_data"])` → `links`.  
2. `get_links_intro(links, model, info["language"])` → `intro_links`.  

**IntroText** –  
1. `get_introdaction(info["global_data"], model, info["language"])` → `intro`.  

Both modules delegate all heavy lifting to the imported `custom_intro` helpers and simply forward the resulting markdown snippet. 
<a name="manager-class"></a>
## `Manager` – Orchestrator of Project‑wide Documentation Pipeline

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `CACHE_FOLDER_NAME` | `str` | Fixed cache directory name | `".auto_doc_cache"` |
| `FILE_NAMES` | `dict[str,str]` | Maps logical keys to cache filenames | Used by `get_file_path` |
| `__init__` | `method` | Sets configuration, logger, progress UI, creates cache folder | `progress_bar` defaults to a fresh `BaseProgress()` instance |
| `read_file_by_file_key` | `method` | Returns raw text of a cached file | Reads UTF‑8, key resolved via `FILE_NAMES` |
| `get_file_path` | `method` | Constructs absolute cache path for a given key | Combines `project_directory`, `CACHE_FOLDER_NAME`, and `FILE_NAMES` |
| `generate_code_file` | `method` | Builds a **code‑mix** file from the repository | Uses `CodeMix.build_repo_content` |
| `generete_doc_parts` | `method` | Splits `code_mix` into ≤ 5 000‑symbol chunks and generates markdown via `gen_doc_parts` | Writes result to `output_doc` |
| `factory_generate_doc` | `method` | Invokes a `DocFactory` to prepend additional modules to the existing doc | Merges new fragments with current output |
| `order_doc` | `method` | Re‑orders markdown sections by anchor using `split_text_by_anchors` & `get_order` | Overwrites `output_doc` |
| `clear_cache` | `method` | Optionally removes the log file based on `config.pbc.save_logs` | No other side‑effects |

> **Warning** – The default argument `progress_bar: BaseProgress = BaseProgress()` creates a mutable instance at import time; repeated `Manager` constructions share the same progress object.

### Initialization Flow
1. Store `project_directory`, `config`, optional models, and `progress_bar`.  
2. Initialise `BaseLogger` and attach a `FileLoggerTemplate` targeting the cache `logs` file.  
3. Ensure the cache folder exists (`os.mkdir` if absent).

### Core Operations  

#### 1. `generate_code_file`
1. Log start (`InfoLog`).  
2. Instantiate `CodeMix` with `project_directory` and `config.ignore_files`.  
3. Call `cm.build_repo_content` → writes `code_mix.txt`.  
4. Log completion and advance the progress bar.

#### 2. `generete_doc_parts`
1. Load `code_mix.txt`.  
2. Log start, invoke `gen_doc_parts(full_code_mix, max_symbols, sync_model, config.language, progress_bar)`.  
3. Persist returned markdown to `output_doc.md`.  
4. Log finish and update progress.

#### 3. `factory_generate_doc`
1. Load current `output_doc.md` and `code_mix.txt`.  
2. Assemble `info` dict (`language`, `full_data`, `code_mix`).  
3. Log detailed start message including module names and input sizes.  
4. Call `doc_factory.generate_doc(info, sync_model, progress_bar)`.  
5. Prepend new fragments to the existing doc and write back.  
6. Update progress.

#### 4. `order_doc`
1. Read current `output_doc.md`.  
2. Split by markdown anchors (`split_text_by_anchors`).  
3. If split succeeded, reorder sections via `get_order(sync_model, parts)`.  
4. Overwrite `output_doc.md` with ordered content.

#### 5. `clear_cache`
1. If `config.pbc.save_logs` is `False`, delete the `report.txt` log file.

All side‑effects are confined to file system writes within the hidden cache directory and logger emissions; no network or external state is accessed beyond the injected `Model` instances. 
<a name="manager-class-usage"></a>!noinfo 
<a name="module-init-logger-setup"></a>
## Module Initialization & Logger Configuration

The **`autodocgenerator/__init__.py`** module performs three concrete actions when the package is imported:

1. Emits a literal string **`"ADG"`** to *stdout* via `print`.
2. Imports the public logger classes from `autodocgenerator.ui.logging`:
   ```python
   from .ui.logging import BaseLogger, BaseLoggerTemplate, InfoLog, ErrorLog, WarningLog
   ```
3. Instantiates a **singleton‑style logger** and binds a default template:
   ```python
   logger = BaseLogger()
   logger.set_logger(BaseLoggerTemplate())
   ```

These steps make a ready‑to‑use `logger` object available to any sub‑module that imports `autodocgenerator`.

--- 
<a name="asyncgptmodel-implementation"></a>
## Asynchronous Generator (`AsyncGPTModel`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `client` | `AsyncGroq` | Async LLM client | Instantiated with `api_key` |
| `logger` | `BaseLogger` | Async‑compatible logger | Same log classes as sync version |
| `generate_answer` | `async method` | Async request/response loop | Returns `awaitable str` |

**Logic flow** (mirrors `GPTModel` but using `await`):  
1. Log async start.  
2. Resolve `messages` from history or `prompt`.  
3. `while True` loop with the same exhaustion check and model rotation.  
4. `await self.client.chat.completions.create(...)`.  
5. On failure: log warning, rotate index, continue.  
6. After success, extract `result`, log both model used and answer, then `return result`.

**Interaction pattern** – Consumed by the orchestrator (`gen_doc`) via `await model.generate_answer(...)`; shares the same rotation logic as the sync counterpart. 
<a name="gptmodel-implementation"></a>
## Synchronous Generator (`GPTModel`)

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `client` | `Groq` | Remote LLM client | Created with `api_key` |
| `logger` | `BaseLogger` | Structured logging | Uses `InfoLog`, `ErrorLog`, `WarningLog` |
| `generate_answer` | `method` | Core request/response loop | Returns `str` |

**Logic flow**  
1. Log start of generation.  
2. Choose `messages` from `history` or supplied `prompt`.  
3. Loop:  
   - If `regen_models_name` empty → log error & raise `ModelExhaustedException`.  
   - Pick `model_name` at `current_model_index`.  
   - Attempt `self.client.chat.completions.create(messages=messages, model=model_name)`.  
   - On exception: log warning, advance index (wrap‑around), retry.  
4. Extract `result` from `chat_completion.choices[0].message.content`.  
5. Log success & result (level 2).  
6. Return `result`.

> **Determinism** – Outcome depends only on input data and external API responses; no hidden branches.

--- 
<a name="document-generation-orchestrator"></a>
## Document Generation Orchestrator (`gen_doc`)  

Coordinates model instantiation, manager setup, and final document retrieval.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_path` | `str` | Root of source tree | Passed to `Manager` |
| `config` | `Config` | Project‑wide settings | From `read_config` |
| `custom_modules` | `list[CustomModule│CustomModuleWithOutContext]` | Doc factories | Forwarded to `DocFactory` |
| `structure_settings` | `StructureSettings` | Output segmentation flags | Controls ordering & intro links |

**Step‑by‑step**  
1. Instantiate `GPTModel` (sync) & `AsyncGPTModel` (async) with global `API_KEY`.  
2. Build `Manager` with path, config, models, and a `ConsoleGtiHubProgress` bar.  
3. Call `manager.generate_code_file()`.  
4. Split docs via `manager.generete_doc_parts(max_symbols=structure_settings.max_doc_part_size)`.  
5. Feed custom factories: `manager.factory_generate_doc(DocFactory(*custom_modules))`.  
6. If `include_order` → `manager.order_doc()`.  
7. If `include_intro_links` → `manager.factory_generate_doc(DocFactory(IntroLinks()))`.  
8. Clean temporary cache, then `manager.read_file_by_file_key("output_doc")` is returned.

--- 
<a name="generate_descriptions_for_code"></a>
## `generate_descriptions_for_code` – LLM‑driven Doc Generation  

| Entity | Type | Role |
|--------|------|------|
| `data` | `list[str]` | Code snippets |
| `model` | `Model` | LLM |
| `project_settings` | `ProjectSettings` | Unused (present for signature) |
| `progress_bar` | `BaseProgress` | Progress |
| return | `list[str]` | Model answers (descriptions) |

**Logic**  
- For each `code` create a two‑message prompt (instruction block + `CONTEXT: {code}`), call `model.get_answer_without_history`, append answer, update progress. 
<a name="gen_doc_parts"></a>
## `gen_doc_parts` – Synchronous Batch Documentation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `full_code_mix` | `str` | Complete source to split | |
| `max_symbols` | `int` | Chunk size for `split_data` | |
| `model` | `Model` | LLM used for each part | |
| `language` | `str` | Output language | |
| `progress_bar` | `BaseProgress` | Sub‑task progress tracker | |
| **return** | `str` | Concatenated documentation of all parts | |

**Logic**  
1. Call `split_data` → list of parts.  
2. Create a sub‑task in `progress_bar` with total length = number of parts.  
3. Iterate parts: invoke `write_docs_by_parts`, append result to `all_result`, keep last 3000 characters of the current result for next iteration (`prev_info`). Update progress bar each loop.  
4. Remove sub‑task, log final length, and return the assembled document. 
<a name="async_gen_doc_parts"></a>
## `async_gen_doc_parts` – Asynchronous Batch Documentation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `full_code_mix` | `str` | Source code | |
| `global_info` | `str` | Passed to each async task (unused in prompt) | |
| `max_symbols` | `int` | Chunk size | |
| `model` | `AsyncModel` | Async LLM | |
| `language` | `str` | Output language | |
| `progress_bar` | `BaseProgress` | Sub‑task progress manager | |
| **return** | `str` | Full documentation assembled from async tasks | |

**Logic**  
1. Split source via `split_data`.  
2. Initialise a sub‑task in `progress_bar`.  
3. Create a semaphore (`4` permits).  
4. Build a list of `async_write_docs_by_parts` tasks, each receiving the shared semaphore and a lambda that updates the progress bar.  
5. `await asyncio.gather(*tasks)` → list of part documents.  
6. Concatenate results with double newlines, clean up sub‑task, log final length, and return.  

> **Critical assumption**: All logging is performed through `BaseLogger`; no file I/O occurs in this module. 
<a name="write_docs_by_parts"></a>
## `write_docs_by_parts` – Synchronous Part‑wise Doc Generation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | Code fragment to document | |
| `model` | `Model` | Synchronous LLM interface | Provides `get_answer_without_history` |
| `prev_info` | `str` | Optional prior output | Inserted into prompt when present |
| `language` | `str` | Target language for docs | Default `"en"` |
| **return** | `str` | Generated documentation for the part | May be trimmed of surrounding ````` markers |

**Logic**  
1. Build a system‑message list: language hint, `BASE_PART_COMPLITE_TEXT`, optional previous info, then the user message containing `part`.  
2. Call `model.get_answer_without_history(prompt)`.  
3. Strip leading/trailing markdown fences (`````), log length and content, and return the cleaned answer. 
<a name="async_write_docs_by_parts"></a>
## `async_write_docs_by_parts` – Async Part‑wise Doc Generation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | Code fragment | |
| `async_model` | `AsyncModel` | Async LLM interface | Provides `await get_answer_without_history` |
| `global_info` | `str` | Unused in prompt construction | Present for signature compatibility |
| `semaphore` | `asyncio.Semaphore` | Concurrency limiter | Acquired via `async with` |
| `prev_info` | `str` | Optional prior output | |
| `language` | `str` | Target language | |
| `update_progress` | `callable` | Optional progress callback | Invoked after answer received |
| **return** | `str` | Documentation for the part | Fence‑stripped like the sync version |

**Logic** mirrors the synchronous variant, wrapped in `async with semaphore:` and awaiting the model call. Progress is reported if `update_progress` is supplied. 
<a name="CONTENT_DESCRIPTION"></a>` tag |

**Logic**  
1. Create a prompt with three system messages: language, analyst role, and a rule‑enforced template demanding a single anchor tag with no filenames, extensions, generic terms, or URLs.  
2. Append a user message containing the task.  
3. Call `model.get_answer_without_history`.  
4. Return the raw answer.

---  

**Cross‑Component Interaction**  
All functions rely on `BaseLogger` for internal diagnostics and on a `Model` implementation (e.g., `GPTModel`) to obtain LLM responses. No other modules are referenced; constants are imported from `engine.config.config`. The module therefore acts as a **post‑processing helper** that extracts navigation anchors and orchestrates LLM‑driven intro and custom description creation. 
<a name="generete_custom_discription"></a>
## `generete_custom_discription` – Context‑Sensitive Custom Description  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `splited_data` | `str` (iterable) | Chunked documentation pieces | Iterated until a satisfactory result |
| `model` | `Model` | LLM interface | |
| `custom_description` | `str` | User‑specified description task | |
| `language` | `str` | Prompt language | Default `"en"` |
| return | `str` | First LLM answer that passes filters | Empty string if none succeed |

**Logic**  
1. Loop over each `sp_data` in `splited_data`.  
2. Build a multi‑system‑message prompt: language, analyst role, context (`sp_data`), constant `BASE_CUSTOM_DISCRIPTIONS`, and the task.  
3. Invoke `model.get_answer_without_history`.  
4. If the result does **not** contain `"!noinfo"` or `"No information found"` (or those markers appear after position 30), break and keep the answer.  
5. Otherwise reset `result` and continue.  
6. Return the final `result`.

--- 
<a name="generete_custom_discription_without"></a>
## `generete_custom_discription_without` – Stand‑Alone Description Generation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | LLM interface | |
| `custom_description` | `str` | Desired description task | |
| `language` | `str` | Prompt language | Default `"en"` |
| return | `str` | LLM answer that obeys strict tag rules | Must start with a single ` 
<a name="extract_links_from_start"></a>
## `extract_links_from_start` – Anchor Extraction  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `chunks` | `list[str]` | Text blocks to scan | Expected to start with an `<a name=…>` tag |
| `links` | `list[str]` | Collected anchors | Prefixed with “#” |
| `pattern` | `str` | Regex `^<a name=["']?(.*?)["']?</a>` | Captures the name attribute at the very start of a chunk |
| return | `list[str]` | Anchor list (only names > 5 chars) | Empty list if none match |

**Logic**  
1. Initialise empty `links`.  
2. For each `chunk` → `chunk.strip()` → `re.search(pattern)`.  
3. If a match and `len(anchor_name) > 5` → append `"#"+anchor_name`.  
4. Return `links`.

> **Assumption**: Only leading anchors are considered; embedded anchors are ignored. 
<a name="get_all_html_links"></a>
## `get_all_html_links` – HTML Anchor Extraction  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Source markdown/HTML text | Expected to contain `<a name="…"></a>` anchors |
| return | `list[str]` | Collected link identifiers | Each returned as `#anchor_name` (anchors longer than 5 chars) |

**Logic**  
1. Instantiate a fresh `BaseLogger`.  
2. Log start message.  
3. Compile regex `r'<a name=["\']?(.*?)["\']?></a>'`.  
4. Iterate over `re.finditer`; for each match, capture group 1.  
5. If captured name length > 5, prepend `#` and append to `links`.  
6. Log count and list of links (debug level 1).  
7. Return the list.  

> **Note** – No filesystem or network access; pure string processing.

--- 
<a name="get_introdaction"></a>
## `get_introdaction` – Global Introduction Generation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `global_data` | `str` | Full documentation content | Sent as user prompt |
| `model` | `Model` | LLM interface | Same contract as above |
| `language` | `str` | Prompt language | Default `"en"` |
| return | `str` | Generated introduction text | No logging performed in this fragment |

**Logic**  
1. Assemble prompt: language system message, constant `BASE_INTRO_CREATE`, and `global_data`.  
2. Call `model.get_answer_without_history`.  
3. Return the answer.

--- 
<a name="get_links_intro"></a>
## `get_links_intro` – Intro Generation with Links  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `links` | `list[str]` | Anchor list from `get_all_html_links` | Serialized via `str()` for prompt |
| `model` | `Model` | LLM interface | Must implement `get_answer_without_history` |
| `language` | `str` | Prompt language selector | Default `"en"` |
| return | `str` | Generated introductory markdown | Contains the supplied links |

**Logic**  
1. Create `BaseLogger`.  
2. Build a system‑user prompt array: set language, inject constant `BASE_INTRODACTION_CREATE_LINKS`, and pass stringified `links`.  
3. Log generation start.  
4. Call `model.get_answer_without_history(prompt=prompt)`.  
5. Log completion and raw result (debug level 1).  
6. Return the LLM’s answer.

--- 
<a name="split_text_by_anchors"></a>
## `split_text_by_anchors` – Chunk Segmentation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `text` | `str` | Full markdown source | Contains `<a name=…>` anchors |
| `pattern` | `str` | Look‑ahead regex `(?=<a name=["']?[^"\'>\s]{6,200}["']?</a>)` | Splits **before** each valid anchor |
| `result_chanks` | `list[str]` | Trimmed non‑empty chunks | One per anchor |
| `all_links` | `list[str]` | Output of `extract_links_from_start` | Must align with `result_chanks` |
| return | `dict[str,str]` or `None` | Mapping `#anchor → chunk` | `None` if counts differ |

**Logic**  
1. `re.split` on `pattern` → raw `chunks`.  
2. Strip and filter empty entries → `result_chanks`.  
3. Call `extract_links_from_start(result_chanks)` → `all_links`.  
4. If `len(all_links) != len(result_chanks)` → `return None`.  
5. Build dict pairing each link with its corresponding chunk. 
<a name="get_order"></a>
## `get_order` – Semantic Title Ordering  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | LLM interface | Provides `get_answer_without_history` |
| `chanks` | `dict[str,str]` | Anchor‑to‑content map | Keys are `#anchor` strings |
| `logger` | `BaseLogger` | Diagnostic output | Uses `InfoLog` at various levels |
| return | `str` | Concatenated content in LLM‑suggested order | Ends with newline after each chunk |

**Logic**  
1. Log start and input keys/values.  
2. Build single‑message prompt asking the model to **return a comma‑separated list** of the titles (keys) sorted semantically, preserving the leading “#”.  
3. Call `model.get_answer_without_history(prompt)`.  
4. Split result on commas, strip whitespace → `new_result`.  
5. Iterate `new_result`; for each key `el` append `chanks[el]` and a newline to `order_output`, logging each addition.  
6. Return `order_output`. 
<a name="split_data"></a>
## `split_data` – Text Chunking Engine  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Raw source text | May contain newline separators |
| `max_symbols` | `int` | Upper size limit for a chunk (symbols) | Used with 1.25 ×  and 1.5 ×  heuristics |
| **return** | `list[str]` | List of chunk strings | Each ≤ `max_symbols` ≈ target size |

**Logic**  
1. Split `data` on newline (`"\n"`).  
2. Repeatedly scan the list; any element longer than `1.5 × max_symbols` is cut in half (first half kept, second half inserted after). Loop until no element exceeds the threshold.  
3. Accumulate elements into `split_objects`, starting a new chunk when the current one would exceed `1.25 × max_symbols`. Newlines are inserted between concatenated parts.  
4. Log start and completion via `BaseLogger`. 
<a name="code_mix"></a>
## `CodeMix` – Repository Snapshot Builder  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `root_dir` | `Path` | Base directory for scanning | Resolved at init |
| `ignore_patterns` | `list[str]` | Glob patterns to exclude | Defaults to empty list |
| `logger` | `BaseLogger` | Progress logger | Uses `InfoLog` |
| `should_ignore(path)` | `bool` | Determines exclusion | Checks path, basename, and each part against patterns |
| `build_repo_content(output_file)` | `None` | Writes repository tree and file contents to `output_file` | Inserts `<file path="…">` tags before each file block |
| return | `None` | Side‑effect: file creation | Prints a completion message in `__main__` |

**Logic**  
1. Open `output_file` for writing.  
2. Write “Repository Structure:” header.  
3. Walk `root_dir.rglob("*")` sorted; for each `path` not ignored, compute depth → indentation → write directory or file line.  
4. Write separator line (`"="*20`).  
5. Walk again; for each non‑ignored file, write `<file path="relative_path">`, then the file’s raw text, then two newlines. Errors are caught and written as `"Error reading …"`.

> **Warning**: Files matching any pattern in `ignore_patterns` (e.g., `*.pyc`, `venv`, `.git`) are silently skipped. 
<a name="compress"></a>
## `compress` – Single‑File LLM Compression  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Raw source text | – |
| `project_settings` | `ProjectSettings` | Supplies system prompt via `project_settings.prompt` | – |
| `model` | `Model` | LLM interface, provides `get_answer_without_history` | – |
| `compress_power` | `int` | Controls token budget for `BASE_COMPRESS_TEXT` | – |
| return | `str` | LLM‑generated compressed text | – |

**Logic**  
1. Build `prompt` list: system prompt from settings, token‑budget prompt from `get_BASE_COMPRESS_TEXT(10000, compress_power)`, then user content `data`.  
2. Call `model.get_answer_without_history(prompt=prompt)`.  
3. Return the answer unchanged. 
<a name="compress_and_compare"></a>
## `compress_and_compare` – Sync Batch Compression  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | Files to compress | – |
| `model` | `Model` | LLM instance | – |
| `project_settings` | `ProjectSettings` | Prompt source | – |
| `compress_power` | `int` | Chunk size (default 4) | – |
| `progress_bar` | `BaseProgress` | Visual progress | Default instance |
| return | `list[str]` | Concatenated chunks, one per `compress_power` files | – |

**Logic**  
1. Allocate result list sized `ceil(len(data)/compress_power)`.  
2. Initialise sub‑task on `progress_bar`.  
3. For each element `el` at index `i`: compute `curr_index = i // compress_power`; append `compress(el, …)` + newline to that slot; update progress.  
4. Remove sub‑task and return the list. 
<a name="async_compress"></a>
## `async_compress` – Async Single Compression  

| Entity | Type | Role |
|--------|------|------|
| `data` | `str` | Source text |
| `project_settings` | `ProjectSettings` | Prompt source |
| `model` | `AsyncModel` | Async LLM |
| `compress_power` | `int` | Token budget |
| `semaphore` | `asyncio.Semaphore` | Concurrency guard |
| `progress_bar` | `BaseProgress` | Progress update |
| return | `str` | Compressed result |

**Logic**  
- Acquire semaphore, build identical prompt as `compress`, await `model.get_answer_without_history`, update progress, release semaphore, return answer. 
<a name="async_compress_and_compare"></a>
## `async_compress_and_compare` – Async Batch  

| Entity | Type | Role |
|--------|------|------|
| `data` | `list[str]` | Files |
| `model` | `AsyncModel` | LLM |
| `project_settings` | `ProjectSettings` | Prompt |
| `compress_power` | `int` | Chunk size |
| `progress_bar` | `BaseProgress` | Sub‑task |
| return | `list[str]` | Chunked concatenations |

**Logic**  
1. Semaphore = 4, spawn `async_compress` tasks for each file.  
2. `await asyncio.gather` → `compressed_elements`.  
3. Group results by `compress_power`, join with newlines, add trailing newline. 
<a name="compress_to_one"></a>
## `compress_to_one` – Iterative Reduction  

| Entity | Type | Role |
|--------|------|------|
| `data` | `list[str]` | Initial chunks |
| `model` | `Model` | LLM |
| `project_settings` | `ProjectSettings` | Prompt |
| `compress_power` | `int` | Base chunk size |
| `use_async` | `bool` | Switch between sync/async |
| `progress_bar` | `BaseProgress` | Progress |
| return | `str` | Single aggregated compressed block |

**Logic**  
- Loop while `len(data) > 1`; adjust `compress_power` (minimum 2); call either `async_compress_and_compare` via `asyncio.run` or `compress_and_compare`; increment iteration counter. Final element returned. 

