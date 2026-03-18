**Project Overview – Auto Doc Generator**

| Section | Description |
|---------|-------------|
| **Project Title** | **Auto‑Doc‑Generator** |
| **Project Goal** | To automatically produce human‑readable Markdown documentation from an arbitrary codebase by orchestrating a sequence of pre‑processing, LLM‑driven generation, and post‑processing steps. The tool removes manual effort from developers, ensuring that every file, function, and class is described in a consistent, up‑to‑date format. |
| **Core Logic & Principles** | 1. **Configuration‑Driven Pipeline** – A YAML configuration (via `read_config()`) supplies ignore patterns, max‑symbols limits, intro flags, etc., which are encapsulated in `Config` and `StructureSettings`. <br>2. **Layered Architecture** – The workflow is split into distinct layers: <br>   * *Pre‑processing*: `Manager.generate_code_file()` → `Preprocessor.code_mix()` → `Preprocessor.spliter()` to tokenize the source into manageable parts while respecting ignore lists.<br>   * *LLM Generation*: `Manager.generete_doc_parts()` sends each part to a lightweight wrapper around the Grock API (`GPTModel` / `AsyncGPTModel`), which returns a Markdown snippet. <br>   * *Post‑processing*: A factory (`DocFactory`) constructs a sequence of `BaseModule` strategies (e.g., `IntroText`, `IntroLinks`, `CustomModule`) that mutate a `DocPart` object by appending or prepending context. <br>3. **Facade Pattern** – `Manager` presents a single surface for the entire workflow, handling caching, progress reporting (via `ConsoleGtiHubProgress`), and final persistence. <br>4. **Factory & Strategy Patterns** – `DocFactory` builds a composite documentation object by invoking all configured `BaseModule` subclasses, allowing extensible customization of the output. |
| **Key Features** | • **End‑to‑End CLI & GitHub Action entry point** (`python -m autodocgenerator.auto_runner.run_file`). <br>• **Customizable ignore rules** and file‑splitting logic. <br>• **Configurable document parts** (maximum symbols, intro rendering, global file usage). <br>• **LLM abstraction** (`GPTModel` / `AsyncGPTModel`) that supports synchronous or asynchronous calls. <br>• **Extensible post‑processing** through a plugin‑style `BaseModule` strategy list. <br>• **Progress visibility** via a console progress bar and a centralized logger (`BaseLogger`). <br>• **Caching and reporting**: generated docs stored in `.auto_doc_cache/output_doc.md`, optional `report.txt`. <br>• **Returnable Markdown string** from `gen_doc()` for further programmatic use. |
| **Dependencies** | • **Python 3.10+** <br>• **Pydantic** (schema validation: `schema.doc_schema`) <br>• **Grock API SDK** (or compatible LLM client) – accessed through `engine.models.gpt_model` <br>• **Rich / tqdm** (optional) – progress bar implementation `ui.progress_base` <br>• **PyYAML** – for parsing the YAML configuration <br>• **Standard library** modules: `logging`, `pathlib`, `os`, `re`, `json` | 

---

### Suggested Module Mapping for Diagram Generation

| Main Package | Primary Modules (≈ 2 k lines total) | Responsibility |
|--------------|------------------------------------|----------------|
| `autodocgenerator` | `auto_runner/run_file.py`, `manage.py`, `config.py`, `structure_settings.py`, `base_logger.py` | Entry point, facade, configuration handling |
| `autodocgenerator.preprocessor` | `spliter.py`, `code_mix.py`, `settings.py` | File parsing, code chunking, user‑defined settings |
| `autodocgenerator.engine.models` | `gpt_model.py` | LLM wrapper (`GPTModel`, `AsyncGPTModel`) |
| `autodocgenerator.factory` | `base_factory.py`, `modules/*.py` | Factory and strategy objects for post‑processing |
| `autodocgenerator.schema` | `doc_schema.py` | Pydantic data models (`DocInfo`, `DocPart`) |
| `autodocgenerator.ui` | `logging.py`, `progress_base.py` | Central logger, progress handling |
| `engine/config` | `config.py` | Environment‑derived API keys |
| `engine/utils` | `progress_bar.py` (optional) | Helper utilities |

These modules collectively illustrate the layered pipeline: configuration → pre‑processing → LLM call → factory post‑processing → final output, with cross‑cutting concerns handled by logging and progress utilities. Use this mapping to draft a hyper‑compressed architectural diagram.
## Executive Navigation Tree

