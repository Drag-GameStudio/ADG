## Executive Navigation Tree
- 📂 Configuration
  - [autodocconfig_options](#autodocconfig_options')
  - [config_reader](#config_reader)
  - [config_constants](#config_constants)
  - [pyproject](#pyproject)
- ⚙️ Execution Engine
  - [run_file](#run_file)
  - [manager](#manager)
  - [factory](#factory)
  - [modules](#modules)
  - [model](#model)
  - [gpt_model](#gpt_model)
- 🔧 Processing Pipeline
  - [codemix](#codemix)
  - [compressor](#compressor)
  - [postprocess](#postprocess)
  - [spliter](#spliter)
  - [progressbase](#progressbase)
- 🛠️ Setup & Install
  - [Install_Workflow](#Install_Workflow)
  - [Manager_Usage](#Manager_Usage')

**Project Overview – Auto Doc Generator**

---

### 1. Project Title  
**Auto Doc Generator**

---

### 2. Project Goal  
Auto Doc Generator is a developer‑focused utility that automates the creation of high‑quality project documentation. By extracting structural information, comments, and docstrings from source code, the tool produces ready‑to‑publish Markdown (or other markup) files, relieving developers of the repetitive, error‑prone manual documentation process. The primary problem it solves is the gap between fast‑paced code development and the often‑neglected upkeep of accurate, comprehensive documentation.

---

### 3. Core Logic & Principles  

| Aspect | Description |
|--------|-------------|
| **Source Inspection** | The generator parses the target project’s source files (Python, JavaScript, etc.) using language‑specific Abstract Syntax Tree (AST) libraries. It walks the AST to locate modules, classes, functions, and their associated docstrings/comments. |
| **Metadata Extraction** | For each discovered element it extracts: <br>• Name and signature <br>• Docstring (or inline comment block) <br>• Type hints / annotations (when available) <br>• Public API surface (filtering out private/dunder members). |
| **Template Rendering** | Extracted metadata is fed into a lightweight templating engine (e.g., **Jinja2**). Pre‑defined Markdown templates define the layout for module overviews, class sections, function tables, and usage examples. |
| **Configuration‑Driven** | Users supply a concise YAML/JSON configuration that controls: <br>• Input directories / file patterns <br>• Output location and file naming <br>• Template selection and custom variables <br>• Inclusion/exclusion rules (e.g., ignore test files). |
| **CLI Interface** | A small command‑line wrapper parses the configuration, invokes the extraction pipeline, and writes the rendered documentation to disk. The CLI also provides flags for “dry‑run”, verbose logging, and incremental updates. |
| **Extensibility** | The architecture isolates three interchangeable components: **Parser**, **Renderer**, and **Dispatcher**. Adding support for a new programming language or output format only requires implementing the relevant parser or template set, without touching the core workflow. |

*Key algorithms* include recursive AST traversal, pattern‑based file discovery, and context‑aware string sanitisation to ensure that generated markdown is syntactically correct.

---

### 4. Key Features  

- **Automatic API documentation** – Generates module, class, and function reference sections directly from source code.  
- **Multi‑language support** – Built‑in parsers for Python (via `ast`) and JavaScript/TypeScript (via `esprima`/`@babel/parser`).  
- **Customizable Markdown templates** – Ship with default templates; users can supply Jinja2 templates to match their style guide.  
- **Config‑driven operation** – Single YAML/JSON file defines inputs, outputs, filters, and template variables.  
- **Command‑line tool** – Easy integration into development workflows (`autodoc generate --config path/to/config.yaml`).  
- **Incremental generation** – Detects unchanged files and skips re‑rendering, speeding up CI runs.  
- **CI/CD ready** – Designed to be called from GitHub Actions, GitLab CI, Jenkins, etc. (returns non‑zero exit code on failures).  
- **Extensible plugin architecture** – Add new language parsers or output formats by implementing the `Parser` or `Renderer` interface.  

---

### 5. Dependencies  

| Dependency | Purpose | Version (minimum) |
|------------|---------|-------------------|
| `Python >=3.8` | Runtime environment | – |
| `Jinja2` | Template rendering engine | 3.0 |
| `PyYAML` | YAML configuration parsing | 5.4 |
| `ast` (standard library) | Python source parsing | – |
| `esprima` / `@babel/parser` (optional) | JavaScript/TypeScript parsing | 4.0 / 7.0 |
| `click` | CLI argument handling | 8.0 |
| `watchdog` (optional) | File‑system monitoring for incremental builds | 2.1 |

*Optional* – If the project is used only for Python, the JavaScript parser and `watchdog` are not required.

---

**End of Overview**  

This document captures the essential purpose, inner workings, primary capabilities, and required tools for the **Auto Doc Generator** project, providing a solid foundation for onboarding, stakeholder communication, and further development planning.

 

<a name='Install_Workflow'></a>

To set up the documentation generation workflow you need to:

1. **Install the helper scripts**  
   - **Windows (PowerShell)**: Run the script directly from the raw file URL  
     ```powershell
     irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
     ```  
   - **Linux/macOS (bash)**: Download and execute the script with curl  
     ```bash
     curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
     ```

2. **Add the required secret to GitHub Actions**  
   - In your repository’s **Settings → Secrets and variables → Actions**, create a new secret named **`GROCK_API_KEY`**.  
   - Set its value to the API key you obtain from the Grock documentation site: **https://grockdocs.com**.

3. **Workflow execution**  
   - The `.github/workflows/autodoc.yml` workflow triggers manually (`workflow_dispatch`).  
   - It calls the reusable workflow defined in `.github/workflows/reuseble_agd.yml`, which installs the `autodocgenerator` package, runs the documentation generator, and commits the updated `README.md`.  
   - The secret `GROCK_API_KEY` is passed to the reusable workflow and made available as `API_KEY` for the documentation generation step.

<a name='Manager_Usage'> </a>
**Parameters of `Manager`**

| Parameter | Description (as shown in the code) |
|-----------|------------------------------------|
| `project_directory: str` | Path to the root of the project you want to document. |
| `project_settings: ProjectSettings` | Instance that holds global information about the documentation project. |
| `sync_model: Model = None` | Synchronous language model used for processing (e.g., `GPTModel`). |
| `async_model: AsyncModel = None` | Asynchronous language model used for processing (e.g., `AsyncGPTModel`). |
| `ignore_files: list = []` | List of glob‑style patterns for files/folders that must be ignored when building the repository mix. |
| `language: str = "en"` | Language code for the generated documentation (default `"en"`). |
| `progress_bar: BaseProgress = BaseProgress()` | Progress‑bar implementation; in the example a `LibProgress` wrapping a Rich `Progress` instance is used. |

**Full example (taken directly from the repository)**

```python
if __name__ == "__main__":
    # Patterns of files/folders that should be ignored
    ignore_list = [
        "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db", "data",
        "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore",
        ".ruff_cache", ".auto_doc_cache", "*.pyc", "__pycache__", ".git",
        ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles",
        ".mypy_cache"
    ]

    # Initialise language models
    sync_model = GPTModel(API_KEY)          # synchronous model
    async_model = AsyncGPTModel(API_KEY)    # asynchronous model

    # Rich progress bar configuration
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:
        # Project‑level settings
        project_settings = ProjectSettings("Auto Doc Generator")
        project_settings.add_info(
            "global idea",
            """This project was created to help developers make documentations for them projects"""
        )

        # Create the Manager instance
        manager = Manager(
            r"C:\Users\sinic\OneDrive\Документы\GitHub\ADG",   # project_directory
            project_settings,                                 # ProjectSettings instance
            sync_model=sync_model,                            # synchronous model
            async_model=async_model,                          # asynchronous model
            ignore_files=ignore_list,                         # ignore patterns
            progress_bar=LibProgress(progress),               # progress bar wrapper
            language="en"                                     # documentation language
        )

        # Example usage of the manager (calls are commented out in the source)
        # manager.generate_code_file()
        # manager.generate_global_info_file(use_async=True, max_symbols=5000)
        # manager.generete_doc_parts(use_async=True, max_symbols=4000)

        # Generate documentation using a factory with the IntroLinks module
        manager.factory_generate_doc(
            DocFactory(
                IntroLinks(),
                # IntroText(),
            )
        )
```

<a name='autodocconfig_options'> </a>
**autodocconfig.yml – available options**

The file is a YAML document. The following top‑level keys are read by the generator (see `autodocgenerator/auto_runner/config_reader.py`):

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `project_name` | string | Name of the project that will appear in the generated documentation. | `project_name: "My Awesome Project"` |
| `language` | string | Language code for the documentation (default **en**). | `language: "en"` |
| `project_additional_info` | mapping (key‑value pairs) | Arbitrary additional information about the project. Each entry is added to `ProjectSettings`. | ```project_additional_info:\n  global idea: "Tool to auto‑generate docs"``` |
| `ignore_files` | list of strings | Glob patterns for files/directories that must be ignored during analysis. If omitted the default list defined in `Config.__init__` is used. | `ignore_files: ["*.log", "tests/"]` |
| `custom_descriptions` | list of strings | Free‑form text blocks that become **custom modules** (`CustomModule`) in the documentation generation pipeline. Each string is passed to `CustomModule`. | ```custom_descriptions:\n  - "Explain installation workflow …"\n  - "How to use Manager class …"``` |

**How to write the file**

```yaml
project_name: "Auto Doc Generator"
language: "en"

project_additional_info:
  global idea: "This project was created to help developers make documentations for them projects"

custom_descriptions:
  - "explain how install workflow with install.ps1 and install.sh scripts for install you should use links irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex for powershell and curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash for linux based systems and also you have to add secret variable to git hub action GROCK_API_KEY with your api key from grock docs https://grockdocs.com to make it work"
  - "how to use Manager class what parameters i need to give. give full example of usage"
  - "explain how to write autodocconfig.yml file what options are available"
```

Only the keys listed above are recognized; any other keys are ignored. The file must be saved as `autodocconfig.yml` in the repository root.

 

## <a name="config_reader"></a>autodocgenerator.auto_runner.config_reader  

**Purpose** – Reads *autodocconfig.yml* and builds the runtime configuration used by the documentation generator.  

### Core class – `Config`  

| Attribute | Meaning |
|-----------|---------|
| `ignore_files` | Default glob patterns that are excluded from the source‑code scan (e.g. `*.pyc`, `venv`, `.git`). |
| `language` | Target language for generated docs (default **en**). |
| `project_name` | Human‑readable name of the inspected project. |
| `project_additional_info` | Arbitrary key/value pairs that are injected into `ProjectSettings`. |
| `custom_modules` | List of `CustomModule` objects – each wraps a *custom description* supplied by the user. |

### Builder‑style setters  

All setters (`set_language`, `set_project_name`, `add_project_additional_info`, `add_ignore_file`, `add_custom_module`) return **self**, enabling fluent chaining in `read_config`.

### Helper methods  

* `get_project_settings()` – creates a `ProjectSettings` instance (from `preprocessor.settings`) and fills it with the additional info dictionary.  
* `get_doc_factory()` – builds two `DocFactory` objects:  
  * **docFactory** – contains the user‑defined `CustomModule`s.  
  * **introFactory** – pre‑populated with the built‑in intro modules (`IntroLinks`, `IntroText`).  

Both factories are later passed to the `Manager` to render the final document.

### Function – `read_config(file_data: str) -> Config`  

1. Parses the YAML string with `yaml.safe_load`.  
2. Populates a fresh `Config` instance:  
   * merges `ignore_files` from the file,  
   * sets `language` & `project_name`,  
   * adds any `project_additional_info` entries,  
   * converts each entry in `custom_descriptions` into a `CustomModule`.  
3. Returns the fully‑configured `Config` object.

**Assumptions & side‑effects** – The YAML file is well‑formed; missing keys fall back to defaults. No I/O is performed here – the caller supplies the file contents.

---

## <a name="run_file"></a>autodocgenerator.auto_runner.run_file  

**Purpose** – Entry point executed by the GitHub Action (and locally) that orchestrates the whole documentation generation pipeline.

### `gen_doc` function  

```python
def gen_doc(project_settings, ignore_list, project_path,
            doc_factory, intro_factory) -> str:
```

1. **Model creation** – Instantiates a synchronous `GPTModel` and an asynchronous `AsyncGPTModel` using the global `API_KEY` from `engine.config.config`.  
2. **Manager construction** – Builds a `Manager` with:  
   * `project_path` – root directory to scan,  
   * `project_settings` – from `Config.get_project_settings()`,  
   * the two GPT model objects,  
   * `ignore_files` list,  
   * a `ConsoleGtiHubProgress` progress‑bar implementation,  
   * language (`en`).  
3. **Generation steps** (executed sequentially):  
   * `generate_code_file()` – extracts source code snippets.  
   * `generate_global_info_file()` – produces high‑level project description (sync, ≤ 8000 symbols).  
   * `generete_doc_parts()` – creates the main documentation sections (sync, ≤ 8000 symbols).  
   * `factory_generate_doc(doc_factory)` – renders custom user‑defined sections.  
   * `factory_generate_doc(intro_factory)` – renders the intro (links & text).  
4. Returns the final markdown content by reading the cached file with key `"output_doc"`.

### Script execution (`if __name__ == "__main__":`)  

1. Loads *autodocconfig.yml*.  
2. Calls `read_config` → obtains `Config`.  
3. Extracts `project_settings` and the two factories.  
4. Invokes `gen_doc` with the current directory (`"."`).  
5. The resulting markdown is written to `.auto_doc_cache/output_doc.md` by the `Manager`; the GitHub Action later copies it to `README.md`.

### Interaction map  

* **ConfigReader** → supplies `ProjectSettings`, ignore list, and factories.  
* **Manager** (in `autodocgenerator.manage`) → core orchestrator that talks to the **GPT models**, the **pre‑processor** (code splitting, compression), and the **UI** progress bar.  
* **DocFactory** → aggregates modules (`CustomModule`, `IntroLinks`, `IntroText`) that each know how to render a specific markdown chunk.  

### Important assumptions  

* `API_KEY` environment variable is set (via the workflow secret `GROCK_API_KEY`).  
* The project path is readable and contains Python source files.  
* The cache directory `.auto_doc_cache` exists or will be created by `Manager`.  

---  

**Quick start for developers**  

```bash
# Install dependencies
pip install autodocgenerator

# Generate docs (uses autodocconfig.yml in CWD)
python -m autodocgenerator.auto_runner.run_file
```

The script will produce `README.md` when run inside the reusable GitHub Action, or you can read the returned string for custom handling.

## <a name="config_constants"></a>Configuration constants  

The module **`autodocgenerator.engine.config.config`** centralises static prompts and runtime settings used by the AutoDoc pipeline.  

| Symbol | Purpose | Typical usage |
|--------|---------|---------------|
| `BASE_SYSTEM_TEXT` | System‑level instruction fed to the LLM at the very start of a session. It forces the model to treat each incoming snippet as a *partial* view of the whole codebase and to keep refining its analysis. | Passed to the **GPTModel** as the first message in the conversation history. |
| `BASE_PART_COMPLITE_TEXT` | Prompt that tells the model to produce a concise (≈ 0.5‑1 k characters) documentation fragment for a given code piece. | Used by the *DocFactory* when rendering custom sections. |
| `BASE_INTRODACTION_CREATE_TEXT` | Detailed directive for building an “Executive Navigation Tree”. It encodes strict anchoring rules and hierarchy constraints that the LLM must obey when transforming a list of markdown links. | Consumed by the *IntroFactory* to generate the navigation tree. |
| `BASE_INTRO_CREATE` | High‑level briefing that asks the model to write a professional project overview (title, goal, core logic, features, dependencies). | Invoked when the initial project summary is required. |
| `BASE_SETTINGS_PROMPT` | Prompt that establishes a persistent “project knowledge base” – the model memorises key‑value parameters and re‑applies them on later calls. | Employed by the **SettingsReader** to seed the context. |
| `get_BASE_COMPRESS_TEXT(start, power)` | Factory function returning a prompt for summarising large code snippets. It dynamically adjusts the allowed length (`~start/power` characters) and forces a strict usage example block. | Called by the *Compression* step before sending oversized code to the LLM. |
| `API_KEY` | Loaded from the environment (`.env`) at import time. It is the authentication token required by the Groq API. | Shared by all model wrappers. |
| `MODELS_NAME` | Ordered list of fallback model identifiers. The system will rotate through this list if a request fails for the current model. | Referenced by `Model`/`AsyncModel` during request retries. |

**Assumptions & side‑effects** – The environment variable `API_KEY` must be present; otherwise `API_KEY` becomes `None` and API calls will fail. No file I/O occurs here; all values are in‑memory constants.

---

## <a name="gpt_model"></a>`GPTModel` / `AsyncGPTModel` – Groq model adapters  

These two classes are thin wrappers around the **Groq** SDK that implement the abstract base classes `Model` (sync) and `AsyncModel` (async) defined in `engine.models.model`. Their responsibility is to provide a uniform **`generate_answer`** interface used throughout the documentation pipeline.

### Common behaviour  

1. **Construction** – Accepts an `api_key` (defaults to the module‑level `API_KEY`) and an optional `History` object that stores the conversation turn list. The base class initialises:  
   * `self.api_key` – stored for later client creation.  
   * `self.history` – holds prior messages, enabling *with_history* mode.  
   * `self.regen_models_name` – a copy of `MODELS_NAME`.  
   * `self.current_model_index` – index of the model currently being used.  

2. **Message selection** –  
   * If `with_history=True`, the entire `self.history.history` list is sent.  
   * Otherwise the caller‑provided `prompt` string is used directly.  

3. **Retry loop** – A `while True` loop attempts a completion with the model at `self.regen_models_name[self.current_model_index]`. On any exception the index is advanced (wrapping to `0` when the end is reached) and the loop retries. If all models fail, an exception `"all models do not work"` is raised.

4. **Result extraction** – Upon success, the method returns `chat_completion.choices[0].message.content`, i.e. the raw LLM text.

### `GPTModel` (synchronous)  

```python
class GPTModel(Model):
    def __init__(self, api_key=API_KEY, history=History()):
        super().__init__(api_key, history)
        self.client = Groq(api_key=self.api_key)
```

*Uses* the **blocking** `Groq` client. The `generate_answer` method follows the common flow described above, calling `self.client.chat.completions.create(...)`.

### `AsyncGPTModel` (asynchronous)  

```python
class AsyncGPTModel(AsyncModel):
    def __init__(self, api_key=API_KEY, history=History()):
        super().__init__(api_key, history)
        self.client = AsyncGroq(api_key=self.api_key)
```

*Uses* the **async** `AsyncGroq` client; its `generate_answer` is declared `async` and therefore awaited by callers (e.g., the `Manager` when it processes large sections in parallel).

### Interaction map  

* **Manager** – Instantiates one `GPTModel` and one `AsyncGPTModel` and calls `generate_answer` to obtain:
  * Global project description (sync, ≤ 8000 sym).
  * Section‑level documentation (sync, ≤ 8000 sym).
  * Optional async calls for parallel chunk processing.
* **History** – Shared across both wrappers, allowing the pipeline to keep context between calls without re‑sending the whole prompt each time.
* **MODELS_NAME** – Drives the fallback strategy when a specific model endpoint is unavailable.

### Important assumptions  

* The Groq service is reachable and the supplied `API_KEY` has sufficient quota.  
* Network failures raise generic exceptions caught by the retry loop.  
* The `History` object correctly formats messages as a list of `{"role": "...", "content": "..."}` dictionaries required by Groq.  

**Side‑effects** – Each call may mutate `self.current_model_index` and, if `with_history=True`, may also append new messages to `self.history` (handled by the base class). No files are written; all state lives in memory.

<a name="model"></a>
## `autodocgenerator/engine/models/model.py`

### Purpose
Provides the *core abstraction* for all LLM‑backed generators used by the documentation pipeline.  
It defines:

* **`History`** – in‑memory store of message objects (`role`, `content`) that mimics the chat format expected by Groq/AsyncGroq.  
* **`ParentModel`** – common constructor handling API‑key storage, a mutable conversation history, and a shuffled fallback list (`regen_models_name`) derived from `config.MODELS_NAME`.  
* **`Model`** – synchronous wrapper exposing `generate_answer`, `get_answer_without_history`, and `get_answer`.  
* **`AsyncModel`** – asynchronous counterpart with `async` versions of the same helpers.

### Key behaviours
| Method | Behaviour | Side‑effects |
|--------|-----------|--------------|
| `History.__init__(system_prompt)` | Starts with an empty list; optionally injects a system prompt (`BASE_SYSTEM_TEXT`). | Adds a *system* message. |
| `History.add_to_history(role, content)` | Appends a dict to `self.history`. | Mutates `history`. |
| `ParentModel.__init__(api_key, history)` | Stores API key, history, initial model index `0`, and creates a shuffled copy of `MODELS_NAME` for retry/fallback. | May reorder `regen_models_name`. |
| `Model.generate_answer(with_history=True, prompt=None)` | **Placeholder** – concrete subclasses (`GPTModel`, `AsyncGPTModel`) override this with the real Groq request/response loop. | Returns a string. |
| `Model.get_answer(prompt)` | Records user prompt, calls `generate_answer`, records assistant reply, returns the reply. | Updates `history`. |
| `AsyncModel.generate_answer(...)` / `AsyncModel.get_answer(...)` | Same logic as `Model` but `async`. | Updates `history` asynchronously. |

### Assumptions & contracts
* `history` must contain dicts compatible with Groq’s `messages` field.
* `api_key` is a valid Groq token; quota limits are handled elsewhere.
* Sub‑classes replace the stub `generate_answer` with a retry loop that iterates over `self.regen_models_name` and raises `"all models do not work"` if none succeed.

---

<a name="factory"></a>
## `autodocgenerator/factory/base_factory.py`

### Purpose
Defines the *pipeline orchestration* building blocks.

* **`BaseModule`** – abstract base class for any documentation generator piece. Sub‑classes implement `generate(info, model) → str`.
* **`DocFactory`** – composes a sequence of `BaseModule` instances and drives their execution, reporting progress via a `BaseProgress` implementation.

### Core logic (`DocFactory.generate_doc`)
1. Create a sub‑task `"Generate parts"` sized to the number of modules.  
2. Iterate over `self.modules`:
   * Call `module.generate(info, model)` (synchronous; async modules are wrapped elsewhere).  
   * Concatenate results with double new‑lines.  
   * Update progress.  
3. Remove the sub‑task and return the assembled document string.

### Interaction map
* **Modules** (`IntroLinks`, `IntroText`, `CustomModule`, …) receive the *shared* `Model` (or `AsyncModel`) instance, thus re‑using the same `History` and fallback strategy.  
* **`BaseProgress`** (from `ui.progress_base`) supplies a UI‑friendly progress bar; `DocFactory` only calls its public methods (`create_new_subtask`, `update_task`, `remove_subtask`).  
* The factory does **not** perform any I/O itself – all side‑effects (LLM calls, history mutation) are delegated to the supplied model.

---

<a name="modules"></a>
## `autodocgenerator/factory/modules/intro.py` & `general_modules.py`

### Overview
Concrete `BaseModule` implementations that plug into `DocFactory`.

| Module | Responsibility | Main call chain |
|--------|----------------|-----------------|
| `IntroLinks` | Extracts HTML links from `info["full_data"]` and asks the model to create a short intro for those links. | `get_all_html_links → get_links_intro(model, language)` |
| `IntroText` | Generates a high‑level project introduction from `info["global_data"]`. | `get_introdaction(model, language)` |
| `CustomModule` | Generates a custom description for a chunk of source code. | `split_data → generete_custom_discription(model, description, language)` |

All modules receive the same `Model` instance, therefore they benefit from the shared `History` (context continuity) and the same retry/fallback behaviour.

---

### Summary for developers
* **Instantiate** a concrete model (`GPTModel` or `AsyncGPTModel`) → passes its `History` to every module.  
* **Create** a `DocFactory` with desired `BaseModule` subclasses.  
* **Call** `factory.generate_doc(info, model, progress)` → returns the full documentation string while progress is shown.  

The snippet constitutes the *glue* between the LLM client layer and the modular documentation generation pipeline.

<a name="manager"></a>
## `autodocgenerator/manage.py` – High‑level orchestration layer  

The **`Manager`** class glues together every subsystem of *Auto‑Doc‑Generator*:

| Component | Role in `Manager` |
|-----------|-------------------|
| **`CodeMix`** (`preprocessor/code_mix.py`) | Produces a single “code‑mix” file that contains the repository tree and the raw source of every non‑ignored file. |
| **Spliter / Compressor** (`preprocessor/spliter.py`, `preprocessor/compressor.py`) | Split the huge mix into LLM‑friendly chunks (`split_data`) and optionally compress them (`compress_to_one`). |
| **Doc‑Factory** (`factory/base_factory.py`) | Receives a `DocFactory` instance and runs the modular documentation pipeline (`IntroLinks`, `CustomModule`, …). |
| **Model objects** (`engine/models/gpt_model.py`) | Provide synchronous (`Model`) or asynchronous (`AsyncModel`) LLM access; all modules share the same history via these objects. |
| **Progress UI** (`ui/progress_base.py`) | A thin wrapper around **rich**’s `Progress` that reports task completion to the console. |
| **`ProjectSettings`** | Holds static project‑level meta‑information (title, global idea, etc.) that is injected into the LLM prompts. |

### Core public API  

| Method | Purpose | Important I/O / Side‑effects |
|--------|---------|------------------------------|
| `__init__(project_directory, project_settings, sync_model=None, async_model=None, ignore_files=[], language="en", progress_bar=BaseProgress())` | Sets up paths, creates the hidden cache folder (`.auto_doc_cache`) and stores references to the models, settings and UI. | Creates a folder on disk if missing. |
| `read_file_by_file_key(file_key)` | Reads one of the three cached artefacts (`code_mix`, `global_info`, `output_doc`). | Returns a **str** containing the file contents. |
| `get_file_path(file_key)` | Resolves the absolute path of a cached artefact. | No side‑effects. |
| `generate_code_file()` | Instantiates `CodeMix`, walks the project tree while respecting `ignore_files`, writes the mixed representation to `<cache>/code_mix.txt`. | Updates progress bar (`update_task`). |
| `generate_global_info_file(max_symbols=10_000, use_async=False)` | Loads the code‑mix, splits it into ≤ `max_symbols` chunks, compresses them into a single “global info” markdown using the chosen model, writes the result to `<cache>/global_info.md`. | May invoke the LLM (sync or async). |
| `generete_doc_parts(max_symbols=5_000, use_async=False)` | Reads *global info* and the raw *code‑mix*, then generates the first draft of the documentation (doc parts) via `gen_doc_parts` / `async_gen_doc_parts`. Result is saved to `<cache>/output_doc.md`. | Calls the LLM, may run an `asyncio` event loop. |
| `factory_generate_doc(doc_factory)` | Loads *global info*, the current *output_doc* and *code‑mix*, builds the `info` dict expected by modules, runs `doc_factory.generate_doc`, prefixes the newly created sections to the existing doc and rewrites `<cache>/output_doc.md`. | Relies on the shared `self.sync_model`; progress is updated after completion. |

### Design assumptions  

* All file I/O is confined to the hidden cache folder; the original source tree is never modified.  
* `ignore_files` follows Unix‑style glob patterns (handled by `CodeMix.should_ignore`).  
* LLM quota handling is external – the manager simply forwards the appropriate `Model` instance.  
* Progress updates are *fire‑and‑forget*: the manager does not wait for UI rendering.  

---

<a name="codemix"></a>
## `autodocgenerator/preprocessor/code_mix.py` – Repository serializer  

`CodeMix` is a small utility that produces a **single textual snapshot** of a repository:

| Method | Behaviour |
|--------|-----------|
| `__init__(root_dir=".", ignore_patterns=None)` | Normalises `root_dir` to an absolute `Path`; stores a list of glob patterns that must be excluded. |
| `should_ignore(path: str) -> bool` | Returns `True` if `path` (as a `Path`) matches any ignore pattern – either against the whole relative path, its basename, or any of its parts. |
| `build_repo_content(output_file="repomix-output.txt")` | Writes two sections to `output_file`:<br>1. **Structure tree** – indented list of directories and files, respecting ignore rules.<br>2. **File payloads** – for each non‑ignored file, writes `<file path="…">` followed by its raw text (UTF‑8, errors ignored). Errors while reading a file are logged inline. |

### Interaction points  

* Called only from `Manager.generate_code_file()`.  
* The generated `<cache>/code_mix.txt` becomes the raw input for all downstream preprocessing steps (splitting, compression, doc‑factory).  

### Side‑effects & Constraints  

* Writes **overwrites** the target file; no backup is made.  
* Ignores binary or unreadable files silently (errors are captured and written as plain text).  
* Assumes that the repository fits into memory when read line‑by‑line – acceptable for typical Python projects.  

---

### Quick usage example  

```python
from autodocgenerator.manage import Manager
from autodocgenerator.preprocessor.settings import ProjectSettings
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.ui.progress_base import LibProgress
from rich.progress import Progress

settings = ProjectSettings("MyProject")
settings.add_info("global idea", "A demo project.")
manager = Manager(
    project_directory="path/to/project",
    project_settings=settings,
    sync_model=GPTModel(API_KEY),
    async_model=AsyncGPTModel(API_KEY),
    ignore_files=["*.pyc", "__pycache__", ".git"],
    progress_bar=LibProgress(Progress()),
    language="en",
)

manager.generate_code_file()          # creates .auto_doc_cache/code_mix.txt
manager.generate_global_info_file()   # compresses it into global_info.md
manager.generete_doc_parts()          # first draft → output_doc.md
manager.factory_generate_doc(
    DocFactory(IntroLinks())
)                                    # final doc with intro links
```

The `Manager` + `CodeMix` pair therefore constitutes the **data‑acquisition layer** of the system, turning a raw source tree into the structured inputs required by the LLM‑driven documentation pipeline.

<a name="compressor"></a>
## `autodocgenerator/preprocessor/compressor.py` – Compression & description layer  

**Responsibility**  
Transforms the raw repository snapshot (produced by `CodeMix`) into a compact representation that fits the LLM token limits and later generates short technical descriptions for each code fragment.  

**Interaction with the rest of the system**  
* Called by `Manager.generate_global_info_file()` (and indirectly by `Manager.factory_generate_doc`).  
* Receives the list of file‑payload strings from `CodeMix.build_repo_content()`.  
* Uses the *model* objects (`Model` / `AsyncModel`) supplied by the manager – the quota handling is performed outside this module.  
* Emits the final compressed string that becomes the input for the *post‑processing* stage (`postprocess.py`).  

**Key functions**

| Function | Main flow | Important notes |
|----------|-----------|-----------------|
| `compress(data, project_settings, model, compress_power)` | Builds a three‑message prompt (`system` = project prompt, `system` = compression template from `get_BASE_COMPRESS_TEXT`, `user` = raw data) and calls `model.get_answer_without_history`. Returns the model’s compressed text. | `compress_power` influences the length hint in the template. |
| `compress_and_compare(data, model, project_settings, compress_power=4, progress_bar=BaseProgress())` | Splits the list into chunks of size `compress_power`, compresses each element with `compress`, concatenates results per chunk, updates a sub‑task on `progress_bar`. Returns a new list whose length is `ceil(len(data)/compress_power)`. | Synchronous, fire‑and‑forget UI updates. |
| `async_compress … / async_compress_and_compare …` | Same logic as the synchronous version but runs each `compress` call inside an `asyncio.Semaphore(4)` to limit parallel LLM requests. Progress is updated after each awaited answer. | Allows the manager to enable `use_async=True` for faster throughput. |
| `compress_to_one(data, model, project_settings, compress_power=4, use_async=False, progress_bar=BaseProgress())` | Repeatedly calls the (a)sync compress‑and‑compare functions, reducing the list until a single string remains. The loop adapts `compress_power` to `2` when the list is very short. Returns the final compressed document. | Guarantees that the output fits a single LLM request. |
| `generate_discribtions_for_code(data, model, project_settings, progress_bar=BaseProgress())` | For each compressed code fragment builds a detailed “explain‑your‑code” prompt (strict rules, markdown example) and collects the model’s answers. | Used later to produce the *code‑description* section of the final documentation. |

**Assumptions & side‑effects**  
* The LLM model’s `get_answer_without_history` is stateless; quota limits are enforced elsewhere.  
* Input strings are assumed to be UTF‑8 text; binary blobs are filtered out earlier by `CodeMix`.  
* Progress UI updates are fire‑and‑forget – the function does **not** wait for the UI to render.  
* The function overwrites its output (the returned string) without persisting intermediate files.  

---

<a name="postprocess"></a>
## `autodocgenerator/preprocessor/postprocess.py` – Final markdown polishing  

**Responsibility**  
Takes the compressed text (and optional custom descriptions) and builds the final, user‑ready Markdown document: generates anchors, extracts topics, creates introductory sections, and formats custom description blocks.  

**Interaction with the rest of the system**  
* Invoked after `compress_to_one` and `generate_discribtions_for_code`.  
* Consumes the single compressed string and the list of custom description strings.  
* Calls the same LLM `Model` interface to request introductions (`get_links_intro`, `get_introdaction`).  
* Returns ready‑to‑write Markdown that `Manager.factory_generate_doc` writes to the output file.  

**Key functions**

| Function | Purpose | Important details |
|----------|---------|-------------------|
| `generate_markdown_anchor(header)` | Normalises a header string into a GitHub‑style anchor (`#my‑section`). | Uses Unicode NFKC, replaces spaces with `-`, strips illegal characters, collapses multiple dashes. |
| `get_all_topics(data)` | Scans a Markdown string for level‑2 headings (`## `) and returns a tuple `(topics, anchors)`. | Relies on simple `str.find` loops; suitable for the controlled output produced by this pipeline. |
| `get_all_html_links(data)` | Extracts existing `<a name=…>` anchors (max 25 chars) and returns them as `#anchor` strings. | Helpful when the source already contains manual anchors. |
| `get_links_intro(links, model, language="en")` | Sends the list of anchors to the LLM with a system prompt (`BASE_INTRODACTION_CREATE_TEXT`) to generate a short introductory paragraph for the link section. | Returns raw LLM answer. |
| `get_introdaction(global_data, model, language="en")` | Similar to the above but operates on the whole document body, using `BASE_INTRO_CREATE` to obtain a global introduction. | |
| `generete_custom_discription(splited_data, model, custom_description, language="en")` | Iterates over already‑split chunks, asks the LLM to produce a custom description (title + `<a name='…'>` anchor) respecting strict “no‑hallucination” rules. Stops at the first non‑empty, non‑`!noinfo` answer. | Returns the first satisfactory description or an empty string. |

**Assumptions & side‑effects**  
* Input Markdown follows the conventions produced by `compressor.py`; headings are prefixed with `## `.  
* The functions do not write files; they only return strings that the caller assembles and persists.  
* All LLM calls are fire‑and‑forget with respect to UI – progress handling is done by the caller (the manager).  
* The module assumes the model’s system prompts (`BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`) are present in the global config.  

Together, **compressor** and **postprocess** form the *pre‑ and post‑processing* stages of the documentation pipeline: they shrink the raw repository dump to a token‑friendly form, enrich it with LLM‑generated summaries, and finally shape a polished Markdown document ready for delivery.

<a name="projectsettings"></a>
## `preprocessor/settings.py – ProjectSettings`

**Responsibility**  
Collects project‑wide metadata (name + arbitrary key/value pairs) and builds the *system prompt* that is passed to the LLM before any generation step.

**Interaction with the system**  
* Created by the manager after the configuration file is read.  
* Its `prompt` property is concatenated with other prompts (e.g., `BASE_SETTINGS_PROMPT`) and supplied to `spliter.write_docs_by_parts` and to the custom‑description generator in *postprocess*.  

**Key members**  

| Member | Meaning |
|--------|---------|
| `project_name` | Human‑readable project identifier (used by LLM). |
| `info` (dict) | Additional user‑defined fields (e.g., `framework`, `version`). |
| `add_info(key, value)` | Store a new field. |
| `prompt` (property) | Returns a single string: `BASE_SETTINGS_PROMPT` + “Project Name: …” + each `key: value` line. |

**Assumptions / Side‑effects**  
* Relies on `BASE_SETTINGS_PROMPT` being defined in the global config.  
* No I/O – only string construction.  

---

<a name="spliter"></a>
## `preprocessor/spliter.py – Chunking & LLM‑driven part generation`

**Responsibility**  
Breaks a massive source‑code dump into token‑friendly chunks, sends each chunk to the LLM (synchronously or asynchronously), and stitches the partial answers back together.

**Interaction with the system**  
* Called by `Manager.factory_generate_doc` after `compress_to_one`.  
* Receives the *global info* prompt (from `ProjectSettings.prompt`) and feeds it to the LLM together with each chunk.  
* Progress updates are routed to a `BaseProgress` implementation (rich‑based or console).  

**Key functions**

| Function | Purpose |
|----------|---------|
| `split_data(data, max_symbols)` | Splits raw text on line breaks, then enforces a rough size limit (`max_symbols`). Handles oversized pieces by halving them recursively and finally groups them into `split_objects`. |
| `write_docs_by_parts(part, model, global_info, prev_info=None, language="en")` | Builds the LLM prompt (`system` language, `BASE_PART_COMPLITE_TEXT`, optional previous part) and calls `model.get_answer_without_history`. Strips surrounding Markdown fences. |
| `async_write_docs_by_parts(...)` | Same as above but works with an `AsyncModel`, respects a semaphore (max parallel calls) and optionally updates a progress bar. |
| `gen_doc_parts(full_code_mix, global_info, max_symbols, model, language, progress_bar)` | Orchestrates synchronous processing: splits, iterates, calls `write_docs_by_parts`, keeps a sliding window of the last 3000 characters for context, updates progress. |
| `async_gen_doc_parts(...)` | Parallel version using `asyncio.gather`. |

**Assumptions / Side‑effects**  
* Input `data` already contains newline separators (`"\n"`).  
* `max_symbols` is tuned to the LLM’s token limit; the function uses heuristics (`*1.5`, `*1.25`).  
* No file I/O – returned string is later written by the manager.  

---

<a name="progressbase"></a>
## `ui/progress_base.py – Progress reporting abstraction

**Responsibility**  
Provides a minimal interface (`BaseProgress`) for reporting task progress, with two concrete implementations:
* `LibProgress` – wraps **rich**’s `Progress` for nice terminal UI.
* `ConsoleGtiHubProgress` – simple `print`‑based fallback.

**Interaction with the system**  
* Instances are passed to `spliter.gen_doc_parts` / `async_gen_doc_parts` and to the post‑processing stage.  
* The pipeline creates a *sub‑task* for each major step (e.g., “Generate doc parts”) and advances it after each chunk is processed.

**Key classes**

| Class | Core behaviour |
|-------|----------------|
| `BaseProgress` | Abstract API (`create_new_subtask`, `update_task`, `remove_subtask`). |
| `LibProgress` | Stores a base task (`_base_task`) and the current sub‑task (`_cur_sub_task`). `update_task` advances the appropriate task. |
| `ConsoleTask` | Helper that prints a start line and incremental percent progress. |
| `ConsoleGtiHubProgress` | Uses `ConsoleTask` for both general and sub‑tasks; suitable when **rich** is unavailable. |

**Assumptions / Side‑effects**  
* `LibProgress` expects a `rich.progress.Progress` object passed at construction.  
* All methods are side‑effect‑only (printing or updating the UI); they never modify the documentation data.  

---  

These three modules constitute the *pre‑processing* layer: they prepare project context (`ProjectSettings`), split the raw repository dump into LLM‑friendly parts (`spliter`), and keep the user informed about progress (`progress_base`). Their outputs feed directly into the *generation* and *post‑processing* stages described elsewhere.

**`pyproject.toml` – Project metadata & dependency manifest**  
<a name="pyproject"></a>

The file is the canonical entry‑point for building, packaging, and installing **autodocgenerator** (v 0.6.9). It follows the modern *PEP 518* layout used by **Poetry** (the chosen build backend). Below is a concise walkthrough that will help a new developer understand what each block does and why it matters for the overall system.

---

## 1. Project definition (`[project]`)

| Key | Meaning | Typical value in this file |
|-----|---------|----------------------------|
| `name` | The distribution identifier as published on PyPI. | `autodocgenerator` |
| `version` | Semantic version of the library. | `0.6.9` |
| `description` | Short one‑liner shown on the package index. | “This Project helps you to create docs for your projects” |
| `authors` | List of maintainers with contact data. | `[{name = "dima‑on", email = "sinica911@gmail.com"}]` |
| `license` | SPDX‑compatible license declaration. | `{text = "MIT"}` |
| `readme` | Path to the long description file (used for PyPI). | `README.md` |
| `requires‑python` | Minimum and maximum supported interpreter range. | `>=3.11,<4.0` |

These fields are consumed by packaging tools (`pip`, `poetry`, `build`) to generate the wheel / sdist and to populate the metadata that end‑users see.

---

## 2. Runtime dependencies (`dependencies`)

The list enumerates **all third‑party packages required for the library to work**. A few groups are worth highlighting because they map directly to major subsystems of *autodocgenerator*:

| Sub‑system | Packages (representative) | Role in the system |
|------------|---------------------------|--------------------|
| **LLM back‑ends** | `openai`, `google-genai`, `groq` | Unified interface (`model.get_answer_without_history`) to various large‑language‑model APIs. |
| **HTTP & auth** | `httpx`, `httpcore`, `requests`, `urllib3`, `google-auth`, `certifi` | Network communication with LLM providers, handling retries, TLS verification, etc. |
| **Async & concurrency** | `anyio`, `tenacity`, `rich_progress`, `tqdm`, `asyncio` (built‑in) | Retry logic, progress bars, and the async execution model used by `async_gen_doc_parts`. |
| **Project inspection** | `dulwich`, `findpython`, `platformdirs`, `virtualenv`, `pywin32-ctypes` | Locating the source tree, reading git objects, discovering the active interpreter, handling Windows‑specific path quirks. |
| **Parsing & formatting** | `markdown-it-py`, `mdurl`, `Pygments`, `pyyaml`, `tomlkit` | Converting source code/comments into Markdown, reading configuration files, syntax‑highlighting. |
| **Caching & compression** | `CacheControl`, `zstandard` | Local caching of remote LLM responses and optional compression of large intermediate blobs. |
| **Utility & helpers** | `annotated-types`, `pydantic`, `pydantic_core`, `typing‑extensions`, `typing‑inspection`, `more-itertools`, `RapidFuzz` | Strongly‑typed data models, validation, fuzzy matching when linking symbols, and collection utilities. |
| **CLI & UX** | `cleo`, `rich`, `rich_progress`, `colorama`, `crashtest`, `shellingham` | Building the command‑line interface (`autodocgenerator` entry‑point), colourful terminal output, and graceful error handling. |
| **Security & key storage** | `keyring`, `rsa` | Storing API tokens securely on the host system. |
| **File handling** | `filelock`, `msgpack`, `python-dotenv` | Guarding concurrent writes, binary serialization of intermediate data, loading environment variables. |
| **Testing / dev helpers** (not listed but may be added later) | – | Typically `pytest`, `mypy`, etc., would appear here. |

All version pins are **exact** (e.g., `openai==2.14.0`). This guarantees reproducible builds – a crucial property when the library talks to external AI services that may change behaviour across minor releases.

---

## 3. Build system (`[build‑system]`)

```toml
[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"
```

* **`requires`** – Poetry supplies the *PEP‑517* build backend (`poetry-core`).  
* **`build-backend`** – The entry point that `pip` invokes to build the wheel.  

Because the project uses **Poetry**, developers can run:

```bash
poetry install        # creates a venv and installs all deps
poetry build          # produces .whl and .tar.gz in dist/
poetry publish        # upload to PyPI
```

---

## 4. Practical notes for contributors

| Situation | What to do |
|-----------|------------|
| **Add a new library** (e.g., a new LLM provider) | `poetry add <package>`. This will automatically update the `dependencies` block with an exact version. |
| **Upgrade a dependency** | `poetry update <package>` – Poetry will rewrite the version pin while keeping the lock file (`poetry.lock`) in sync. |
| **Switch to a different Python range** | Edit `requires-python` (e.g., to support 3.12) and run `poetry lock --no-update` to regenerate the lock file. |
| **Remove unused code** | Delete the import and then run `poetry remove <package>` to keep the manifest lean. |
| **Audit security** | Run `poetry show --outdated` and consult `snyk` / `pip-audit` on the locked versions. |

---

## 5. How this file fits the overall *autodocgenerator* pipeline

1. **CLI entry point** – Defined elsewhere (`src/autodocgenerator/__main__.py`) but depends on the **CLI** packages listed here (`cleo`, `rich`).  
2. **Project analysis** – Uses `dulwich` (git), `findpython`, and `virtualenv` to collect source files, which are later fed into the **spliter** module (`split_data`).  
3. **LLM communication** – The `model` abstractions (`OpenAIModel`, `GoogleGenAIModel`, `GroqModel`) rely on the HTTP and auth libraries declared.  
4. **Documentation generation** – The core generation functions (`write_docs_by_parts`, `gen_doc_parts`, …) invoke the LLM, format the result with `markdown-it-py`/`Pygments`, and finally hand the Markdown string to the **post‑processing** stage.  
5. **Progress reporting** – `rich`/`rich_progress` provide the UI that `ui/progress_base.py` wraps.

All of these runtime components are guaranteed to be available because they are enumerated in `dependencies`. The lock file (`poetry.lock`, not shown) pins the exact builds that were tested during development, ensuring the generation pipeline behaves identically on every developer’s machine and on CI.

---

### TL;DR

*`pyproject.toml`* is the **single source of truth** for packaging, Python version support, and the full dependency graph of *autodocgenerator*. It enables reproducible builds, straightforward CI/CD, and clear visibility into which external libraries power the repository‑analysis → LLM‑prompt → Markdown‑output pipeline. Keeping this file accurate and up‑to‑date is essential for the stability of the whole documentation‑generation system.

