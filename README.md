## Executive Navigation Tree
- 📂 Core Engine
  - [manager_usage](#manager_usage)
  - [autodocgenerator__init__](#autodocgenerator__init__)
  - [config_reader](#config_reader)
  - [run_file](#run_file)

- ⚙️ Model Layer
  - [model-base](#model-base)
  - [gpt-model](#gpt-model)

- 🏭 Factory
  - [factory-init](#factory-init)
  - [base-factory](#base-factory)

- 📦 Modules
  - [custom-module](#custom-module)
  - [intro-modules](#intro-modules)
  - [code-mix](#code-mix)

- 🔧 Processing
  - [compressor](#compressor)
  - [postprocess](#postprocess)
  - [spliter](#spliter)

- 🖥️ UI
  - [ui.progress_base](#ui.progress_base)

**Project Overview – Auto Doc Generator**

---

### 1. Project Title
**Auto Doc Generator** – Automated Documentation Engine for Software Projects  

---

### 2. Project Goal
Auto Doc Generator is a developer‑centric tool that **automatically produces high‑quality documentation** (README files, API references, design overviews, etc.) for any codebase. By extracting structural information, code comments, and project metadata, then feeding it to a configurable Large Language Model (LLM), the tool eliminates the repetitive, time‑consuming manual writing of documentation while ensuring consistency, completeness, and up‑to‑date content.

---

### 3. Core Logic & Principles  

| Layer | Responsibility | Key Classes / Concepts | How It Works |
|-------|----------------|------------------------|--------------|
| **Configuration** | Holds global settings, paths, and runtime flags. | `Config` | Parses a YAML/JSON file, validates required keys, and provides a singleton‑style access point for downstream components. |
| **Project Settings** | Derives project‑specific data (language, entry point, doc format). | `ProjectSettings` | Reads the project’s `pyproject.toml`, `package.json`, or similar manifests; infers language, module structure, and user‑defined documentation preferences. |
| **LLM Engine** | Interfaces with the language model that generates natural‑language text. | `Model` (synchronous) / `AsyncModel` (asynchronous) | Wraps OpenAI, Anthropic, or locally‑hosted LLM APIs; abstracts request building, token limits, and retry logic. |
| **Factories** | Transforms raw generation results into concrete documentation files. | `DocFactory`, `LibProgress` | `DocFactory` knows the target format (Markdown, reStructuredText, HTML) and assembles sections; `LibProgress` tracks and reports generation progress. |
| **Manager** | Orchestrates the end‑to‑end pipeline. | `Manager` | Calls the pipeline steps in the correct order, handles errors, and ensures each component receives the data it expects. |
| **CLI** | User‑facing entry point. | `cli.py` (uses `argparse`/`click`) | Parses command‑line arguments, loads `Config`, instantiates `Manager`, and starts the generation flow. |

#### Pipeline Steps (as executed by the `Manager`)

1. **`generate_code_file`** – Scans the source tree, parses modules (using `ast` for Python, `ts-morph` for TypeScript, etc.), and extracts signatures, docstrings, and inline comments. The result is a structured representation of the codebase.  
2. **`generate_global_info_file`** – Collects project‑wide metadata (name, version, license, contributors), reads the `README` template if present, and builds a high‑level overview object.  
3. **`generete_doc_parts`** – Sends the code‑structure and global‑info objects to the LLM engine. The engine is prompted with carefully crafted system prompts that guide it to produce concise, accurate sections (e.g., *Module Overview*, *Class/API Reference*, *Usage Examples*, *Installation Instructions*).  
4. **`factory_generate_doc`** – Receives the raw textual fragments, passes them through `DocFactory` which formats them according to the target documentation style, inserts tables of contents, code fences, and cross‑references. The final files are written to the output directory.  

**Design Principles**

* **Separation of Concerns** – Each layer has a single, well‑defined responsibility, making the system easy to test and extend.  
* **Pluggable LLM Back‑ends** – The `Model` abstraction allows swapping providers or running a local inference server without touching the rest of the code.  
* **Asynchronous Processing** – `AsyncModel` enables parallel prompt calls, drastically reducing generation time for large projects.  
* **Progress Visibility** – `LibProgress` provides real‑time feedback (percentage, current step) in the CLI, improving UX for long runs.  
* **Configurability** – All paths, prompts, and output formats are driven by the `Config` file, allowing per‑project customisation without code changes.  

---

### 4. Key Features
- **Zero‑manual documentation** – Generate README, API reference, and design docs with a single command.  
- **Multi‑language support** – Built‑in parsers for Python, JavaScript/TypeScript, and easy extension points for additional languages.  
- **Customizable prompts & templates** – Tailor LLM instructions and output format (Markdown, reST, HTML) via the configuration file.  
- **Synchronous & asynchronous LLM calls** – Choose between fast, blocking generation or parallel, non‑blocking execution.  
- **Progress tracking & logging** – Real‑time CLI progress bar and detailed log file for debugging.  
- **Extensible factory system** – Add new documentation sections (e.g., security considerations, changelog) by implementing additional factory methods.  
- **CLI with sensible defaults** – Simple command line interface (`autodoc generate --project ./my-app`) that auto‑detects settings.  
- **Error resilience** – Automatic retries on transient LLM failures, graceful fallback to partial documentation.  

---

### 5. Dependencies
| Category | Library / Tool | Purpose |
|----------|----------------|---------|
| **Core Language** | Python ≥ 3.9 | Runtime environment |
| **CLI** | `click` (or `argparse`) | Command‑line parsing |
| **Configuration** | `PyYAML` or `jsonschema` | Load & validate `config.yaml` |
| **Code Parsing** | `ast` (standard), `typed‑ast`, `ts‑morph` (for TS) | Extract signatures/comments |
| **LLM Integration** | `openai` SDK, `anthropic` SDK, or `transformers` (for local models) | Communicate with LLM back‑ends |
| **Async Support** | `aiohttp`, `asyncio` | Non‑blocking HTTP requests |
| **Progress Reporting** | `tqdm` or custom `LibProgress` | Visual progress bar |
| **Testing** | `pytest`, `pytest‑asyncio` | Unit & integration tests |
| **Formatting** | `markdown-it-py`, `docutils` (for reST) | Render final documentation |
| **Packaging** | `setuptools` / `poetry` | Distribution of the tool |

*Optional* (for CI/CD integration):
- `pre-commit` hooks to automatically run the generator before each release.
- `GitHub Actions` workflow templates for automated documentation updates.

---

**End of Overview**  

Feel free to ask for deeper technical details, code snippets for extending a particular layer, or guidance on integrating the generator into your CI pipeline.

 

<a name='install_workflow'>To install the workflow, run the appropriate script for your platform:

- **Windows (PowerShell)**  
  ```powershell
  irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
  ```

- **Linux/macOS (bash)**  
  ```bash
  curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
  ```

After installing, add a secret variable **GROCK_API_KEY** to your GitHub Actions settings. Use the API key obtained from the Grock documentation at <https://grockdocs.com>. This secret is required for the documentation generation workflow to function correctly.</a>

<a name='manager_usage'></a>

**Manager Class – Parameters**

| Parameter | Description (based on usage) |
|-----------|------------------------------|
| `project_path` | Path to the root of the project you want to document (e.g., `"."` for current directory). |
| `project_settings` | An instance of `ProjectSettings` that contains the project name and any additional info. |
| `sync_model` | Synchronous GPT model instance (`GPTModel`) used for generating documentation. |
| `async_model` | Asynchronous GPT model instance (`AsyncGPTModel`). |
| `ignore_files` | List of glob patterns for files/folders that should be ignored during processing. |
| `progress_bar` | An object implementing progress reporting, created here with `LibProgress(progress)`. |
| `language` | Language code for the generated documentation (e.g., `"en"`). |

**Full Example of Usage**

```python
from autodocgenerator.manage import Manager
from autodocgenerator.preprocessor.settings import ProjectSettings
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.ui.progress_base import LibProgress
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

# 1. Prepare project settings (normally created via autodocconfig.yml)
project_settings = ProjectSettings(project_name="MyProject")
project_settings.add_info("global idea", "Example project for documentation generation")

# 2. Define ignore patterns (same as in autodocconfig.yml)
ignore_list = [
    "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db",
    "data", "venv", "env", ".venv", ".env", ".vscode", ".idea",
    "*.iml", ".gitignore", ".ruff_cache", ".auto_doc_cache", "*.pyc",
    "__pycache__", ".git", ".coverage", "htmlcov", "migrations",
    "*.md", "static", "staticfiles", ".mypy_cache"
]

# 3. Create GPT model instances (API_KEY is read from autodocgenerator.engine.config.config)
sync_model = GPTModel(API_KEY)          # Synchronous model
async_model = AsyncGPTModel(API_KEY)    # Asynchronous model

# 4. Set up a progress bar (optional but used in the example)
with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
) as progress:
    progress_bar = LibProgress(progress)

    # 5. Initialise the Manager
    manager = Manager(
        project_path=".",                # current directory
        project_settings=project_settings,
        sync_model=sync_model,
        async_model=async_model,
        ignore_files=ignore_list,
        progress_bar=progress_bar,
        language="en"
    )

    # 6. Run the documentation generation steps
    manager.generate_code_file()
    manager.generate_global_info_file(use_async=False, max_symbols=8000)
    manager.generete_doc_parts(use_async=False, max_symbols=4000)

    # 7. Generate intro and custom documentation parts (doc factories must be prepared)
    # Example factories (replace with your own if needed)
    from autodocgenerator.factory.base_factory import DocFactory
    from autodocgenerator.factory.modules.intro import IntroLinks, IntroText

    doc_factory = DocFactory(
        IntroLinks(),
        IntroText(),
    )
    intro_factory = DocFactory(
        IntroLinks(),
        IntroText(),
    )
    manager.factory_generate_doc(doc_factory)
    manager.factory_generate_doc(intro_factory)

    # 8. Retrieve the final documentation
    output_md = manager.read_file_by_file_key("output_doc")
    print(output_md)   # or write to a file, e.g., README.md
```

<a name='autodocconfig.yml_options'> </a>
**autodocconfig.yml** is a YAML file that defines the configuration for the Auto Doc Generator. The following options are recognized by the generator (as implemented in `autodocgenerator/auto_runner/config_reader.py`):

| Option | Type | Description | Example |
|--------|------|-------------|---------|
| `project_name` | string | Name of the project. Used in the generated documentation. | `project_name: "My Awesome Project"` |
| `language` | string | Language code for the documentation (default: `en`). | `language: "en"` |
| `ignore_files` | list of strings | Glob patterns for files/directories that should be ignored during analysis. If omitted, a built‑in default list is used. | `ignore_files: ["*.log", "venv", ".git"]` |
| `project_additional_info` | mapping (key‑value) | Arbitrary extra information about the project that will be added to the documentation. | ```yaml\nproject_additional_info:\n  global idea: "This project helps developers generate docs automatically"\n``` |
| `custom_descriptions` | list of strings | Custom text blocks that will be turned into modules (`CustomModule`) and injected into the documentation. Each string can contain a full description or instruction. | ```yaml\ncustom_descriptions:\n  - "explain how install workflow with install.ps1 ..."\n  - "how to use Manager class ..."\n  - "explain how to write autodocconfig.yml file ..."\n``` |

**Minimal example**

```yaml
project_name: "Auto Doc Generator"
language: "en"
project_additional_info:
  global idea: "This project was created to help developers make documentations for them projects"
custom_descriptions:
  - "explain how install workflow with install.ps1 and install.sh scripts ..."
  - "how to use Manager class what parameters i need to give ..."
  - "explain how to write autodocconfig.yml file what options are available"
```

You can also add an `ignore_files` section if you need to override or extend the default ignore patterns. All listed options are optional except `project_name` (required by the code to set the project name).

 

<a name="autodocgenerator__init__"></a>
## autodocgenerator/__init__.py

**Purpose**  
The top‑level package initializer for **autodocgenerator**. Its sole responsibility is to emit a short identification string (`"ADG"`) when the package is imported. This acts as a lightweight sanity check confirming that the library is correctly installed and importable.

**Interaction with the system**  
- **Import side‑effect** – Any module that does `import autodocgenerator` (directly or indirectly via sub‑packages such as `autodocgenerator.auto_runner.run_file`) will trigger the `print` statement.  
- **No functional coupling** – The initializer does **not** expose symbols, configure logging, or modify global state beyond the stdout side‑effect, so it does not affect the rest of the documentation generation pipeline (config reading, model loading, UI progress handling, etc.).

**Key elements**

| Element | Type | Description |
|---------|------|-------------|
| `print("ADG")` | Statement | Writes the literal string `ADG` to standard output at import time. |

**Assumptions**  
- The environment’s stdout is available (e.g., running in a console or CI job).  
- The printed token is primarily for human verification; downstream code does not rely on it.

**Inputs / Outputs**  
- **Input:** None (execution occurs automatically on import).  
- **Output:** The string `ADG` is sent to `sys.stdout`. No return value.

**Side effects**  
- A console message may appear in CI logs, local shells, or any process that imports the package. This is harmless but could be noisy if the package is imported repeatedly.

**Typical usage**

```python
# In any script that needs the autodocgenerator functionality
import autodocgenerator   # => prints "ADG" once
from autodocgenerator.auto_runner import run_file

run_file.main()           # start the documentation generation workflow
```

**Notes for developers**  
- Because the initializer performs I/O on import, consider removing or guarding the `print` statement in production environments to keep logs clean.  
- If additional package‑wide setup becomes necessary (e.g., version checks, logging configuration), this file is the canonical place to add such logic while preserving the existing side‑effect for backward compatibility.

<a name="config_reader"></a>
## `autodocgenerator.auto_runner.config_reader`

**Purpose**  
Parse a user‑supplied *autodocconfig.yml* and translate it into runtime objects that drive the documentation generation pipeline.

**Key class – `Config`**  
- Holds global options: `ignore_files`, `language`, `project_name`, `project_additional_info` and a list of `custom_modules` (`CustomModule` instances).  
- Fluent setters (`set_language`, `set_project_name`, …) return `self` to enable chaining.  
- `get_project_settings()` builds a `ProjectSettings` object populated with the additional key/value pairs.  
- `get_doc_factory()` creates two `DocFactory` instances:  
  1. One containing all user‑defined `custom_modules`.  
  2. An “intro” factory pre‑populated with `IntroLinks` and `IntroText`.

**Helper – `read_config(file_data: str) -> Config`**  
1. `yaml.safe_load` reads the raw YAML.  
2. Populates a `Config` instance:  
   - Default ignore patterns are extended with any supplied in `ignore_files`.  
   - Language defaults to *en* but can be overridden.  
   - Project name & extra info are stored.  
   - Each entry in `custom_descriptions` becomes a `CustomModule` and is added via `add_custom_module`.  
3. Returns the fully‑initialised `Config`.

**Assumptions & side‑effects**  
- The YAML file follows the expected schema; missing keys fall back to defaults.  
- No I/O is performed here – the caller supplies the file contents.  
- The function raises the usual `yaml.YAMLError` if parsing fails.

---

<a name="run_file"></a>
## `autodocgenerator.auto_runner.run_file`

**Purpose**  
Orchestrate the end‑to‑end generation of project documentation using the configuration produced by `config_reader`.

**Core function – `gen_doc`**  
```python
gen_doc(project_settings, ignore_list, project_path, doc_factory, intro_factory)
```
- Instantiates a `rich.Progress` bar to give visual feedback.  
- Creates synchronous (`GPTModel`) and asynchronous (`AsyncGPTModel`) LLM wrappers using the package‑wide `API_KEY`.  
- Builds a `Manager` with: project root, settings, both models, the ignore list, a `LibProgress` wrapper around the progress bar, and the language (hard‑coded to *en*).  
- Executes the generation steps in order:
  1. `generate_code_file()` – extracts source code snippets.  
  2. `generate_global_info_file()` – produces high‑level project overview (sync, ≤8000 symbols).  
  3. `generete_doc_parts()` – creates section‑level docs (sync, ≤4000 symbols).  
  4. `factory_generate_doc()` twice – first with the custom `doc_factory`, then with the intro factory.  
- Returns the final assembled document via `manager.read_file_by_file_key("output_doc")`.

**CLI entry point** (`if __name__ == "__main__":`)  
- Reads *autodocconfig.yml*, builds a `Config` object, extracts `ProjectSettings` and both factories, then calls `gen_doc` for the current directory (`"."`).  
- The resulting markdown (or other format) is stored in `output_doc`.

**Interactions**  
- Relies on `Manager` (core engine), `DocFactory` (module aggregation), `ProjectSettings` (metadata), and the LLM models.  
- Progress UI is provided by `rich` and wrapped by `LibProgress` to conform to the internal progress interface.

**Assumptions & side‑effects**  
- `API_KEY` is a valid OpenAI key; missing/invalid keys will cause runtime errors in the model classes.  
- The function performs I/O through `Manager` (file reads/writes) and prints progress; it should be run in a controlled environment.  
- All ignore patterns are respected when traversing the project tree.

<a name="model-base"></a>
## `autodocgenerator.engine.models.model`

**Responsibility**  
Provides the common foundation for all LLM‑wrapper classes used by the documentation generator. It defines:

| Element | Purpose |
|---------|---------|
| `History` | Holds the message list sent to the LLM. Starts with the system prompt (`BASE_SYSTEM_TEXT`). |
| `ParentModel` | Stores the API key, a shared `History` instance, and a shuffled list of model identifiers (`MODELS_NAME`). The shuffle enables simple fail‑over: if one model fails, the next one is tried. |
| `Model` (sync) | Implements the high‑level “conversation” API: `get_answer` adds a user message, calls `generate_answer`, stores the assistant reply, and returns it. The default `generate_answer` is a stub that child classes override. |
| `AsyncModel` (async) | Mirrors `Model` but with `async` methods, allowing the engine to drive non‑blocking LLM calls. |

**Key Logic**  

* **History handling** – `add_to_history(role, content)` appends a dict compatible with the OpenAI/Groq chat API (`{"role": "...", "content": "…"}`).
* **Model rotation** – `self.regen_models_name` is a shuffled copy of `MODELS_NAME`. After each failed request the index is advanced (`self.current_model_index`). When the list is exhausted an exception is raised.
* **Answer helpers** – `get_answer_without_history` forwards a pre‑built list of messages directly to `generate_answer`; `get_answer` is the typical entry point used by higher‑level components (e.g., `Manager`).

**Assumptions & side‑effects**  

* `BASE_SYSTEM_TEXT`, `API_KEY` and `MODELS_NAME` are defined in `autodocgenerator.config.config`.  
* No network I/O occurs here; subclasses create the actual client objects.  
* History is mutable and shared across calls – callers must be aware that earlier exchanges remain in the context unless a fresh `History` is supplied.  

---

<a name="gpt-model"></a>
## `autodocgenerator.engine.models.gpt_model`

**Responsibility**  
Concrete LLM adapters that talk to the **Groq** inference service (both sync and async). They inherit the conversation handling from `Model` / `AsyncModel` and implement the real `generate_answer` logic.

### `GPTModel` (synchronous)

```python
class GPTModel(Model):
    def __init__(self, api_key=API_KEY, history=History()):
        super().__init__(api_key, history)
        self.client = Groq(api_key=self.api_key)
```

* **`generate_answer`** –  
  1. Chooses the current model name from `self.regen_models_name`.  
  2. Calls `self.client.chat.completions.create(messages=..., model=model_name)`.  
  3. On any exception, logs it (`print(e)`) and moves to the next model in the list, retrying until a response is obtained or the list is exhausted.  
  4. Returns the content of the first choice (`chat_completion.choices[0].message.content`).  

### `AsyncGPTModel` (asynchronous)

```python
class AsyncGPTModel(AsyncModel):
    def __init__(self, api_key=API_KEY, history=History()):
        super().__init__(api_key, history)
        self.client = AsyncGroq(api_key=self.api_key)
```

* **`generate_answer`** – identical logic to the sync version but uses `await` on the Groq async client.

**Interactions with the rest of the system**

* The **`auto_runner.gen_doc`** function creates one instance of each (`GPTModel`, `AsyncGPTModel`) and passes them to the central `Manager`.  
* `Manager` invokes `model.get_answer(prompt)` (or its async counterpart) to obtain LLM‑generated documentation fragments.  
* The fail‑over rotation defined in `ParentModel` ensures the engine continues even if a particular Groq model is temporarily unavailable.

**Important assumptions & side‑effects**

* A valid **Groq** API key (`API_KEY`) must be present; otherwise client construction fails.  
* Network errors are caught, printed, and trigger model rotation; no custom retry‑policy is applied.  
* The function raises a generic `Exception("all models do not work")` if every model in `MODELS_NAME` fails – callers should handle this to avoid crashing the whole generation run.  
* The returned string is raw LLM output; downstream components (e.g., `DocFactory`) are responsible for formatting or truncating it.

---

<a name="factory-init"></a>
## `autodocgenerator.factory.__init__`

The package’s `__init__.py` is currently empty; it simply marks `autodocgenerator.factory` as a Python package. Concrete factories (e.g., `DocFactory`) are defined in sibling modules and rely on the model classes above to obtain LLM answers.  

---  

**Summary for new developers**  
`model.py` establishes a reusable conversation framework with history and automatic model‑fallback. `gpt_model.py` supplies the actual Groq client implementations (sync/async) that the rest of the autodoc pipeline uses via the `Manager`. Understanding the flow from `auto_runner → Manager → GPTModel/AsyncGPTModel → Groq` is essential for extending or swapping out the LLM backend.

<a name="base-factory"></a>
## `autodocgenerator/factory/base_factory.py`

**Responsibility**  
Provides the core *factory* infrastructure that assembles documentation fragments.  
* `BaseModule` – abstract contract for a documentation‑generation unit.  
* `DocFactory` – orchestrates a list of `BaseModule` instances, runs them sequentially and aggregates their output while reporting progress.

**Key elements**

| Class / Method | Purpose |
|----------------|---------|
| `BaseModule` (ABC) | Declares `generate(info: dict, model: Model)`; every concrete module must implement it. |
| `DocFactory.__init__(*modules)` | Stores the supplied modules (`list[BaseModule]`). |
| `DocFactory.generate_doc(info, model, progress)` | <ul><li>Creates a sub‑task in `BaseProgress` (`"Generate parts"`).</li><li>Iterates over `self.modules`, calling `module.generate(info, model)`.</li><li>Appends each fragment to the final markdown string (`output`).</li><li>Updates progress after each module and finally removes the sub‑task.</li></ul> |
| `if __name__ == "__main__"` | Simple sanity‑check that the factory can be instantiated (uses dummy `BaseModule`). |

**Interactions**  
* Receives a *LLM model* (`Model` or `AsyncModel`) from the **engine** layer; modules use this model to request generated text.  
* Reports status to the UI layer via `BaseProgress` (`autodocgenerator/ui/progress_base.py`).  
* The assembled document is later handed to `DocFactory` callers (e.g., `auto_runner` or higher‑level `Manager`) for writing to files or further post‑processing.

**Assumptions & side‑effects**  
* All supplied modules respect the `BaseModule` contract; otherwise a `TypeError` occurs at runtime.  
* `progress` implements `create_new_subtask`, `update_task`, and `remove_subtask`; missing methods raise `AttributeError`.  
* No async handling here – the factory is synchronous; async pipelines must wrap calls accordingly.

---

<a name="custom-module"></a>
## `autodocgenerator/factory/modules/general_modules.py`

**Responsibility**  
Implements a concrete `BaseModule` that generates a custom description based on the *code‑mix* payload.

* `CustomModule` – stores a user‑provided `discription` (typo kept for backward compatibility).  
* `generate(info, model)` –  
  1. Retrieves the mixed‑code string from `info["code_mix"]`.  
  2. Splits it into chunks ≤ 7000 symbols via `split_data`.  
  3. Calls `generete_custom_discription` (pre‑processor) with the chunks, the LLM `model`, the custom description prompt, and the target language.  
  4. Returns the LLM‑generated fragment.

**Interactions**  
* Depends on `engine.models.model.Model` for LLM calls.  
* Uses preprocessing helpers from `autodocgenerator/preprocessor`: `split_data` (splits large texts) and `generete_custom_discription` (asks the model to produce a description).  
* Inserted into `DocFactory` alongside other modules to become part of the final doc.

**Assumptions**  
* `info` contains keys `"code_mix"` and `"language"`; missing keys raise `KeyError`.  
* `split_data` must accept `max_symbols` and return an iterable of strings.  
* The LLM model can handle the supplied prompt size; otherwise the call may fail and propagate an exception.

---

<a name="intro-modules"></a>
## `autodocgenerator/factory/modules/intro.py`

**Responsibility**  
Provides two introductory modules:

| Class | Description |
|-------|-------------|
| `IntroLinks` | Extracts all HTML links from the full repository dump (`info["full_data"]`), prints them (debug), and asks the LLM to generate a concise “links introduction” via `get_links_intro`. |
| `IntroText` | Generates a high‑level project introduction from `info["global_data"]` using `get_introdaction`. |

Both classes inherit from `BaseModule` and implement `generate(info, model)`.

**Key workflow**  
1. Retrieve raw data (`full_data` or `global_data`).  
2. Use post‑processing utilities (`get_all_html_links`, `get_links_intro`, `get_introdaction`) to format the data and invoke the LLM.  
3. Return the resulting markdown fragment.

**Interactions**  
* Relies on the same LLM `Model` instance passed by `DocFactory`.  
* Calls utility functions from `autodocgenerator/preprocessor/postprocess.py` which handle HTML parsing and prompt construction.  
* Contributes the introductory sections that appear at the top of the final documentation.

**Assumptions**  
* `info` must contain `"full_data"`, `"global_data"` and `"language"`.  
* The HTML extraction utilities expect well‑formed HTML; malformed input may lead to empty link lists.  

---

<a name="code-mix"></a>
## `autodocgenerator/preprocessor/code_mix.py`

**Responsibility**  
Collects a repository’s file tree and source contents into a single textual “code‑mix” file, while respecting ignore patterns.

* `CodeMix(root_dir, ignore_patterns)` – initializes with a base directory and a list of glob‑style patterns to skip (e.g., virtual‑env folders, compiled artefacts).  
* `should_ignore(path)` – determines if a `Path` matches any ignore pattern (checks full relative path, basename, and each path component).  
* `build_repo_content(output_file)` – writes to `output_file`:
  1. A tree view of directories/files (indented).  
  2. A separator line (`=====`).  
  3. For every non‑ignored file, a `<file path="...">` block containing its raw text. Errors while reading a file are logged inline.

**Interactions**  
* Used by the **pre‑processing** stage (e.g., `auto_runner`) to create the `"code_mix"` string that later modules (like `CustomModule`) consume.  
* Does **not** depend on the LLM layer; purely filesystem‑oriented.

**Assumptions & side‑effects**  
* `root_dir` exists and is readable; otherwise `Path.rglob` yields no results.  
* `ignore_patterns` are valid glob strings; overly broad patterns may omit needed files.  
* File reading uses UTF‑8 with error‑ignore, so binary files become garbled text rather than causing crashes.  
* Writes to `output_file` overwriting any existing content.

---

**Summary for new developers**  

The *factory* layer (`base_factory.py` + `modules/…`) defines a plug‑in system where each `BaseModule` knows how to turn a slice of the repository (links, intro, custom description) into LLM‑generated markdown. `DocFactory` strings these fragments together, reporting progress to the UI.  

The *preprocessor* (`code_mix.py`) prepares the raw repository dump that feeds the modules. Together with the LLM adapters (`engine/models/gpt_model.py`), they form the end‑to‑end pipeline:  

`auto_runner → CodeMix → info dict → DocFactory (Intro + Custom + …) → Model.generate_answer → final documentation`.  

Understanding the contract (`generate(info, model)`) and the required keys in the `info` dictionary is the key to extending the system with new documentation modules.

<a name="compressor"></a>
## `autodocgenerator/preprocessor/compressor.py`

**Purpose in the pipeline**  
`compressor.py` belongs to the **pre‑processing** stage. After the repository has been turned into a large “code‑mix” string, this module reduces its size and extracts concise, LLM‑friendly descriptions. It is the bridge between raw source material and the *DocFactory* modules that later ask the LLM to generate full documentation.

**Key responsibilities**  

| Function | Role | Main inputs | Main outputs | Side‑effects |
|----------|------|-------------|--------------|--------------|
| `compress` | Sends a single text chunk to the LLM with a compression prompt. | `data: str`, `project_settings: ProjectSettings`, `model: Model`, `compress_power: int` | Compressed string (LLM answer). | None (pure request). |
| `compress_and_compare` | Serially compresses a list of chunks, concatenating *compress_power* results into a new list (one element per group). | `data: List[str]`, `model`, `project_settings`, `compress_power`, optional `progress_bar` | `List[str]` with fewer, larger chunks. | Updates `BaseProgress` sub‑task. |
| `async_compress` | Same as `compress` but runs inside a semaphore‑protected coroutine, allowing concurrent calls. | Same as `compress` plus `semaphore`, `progress_bar` | Compressed string (awaitable). | Updates progress bar. |
| `async_compress_and_compare` | Parallel version of `compress_and_compare`. | `data: List[str]`, `model: AsyncModel`, `project_settings`, `compress_power`, optional `progress_bar` | `List[str]` grouped like the sync version. | Creates/tears down async progress sub‑task. |
| `compress_to_one` | Repeatedly compresses the list until a single chunk remains – the “final compressed representation” fed to downstream modules. | `data: List[str]`, `model`, `project_settings`, `compress_power`, `use_async` flag, optional `progress_bar` | Single `str` (the final compressed text). | May invoke many LLM calls; loops until length = 1. |
| `generate_discribtions_for_code` | For each compressed code fragment, asks the LLM to produce a developer‑focused description (components, params, usage example). | `data: List[str]`, `model`, `project_settings`, optional `progress_bar` | `List[str]` of markdown‑formatted descriptions. | Progress updates; no file I/O. |

**Interaction with the rest of the system**

* **`ProjectSettings`** – provides the *system* prompt (`project_settings.prompt`) that guides the LLM’s style.  
* **LLM adapters** – imports `Model` / `AsyncModel` from `engine/models/gpt_model.py`. Calls `model.get_answer_without_history` which sends the constructed prompt to the underlying OpenAI‑compatible service.  
* **Progress UI** – uses `BaseProgress` (from `ui/progress_base.py`) to expose sub‑tasks to the CLI/GUI, keeping the user informed about long‑running compression loops.  
* **Downstream modules** – the string returned by `compress_to_one` (or the list from `generate_discribtions_for_code`) is stored in the `info` dictionary that `DocFactory` later passes to modules such as `IntroModule`, `CustomModule`, etc.

**Assumptions & constraints**

* `compress_power` determines how many original chunks are merged per LLM call; higher values reduce the number of API requests but increase token usage.  
* The LLM is expected to respect the “compression” system prompt delivered by `get_BASE_COMPRESS_TEXT(max_tokens, compress_power)`.  
* Input strings must be UTF‑8; binary files should have been filtered out earlier (e.g., by `CodeMix`).  
* Async version limits concurrency to 4 simultaneous LLM calls (`asyncio.Semaphore(4)`). Adjust if API rate limits differ.  
* Functions are side‑effect‑free except for progress‑bar updates and the implicit network request to the LLM.

**Typical workflow**

```python
# 1️⃣ Build raw code‑mix (outside this file)
raw_chunks = [...]                     # list of strings, each a file or group

# 2️⃣ Reduce size
compressed = compress_to_one(
    data=raw_chunks,
    model=gpt_model,                  # Model or AsyncModel instance
    project_settings=settings,
    compress_power=4,
    use_async=True,
    progress_bar=ui_progress
)

# 3️⃣ Generate human‑readable descriptions
descriptions = generate_discribtions_for_code(
    data=[compressed],
    model=gpt_model,
    project_settings=settings,
    progress_bar=ui_progress
)
```

The resulting `descriptions` list becomes part of the `info` dict that `DocFactory` stitches together into the final markdown documentation.  

**What a newcomer should remember**

* The module does **no file I/O** – it only transforms strings via the LLM.  
* All public functions accept a `BaseProgress` (or default) to keep UI responsive.  
* When extending the system, you can adjust `compress_power` or the async semaphore to balance cost vs. speed, but keep the prompt contract (`project_settings.prompt` + `BASE_COMPRESS_TEXT`) intact.  

---  

*End of `compressor.py` documentation.*

<a name="postprocess"></a>
## `autodocgenerator/preprocessor/postprocess.py`

**Responsibility**  
This module post‑processes the raw markdown that is produced by the earlier stages of the documentation pipeline. Its main jobs are:

1. **Anchor generation** – turn a human‑readable header into a URL‑safe markdown anchor (`generate_markdown_anchor`).  
2. **Topic extraction** – locate all level‑2 headings (`## …`) in a markdown string and return both the plain titles and the corresponding anchors (`get_all_topics`).  
3. **HTML‑style link extraction** – find legacy `<a name="…">` markers that may still be present in generated files (`get_all_html_links`).  
4. **LLM‑driven intro generation** – ask the LLM to create a short introductory paragraph for a list of links (`get_links_intro`) and a project‑wide introduction from the whole markdown (`get_introdaction`).  
5. **Custom description extraction** – given a list of code/documentation fragments, repeatedly query the LLM until a fragment yields a useful answer for a user‑supplied custom query (`generete_custom_discription`).

**Interaction with the rest of the system**  

| Component | How it is used |
|-----------|----------------|
| `Model` / `GPTModel` (``engine/models``) | All LLM calls go through `model.get_answer_without_history`. The module does **no** token‑history management – it sends a fresh prompt each time. |
| `ProjectSettings` (``preprocessor/settings.py``) | The `prompt` property of `ProjectSettings` supplies a system prompt that other modules concatenate with the constants imported from ``engine/config/config.py``. |
| `BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE` | Fixed system prompts that shape the style of the generated introductions. |
| UI / progress layer | Not referenced directly here, but the calling code (e.g. `DocFactory`) passes a `BaseProgress` instance to the higher‑level functions that wrap the calls in this file. |

**Key Functions**

| Function | Signature | Purpose | Important notes |
|----------|-----------|---------|-----------------|
| `generate_markdown_anchor` | `header: str → str` | Normalises a heading to a markdown‑compatible anchor (`#my‑section`). Uses Unicode NFKC, strips illegal characters, collapses dashes. | Returns the leading `#` so callers can embed it directly in markdown links. |
| `get_all_topics` | `data: str → tuple[list[str], list[str]]` | Scans `data` for `\n## ` headings, extracts the title text, then builds anchors via `generate_markdown_anchor`. | Stops at the first newline after each heading; works for well‑formed markdown only. |
| `get_all_html_links` | `data: str → list[str]` | Looks for legacy `<a name="…">` tags, returns the fragment prefixed with `#`. Skips tags longer than 25 characters (likely noise). | Simple string search – not a full HTML parser. |
| `get_links_intro` | `links: list[str], model: Model, language: str = "en" → str` | Sends the list of anchors to the LLM with a system prompt that forces the requested language and a static intro‑creation prompt. Returns the LLM‑generated paragraph. |
| `get_introdaction` | `global_data: str, model: Model, language: str = "en" → str` | Similar to `get_links_intro` but works on the entire markdown document, using `BASE_INTRO_CREATE`. |
| `generete_custom_discription` | `splited_data: str, model: Model, custom_description: str, language: str = "en" → str` | Iterates over a sequence of text fragments, asking the LLM to answer a custom query. Breaks when a non‑empty, non‑“noinfo” answer is obtained; otherwise returns an empty string. | The function name contains a typo (kept for backward compatibility). The strict rules in the prompt force the model to answer only from the given context. |

**Assumptions & Side‑effects**

* Input markdown is UTF‑8 and follows conventional heading syntax (`##`).  
* The LLM respects the supplied system prompts; no token‑budget handling is performed here.  
* Functions are pure apart from the network request to the LLM; they do **not** read/write files.  
* `generete_custom_discription` expects `splited_data` to be an iterable of strings; the current type hint (`str`) is inaccurate.  
* The module assumes that the caller handles rate‑limits, retries, and progress‑bar updates.

**Typical usage flow**

```python
# 1. Extract topics and anchors from a generated markdown block
titles, anchors = get_all_topics(rendered_md)

# 2. Build a short intro for the table‑of‑contents links
toc_intro = get_links_intro(anchors, model=gpt_model, language="en")

# 3. Create a project‑wide introduction
project_intro = get_introdaction(rendered_md, model=gpt_model)

# 4. Optionally, fetch a custom description for a user‑defined query
custom_desc = generete_custom_discription(
    splited_data=code_fragments,
    model=gpt_model,
    custom_description="How does the authentication flow work?"
)
```

The returned strings are later stored in the `info` dictionary of a `ProjectSettings` instance and finally assembled by `DocFactory` into the final documentation markdown.

<a name="settings"></a>
## `autodocgenerator/preprocessor/settings.py`

**Responsibility**  
`ProjectSettings` aggregates static metadata about the project (name, arbitrary key‑value pairs) and builds a **system prompt** that is injected into every LLM request throughout the pipeline.

**Key Class**

| Class | Constructor | Important members |
|-------|-------------|-------------------|
| `ProjectSettings` | `project_name: str` | `project_name`, `info: dict`, `prompt` property |

* `add_info(key, value)` – stores additional context (e.g., framework, version).  
* `prompt` – concatenates `BASE_SETTINGS_PROMPT` (a constant from ``engine/config/config.py``) with the project name and all `info` entries, each on its own line. The resulting string is used as the **system** message for LLM calls that need project‑specific guidance.

**Assumptions**

* Callers will populate `info` before the first LLM request; the property lazily builds the prompt each time it is accessed.  
* No validation is performed on keys/values – they are inserted verbatim.

**Interaction**

* Modules such as `compressor.py`, `postprocess.py`, and any other component that talks to the LLM import `ProjectSettings` and use `settings.prompt` as part of the prompt chain.  
* Keeping the prompt consistent ensures the LLM respects project‑level constraints (e.g., naming conventions, target audience).

**Typical usage**

```python
settings = ProjectSettings(project_name="MyApp")
settings.add_info("Framework", "FastAPI")
settings.add_info("TargetAudience", "Developers")

# Later, when building an LLM request:
prompt = [
    {"role": "system", "content": settings.prompt},
    {"role": "user",   "content": user_question}
]
answer = model.get_answer_without_history(prompt=prompt)
```

Together, `postprocess.py` and `settings.py` form the finishing layer of the autodoc generator: they tidy up headings, create navigable anchors, and inject project‑specific guidance into the LLM, enabling the final markdown documentation to be coherent, searchable, and tailored to the target audience.

<a name="spliter"></a>
## `autodocgenerator/preprocessor/spliter.py`

**Purpose**  
This module slices a large mixed‑code string into LLM‑friendly chunks, sends each chunk to a GPT model (sync or async), and reassembles the generated markdown. It is the bridge between the raw source extraction stage and the final documentation assembly performed by `DocFactory`.

### Imports & Dependencies
| Import | Role |
|--------|------|
| `GPTModel, AsyncGPTModel, AsyncModel, Model` (engine.models.gpt_model) | Unified interface for LLM calls (`get_answer_without_history`). |
| `BASE_PART_COMPLITE_TEXT` (engine.config.config) | System‑prompt fragment that tells the model to “complete a documentation part”. |
| `BaseProgress` (ui.progress_base) | Simple progress‑bar abstraction used by the caller to visualise chunk processing. |
| `asyncio` | Concurrency control for the async path (`Semaphore`). |

### Core Functions  

| Function | Signature | Responsibility |
|----------|-----------|----------------|
| **`split_data(data: str, max_symbols: int) -> list[str]`** | `data` – full mixed code, `max_symbols` – target chunk size | Breaks the input on newline boundaries, then repeatedly halves any segment that exceeds `1.5 × max_symbols`. Afterwards it greedily packs the pieces into a list whose each element is ≤ `1.25 × max_symbols`. Returns a list of strings ready for LLM consumption. |
| **`write_docs_by_parts(part: str, model: Model, global_info: str, prev_info: str | None = None, language: str = "en") -> str`** | Sends a single chunk to a synchronous LLM. Builds a prompt consisting of: <br>• language hint (system) <br>• `BASE_PART_COMPLITE_TEXT` (system) <br>• optional *previous part* context (system) <br>• the code chunk (user) <br>• the same chunk again (user, to satisfy the original design). Strips surrounding markdown fences (``` … ```). Returns the raw documentation fragment. |
| **`async_write_docs_by_parts(...) -> str`** | Same parameters plus `semaphore` and optional `update_progress` callback. | Mirrors `write_docs_by_parts` but runs inside an `async with semaphore` block, allowing up‑to‑four concurrent LLM calls. Calls `update_progress()` after each answer is received. |
| **`gen_doc_parts(full_code_mix: str, global_info: str, max_symbols: int, model: Model, language: str, progress_bar: BaseProgress) -> str`** | Orchestrates the synchronous pipeline: <br>1. `split_data` → `splited_data`. <br>2. Creates a sub‑task on the supplied `progress_bar`. <br>3. Iteratively calls `write_docs_by_parts`, concatenates results, keeps the last 3 k characters as context for the next chunk, updates progress. <br>Returns the full assembled markdown. |
| **`async_gen_doc_parts(...) -> str`** | Async counterpart of `gen_doc_parts`. <br>Creates a semaphore (max 4 concurrent calls), builds a list of `async_write_docs_by_parts` tasks, gathers them, concatenates the answers, and returns the final documentation. |

### Interaction with the Rest of the System
* **`ProjectSettings`** supplies the *project‑wide* system prompt (not used directly here but concatenated upstream).  
* **`DocFactory`** receives the string returned by `gen_doc_parts` / `async_gen_doc_parts` and inserts it into the final markdown file.  
* **Progress UI** (`BaseProgress`) is driven by this module; callers must provide an instantiated progress bar.  

### Assumptions & Side‑effects
* Callers handle rate‑limiting, retries, and progress‑bar lifecycle.  
* `global_info` is currently unused (commented out) but kept for future extension.  
* The functions mutate only local variables; no filesystem I/O occurs.  

---  

*Typical usage (synchronous)*  

```python
parts_md = gen_doc_parts(
    full_code_mix=code_blob,
    global_info="",
    max_symbols=4000,
    model=gpt_model,
    language="en",
    progress_bar=pb,
)
```  

*Typical usage (asynchronous)*  

```python
final_md = await async_gen_doc_parts(... )
```  

<a name="ui.progress_base"></a>
## `autodocgenerator.ui.progress_base`

The **progress module** supplies a thin abstraction over *rich*’s `Progress` object so the documentation‑generation pipeline can report its work without being tied to a concrete UI library.

### Responsibility
* Provide a **minimal, interchangeable interface** (`BaseProgress`) that the core generators (`gen_doc_parts`, `async_gen_doc_parts`) use to create, update and clean up progress sub‑tasks.
* Offer a concrete implementation (**`LibProgress`**) that drives a `rich.progress.Progress` instance – the default UI when the tool is run from a terminal.

### Core Classes  

| Class | Key API | Behaviour |
|-------|---------|-----------|
| **`BaseProgress`** | `create_new_subtask(name: str, total_len: int)`<br>`update_task()`<br>`remove_subtask()` | Abstract protocol. The base class does nothing; concrete subclasses implement the three methods. Used by the generators only through this interface, allowing future UI replacements (e.g., a Qt widget or a CI‑friendly logger). |
| **`LibProgress`** | Inherits `BaseProgress` | *Constructor* receives a pre‑configured `rich.progress.Progress` and an optional `total` (default 4) – the number of high‑level steps the generator will perform (split, send, assemble, finalize). It creates a **base task** that represents overall progress. When `create_new_subtask` is called a **sub‑task** is added; subsequent `update_task` calls advance either the sub‑task (if present) or the base task. `remove_subtask` discards the reference so further updates fall back to the base task. |

#### Implementation Sketch
```python
class LibProgress(BaseProgress):
    def __init__(self, progress: Progress, total=4):
        self.progress = progress
        self._base_task = progress.add_task("General progress", total=total)
        self._cur_sub_task = None

    def create_new_subtask(self, name, total_len):
        self._cur_sub_task = self.progress.add_task(name, total=total_len)

    def update_task(self):
        if self._cur_sub_task is None:
            self.progress.update(self._base_task, advance=1)
        else:
            self.progress.update(self._cur_sub_task, advance=1)

    def remove_subtask(self):
        self._cur_sub_task = None
```

### Interaction with the Rest of the System
* **`gen_doc_parts` / `async_gen_doc_parts`** receive a `BaseProgress` instance (commonly a `LibProgress`) and use it to:
  1. `create_new_subtask` for the *splitting* step (total = len(chunks)).
  2. `update_task` after each LLM call finishes.
  3. `remove_subtask` when a stage ends, allowing the base task to continue.
* **`DocFactory`** and the CLI never touch this module directly; they only pass the progress object down the call chain.
* Because the API is deliberately tiny, swapping to a different progress backend (e.g., a simple stdout logger for CI) only requires implementing the three abstract methods.

### Assumptions & Side‑effects
* The caller supplies a **ready‑to‑use** `rich.Progress` (started with `with Progress() as prog:`). `LibProgress` does not start or stop the progress context itself.
* No I/O or state is persisted – all tasks are in‑memory and disappear when the `Progress` instance is closed.
* The `total` argument of the base task should match the number of high‑level operations the generator will report; mismatches simply affect the visual percentage.

### Typical Usage (CLI)

```python
from rich.progress import Progress
from autodocgenerator.ui.progress_base import LibProgress
from autodocgenerator.doc_factory import DocFactory

with Progress() as prog:
    ui = LibProgress(prog)                # progress UI for the run
    doc_md = await async_gen_doc_parts(
        full_code_mix=code_blob,
        global_info="",
        max_symbols=4000,
        model=gpt_model,
        language="en",
        progress_bar=ui,
    )
    DocFactory.save(doc_md, "README.md")
```

The `LibProgress` implementation fulfills the contract expected by the documentation pipeline while keeping the UI layer loosely coupled, making the system easy to test and to extend with alternative progress reporters.