- **Documentation Overview**
  - [architecture](#architecture)
  - [critical_constraints](#critical_constraints)
  - [limitations_and_future_development](#limitations_and_future_development)
  - [conclusion](#conclusion)

- **Performance & Scalability**
  - [security](#security)
  - [scalability](#scalability)
  - [performance](#performance)

- **Development Practices**
  - [testing](#testing)
  - [maintenance](#maintenance)
  - [logging-and-progress](#logging-and-progress)
    - [ui-logging](#ui-logging)
    - [ui-progress](#ui-progress)
    - [base-logger](#base-logger)

- **Data Handling**
  - [database](#database)
  - [data_contract](#data_contract)
  - [data-contract](#data-contract)
  - [dependencies](#dependencies)
  - [inputs_outputs_and_parameters](#inputs_outputs_and_parameters)
  - [inputs_outputs_and_side_effects](#inputs_outputs_and_side_effects)

- **Core Architecture**
  - [key_components_and_functionalities](#key_components_and_functionalities)
  - [technical_logic_flow](#technical_logic_flow)
  - [layered_approach](#layered_approach)

- **Design Patterns**
  - [factory_pattern](#factory_pattern)
  - [factory-generate-doc](#factory-generate-doc)
  - [gptmodel-class](#gptmodel-class)
  - [asyncgptmodel](#asyncgptmodel)
  - [parentmodel](#parentmodel)
  - [history-class](#history-class)
  - [codemix-class](#codemix-class)

- **Manager Modules**
  - [manager-class-responsibility](#manager-class-responsibility)
  - [manager-class-usage](#manager-class-usage)

- **Code Structure**
  - [code_structure](#code_structure)
  - [file-structure](#file-structure)
  - [init-method](#init-method)
  - [generate-code-file](#generate-code-file)
  - [generate-global-info](#generate-global-info)

- **Modules**
  - [base-module](#base-module)
  - [custommodule](#custommodule)
  - [custommodule-withoutcontext](#custommodule-withoutcontext)
  - [custom-intro-module](#custom-intro-module)
  - [docfactory](#docfactory)
  - [spliter-module](#spliter-module)
  - [compressor-module](#compressor-module)

- **Document Generation Flow**
  - [generate-doc-parts](#generate-doc-parts)
  - [gen-doc-parts](#gen-doc-parts)
  - [write-docs-by-parts](#write-docs-by-parts)
  - [order-documentation](#order-documentation)
  - [split-text-by-anchors](#split-text-by-anchors)
  - [split-data-function](#split-data-function)

- **Link Extraction & Patterns**
  - [\\\"?[^\\\"'>\\s]{6,200}\\\"?](#\\\"?[^\\\"'>\\s]{6,200}\\\"?)
  - [extract-links-from-start](#extract-links-from-start)
  - [\\\"?(.*?)\\\"?](#\\\"?(.*?)\\\"?)
  - [get-all-html-links](#get-all-html-links)
  - [get-links-intro](#get-links-intro)
  - [get-introdaction](#get-introdaction)
  - [get-order](#get-order)
  - [ignore-list](#ignore-list)

- **Interaction & Diagrams**
  - [module-interactions](#module-interactions)
  - [module-interactions-2](#module-interactions-2)
  - [interaction-diagram](#interaction-diagram)
  - [introlinks](#introlinks)
  - [introtext](#introtext)

- **Project Settings & Utilities**
  - [project-settings](#project-settings)
  - [install-workflow-with-scripts](#install-workflow-with-scripts)
  - [autodoc-generator-options](#autodoc-generator-options)
  - [cache-cleanup](#cache-cleanup)
  - [save-doc](#save-doc)
  - [CONTENT_DESCRIPTION](#CONTENT_DESCRIPTION)
  - [generate-custom-discription](#generate-custom-discription)
  - [generate-custom-discription-without](#generate-custom-discription-without)
  - [doc-schema](#doc-schema)
<a name="architecture"></a> Architecture: Auto Doc Generator - Layered + Factory Pattern
The architecture of the Auto Doc Generator project is based on a layered approach, with each layer having a specific responsibility. The layers are as follows:
- **Presentation Layer**: This layer is responsible for handling user input and displaying the generated documentation.
- **Application Layer**: This layer is responsible for coordinating the documentation generation process.
- **Business Layer**: This layer is responsible for generating the documentation.
- **Data Access Layer**: This layer is responsible for accessing the codebase and storing the generated documentation.

The project also uses a factory pattern to assemble the documentation parts into a single document. The factory pattern is used to create objects that have a common base class, but may have different implementations. In this case, the factory pattern is used to create documentation parts that have a common base class, but may have different implementations.

##
<a name="critical_constraints"></a> Critical Constraints
The critical constraints for the Auto Doc Generator project are as follows:
- **Configuration**: The `autodocconfig.yml` file must be present and valid.
- **Grock API Key**: A valid Grock API key must be provided.
- **Code Quality**: The code to generate documentation for must be of high quality and follow best practices.

##
<a name="limitations_and_future_development"></a> Limitations and Future Development
The limitations and future development of the Auto Doc Generator project are as follows:
- The project currently only supports Python codebases.
- The project currently only supports the Grock API for language model interactions.
- Future development could include supporting other programming languages and APIs.
- Future development could include improving performance and scalability.
- Future development could include adding more features, such as support for multiple documentation formats. 

##
<a name="conclusion"></a> Conclusion
In conclusion, the Auto Doc Generator project is a complex system that requires careful consideration of technical requirements, dependencies, APIs, database, security, scalability, performance, testing, and maintenance. The project has limitations and future development possibilities, but it has the potential to be a powerful tool for generating documentation for codebases. 

##
<a name="security"></a> Security
The security considerations for the Auto Doc Generator project are as follows:
- The project must handle API keys and other sensitive information securely.
- The project must validate user input to prevent security vulnerabilities.

##
<a name="scalability"></a> Scalability
The scalability considerations for the Auto Doc Generator project are as follows:
- The project must be able to handle large codebases and generate documentation efficiently.
- The project must be able to scale to meet the needs of large projects.

##
<a name="performance"></a> Performance
The performance considerations for the Auto Doc Generator project are as follows:
- The project must be able to generate documentation quickly and efficiently.
- The project must be able to handle large codebases and generate documentation without significant performance degradation.

##
<a name="testing"></a> Testing
The testing strategy for the Auto Doc Generator project is as follows:
- The project must have unit tests to ensure individual components are working correctly.
- The project must have integration tests to ensure the entire system is working correctly.
- The project must have performance tests to ensure the system can handle large codebases and generate documentation efficiently.

##
<a name="maintenance"></a> Maintenance
The maintenance strategy for the Auto Doc Generator project is as follows:
- The project must have a clear and concise code structure to make it easy to maintain.
- The project must have automated tests to ensure changes do not break the system.
- The project must have a clear and concise documentation to make it easy for new developers to understand the system. 

##
<a name="logging-and-progress"></a>  
## Logging & Progress Mechanisms

| Module | Purpose | Key Classes | Notes |
|--------|---------|-------------|-------|
| `autodocgenerator.ui.logging` | Singleton logger used across the pipeline | `BaseLogger` | Handles level‑controlled output and message formatting |
| `autodocgenerator.ui.progress_base` | Visual progress tracking for long‑running steps | `BaseProgress`, `LibProgress`, `ConsoleTask`, `ConsoleGtiHubProgress` | Provides a pluggable interface that supports Rich‑based bars and plain console counters |

---
<a name="ui-logging"></a>  
## UI Logging Module (`autodocgenerator.ui.logging`)

| Class | Purpose | Key Methods | Notes |
|-------|---------|-------------|-------|
| `BaseLog` | Base data class for log entries | `__init__(message, level)`<br>`format()`<br>`_log_prefix` property | Provides a timestamped prefix via `datetime.fromtimestamp(time.time())`. |
| `ErrorLog`, `WarningLog`, `InfoLog` | Sub‑classes that prepend a severity tag to the base format | `format()` | Severity strings: *ERROR*, *WARNING*, *INFO*. |
| `BaseLoggerTemplate` | Abstract logger that can be swapped at runtime | `log(log)`<br>`global_log(log)` | `global_log` respects `log_level` filtering: logs with level ≤ `log_level` or if `log_level` < 0. |
| `FileLoggerTemplate` | Writes logs to a file | `log(log)` | Appends `log.format()` with a newline. |
| `BaseLogger` | Singleton façade that delegates to a `BaseLoggerTemplate` | `set_logger(logger)`<br>`log(log)` | `__new__` guarantees a single instance; `log` forwards to the template’s `global_log`. |

### Interaction Flow

1. **Log creation**  
   ```python
   log = InfoLog("Initialization complete", level=1)
   ```
2. **Template selection** – user calls `BaseLogger.set_logger(FileLoggerTemplate('app.log', log_level=1))`.  
3. **Logging** – `BaseLogger().log(log)` triggers the template’s `global_log`, which in turn calls `log.format()` and writes the message to the configured destination.

### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `message` | `str` | Log payload | Human‑readable text. |
| `level` | `int` | Severity rank | Lower values denote more critical logs. |
| `log_prefix` | `str` | Timestamp string | Generated on demand. |
| `log_level` | `int` | Minimum level to output | Negative values bypass filtering. |

> **Critical** – `BaseLogger` is a *singleton*; any call to `BaseLogger()` returns the same instance. Use `set_logger` to change the underlying template once per application lifetime.

---
<a name="ui-progress"></a>  
## UI Progress Module (`autodocgenerator.ui.progress_base`)

The progress subsystem supplies lightweight visual feedback for CLI or GitHub Action runs, primarily used during `gen_doc_parts` and other long‑running phases.

### Core Classes

| Class | Purpose | Core Methods | Notes |
|-------|---------|--------------|-------|
| `BaseProgress` | Abstract interface | `create_new_subtask(name, total_len)`, `update_task()`, `remove_subtask()` | Default implementations are no‑ops; serves as a contract for concrete progress types. |
| `LibProgress` | Rich‑based visual bar | `create_new_subtask(name, total_len)`, `update_task()`, `remove_subtask()` | Uses `rich.progress.Progress`; tracks base task and optional subtasks. |
| `ConsoleTask` | Plain console counter | `start_task()`, `progress()` | Prints a textual percentage on each `progress()` call. |
| `ConsoleGtiHubProgress` | GitHub‑friendly console progress | `create_new_subtask(name, total_len)`, `update_task()`, `remove_subtask()` | Delegates to `ConsoleTask` or a default “General Progress” task. |

### Interaction Flow

1. **Initialization** – `ConsoleGtiHubProgress()` creates a generic task with `total = 4`.  
2. **Sub‑task creation** – `create_new_subtask('Splitting files', 10)` instantiates a `ConsoleTask`.  
3. **Progress updates** – `update_task()` increments the active sub‑task or the generic task if none exists.  
4. **Completion** – `remove_subtask()` resets the current task to `None`.

### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `name` | `str` | Task label | Displayed in console output. |
| `total_len` | `int` | Expected steps | Used to compute percent completion. |
| `current_len` | `int` | Internal counter | Incremented on each `progress()`. |
| `progress` | `float` | Percent completion | Calculated as `(current_len / total_len) * 100`. |

> **Warning** – The `BaseProgress` stub methods (`...`) indicate incomplete implementation; `LibProgress` and `ConsoleGtiHubProgress` provide concrete behavior.

---

### Relation to the Auto Doc Generator

* `BaseLogger` is invoked by almost every stage of the pipeline (e.g., `Manager.save()`, `Manager.generate_doc_parts()`).
* `ConsoleGtiHubProgress` drives the visual feedback during `gen_doc_parts`, `preprocessor.spliter()`, and `manager.factory_generate_doc()` steps.
* Both components share a common contract: they are lightweight, non‑blocking, and configurable via the global settings (`build_settings.log_level`, `progress_bar` type).

These modules form the foundation for consistent, level‑controlled logging and user‑friendly progress reporting throughout the Auto Doc Generator pipeline.
<a name="base-logger"></a>  
## `BaseLogger` – Singleton Message Dispatcher

**Functional Role**  
Centralizes log generation and dispatch in the Auto Doc Generator. Any component invoking `BaseLogger()` receives the same instance, guaranteeing consistent log formatting and level filtering.

### Interaction Flow
1. **Instantiation** – `logger = BaseLogger()` always returns the singleton.  
2. **Configuration** – `set_logger(template, log_level)` modifies the underlying formatter and the minimal severity threshold once per application lifetime.  
3. **Logging** – `logger.info(message)`, `logger.error(message)`, etc. route the payload to the configured destination (stdout, file, or GitHub Action output) after applying `log_prefix` and `log_level` checks.  
4. **Termination** – When the application finishes, the last log is flushed and the destination is closed (if applicable).

### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `message` | `str` | Log payload | Human‑readable text. |
| `level` | `int` | Severity rank | Lower values denote more critical logs. |
| `log_prefix` | `str` | Timestamp string | Generated on demand. |
| `log_level` | `int` | Minimum level to output | Negative values bypass filtering. |

> **Critical** – `BaseLogger` is a **singleton**; any call to `BaseLogger()` returns the same instance. Use `set_logger` to change the underlying template once per application lifetime.

---
<a name="database"></a> Database
The Auto Doc Generator project does not use a database.

##
<a name="data_contract"></a> Data Contract
The data contract for the Auto Doc Generator project is as follows:
- **Inputs**:
    - `autodocconfig.yml` file
    - Code to generate documentation for
- **Outputs**:
    - Generated documentation file
    - Log file (optional)
- **Side Effects**:
    - Writing to files
    - API calls to Grock

##
<a name="data-contract"></a>  
## Data Contract

| Input | Type | Role | Notes |
|-------|------|------|-------|
| `prompt` | `list[dict[str,str]]` | LLM messages | Optional when `with_history=True` |
| `with_history` | `bool` | Flag to include history | If `False`, uses supplied `prompt` |
| `model_name` | `str` | Current LLM | Selected from `regen_models_name` |
| `chat_completion` | `object` | Response | `chat_completion.choices[0].message.content` |
| `result` | `str` | Final answer | Returned to caller |

All interactions are synchronous; asynchronous logic is present only in the stub `AsyncGPTModel`.
<a name="dependencies"></a> Dependencies
The dependencies for the Auto Doc Generator project are as follows:
- `yaml`: For loading configuration settings from the `autodocconfig.yml` file.
- `grock`: For interacting with the Grock API.
- `python`: For running the project code.

## <a name="api"></a> API
The API used in the Auto Doc Generator project is as follows:
- `Grock API`: For generating documentation parts.

##
<a name="inputs_outputs_and_parameters"></a> Inputs, Outputs, and Parameters
The inputs, outputs, and parameters for the Auto Doc Generator project are as follows:
| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `autodocconfig.yml` file | File | Input | Configuration file for the project |
| Code to generate documentation for | Codebase | Input | The codebase to generate documentation for |
| Generated documentation file | File | Output | The generated documentation file |
| Log file | File | Output | The log file for the project |
| API key | String | Parameter | The API key for the Grock API |
| Language | String | Parameter | The language of the codebase |
<a name="inputs_outputs_and_side_effects"></a> Inputs, Outputs, and Side Effects
The inputs, outputs, and side effects for the Auto Doc Generator project are as follows:
- **Inputs**:
    - `autodocconfig.yml` file
    - Code to generate documentation for
- **Outputs**:
    - Generated documentation file
    - Log file (optional)
- **Side Effects**:
    - Writing to files
    - API calls to Grock

##
<a name="key_components_and_functionalities"></a> Key Components and Functionalities
The key components and their functionalities are as follows:
- `Manager` class: Coordinates the documentation generation process.
- `GPTModel` class: Wraps the Grock API for language model interactions.
- `DocFactory` class: Assembles documentation parts into a single document.
- `BaseModule` subclasses: Strategy objects for generating documentation parts.
- `preprocessor` subpackage: Contains classes for pre-processing, including code splitting and markdown cleaning.
- `postprocessor` subpackage: Contains classes for post-processing, including intro text and sorting.

##
<a name="technical_logic_flow"></a> Technical Logic Flow
The technical logic flow for the Auto Doc Generator project is as follows:
1. **Configuration**: The `autodocconfig.yml` file is read, and the configuration settings are loaded.
2. **Project Setup**: The project is set up, including the creation of the `Manager` instance.
3. **Pre-processing**: The pre-processing step involves splitting the code into parts, building LLM prompts, and cleaning markdown fences.
4. **LLM Generation**: The LLM generation step involves calling the Grock API to generate documentation parts.
5. **Post-processing**: The post-processing step involves assembling the documentation parts into a single document, including intro text and sorting.
6. **Final Save**: The final document is saved to a file.

##
<a name="layered_approach"></a> Layered Approach
The layered approach used in the Auto Doc Generator project is as follows:
- The **Presentation Layer** is responsible for handling user input and displaying the generated documentation.
- The **Application Layer** is responsible for coordinating the documentation generation process.
- The **Business Layer** is responsible for generating the documentation.
- The **Data Access Layer** is responsible for accessing the codebase and storing the generated documentation.

##
<a name="factory_pattern"></a> Factory Pattern
The factory pattern used in the Auto Doc Generator project is as follows:
- The `DocFactory` class is used to assemble documentation parts into a single document.
- The `BaseModule` subclasses are used to create documentation parts that have a common base class, but may have different implementations.

##
<a name="factory-generate-doc"></a>  
## `factory_generate_doc(doc_factory, to_start=False)`

| Step | Action | Notes |
|------|--------|-------|
| 1 | Build `info` dict: language, full_data, code_mix, global_info. |
| 2 | Log module names and input keys. |
| 3 | `doc_factory.generate_doc(info, llm_model, progress_bar)` → returns `DocHeadSchema`. |
| 4 | Prepend or append to `self.doc_info.doc` depending on `to_start`. |
| 5 | Update progress bar. |

---
<a name="gptmodel-class"></a>  
## GPTModel Class

`GPTModel` is the synchronous LLM wrapper used by the **Auto Doc Generator** to query the Groq API.  
It inherits from `Model`, which in turn implements the `ParentModel` abstract base that holds the common state (API keys, model ordering, and conversation history).  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `dict[str,str]` | API key dictionary | Loaded from `engine.config.config.API_KEYS` |
| `history` | `History` | Conversation context | Stored as a list of `{role, content}` dictionaries |
| `models_list` | `list[str]` | Ordered LLM names | Shuffled if `use_random=True` |
| `client` | `Groq` | Low‑level API client | Instantiated per `current_key_index` |
| `logger` | `BaseLogger` | Logging facility | Uses `InfoLog`, `ErrorLog`, `WarningLog` |

### Functional Flow
1. **Initialization**  
   - Calls `ParentModel.__init__`, shuffling `models_list` if requested.  
   - Instantiates a `Groq` client using the first API key.  

2. **generate_answer**  
   *Input* – `with_history` (default `True`) and optional `prompt`.  
   *Process* –  
   - If `with_history`, the message list is taken from `self.history.history`; otherwise from the supplied `prompt`.  
   - Enters a retry loop over `self.regen_models_name`.  
   - For each model name, attempts `client.chat.completions.create(...)`.  
   - On success, extracts the assistant content and logs the model used.  
   - On failure, logs a warning, switches to the next API key/model, and retries.  
   - If all combinations exhaust, raises `ModelExhaustedException`.  
   *Output* – The assistant’s answer as a `str`.  

3. **get_answer_without_history** – Delegates to `generate_answer(with_history=False, prompt)`.  
4. **get_answer** – Adds the user prompt to history, calls `generate_answer()`, then records the assistant response in history and returns it.

### Key Interactions
- **History** (`history.add_to_history`) is modified in `get_answer`.  
- **Logger** logs every major step (`InfoLog`, `WarningLog`, `ErrorLog`).  
- **API_KEYS** and **regen_models_name** drive the fallback strategy.  

---
<a name="asyncgptmodel"></a>  
## AsyncGPTModel Class

Placeholder inheriting from `AsyncModel`.  
No implementation is provided in the fragment; any call will return the stub `"answer"` defined in `AsyncModel.generate_answer`.  

---
<a name="parentmodel"></a>  
## ParentModel Abstract Base

Defines shared attributes and the contract for `generate_answer`, `get_answer_without_history`, and `get_answer`.  
Concrete subclasses (`Model`, `AsyncModel`) implement the synchronous and asynchronous variants.  
No logic is present in the abstract methods.

---
<a name="history-class"></a>  
## History Class

Maintains a mutable list of messages exchanged with the LLM.  

- **add_to_history(role, content)** appends a `{role, content}` entry.  
- Initialized with an optional system prompt (`BASE_SYSTEM_TEXT`).

---
<a name="codemix-class"></a>  
## `CodeMix` – Repository Content Builder

**Purpose**  
Walks a filesystem tree, filters files and directories based on a pattern list, and serializes the entire repository into a single markdown document.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `root_dir` | `str` | Base directory | Defaults to current working directory. |
| `ignore_patterns` | `list[str]` | Glob patterns to exclude | Used by `should_ignore`. |
| `ignore_list` | `list[str]` | Default ignore set | Provided at module level. |
| `content` | `list[str]` | Accumulated markdown lines | Joined with newline for output. |

### `__init__(root_dir, ignore_patterns)`

| Entity | Type | Role |
|--------|------|------|
| `root_dir` | `str` | Resolved to an absolute `Path`. |
| `ignore_patterns` | `list[str]` | Stored for subsequent filtering. |
| `logger` | `BaseLogger` | Used for logging ignored paths. |

### `should_ignore(path)`

| Entity | Type | Role |
|--------|------|------|
| `path` | `str` | File or directory path. |
| `relative_path` | `Path` | Path relative to `root_dir`. |
| `path_str` | `str` | String representation of `relative_path`. |

**Logic Flow**

1. Convert `path` to a `Path` relative to the repository root.  
2. Iterate over each `pattern` in `ignore_patterns`.  
3. Return `True` if:
   - `fnmatch.fnmatch(path_str, pattern)`
   - `fnmatch.fnmatch(os.path.basename(path_str), pattern)`
   - Any component of `path.parts` matches the pattern.  
4. If no pattern matches, return `False`.

> **Note** – The method assumes `path` is a `Path` object; otherwise a `TypeError` could occur.

### `build_repo_content()`

| Entity | Type | Role |
|--------|------|------|
| `content` | `list[str]` | Collects lines representing structure and file contents. |

**Logic Flow**

1. Append header `"Repository Structure:"`.  
2. Iterate over all entries (`rglob("*")`) sorted lexicographically:
   - If `should_ignore(path)` is `True`, log the ignore and continue.  
   - Compute `depth` relative to `root_dir`, calculate indentation, and append either a directory name ending with `/` or a file name.  
3. Append a separator `"="*20`.  
4. Perform a second traversal to append file bodies:
   - For each file not ignored:
     - Append `<file path="{relative_path}">` marker.  
     - Append the file’s text, reading with `encoding="utf-8", errors="ignore"`.  
     - Append a newline block `"\n\n"`.  
   - If reading fails, append an error notice.  
5. Return the joined string `"\n".join(content)`.

> **Side effect** – Generates a markdown string containing a directory tree followed by raw file contents wrapped in file tags.

---
<a name="manager-class-responsibility"></a>  
## Manager Class Responsibilities

**Role** – Central orchestrator that:  
1. Generates a *code mix* from the repository.  
2. Compresses the entire source into a single **global** Markdown description.  
3. Splits the code mix into manageable parts, runs LLM generation, and collects the results.  
4. Invokes a `DocFactory` to post‑process and assemble final documentation.  
5. Persists intermediate artefacts in `.auto_doc_cache`.

---
<a name="manager-class-usage"></a>  
The **Manager** class is instantiated with a project path, a `Config` object, an LLM model, and a progress bar. After creation, the following public methods can be invoked in sequence to produce documentation:

| Method | Purpose | Typical arguments | Example usage |
|--------|---------|-------------------|---------------|
| `generate_code_file()` | Scans the project and builds an internal representation of source files, respecting `ignore_files` in the config. | None | `manager.generate_code_file()` |
| `generate_global_info(compress_power: int)` | Builds a global information section (e.g., project overview) and compresses it with the provided power. | `compress_power` | `manager.generate_global_info(compress_power=4)` |
| `generete_doc_parts(max_symbols: int, with_global_file: bool)` | Splits the documentation into parts not exceeding `max_symbols` characters; optionally includes the global file. | `max_symbols`, `with_global_file` | `manager.generete_doc_parts(max_symbols=5000, with_global_file=True)` |
| `factory_generate_doc(factory: DocFactory, to_start: bool = False, with_splited: bool = True)` | Uses a `DocFactory` to create documentation blocks from supplied modules. `to_start=True` inserts the result at the beginning of the document. | `factory`, optional flags | `manager.factory_generate_doc(DocFactory(*custom_modules))` |
| `order_doc()` | Reorders document sections if the configuration demands an explicit order. | None | `manager.order_doc()` |
| `clear_cache()` | Deletes temporary cache files used during processing. | None | `manager.clear_cache()` |
| `save()` | Persists the generated documentation to the output destination. | None | `manager.save()` |

After all steps, the full documentation can be retrieved with:

```python
full_doc = manager.doc_info.doc.get_full_doc()
```

**Example Workflow**

```python
from autodocgenerator.auto_runner.run_file import gen_doc
from autodocgenerator.auto_runner.config_reader import read_config

# Read configuration from YAML
with open("autodocconfig.yml", "r", encoding="utf-8") as file:
    yaml_text = file.read()
config, custom_modules, structure_settings = read_config(yaml_text)

# Generate documentation
output = gen_doc(
    project_path=".",            # root of the project
    config=config,
    custom_modules=custom_modules,
    structure_settings=structure_settings
)

print(output)  # Full generated documentation
```

In this pattern:

1. `Manager` is created inside `gen_doc`.
2. Each method is called in order to build, split, and finalize the documentation.
3. Auxiliary modules (`IntroText`, `IntroLinks`) are added via `factory_generate_doc` after the main doc is assembled.
4. Finally, `manager.save()` writes the output and `manager.doc_info.doc.get_full_doc()` returns the complete string.
<a name="code_structure"></a> Code Structure
The code structure for the Auto Doc Generator project is as follows:
- The `autodocgenerator` package contains the main code for the project.
- The `config` package contains classes for loading and storing configuration settings.
- The `engine` package contains classes for interacting with the Grock API.
- The `factory` package contains classes for assembling documentation parts into a single document.
- The `manage` package contains classes for coordinating the documentation generation process.
- The `preprocessor` package contains classes for pre-processing, including code splitting and markdown cleaning.
- The `postprocessor` package contains classes for post-processing, including intro text and sorting.

##
<a name="file-structure"></a>  
## Cache File Mapping

| Key | File | Purpose |
|-----|------|---------|
| `code_mix` | `code_mix.txt` | Raw concatenated repository contents. |
| `global_info` | `global_info.md` | Single‑segment project overview produced by compression. |
| `logs` | `report.txt` | Structured log file written by `BaseLogger`. |
| `output_doc` | `output_doc.md` | Generated markdown (pre‑factory) and final cache. |

---
<a name="init-method"></a>  
## `__init__(project_directory, config, llm_model, progress_bar)`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_directory` | `str` | Repo root | Where all files are read/written. |
| `config` | `Config` | User settings | Includes `ignore_files`, `pbc.log_level`, etc. |
| `llm_model` | `Model` | LLM wrapper | Synchronous Grok interface. |
| `progress_bar` | `BaseProgress` | UI progress | Defaults to an empty instance. |

Creates the cache folder if missing, configures `BaseLogger` to write to `report.txt`.

---
<a name="generate-code-file"></a>  
## `generate_code_file()`

1. `CodeMix(self.project_directory, self.config.ignore_files).build_repo_content()`  
2. Stores result in `self.doc_info.code_mix`.  
3. Updates progress bar and logs the start/completion.  

> **Side Effect** – Populates `self.doc_info.code_mix` for downstream steps.

---
<a name="generate-global-info"></a>  
## `generate_global_info(compress_power=4, max_symbols=10000)`

| Step | Action | Notes |
|------|--------|-------|
| 1 | `split_data(self.doc_info.code_mix, max_symbols)` | Splits code mix into chunks. |
| 2 | `compress_to_one(data, self.llm_model, self.config.get_project_settings(), compress_power=compress_power, progress_bar=self.progress_bar)` | LLM compresses all chunks into a single string. |
| 3 | Write to `global_info.md`. | Persist compressed doc. |
| 4 | Update progress bar. | Logs progress. |

---
<a name="base-module"></a>  
## BaseModule

**Role** – Abstract strategy interface used by `DocFactory` to produce a single documentation fragment.  

| Method | Parameters | Return | Notes |
|--------|------------|--------|-------|
| `generate(info: dict, model: Model)` | `info` – data from the pipeline; `model` – synchronous `Model` instance | `str` – raw markdown of the part | Must be overridden; implementation omitted in this file. |

---
<a name="custommodule"></a>  
## CustomModule

**Purpose** – Generates a user‑defined description that incorporates the project's code mix.  

| Step | Action | Details |
|------|--------|---------|
| 1 | `split_data(info["code_mix"], max_symbols=5000)` | Breaks the combined code into manageable chunks. |
| 2 | `generete_custom_discription(..., self.discription, info["language"])` | Feeds chunks, the custom description, and language into the LLM wrapper. |
| 3 | Return LLM output. | Result is a string representing the module’s doc part. |

*Parameters*  
- `discription` (note the misspelling) – a user‑supplied prompt fragment.  

*Interaction* – Calls to `generete_custom_discription` belong to the `postprocessor.custom_intro` module.

---
<a name="custommodule-withoutcontext"></a>  
## CustomModuleWithOutContext

**Purpose** – Similar to `CustomModule`, but **excludes** the code mix from the LLM prompt.

| Step | Action | Details |
|------|--------|---------|
| 1 | `generete_custom_discription_without(model, self.discription, info["language"])` | Supplies only the description and language. |
| 2 | Return LLM output. | Result is a string for the documentation part. |

*Use‑case* – When the user wants a static section not tied to any code snippet.

---
<a name="custom-intro-module"></a>  
## Custom Intro Module – Documentation Generation Utilities  

**Purpose** – Provides helper functions that generate introductory content for auto‑generated documentation by querying an LLM (`Model`) and parsing HTML anchor tags.

---
<a name="docfactory"></a>  
## DocFactory

**Role** – Orchestrates the execution of multiple `BaseModule` instances, collects their outputs into a unified `DocHeadSchema`, and optionally splits each output into anchors.

### Initialization

| Attribute | Type | Notes |
|-----------|------|-------|
| `modules` | `list[BaseModule]` | Variadic collection of concrete modules supplied on construction. |
| `logger` | `BaseLogger` | Emits informational logs during generation. |
| `with_splited` | `bool` | Flag to control whether results are split by anchors via `split_text_by_anchors`. |

### generate_doc(info, model, progress) → `DocHeadSchema`

1. **Setup** – Creates a new sub‑task in `progress` for the number of modules.  
2. **Iterate Modules**  
   - Call `module.generate(info, model)`.  
   - If `with_splited` is `True`, split the returned string by anchors (`split_text_by_anchors`).  
   - Add each split part to `doc_head` with a key derived from the anchor name; otherwise use a synthetic task name.  
3. **Logging** – After each module, emit `InfoLog` with the class name and raw output (level 2).  
4. **Progress** – Increment sub‑task progress and finally remove it.  
5. **Return** – The populated `DocHeadSchema` instance.

> **Critical Logic**: The order of modules defines the order of parts in the final document; splitting preserves anchor hierarchy.

---
<a name="spliter-module"></a>  
## File Splitting Stub (`autodocgenerator.preprocessor.spliter`)

The provided fragment only shows the beginning of `split_data`. The function is intended to partition raw repository text into segments that respect `max_symbols`, preparing them for LLM ingestion. The logic is incomplete in the snippet, but the following is inferred:

| Function | Role | Notes |
|----------|------|-------|
| `split_data(data, max_symbols)` | Splits a string into chunks no longer than `max_symbols`. | Implementation uses `data.split(...)` and likely recursive or iterative logic to avoid cutting off in the middle of markdown fences. |

> **Information not present in the provided fragment** – Exact delimiter usage, handling of markdown fences, and return type beyond a list of strings.  

---
<a name="compressor-module"></a>  
## Compression Pipeline (`autodocgenerator.preprocessor.compressor`)

### `compress(data, project_settings, model, compress_power)`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Full text chunk to compress | Raw LLM prompt target |
| `project_settings` | `ProjectSettings` | Supplies base prompt via `project_settings.prompt` | See **Project Settings Prompt Builder** below |
| `model` | `Model` | LLM interface | Must implement `get_answer_without_history` |
| `compress_power` | `int` | Power of compression | Influences length of compressed output |

**Logic Flow**

1. Assemble a three‑message **ChatGPT** prompt:  
   * System: global project description (`project_settings.prompt`).  
   * System: a compression instruction string produced by `get_BASE_COMPRESS_TEXT(len(data), compress_power)`.  
   * User: the raw `data`.  
2. Call `model.get_answer_without_history(prompt=prompt)` to obtain the compressed fragment.  
3. Return the resulting string.

> **Important** – The function expects `model` to provide a stateless `get_answer_without_history` interface. No retry logic is performed here.

### `compress_and_compare(data, model, project_settings, compress_power=4, progress_bar=BaseProgress())`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | List of file contents or text chunks | Each element is a separate chunk |
| `model` | `Model` | LLM interface | Same as above |
| `project_settings` | `ProjectSettings` | Prompt provider | Same as above |
| `compress_power` | `int` | Grouping factor | Determines how many chunks are fused before compression |
| `progress_bar` | `BaseProgress` | Progress visualizer | Default instance used when none supplied |

**Logic Flow**

1. Create `compress_and_compare_data`, a list pre‑filled with empty strings sized `ceil(len(data)/compress_power)`.  
2. Start a sub‑task in `progress_bar` labeled `"Compare all files"`.  
3. Iterate over `data`; for each element `el` at index `i`:  
   * Compute `curr_index = i // compress_power`.  
   * Concatenate `compress(el, …)` into the corresponding group with a newline separator.  
   * Update the progress bar.  
4. Remove the sub‑task once finished.  
5. Return the list of compressed groups.

> **Note** – This routine aggregates multiple file contents into a smaller set of compressed texts that can be later fed to the LLM for holistic analysis.

### `compress_to_one(data, model, project_settings, compress_power=4, progress_bar=BaseProgress())`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | List of compressed groups | Produced by `compress_and_compare` |
| `model` | `Model` | LLM interface | Same as above |
| `project_settings` | `ProjectSettings` | Prompt provider | Same as above |
| `compress_power` | `int` | Power of compression | Reused in each iteration |
| `progress_bar` | `BaseProgress` | Progress visualizer | Default instance used |

**Logic Flow**

1. Initialize `count_of_iter = 0`.  
2. While more than one string remains in `data`:  
   * If `len(data)` is less than `compress_power + 1`, set `new_compress_power = 2` to avoid trivial groups.  
   * Replace `data` with the result of `compress_and_compare(data, …, new_compress_power, progress_bar)`.  
   * Increment iteration counter.  
3. After convergence, return the single remaining element (`data[0]`).

> **Side Effect** – This function reduces an arbitrary number of text fragments into a single compressed string, suitable for passing to the final documentation generation step.

---
<a name="generate-doc-parts"></a>  
## `generete_doc_parts(max_symbols=5_000, with_global_file=False)`

1. Reads `global_info.md` (overrides `with_global_file`).  
2. Calls `gen_doc_parts(full_code_mix, max_symbols, llm_model, config, language, progress_bar, global_info=global_file)`.  
3. Saves raw output to `output_doc.md`.  
4. Splits by anchor tags: `split_text_by_anchors(result)`.  
5. Populates `self.doc_info.doc` with `DocContent` per anchor.  

---
<a name="gen-doc-parts"></a>  
## `gen_doc_parts` – Orchestrating Multi‑Part Documentation Generation (autodocgenerator.preprocessor.spliter)

**Role**  
Splits the entire codebase mix into manageable parts and sequentially generates documentation for each, maintaining context by passing the last 3 k characters of the previous answer.

| Parameter | Type | Role | Notes |
|-----------|------|------|-------|
| `full_code_mix` | `str` | Unprocessed repository string | Source for `split_data`. |
| `max_symbols` | `int` | Chunk size limit | Propagates to `split_data`. |
| `model` | `Model` | LLM wrapper | Drives `write_docs_by_parts`. |
| `project_settings` | `ProjectSettings` | Project metadata | Injected into each prompt. |
| `language` | `str` | Language hint | Passed to LLM. |
| `progress_bar` | `BaseProgress` | UI progress control | Subtask created per call. |
| `global_info` | `str | None` | Optional relations | Forwarded to each part. |

| Output | Type | Role | Notes |
|--------|------|------|-------|
| `all_result` | `str` | Concatenated documentation | Final markdown for the project. |

**Flow**  
1. `split_data(full_code_mix, max_symbols)` → `splited_data`.  
2. Create a subtask in `progress_bar`.  
3. Iterate over `splited_data`:  
   * Call `write_docs_by_parts` with current part, previous result slice (last 3 k chars) and other params.  
   * Append returned text to `all_result`.  
   * Trim `result` to 3 k chars for next iteration.  
   * Advance progress bar.  
4. Remove subtask, log total length, return `all_result`.  

> **Critical note** – The `prev_info` parameter carries a sliding window of the most recent 3 k characters to preserve LLM context without exceeding token limits.

---
<a name="write-docs-by-parts"></a>  
## `write_docs_by_parts` – LLM Prompt Assembly & Retrieval (autodocgenerator.preprocessor.spliter)

**Role**  
Generates a single documentation block for a code fragment by crafting a multi‑system prompt and invoking the LLM via `Model.get_answer_without_history`.

| Parameter | Type | Role | Notes |
|-----------|------|------|-------|
| `part` | `str` | Code fragment to describe | Sent as *user* content. |
| `model` | `Model` | LLM interface | Calls `get_answer_without_history`. |
| `project_settings` | `ProjectSettings` | Provides project‑wide metadata | `project_settings.prompt` is embedded as a system message. |
| `prev_info` | `str | None` | Context from preceding part | Passed only if not `None`. |
| `language` | `str` | Language hint for the LLM | Defaults to `"en"`. |
| `global_info` | `str | None` | Global relation text | Optional. |

| Output | Type | Role | Notes |
|--------|------|------|-------|
| `answer` | `str` | Raw LLM response | May contain markdown fences. |

**Process**  
1. Build a *system* prompt array with language, project metadata, and `BASE_PART_COMPLITE_TEXT`.  
2. Append optional global and previous‑part context.  
3. Append the actual `part` as *user* content.  
4. Call `model.get_answer_without_history(prompt)`.  
5. Strip leading/trailing triple backticks if present, returning cleaned text.  

> **Warning** – If the response does not start with a fence, the function returns it unchanged; otherwise fences are removed to keep output clean.

---
<a name="order-documentation"></a>  
## `order_doc()`

Invokes `get_order(self.llm_model, self.doc_info.doc.content_orders)` to reorder sections based on LLM feedback, then writes back to `content_orders`.

---
<a name="split-text-by-anchors"></a>  
## `split_text_by_anchors(text)` – Anchor‑Based Document Segmentation

**Purpose**  
Partitions a raw markdown document into a dictionary mapping anchor identifiers to their associated content blocks.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `text` | `str` | Entire markdown document | Must contain `<a name>` tags. |
| `chunks` | `list[str]` | Raw split segments | Result of `re.split`. |
| `result_chanks` | `list[str]` | Non‑empty, trimmed chunks | Pre‑filtered for processing. |
| `all_links` | `list[str]` | Anchor URLs extracted by `extract_links_from_start` | Must match `result_chanks` count. |
| `have_to_del_first` | `bool` | Whether the first chunk is a leading anchor | Influences trimming of `result_chanks`. |
| `result` | `dict[str, str]` | Final mapping | Keys are anchors, values are associated content. |

**Logic Flow**

1. Compile `pattern = r'(?=<a name=["\']?[^"\'>\s]{6,200}["\']?></a>)'`.  
2. Split `text` on the pattern, trim each resulting chunk, filter empties → `result_chanks`.  
3. Call `extract_links_from_start(result_chanks)` to obtain `all_links` and `have_to_del_first`.  
4. If the original text contains `<a name>` after the 10th character or `have_to_del_first` is `True`, remove the first element of `result_chanks`.  
5. Verify that `len(all_links)` equals `len(result_chanks)`; otherwise raise `Exception("Somthing with anchors")`.  
6. Assemble `result` as a mapping of each anchor to its corresponding chunk.  
7. Return `result`.

> **Constraint** – This routine assumes that anchor names are unique and that every chunk begins with a matching anchor tag.

---
<a name="split-data-function"></a>  
## `split_data` – File Splitting Logic (autodocgenerator.preprocessor.spliter)

**Role**  
Partitions a raw repository string into a list of markdown‑friendly chunks that respect the *max_symbols* limit. The routine guarantees that each chunk will not be truncated in the middle of a token or fence by iteratively refining oversized parts.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `splited_by_files` | `list[str]` | Mutable buffer of raw file fragments | Initially produced by an earlier, unseen step. |
| `max_symbols` | `int` | Threshold for chunk length | Used twice: first for *safe* half‑split, then for final accumulation. |
| `split_objects` | `list[str]` | Resulting chunks | Each element is a concatenated string of one or more original fragments. |

> **Assumption** – The function receives a pre‑tokenized list; any markdown fence logic is handled elsewhere.  
> **Side effect** – Logs start/end of splitting and number of parts.

**Algorithm**  
1. **Iterative Refinement** – While any element exceeds `max_symbols*1.5`, the element is split roughly in half and re‑inserted.  
2. **Chunk Accumulation** – Elements are merged into `split_objects` until adding another would exceed `max_symbols*1.25`.  
3. **Return** – The final list of strings is returned.  

---
<a name="extract-links-from-start"></a>  
## `extract_links_from_start(chunks)` – Anchor Extraction Utility

**Purpose**  
Analyzes a sequence of markdown fragments and extracts HTML anchor names that start each chunk.  
It also determines whether the first chunk should be discarded when the overall document starts with an anchor.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `chunks` | `list[str]` | List of markdown chunks | Supplied by a higher‑level splitter. |
| `links` | `list[str]` | Collected anchor URLs | Formed as `#anchor_name`. |
| `have_to_del_first` | `bool` | Flag that the document does **not** begin with an anchor | Used by `split_text_by_anchors` to trim the first chunk. |
| `result` | `tuple[list[str], bool]` | Returned value | `(links, have_to_del_first)` |

**Logic Flow**

1. Initialise `links` and regex `pattern = r'^<a name=["\']?(.*?)["\']?></a>'`.  
2. Iterate over each `chunk` in `chunks`:  
   - Strip whitespace and search for a leading anchor tag.  
   - If a match is found and the captured anchor name length > 5, record the link (`#<anchor>`) and set `is_find` to `True`.  
   - If no anchor is present in a chunk, set `have_to_del_first` to `True`.  
3. Return the accumulated `links` and the flag.

> **Warning** – The function only matches anchors that appear at the very beginning of a chunk. It ignores any anchors that are nested or appear later within the text.

---
<a name="get-all-html-links"></a>  
## `get_all_html_links(data: str) → list[str]`

Extracts markdown anchor names from `data` and returns a list of link strings.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Input markdown source | Must contain `<a name="..."></a>` tags. |
| `links` | `list[str]` | Output | Each item prefixed with `#`. |

**Logic Flow**

1. Instantiates `BaseLogger` and logs start.  
2. Uses regex pattern `<a name=["\']?(.*?)["\']?</a>` to find all anchors.  
3. Filters names longer than 5 characters, converting them to `"#" + anchor_name`.  
4. Logs count and the list (debug level 1).  
5. Returns the list.

> **Side Effect** – Logs extraction progress only.

---
<a name="get-links-intro"></a>  
## `get_links_intro(links: list[str], model: Model, language: str = "en") → str`

Assembles a prompt for the LLM to produce a link‑rich introduction.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `links` | `list[str]` | Input link list | Generated by `get_all_html_links`. |
| `model` | `Model` | LLM wrapper | Must expose `get_answer_without_history`. |
| `language` | `str` | Optional language spec | Default `"en"`. |
| `intro_links` | `str` | Output | Generated introduction text. |

**Logic Flow**

1. Constructs a 3‑message prompt: system messages for language and `BASE_INTRODACTION_CREATE_LINKS` constant, user message containing `links`.  
2. Sends to `model.get_answer_without_history`.  
3. Logs generation stages.  
4. Returns the LLM reply.

---
<a name="get-introdaction"></a>  
## `get_introdaction(global_data: str, model: Model, language: str = "en") → str`

Generates a generic introduction from `global_data`.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `global_data` | `str` | Project‑wide description | Provided by calling context. |
| `model` | `Model` | LLM wrapper | Must expose `get_answer_without_history`. |
| `language` | `str` | Optional language spec | Default `"en"`. |
| `intro` | `str` | Output | Generated intro text. |

**Logic Flow**

1. Builds a 3‑message prompt: language system, `BASE_INTRO_CREATE`, user with `global_data`.  
2. Calls `model.get_answer_without_history` and returns the answer.

---
<a name="get-order"></a>  
## `get_order(model, chanks)` – Semantic Ordering of Titles

**Purpose**  
Delegates a semantic sort operation to a language‑model via a simple prompt, converting a list of titles into a sorted order.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | LLM wrapper | Must expose `get_answer_without_history`. |
| `chanks` | `list[str]` | Titles to order | Expected to be raw strings (no punctuation). |
| `prompt` | `list[dict]` | Prompt payload | One user message containing instructions and the title list. |
| `result` | `str` | Raw LLM answer | A comma‑separated list. |
| `new_result` | `list[str]` | Final sorted titles | Trims whitespace from each item. |

**Logic Flow**

1. Create a `BaseLogger` instance and log the start of ordering.  
2. Log the provided `chanks` at level 1.  
3. Compose a prompt that instructs the LLM to return a **comma‑separated** list of titles sorted semantically.  
4. Invoke `model.get_answer_without_history(prompt)` and capture the raw string.  
5. Split the result by commas, strip whitespace, and produce `new_result`.  
6. Log the final ordering.  
7. Return `new_result`.

> **Information not present in the provided fragment** – The exact structure of `Model`, the content of `BaseLogger`, and any error handling for a failed LLM call.

---
<a name="ignore-list"></a>  
## `ignore_list`

A hard‑coded list of glob patterns used to filter out non‑source files and temporary directories when generating repository content. Examples include `*.pyo`, `venv`, `.git`, `*.md`, etc.

> **Use** – Passed to `CodeMix` via the `ignore_patterns` argument.

---
<a name="module-interactions"></a>  
## Inter‑Module Interaction Summary

| Module | Functionality | Partner |
|--------|---------------|---------|
| `postprocessor.splitting` | Parses markdown by anchors and orders titles | `engine.models.model.Model` (LLM) |
| `preprocessor.code_mix` | Builds a text representation of a repo | `ui.logging.BaseLogger` (logging) |
| `ignore_list` | Provides default exclusion patterns | `CodeMix` |

> **Information not present in the provided fragment** – The definitions of `BASE_INTRO_CREATE_LINKS`, `BASE_INTRO_CREATE`, `BASE_CUSTOM_DISCRIPTIONS`; any external logging configuration beyond `BaseLogger`.

---
<a name="module-interactions-2"></a>  
## Inter‑Module Interaction Summary (Compression Layer)

| Module | Functionality | Partner |
|--------|---------------|---------|
| `compressor.compressor.compress` | Single‑chunk compression | `engine.models.model.Model` (LLM) |
| `compressor.compressor.compress_and_compare` | Group‑wise aggregation + progress | `BaseProgress`, `compress` |
| `compressor.compressor.compress_to_one` | Iterative reduction to single text | `compress_and_compare` |
| `preprocessor.settings.ProjectSettings` | Supplies prompt content | All compressor functions |
| `engine.config.config.get_BASE_COMPRESS_TEXT` | Generates compression instruction | `compress` |

> **Information not present in the provided fragment** – The definition of `get_BASE_COMPRESS_TEXT`, exact content of `BASE_SETTINGS_PROMPT`, and error handling inside the LLM calls.
<a name="interaction-diagram"></a>  
## Interaction Flow (High‑level)

1. **`DocFactory`** receives `info`, `model`, and `progress`.  
2. Iteratively invokes `generate()` on each `BaseModule`.  
3. Module outputs are optionally split and registered in `DocHeadSchema`.  
4. Progress bar and logger are updated after every module.  
5. Final `DocHeadSchema` is returned to the caller (typically `Manager.factory_generate_doc`).

All components are purely synchronous in this fragment; asynchronous behaviour is only hinted at in `AsyncGPTModel`, which is not used here.
<a name="introlinks"></a>  
## IntroLinks

**Purpose** – Produces a list of hyperlinks extracted from the full project data.

| Step | Action | Details |
|------|--------|---------|
| 1 | `get_all_html_links(info["full_data"])` | Parses all URLs from the project. |
| 2 | `get_links_intro(links, model, info["language"])` | Formats the links into a language‑appropriate markdown snippet using the LLM. |
| 3 | Return formatted string. | Acts as a header section in the final doc. |

---
<a name="introtext"></a>  
## IntroText

**Purpose** – Generates an introductory paragraph describing the entire project.

| Step | Action | Details |
|------|--------|---------|
| 1 | `get_introdaction(info["global_info"], model, info["language"])` | Feeds the global project metadata to the LLM to produce a prose summary. |
| 2 | Return the resulting markdown string. | Appears at the very start of the documentation. |

---

### Data Contract for `DocFactory.generate_doc`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `info` | `dict` | Source data from `Manager` | Contains keys: `code_mix`, `full_data`, `global_info`, `language`, etc. |
| `model` | `Model` | LLM interface | Synchronous wrapper around Grok. |
| `progress` | `BaseProgress` | UI progress bar | Used to track module execution. |
| `doc_head` | `DocHeadSchema` | Return container | Accumulates parts via `add_parts`. |
| `module_result` | `str` | Raw LLM output | May be split into sub‑parts. |

> **Side Effect** – Each module may produce logs; `progress` is updated accordingly.

---
<a name="project-settings"></a>  
## Project Settings Prompt Builder (`autodocgenerator.preprocessor.settings`)

### `ProjectSettings.__init__(project_name)`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_name` | `str` | Identifier for the target project | Appears in the LLM system message |
| `info` | `dict` | Dictionary of arbitrary key/value pairs | Added via `add_info` |

### `add_info(key, value)`

| Entity | Type | Role |
|--------|------|------|
| `key` | `any` | Metadata key |
| `value` | `any` | Corresponding metadata value |

> **Usage** – Store supplemental configuration such as `max_symbols`, `intro_enabled`, etc., to be injected into the LLM prompt.

### `prompt` (property)

| Output | Type | Role | Notes |
|--------|------|------|-------|
| `str` | Concatenated prompt | Base prompt for all compression/LLM calls | Includes `BASE_SETTINGS_PROMPT` + project name + any additional info |

**Logic Flow**

1. Start with the constant `BASE_SETTINGS_PROMPT` imported from configuration.  
2. Append a line `Project Name: {self.project_name}`.  
3. Iterate over `self.info`, adding `"{key}: {value}"` for each entry.  
4. Return the assembled string.

> **Note** – This property is read‑only; modifications to `info` must be done through `add_info`.

---
<a name="install-workflow-with-scripts"></a>  
To install, run the PowerShell script on Windows:  
`irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex`  

On Linux-based systems, execute:  
`curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash`  

For CI pipelines, create a secret named `GROCK_API_KEY` in GitHub Actions and set its value to the API key obtained from the Grock documentation site. This secret enables authentication for subsequent workflow steps.
<a name="autodoc-generator-options"></a>  
Project metadata – `project_name` and `language`.  
File exclusion – `ignore_files` holds glob patterns for items that should not be parsed, such as compiled Python files, cache directories, IDE settings, database files, logs, version‑control folders and markdown files.  
Build behavior – `build_settings` contains `save_logs` (boolean flag) and `log_level` (numeric level).  
Document layout – `structure_settings` includes flags for whether to add introductory links and text, whether to preserve ordering, whether to merge all output into a single file (`use_global_file`), and the maximum size of each documentation part (`max_doc_part_size`).  
Supplementary project context – `project_additional_info` allows a free‑text description of the overall idea.  
Custom description entries – `custom_descriptions` is a list of free‑text snippets that can explain installation steps, configuration guidelines, or usage of the Manager class, with example code where appropriate.
<a name="cache-cleanup"></a>  
## `clear_cache()`

Deletes `report.txt` if `config.pbc.save_logs` is `False`.

---
<a name="save-doc"></a>  
## `save()`

Writes `self.doc_info.doc.get_full_doc()` to `output_doc.md`.

---

### Interaction Flow (Manager ➜ External)

```
Manager
 ├─> CodeMix → repo → code_mix
 ├─> split_data → compressor → global_info
 ├─> gen_doc_parts → LLM → doc parts
 ├─> DocFactory → BaseModule chain → enhanced doc
 ├─> get_order → LLM → reordered sections
 └─> BaseLogger & BaseProgress → user feedback
```

All operations are synchronous; asynchronous LLM variants (`AsyncGPTModel`) are not employed here.
<a name="CONTENT_DESCRIPTION"></a>` | Enforced format in prompt. |

**Logic Flow**

1. Constructs a detailed system prompt enforcing strict tag placement and forbidding file names, extensions, generic terms, etc.  
2. Calls `model.get_answer_without_history`.  
3. Returns the raw output.

---

### Module Interaction Summary  

* All functions rely on a `BaseLogger` instance for informational logs.  
* LLM interactions are synchronous via `Model.get_answer_without_history`.  
* Constants (`BASE_INTRODACTION_CREATE_LINKS`, `BASE_INTRO_CREATE`, `BASE_CUSTOM_DISCRIPTIONS`) supply system messages; their content is not visible in this snippet.  
* Regular expressions are only used in `get_all_html_links`.

> **Information not present in the provided fragment** – definitions of the imported constants, structure of `Model`, or exact formatting of `global_data`.
<a name="generate-custom-discription"></a>  
## `generete_custom_discription(splited_data: str, model: Model, custom_description: str, language: str = "en") → str`

Iteratively requests a description of a `custom_description` within each chunk of `splited_data`.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `splited_data` | `str` | Code or documentation snippets | Expected iterable string of chunks. |
| `model` | `Model` | LLM wrapper | Must expose `get_answer_without_history`. |
| `custom_description` | `str` | Target text to describe | Human‑readable query. |
| `language` | `str` | Language | Default `"en"`. |
| `result` | `str` | First non‑empty LLM reply | Empty if no info found. |

**Logic Flow**

1. Iterates over each `sp_data` in `splited_data`.  
2. Builds a prompt with system messages for language, a precise technical analyst role, context block, and `BASE_CUSTOM_DISCRIPTIONS`.  
3. Sends to the model.  
4. Breaks when a result not containing “!noinfo” or “No information found” is received.  
5. Returns the first valid result (or empty string).

---
<a name="generate-custom-discription-without"></a>  
## `generete_custom_discription_without(model: Model, custom_description: str, language: str = "en") → str`

Produces a succinct, hyphenated summary without external links.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | LLM wrapper | Must expose `get_answer_without_history`. |
| `custom_description` | `str` | Target text to describe | Human‑readable query. |
| `language` | `str` | Language | Default `"en"`. |
| `result` | `str` | LLM response starting with `
<a name="doc-schema"></a>  
## Data Models (`autodocgenerator.schema.doc_schema`)

| Model | Purpose |
|-------|---------|
| `DocContent` | Holds a single markdown string (`content`). |
| `DocHeadSchema` | Manages ordered parts (`content_orders`) and a mapping (`parts`). Provides `add_parts`, `get_full_doc`, and additive operator. |
| `DocInfoSchema` | Aggregates global info, raw code mix, and the `DocHeadSchema` instance for a full documentation set. |

These Pydantic models enforce the structure of the documentation artifact that the higher‑level `Manager` ultimately saves.
