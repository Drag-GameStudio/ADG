## Executive Navigation Tree
- 📂 **Installation & Setup**
  - [install_workflow'](#install_workflow')
  - [manager_usage'](#manager_usage')
  - [package-initializer](#package-initializer)
  - [auto_runner_config_reader](#auto_runner_config_reader)
  - [auto_runner_run_file](#auto_runner_run_file)

- ⚙️ **Manager & Core**
  - [engine_init](#engine_init)
  - [config_constants_prompts](#config_constants_prompts)
  - [environment_api_key](#environment_api_key)
  - [model_names](#model_names)
  - [factory‑core](#factory‑core)
  - [intro-modules](#intro‑modules)
  - [manager-overview](#manager-overview)
  - [responsibility](#responsibility)
  - [interaction](#interaction)
  - [key-methods](#key-methods)
  - [usage-example](#usage-example)
  - [model‑hierarchy](#model‑hierarchy)
  - [gpt‑models](#gpt‑models)

- 🧩 **Compression Utilities**
  - [compress_prompt_helper](#compress_prompt_helper)
  - [compress](#compress)
  - [compress-and-compare](#compress-and-compare)
  - [async‑compress](#async‑compress)
  - [compress-to-one](#compress-to-one)
  - [generate-descriptions](#generate-descriptions)
  - [compressor‑overview](#compressor‑overview)

- 🔧 **Exceptions & Helpers**
  - [exceptions](#exceptions)
  - [markdown-anchor](#markdown-anchor)

- 🔗 **Extraction & Parsing**
  - [topic‑extraction](#topic‑extraction)
  - [html-link‑extraction](#html‑link‑extraction)
  - [global‑intro](#global‑intro)
  - [custom‑description](#custom‑description)

- 📊 **Data Processing**
  - [data‑splitting](#data‑splitting)
  - [data‑splitting‑engine](#data‑splitting‑engine)

- 📝 **Documentation Assembly**
  - [part‑doc‑writer](#part‑doc‑writer)
  - [async‑part‑doc‑writer](#async‑part‑doc‑writer)
  - [doc‑assembly‑sync](#doc‑assembly‑sync)
  - [doc‑assembly‑async](#doc‑assembly‑async)

- 🚀 **Progress & Interface**
  - [base‑progress‑interface](#base‑progress‑interface)

 

<a name='install_workflow'> </a>
Explain how install workflow with `install.ps1` and `install.sh` scripts for install you should use links `irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex` for PowerShell and `curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash` for Linux‑based systems and also you have to add secret variable to GitHub Action `GROCK_API_KEY` with your API key from Grock docs https://grockdocs.com to make it work.

<a name='manager_usage'> </a>
**How to use the `Manager` class**

The `Manager` class is instantiated in the **autodocgenerator/auto_runner/run_file.py** script with the following parameters:

| Parameter | Type | Description (inferred from usage) |
|-----------|------|------------------------------------|
| `project_path` | `str` | Path to the root of the project you want to document. |
| `project_settings` | `ProjectSettings` | Holds project‑specific metadata (name, additional info, etc.). |
| `sync_model` | `GPTModel` | Synchronous GPT model used for generating documentation. |
| `async_model` | `AsyncGPTModel` | Asynchronous GPT model (optional, can be used for async generation). |
| `ignore_files` | `list[str]` | List of file‑patterns that should be ignored during processing. |
| `progress_bar` | `BaseProgress` (e.g., `ConsoleGtiHubProgress`) | Progress‑bar implementation that displays generation status. |
| `language` | `str` | Language code for the generated docs (e.g., `"en"`). |

### Full example of usage

```python
# example_usage.py
from autodocgenerator.manage import Manager
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.preprocessor.settings import ProjectSettings
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress

# 1. Prepare required objects
project_path = "."                     # current directory (or any other path)
project_settings = ProjectSettings("MyProject")  # initialise with project name
# (add any additional info to `project_settings` if needed)

# 2. Initialise GPT models (API key is taken from autodocgenerator.engine.config.config)
sync_model = GPTModel(API_KEY)
async_model = AsyncGPTModel(API_KEY)

# 3. Define ignore patterns (can be extended)
ignore_list = [
    "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db",
    "data", "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml",
    ".gitignore", ".ruff_cache", ".auto_doc_cache", "*.pyc", "__pycache__",
    ".git", ".coverage", "htmlcov", "migrations", "*.md", "static",
    "staticfiles", ".mypy_cache"
]

# 4. Choose a progress bar implementation
progress = ConsoleGtiHubProgress()

# 5. Create the Manager instance
manager = Manager(
    project_path,
    project_settings,
    sync_model=sync_model,
    async_model=async_model,
    ignore_files=ignore_list,
    progress_bar=progress,
    language="en"
)

# 6. Run the documentation generation workflow
manager.generate_code_file()
manager.generate_global_info_file(use_async=False, max_symbols=8000)
manager.generete_doc_parts(use_async=False, max_symbols=5000)

# 7. Generate the final documentation using factories
# (doc_factory and intro_factory are obtained from autodocgenerator.auto_runner.config_reader)
from autodocgenerator.auto_runner.config_reader import read_config, Config
with open("autodocconfig.yml", "r", encoding="utf-8") as f:
    cfg_data = f.read()
cfg: Config = read_config(cfg_data)
doc_factory, intro_factory = cfg.get_doc_factory()

manager.factory_generate_doc(doc_factory)
manager.factory_generate_doc(intro_factory)

# 8. Retrieve the generated documentation
output = manager.read_file_by_file_key("output_doc")
print(output)   # or write it to README.md, etc.
```

**Key points**

* All required parameters are supplied when constructing `Manager`.
* After creation, invoke the sequence of methods shown above to generate code snippets, global info, documentation parts, and finally assemble the full document.
* The example mirrors the exact flow used in `autodocgenerator/auto_runner/run_file.py`.

<a name='autodocconfig'> 
**autodocconfig.yml – available options**

The file is a plain YAML document that can contain the following top‑level keys, which are read by `autodocgenerator.auto_runner.config_reader.read_config`:

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `ignore_files` | list of strings | File‑name patterns that the generator will skip while scanning the project. If omitted the default list from `Config.__init__` is used. | `ignore_files: ["*.log", "venv", ".git"]` |
| `language` | string | Language code for the generated documentation (default: `"en"`). | `language: "ru"` |
| `project_name` | string | Name of the project – used in the intro section and for overall context. | `project_name: "My Awesome Library"` |
| `project_additional_info` | mapping (key → string) | Arbitrary key‑value pairs that are added to `ProjectSettings`. They can be referenced by custom modules. | ```project_additional_info:\n  author: \"John Doe\"\n  license: \"MIT\"``` |
| `custom_descriptions` | list of strings | Each string becomes a `CustomModule` that will be processed by the documentation engine. Use them to request specific sections, explanations, or any custom text. | ```custom_descriptions:\n  - "explain how to install the library"\n  - "provide usage example for Manager class"``` |

**Minimal example**

```yaml
project_name: "My Project"
language: "en"

project_additional_info:
  description: "A short summary of the project."
  version: "0.1.0"

custom_descriptions:
  - "Explain the installation steps."
  - "Show an example of using the Manager class."

# optional, overrides the built‑in ignore list
ignore_files:
  - "*.tmp"
  - "build"
```

Only the keys you need must be present; missing keys fall back to the defaults defined in `Config`. </a>

 

<a name="package-initializer"></a>
## Package Initializer (`autodocgenerator/__init__.py`)

**Responsibility**  
The `__init__.py` file marks the *autodocgenerator* directory as a Python package and executes a single side‑effect: it prints the literal string **`ADG`** to standard output whenever the package is imported.

**Interactions**  
- **Importers** – Any module that performs `import autodocgenerator` (directly or indirectly via sub‑modules such as `autodocgenerator.auto_runner.run_file`) will trigger the `print`.  
- **No external dependencies** – The file contains no imports, configuration reads, or runtime logic, so it does not rely on or affect other components (engine, factory, UI, etc.).

**Key Logic Flow**  
1. Python evaluates the file during package import.  
2. Executes `print("ADG")`.  
3. Returns control to the importer; the package’s sub‑modules become available.

**Assumptions & Side Effects**  
- **Assumption** – The package is imported in a context where writing to `stdout` is harmless (e.g., CLI tools, CI runs).  
- **Side Effect** – Unconditional console output may clutter logs or interfere with programs that capture stdout; it does not affect functional behavior.

**Typical Usage**  
```python
import autodocgenerator   # Triggers the "ADG" banner
from autodocgenerator.auto_runner import run_file
# Normal operation proceeds after the banner is printed
```

**Recommendation**  
For library consumers, consider removing the `print` statement or guarding it behind a debug flag to avoid unwanted output in production environments.

<a name="auto_runner_config_reader"></a>
## `autodocgenerator.auto_runner.config_reader` – Configuration Loader  

**Responsibility**  
Parses a YAML‑style configuration file and builds a **`Config`** object that centralises all runtime settings required by the auto‑doc generation pipeline.

**Interactions**  
- Consumed by **`autodocgenerator.auto_runner.run_file`** (via `read_config`).  
- Supplies objects to the **factory** (`DocFactory`) and **pre‑processor** (`ProjectSettings`).  
- Does **not** touch the engine, UI or external services.

**Key API**  
| Member | Purpose |
|--------|---------|
| `Config` | Holds mutable defaults: `ignore_files`, `language`, `project_name`, `project_additional_info`, `custom_modules`. |
| `Config.set_language / set_project_name` | Fluent setters used while building the config. |
| `Config.add_ignore_file` | Extends the default ignore pattern list. |
| `Config.add_custom_module` | Registers a `CustomModule` (user‑provided description). |
| `Config.get_project_settings()` | Returns a `ProjectSettings` instance populated with the project name and any extra key/value info. |
| `Config.get_doc_factory()` | Creates two `DocFactory` instances – one for custom modules, another for built‑in intro modules (`IntroLinks`, optionally `IntroText`). |
| `read_config(file_data: str) -> Config` | Core parser: `yaml.safe_load` → fills `Config` fields, handling optional keys (`ignore_files`, `language`, `project_name`, `project_additional_info`, `custom_descriptions`). |

**Assumptions & Side Effects**  
- Input YAML is well‑formed; missing keys fall back to sensible defaults (e.g., `"en"` for language, empty project name).  
- No I/O or network calls – pure data transformation.  

---

<a name="auto_runner_run_file"></a>
## `autodocgenerator.auto_runner.run_file` – Entry Point for Documentation Generation  

**Responsibility**  
Orchestrates the full documentation generation flow: loads configuration, instantiates models, creates a `Manager`, runs all generation steps, and returns the final assembled document.

**Interactions**  
- Imports **`Config`** and **`read_config`** from the sibling `config_reader`.  
- Instantiates **`GPTModel`** / **`AsyncGPTModel`** (engine).  
- Builds a **`Manager`** (core orchestration) with a **`ConsoleGtiHubProgress`** UI component.  
- Calls manager methods that rely on factories (`DocFactory`) and settings (`ProjectSettings`).  

**Key Function**  
```python
def gen_doc(project_settings, ignore_list, project_path,
            doc_factory, intro_factory) -> str:
    """
    Executes the complete doc‑generation pipeline and returns the final
    markdown/text output.
    """
```
- Creates sync/async LLM wrappers using the global `API_KEY`.  
- Constructs `Manager` with all required collaborators.  
- Sequentially triggers:
  1. `generate_code_file()`
  2. `generate_global_info_file(use_async=False, max_symbols=8000)`
  3. `generete_doc_parts(use_async=False, max_symbols=5000)`
  4. `factory_generate_doc` for both the custom and intro factories.  
- Returns `manager.read_file_by_file_key("output_doc")`.

**CLI Guard**  
When run as a script (`python -m autodocgenerator.auto_runner.run_file`) it reads `autodocconfig.yml`, builds the config, and prints the generated document.  

**Assumptions & Side Effects**  
- `API_KEY` is available and valid; otherwise LLM calls will fail.  
- The progress UI writes to stdout/stderr, which is acceptable for interactive runs.  
- All file I/O is limited to the project directory (`project_path`).  

---

<a name="engine_init"></a>
## `autodocgenerator.engine.__init__`  

**Responsibility**  
Package marker; currently empty, serving only to make `autodocgenerator.engine` a importable Python package. No runtime behavior is defined here.

<a name="config_constants_prompts"></a>
## Configuration constants & prompt templates  

**Responsibility** – Provides the static textual prompts that drive the LLM agents used throughout the AutoDoc system.  
**Interaction** – All higher‑level modules import these strings (e.g., `BASE_SYSTEM_TEXT`, `BASE_PART_COMPLITE_TEXT`, `BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`, `BASE_SETTINGS_PROMPT`) and feed them to the language model when constructing system or user messages.  
**Key data** – Multi‑line strings describing how snippets are analyzed, how documentation parts are generated, how navigation trees are built, and how project settings are memorised.  

---

<a name="environment_api_key"></a>
## Environment loading & API key validation  

```python
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise Exception("API_KEY is not set in environment variables.")
```  

*Loads* `.env` files, extracts `API_KEY`, and aborts early if missing.  
**Assumption** – The runtime environment supplies a valid OpenAI (or compatible) API key; otherwise any LLM call will fail. No side effects besides environment variable access.

---

<a name="model_names"></a>
## Supported model identifiers  

```python
MODELS_NAME = [
    "openai/gpt-oss-120b",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-safeguard-20b",
]
```  

A hard‑coded list of model names the engine may select for generation. Other components (e.g., `engine.models`) reference this list to instantiate the appropriate LLM wrapper.

---

<a name="compress_prompt_helper"></a>
## `get_BASE_COMPRESS_TEXT(start, power)` – Prompt generator for large snippets  

**Purpose** – Returns a formatted instruction prompting the model to summarise a large code fragment and provide a strict usage example.  
**Parameters**  
- `start` (int): Approximate maximum character count of the incoming snippet.  
- `power` (int): Divisor controlling the allowed summary length (`~ start/power` chars).  

**Returned value** – A multi‑line string containing three sections: analysis request, length‑limited summary, and a precise Python usage example template.  

**Interaction** – Called by the compression stage of the pipeline (e.g., when a file exceeds token limits) to produce a custom system prompt for the LLM.  

**Assumptions & side effects** – Pure function; no I/O, only string interpolation.  

---

<a name="exceptions"></a>
## Exceptions – ModelExhaustedException
`ModelExhaustedException` is raised when the shuffled list `regen_models_name` becomes empty, i.e. no fallback model is left. It inherits directly from `Exception` and carries a short doc‑string; no side‑effects.

<a name="model‑hierarchy"></a>
## Model hierarchy (`model.py`)
* **History** – stores the conversation as a list of `{role, content}` dicts. The constructor injects the system prompt (`BASE_SYSTEM_TEXT`) unless `None`.
* **ParentModel** – base for both sync and async models. It keeps the API key, a `History` instance, a shuffled copy of `MODELS_NAME` (`regen_models_name`) and an index (`current_model_index`) used for round‑robin fallback.
* **Model** (sync) – implements:
  * `generate_answer` – abstract placeholder overridden in concrete models.
  * `get_answer_without_history` – forwards a raw message list to `generate_answer`.
  * `get_answer` – records the user prompt, calls `generate_answer`, records the assistant reply, and returns it.
* **AsyncModel** – async counterparts of the above methods.

Assumptions: `MODELS_NAME` is a non‑empty list; `History` can be shared safely because it contains only in‑memory data.

<a name="gpt‑models"></a>
## Concrete GPT models (`gpt_model.py`)
* **AsyncGPTModel** (`AsyncModel` subclass) – creates an `AsyncGroq` client.  
  * `generate_answer` builds the message payload from history or a raw `prompt`, then loops over `regen_models_name` attempting `client.chat.completions.create`. On failure it prints the exception, advances `current_model_index`, and retries until a response is obtained or the list is exhausted (raising `ModelExhaustedException`). Returns the first choice’s `content`.
* **GPTModel** – same logic but synchronous, using `Groq`.

Interaction: factories inject a `Model` (or `AsyncModel`) instance into modules; modules call `model.get_answer…` which internally uses the above generation logic.

<a name="factory‑core"></a>
## Documentation factory core (`base_factory.py` & `general_modules.py`)
* **BaseModule (ABC)** – contract for pluggable documentation generators; must implement `generate(info, model)`.
* **DocFactory** – aggregates `BaseModule` instances. `generate_doc(info, model, progress)`:
  1. Starts a sub‑task in `BaseProgress`.
  2. Calls each module’s `generate`, concatenates results with double newlines.
  3. Updates progress after every module and removes the sub‑task.
  Returns the final markdown string.

* **CustomModule** (in `general_modules.py`) – a concrete `BaseModule` that:
  * Splits the mixed code (`info["code_mix"]`) into ≤ 7000‑symbol chunks via `split_data`.
  * Calls `generete_custom_discription` (typo intentional) with the chunks, the supplied `model`, a custom description string, and the target language.
  * Returns the generated text.

**Side‑effects** – only console output on errors; all other state changes are confined to the `History` object and progress tracker.

<a name="intro-modules"></a>
## Intro Modules – Generating the Documentation Introduction

The **intro** package supplies the final step of the documentation pipeline – creating the opening section that appears at the top of each generated page. It consists of two concrete `BaseModule` implementations that are invoked by the *project‑and‑progress* orchestrator after the core content has been collected.

### `IntroLinks` – Link extraction & model‑driven phrasing  
```python
class IntroLinks(BaseModule):
    def generate(self, info: dict, model: Model):
        links = get_all_html_links(info.get("full_data"))
        print(links)                     # debugging aid
        intro_links = get_links_intro(links, model, info.get("language"))
        return intro_links
```
* **Responsibility** – Pull every `<a href>` from the raw HTML (`full_data`), then ask the language model (`model`) to compose a short introductory paragraph that references those links in the target language.  
* **Inputs** – `info["full_data"]` (raw HTML string), `info["language"]` (ISO code), and a configured `Model` instance.  
* **Outputs** – A string (or markup) ready for insertion into the final document.  
* **Side‑effects** – Emits the extracted link list to stdout (useful during development).  

### `IntroText` – High‑level project summary  
```python
class IntroText(BaseModule):
    def generate(self, info: dict, model: Model):
        intro = get_introdaction(info.get("global_data"), model, info.get("language"))
        return intro
```
* **Responsibility** – Ask the model to write a concise project overview based on the aggregated `global_data` (e.g., project name, goals, scope).  
* **Inputs** – `info["global_data"]` (structured summary dict), `info["language"]`, and the same `Model`.  
* **Outputs** – A ready‑to‑display introductory text block.  

### Integration Flow
1. The orchestrator gathers `info` from previous modules (pre‑processor, extractor).  
2. It instantiates `IntroLinks` and `IntroText`, feeding them the shared `info` and the active `Model`.  
3. Their `generate` methods return the two pieces that are later concatenated and placed at the very top of the final documentation page, just before the progress tracker.  

Both classes rely on the **postprocess** helpers (`get_all_html_links`, `get_links_intro`, `get_introdaction`) to keep the generation logic isolated from the underlying LLM calls. This design makes the intro stage easily replaceable or extendable without touching the rest of the pipeline.

<a name="manager-overview"></a>
## Manager – Orchestrator of the ADG Pipeline  

The **`Manager`** class is the high‑level coordinator that ties together every preprocessing, LLM‑generation, and post‑processing component of the *Auto Doc Generator* (ADG). It lives in `autodocgenerator/manage.py` and is the entry point used by the CLI script (the `if __name__ == "__main__"` block).  

---

<a name="responsibility"></a>
### Responsibility  

* **Prepare a cache directory** (`.auto_doc_cache`) inside the target project.  
* **Run each pipeline stage** in order – code mixing, global‑info extraction, documentation chunk generation, and optional factory‑based enrichment (e.g., intro links).  
* **Persist intermediate artefacts** (`code_mix.txt`, `global_info.md`, `output_doc.md`) so later stages can be re‑run without re‑processing the whole repository.  
* **Update the UI progress bar** (`BaseProgress` / `LibProgress`) after every stage.

---

<a name="interaction"></a>
### Interaction with Other Parts  

| Component | Interaction Point |
|-----------|-------------------|
| `CodeMix` (`preprocessor/code_mix.py`) | `generate_code_file()` – builds a flat text dump of the repo. |
| Split‑/Compress utilities (`spliter.py`, `compressor.py`) | `generate_global_info_file()` (currently stubbed) would split the mix and compress it with the selected LLM. |
| Doc‑generation helpers (`spliter.gen_doc_parts`, `spliter.async_gen_doc_parts`) | `generete_doc_parts()` – creates the main documentation body. |
| Factory modules (`factory/base_factory.py`, `factory/modules/*`) | `factory_generate_doc()` – injects custom modules (e.g., `IntroLinks`, `CustomModule`). |
| LLM models (`engine/models/*`) | Passed to the above helpers as `sync_model` or `async_model`. |
| UI (`ui/progress_base.py`) | `progress_bar.update_task()` is called after each step. |

---

<a name="key-methods"></a>
### Key Methods & Logic Flow  

| Method | Purpose | Important Parameters | Output / Side‑Effect |
|--------|---------|----------------------|----------------------|
| `__init__(project_directory, project_settings, sync_model, async_model, ignore_files, language, progress_bar)` | Initialise paths, store settings, create cache folder. | `project_directory`, `ignore_files`, `language`. | Creates `CACHE_FOLDER_NAME` directory. |
| `read_file_by_file_key(file_key)` | Convenience wrapper to read a cached artefact. | `file_key` (`"code_mix"`, `"global_info"`, `"output_doc"`). | Returns file contents as `str`. |
| `get_file_path(file_key)` | Builds absolute path for a cached file. | Same as above. | Returns path `str`. |
| `generate_code_file()` | Calls `CodeMix.build_repo_content` → writes `code_mix.txt`. | None. | Cached *code mix* file + progress update. |
| `generate_global_info_file(max_symbols, use_async)` | (Stub) would split `code_mix`, compress with LLM, and write `global_info.md`. | `max_symbols` limits chunk size, `use_async` selects model. | Currently writes placeholder `"ss"`; progress update. |
| `generete_doc_parts(max_symbols, use_async)` | Reads `global_info` & `code_mix`, then calls `gen_doc_parts` (sync) or `async_gen_doc_parts` (async) to produce the main markdown body. | Same as above. | Writes `output_doc.md`; progress update. |
| `factory_generate_doc(doc_factory)` | Supplies all artefacts to a `DocFactory`, receives additional markdown (e.g., intro links), prepends it to existing `output_doc.md`. | `doc_factory` – an instance of `DocFactory` with one or more modules. | Overwrites `output_doc.md` with enriched content; progress update. |

---

<a name="assumptions-inputs-outputs"></a>
### Assumptions, Inputs & Outputs  

* **Assumptions** – The repository is accessible and the ignore list correctly filters unwanted files. The LLM models provided implement the `Model` / `AsyncModel` interfaces.  
* **Inputs** – Project root path, `ProjectSettings` (global description), optional LLM models, language code, ignore patterns.  
* **Outputs** – Three cached files in `.auto_doc_cache` and a final documentation markdown (`output_doc.md`). No external side‑effects beyond file I/O and optional LLM API calls.

---

<a name="usage-example"></a>
### Typical Usage (as shown in `__main__`)  

```python
manager = Manager(
    project_directory=r"C:\Path\To\Repo",
    project_settings=ProjectSettings("Auto Doc Generator")
        .add_info("global idea", "This project helps developers generate docs."),
    sync_model=GPTModel(API_KEY),
    async_model=AsyncGPTModel(API_KEY),
    ignore_files=ignore_list,
    progress_bar=LibProgress(progress),
    language="en"
)

# Run selected stages (uncomment as needed)
# manager.generate_code_file()
# manager.generate_global_info_file(use_async=True, max_symbols=5_000)
# manager.generete_doc_parts(use_async=True, max_symbols=4_000)

# Add an introductory links block via the factory
manager.factory_generate_doc(
    DocFactory(IntroLinks())
)
```

The manager can be extended by adding more modules to the `DocFactory` (e.g., `CustomModule`) to tailor the final documentation.

<a name="code-mix‑component"></a>
## CodeMix – Repository‑wide source collector  

The **CodeMix** class lives in `autodocgenerator/preprocessor/code_mix.py`.  
Its sole responsibility is to traverse a project directory, filter out unwanted paths, and produce a single text artefact that contains:

1. A tree‑like listing of the repository structure.  
2. The raw contents of every non‑ignored source file wrapped in `<file path="…">` tags.

### Interaction with the system  
`Manager.generate_code_file()` creates a `CodeMix` instance (passing the project root and the global `ignore_list`) and calls `build_repo_content()`.  
The resulting file (`code_mix.txt`) becomes the first cached artefact that downstream stages (global‑info extraction, doc‑part generation) read via `Manager.read_file_by_file_key`.

### Key API  

| Method | Purpose | Important details |
|--------|---------|-------------------|
| `__init__(root_dir=".", ignore_patterns=None)` | Stores the absolute project root and the list of glob patterns used to skip files/folders. |
| `should_ignore(path: Path) -> bool` | Returns **True** if the relative path matches any ignore pattern (full path, basename, or any path component). Uses `fnmatch` for Unix‑style globbing. |
| `build_repo_content(output_file="repomix-output.txt")` | Writes two sections to `output_file`:<br>* **Repository Structure** – indented tree built from `Path.rglob("*")` respecting ignore rules.<br>* **File payloads** – for each kept file, writes a `<file path="…">` header followed by the file text (UTF‑8, errors ignored). Errors are logged inline. |

### Assumptions, inputs & outputs  

* **Assumptions** – The supplied `root_dir` exists and is readable; ignore patterns correctly describe files that should not appear in the documentation.  
* **Inputs** – `root_dir` (project path), `ignore_patterns` (list of glob strings).  
* **Outputs** – A single UTF‑8 text file (`output_file`) placed in the working directory; no side‑effects besides file I/O and console prints in the `__main__` demo.

### Usage excerpt (as used by the manager)  

```python
code_mix = CodeMix(root_dir=project_dir, ignore_patterns=ignore_list)
code_mix.build_repo_content("code_mix.txt")   # → cached artefact for later stages
```

The generated `code_mix.txt` is later consumed by the LLM‑driven pipeline to derive a high‑level overview and the final documentation.

<a name="compressor-overview"></a>
## Compressor – Core Pre‑processor

The **compressor** module reduces raw source‑code strings into concise summaries that can be fed to the LLM‑driven documentation pipeline. It works together with:

* `engine.models.gpt_model` – provides synchronous (`Model`) and asynchronous (`AsyncModel`) wrappers around the LLM.
* `engine.config.config.get_BASE_COMPRESS_TEXT` – returns a system‑prompt fragment that instructs the model how aggressively to compress (parameter `compress_power`).
* `ui.progress_base.BaseProgress` – visualises work in the console.
* `settings.ProjectSettings` – supplies the project‑specific system prompt (`project_settings.prompt`).

All functions return plain UTF‑8 strings or lists of strings; side‑effects are limited to progress‑bar updates and the final file write performed by the caller.

---

<a name="compress"></a>
### `compress(data, project_settings, model, compress_power) → str`

* **Purpose** – Sends a single code block to the LLM with a compression prompt and returns the model’s answer.
* **Inputs**  
  * `data` – raw code text.  
  * `project_settings` – contains `prompt` (system instruction).  
  * `model` – an instance of `Model` (synchronous).  
  * `compress_power` – integer controlling summary length.
* **Output** – compressed text string.

---

<a name="compress-and-compare"></a>
### `compress_and_compare(data, model, project_settings, compress_power=4, progress_bar=BaseProgress()) → List[str]`

* Splits `data` (list of file texts) into chunks of size `compress_power`.  
* Calls `compress` for each element, concatenating results per chunk.  
* Returns a list whose length is `ceil(len(data)/compress_power)`.  
* Updates `progress_bar` for each file processed.

---

<a name="async-compress"></a>
### Async variants (`async_compress`, `async_compress_and_compare`)

* Mirrors the synchronous flow but runs compression calls concurrently, limited by an `asyncio.Semaphore(4)`.  
* Accepts an `AsyncModel` and returns the same structures as their sync counterparts.  
* Progress updates happen inside the semaphore‑protected region.

---

<a name="compress-to-one"></a>
### `compress_to_one(data, model, project_settings, compress_power=4, use_async=False, progress_bar=BaseProgress()) → str`

* Repeatedly compresses the list until a single aggregated summary remains.  
* Dynamically reduces `compress_power` to `2` when the list becomes small.  
* Chooses the async or sync pipeline based on `use_async`.  
* Returns the final consolidated description.

---

<a name="generate-descriptions"></a>
### `generate_describtions_for_code(data, model, project_settings, progress_bar=BaseProgress()) → List[str]`

* For each compressed code chunk, builds a detailed LLM prompt that asks for:
  1. Main components,  
  2. Their purpose,  
  3. Parameters & types,  
  4. A copy‑pasteable usage example.  
* Sends the prompt via `model.get_answer_without_history`.  
* Returns a list of the generated documentation snippets.

---

<a name="exceptions"></a>
## Exceptions (`preprocessor/exceptions.py`)

The file is currently empty; the module reserves a namespace for future custom exception types (e.g., `CompressionError`, `RateLimitExceeded`). Adding specific exceptions will allow callers to distinguish LLM‑related failures from I/O issues.

**Documentation – `autodocgenerator.preprocessor` (post‑processing & helper utilities)**  

<a name="markdown-anchor"></a>
### `generate_markdown_anchor(header: str) → str`  
Creates a GitHub‑style markdown anchor from a heading.  
* Normalises Unicode, lower‑cases, replaces spaces with “‑”, strips disallowed characters and collapses duplicate hyphens.  
* Returns the anchor prefixed with “#”.  
* **Side‑effects:** none – pure function.

<a name="topic-extraction"></a>
### `get_all_topics(data: str) → tuple[list[str], list[str]]`  
Scans a generated markdown document for top‑level sections (`## …`).  
* Returns a tuple: (`topics`, `links`) where `links` are the anchors produced by `generate_markdown_anchor`.  
* Used by the final formatter to build a table‑of‑contents.

<a name="html-link‑extraction"></a>
### `get_all_html_links(data: str) → list[str]`  
Extracts legacy HTML anchors (`<a name="…">`) from the document.  
* Ignores anchors longer than 25 characters (treated as noise).  
* Returns a list of markdown links (`#anchor`).  

<a name="intro‑links"></a>
### `get_links_intro(links: list[str], model: Model, language: str = "en") → str`  
Builds a system‑prompt that asks the LLM to write an introductory paragraph for a list of section links.  
* Sends the prompt via `model.get_answer_without_history`.  
* Returns the raw LLM text.  

<a name="global‑intro"></a>
### `get_introdaction(global_data: str, model: Model, language: str = "en") → str`  
Similar to `get_links_intro` but operates on the whole document text (`global_data`).  
* Uses the constant `BASE_INTRO_CREATE` as the system instruction.  

<a name="custom‑description"></a>
### `generete_custom_discription(splited_data: str, model: Model, custom_description: str, language: str = "en") → str`  
Iterates over pre‑split code/document fragments until the LLM can produce a non‑empty, qualified answer for a user‑supplied `custom_description`.  
* Prompt enforces strict “use only the provided context” rules and asks for a title + `<a name='…'>` anchor.  
* If the LLM returns “!noinfo” or “No information found”, the loop continues; otherwise the result is returned.  
* Returns an empty string when no fragment yields information.

---

<a name="project‑settings"></a>
### `ProjectSettings` (in *settings.py*)  
Container for per‑project metadata that is injected into LLM system prompts.  

| Member | Description |
|--------|-------------|
| `project_name` (str) | Human‑readable project identifier. |
| `info` (dict) | Arbitrary key/value pairs added via `add_info`. |
| `prompt` (property) | Concatenates `BASE_SETTINGS_PROMPT` with the project name and all `info` entries, producing the final system‑prompt string. |

*No side‑effects* – the class only stores data.

---

<a name="data‑splitting"></a>
### `split_data(data: str, max_symbols: int) → list[str]` *(partial implementation in *spliter.py*)*  
Intended to chunk a large markdown string into pieces that respect the LLM token limit (`max_symbols`).  
* Currently creates an empty `split_objects` list and begins to split on the marker `"* The function will eventually return a list of string chunks, each ≤ `max_symbols` characters, preserving file boundaries where possible.  
* At the moment it only initialises `split_objects` and splits the input on the sentinel `

<a name="data‑splitting‑engine"></a>### `split_data(data: str, max_symbols: int) → list[str]`  
Chunk a large markdown source into pieces that fit the LLM token budget.  
* Splits on file‑level markers, then repeatedly breaks any chunk > 1.5 × `max_symbols` into two halves.  
* Re‑assembles pieces while keeping each ≤ 1.25 × `max_symbols`.  
* Returns a list of strings ready for LLM consumption.  
* **Side‑effects:** none – pure function.

<a name="part‑doc‑writer"></a>### `write_docs_by_parts(part: str, model: Model, global_info: str, prev_info: str | None = None, language: str = "en") → str`  
Builds a prompt (system‑language hint + `BASE_PART_COMPLITE_TEXT` + optional previous output) and calls `model.get_answer_without_history`.  
* Strips surrounding markdown fences (```).  
* Returns the raw LLM‑generated documentation for the supplied code fragment.  

<a name="async‑part‑doc‑writer"></a>### `async_write_docs_by_parts(...) → str`  
Async counterpart of `write_docs_by_parts`.  
* Executes the same prompt inside an `asyncio.Semaphore` to limit concurrency.  
* Calls `async_model.get_answer_without_history` and optionally fires `update_progress`.  

<a name="doc‑assembly‑sync"></a>### `gen_doc_parts(full_code_mix, global_info, max_symbols, model, language, progress_bar)`  
* Splits the whole source via `split_data`.  
* Iterates over chunks, invoking `write_docs_by_parts` sequentially, feeding the last 3000 chars of the previous answer as context (`prev_info`).  
* Updates a `BaseProgress` sub‑task after each chunk and concatenates all parts into the final markdown document.  

<a name="doc‑assembly‑async"></a>### `async_gen_doc_parts(...)`  
* Mirrors `gen_doc_parts` but launches `async_write_docs_by_parts` for all chunks concurrently (default 4‑worker semaphore).  
* Aggregates results preserving order, updates progress via callbacks, and returns the combined documentation.  

**Interaction flow** – `split_data` → (sync/async) `write_docs_by_parts` → `gen_doc_parts`/`async_gen_doc_parts` → final markdown. All functions are pure besides the LLM calls and progress updates.

**Progress handling utilities** – `autodocgenerator/ui/progress_base.py`  

<a name="base‑progress‑interface"></a>### `BaseProgress` (interface)  
*Abstract contract used by the documentation pipeline to report incremental work.*  
- **Methods**  
  - `create_new_subtask(name: str, total_len: int)`: allocate a sub‑task that will receive `total_len` update calls.  
  - `update_task()`: advance the *currently active* task by one step.  
  - `remove_subtask()`: discard the active sub‑task, causing subsequent calls to affect the parent task.  
- **Assumptions** – concrete subclasses implement the three methods; the class itself does nothing.

<a name="rich‑progress‑implementation"></a>### `LibProgress` – Rich‑based visualizer  
- **Constructor** `__init__(self, progress: Progress, total: int = 4)`  
  - Receives a **Rich `Progress`** instance (shared UI object).  
  - Creates a *base* task “General progress” with `total` steps; stores its ID in `_base_task`.  
- **`create_new_subtask`** – registers a new Rich task and stores its ID in `_cur_sub_task`.  
- **`update_task`** – if a sub‑task exists, updates it; otherwise advances the base task.  
- **`remove_subtask`** – clears the stored sub‑task reference.  
- **Side‑effects** – updates the Rich live‑rendered progress bar shown to the user.

<a name="console‑progress‑implementation"></a>### `ConsoleGtiHubProgress` – fallback for CI / non‑TTY runs  
- Uses the lightweight `ConsoleTask` helper to emit plain‑text progress lines.  
- Keeps a single *general* task (`gen_task`) and an optional *current* sub‑task (`curr_task`).  
- `create_new_subtask` → spawns a new `ConsoleTask`.  
- `update_task` → calls `progress()` on the active task, falling back to the general one.  
- `remove_subtask` → discards the sub‑task reference.  

**Interaction with the rest of the system**  
Both progress classes are injected into the *doc‑assembly* functions (`gen_doc_parts`, `async_gen_doc_parts`). After each chunk is processed they call `update_task()` to move the visual indicator forward and `remove_subtask()` when a chunk finishes. The rest of the pipeline treats them as pure side‑effect objects; no return values are expected.  

**Typical usage**  

```python
from rich.progress import Progress
progress = Progress()
pbar = LibProgress(progress, total=len(chunks))

for chunk in chunks:
    pbar.create_new_subtask("Chunk", total_len=len(chunk))
    # … generate docs for the chunk …
    pbar.update_task()
    pbar.remove_subtask()
```  

The console implementation follows the same API, enabling the same pipeline to run in headless CI environments.  

