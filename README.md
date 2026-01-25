## Executive Navigation Tree
- 📦 **Installation**
  - [install_workflow'](#install_workflow')
  - [install-scripts](#install-scripts)
- 🛠️ **Manager**
  - [Using_Manager_Class](#Using_Manager_Class)
  - [manager-overview](#manager-overview)
  - [manager‑init](#manager‑init)
  - [manager‑helpers](#manager‑helpers)
  - [manager‑code‑mix](#manager‑code‑mix)
  - [manager‑global‑info](#manager‑global‑info)
  - [manager‑doc‑parts](#manager‑doc‑parts)
  - [manager‑factory‑doc](#manager‑factory‑doc)
  - [manager‑cleanup](#manager‑cleanup)
- 📦 **Modules**
  - [module‑initialisation](#module‑initialisation)
  - [config_reader](#config_reader)
  - [run_file](#run_file)
  - [base-module](#base-module)
  - [custom-module](#custom-module)
  - [intro-modules](#intro-modules)
- 📂 **Code Mix**
  - [code‑mix‑overview](#code‑mix‑overview)
  - [code‑mix‑api](#code‑mix‑api)
  - [code‑mix‑interaction](#code‑mix‑interaction)
- 🗜️ **Compressor**
  - [compressor‑overview](#compressor‑overview)
- ⚙️ **Core Functions**
  - [core‑functions](#core‑functions)
  - [doc‑factory](#doc-factory)
- 🤖 **Interaction Model**
  - [interaction‑model](#interaction‑model)
  - [parent-model](#parent-model)
  - [sync-model](#sync-model)
  - [async-model](#async-model)
  - [gptmodel](#gptmodel)
  - [asyncgptmodel](#asyncgptmodel)
- 📈 **Execution Parts**
  - [sync-part-doc-generation](#sync-part-doc-generation)
  - [async-part-doc-generation](#async-part-doc-generation)
- 📊 **Orchestration**
  - [orchestration](#orchestration)
- 📜 **Logging & Progress**
  - [logging](#logging)
  - [progress](#progress)
- 📚 **Postprocess**
  - [postprocess-overview](#postprocess-overview)
- 📜 **Assumptions & Limits**
  - [assumptions‑limits](#assumptions‑limits)
- 📜 **History**
  - [history](#history)
- ❗ **Exceptions**
  - [model-exhausted-exception](#model-exhausted-exception)

 

<a name='install_workflow'> </a>
explain how install workflow with install.ps1 and install.sh scripts for install you should use links irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex for powershell and curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash for linux based systems and also you have to add secret variable to git hub action GROCK_API_KEY with your api key from grock docs https://grockdocs.com to make it work

<a name='Using_Manager_Class'></a>
**Parameters required by `Manager`**

- `project_path` – path to the project (e.g., `"."`).
- `project_settings` – an instance of `ProjectSettings`.
- `pcs` – an instance of `ProjectConfigSettings`.
- `sync_model` – an instance of `GPTModel`.
- `async_model` – an instance of `AsyncGPTModel`.
- `ignore_files` – list of file names to ignore (`list[str]`).
- `progress_bar` – an instance of a progress UI, e.g., `ConsoleGtiHubProgress()`.
- `language` – language code string, e.g., `"en"`.

**Full example of usage (taken from the provided context)**

```python
from autodocgenerator.manage import Manager
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.preprocessor.settings import ProjectSettings
from autodocgenerator.factory.base_factory import DocFactory
from .config_reader import Config, read_config, ProjectConfigSettings
from autodocgenerator.engine.config.config import API_KEY

# Load configuration
with open("autodocconfig.yml", "r", encoding="utf-8") as file:
    config_data = file.read()
config: Config = read_config(config_data)

# Extract needed objects from config
project_settings = config.get_project_settings()
doc_factory, intro_factory = config.get_doc_factory()

# Prepare GPT models
sync_model = GPTModel(API_KEY, use_random=False)
async_model = AsyncGPTModel(API_KEY)

# Other arguments
project_path = "."                     # current directory
pcs: ProjectConfigSettings = config.pcs
ignore_list = config.ignore_files
progress = ConsoleGtiHubProgress()
language = "en"

# Create the Manager instance
manager = Manager(
    project_path,
    project_settings,
    pcs,
    sync_model=sync_model,
    async_model=async_model,
    ignore_files=ignore_list,
    progress_bar=progress,
    language=language,
)

# Example operations using the manager
manager.generate_code_file()
manager.generate_global_info_file(use_async=False, max_symbols=8000)
manager.generete_doc_parts(use_async=False, max_symbols=5000)
manager.factory_generate_doc(doc_factory)
manager.factory_generate_doc(intro_factory)
manager.clear_cache()
output_doc = manager.read_file_by_file_key("output_doc")
```

<a name='how_to_write_autodocconfig.yml'> </a>

The **autodocconfig.yml** file is a YAML document that defines the configuration for the Auto Doc Generator.  
Based on the provided context, the following top‑level keys are recognized:

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `project_name` | string | Name of the project that will appear in the generated documentation. | `project_name: "Auto Doc Generator"` |
| `language` | string | Language code for the documentation (default **en**). | `language: "en"` |
| `project_settings` | mapping | Settings that affect the documentation generation process. | <pre>project_settings:<br>  save_logs: true<br>  log_level: 2</pre> |
| `project_additional_info` | mapping | Arbitrary key‑value pairs that are added to the project information section. | <pre>project_additional_info:<br>  global idea: "This project was created to help developers make documentations for them projects"</pre> |
| `ignore_files` | list of strings *(optional)* | Glob patterns for files/folders that should be ignored during scanning. If omitted the default list from `Config` is used. | <pre>ignore_files:<br>  - "*.md"<br>  - "tests/**"</pre> |
| `custom_descriptions` | list of strings | Custom textual descriptions that will be turned into modules by the generator. Each entry is processed as a `CustomModule`. | <pre>custom_descriptions:<br>  - "explain how install workflow…"<br>  - "how to use Manager class…"<br>  - "explain how to write autodocconfig.yml file…"</pre> |

**Typical structure**

```yaml
project_name: "My Project"
language: "en"

project_settings:
  save_logs: true
  log_level: 2

project_additional_info:
  description: "Short description of the project"
  author: "Your Name"

ignore_files:
  - "*.md"
  - "docs/**"

custom_descriptions:
  - "First custom description"
  - "Second custom description"
```

 

<a name="module‑initialisation"></a>
## 📦 autodocgenerator package initialisation  

The ``autodocgenerator/__init__.py`` file is executed on every import of the **ADG** library.  
Its sole responsibilities are:

1. **Signal successful import** – the ``print("ADG")`` statement writes a short banner to *stdout* (useful during debugging or when the package is invoked as a script).  
2. **Expose a ready‑to‑use logger** – it imports the concrete logging classes from ``autodocgenerator.ui.logging`` and creates a module‑level ``logger`` instance:
   ```python
   logger = BaseLogger()
   logger.set_logger(BaseLoggerTemplate())
   ```
   This singleton is shared across the entire code‑base, so any sub‑module can simply ``from autodocgenerator import logger`` and emit ``InfoLog``, ``WarningLog`` or ``ErrorLog`` messages without configuring a logger themselves.

### Interaction with the rest of the system
- **UI → Engine → Factory** components all import ``logger`` to report progress, configuration problems, or fatal errors.  
- The logger respects the global settings defined in ``autodocconfig.yml`` (e.g., ``save_logs`` and ``log_level``) because ``BaseLoggerTemplate`` reads those values during its own initialisation.

### Assumptions & side‑effects
- The environment must have the ``autodocgenerator.ui.logging`` module available; otherwise an ``ImportError`` aborts package loading.  
- The ``print`` side‑effect writes to standard output every time the package is imported – in production pipelines this can be silenced by redirecting stdout or by removing the line.

Overall, this file provides a tiny but essential bootstrap: a consistent logger and a visual cue that the **Auto Doc Generator** library has been loaded.

<a name="config_reader"></a>
## `autodocgenerator.auto_runner.config_reader` – Configuration Bootstrap  

This module translates *autodocconfig.yml* into runtime objects used throughout the generator.  

* **`ProjectConfigSettings`** – holds global logger flags (`save_logs`, `log_level`). `load_settings()` copies any YAML keys into the instance via `setattr`.  
* **`Config`** – central holder for:
  * `ignore_files` – default file‑patterns excluded from scanning.  
  * `language`, `project_name`, `project_additional_info`.  
  * `custom_modules` – list of `CustomModule` objects supplied by the user.  
  * `pcs` – an attached `ProjectConfigSettings`.  
  It supplies fluent setters (`set_language`, `add_ignore_file`, …) and two factories:  
  * `get_project_settings()` → builds a `ProjectSettings` object populated with extra info.  
  * `get_doc_factory()` → creates the main `DocFactory` (with custom modules) and an *intro* factory (`IntroLinks`, optionally `IntroText`).  

* **`read_config(file_data: str) -> Config`** – parses the YAML, fills a `Config` instance, and returns it.  
  * Reads `ignore_files`, `language`, `project_name`, `project_additional_info`, `project_settings`, and `custom_descriptions`.  
  * Instantiates `CustomModule` for each user‑provided description.  

**Interaction** – All higher‑level components (`run_file`, `Manager`, factories) import `Config` to obtain:
* the ignore list passed to `Manager`,
* the `ProjectSettings` for metadata,
* the prepared `DocFactory` objects, and
* the logger configuration (`pcs`).  

**Assumptions / Side‑effects**  
* The YAML file is syntactically correct; otherwise `yaml.safe_load` raises.  
* `CustomModule` accepts a raw description dict.  
* No I/O is performed here – the caller must read the file (as `run_file` does).

---

<a name="run_file"></a>
## `autodocgenerator.auto_runner.run_file` – Execution Entrypoint  

`run_file.py` glues the configuration, AI models, and generation pipeline together.

* **`gen_doc(...) -> str`**  
  * Instantiates `GPTModel` (sync) and `AsyncGPTModel` (async) using the global `API_KEY`.  
  * Builds a `Manager` with project path, `ProjectSettings`, `ProjectConfigSettings`, the models, ignore list, a `ConsoleGtiHubProgress` bar, and language.  
  * Calls the manager’s stages in order:
    1. `generate_code_file` – extracts source code snippets.  
    2. `generate_global_info_file` – creates a high‑level overview (max 8 000 symbols).  
    3. `generete_doc_parts` – produces modular doc chunks (max 5 000 symbols).  
    4. `factory_generate_doc` – runs both the main and intro `DocFactory` objects.  
    5. `clear_cache` – removes temporary artefacts.  
  * Returns the assembled documentation via `manager.read_file_by_file_key("output_doc")`.

* **`__main__` block** – reads *autodocconfig.yml*, builds a `Config` via `read_config`, extracts `ProjectSettings` and factories, then calls `gen_doc` and stores the result in `output_doc`.

**Interaction** –  
* Relies on `Config` (above) for all runtime parameters.  
* Uses the singleton `logger` from `autodocgenerator.ui.logging` (imported but not explicitly called here; internal `Manager` and factories emit logs).  
* Progress is visualised through `ConsoleGtiHubProgress`, a subclass of `BaseProgress`.

**Assumptions** –  
* `API_KEY` is defined in `engine.config.config`.  
* Required packages (`rich`, `yaml`, GPT model wrappers) are installed.  
* The current working directory is the project root (passed as `"."`).  

Together, these two files form the bootstrap that reads user configuration, prepares AI back‑ends, and drives the full documentation generation pipeline.

<a name="config_prompts_and_constants"></a>
## `autodocgenerator.engine.config.config` – Prompt Templates & Global Settings  

**Responsibility**  
This module centralises all static prompt texts and runtime constants used by the AutoDoc generation pipeline. The strings (`BASE_SYSTEM_TEXT`, `BASE_PART_COMPLITE_TEXT`, `BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`, `BASE_SETTINGS_PROMPT`) are injected into LLM calls to steer behaviour (e.g., step‑by‑step code analysis, documentation scaffolding, navigation‑tree creation).  

**Key Elements**  

| Symbol | Type | Purpose |
|--------|------|---------|
| `BASE_SYSTEM_TEXT` | `str` | System‑level instruction for incremental code‑snippet analysis. |
| `BASE_PART_COMPLITE_TEXT` | `str` | Template for the “write documentation” stage. |
| `BASE_INTRODACTION_CREATE_TEXT` | `str` | Prompt that generates an executive navigation tree from Markdown links. |
| `BASE_INTRO_CREATE` | `str` | Prompt for a full project overview (title, goal, core logic, etc.). |
| `BASE_SETTINGS_PROMPT` | `str` | Prompt that establishes a persistent project knowledge base for later interactions. |
| `get_BASE_COMPRESS_TEXT(start, power)` | `Callable[[int, int], str]` | Factory that builds a compression‑task prompt, scaling the allowed summary length (`~start/power` chars) and embedding a strict usage‑example skeleton. |
| `API_KEY` | `str` | Obtained from environment (`.env`) – required by the GPT model wrappers. |
| `MODELS_NAME` | `list[str]` | Default model identifiers the system can select from. |

**Interaction with the System**  
* **LLM factories / managers** import these constants to build prompts for `GPTModel`, `AsyncGPTModel`, and the various `DocFactory` objects.  
* **`read_config`** (in the configuration loader) does **not** use them directly, but the generated `Config` object later supplies them to the pipeline via `Manager`.  
* **`run_file`** pulls `API_KEY` and `MODELS_NAME` to instantiate model wrappers before constructing the `Manager`.  

**Assumptions & Side‑effects**  
* The `.env` file is present and defines `API_KEY`; otherwise an exception aborts start‑up.  
* Prompt strings are treated as raw literals – no runtime formatting occurs here.  
* `get_BASE_COMPRESS_TEXT` only returns a formatted string; it does not perform any I/O.  

**Typical Usage Example**  

```python
from autodocgenerator.engine.config.config import (
    BASE_SYSTEM_TEXT,
    get_BASE_COMPRESS_TEXT,
    API_KEY,
    MODELS_NAME,
)

# Build a compression prompt for a 5000‑char snippet, aiming for ~500‑char summary
compress_prompt = get_BASE_COMPRESS_TEXT(start=5000, power=10)

# Pass prompts to the LLM wrapper (pseudo‑code)
gpt = GPTModel(api_key=API_KEY, model_name=MODELS_NAME[0])
response = gpt.complete(system=BASE_SYSTEM_TEXT, user=compress_prompt)
```

**<a name="model-exhausted-exception"></a>ModelExhaustedException**  
`ModelExhaustedException` is a custom sentinel raised when the runtime‑selected list of model identifiers (`regen_models_name`) becomes empty. It propagates up to the calling factory or UI layer, signalling that no fallback LLM is available and that request processing must abort.

---

**<a name="history"></a>History**  
A lightweight container for the conversation payload sent to Groq.  
* **Constructor** `History(system_prompt: str = BASE_SYSTEM_TEXT)` – starts with an empty list and optionally injects the system prompt.  
* **add_to_history(role, content)** – appends a dict `{"role": role, "content": content}`.  
* **Interaction**: Instances are shared with `Model`/`AsyncModel` so every generated answer can be stored and later reused when `with_history=True`.

---

**<a name="parent-model"></a>ParentModel**  
Base class that prepares common state for concrete model wrappers.  
* Stores the API key, a `History` object, and an index (`current_model_index`).  
* Copies the global `MODELS_NAME` list, shuffles it when `use_random=True`, and exposes the ordered list as `regen_models_name`.  
* **Assumption**: `MODELS_NAME` contains at least one valid Groq model identifier; otherwise `ModelExhaustedException` will be raised later.

---

**<a name="sync-model"></a>Model (synchronous)**  
Derives from `ParentModel` and implements the high‑level public API used by the rest of the system.  
* `generate_answer(with_history=True, prompt=None) → str` – abstract placeholder overridden by `GPTModel`.  
* `get_answer_without_history(prompt)` – convenience wrapper that forwards a raw message list directly to `generate_answer`.  
* `get_answer(prompt)` – records the user message, calls `generate_answer` (which uses history by default), stores the assistant reply, and returns it.  
* **Side‑effects**: Mutates `self.history` by appending user and assistant entries.

---

**<a name="async-model"></a>AsyncModel (asynchronous)**  
Mirrors `Model` but with `async` signatures, enabling non‑blocking UI or batch pipelines.  
* Same three public helpers (`generate_answer`, `get_answer_without_history`, `get_answer`) but all `await`able.  
* History handling is identical to the sync version.

---

**<a name="gptmodel"></a>GPTModel** – concrete synchronous wrapper around Groq’s SDK.  
* Instantiates `self.client = Groq(api_key=self.api_key)` and a `BaseLogger`.  
* **generate_answer**  
  1. Logs start.  
  2. Picks `messages` from `self.history` or the supplied `prompt`.  
  3. Loops over `regen_models_name` trying each model until a successful `chat.completions.create` call returns.  
  4. On failure logs a warning, advances `current_model_index`, and retries; if the list empties, raises `ModelExhaustedException`.  
  5. Extracts `result = chat_completion.choices[0].message.content`, logs it, and returns the string.  
* **Inputs**: `with_history` flag, optional raw `prompt`.  
* **Outputs**: generated answer string.  
* **Side‑effects**: logging, possible index mutation, no direct history mutation (handled by `Model.get_answer`).

---

**<a name="asyncgptmodel"></a>AsyncGPTModel** – asynchronous counterpart of `GPTModel`.  
* Uses `AsyncGroq` client and the same logging strategy.  
* The `generate_answer` coroutine follows the identical retry logic, awaiting `self.client.chat.completions.create`.  
* Returns the answer string once the awaitable completes.  

---

**Interaction Overview**  
1. **Factory / UI** creates a `GPTModel` or `AsyncGPTModel`, passing the global `API_KEY` and optionally a custom `History`.  
2. Callers invoke `get_answer` / `get_answer_without_history`.  
3. The wrapper builds the message payload, selects a model (randomised order), contacts Groq, logs each step, and returns the assistant response.  
4. If every candidate model fails, `ModelExhaustedException` bubbles up for graceful error handling.  

**<a name="base-module"></a>BaseModule (abstract)**  
Defines the contract for all documentation‑generation plug‑ins.  
* **Responsibility** – Provide a `generate(info, model)` method that receives a parsed source‑code dictionary (`info`) and a concrete `Model` (sync or async) to query LLMs.  
* **Interaction** – Sub‑classes are instantiated by `DocFactory` and called sequentially. No side effects beyond returning a string fragment.

**<a name="doc-factory"></a>DocFactory**  
Orchestrates module execution and aggregates results.  
* **Constructor** – Accepts any number of `BaseModule` instances; stores them in `self.modules`.  
* **generate_doc(info, model, progress)** –  
  1. Creates a sub‑task in the supplied `BaseProgress` UI component.  
  2. Iterates over `self.modules`, invoking `module.generate(info, model)`.  
  3. Concatenates each fragment (`module_result`) with double new‑lines.  
  4. Logs success and raw output via `BaseLogger`.  
  5. Updates progress after each module and finally removes the sub‑task.  
* **Outputs** – The full assembled documentation string.  
* **Side effects** – UI progress updates, structured logging, no mutation of `info` or `model`.

**<a name="custom-module"></a>CustomModule (general‑purpose)**  
* **Purpose** – Produce a user‑defined description block.  
* **Inputs** – `info["code_mix"]` (mixed source code), `info["language"]`, and the constructor‑provided `discription` text.  
* **Logic** – Splits the code into ≤ 7 000‑symbol chunks (`split_data`), then calls `generete_custom_discription` with the chunks, the LLM `model`, the custom description, and the target language. Returns the resulting markdown/HTML fragment.

**<a name="intro-modules"></a>IntroLinks & IntroText**  
* **IntroLinks** – Extracts every HTML anchor from `info["full_data"]` (`get_all_html_links`), prints the list (debug), and asks the LLM (`get_links_intro`) to compose a brief “quick‑links” section in the desired language.  
* **IntroText** – Requests a high‑level introduction for the project (`get_introdaction`) based on `info["global_data"]` and the language.  
Both modules return plain strings that are later stitched by `DocFactory`.

**<a name="manager-overview"></a>Manager – Orchestrator of the documentation pipeline**  
The `Manager` class is the central coordinator that ties together all preprocessing, LLM‑driven generation, post‑processing and UI‑feedback components of **AutoDocGenerator**. It receives a project path and configuration objects, prepares a cache directory, and exposes high‑level actions that are called by the CLI / UI.

---

### <a name="manager‑init"></a>Construction & state  
```python
def __init__(self,
             project_directory: str,
             project_settings: ProjectSettings,
             pcs: ProjectConfigSettings,
             sync_model: Model = None,
             async_model: AsyncModel = None,
             ignore_files: list = [],
             language: str = "en",
             progress_bar: BaseProgress = BaseProgress())
```
* **Inputs** – paths, settings, optional synchronous/asynchronous LLM wrappers, file‑ignore list, UI progress object.  
* **Side‑effects** – creates `<project>/ .auto_doc_cache` if missing and configures a file logger (`FileLoggerTemplate`) that writes to `report.log`.  
* **Assumptions** – at least one of `sync_model`/`async_model` is supplied; `pcs.log_level` is a valid `logging` level.

---

### <a name="manager‑helpers"></a>Helper utilities  
* `read_file_by_file_key(file_key)` – opens a cached file (code mix, global info, output, logs) and returns its text.  
* `get_file_path(file_key)` – builds an absolute path inside the cache folder using `FILE_NAMES`.  

Both helpers are used by every public method, ensuring a single source of truth for cache locations.

---

### <a name="manager‑code‑mix"></a>`generate_code_file` – building the raw source snapshot  
1. Logs start/end via `BaseLogger`.  
2. Instantiates `CodeMix(project_directory, ignore_files)`.  
3. Calls `CodeMix.build_repo_content(target_path)` which walks the repository, concatenates source files (respecting `ignore_files`) and writes the result to `code_mix.txt`.  
4. Updates the UI progress bar.

*Outputs*: a plain‑text “code mix” file used by later stages.

---

### <a name="manager‑global‑info"></a>`generate_global_info_file` – placeholder for project‑wide summary  
*Current implementation* reads the previously generated code mix, then writes a stub (`"ss"`) to `global_info.md`.  
*Intended flow* (commented out) would:
1. Split the code mix (`split_data`) into ≤ `max_symbols` chunks.  
2. Choose `sync_model` or `async_model`.  
3. Call `compress_to_one` to let the LLM synthesize a high‑level description of the whole project.  

The method also advances the progress bar.

---

### <a name="manager‑doc‑parts"></a>`generete_doc_parts` – chunk‑wise documentation creation  
* Reads `global_info` and the full code mix.  
* Depending on `use_async`, runs either `async_gen_doc_parts` (via `asyncio.run`) or `gen_doc_parts`. Both functions:
  * Split the source into ≤ `max_symbols` pieces.  
  * Prompt the LLM (sync or async) to produce module‑level docs.  
  * Return a concatenated markdown string.  
* Writes the result to `output_doc.md` and updates the progress UI.

*Outputs*: a first‑pass documentation file containing generated sections for every code chunk.

---

### <a name="manager‑factory‑doc"></a>`factory_generate_doc` – post‑processing with a `DocFactory`  
1. Loads `global_info`, the current `output_doc`, and the original `code_mix`.  
2. Packages them into an `info` dict (`language`, `global_data`, `full_data`, `code_mix`).  
3. Logs a detailed start message, listing the concrete module classes contained in the supplied `DocFactory`.  
4. Calls `doc_factory.generate_doc(info, self.sync_model, self.progress_bar)`.  
   * The factory runs a configurable pipeline of modules (e.g., `IntroLinks`, `IntroText`, `CustomModule`) that may add introductions, quick‑link sections, or custom markdown.  
5. Prepends the factory output to the existing documentation and rewrites `output_doc.md`.  
6. Updates the progress bar.

*Side‑effects*: modifies the final doc file and produces additional log entries.

---

### <a name="manager‑cleanup"></a>`clear_cache` – optional log cleanup  
If `pcs.save_logs` is `False`, removes `report.log` from the cache folder. No other files are touched.

---

### <a name="manager‑interaction‑summary"></a>Interaction diagram (textual)  

```
[CLI/UI] → Manager
    │
    ├─> CodeMix (preprocessor) → code_mix.txt
    ├─> split_data / compress_to_one (preprocessor) → global_info.md
    ├─> gen_doc_parts / async_gen_doc_parts (preprocessor) → output_doc.md
    ├─> DocFactory (factory) → IntroLinks, IntroText, CustomModule → enrich output_doc.md
    └─> BaseLogger / BaseProgress → console & file logs
```

All heavy LLM calls are delegated to the `Model`/`AsyncModel` objects; the manager merely forwards them and handles I/O, logging and progress reporting.

---  

*This documentation covers the `Manager` component only; other modules (spliter, compressor, postprocess, UI) are described elsewhere.*

### <a name="code‑mix‑overview"></a>CodeMix – repository‑wide source collector  
**Responsibility** – Walk a project directory, filter out unwanted files/folders and emit a single *code‑mix* text file that contains a tree view of the repository followed by the raw contents of every kept file. This file is the primary input for later preprocessing (splitting, compression) and documentation generation stages.

### <a name="code‑mix‑api"></a>Public API  
| Member | Type / signature | Description |
|--------|-------------------|-------------|
| `__init__(self, root_dir=".", ignore_patterns=None)` | `root_dir: str | Path` – base folder; `ignore_patterns: list[str]` – glob patterns. | Resolves `root_dir`, stores ignore list, creates a `BaseLogger` for status messages. |
| `should_ignore(self, path: Path) -> bool` | Returns *True* if `path` (relative to `root_dir`) matches any pattern (full path, basename, or any path component). |
| `build_repo_content(self, output_file="repomix-output.txt")` | Writes the mixed file. | 1️⃣ Emits “Repository Structure” with indented tree. 2️⃣ Inserts a separator line. 3️⃣ For each non‑ignored file writes `<file path="…">` header and its UTF‑8 text (errors ignored). Logs ignored items at level 1. |

### <a name="code‑mix‑interaction"></a>Interaction with the system  
* **Inputs** – Physical files under `root_dir`; optional `ignore_patterns`.  
* **Outputs** – `output_file` (plain‑text “code‑mix”); log entries via `BaseLogger`.  
* **Consumers** – `Manager.generate_global_info_file`, `Manager.generete_doc_parts`, and any downstream component that expects a single mixed source file.  
* **Side effects** – File creation on disk, logging; no mutation of source files.

### <a name="code‑mix‑assumptions‑limits"></a>Assumptions & limits  
* All source files are readable as UTF‑8 (binary files are filtered out by patterns).  
* Ignoring is purely pattern‑based; complex VCS‑aware rules must be expressed as globs.  
* The separator (`"="*20`) marks the boundary for downstream splitters.  

---  
*The `ignore_list` defined at module level provides sensible defaults (virtual envs, caches, compiled artefacts, markdown docs, etc.).*

## <a name="compressor‑overview"></a>Compressor module – high‑level view  
The *compressor* prepares source‑code chunks for downstream processing (e.g., global‑info generation). It reduces large texts by sending them to a LLM ( `Model` / `AsyncModel` ) with a system prompt derived from **ProjectSettings** and a configurable *compress_power*. The output is a shortened representation that still preserves structural clues.

---

## <a name="core‑functions"></a>Key functions  

| Function | Responsibility | Main I/O | Side‑effects |
|----------|----------------|----------|--------------|
| **compress** | Build a three‑message prompt and obtain a single LLM answer. | `data: str` → `str` | None (network call only). |
| **compress_and_compare** | Synchronously batch‑compress *compress_power* files, concatenate results, and report progress. | `list[str]` → `list[str]` (≈ len/ compress_power items) | Updates `BaseProgress`. |
| **async_compress** | Same as *compress* but guarded by an `asyncio.Semaphore` and updates progress asynchronously. | `str` → `str` (awaitable) | None besides progress update. |
| **async_compress_and_compare** | Parallel version of *compress_and_compare* using a semaphore (default 4 workers). | `list[str]` → `list[str]` | Progress sub‑task handling. |
| **compress_to_one** | Repeatedly compresses until a single aggregated string remains; switches to async mode if requested. | `list[str]` → `str` | May invoke `asyncio.run`. |
| **generate_describtions_for_code** | Sends each compressed block to the LLM with a strict “describe API” prompt, collects markdown‑ready descriptions. | `list[str]` → `list[str]` | Progress updates; no file I/O. |

---

## <a name="interaction‑model"></a>Interaction with the rest of the system  

* **Inputs** – Raw source‑code strings produced by the *collector* stage.  
* **Outputs** – Compressed text blobs consumed by `Manager.generate_global_info_file` and later splitters; description strings fed to the *doc‑generator* stage.  
* **Dependencies** –  
  * `ProjectSettings.prompt` (system context).  
  * `get_BASE_COMPRESS_TEXT` (template for compression intensity).  
  * `BaseProgress` for UI feedback.  
  * LLM model interfaces (`Model`, `AsyncModel`).  

The module is pure‑logic: it never writes files, only returns strings and updates the progress UI.

---

## <a name="assumptions‑limits"></a>Assumptions & limits  

* All incoming texts are UTF‑8 readable; binary artefacts must be filtered earlier.  
* Compression quality is driven solely by *compress_power* (default 4) and the static prompt template – no VCS‑aware heuristics.  
* Asynchronous workers are capped at four concurrent calls to avoid overwhelming the LLM endpoint.  

---  

*Use this module when you need to shrink large codebases into a single “code‑mix” representation before documentation generation.*

<a name="postprocess-overview"></a>
## postprocess – Final‑stage documentation polishing  

The *postprocess* module is the last step of the **autodocgenerator** pipeline.  
After the raw “code‑mix” markdown has been created it extracts headings and
HTML anchors, asks the LLM to craft a short introduction that lists the
available sections, and optionally generates a custom description for a
user‑supplied topic.

**Responsibility**  
* Parse markdown headers (`##`) → generate Markdown‑compatible anchors.  
* Scan existing `<a name=…>` tags → collect internal HTML links.  
* Build LLM prompts (using `BASE_INTRODACTION_CREATE_TEXT` / `BASE_INTRO_CREATE`)
  and retrieve generated introductory text.  
* Provide a helper (`generete_custom_discription`) that iteratively asks the
  model for a concise description until a non‑empty answer is obtained.

**Interaction with the system**  
* Relies on the generic **Model** interface (`model.get_answer_without_history`).  
* Uses configuration constants from `engine.config.config`.  
* Emits progress information through `ui.logging.BaseLogger` (InfoLog).  

**Key functions**

| Function | Purpose | Input / Output |
|----------|---------|----------------|
| `generate_markdown_anchor(header:str) -> str` | Normalises a header to a GitHub‑style `#anchor`. | Header text → `#slug` |
| `get_all_topics(data:str) -> tuple[list[str], list[str]]` | Finds every `##` heading, returns titles and their markdown anchors. | Full markdown → `(titles, anchors)` |
| `get_all_html_links(data:str) -> list[str]` | Extracts internal `<a name=…>` links (max 25 chars) and logs the count. | Full markdown → list of `#name` |
| `get_links_intro(links:list[str], model:Model, language:str="en") -> str` | Calls the LLM to produce an introductory paragraph that enumerates the supplied links. | Links + model → generated text |
| `get_introdaction(global_data:str, model:Model, language:str="en") -> str` | Generates a generic introduction for the whole documentation block. | Full doc + model → intro |
| `generete_custom_discription(splited_data:str, model:Model, custom_description:str, language:str="en") -> str` | Loops over split fragments, asking the model for a strict description of a custom topic; stops on the first non‑empty answer. | Fragments + description + model → description or empty string |

**Assumptions & side effects**  
* Input markdown uses `\n## ` for top‑level sections and `<a name=…>` for anchors.  
* The LLM is expected to respect the *Strict Rules* prompt; otherwise the
  function may return `"!noinfo"` or `"No information found"`.  
* Logging is performed synchronously; no external state is mutated besides
  the logger.  

This module therefore “tidies up” the generated documentation, making it
navigable and providing human‑readable introductions before the final output
is written to disk.

<a name="data-splitting"></a>
## Data Splitting – `split_data`

*Responsibility* – Breaks a large source‑code string into chunks that respect `max_symbols` (≈ token limit of the LLM).  
*Interaction* – Called by the orchestration functions (`gen_doc_parts`, `async_gen_doc_parts`) to produce the list `splited_data`.  
*Logic* – Iteratively trims any chunk > 1.5 × `max_symbols` by inserting a half‑size slice, then packs the resulting pieces into `split_objects` while ensuring no object exceeds 1.25 × `max_symbols`.  
*Assumptions* – Input is a plain‑text code dump; `max_symbols` is a positive integer.  
*Outputs* – `List[str]` where each element is safe to send to the LLM.  

<a name="sync-part-doc-generation"></a>
## Synchronous Part Documentation – `write_docs_by_parts`

*Responsibility* – Sends a single code chunk to the LLM and returns the generated markdown.  
*Interaction* – Consumes `Model.get_answer_without_history`; receives the previous part’s output (`prev_info`) to maintain context.  
*Key Steps* –  
1. Build a system‑prompt that forces the requested language and injects `BASE_PART_COMPLITE_TEXT`.  
2. Optionally append the previous documentation fragment.  
3. Append the user‑prompt containing the code part (twice, per original design).  
4. Strip surrounding triple‑backticks from the LLM answer.  
*Inputs* – `part: str`, `model: Model`, `global_info: str` (currently unused), optional `prev_info`, `language`.  
*Outputs* – Cleaned documentation string for the part.  

<a name="async-part-doc-generation"></a>
## Asynchronous Part Documentation – `async_write_docs_by_parts`

*Responsibility* – Same as the sync version but runs concurrently under a semaphore.  
*Interaction* – Uses `AsyncModel.get_answer_without_history`; calls `update_progress` after each LLM response.  
*Side Effects* – Logs progress and may raise if the semaphore limit is exceeded.  

<a name="orchestration"></a>
## Orchestration – `gen_doc_parts` / `async_gen_doc_parts`

*Responsibility* – Drives full‑document generation by:
1. Splitting the whole code base (`split_data`).  
2. Serially (or concurrently) invoking the part‑generation helpers.  
3. Accumulating results, keeping a 3 000‑character tail (`result = result[-3000:]`) to provide context for the next chunk.  
4. Updating a `BaseProgress` sub‑task for UI feedback.  
*Interactions* – Relies on the logger (`BaseLogger`), progress bar, and the appropriate model interface.  
*Outputs* – The complete documentation string for the supplied code base.  

These components together enable the AutoDocGenerator to respect LLM token limits while producing coherent, language‑specific documentation in both synchronous and asynchronous pipelines.

**AutoDocGenerator – UI & Setup Documentation**  

<a name="logging"></a>**Logging subsystem (`ui/logging.py`)**  
- **Responsibility** – Provides a lightweight, extensible logging façade used throughout the generator (e.g., during parsing, model calls, file writes).  
- **Core classes**  
  - `BaseLog`: stores `message` and numeric `level`; `_log_prefix` adds a timestamp.  
  - `ErrorLog`, `WarningLog`, `InfoLog`: override `format()` to prepend severity tags.  
  - `BaseLoggerTemplate`: holds a `log_level` filter and routes logs to `print()`.  
  - `FileLoggerTemplate`: same API but appends formatted messages to a user‑specified file.  
  - `BaseLogger` (singleton): holds the active `logger_template`; `set_logger()` swaps implementations, `log()` forwards to `global_log()` which respects the filter.  
- **Interaction** – UI components (e.g., `progress_base`, CLI) call `BaseLogger().log(ErrorLog(...))`; the concrete template decides where the text ends up.

<a name="progress"></a>**Progress subsystem (`ui/progress_base.py`)**  
- **Responsibility** – Visual feedback for multi‑step documentation generation, abstracted to allow Rich‑based or plain‑console rendering.  
- **Key abstractions**  
  - `BaseProgress`: defines the interface (`create_new_subtask`, `update_task`, `remove_subtask`).  
  - `LibProgress`: wraps a `rich.progress.Progress` object, creates a “General progress” task and optional sub‑tasks, advancing the appropriate bar on each `update_task()`.  
  - `ConsoleTask`: tiny helper that prints start and percentage updates.  
  - `ConsoleGtiHubProgress`: implements `BaseProgress` using `ConsoleTask`; useful when Rich is unavailable (e.g., CI logs).  
- **Interaction** – The main generation pipeline instantiates either `LibProgress` or `ConsoleGtiHubProgress` and calls the three interface methods as stages (parsing, model inference, file writing) progress.

<a name="install-scripts"></a>**Project bootstrap scripts**  
- **`install.ps1` (PowerShell)** and **`install.sh` (Bash)** create a GitHub‑Actions workflow (`.github/workflows/autodoc.yml`) and a minimal `autodocconfig.yml`.  
- They ensure the workflow directory exists, write static YAML content with proper escaping, inject the current folder name as `project_name`, and confirm success via console output.  
- These scripts are the entry point for users to enable the AutoDocGenerator CI integration with a single command.

---  

*All components cooperate: the logger records events, the progress visualizer reflects the pipeline state, and the install scripts set up CI to run the generator automatically.*

It looks like you’ve pasted the **`pyproject.toml`** file twice, but the request was to write documentation for a specific code fragment (the “last part” of the documentation that sets up the CI‑integration entry point).  

Could you share the actual Python script / module you’d like documented (e.g., the install‑or‑setup script that prints the folder name as `project_name` and confirms success on the console)? Once I have that snippet I can produce the concise, linked documentation you need.

