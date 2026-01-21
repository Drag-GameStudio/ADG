## Executive Navigation Tree
- 📂 Core Engine
  - [Engine Models Overview](#engine-models-overview)
  - [Parentmodel](#parentmodel)
  - [Sync Model](#sync-model)
  - [Async Model](#async-model)
  - [Gptmodel](#gptmodel)
  - [Asyncgptmodel](#asyncgptmodel)

- 📂 Documentation Generation
  - [Docfactory Examples](#DocFactory_examples)
  - [Autodocconfig](#autodocconfig)
  - [Autodocgenerator Init](#autodocgenerator_init)
  - [Write Docs By Parts](#write_docs_by_parts)
  - [Async Write Docs By Parts](#async_write_docs_by_parts)
  - [Gen Doc Parts](#gen_doc_parts)
  - [Async Gen Doc Parts](#async_gen_doc_parts)
  - [Generate Descriptions](#generate_descriptions)
  - [Postprocess-Module](#postprocess-module)
  - [Spliter-Module](#spliter-module)
  - [Split Data](#split_data)

- 📂 Compression Utilities
  - [Compressor](#compressor)
  - [Compress](#compress)
  - [Compress And Compare](#compress_and_compare)
  - [Async Compress](#async_compress)
  - [Compress To One](#compress_to_one)

- 📂 Progress & Interaction
  - [Baseprogress](#baseprogress)
  - [Libprogress](#libprogress)
  - [Interaction](#interaction)

- 📂 Extensibility & Integration
  - [Integration](#integration)
  - [Extensibility](#extensibility)
  - [Extending](#extending)
  - [Basefactory](#basefactory)
  - [Generalmodules](#generalmodules)
  - [Codemix](#codemix)

- 📂 Manager Utilities
  - [Using Manager Class](#Using_Manager_Class)

- 📂 Testing & Assumptions
  - [Testing](#testing)
  - [Assumptions](#assumptions)

- 📂 Overview & Intro
  - [Intro](#intro)
  - [Overview](#overview)
  - [Example](#example)
  - [History](#history)

 


<a name='Using_Manager_Class'></a>
**How to use the `Manager` class**

The `Manager` class is instantiated with the following parameters (as shown in `autodocgenerator/auto_runner/run_file.py`):

| Parameter | Description (inferred from usage) |
|-----------|-----------------------------------|
| `project_path` | Path to the root of the project (e.g., `"."`). |
| `project_settings` | An instance of `ProjectSettings` containing project metadata. |
| `sync_model` | An instance of `GPTModel` (synchronous model). |
| `async_model` | An instance of `AsyncGPTModel` (asynchronous model). |
| `ignore_files` | List of file patterns to ignore during documentation generation. |
| `progress_bar` | An object implementing progress reporting, e.g., `LibProgress(progress)`. |
| `language` | Language code for the documentation (e.g., `"en"`). |

**Full example of usage**

```python
# Example: Using the Manager class to generate documentation

from autodocgenerator.manage import Manager
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.engine.config.config import API_KEY
from autodocgenerator.preprocessor.settings import ProjectSettings
from autodocgenerator.ui.progress_base import LibProgress
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

# 1. Prepare project settings (could be read from autodocconfig.yml)
project_settings = ProjectSettings("MyProject")
project_settings.add_info("global idea", "Example project for documentation generation")

# 2. Define ignore patterns (same as default or custom)
ignore_list = [
    "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db", "data",
    "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore",
    ".ruff_cache", ".auto_doc_cache", "*.pyc", "__pycache__", ".git",
    ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles",
    ".mypy_cache"
]

# 3. Initialize GPT models (API key is taken from the config)
sync_model = GPTModel(API_KEY)
async_model = AsyncGPTModel(API_KEY)

# 4. Set up a Rich progress bar
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
) as progress:
    progress_bar = LibProgress(progress)

    # 5. Create the Manager instance
    manager = Manager(
        project_path=".",                # path to the project root
        project_settings=project_settings,
        sync_model=sync_model,
        async_model=async_model,
        ignore_files=ignore_list,
        progress_bar=progress_bar,
        language="en"                    # documentation language
    )

    # 6. Run the generation steps (as in run_file.py)
    manager.generate_code_file()
    manager.generate_global_info_file(use_async=False, max_symbols=8000)
    manager.generete_doc_parts(use_async=False, max_symbols=4000)

    # Example: generate documentation using a factory (doc_factory must be created elsewhere)
    # manager.factory_generate_doc(doc_factory)

    # Retrieve the final documentation content
    output = manager.read_file_by_file_key("output_doc")
    print(output)
```

This example mirrors the workflow used in `autodocgenerator/auto_runner/run_file.py`, showing all required parameters and a typical sequence of method calls on the `Manager` instance.

<a name='DocFactory_examples'> </a>

**Example 1 – Using custom description modules**

```python
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.general_modules import CustomModule

# Create custom modules from description strings
mod1 = CustomModule("how to use Manager class what parameters i need to give. give full example of usage")
mod2 = CustomModule("give me examples of usage for DocFactory with different modules")
mod3 = CustomModule("explain how to write autodocconfig.yml file what options are available")

# Initialise DocFactory with the custom modules
custom_doc_factory = DocFactory(mod1, mod2, mod3)
```

**Example 2 – Using built‑in introductory modules**

```python
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.intro import IntroLinks, IntroText

# Initialise DocFactory with the standard intro modules
intro_factory = DocFactory(
    IntroLinks(),
    IntroText(),
)
```

**Example 3 – Combining both custom and intro modules**

```python
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.general_modules import CustomModule
from autodocgenerator.factory.modules.intro import IntroLinks, IntroText

custom = CustomModule("custom description for a specific feature")
intro_links = IntroLinks()
intro_text = IntroText()

# DocFactory can receive any mix of modules
mixed_factory = DocFactory(custom, intro_links, intro_text)
```

**Typical usage in the generation pipeline**

```python
from autodocgenerator.auto_runner.run_file import gen_doc
from autodocgenerator.auto_runner.config_reader import read_config

# Load configuration (autodocconfig.yml)
with open("autodocconfig.yml", "r", encoding="utf-8") as f:
    cfg = read_config(f.read())

project_settings = cfg.get_project_settings()
doc_factory, intro_factory = cfg.get_doc_factory()

# Generate documentation
output = gen_doc(
    project_settings,
    cfg.ignore_files,
    ".",                # project root
    doc_factory,        # custom content
    intro_factory,      # introductory content
)
```

<a name='autodocconfig'> </a>
The `autodocconfig.yml` file is a YAML configuration used by **autodocgenerator**.  
Based on the repository code (`autodocgenerator/auto_runner/config_reader.py`) the following top‑level options are recognized:

- **project_name** *(string)* – The name of the project.  
- **language** *(string, default “en”)* – Language for the generated documentation.  
- **ignore_files** *(list of string patterns, optional)* – File‑name patterns that will be excluded from the documentation process (e.g., `*.pyc`, `__pycache__`, `venv`, etc.).  
- **project_additional_info** *(mapping)* – Arbitrary key‑value pairs that are added to the project settings; each key is a string and the value is a string.  
- **custom_descriptions** *(list of strings)* – Descriptions that are turned into `CustomModule` objects and incorporated into the documentation generation pipeline.

Only these options are parsed by `read_config`; any other fields are ignored. An example configuration from the repository:

```yaml
project_name: "Auto Doc Generator"
language: "en"

project_additional_info:
  global idea: "This project was created to help developers make documentations for them projects"

custom_descriptions:
  - "how to use Manager class what parameters i need to give. give full example of usage"
  - "give me examples of usage for DocFactory with different modules"
  - "explain how to write autodocconfig.yml file what options are available"
```

 

<a name="autodocgenerator_init"></a>
## autodocgenerator/__init__.py

### Overview
`autodocgenerator/__init__.py` is the **package initializer** for the *Auto Doc Generator* (ADG) library.  
Its sole purpose is to emit a short banner (`"ADG"`) when the package is imported.  
Although minimal, this file plays a key role in the **module discovery** performed by the CI/CD pipelines and the documentation‑generation runner (`autodocgenerator.auto_runner.run_file`).

### Responsibility
- **Side‑effect notification** – prints a recognizable string (`"ADG"`) to standard output the first time the package is imported.  
- **Package marker** – signals to Python that `autodocgenerator` is a proper package, allowing relative imports such as `from .engine import config` throughout the codebase.

### Interaction with the System
| Component | Interaction |
|-----------|-------------|
| **GitHub Actions (`docs.yml`)** | Executes `python -m autodocgenerator.auto_runner.run_file`. Importing `autodocgenerator` triggers this `__init__` file, resulting in the banner appearing in the CI logs (useful for quick sanity checks). |
| **`autodocgenerator.auto_runner.run_file`** | Imports the top‑level package (`import autodocgenerator`). The banner confirms that the import succeeded before the runner proceeds to read configuration, load factories, and generate documentation. |
| **Developers / End‑users** | When they run `python -m autodocgenerator` or import any sub‑module, they see the `"ADG"` output, confirming that the correct package version is being used. |

### Key Logic Flow
```python
# autodocgenerator/__init__.py
print("ADG")
```
1. **Module import** – Python evaluates the package’s `__init__` file.
2. **`print` statement** – Sends the literal string `"ADG"` to `stdout`.
3. **Import completes** – Control returns to the caller (e.g., the runner or user script).

### Assumptions
- The environment’s standard output is not redirected or suppressed; otherwise the banner may be invisible.
- No other side effects (e.g., logging configuration) are required at import time. The simplicity is intentional to keep import overhead negligible.

### Inputs & Outputs
| Aspect | Description |
|--------|-------------|
| **Input** | Implicit import mechanism; no explicit arguments. |
| **Output** | A single line printed to `stdout`: `ADG`. No return value, no raised exceptions. |
| **Side Effects** | The only side effect is the console output; no file I/O, network calls, or state mutation. |

### Extensibility & Best Practices
- **Do not add heavy logic** here. Heavy initialisation should live in dedicated modules (e.g., `engine/config/config.py`) to avoid slowing down imports.
- If future versions need richer startup information (version, environment), consider replacing the plain `print` with a structured logger:
  ```python
  import logging
  logger = logging.getLogger(__name__)
  logger.info("Auto Doc Generator (ADG) initialized")
  ```
- Keep the banner consistent with CI logs and documentation generation output to aid debugging.

### Example Usage
```bash
$ python -c "import autodocgenerator"
ADG
```
Or via the documentation runner:
```bash
$ python -m autodocgenerator.auto_runner.run_file
# CI log will contain:
# ADG
# ... (subsequent runner output)
```

### Summary
`autodocgenerator/__init__.py` is a lightweight entry point that confirms successful package import by printing `"ADG"`. It ensures the package is recognized by Python’s import system and provides a quick visual cue in CI pipelines and interactive sessions. Its design intentionally avoids any heavy computation, delegating all functional responsibilities to the sub‑packages under `autodocgenerator`.

<a name="autodocgenerator.auto_runner.config_reader"></a>
## `autodocgenerator/auto_runner/config_reader.py`

### Purpose  
`config_reader.py` translates a user‑provided YAML configuration file into a **runtime `Config` object** that the documentation‑generation pipeline can consume. It centralises all static settings (ignore patterns, language, project metadata, custom modules) and supplies ready‑to‑use factories for the documentation engine.

### Core Class – `Config`

| Attribute | Meaning | Default |
|-----------|---------|---------|
| `ignore_files` | Glob patterns that the `Manager` will skip while scanning the project tree. | A comprehensive list covering compiled artefacts, virtual‑env folders, IDE caches, etc. |
| `language` | Target language for generated docs. | `"en"` |
| `project_name` | Human‑readable name of the analysed project. | `""` (must be supplied by the user) |
| `project_additional_info` | Arbitrary key/value pairs that are injected into `ProjectSettings`. | `{}` |
| `custom_modules` | Instances of `CustomModule` that extend the documentation generation (e.g., extra sections, specialised parsers). | `[]` |

#### Fluent API  
All mutators (`set_language`, `set_project_name`, `add_*`) return `self`, enabling a builder‑style configuration:

```python
cfg = Config().set_language("fr").add_ignore_file("*.tmp")
```

#### Helper Methods  

* **`get_project_settings()`** – builds a `ProjectSettings` object (from `autodocgenerator.preprocessor.settings`) populated with `project_name` and any additional info.  
* **`get_doc_factory()`** – creates two `DocFactory` instances:  
  1. **`docFactory`** – contains all user‑defined `custom_modules`.  
  2. **`intro_factory`** – always includes the built‑in intro modules (`IntroLinks`, `IntroText`).  

These factories are later passed to the `Manager` to render the final documentation.

### `read_config(file_data: str) -> Config`

1. **Parse YAML** – `yaml.safe_load` converts the raw string into a Python dict.  
2. **Instantiate `Config`** – starts from the defaults defined in `__init__`.  
3. **Populate fields** –  
   * `ignore_files` → `add_ignore_file` (preserves defaults).  
   * `language` → `set_language`.  
   * `project_name` → `set_project_name`.  
   * `project_additional_info` → `add_project_additional_info`.  
   * `custom_descriptions` → each entry wrapped in `CustomModule` and added via `add_custom_module`.  
4. **Return** the fully‑initialised `Config` object.

#### Assumptions & Side‑effects  

* The YAML file is well‑formed; malformed content will raise `yaml.YAMLError`.  
* No I/O is performed here – the caller supplies the file contents.  
* All fields are optional; missing keys fall back to sensible defaults.

---

<a name="autodocgenerator.auto_runner.run_file"></a>
## `autodocgenerator/auto_runner/run_file.py`

### Purpose  
`run_file.py` is the **entry point** for the command‑line execution of the Auto‑Doc Generator (ADG). It wires together configuration, LLM models, progress UI, and the core `Manager` to produce a single markdown (or similar) document representing the analysed project.

### Main Function – `gen_doc`

```python
def gen_doc(
    project_settings: ProjectSettings,
    ignore_list: list[str],
    project_path: str,
    doc_factory: DocFactory,
    intro_factory: DocFactory,
) -> str:
```

#### Workflow  

1. **Progress UI** – a `rich.Progress` bar with spinner, description, and bar columns visualises the long‑running steps.  
2. **LLM Clients** –  
   * `sync_model = GPTModel(API_KEY)` – synchronous OpenAI‑compatible client.  
   * `async_model = AsyncGPTModel(API_KEY)` – asynchronous counterpart (currently used synchronously).  
3. **Manager Construction** – `Manager` receives:  
   * `project_path` – root directory to scan.  
   * `project_settings` – metadata from `Config`.  
   * LLM clients, ignore patterns, progress wrapper (`LibProgress`), and language.  
4. **Generation Steps** (executed sequentially):  
   * `generate_code_file()` – extracts source‑code snippets.  
   * `generate_global_info_file()` – creates a high‑level overview (max 8000 symbols).  
   * `generete_doc_parts()` – splits the work into manageable chunks (max 4000 symbols).  
   * `factory_generate_doc(doc_factory)` – runs user‑defined custom modules.  
   * `factory_generate_doc(intro_factory)` – adds the standard intro sections.  
5. **Result Retrieval** – `manager.read_file_by_file_key("output_doc")` returns the final assembled document as a string.

#### Return Value  
A **single string** containing the complete generated documentation.

### Script Execution (`if __name__ == "__main__":`)

1. Reads `autodocconfig.yml` from the current working directory.  
2. Calls `read_config` (from `config_reader.py`) to obtain a `Config` instance.  
3. Extracts `ProjectSettings` and the two `DocFactory` objects.  
4. Invokes `gen_doc` with the current directory (`"."`) as the project root.  
5. Stores the resulting document in `output_doc` (the script does not automatically write it to disk; callers can add that step).

### Interaction with the Rest of the System  

| Component | Role in the Flow |
|-----------|------------------|
| **`autodocgenerator.manage.Manager`** | Orchestrates file discovery, LLM calls, and assembly of documentation parts. |
| **`autodocgenerator.engine.models.gpt_model`** | Provides the LLM API wrappers used by `Manager`. |
| **`autodocgenerator.ui.progress_base`** | Supplies `LibProgress`, a thin adapter that lets `Manager` report progress to the `rich` bar. |
| **`autodocgenerator.factory.*`** | Supplies modular document generators (custom or built‑in intro). |
| **`autodocgenerator.preprocessor.settings.ProjectSettings`** | Holds project‑level metadata consumed by the factories. |

### Assumptions & Constraints  

* `API_KEY` is defined in `autodocgenerator.engine.config.config` and is a valid OpenAI (or compatible) key.  
* The environment has network access for LLM calls.  
* The progress bar is displayed on a terminal that supports ANSI escape codes.  
* All factories supplied are stateless or safely reusable across a single run.

### Extensibility Tips  

* **Async Generation** – `Manager` already supports async calls; switch `use_async=True` and adjust the `max_symbols` parameters to leverage concurrency.  
* **Additional Intro Modules** – Extend `IntroLinks`/`IntroText` or replace them by providing a custom `DocFactory` via the YAML `custom_descriptions` field.  
* **Custom Progress UI** – Implement another `BaseProgress` subclass and pass it to `Manager` if richer UI is required.

### Example Command‑Line Use  

```bash
$ python -m autodocgenerator.auto_runner.run_file
# Reads autodocconfig.yml, shows a progress bar, and prints the final doc string.
```

Or programmatically:

```python
from autodocgenerator.auto_runner.run_file import gen_doc
from autodocgenerator.auto_runner.config_reader import read_config, Config

with open("autodocconfig.yml", "r", encoding="utf-8") as f:
    cfg = read_config(f.read())

proj_settings = cfg.get_project_settings()
doc_factory, intro_factory = cfg.get_doc_factory()

doc = gen_doc(
    proj_settings,
    cfg.ignore_files,
    project_path=".",
    doc_factory=doc_factory,
    intro_factory=intro_factory,
)
print(doc)
```

### Summary  

`config_reader.py` converts a YAML description into a structured `Config` object, while `run_file.py` consumes that object to drive the full documentation generation pipeline. Together they form the **bootstrap layer** of the Auto‑Doc Generator, handling configuration, progress reporting, LLM initialisation, and final document assembly without embedding any heavy business logic—those responsibilities reside in the `Manager` and the various `DocFactory` modules.

<a name="engine-models-overview"></a>
## Engine Models Overview  

The **`autodocgenerator.engine.models`** package provides thin wrappers around the Groq LLM API.  
These wrappers are the only components that know how to talk to the remote model; all higher‑level logic (file discovery, prompt construction, document assembly) lives in the **`Manager`** and the various **`DocFactory`** modules.  

---

<a name="history"></a>
### `History`  

* **Purpose** – Holds the conversation history that is sent to the LLM.  
* **Key data** – `self.history` – a list of dictionaries `{role, content}`.  
* **Behaviour** – On construction a *system* message containing `BASE_SYSTEM_TEXT` (from `config.config`) is added automatically, unless the caller passes `None`.  
* **Side‑effects** – `add_to_history` mutates the internal list; the same `History` instance is shared by a model and its callers, so every `get_answer` call appends a *user* and *assistant* entry.  

---

<a name="parentmodel"></a>
### `ParentModel`  

* **Responsibility** – Stores common configuration for concrete model classes: API key, a `History` object, and a shuffled list of model names (`MODELS_NAME`).  
* **Model rotation** – `self.regen_models_name` is a random permutation of the configured model identifiers. When a request fails, the wrapper will advance `self.current_model_index` and retry with the next model.  

---

<a name="sync-model"></a>
### `Model` (synchronous)  

* **Base class** for `GPTModel`.  
* **Public helpers**  
  * `get_answer(prompt: str) → str` – records the user prompt, calls `generate_answer`, records the assistant reply, and returns it.  
  * `get_answer_without_history(prompt: list[dict]) → str` – forwards a pre‑built message list directly to `generate_answer`.  
* **Default `generate_answer`** – placeholder returning `"answer"`; overridden in `GPTModel`.  

---

<a name="async-model"></a>
### `AsyncModel` (asynchronous)  

* Mirrors `Model` but with `async` methods, enabling the `Manager` to run many LLM calls concurrently.  

---

<a name="gptmodel"></a>
### `GPTModel` (synchronous Groq wrapper)  

```python
class GPTModel(Model):
    def __init__(self, api_key=API_KEY, history=History()):
        super().__init__(api_key, history)
        self.client = Groq(api_key=self.api_key)
```

* **`generate_answer`**  
  1. Chooses the current model name from `self.regen_models_name`.  
  2. Calls `self.client.chat.completions.create(messages=…, model=model_name, temperature=0.3)`.  
  3. On any exception the failing model is removed from the rotation; the loop retries with the next entry.  
  4. Returns the content of the first choice (`chat_completion.choices[0].message.content`).  

* **Error handling** – If every configured model fails, an exception *“all models do not work”* is raised.  

---

<a name="asyncgptmodel"></a>
### `AsyncGPTModel` (asynchronous Groq wrapper)  

* Same logic as `GPTModel` but uses `AsyncGroq` and `await` for the API call.  
* On failure it cycles the index instead of removing the model, allowing a retry with the next candidate.  

---

<a name="integration"></a>
## Interaction with the Rest of the System  

| Component | How it uses the model layer |
|-----------|-----------------------------|
| **`autodocgenerator.manage.Manager`** | Instantiates either `GPTModel` or `AsyncGPTModel` (depending on `use_async`) and calls `get_answer` / `get_answer_without_history` to obtain LLM completions for each code fragment. |
| **`autodocgenerator.factory.*`** | Supplies the textual prompts (intro, description, etc.) that are fed to the model via the `History` object. |
| **`autodocgenerator.ui.progress_base.LibProgress`** | Receives progress updates from `Manager`; it does **not** interact with the model directly. |
| **`autodocgenerator.engine.config.config`** | Provides constants (`API_KEY`, `BASE_SYSTEM_TEXT`, `MODELS_NAME`) consumed by `ParentModel`. |

The model classes are deliberately stateless aside from the rotating list and the shared `History`; they can be safely recreated for each run or reused across a single documentation generation session.

---

<a name="assumptions"></a>
## Assumptions & Constraints  

* `API_KEY` must be a valid Groq (or compatible) token; otherwise the client raises an authentication error.  
* Network connectivity is required for every `generate_answer` call.  
* `MODELS_NAME` contains at least one model identifier; an empty list will cause an `IndexError`.  
* The `History` object is expected to contain only dictionaries with `"role"` (`"system"`, `"user"`, `"assistant"`) and `"content"` keys – this matches Groq’s chat schema.  

---

<a name="extensibility"></a>
## Extensibility Tips  

* **Custom LLM providers** – Subclass `ParentModel` and replace `self.client` with another SDK; keep the same `generate_answer` signature.  
* **Alternative retry policy** – Override the while‑loop logic in `GPTModel`/`AsyncGPTModel` to implement exponential back‑off or circuit‑breaker patterns.  
* **History persistence** – Swap the default `History` with a subclass that writes to disk if you need to audit the full prompt/response trail.  

---

<a name="example"></a>
## Quick Example  

```python
from autodocgenerator.engine.models.gpt_model import GPTModel

model = GPTModel()
answer = model.get_answer("Explain the purpose of the `History` class.")
print(answer)
```

In an asynchronous pipeline the same code would use `AsyncGPTModel` and `await model.get_answer(...)`.  

---  

*These classes constitute the **LLM access layer** of Auto‑Doc Generator, isolating the rest of the codebase from vendor‑specific details while providing simple, retry‑aware synchronous and asynchronous interfaces.*

**Documentation – Factory Layer & Repository‑mix Pre‑processor**  
*(part of the Auto‑Doc Generator pipeline – the “LLM‑driven documentation builder”)*  

---  

<a name="basefactory"></a>  
## `autodocgenerator/factory/base_factory.py`

### Purpose  
Provides the **pluggable module framework** that the manager uses to assemble a documentation page.  
* `BaseModule` – abstract contract for any “generation step” (e.g., intro text, custom description).  
* `DocFactory` – orchestrates a list of `BaseModule` instances, feeds them the same `info` payload and a concrete `Model` (sync or async), and concatenates their outputs.

### Core Classes  

| Class | Responsibility | Important Methods |
|-------|----------------|-------------------|
| **`BaseModule`** (ABC) | Defines the interface for a generation step. Sub‑classes implement `generate(info, model) → str`. | `generate` – abstract. |
| **`DocFactory`** | Holds an ordered collection of modules, creates a sub‑task in the UI progress bar, runs each module sequentially, aggregates results. | `__init__(*modules)` – stores modules.<br>`generate_doc(info, model, progress) → str` – main driver. |

### Interaction with the Rest of the System  

| Component | How it connects |
|-----------|-----------------|
| **`autodocgenerator.manage.Manager`** | Instantiates a `DocFactory` with the desired modules (e.g., `IntroText`, `CustomModule`). Calls `factory.generate_doc(info, model, progress)` to obtain the final markdown/HTML. |
| **`autodocgenerator.engine.models.*`** | Passed as the `model` argument; modules call `model.get_answer…` inside their `generate` implementation. |
| **`autodocgenerator.ui.progress_base.BaseProgress`** | Provides `create_new_subtask`, `update_task`, `remove_subtask` used by `DocFactory` to report per‑module progress. |
| **`autodocgenerator.factory.modules.*`** | Concrete `BaseModule` subclasses that live in the same package; they are the only objects `DocFactory` ever invokes. |

### Assumptions & Side‑effects  

* `info` is a dictionary produced by the **pre‑processor** (see `code_mix.py`) and contains keys such as `"code_mix"`, `"full_data"`, `"global_data"`, `"language"`.  
* Each module returns a **plain string** (markdown/HTML). `DocFactory` simply concatenates them with double new‑lines.  
* The progress object must support the three methods used; otherwise a runtime `AttributeError` is raised.  
* No state is kept inside `DocFactory` after `generate_doc` returns – it can be reused for multiple runs.  

---  

<a name="generalmodules"></a>  
## `autodocgenerator/factory/modules/general_modules.py`

### Responsibility  
Implements a **custom description module** that lets the user supply a free‑form prompt (`discription`).  
* Splits the large source‑code blob (`info["code_mix"]`) into chunks ≤ 7 000 symbols (via `split_data`).  
* Calls `generete_custom_discription` (typo‑preserved from the original code) which internally talks to the LLM model, feeding each chunk together with the custom prompt.  

### Key Points  

* **Constructor** stores the user‑provided description text.  
* `generate` returns the concatenated LLM answer for all chunks.  

### Interaction  

* Relies on **`engine.models.model.Model`** for the LLM client.  
* Uses **`preprocessor.spliter.split_data`** to respect token limits.  
* Calls **`preprocessor.postprocess.generete_custom_discription`** – the function that builds the final prompt and parses the model response.  

---  

<a name="intro"></a>  
## `autodocgenerator/factory/modules/intro.py`

### Responsibility  
Two small modules that produce the **introductory part** of the documentation:  

| Class | What it does |
|-------|--------------|
| **`IntroLinks`** | Extracts all HTML links from `info["full_data"]` (`get_all_html_links`) and asks the model to write a short description for each (`get_links_intro`). |
| **`IntroText`** | Generates a high‑level project introduction from `info["global_data"]` (`get_introdaction`). |

Both modules follow the same `BaseModule` contract and return a string ready to be concatenated.  

### Interaction  

* Import the same **`Model`** type as other modules.  
* Depend on **`preprocessor.postprocess`** helpers for link extraction and prompt creation.  

---  

<a name="codemix"></a>  
## `autodocgenerator/preprocessor/code_mix.py`

### Purpose  
Creates a **single text representation of an entire repository** (the “code‑mix”) that later feeds the LLM. It is used by the manager to populate `info["code_mix"]`.  

### Core Class  

| Method | Description |
|--------|-------------|
| `__init__(root_dir=".", ignore_patterns=None)` | Sets the repository root (resolved to an absolute `Path`) and a list of glob patterns / directory names to skip. |
| `should_ignore(path: Path) → bool` | Returns `True` if the given path matches any ignore pattern (supports full‑path, basename, and any path component). |
| `build_repo_content(output_file="repomix-output.txt")` | Writes two sections to `output_file`: <br>1️⃣ A tree‑like listing of directories/files (respecting ignore rules). <br>2️⃣ The raw content of each non‑ignored file wrapped in `<file path="…">` tags. Errors while reading a file are captured and written as a comment line. |

### Interaction  

* Called **once per documentation run** (usually by `Manager` before any LLM calls).  
* The generated file is read back by a separate pre‑processor (not shown) that stores its content in `info["code_mix"]`.  

### Assumptions & Side‑effects  

* `ignore_patterns` must be a list of glob strings; the default list (`ignore_list` defined at the bottom) filters out binaries, virtual‑env folders, IDE caches, etc.  
* The method opens the output file in **write‑mode**, overwriting any existing file.  
* File reading uses `encoding="utf-8"` with `errors="ignore"` – non‑UTF‑8 files are silently stripped of undecodable bytes.  
* The function may raise `OSError` if the output path is not writable.  

---  

<a name="extensibility"></a>  
## Extensibility Tips  

1. **Add a new generation step** – subclass `BaseModule`, implement `generate(self, info, model)`, and pass an instance to `DocFactory`.  
2. **Custom ignore logic** – override `should_ignore` in a subclass of `CodeMix` (e.g., to exclude large binary files by size).  
3. **Parallel module execution** – replace the simple `for` loop in `DocFactory.generate_doc` with `asyncio.gather` and use `AsyncModel` for true concurrency (requires a thread‑safe progress implementation).  

---  

*These components together form the **factory layer** of Auto‑Doc Generator: they turn raw repository data into structured prompts, invoke the LLM via the model layer, and stitch the pieces into a final documentation string.*

<a name="compressor"></a>
## `autodocgenerator/preprocessor/compressor.py`

### Overview  
This module implements the **compression pipeline** used by the Auto‑Doc Generator to shrink large code fragments (or any textual payload) before they are sent to the LLM.  
It works on the *pre‑processed* data produced by earlier steps (e.g., `code_mix` or raw file contents) and returns a single, highly‑condensed string that still preserves the essential information required for documentation generation.

The pipeline can run **synchronously** or **asynchronously**, and it reports its progress through the shared `BaseProgress` UI component.

---

<a name="compress"></a>
### `compress(data, project_settings, model, compress_power) → str`  
* **Purpose** – Build a three‑message prompt (system + system + user) and ask the LLM to compress `data`.  
* **Inputs**  
  * `data` – raw text to be shortened.  
  * `project_settings` – `ProjectSettings` instance providing the base system prompt (`project_settings.prompt`).  
  * `model` – an object implementing the `Model` protocol (`get_answer_without_history`).  
  * `compress_power` – integer controlling the aggressiveness of compression; passed to `get_BASE_COMPRESS_TEXT`.  
* **Output** – The LLM’s answer (a compressed version of `data`).  
* **Side‑effects** – None (pure function apart from the LLM call).

---

<a name="compress_and_compare"></a>
### `compress_and_compare(data, model, project_settings, compress_power=4, progress_bar=BaseProgress()) → list[str]`  
* **Purpose** – Batch‑compress a list of strings, then concatenate every `compress_power` results into a single chunk.  
* **Logic Flow**  
  1. Allocate a result list sized `ceil(len(data)/compress_power)`.  
  2. Create a sub‑task on `progress_bar` (total = `len(data)`).  
  3. Iterate over `data`, compress each element with `compress`, and append the result to the appropriate chunk (`curr_index = i // compress_power`).  
  4. Update the progress bar after each element.  
  5. Remove the sub‑task and return the list of concatenated chunks.  
* **Assumptions** – `compress_power` ≥ 1; `progress_bar` implements `create_new_subtask`, `update_task`, `remove_subtask`.

---

<a name="async_compress"></a>
### `async_compress(data, project_settings, model, compress_power, semaphore, progress_bar) → str` *(coroutine)*  
* Mirrors `compress` but runs inside an `asyncio.Semaphore` to limit concurrent LLM calls.  
* Calls `await model.get_answer_without_history(...)` and updates the progress bar once the answer is received.

---

<a name="async_compress_and_compare"></a>
### `async_compress_and_compare(data, model, project_settings, compress_power=4, progress_bar=BaseProgress()) → list[str]` *(coroutine)*  
* **Purpose** – Parallel version of `compress_and_compare`.  
* **Steps**  
  1. Initialise a semaphore (max 4 concurrent requests).  
  2. Spawn a task for each element via `async_compress`.  
  3. `await asyncio.gather(*tasks)` to collect all compressed pieces.  
  4. Re‑group the flat list into chunks of size `compress_power` (identical to the synchronous version).  
* **Side‑effects** – Progress bar updates are performed inside each `async_compress` call.

---

<a name="compress_to_one"></a>
### `compress_to_one(data, model, project_settings, compress_power=4, use_async=False, progress_bar=BaseProgress()) → str`  
* **Purpose** – Repeatedly compress the list until only a single string remains (the final “code‑mix” summary).  
* **Algorithm**  
  * While `len(data) > 1`:
    * Adjust `compress_power` to `2` when the list is too short for the default chunk size.  
    * Call either `compress_and_compare` or `async_compress_and_compare` based on `use_async`.  
    * Replace `data` with the newly produced list and increment an iteration counter.  
* **Result** – The sole element `data[0]`, a fully compressed representation of the original input set.

---

<a name="generate_descriptions"></a>
### `generate_discribtions_for_code(data, model, project_settings, progress_bar=BaseProgress()) → list[str]`  
* **Purpose** – Ask the LLM to produce developer‑oriented documentation snippets for each code block in `data`.  
* **Prompt** – A fixed system message describing the required output format (markdown, parameter tables, usage example) and a user message containing the raw code (`CONTEXT: {code}`).  
* **Flow**  
  1. Create a progress sub‑task (`len(data)`).  
  2. For each `code` element, send the prompt via `model.get_answer_without_history`.  
  3. Append the answer to `describtions` and update the progress bar.  
  4. Return the list of generated descriptions.  

---

### Interaction with the Rest of the System  
* **Model Layer** – Imports `Model` / `AsyncModel` from `engine.models.gpt_model`. All compression calls delegate the heavy‑lifting to the LLM via `get_answer_without_history`.  
* **Configuration** – Uses `get_BASE_COMPRESS_TEXT` (engine config) to inject a reusable system prompt fragment that encodes the desired compression ratio.  
* **UI** – Progress reporting is unified through `BaseProgress`, allowing the manager UI to display nested tasks (e.g., “Compare all files”, “Generate describtions”).  
* **Pre‑processor Pipeline** – The output of `compress_to_one` feeds `info["code_mix"]` (or similar) which later becomes part of the final prompt stack assembled by the `DocFactory` modules.

---

### Key Assumptions & Side‑effects  
* All text inputs are UTF‑8 compatible; the LLM is expected to handle any encoding quirks.  
* `compress_power` influences both the granularity of chunking and the aggressiveness of the compression prompt.  
* Asynchronous functions assume the event loop is not already running; `compress_to_one` safely invokes `asyncio.run` when `use_async=True`.  
* Errors from the LLM (network failures, rate limits) propagate as exceptions; callers (typically the manager) must handle them.  

---  

*This module is the “size‑reduction” stage of the Auto‑Doc Generator, turning potentially huge repository dumps into a compact, LLM‑friendly representation before the final documentation generation steps.*

<a name="postprocess-module"></a>
## `autodocgenerator.preprocessor.postprocess` – Post‑processing Helpers  

**Responsibility**  
This module prepares the raw markdown produced by the *compression* stage for the final documentation output.  
It extracts section titles, builds markdown anchors, generates introductory texts for the whole document and for individual link groups, and creates custom descriptions on demand. All heavy‑lifting (LLM calls) is delegated to the **Model** abstraction from `engine.models`.

**Key Functions**

| Function | Purpose | Important I/O |
|----------|---------|---------------|
| `generate_markdown_anchor(header: str) → str` | Normalises a heading into a GitHub‑style markdown anchor (`#my‑section`). | **Input:** raw heading text.<br>**Output:** anchor string prefixed with `#`. |
| `get_all_topics(data: str) → tuple[list[str], list[str]]` | Scans a markdown document for level‑2 headings (`## …`) and returns both the titles and their generated anchors. | **Input:** full markdown text.<br>**Output:** `(titles, anchors)`. |
| `get_all_html_links(data: str) → list[str]` | Extracts the names of existing HTML `<a name="…">` anchors (used by the generator to keep track of previously created links). | **Input:** markdown/HTML text.<br>**Output:** list of anchor names. |
| `get_links_intro(links: list[str], model: Model, language: str = "en") → str` | Sends the list of link anchors to the LLM and asks it to produce a short introductory paragraph that will be placed before the *Links* section. | **Input:** list of anchor strings, LLM model, language code.<br>**Output:** generated paragraph. |
| `get_introdaction(global_data: str, model: Model, language: str = "en") → str` | Generates a high‑level introduction for the whole documentation set, based on the compressed “code‑mix” text. | **Input:** concatenated compressed data, LLM model, language code.<br>**Output:** introduction markdown. |
| `generete_custom_discription(splited_data: str, model: Model, custom_description: str, language: str = "en") → str` | Iterates over pre‑split chunks of text, asking the LLM to answer a *custom* query (e.g., “Describe the authentication flow”). Stops at the first non‑empty answer that does not contain the sentinel `!noinfo`. | **Input:** iterable of text chunks, LLM model, user‑provided query, language.<br>**Output:** the first satisfactory description or an empty string. |

**Logic Flow Highlights**

1. **Anchor Generation** – `generate_markdown_anchor` normalises Unicode, replaces spaces with hyphens, strips illegal characters, collapses repeated hyphens, and finally prefixes `#`.  
2. **Topic Extraction** – `get_all_topics` walks the markdown string searching for `\n## ` markers, slices out the heading text, and builds a parallel list of anchors via the helper above.  
3. **LLM Interaction** – Both `get_links_intro` and `get_introdaction` construct a *system‑user* prompt array and call `model.get_answer_without_history`. The system messages embed static prompts (`BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`) from the central configuration, ensuring consistent wording across the pipeline.  
4. **Custom Description Loop** – `generete_custom_discription` respects strict response rules (no hallucination, empty output on missing info). It repeats the request for each chunk until a meaningful answer appears, using the sentinel `!noinfo` to detect “no data”.

**Assumptions & Side‑effects**

* Input markdown follows the conventional `##` heading style; otherwise topics will be missed.  
* The LLM model supplied implements `get_answer_without_history(prompt: list[dict]) → str` and may raise network‑related exceptions – callers must handle them.  
* All functions are pure except for the LLM calls, which have external side‑effects (API usage, rate limits).  
* The module does **not** modify the original `data` strings; it only returns derived values.

**Interaction with the Rest of the System**

* **Compression Stage** – The output of `compress_to_one` (a single large string) is passed to `get_introdaction` to obtain a human‑readable preface.  
* **DocFactory / UI** – The tuples `(titles, anchors)` from `get_all_topics` feed the table‑of‑contents builder; the introductory paragraphs are concatenated with the generated code‑block descriptions to form the final markdown document shown in the UI.  
* **Configuration Layer** – Static prompt fragments (`BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`) live in `engine.config.config`; any change there instantly propagates to this module.  

---

<a name="settings-module"></a>
## `autodocgenerator.preprocessor.settings` – Project‑wide Configuration Wrapper  

**Responsibility**  
Encapsulates per‑project metadata (name, arbitrary key/value pairs) and produces a ready‑to‑inject prompt segment (`ProjectSettings.prompt`) that is later concatenated with other system prompts (e.g., compression, introduction).

**Key Class**

```python
class ProjectSettings:
    def __init__(self, project_name: str)
    def add_info(self, key, value)          # store additional metadata
    @property
    def prompt(self) -> str                  # render the full settings block
```

* **Construction** – `project_name` is mandatory; additional data can be added at any time via `add_info`.  
* **Prompt Generation** – The `prompt` property concatenates the global `BASE_SETTINGS_PROMPT` (from `engine.config.config`) with a line `Project Name: …` and then each `key: value` pair on its own line. The result is a plain‑text block that can be inserted into any LLM prompt to give the model context about the target project.

**Assumptions & Side‑effects**

* The caller is responsible for calling `add_info` before accessing `prompt`; otherwise only the project name appears.  
* No external I/O occurs; the class is purely in‑memory.  

**System Interaction**

* **Model Layer** – When building prompts for compression or description generation, the `ProjectSettings.prompt` string is appended to the system messages, ensuring the LLM is aware of project‑specific constraints (e.g., target framework, coding standards).  
* **Configuration Centralisation** – By pulling `BASE_SETTINGS_PROMPT` from the shared config, the module guarantees that any organisational policy changes (license headers, confidentiality notices) are automatically reflected across all generated documentation.  

---  

*Together, `postprocess.py` and `settings.py` form the *post‑compression* phase of the Auto‑Doc Generator: they turn the compact “code‑mix” into a structured, navigable markdown document enriched with project‑specific context.*

<a name="spliter-module"></a>
## `autodocgenerator.preprocessor.spliter` – Chunking & LLM‑driven Documentation Generation  

**Purpose**  
This module bridges the *compression* stage (a single large “code‑mix” string) and the *post‑processing* stage that produces the final markdown document. It:

1. **Splits** the massive mixed‑code payload into size‑limited chunks that respect the LLM token limits.  
2. **Invokes** the configured language model (sync or async) for each chunk, feeding the previous chunk’s output as context so the generated documentation remains coherent across parts.  
3. **Aggregates** the per‑chunk answers into one continuous markdown string while reporting progress to the UI.

---

<a name="split_data"></a>
### `split_data(data: str, max_symbols: int) -> list[str]`

| Parameter | Meaning |
|-----------|---------|
| `data` | The full compressed code‑mix (plain text). |
| `max_symbols` | Approximate maximum character count that a single LLM request may contain (derived from the model’s token budget). |

**Logic flow**

1. **Initial line split** – `data.split("\n")` creates a list of logical lines (`splited_by_files`).  
2. **Oversize line handling** – A loop repeatedly checks each line; if a line exceeds `1.5 × max_symbols` it is broken in half (using `int(max_symbols/2)`) and the two halves are re‑inserted. This guarantees no individual element is dramatically larger than the budget.  
3. **Chunk assembly** – A second pass walks the (now‑sanitized) line list, concatenating lines into `split_objects`. A new chunk starts when the current chunk would exceed `1.25 × max_symbols`. Newlines are preserved.  

**Output** – A list of strings, each guaranteed to be ≤ ≈ `max_symbols` characters, ready for a single LLM call.

**Assumptions & side‑effects**

* Input is plain‑text; no binary data is expected.  
* The function never performs I/O; it works purely in memory.  
* It assumes `"\n"` is the line delimiter used throughout the pipeline.

---

<a name="write_docs_by_parts"></a>
### `write_docs_by_parts(part: str, model: Model, global_info: str, prev_info: str = None, language: str = "en") -> str`

**Responsibility**  
Builds a prompt for the *part‑completion* LLM and returns the model’s raw answer stripped of surrounding markdown fences.

**Prompt composition**

| Message role | Content |
|--------------|---------|
| `system` | “For the following task use language {language}”. |
| `system` | `BASE_PART_COMPLITE_TEXT` (static instruction fragment from `engine.config`). |
| `user`   | The current code chunk (`part`). |
| *(optional)* `system` | “it is last part of documentation that you have write before{prev_info}” – provides continuity when `prev_info` contains the previous chunk’s output. |
| `user`   | The same `part` again (keeps the user‑side payload at the end of the list). |

The model is called via `model.get_answer_without_history(prompt=prompt)`.  
If the answer is wrapped in triple back‑ticks, they are removed; otherwise the raw answer is returned.

**Inputs / Outputs**

* `part` – a single chunk from `split_data`.  
* `model` – any concrete implementation of `engine.models.gpt_model.Model` (sync).  
* `global_info` – currently unused (commented out) but reserved for future global context.  
* `prev_info` – the tail of the previous answer (up to ~3000 chars) to keep the narrative consistent.  
* Returns a markdown‑ready string (code fences stripped).

**Side‑effects** – None; the function only builds data structures and calls the LLM.

---

<a name="async_write_docs_by_parts"></a>
### `async_write_docs_by_parts(...) -> Awaitable[str]`

Same semantics as `write_docs_by_parts` but:

* Accepts an `AsyncModel` instance and runs `await async_model.get_answer_without_history`.  
* Executes inside an `asyncio.Semaphore` supplied by the caller, limiting concurrent LLM requests (default 4 in `async_gen_doc_parts`).  
* Optionally calls `update_progress()` after the model response to drive UI progress bars.

All other behaviours (prompt layout, fence stripping) are identical.

---

<a name="gen_doc_parts"></a>
### `gen_doc_parts(full_code_mix, global_info, max_symbols, model, language, progress_bar) -> str`

**Workflow**

1. `split_data` → list of chunks.  
2. `progress_bar.create_new_subtask` registers a sub‑task whose length equals the number of chunks.  
3. Iterates over chunks:
   * Calls `write_docs_by_parts` with the current chunk, the model, and the previous chunk’s tail (`result`).  
   * Appends the returned markdown to `all_result`.  
   * Truncates `result` to its last 3000 characters (kept for continuity).  
   * Updates the UI progress bar.  
4. Removes the sub‑task and returns the concatenated documentation.

**Assumptions**

* `progress_bar` implements the `BaseProgress` interface (create/update/remove sub‑tasks).  
* The model respects the token budget implied by `max_symbols`.

---

<a name="async_gen_doc_parts"></a>
### `async_gen_doc_parts(...) -> Awaitable[str]`

Parallel version of `gen_doc_parts`:

* Splits the input once.  
* Creates a semaphore (`max 4 concurrent calls`).  
* Launches an `async_write_docs_by_parts` task for each chunk, passing a lambda that updates the progress bar.  
* Awaits `asyncio.gather` to collect all answers, concatenates them with double newlines, and cleans up the progress UI.

**Interaction with the Rest of the System**

* **Compression Stage** – Receives the output of `compress_to_one` (a single large string).  
* **DocFactory / UI** – The returned markdown is fed to the final document assembler, which adds the table‑of‑contents (from `get_all_topics`) and introductory sections.  
* **Configuration Layer** – Prompt fragments (`BASE_PART_COMPLITE_TEXT`) are centrally defined; any change propagates automatically.  
* **Model Layer** – Both sync and async model classes live in `engine.models.gpt_model`; this module treats them uniformly via the `Model`/`AsyncModel` abstractions.

---

### Key Takeaways for New Developers

* The module’s **only external side‑effects** are LLM API calls and UI progress updates.  
* All chunk‑splitting logic is deterministic and pure; you can safely unit‑test `split_data` with various `max_symbols`.  
* When extending the pipeline (e.g., adding a new system prompt), modify `BASE_PART_COMPLITE_TEXT` or adjust the `prompt` construction in the two “write” functions.  
* For higher throughput, tune the semaphore limit in `async_gen_doc_parts` according to your LLM provider’s rate limits.  

**Module:** `autodocgenerator.ui.progress_base`  
*(UI‑level helpers that expose a tiny, test‑friendly progress‑tracking API for the rest of the documentation‑generation pipeline.)*  

<a name="overview"></a>
## Overview
This file defines a very small abstraction layer over **Rich**’s `Progress` object.  
The rest of the system (e.g. the doc‑generation workers in `autodocgenerator.core`) never talks to Rich directly – they depend only on the `BaseProgress` protocol.  
`LibProgress` is the concrete implementation used by the CLI, while the abstract base makes it trivial to swap in a mock progress reporter for unit‑tests.

<a name="baseprogress"></a>
## `BaseProgress` (abstract protocol)

| Method | Purpose | Expected behaviour |
|--------|---------|--------------------|
| `create_new_subtask(name: str, total_len: int)` | Starts a *sub‑task* that represents the processing of a single chunk of code (e.g. one call to the LLM). | Returns nothing; the concrete class should store an identifier for later updates. |
| `update_task()` | Advances the *currently active* task by one step. | If a sub‑task is active it is advanced, otherwise the global “General progress” task is advanced. |
| `remove_subtask()` | Marks the current sub‑task as finished and discards its handle. | After this call `update_task()` will affect the base task again. |

`BaseProgress` contains only the method signatures (implemented as `...`). It is deliberately lightweight – no state, no Rich dependency – so that test doubles can inherit from it and override the methods.

<a name="libprogress"></a>
## `LibProgress` (Rich‑backed implementation)

```python
class LibProgress(BaseProgress):
    def __init__(self, progress: Progress, total: int = 4):
        …
```

### Constructor
* **`progress`** – an already‑configured `rich.progress.Progress` instance (usually created in the CLI entry‑point).  
* **`total`** – the expected number of *top‑level* steps (default 4).  
* Creates a *base task* named **“General progress”** with the supplied total.  
* Initializes `_cur_sub_task` to `None`; this attribute holds the Rich task ID of the active sub‑task.

### `create_new_subtask(name, total_len)`
* Calls `self.progress.add_task(name, total=total_len)` and stores the returned task ID in `_cur_sub_task`.  
* The `total_len` argument is the number of incremental updates the sub‑task will receive (e.g. the number of code chunks).

### `update_task()`
* If a sub‑task is active (`_cur_sub_task` is not `None`) it advances that task by one unit.  
* Otherwise it advances the *base* task.  
* This design lets the higher‑level generator code treat both granular (per‑chunk) and overall progress uniformly.

### `remove_subtask()`
* Clears the reference to the current sub‑task, effectively signalling its completion.  
* No explicit call to `Progress.remove_task` is made – Rich automatically hides finished tasks; the UI only stops updating the sub‑task.

### Side‑effects
* **UI updates** – each call to `update_task` triggers a redraw of the Rich progress bar.  
* **State mutation** – internal task IDs are stored/cleared; no external data is modified.

<a name="interaction"></a>
## Interaction with the Rest of the System
1. **Doc‑generation workers** (`gen_doc_parts`, `async_gen_doc_parts`, etc.) receive a `BaseProgress` instance via dependency injection.  
2. Before processing a batch of code chunks they call `create_new_subtask` with a descriptive name (e.g. *“Generating docs for module X”*) and the number of chunks.  
3. After each LLM request they invoke `update_task()` – this drives the progress bar shown to the user.  
4. When the batch finishes they call `remove_subtask()` so that subsequent batches reuse the base task.  

Because the workers only depend on the abstract protocol, they can be exercised in tests with a **dummy progress** that simply records calls, keeping the test suite fast and deterministic.

<a name="extending"></a>
## Extending / Customising
* **Alternative UI back‑ends** – implement a new subclass of `BaseProgress` that forwards calls to `tqdm`, a web‑socket UI, or a logger.  
* **More detailed metrics** – add extra methods (e.g. `set_description`) to the abstract class and implement them in `LibProgress` using `Progress.update(task_id, description=…)`.  
* **Rate‑limit handling** – the progress layer is deliberately stateless; any throttling logic belongs in the model‑calling code, not here.

<a name="testing"></a>
## Testing Tips
```python
class DummyProgress(BaseProgress):
    def __init__(self):
        self.calls = []

    def create_new_subtask(self, name, total_len):
        self.calls.append(("create", name, total_len))

    def update_task(self):
        self.calls.append(("update",))

    def remove_subtask(self):
        self.calls.append(("remove",))
```
Inject `DummyProgress` into `gen_doc_parts` and assert the expected sequence of calls – this validates that the generation pipeline correctly reports progress without needing a terminal.

---

**Key Takeaway for New Developers**  
`progress_base.py` isolates UI concerns from the core documentation engine. By coding against `BaseProgress` you keep the generation logic pure, enable fast unit tests, and retain the flexibility to swap the visual progress implementation at runtime.

