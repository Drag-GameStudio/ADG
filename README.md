## Executive Navigation Tree
* 📂 Setup & Configuration
  * [Install Workflow Setup](#install-workflow-setup)
  * [Reusable Docs Workflow](#reusable-docs-workflow)
  * [Run File Documentation Pipeline](#run-file-documentation-pipeline)
  * [DocFactory](#docfactory)
  * [Factory Generate Doc](#factory-generate-doc)
  * [Write Docs By Parts](#write-docs-by-parts)
  * [Generate Code File](#generate-code-file)
  * [Generate Global Info](#generate-global-info)
  * [Generate Doc Parts](#generate-doc-parts)
  * [Order Doc](#order-doc)
  * [AutoDocFile Settings](#autodocfile-settings)
  * [Config Reader Yaml Parsing](#config-reader-yaml-parsing)
* ⚙️ Core Engine
  * [Get Path](#get-path)
  * [Read File](#read-file)
  * [CLI Entrypoint](#cli-entrypoint)
  * [Manager Class Usage and Methods](#manager-class-usage-and-methods)
  * [Manager Orchestrator](#manager-orchestrator)
  * [BaseModule](#basemodule)
  * [CustomModule](#custommodule)
  * [CustomModuleWithout](#custommodulewithout)
  * [Async GPTModel Class](#async-gptmodel-class)
  * [GPTModel Class](#gptmodel-class)
  * [Code Mix Class](#code-mix-class)
  * [ProjectSettings Class](#projectsettings-class)
  * [ProjectSettings](#projectsettings)
  * [PyProject Toml Config](#pyproject-toml-config)
* 📄 Information Extraction
  * [IntroLinks](#introlinks)
  * [IntroText](#introtext)
  * [Get All HTML Links](#get-all-html-links)
  * [Get Links Intro](#get-links-intro)
  * [Get Introdaction](#get-introdaction)
  * [Extract Links From Start](#extract-links-from-start)
  * [Split Text By Anchors](#split-text-by-anchors)
  * [Get Order](#get-order)
* 📈 Utilities
  * [Clear Cache](#clear-cache)
  * [Generate Custom Description](#generate-custom-description)
  * [Generate Custom Description Without](#generate-custom-description-without)
  * [Content Description](#CONTENT_DESCRIPTION)
  * [Compress Function](#compress-function)
  * [Compress Func](#compress-func)
  * [Compress and Compare](#compress-and-compare)
  * [Compress Compare](#compress-compare)
  * [Compress To One](#compress-to-one)
  * [BaseProgress Abstract](#baseprogress-abstract)
  * [LibProgress Concrete](#libprogress-concrete)
  * [Consoletask Helper](#consoletask-helper)
  * [ConsoleGithubProgress Implementation](#consolegithubprogress-implementation)
  * [Spliter Partial](#spliter-partial)

 

<a name="install-workflow-setup"></a>

**Installation workflow overview**

1. **Windows PowerShell execution**  
   Open a PowerShell terminal with administrative rights and execute the following one‑liner:  

   ```powershell
   irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/install-script | iex
   ```

   - `irm` fetches the installer script directly from the repository.  
   - The pipeline to `iex` evaluates the retrieved script in the current session, performing all necessary setup steps.

2. **Linux/macOS shell execution**  
   Open a terminal and run the equivalent command for POSIX shells:  

   ```bash
   curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/install-script | bash
   ```

   - `curl -sSL` silently downloads the installer script.  
   - The output is piped to `bash`, which executes the script to complete the installation.

3. **GitHub Actions secret configuration**  
   To enable the workflow to interact with the external service, add a secret variable to the repository’s GitHub Actions environment:

   - **Name:** `GROCK_API_KEY`  
   - **Value:** the API key obtained from the official Grock documentation (consult the Grock docs for retrieval instructions).

   This secret will be automatically injected into the workflow runtime, allowing authenticated calls to the Grock API.

4. **Verification**  
   After executing the appropriate installer command, verify that the expected binaries, environment variables, and GitHub Actions secret are correctly set up by:

   - Checking the output logs for a “setup completed” message.  
   - Inspecting the GitHub Actions settings page to confirm the presence of `GROCK_API_KEY`.  

Following these steps ensures a consistent, automated installation across Windows and Linux environments, with secure API access for subsequent CI/CD processes. 
<a name="reusable-docs-workflow"></a>
## Reusable Documentation Workflow (`reuseble_agd.yml`)

**Functional role** – Executes the *Auto Doc Generator* as a callable GitHub Action, producing a markdown documentation file and optional log artifact, then commits the changes back to the repository.

### Visible Interactions
| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `GROCK_API_KEY` | secret | Auth token for the LLM service | Passed to the container as `API_KEY` |
| `autodocgenerator` package | dependency | Provides the CLI entry point `python -m autodocgenerator.auto_runner.run_file` | Installed via `pip install autodocgenerator` |
| `.auto_doc_cache/output_doc.md` | file | Generated documentation source | Copied into `README.md` |
| `.auto_doc_cache/report.txt` | file | Optional log output | Appended to `agd_report.txt` if present |
| Git repository | VCS | Target for commit/push | Updated by the action itself |

### Technical Logic Flow
1. **Checkout** – `actions/checkout@v4` places the repo in the runner workspace.  
2. **Setup Python** – `actions/setup-python@v5` installs Python 3.12.  
3. **Install ADG** – `pip install autodocgenerator` makes the library available.  
4. **Run generator** – Executes `python -m autodocgenerator.auto_runner.run_file` with environment variables:  
   - `API_KEY` ← `${{ secrets.GROCK_API_KEY }}`  
   - `PYTHONUNBUFFERED=1`, `FORCE_COLOR=1`, `TERM=xterm-256color`.  
5. **Publish docs** – `cat .auto_doc_cache/output_doc.md > README.md` overwrites the repository’s README.  
6. **Collect logs** – Attempts to concatenate `.auto_doc_cache/report.txt` into `agd_report.txt`; ignores failure.  
7. **Commit & push** – Configures a bot identity, stages `README.md` and `agd_report.txt`, commits only if changes exist, and pushes to the default branch.

### Data Contract
| Entity | Type | Role | Notes |
|--------|------|------|-------|
| Input secret `GROCK_API_KEY` | string (secret) | Authenticates LLM calls inside ADG | Required; missing leads to failure. |
| Generated file `output_doc.md` | markdown | Primary documentation output | Must exist after step 4; otherwise commit fails. |
| Optional file `report.txt` | text | Execution log | May be absent; step 6 tolerates missing file. |
| Final `README.md` | markdown | Repository entry point for users | Replaced wholesale; ensure downstream CI tolerates changes. |

> **⚠️** The workflow **writes** directly to `README.md`. If the repository relies on a custom README layout, incorporate a merge strategy or preserve sections before invoking this action. 
<a name="run-file-documentation-pipeline"></a>
## RunFile – End‑to‑End Documentation Generation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `gen_doc` | function | Orchestrates the full generation workflow using the supplied `Config`, modules, and `StructureSettings`. | Returns the final markdown string. |
| `sync_model`, `async_model` | `GPTModel` / `AsyncGPTModel` | LLM wrappers used by `Manager`. | Created with global `API_KEY`. |
| `manager` | `Manager` | Core orchestrator handling code extraction, global compression, part creation, factory calls, ordering, intro links, and cache cleanup. | Initialized with path, config, models, and a progress bar. |
| `DocFactory` | class | Factory that receives custom modules (including `IntroLinks`) and produces documentation parts. | Instantiated per call to `manager.factory_generate_doc`. |

**Step‑by‑Step Execution**  
1. Instantiate LLM wrappers.  
2. Create `Manager` with project root, `config`, models, and a `ConsoleGtiHubProgress` bar.  
3. `manager.generate_code_file()` – extracts repository source into a mixed text file.  
4. If `structure_settings.use_global_file` → `manager.generate_global_info(compress_power=4)` compresses the mixed text.  
5. `manager.generete_doc_parts(max_symbols=…, with_global_file=…)` chunks the (optional) global file into parts respecting `max_doc_part_size`.  
6. `manager.factory_generate_doc(DocFactory(*custom_modules))` runs the LLM on each part via the supplied custom modules.  
7. If ordering enabled → `manager.order_doc()` re‑orders parts.  
8. If intro links enabled → another factory call with `IntroLinks()` inserts navigation anchors.  
9. `manager.clear_cache()` removes temporary artifacts.  
10. Return `manager.read_file_by_file_key("output_doc")` – the assembled markdown.  

> **Warning** – The script overwrites `README.md`; callers must ensure downstream CI tolerates this replacement. 
<a name="docfactory"></a>
## `DocFactory` – Pipeline Coordinator  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `modules` | `list[BaseModule]` | Ordered plugin collection | Supplied at construction |
| `logger` | `BaseLogger` | Structured event recorder | Logs module success |
| `generate_doc` | `def` | Executes each module, aggregates results | Returns final markdown string |

**Responsibility** – Drives the documentation generation pipeline: creates a progress sub‑task, invokes every registered `BaseModule`, concatenates their outputs, and logs each step.  

**Visible Interactions**  
- Calls `module.generate(info, model)` for each plugin.  
- Updates `BaseProgress` via `create_new_subtask`, `update_task`, `remove_subtask`.  
- Emits `InfoLog` entries through `BaseLogger`.  

**Logic Flow**  
1. Initialise progress sub‑task with the module count.  
2. Iterate `self.modules`:  
   a. Invoke `module.generate`.  
   b. Append result plus a double newline to `output`.  
   c. Log module completion (level 1) and raw output (level 2).  
   d. Increment progress.  
3. Remove the sub‑task and return the aggregated `output`.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `info` | `dict` | Input payload (e.g., `code_mix`, `full_data`, `language`) | Consumed by all modules |
| `model` | `Model` | LLM interface used by modules | Passed unchanged |
| `progress` | `BaseProgress` | UI progress controller | Must support the called methods |

--- 
<a name="factory-generate-doc"></a>
## `factory_generate_doc` – Extensible Module Pipeline  

1. Load current `output_doc.md` and `code_mix.txt`.  
2. Assemble `info` dict (`language`, `full_data`, `code_mix`).  
3. Log module list and input sizes.  
4. Call `doc_factory.generate_doc(info, self.sync_model, self.progress_bar)`.  
5. Prepend factory result to existing doc and rewrite `output_doc.md`.  
6. Update progress.  

**Visible Interaction:** Uses `DocFactory` and its registered modules (e.g., `IntroLinks`, `CustomModule`).

--- 
<a name="write-docs-by-parts"></a>
## `write_docs_by_parts` – Part‑wise Documentation Generation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | **Input** – raw code fragment to document. |
| `model` | `Model` | **Dependency** – LLM wrapper providing `get_answer_without_history`. |
| `project_settings` | `ProjectSettings` | Supplies deterministic system prompt via `prompt`. |
| `prev_info` | `str` | Optional – previous part’s generated doc (used for context). |
| `language` | `str` | Language selector for the system prompt (default `"en"`). |
| `global_info` | `str` | Optional – extra project‑wide relations injected into prompt. |
| **Return** | `str` | Final documentation for the supplied part (raw LLM response, trimmed of surrounding markdown fences). |

**Responsibility** – Build a three‑message prompt (project settings, compression hint, file content) and forward it to `model.get_answer_without_history`. The response is returned unchanged, except for removal of leading/trailing ``````` fences.

**Logic Flow**  
1. Initialise a singleton `BaseLogger` and log start.  
2. Construct `prompt` list:  
   - System message setting the target `language`.  
   - System message embedding `project_settings.prompt`.  
   - System message with constant `BASE_PART_COMPLITE_TEXT`.  
   - *(Conditional)* System message with `global_info` if provided.  
   - *(Conditional)* System message with `prev_info` prefixed by “it is last part of documentation that you have write before”.  
   - User message containing the actual `part` text.  
3. Call `model.get_answer_without_history(prompt=prompt)` and store in `answer`.  
4. Strip leading ``````` and trailing ``````` if present, logging the raw length and optionally the full answer at debug level.  
5. Return the cleaned `answer`.  

> **Assumption** – `BASE_PART_COMPLITE_TEXT` is defined elsewhere; its exact content does not affect this fragment’s behavior.  

The function performs no side effects beyond logging and the LLM call; it produces a deterministic output solely based on its inputs. 
<a name="generate-code-file"></a>
## `generate_code_file` – Repo‑Content Extraction  

1. Log start (level 1).  
2. Instantiate `CodeMix` with `project_directory` and `config.ignore_files`.  
3. Call `cm.build_repo_content` → writes `code_mix.txt`.  
4. Log completion and advance progress.  

**Side‑Effect:** Produces `code_mix.txt` in the cache.

--- 
<a name="generate-global-info"></a>
## `generate_global_info` – Single‑Chunk Compression  

1. Load `code_mix.txt`.  
2. Split via `split_data(..., max_symbols)`.  
3. Call `compress_to_one` with `sync_model`, project settings, and `compress_power`.  
4. Write result to `global_info.md`.  
5. Update progress.  

**Parameters:** `compress_power:int=4`, `max_symbols:int=10000`.

--- 
<a name="generate-doc-parts"></a>
## `generete_doc_parts` – Chunk‑Based Documentation  

1. Retrieve `code_mix.txt` (and optional `global_info.md`).  
2. Log start.  
3. Invoke `gen_doc_parts` with code, size limit (default 5 000), model, settings, language, progress, and optional `global_info`.  
4. Write combined output to `output_doc.md`.  
5. Log completion and update progress.  

**Outputs:** Full documentation split into LLM‑generated parts.

--- 
<a name="order-doc"></a>
## `order_doc` – Anchor‑Based Reordering  

1. Read `output_doc.md`.  
2. Split into anchor blocks via `split_text_by_anchors`.  
3. If split succeeds, request ordering from `get_order` (LLM call).  
4. Overwrite `output_doc.md` with ordered result.  

**Failure Path:** Returns early if no anchors are found.

--- 
<a name="autodocfile-settings"></a>
The configuration file is a YAML document that defines the behavior of the documentation generator. The top‑level sections and their available fields are:

- **project_name** – a string that sets the display name of the project.
- **language** – the language code (e.g., “en”) used for generated text.

- **ignore_files** – a list of patterns for files and directories that must be omitted during scanning. Common entries include build folders, Python caches, virtual‑environment directories, IDE settings, database files, log files, coverage reports, version‑control metadata, static assets, and markdown files.

- **build_settings** – controls the generation process:
  - **save_logs** – boolean, whether to keep the generation logs.
  - **log_level** – numeric level (e.g., 0‑3) indicating the verbosity of logs.

- **structure_settings** – influences how the final documentation is organized:
  - **include_intro_links** – boolean, adds navigation links to the introduction section.
  - **include_order** – boolean, preserves the order of processed files.
  - **use_global_file** – boolean, merges all content into a single global document.
  - **max_doc_part_size** – integer, maximum size (in characters) for each documentation chunk.

- **project_additional_info** – a mapping for extra project metadata; for example, a **global idea** field describing the project’s purpose.

- **custom_descriptions** – a list of free‑form strings that the generator will embed as custom explanatory sections. Each entry can contain instructions, usage tips, or any narrative you want to appear in the output.

When writing the file, follow proper YAML indentation (two spaces per level) and ensure each key is correctly spelled as shown above. The sections are optional; omit any that are not needed, and the generator will apply its defaults. 
<a name="config-reader-yaml-parsing"></a>
## ConfigReader – YAML Parsing & Settings Instantiation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `StructureSettings` | class | Holds boolean flags and size limit for the documentation pipeline. | Defaults: `include_intro_links=True`, `include_order=True`, `use_global_file=True`, `max_doc_part_size=5_000`. |
| `read_config` | function | Parses a YAML string, builds a `Config` object, a list of `CustomModule`/`CustomModuleWithOutContext`, and a populated `StructureSettings`. | Returns `tuple[Config, list[CustomModule], StructureSettings]`. |

**Logic Flow**  
1. `yaml.safe_load` converts `file_data` to a dict.  
2. Instantiates `Config()` and extracts `ignore_files`, `language`, `project_name`, `project_additional_info`.  
3. Loads `build_settings` into a fresh `ProjectBuildConfig` via `load_settings`.  
4. Chains setters on `config` to apply language, name, and the `pcs`.  
5. Populates ignore‑file patterns and additional project info via `add_ignore_file` / `add_project_additional_info`.  
6. Transforms each entry in `custom_descriptions` into a `CustomModule` (prefix “%” → `CustomModuleWithOutContext`).  
7. Loads optional `structure_settings` into a `StructureSettings` instance via `load_settings`.  

> **Assumption** – The `custom_descriptions` list contains strings where the first character indicates the module type; any other format is ignored. 
<a name="get-path"></a>
## `get_file_path` – Cache Path Builder  

Concatenates `project_directory`, `CACHE_FOLDER_NAME`, and the filename from `FILE_NAMES`. Returns the full path (`str`).

--- 
<a name="read-file"></a>
## `read_file_by_file_key` – Cached File Reader  

*Reads the content of a cached file identified by a key (`code_mix`, `global_info`, `output_doc`, `logs`).*  
- Builds absolute path via `self.get_file_path`.  
- Returns file text (`str`).  

**Data Contract** – Input: `file_key:str`; Output: file contents `str`.

--- 
<a name="cli-entrypoint"></a>
## CLI Entry Point  

The `if __name__ == "__main__"` block reads `autodocconfig.yml`, invokes `read_config`, then calls `gen_doc(".", config, custom_modules, structure_settings)`. The resulting markdown is stored in `output_doc` but not automatically written to disk within this fragment. 
<a name="manager-class-usage-and-methods"></a>
The Manager class is used to manage the generation of documentation. To use the Manager class, you need to create an instance of it by passing the project directory, config, and optional sync_model, async_model, and progress_bar. 

Here is an example of how to create a Manager instance:
```python
from .config.config import Config
from .engine.models.gpt_model import GPTModel
from .ui.progress_base import BaseProgress

config = Config()
sync_model = GPTModel()
progress_bar = BaseProgress()

manager = Manager("project_directory", config, sync_model, progress_bar=progress_bar)
```

The Manager class has several methods available:

1. `read_file_by_file_key(file_key: str)`: This method reads a file from the cache directory based on the file key.
```python
data = manager.read_file_by_file_key("code_mix")
```

2. `get_file_path(file_key: str)`: This method returns the file path for a given file key.
```python
file_path = manager.get_file_path("code_mix")
```

3. `generate_code_file()`: This method generates the code mix file.
```python
manager.generate_code_file()
```

4. `generate_global_info(compress_power: int = 4, max_symbols: int = 10000)`: This method generates the global info file.
```python
manager.generate_global_info(compress_power=4, max_symbols=10000)
```

5. `generete_doc_parts(max_symbols=5_000, with_global_file: bool = False)`: This method generates the documentation parts.
```python
manager.generete_doc_parts(max_symbols=5000, with_global_file=True)
```

6. `factory_generate_doc(doc_factory: DocFactory)`: This method generates the documentation using a doc factory.
```python
from .factory.base_factory import DocFactory
doc_factory = DocFactory()
manager.factory_generate_doc(doc_factory)
```

7. `order_doc()`: This method orders the documentation.
```python
manager.order_doc()
```

8. `clear_cache()`: This method clears the cache directory.
```python
manager.clear_cache()
``` 
<a name="manager-orchestrator"></a>
## `Manager` – Pipeline Orchestrator  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_directory` | `str` | Root of the target repo | Used to locate cache and files |
| `config` | `Config` | Global settings (ignore patterns, language, log level) | Accessed via `self.config` |
| `sync_model` / `async_model` | `Model` / `AsyncModel` | LLM interface supplied to all processing steps | May be `None` if not provided |
| `progress_bar` | `BaseProgress` | UI progress controller (default `BaseProgress()`) | Calls `update_task()` after each stage |
| `logger` | `BaseLogger` | File‑based logger | Writes INFO logs to `report.txt` |
| `CACHE_FOLDER_NAME` / `FILE_NAMES` | `str` / `dict` | Constant cache folder and file mapping | Stored in `.auto_doc_cache` |

**Responsibility** – Coordinates the end‑to‑end documentation flow: code mixing → global compression → chunked generation → optional factory extensions → ordering → cache maintenance.

**Visible Interactions** – Calls functions from `preprocessor`, `postprocessor`, and `factory` modules, passing the configured `Model` and `BaseProgress` instances; reads/writes cached files via `self.get_file_path()`.

---

<a name="init"></a>
## `__init__` – Instance Bootstrap  

1. Store `project_directory`, `config`, models, and `progress_bar`.  
2. Initialise `BaseLogger` with a `FileLoggerTemplate` targeting `logs`.  
3. Ensure cache folder `.<project>/.auto_doc_cache` exists (creates it if missing).  

> **Note:** No I/O beyond directory creation; all heavy work is deferred to other methods.

--- 
<a name="basemodule"></a>
## `BaseModule` – Abstract Documentation Piece  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `generate` | `abstractmethod` | Produce a markdown fragment | Receives `info: dict` and a `Model` instance |

**Responsibility** – Defines the contract each documentation‑generation plugin must satisfy.  

**Visible Interactions** – Sub‑classes are instantiated by `DocFactory` and called with the shared `info` payload and a concrete `Model`. No runtime logic is present here.  

> **Note** – Because it is abstract, the class itself contributes no output.

--- 
<a name="custommodule"></a>
## `CustomModule` – Context‑Aware Description Generator  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `discription` | `str` | Prompt snippet supplied by the caller | Stored on init |
| `generate` | `def` | Calls `generete_custom_discription` | Uses split code and language |

**Responsibility** – Generates a custom section by feeding a chunked code slice (≤ 5000 symbols) to the LLM with a user‑provided description.  

**Visible Interactions** – Calls `split_data(info["code_mix"], max_symbols=5000)` then `generete_custom_discription(..., model, self.discription, info["language"])`.  

**Logic Flow**  
1. Retrieve `code_mix` from `info`.  
2. Chunk it via `split_data`.  
3. Invoke the post‑processor helper with the chunk, `model`, description, and language.  
4. Return the helper’s string result.  

--- 
<a name="custommodulewithout"></a>
## `CustomModuleWithOutContext` – Stand‑Alone Description Generator  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `discription` | `str` | Prompt fragment | Set at construction |
| `generate` | `def` | Calls `generete_custom_discription_without` | No code context required |

**Responsibility** – Produces a description solely from the supplied text prompt, bypassing any code context.  

**Visible Interactions** – Directly invokes `generete_custom_discription_without(model, self.discription, info["language"])`.  

--- 
<a name="async-gptmodel-class"></a>
## `AsyncGPTModel` – Asynchronous LLM Wrapper  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `str` | Credential for Groq API | Defaults to module‑level `API_KEY` |
| `history` | `History` | Conversation buffer | Initialized via parent |
| `use_random` | `bool` | Shuffle model list flag | Defaults `True` |
| `client` | `AsyncGroq` | Async HTTP client | Created with `api_key` |
| `logger` | `BaseLogger` | Structured logging | Instantiated in ctor |
| `regen_models_name` | `list[str]` | Rotating model names | Shuffled copy of `MODELS_NAME` |
| `current_model_index` | `int` | Index of current model | Starts 0 |
| `generate_answer()` | `async def` | Sends a chat request, retries on failure | Returns generated `str` |

**Responsibility** – Provides an asynchronous interface to Groq’s LLMs, managing a rotating list of model names and logging each step.

**Visible Interactions** – Calls `self.client.chat.completions.create(messages=…, model=…)`; logs via `BaseLogger`; raises `ModelExhaustedException` if no models remain; updates `self.history` indirectly through parent methods (not shown here).

**Logic Flow**  
1. Log start of async generation.  
2. Choose `messages` from `self.history.history` or the supplied `prompt`.  
3. Loop:  
   a. If `regen_models_name` empty → log error & raise `ModelExhaustedException`.  
   b. Select `model_name` at `current_model_index`.  
   c. Attempt `await self.client.chat.completions.create`.  
   d. On exception → log warning, advance index (wrap to 0), retry.  
4. Extract `chat_completion.choices[0].message.content` as `result`.  
5. Log model used and answer (level 2).  
6. Return `result`.

> **Warning** – The `while True` loop will continue indefinitely until a model succeeds; if all models fail repeatedly, it may cause a long‑running task. 
<a name="gptmodel-class"></a>
## `GPTModel` – Synchronous LLM Wrapper  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `str` | Credential for Groq API | Defaults to `API_KEY` |
| `history` | `History` | Conversation buffer | Inherited |
| `client` | `Groq` | Sync HTTP client | Created with `api_key` |
| `logger` | `BaseLogger` | Structured logging | Instantiated in ctor |
| `regen_models_name` | `list[str]` | Rotating model names | Shuffled if `use_random` |
| `generate_answer()` | `def` | Sends a chat request, retries on failure | Returns generated `str` |

**Responsibility** – Mirrors `AsyncGPTModel` but provides a blocking API for Groq LLM calls.

**Visible Interactions** – Uses `self.client.chat.completions.create`; logs via `BaseLogger`; raises `ModelExhaustedException` when model list empty.

**Logic Flow**  
1. Log start of generation.  
2. Select `messages` from history or `prompt`.  
3. Loop identical to async version, but with synchronous `self.client.chat.completions.create`.  
4. On success, extract content, log model and answer, return the string.

Both classes inherit the **history‑management** and **model‑rotation** logic from `ParentModel` (defined in `model.py`). No other external behavior is assumed. 
<a name="code-mix-class"></a>
## `CodeMix` – Repository‑Content Packager  

Generates a plain‑text snapshot of a project's directory tree and file contents, respecting an ignore list.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `root_dir` | `str` / `Path` | Init argument | Base directory to scan. |
| `ignore_patterns` | `list[str]` | Init argument | Glob patterns for files/dirs to skip. |
| `logger` | `BaseLogger` | Member | Logs ignored paths (level 1). |
| `should_ignore` | `method` | Predicate | Returns `True` if a path matches any ignore pattern (directory name, basename, or any path part). |
| `build_repo_content` | `method` | Producer | Writes a structured listing and raw file bodies to `output_file`. |
| `output_file` | `str` | Argument to `build_repo_content` | Destination text file. |
| `ignore_list` | `list[str]` | Module constant | Default patterns (virtualenvs, caches, binaries, etc.). |

**`should_ignore` Logic** – Convert `path` to a relative string, then for each pattern check:  
1. Full relative match,  
2. Basename match,  
3. Any component match (`path.parts`).  

If any succeed, return `True`; otherwise `False`.  

**`build_repo_content` Logic** –  
1. Open `output_file` for UTF‑8 write.  
2. Write a “Repository Structure” header, then iterate sorted `root_dir.rglob("*")`.  
   * For each entry, if `should_ignore` is `True` → log and skip.  
   * Compute depth, prepend two spaces per level, and write directory names with trailing `/` or file names.  
3. Write a separator line (`"="*20`).  
4. Iterate again, this time handling only files not ignored:  
   * Write a `<file path="relative">` tag, then the raw file text (read with `errors="ignore"`), then two newlines.  
   * On read errors, write an error line.  

The class produces a single text artifact that downstream preprocessors (e.g., compressors, splitters) consume.  

---  

These components together enable **Auto Doc Generator** to locate meaningful anchors, order them semantically via LLM, and feed a full repository snapshot into the documentation pipeline. 
<a name="projectsettings-class"></a>
## `ProjectSettings` – Prompt Builder  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_name` | `str` | **Init argument** | Inserted into the system prompt. |
| `info` | `dict` | **Member** | Stores arbitrary key/value pairs added via `add_info`. |
| `prompt` | `property` | **Derived output** | Concatenates `BASE_SETTINGS_PROMPT`, project name, and each `info` entry, each terminated by a newline. |

**Responsibility** – Produce a deterministic system prompt for the LLM, enriched with project‑specific metadata.  

**Logic Flow**  
1. Start with `BASE_SETTINGS_PROMPT`.  
2. Append `Project Name:` line.  
3. Iterate over `self.info` and append `key: value` lines.  
4. Return the assembled string.  

--- 
<a name="projectsettings"></a>
## `ProjectSettings` – Prompt Builder  

| Entity | Type | Role |
|--------|------|------|
| `project_name` | `str` | Init argument. |
| `info` | `dict` | Stores key/value pairs via `add_info`. |
| `prompt` | `property` | Derived system prompt. |

**Responsibility** – Produce a deterministic LLM system prompt: start with `BASE_SETTINGS_PROMPT`, add “Project Name”, then each `info` entry, each on its own line.

--- 
<a name="pyproject-toml-config"></a>
## `pyproject.toml` – Project Metadata & Build Configuration  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `[project]` | table | Core PEP 621 metadata consumed by **Poetry** and **pip** during packaging. | Defines name, version, description, authors, license, readme, and Python version constraints. |
| `name` | `str` | Package identifier on PyPI. | `"autodocgenerator"` |
| `version` | `str` | Semantic version used for distribution tags. | `"0.9.2.8"` |
| `description` | `str` | Short human‑readable summary. | `"This Project helps you to create docs for your projects"` |
| `authors` | list[dict] | Maintainer contact information. | `{name: "dima-on", email: "sinica911@gmail.com"}` |
| `license` | dict | License declaration for downstream users. | `{text: "MIT"}` |
| `readme` | `str` | File rendered on PyPI project page. | `"README.md"` |
| `requires-python` | `str` | Minimum/maximum interpreter versions accepted. | `">=3.11,<4.0"` |
| `dependencies` | list[`str`] | Runtime packages required by **Auto Doc Generator**. | Includes `rich`, `groq`, `openai`, `pydantic`, etc. |
| `[build-system]` | table | Informs **PEP 517** build front‑end. | `requires = ["poetry-core>=2.0.0"]`, `backend = "poetry.core.masonry.api"` |

> **Critical assumption:** The file is processed by **Poetry** (as indicated by the `poetry-core` requirement). No other build back‑ends are present.

### Functional Responsibility  
This fragment supplies **all static package metadata** and **dependency declarations** required to produce distributable artefacts (wheel, sdist). It is the single source of truth for versioning, licensing, and the Python runtime envelope.

### Visible Interactions  
- **Poetry** reads `pyproject.toml` to resolve `dependencies`, generate a lock file, and invoke the specified `build-backend`.  
- **pip** (via PEP 517) invokes the backend (`poetry.core.masonry.api`) which consumes the same tables to create distribution archives.  
- CI pipelines (e.g., GitHub Actions) may `poetry install` or `poetry build` directly referencing this file.

### Data Flow Summary  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| Input | `pyproject.toml` file | Provides declarative configuration to the build system. | Parsed once per build. |
| Output | Distribution artefacts (`.whl`, `.tar.gz`) | Result of the build process, containing the source code and metadata. | Uploaded to PyPI or used locally. |
| Side‑effects | `poetry.lock` generation | Locks transitive dependencies to exact versions. | Not part of the source file but derived from it. |

*The module performs no runtime I/O beyond reading this file during packaging.* 
<a name="introlinks"></a>
## `IntroLinks` – Auto‑Generated Introductory Links  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `generate` | `def` | Extracts HTML anchors & builds an intro list | Uses `info["full_data"]` |

**Responsibility** – Gathers all HTML links from the full document and asks the LLM to craft an introductory link section.  

**Visible Interactions** – Calls `get_all_html_links(info["full_data"])` then `get_links_intro(links, model, info["language"])`.  

--- 
<a name="introtext"></a>
## `IntroText` – Introductory Narrative Generator  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `generate` | `def` | Produces a prose introduction from global data | Uses `info["global_data"]` |

**Responsibility** – Sends the repository‑wide summary to the LLM to obtain a human‑readable intro paragraph.  

**Visible Interactions** – Calls `get_introdaction(info["global_data"], model, info["language"])`. 
<a name="get-all-html-links"></a>
## `get_all_html_links` – HTML Anchor Extractor  

**Responsibility** – Scan a documentation string and return a list of markdown‑style anchors (`#anchor`).  

**Interactions** – Uses only the standard **`re`** module and the **`BaseLogger`** singleton for informational logs.  

**Logic Flow**  
1. Initialise `BaseLogger`.  
2. Log start of extraction.  
3. Compile pattern `r'<a name=["\']?(.*?)["\']?></a>'`.  
4. Iterate over all matches; keep anchors whose name length > 5, prefix with `#`.  
5. Log count and raw list, then return them.  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Input documentation | Must contain HTML anchors. |
| `links` | `list[str]` | Output | Each entry is `#anchor_name`. |
| Return | `list[str]` | – | Empty list if none found. |

> **Assumption:** Anchor names longer than five characters are considered meaningful; shorter ones are ignored. 
<a name="get-links-intro"></a>
## `get_links_intro` – Link‑Based Intro Generator  

Creates an introductory paragraph that references the supplied anchors via an LLM call.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `links` | `list[str]` | Input | Anchor list from `get_all_html_links`. |
| `model` | `Model` | Dependency | LLM wrapper providing `get_answer_without_history`. |
| `language` | `str` | Optional | Default `"en"`; injected into system prompt. |
| Return | `str` | Generated intro | May contain markdown links. |

**Logic** – Build a three‑message system/user prompt using `BASE_INTRODACTION_CREATE_LINKS`, log before/after the LLM call, and return the model’s answer. 
<a name="get-introdaction"></a>
## `get_introdaction` – Global Intro Builder  

Produces a high‑level introduction from the aggregated global data.  

| Entity | Type | Role |
|--------|------|------|
| `global_data` | `str` | Input text (e.g., compressed repo summary). |
| `model` | `Model` | LLM interface. |
| `language` | `str` | Optional language selector. |
| Return | `str` | Intro paragraph. |

**Logic** – Sends a prompt built from `BASE_INTRO_CREATE` and returns the model’s response. 
<a name="extract-links-from-start"></a>
## `extract_links_from_start` – Anchor Collector  

Scans a list of raw **chunks** and returns Markdown‑style links for anchors whose names exceed five characters.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `chunks` | `list[str]` | Input | Raw text blocks, each may start with an `<a name=…>` tag. |
| `links` | `list[str]` | Return | `"#"` + anchor name for each qualifying anchor. |
| `pattern` | `str` | Internal | `r'^<a name=["\']?(.*?)["\']?></a>'` – captures the anchor name at the very start of a chunk. |
| `anchor_name` | `str` | Local | Extracted name; kept only if `len(anchor_name) > 5`. |

> **Assumption** – Anchor names longer than five characters are considered meaningful; shorter ones are ignored.

**Logic** – Iterate `chunks`; `re.search` the pattern; if a match and length condition passes, prepend `#` and append to `links`; finally return the list.  

--- 
<a name="split-text-by-anchors"></a>
## `split_text_by_anchors` – Anchor‑Based Chunk Splitter  

Divides a full markdown document into discrete sections anchored by `<a name=…>` tags and builds a mapping from link to section content.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `text` | `str` | Input | Entire document string. |
| `pattern` | `str` | Internal | Positive look‑ahead `(?=<a name=["\']?[^"\'>\s]{6,200}["\']?></a>)` – finds anchors ≥ 6 chars. |
| `chunks` | `list[str]` | Intermediate | Result of `re.split`. |
| `result_chanks` | `list[str]` | Cleaned chunks | Stripped, non‑empty pieces. |
| `all_links` | `list[str]` | From `extract_links_from_start`. |
| `result` | `dict[str, str]` | Return | `{ "#anchor": "section text" }` or `None` on mismatch. |

**Logic** – Split `text` by the anchor look‑ahead, strip empties, extract links via `extract_links_from_start`. If the number of links differs from chunks, the function aborts (`None`). Otherwise, build a dict mapping each link to its corresponding chunk.  

--- 
<a name="get-order"></a>
## `get_order` – Semantic Title Sorter  

Calls the LLM to obtain a comma‑separated ordering of provided anchor titles and assembles the final ordered document.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | Dependency | Provides `get_answer_without_history`. |
| `chanks` | `dict[str, str]` | Input | Mapping `"#anchor"` → section text. |
| `logger` | `BaseLogger` | Local | Logs start, inputs, and each assembly step. |
| `prompt` | `list[dict]` | LLM request | Single *user* message with titles list. |
| `result` | `str` | LLM raw answer | Expected CSV of titles (including `#`). |
| `new_result` | `list[str]` | Parsed order | Trimmed titles. |
| `order_output` | `str` | Return | Concatenated sections in LLM‑specified order, each followed by a newline. |

**Logic** – Log start, build a user‑only prompt that asks the model to “Sort the following titles semantically … Return ONLY a comma‑separated list … leave # in title”. Invoke `model.get_answer_without_history`, split and trim the CSV, then iterate over the ordered titles, appending each corresponding chunk to `order_output` while logging each addition. Return the assembled markdown.  

--- 
<a name="clear-cache"></a>
## `clear_cache` – Log Cleanup  

If `config.pbc.save_logs` is falsy, deletes the `report.txt` log file from the cache.  

---  

**Overall Data Flow** – Each stage reads from the cache, processes via LLM helpers, writes back, and advances the `BaseProgress` UI, enabling a deterministic, repeatable documentation pipeline. 
<a name="generate-custom-description"></a>
## `generete_custom_discription` – Iterative Custom Description  

Generates a custom description for each chunk in `splited_data` until the model returns substantive content.  

| Entity | Type | Role |
|--------|------|------|
| `splited_data` | `iterable[str]` | Chunked source strings. |
| `model` | `Model` | LLM driver. |
| `custom_description` | `str` | Task description for the model. |
| `language` | `str` | Language selector (default `"en"`). |
| Return | `str` | First non‑empty description. |

**Logic** – For each chunk: assemble a prompt (system role, context, `BASE_CUSTOM_DISCRIPTIONS`, task), query the model, break on a result that does **not** contain `"!noinfo"` or `"No information found"` within the first 30 characters. 
<a name="generate-custom-description-without"></a>
## `generete_custom_discription_without` – Stand‑alone Description Builder  

Creates a description without source context, enforcing a strict anchor tag rule.  

| Entity | Type | Role |
|--------|------|------|
| `model` | `Model` | LLM interface. |
| `custom_description` | `str` | Desired description task. |
| `language` | `str` | Language selector. |
| Return | `str` | LLM‑generated text beginning with ` 
<a name="CONTENT_DESCRIPTION"></a>`. |

**Logic** – Sends a prompt that embeds detailed formatting constraints (no filenames, extensions, generic terms, or URLs) and returns the model’s answer.  

---  

**Overall Interaction** – All functions log via `BaseLogger`, rely on the shared `Model` abstraction, and produce plain‑text fragments consumed by downstream post‑processors (e.g., `IntroLinks` module). 
<a name="compress-function"></a>
## `compress` – Single‑File Text Compression  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | **Input** | Raw file content to be reduced. |
| `project_settings` | `ProjectSettings` | **Input** | Supplies system prompt via its `prompt` property. |
| `model` | `Model` | **Dependency** | LLM wrapper exposing `get_answer_without_history`. |
| `compress_power` | `int` | **Parameter** | Determines target compression ratio (used in prompt). |
| `prompt` | `list[dict]` | **LLM request** | Two *system* messages (project settings + compression hint) and one *user* message (the data). |
| `answer` | `str` | **Output** | Raw model response, returned unchanged. |

**Responsibility** – Build a three‑message prompt that tells the model the project context, how aggressively to compress (`compress_power`), and the text to shrink, then forward it to `model.get_answer_without_history`.  

**Interactions** – Calls `project_settings.prompt` (property) and `model.get_answer_without_history`. No file I/O occurs.  

**Logic Flow**  
1. Assemble `prompt`.  
2. Invoke the model.  
3. Return the model’s answer.  

--- 
<a name="compress-func"></a>
## `compress` – Single‑File LLM Compression  

| Entity | Type | Role |
|--------|------|------|
| `data` | `str` | Input – raw file text. |
| `project_settings` | `ProjectSettings` | Input – provides system prompt via `prompt`. |
| `model` | `Model` | Dependency – LLM wrapper. |
| `compress_power` | `int` | Parameter – controls aggressiveness. |
| 
<a name="compress-and-compare"></a>
## `compress_and_compare` – Batch Compression & Concatenation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | **Input** | Individual file texts. |
| `model` | `Model` | **Dependency** | Same as in `compress`. |
| `project_settings` | `ProjectSettings` | **Input** | Passed to each `compress` call. |
| `compress_power` | `int` | **Parameter** | Max files per aggregated chunk (default 4). |
| `progress_bar` | `BaseProgress` | **Local** | Reports sub‑task progress. |
| `compress_and_compare_data` | `list[str]` | **Output** | List whose length = ⌈len(data)/compress_power⌉, each entry = concatenated compressed results. |

**Responsibility** – Compress groups of *compress_power* files, appending a newline after each file’s compressed text, while updating a progress bar.  

**Logic Flow**  
1. Initialise output list sized for required groups.  
2. `progress_bar.create_new_subtask` for the whole file set.  
3. Iterate `enumerate(data)`:  
   • Compute `curr_index = i // compress_power`.  
   • Call `compress` on the file text and append result + “\n” to the group entry.  
   • `progress_bar.update_task()`.  
4. Remove sub‑task and return the aggregated list.  

> **Note:** No error handling for `compress` failures is present; any exception propagates.

--- 
<a name="compress-compare"></a>
## `compress_and_compare` – Batched Compression  

| Entity | Type | Role |
|--------|------|------|
| `data` | `list[str]` | Input – file texts. |
| `compress_power` | `int` | Parameter – max files per batch (default 4). |
| `progress_bar` | `BaseProgress` | Local – shows sub‑task progress. |
| **Return** | `list[str]` | Aggregated compressed batches. |

**Responsibility** – Compress groups of `compress_power` files, concatenate each batch with newline separators, and update a progress bar.  

**Logic** – Create output list → start sub‑task → loop `enumerate(data)`: compute batch index, `compress` each element, append “\n”, update bar → finish sub‑task → return list.

--- 
<a name="compress-to-one"></a>
## `compress_to_one` – Iterative Consolidation  

| Entity | Type | Role |
|--------|------|------|
| `data` | `list[str]` | Input – result of `compress_and_compare`. |
| `compress_power` | `int` | Parameter – initial batch size (default 4). |
| **Return** | `str` | Fully compressed single string. |

**Responsibility** – Re‑apply `compress_and_compare` until only one chunk remains, lowering batch size to 2 when the list becomes small.  

**Logic** – While `len(data) > 1`: set `new_compress_power` (2 if list < `compress_power+1`), replace `data` with new batch result, repeat; finally return `data[0]`.

--- 
<a name="baseprogress-abstract"></a>
## `BaseProgress` Abstract Class  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseProgress` | class | Minimal progress‑tracking interface used by the UI layer. | Provides three abstract methods: `create_new_subtask`, `update_task`, `remove_subtask`. No internal state. |
| `create_new_subtask(name: str, total_len: int)` | method | Declare a sub‑task with a descriptive name and total work units. | Implemented by concrete subclasses. |
| `update_task()` | method | Advance the current task (sub‑task if present, otherwise the base task). | Concrete implementation decides how progress is rendered. |
| `remove_subtask()` | method | Clean up the current sub‑task reference. | No side‑effects beyond state reset. |

> **Assumption**: `BaseProgress` is never instantiated directly; it exists solely as a contract for derived progress reporters.

--- 
<a name="libprogress-concrete"></a>
## `LibProgress` – Rich‑Based Progress Reporter  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `LibProgress` | class (subclass of `BaseProgress`) | Wraps **rich.progress.Progress** to display a visual progress bar in the terminal. | Accepts a `Progress` instance and optional total number of high‑level steps (`total`). |
| `self.progress` | `Progress` | Rich progress manager handling rendering. | Created outside and injected. |
| `self._base_task` | task ID (int) | Represents the overall pipeline progress. | Initialized with label “General progress”. |
| `self._cur_sub_task` | task ID or `None` | Tracks the currently active sub‑task, if any. | Set by `create_new_subtask`. |
| `create_new_subtask(name, total_len)` | method | Registers a new sub‑task under the Rich manager. | Stores its task ID in `_cur_sub_task`. |
| `update_task()` | method | Advances either the sub‑task or the base task by one unit. | Calls `self.progress.update(...)` with `advance=1`. |
| `remove_subtask()` | method | Clears the sub‑task reference, allowing the base task to resume. | No Rich call; merely resets `_cur_sub_task`. |

--- 
<a name="consoletask-helper"></a>
## `ConsoleTask` – Simple Console Progress Helper  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `ConsoleTask` | class | Provides lightweight, stdout‑based progress feedback when Rich is unavailable. | Emits start message and incremental percentage updates. |
| `self.name` | `str` | Human‑readable identifier of the task. | |
| `self.total_len` | `int` | Total number of steps expected. | |
| `self.current_len` | `int` | Counter incremented on each `progress()` call. | |
| `start_task()` | method | Prints initial “Starting task” line and resets `current_len`. | Called from `__init__`. |
| `progress()` | method | Increments `current_len`, computes percent, and prints a status line. | Uses formatted string with one decimal place. |

--- 
<a name="consolegithubprogress-implementation"></a>
## `ConsoleGtiHubProgress` – Console‑Only `BaseProgress` Implementation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `ConsoleGtiHubProgress` | class (subclass of `BaseProgress`) | Implements the `BaseProgress` contract using `ConsoleTask` for both general and sub‑task reporting. | Suitable for environments without Rich (e.g., GitHub Actions logs). |
| `self.curr_task` | `ConsoleTask` or `None` | Holds the active sub‑task. | Set by `create_new_subtask`. |
| `self.gen_task` | `ConsoleTask` | Represents the always‑present “General Progress” task (4 steps by default). | Initialized in `__init__`. |
| `create_new_subtask(name: str, total_len: int)` | method | Instantiates a new `ConsoleTask` for the sub‑task. | Replaces any existing `curr_task`. |
| `update_task()` | method | Calls `progress()` on `curr_task` if it exists; otherwise updates `gen_task`. | Mirrors the conditional logic of `LibProgress`. |
| `remove_subtask()` | method | Clears the sub‑task reference, causing subsequent updates to affect the general task. | No output beyond state change. |

---

### Data Contract Summary  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `progress` (parameter to `LibProgress.__init__`) | `Progress` | External Rich progress manager. | Must be alive for the lifetime of `LibProgress`. |
| `total` (optional) | `int` | Number of high‑level steps in the overall workflow. | Default `4` matches the typical pipeline stage count. |
| `name` (to `create_new_subtask`) | `str` | Human‑readable sub‑task label. | Used only for display. |
| `total_len` (to `create_new_subtask`) | `int` | Expected work units for the sub‑task. | Determines progress bar length. |

---

**Logging & Side Effects**  
- No logging calls are present in this module; progress updates are emitted directly to the console (Rich or `print`).  
- The module performs **no I/O** beyond stdout rendering.  

---  

*This documentation isolates the progress‑handling component of **Auto Doc Generator**, enabling developers to understand how UI progress is reported in both Rich‑enabled and plain‑console environments.* 
<a name="spliter-partial"></a>
## `split_data` (partial) – Size‑Based Chunking  

| Entity | Type | Role |
|--------|------|------|
| `data` | `str` | Input – repository snapshot. |
| `max_symbols` | `int` | Parameter – desired max chunk size (unused in fragment). |
| `split_objects` | `list` | Local – intended container for chunks. |

**Responsibility** – Intended to split a large text into pieces respecting `max_symbols`. The shown fragment only initializes the list and splits on the sentinel ` 
