**Project Title**  
AutoDoc — Automatic Project Documentation Generator  

---

### Project Goal  
AutoDoc automatically produces high‑quality, up‑to‑date documentation for a codebase by combining source‑code analysis, large‑language‑model (LLM) text generation, and semantic embeddings. The tool scans all relevant files, extracts meaningful snippets, compresses and sorts them, and assembles a coherent document that can be written in one or more parts. It also intelligently decides whether regeneration is necessary by comparing the current repository state against a cached Git commit SHA.

---

### Core Logic & Principles  

| Layer | Responsibility | Key Components | Interaction Flow |
|-------|----------------|----------------|------------------|
| **Orchestrator** | Holds configuration, models, and mutable documentation state. | `Manager` – singleton‑like object that stores `config`, `llm_model`, `embedding_model`, a progress UI, and a mutable `doc_info` (`DocSchema`). | Every module receives a reference to the `Manager` so they can read/write documentation sections. |
| **Configuration** | Reads `autodocconfig.yml` and exposes runtime settings. | `ConfigReader` → `Config` & `StructureSettings`. | `Doc Factory` uses these settings to decide which modules to invoke and how large each part can be (`max_doc_part_size`, `include_intro_*`). |
| **Source‑Code Pipeline** | Pre‑processes repository files into chunks suitable for LLM consumption. | `preprocessor` → `code_mix` → `compressor` → `spliter` | `Manager.generate_code_file` orchestrates this chain, producing a list of code‑to‑text candidates. |
| **LLM & Embedding** | Transforms code snippets into natural‑language explanations and generates vector embeddings for semantic ordering. | `LLM Wrapper` (`GPTModel` → `sync_model`), `Embedding` (`embedding_model`). | `run_file.gen_doc` calls the LLM to produce text and the embedding model to produce vectors used later by the sorting logic. |
| **Semantic Ordering & Compression** | Sorts the generated text by meaning, compresses large sections, and splits the final output into manageable parts. | `Sorting`, `Compressor`, `split_text_by_anchors` | After the LLM produces a raw output, `sort_vectors`, `compress`, and `split_text_by_anchors` produce a clean, well‑structured document. |
| **Persistence & Incremental Regeneration** | Writes the final documentation and records the current Git commit for future change detection. | `check_git_status`, `should_change?`, `CacheSettings.last_commit` | The Manager checks if the repository state has changed before running a full pipeline. |
| **Factory Pattern** | Enables plug‑in of new documentation modules. | `Doc Factory`, `BaseModule` subclasses | Modules are dynamically aggregated and executed against the `Manager`, making the system highly extensible. |

The entire workflow can be started from the command line (`Auto Runner`) which instantiates the models, loads the configuration, and runs the full generation pipeline.

---

### Key Features  

* **Automated Doc Generation** – Scans all project files, ignoring patterns defined in the config, and produces natural‑language documentation.  
* **LLM‑Driven Text Generation** – Uses a GPT‑based wrapper to convert code snippets into explanatory text.  
* **Semantic Embedding & Ordering** – Generates vector embeddings for each section, sorts them by meaning, and splits long texts into logical anchors.  
* **Compression** – Compresses verbose outputs with a dedicated model to keep sections within user‑defined size limits (`max_doc_part_size`).  
* **Incremental Builds** – Checks the current Git SHA against a cached value to decide whether regeneration is needed, saving time on unchanged projects.  
* **Pluggable Module System** – Employs a factory pattern (`Doc Factory`) to allow developers to add custom processing modules without modifying core logic.  
* **Configurable Pipeline** – `autodocconfig.yml` controls language, ignore patterns, project name, thresholds, logging levels, and toggles such as `use_global_file` or `include_intro_*`.  
* **Cross‑Library Integration** – Built on top of `google.genai` for embeddings, `numpy` for vector operations, and standard libraries (`re`, `fnmatch`, `yaml`) for parsing and text manipulation.  
* **Progress Feedback** – Integrated progress bar to keep users informed during long runs.  

---

### Dependencies  

| Category | Library / Tool | Purpose |
|----------|----------------|---------|
| **Configuration** | `yaml` | Parse `autodocconfig.yml`. |
| **Git Integration** | `gitpython` or subprocess calls | Retrieve current commit SHA. |
| **LLM & Embeddings** | `google.genai` | Generate embeddings and LLM text. |
| **Numerics & Vector Ops** | `numpy` | Handle vector calculations (length, sorting). |
| **Text Processing** | `re`, `fnmatch` | Pattern matching, ignore list handling. |
| **CLI & UX** | `argparse`, `tqdm` | Command line interface & progress bar. |
| **Utilities** | `os`, `pathlib`, `logging` | File system operations, logging. |
| **Project Settings** | Custom modules (`projectsettings.py`) | Manage project‑level settings. |
| **Packaging** | `setuptools`/`pip` | Install the AutoDoc package. |

All dependencies are pure‑Python and available via `pip`. The project can be installed and run on any environment that has Python 3.10+ and the necessary credentials for the Google GenAI API.

---
## Executive Navigation Tree

📂 Git & Deployment  
- [#check-git-status-component](#check-git-status-component)  
- [#install_script](#install_script)  
- [#install_sh](#install_sh)  
- [#install-workflow-with-remote-scripts-and-github-secret](#install-workflow-with-remote-scripts-and-github-secret)  
- [#run-file-component](#run-file-component)  
- [#folder-system](#folder-system)  
- [#file-paths](#file-paths)  

📂 Configuration  
- [#config-reader-component](#config-reader-component)  
- [#projectsettings](#projectsettings)  
- [#autodoc-config-structure](#autodoc-config-structure)  
- [#dependencies](#dependencies)  
- [#cache_settings](#cache_settings)  

📂 Core Architecture  
- [#gpt-model-component](#gpt-model-component)  
- [#gptmodel-class](#gptmodel-class)  
- [#inputs-outputs](#inputs-outputs)  
- [#responsibility](#responsibility)  
- [#interaction](#interaction)  
- [#logic-flow](#logic-flow)  
- [#manager-class](#manager-class)  
- [#manager-class-usage](#manager-class-usage)  
- [#code-mix](#code-mix)  
- [#codemix-module](#codemix-module)  
- [#global-info](#global-info)  
- [#custom-intro](#custom-intro)  
- [#factory](#factory)  
- [#ordering](#ordering)  
- [#sorting-module](#sorting-module)  
- [#cleanup](#cleanup)  

📂 Data Processing  
- [#embedding](#embedding)  
- [#embedding-layer](#embedding-layer)  
- [#compressor-component](#compressor-component)  
- [#compressor-flow](#compressor-flow)  
- [#compress-function](#compress-function)  
- [#compress-and-compare-function](#compress-and-compare-function)  
- [#compress-to-one-function](#compress-to-one-function)  
- [#data-contracts](#data-contracts)  
- [#data-contract-summary](#data-contract-summary)  
- [#split_data](#split_data)  

📂 Logging & Error Handling  
- [#logging-and-errors](#logging-and-errors)  
- [#logging_component](#logging_component)  
- [#error-handling](#error-handling)  
- [#progress_component](#progress_component)  

📂 Documentation Generation  
- [#doc-parts](#doc-parts)  
- [#write_docs_by_parts](#write_docs_by_parts)  
- [#gen_doc_parts](#gen_doc_parts)  
- [#doc_content](#doc_content)  
- [#doc_head_schema](#doc_head_schema)  
- [#doc_info_schema](#doc_info_schema)
<a name="check-git-status-component"></a> Check Git Status Component
#### Description
The `check_git_status` function is a critical component in the Auto Doc Generator pipeline, responsible for determining whether the documentation needs to be regenerated based on Git repository changes.

#### Functional Flow
The function takes a `Manager` instance as input and performs the following steps:
1. Checks if the current GitHub event is a workflow dispatch. If so, it returns `True`, indicating that the documentation should be regenerated.
2. Retrieves the last commit hash from the `.auto_doc_cache_file.json` file.
3. Uses the `get_diff_by_hash` function to compare the current repository state with the last committed state, excluding Markdown files.
4. If the difference exceeds the threshold defined in the `Manager` instance's configuration or if the last commit hash is empty, it updates the last commit hash and returns `True`.
5. Otherwise, it returns `False`, indicating that the documentation does not need to be regenerated.

#### Code Structure
The `check_git_status` function is defined in the `autodocgenerator/auto_runner/check_git_status.py` file and relies on the following external dependencies:
* `subprocess` for executing Git commands
* `Manager` instance for accessing configuration and repository information
* `CacheSettings` for loading and updating the last commit hash

###
<a name="config-reader-component"></a> Config Reader Component
#### Description
The `config_reader` module is responsible for parsing the `autodocconfig.yml` file and extracting relevant configuration settings for the Auto Doc Generator.

#### Functional Flow
The `read_config` function takes the contents of the `autodocconfig.yml` file as input and performs the following steps:
1. Loads the configuration data using the `yaml` library.
2. Extracts the project name, language, ignore files, and build settings from the configuration data.
3. Creates a `Config` instance and populates it with the extracted settings.
4. Extracts custom module descriptions and creates a list of `BaseModule` instances.
5. Extracts structure settings and creates a `StructureSettings` instance.
6. Returns the `Config`, `BaseModule` list, and `StructureSettings` instance.

#### Code Structure
The `config_reader` module is defined in the `autodocgenerator/auto_runner/config_reader.py` file and relies on the following external dependencies:
* `yaml` for loading configuration data
* `Config` and `StructureSettings` for representing configuration settings
* `BaseModule` for creating custom module instances

###
<a name="projectsettings"></a>
## `ProjectSettings` – Metadata Container

* **Construction** – Instantiated with a mandatory `project_name`.  
* **Dynamic Properties** – `info` dictionary holds arbitrary key/value pairs that are appended to the prompt.  
* **`prompt` Property** – Concatenates:
  1. Global `BASE_SETTINGS_PROMPT` constant.
  2. `Project Name` line.
  3. One line per key/value in `info`.

| Method | Input | Output | Notes |
|--------|-------|--------|-------|
| `add_info(key, value)` | `str`, `Any` | None | Mutates `info` dictionary |
| `prompt` | None | `str` | Generated on each access |

---
<a name="autodoc-config-structure"></a>  
The file is a YAML document that defines several top‑level sections used by the documentation generator.

- **project_name** – Title of the project.  
- **language** – Language code for generated documentation.

- **ignore_files** – List of patterns (glob style) for files and directories that the tool should skip. Typical entries include compiled artefacts, virtualenv folders, IDE folders, databases, logs, and markdown files.

- **build_settings** – Controls the build process.  
  - *save_logs*: Boolean to keep log files.  
  - *log_level*: Integer indicating verbosity.  
  - *threshold_changes*: Numeric limit for what constitutes a significant change.

- **structure_settings** – Determines how the output is organized.  
  - *include_intro_links*: Add links at the beginning.  
  - *include_intro_text*: Add introductory text.  
  - *include_order*: Preserve ordering of elements.  
  - *use_global_file*: Reference a single global documentation file.  
  - *max_doc_part_size*: Size cap for individual documentation blocks.

- **project_additional_info** – Custom free‑form fields; here a key *global idea* contains a short project description.

- **custom_descriptions** – List of descriptive strings that can be injected into generated content, often containing instructions or explanations about installation scripts, environment secrets, or how to use certain classes or modules.
<a name="install_script"></a>
## `install.ps1` – CI Setup & Project Configuration

**Purpose**  
Automates creation of the GitHub Actions workflow file and a default `autodocconfig.yml` for a newly cloned project.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `$currentFolderName` | Variable | Project name | Derived from current folder, inserted into config |
| `.github/workflows/autodoc.yml` | Workflow file | Reusable workflow trigger | Points to Drag‑GameStudio/ADG reusable workflow |
| `autodocconfig.yml` | YAML | Runtime configuration | Contains ignore patterns, build and structure settings |

**Core Flow**

1. **Directory Creation** – `New-Item -ItemType Directory` ensures `.github/workflows/` exists.  
2. **Workflow Generation** – `$content` holds the workflow YAML; written via `Out-File`.  
3. **Configuration Generation** – `$configContent` is a multi‑line PowerShell string that populates `autodocconfig.yml`.  
4. **Feedback** – `Write-Host` signals completion.

> *The script uses here‑strings (`@'…'@` and `@"…@"`) to avoid variable interpolation.*

---

### Interaction with the Rest of the Pipeline

| Component | Interaction | Notes |
|-----------|-------------|-------|
| `BaseLogger` | Used by `DocFactory`, `Manager`, and other modules to emit status messages. | Singleton ensures a single logger instance. |
| `BaseProgress` subclasses | Employed by `Manager.generate_doc_parts` and `DocFactory` to report progress. | `LibProgress` is optional if Rich is available. |
| `install.ps1` | Pre‑runs during project bootstrap to provide CI hooks and configuration. | Generates files before `Auto Runner` is invoked. |

---

### Data Contract Summary

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `log.message` | `str` | Log text | Human‑readable |
| `log.level` | `int` | Severity threshold | Lower = less filtering |
| `log.file_path` | `str` | Target file for `FileLoggerTemplate` | Appended, UTF‑8 |
| `progress.total_len` | `int` | Sub‑task length | Updated per increment |
| `config.project_name` | `str` | Project identifier | Injected into config file |

The provided code contains no external library calls beyond standard library and `rich`; therefore, no external behavior assumptions are made.
<a name="install_sh"></a>
## `install.sh` – CI Setup & Runtime Configuration

**Purpose**  
Automates the creation of a GitHub Actions workflow (`autodoc.yml`) and a default `autodocconfig.yml` for a freshly cloned Auto‑Doc project. The script is executed during project bootstrap.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `.github/workflows` | Directory | Workflow host | Created if missing |
| `autodoc.yml` | YAML | Reusable workflow trigger | Uses `Drag‑GameStudio/ADG/.github/workflows/reuseble_agd.yml@main` |
| `autodocconfig.yml` | YAML | Runtime configuration | Populated with project name, language, ignore patterns, build and structure settings |
| `$currentFolderName` | Variable | Project identifier | Derived from the current working directory (`basename "$PWD"`) |
| `GROCK_API_KEY` | Secret | LLM API key | Referenced via `${{ secrets.GROCK_API_KEY }}` in the workflow |

### Core Flow

1. **Directory Preparation**  
   ```bash
   mkdir -p .github/workflows
   ```
   Guarantees the workflow folder exists.

2. **Workflow Generation**  
   - `cat <<EOF > .github/workflows/autodoc.yml` writes a minimal reusable workflow that triggers on `workflow_dispatch`.
   - The workflow file contains a placeholder for the `GROCK_API_KEY` secret.

3. **Configuration Generation**  
   - `cat <<EOF > autodocconfig.yml` creates a YAML file containing:
     - **project_name** – the folder name.
     - **language** – default `"en"`.
     - **ignore_files** – comprehensive list of patterns to skip during scanning.
     - **build_settings** – flags for log persistence and level.
     - **structure_settings** – toggles for introductory text, links, ordering, global file usage, and maximum document part size.

4. **User Feedback**  
   ```bash
   echo "✅ Done! .github/workflows/autodoc.yml has been created."
   echo "✅ Done! autodocconfig.yml has been created."
   ```

### Interaction with the Rest of the Pipeline

| Component | Interaction | Notes |
|-----------|-------------|-------|
| **Auto Runner** | Reads `autodocconfig.yml` during execution | Provides `Config` for module orchestration |
| **GitHub Actions** | `autodoc.yml` triggers the CI pipeline | Delegates to the reusable ADG workflow |
| **Manager** | Consumes `config.project_name` | Influences output directory and logging |

### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `autodoc.yml` | File | CI trigger | Contains `permissions`, `uses`, and `secrets` sections |
| `autodocconfig.yml` | File | Runtime config | Parsed by `Config Reader` to produce `Config` object |
| `project_name` | `str` | Identifier | Injected into config; used by `DocFactory` |
| `language` | `str` | Output language | `"en"` by default |
| `ignore_files` | `list[str]` | Skipped paths | Applied by `BaseLogger`/`Manager` when scanning repo |
| `build_settings` | `dict` | Build flags | `save_logs`, `log_level` |
| `structure_settings` | `dict` | Output layout flags | `include_intro_*`, `include_order`, `use_global_file`, `max_doc_part_size` |

> *The script uses Bash here‑strings (`@'…'@`/`@"…@"`) to prevent unintended variable interpolation inside the generated YAML.*
<a name="install-workflow-with-remote-scripts-and-github-secret"></a>  
The installation procedure uses two remote scripts – one for Windows PowerShell and one for Unix-like systems – accessed through short pipelines. For PowerShell you execute a command that downloads the script and runs it in one step. For Linux and macOS, a similar one-liner pulls the shell script and pipes it to the shell interpreter.  
In a Continuous‑Integration environment, you also need to provide an API key to the external service “Grock.” This is done by creating a repository secret called **GROCK_API_KEY** in GitHub Actions and assigning it the key obtained from the Grock documentation site. The secret is then referenced in workflow files so that the installation scripts can authenticate automatically.
<a name="run-file-component"></a> Run File Component
#### Description
The `gen_doc` function is the entry point for generating documentation using the Auto Doc Generator.

#### Functional Flow
The `gen_doc` function takes the project path, `Config`, `BaseModule` list, and `StructureSettings` instance as input and performs the following steps:
1. Creates a `GPTModel` instance for code-to-text generation and an `Embedding` instance for vector embeddings.
2. Creates a `Manager` instance with the provided configuration and models.
3. Checks if the documentation needs to be regenerated using the `check_git_status` function.
4. If regeneration is required, it generates code files, global information, and document parts using the `Manager` instance.
5. Applies custom modules and additional modules (e.g., intro text and links) to the document.
6. Creates an embedding layer, clears the cache, and saves the generated document.
7. Returns the generated document as a string.

#### Code Structure
The `gen_doc` function is defined in the `autodocgenerator/auto_runner/run_file.py` file and relies on the following external dependencies:
* `Manager` instance for accessing configuration and repository information
* `GPTModel` and `Embedding` for code-to-text generation and vector embeddings
* `Config` and `StructureSettings` for representing configuration settings
* `BaseModule` for creating custom module instances

### Data Contract
The following table summarizes the inputs, outputs, and parameters of the `gen_doc` function:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| project_path | string | input | project directory path |
| config | Config | input | project configuration |
| custom_modules | list[BaseModule] | input | custom module instances |
| structure_settings | StructureSettings | input | structure settings instance |
| output_doc | string | output | generated document |
| manager | Manager | parameter | manager instance |
| gpt_model | GPTModel | parameter | GPT model instance |
| embedding_model | Embedding | parameter | embedding model instance |

### Technical Logic Flow
The `gen_doc` function follows a linear logic flow, with each step building upon the previous one:
1. Create models and manager instance
2. Check if regeneration is required
3. Generate code files, global information, and document parts
4. Apply custom modules and additional modules
5. Create embedding layer, clear cache, and save document
6. Return generated document

Note that this logic flow assumes a linear execution path, with no branching or conditional statements that would alter the overall flow.

###
<a name="gpt-model-component"></a> GPT Model Component
#### Description
The `GPTModel` class is a key component of the Auto Doc Generator, responsible for generating human-like text based on a given prompt. It leverages the Groq API and various pre-trained models to produce high-quality text.

#### Functional Flow
The `GPTModel` class follows these steps to generate text:
1. Initialize the model with an API key, history, and a list of available models.
2. Set up the Groq client and logger.
3. When `generate_answer` is called, check if the history or prompt should be used.
4. Attempt to generate text using the current model. If it fails, try the next model in the list.
5. If all models fail, raise a `ModelExhaustedException`.
6. Log the generated answer and return it as a string.

#### Code Structure
The `GPTModel` class is defined in the `autodocgenerator/engine/models/gpt_model.py` file and relies on the following external dependencies:
* `Groq` and `AsyncGroq` for interacting with the Groq API
* `Model` and `AsyncModel` for inheritance and shared functionality
* `History` for storing and retrieving conversation history
* `BaseLogger` and log classes for logging events and errors

#### Data Contract
The following table summarizes the inputs, outputs, and parameters of the `GPTModel` class:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| api_key | string | input | Groq API key |
| history | History | input | conversation history |
| models_list | list[string] | input | list of available models |
| use_random | bool | input | whether to use a random model |
| prompt | list[dict[string, string]] | input | optional prompt to use instead of history |
| result | string | output | generated text |
| model_name | string | parameter | current model being used |
| client | Groq | parameter | Groq client instance |
| logger | BaseLogger | parameter | logger instance |

#### Technical Logic Flow
The `GPTModel` class follows a linear logic flow, with each step building upon the previous one:
1. Initialize the model and its dependencies.
2. Set up the Groq client and logger.
3. When `generate_answer` is called, determine which input to use (history or prompt).
4. Attempt to generate text using the current model.
5. If the model fails, try the next model in the list.
6. If all models fail, raise a `ModelExhaustedException`.
7. Log the generated answer and return it as a string.

Note that this logic flow assumes a linear execution path, with no branching or conditional statements that would alter the overall flow. However, the `generate_answer` method does contain a loop that will continue until a model successfully generates text or all models have been exhausted. 

> **Critical Logic Assumption:** The `GPTModel` class assumes that at least one model in the `models_list` will be available and functional. If all models fail, a `ModelExhaustedException` is raised, and the generator will not produce any text. 

> **Warning:** The `GPTModel` class uses a random model from the `models_list` if `use_random` is `True`. This may lead to inconsistent results if the models have different capabilities or biases.
<a name="gptmodel-class"></a>  
## GPTModel Class – Text Generation Engine  

**Location:** `autodocgenerator/engine/models/gpt_model.py`  
**Role in Pipeline:** Provides synchronous text generation to the rest of the Auto Doc Generator. It sits between the high‑level *DocFactory* and the Groq API, exposing a simple `generate_answer`, `get_answer_without_history`, and `get_answer` interface.  

---
<a name="inputs-outputs"></a>  
### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `str` | input | Groq API key supplied at construction. |
| `history` | `History` | input | Conversation log that may be prepended to each request. |
| `models_list` | `list[str]` | input | Ordered (or shuffled if `use_random=True`) list of model identifiers. |
| `use_random` | `bool` | input | Whether to randomise the model order on initialization. |
| `prompt` | `list[dict[str,str]]` | input | Optional override to the historical prompt. |
| `result` | `str` | output | Generated text returned by `generate_answer`. |
| `model_name` | `str` | parameter | Current model being attempted. |
| `client` | `Groq` | parameter | Low‑level client used for API calls. |
| `logger` | `BaseLogger` | parameter | Logger used for audit and error reporting. |

---
<a name="responsibility"></a>  
### Functional Responsibility  

The **GPTModel** orchestrates a fail‑over loop across a set of pre‑configured LLMs hosted on Groq. It:

1. **Initialises** a `Groq` client with the provided API key(s) and stores the model list.  
2. **Selects** the current model (potentially at random).  
3. **Builds** a prompt that may include the conversation `history` or a supplied `prompt`.  
4. **Invokes** the Groq API until a model returns a successful response or all options are exhausted.  
5. **Logs** the event and returns the raw text.

If the loop completes without success, a `ModelExhaustedException` is raised, aborting the documentation generation for that segment.

---
<a name="interaction"></a>  
### Visible Interactions  

- **With `History`** – appends user and assistant turns when `get_answer` is used.  
- **With `BaseLogger`** – records each attempt, success, or failure at the module level.  
- **With `Model` / `AsyncModel`** – inherits method signatures, enabling synchronous or asynchronous usage throughout the factory pipeline.  
- **With external API** – uses `Groq` (synchronous client) to send messages and receive completions.  

---
<a name="logic-flow"></a>  
### Technical Logic Flow

1. **Constructor**  
   - Copies `models_list`.  
   - If `use_random`, shuffles the list.  
   - Sets `current_model_index` and `current_key_index` to zero.  

2. **`generate_answer(with_history=True, prompt=None)`**  
   - If `with_history` and `prompt` is `None`, constructs a request from `self.history`.  
   - Otherwise, uses supplied `prompt`.  
   - Tries `client.generate` on `self.regen_models_name[self.current_model_index]`.  
   - On exception, increments `current_model_index` and retries.  
   - Continues until a model succeeds or the list is exhausted.  

3. **`get_answer_without_history(prompt)`**  
   - Calls `generate_answer(with_history=False, prompt=prompt)` and returns result.  

4. **`get_answer(prompt)`**  
   - Adds user turn to history.  
   - Calls `generate_answer()`.  
   - Adds assistant turn to history.  
   - Returns answer.  

> **Critical Logic Assumption:**  
> At least one model in `models_list` will be reachable; otherwise a `ModelExhaustedException` is raised.  

> **Warning:**  
> Random selection (`use_random=True`) introduces variability in model performance and output style, which may affect consistency of generated documentation.  

---

<a name="notes"></a>  
### Missing or Unimplemented Details  

- The actual HTTP/GRPC call syntax to `Groq` is not present in the provided snippet; implementation details are omitted.  
- Error handling for specific Groq responses is not shown.  
- No unit tests or configuration examples for `api_keys` are included in the fragment.  

---
<a name="manager-class"></a>
## Manager Class Overview

The **`Manager`** encapsulates the end‑to‑end workflow that transforms a project’s source code into a coherent markdown document.  
It owns the mutable **`doc_info`** schema, orchestrates the LLM and embedding pipelines, and writes intermediate artefacts into a hidden cache directory.

---

<a name="init"></a>
## Manager Initialization

```python
def __init__(self, project_directory: str,
             config: Config,
             llm_model: Model,
             embedding_model: Embedding,
             progress_bar: BaseProgress = BaseProgress())
```

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_directory` | `str` | Root of the target project | Path on disk |
| `config` | `Config` | Runtime configuration | Parsed from `autodocconfig.yml` |
| `llm_model` | `Model` | LLM wrapper | Handles generation requests |
| `embedding_model` | `Embedding` | Vector‑generation engine | Used later in `create_embedding_layer` |
| `progress_bar` | `BaseProgress` | UI progress indicator | Default is a dummy base class |

**Behaviour**  
- Instantiates a `DocInfoSchema`.  
- Sets up a file‑based `BaseLogger` writing to `<project>/.auto_doc_cache/report.txt`.  
- Invokes `init_folder_system()` to create cache artefacts.  

---
<a name="manager-class-usage"></a>  
The **Manager** class is used as the central orchestrator for generating documentation.  
It is instantiated with the project root, a configuration object, a language‑model instance, an embedding model, and a progress‑bar helper:

```python
sync_model = GPTModel(GROQ_API_KEYS, use_random=False)
embedding = Embedding(GOOGLE_EMBEDDING_API_KEY)

manager = Manager(
    project_path, 
    config=config,
    llm_model=sync_model,
    embedding_model=embedding,
    progress_bar=ConsoleGtiHubProgress(),
)
```

Typical lifecycle of a `Manager` instance in a script:

```python
# decide whether to regenerate documentation
if not check_git_status(manager):
    exit()

# 1. Produce a representation of the codebase
manager.generate_code_file()

# 2. Create a global summary file if enabled
if structure_settings.use_global_file:
    manager.generate_global_info(compress_power=4)

# 3. Split the documentation into manageable parts
manager.generete_doc_parts(
    max_symbols=structure_settings.max_doc_part_size,
    with_global_file=structure_settings.use_global_file,
)

# 4. Build the documentation using a factory of modules
manager.factory_generate_doc(DocFactory(*custom_modules))

# 5. Optionally order sections
if structure_settings.include_order:
    manager.order_doc()

# 6. Add intro elements
additionals = []
if structure_settings.include_intro_text:
    additionals.append(IntroText())
if structure_settings.include_intro_links:
    additionals.append(IntroLinks())
manager.factory_generate_doc(DocFactory(*additionals, with_splited=False), to_start=True)

# 7. Final touches
manager.create_embedding_layer()
manager.clear_cache()
manager.save()

# 8. Retrieve the assembled document
full_doc = manager.doc_info.doc.get_full_doc()
```

Key methods exposed by **Manager** (as used in the provided code):

| Method | Purpose |
|--------|---------|
| `generate_code_file()` | Scans the repository and generates internal code representations. |
| `generate_global_info(compress_power)` | Builds a global information file, optionally compressing it. |
| `generete_doc_parts(max_symbols, with_global_file)` | Splits documentation into parts limited by `max_symbols`. |
| `factory_generate_doc(factory, to_start=False)` | Generates documentation sections using a `DocFactory`. |
| `order_doc()` | Orders the generated documentation sections. |
| `create_embedding_layer()` | Builds embeddings for the documentation content. |
| `clear_cache()` | Clears temporary cache files. |
| `save()` | Persists all generated artifacts to disk. |
| `doc_info.doc.get_full_doc()` | Retrieves the full assembled document as a string. |
| `read_file_by_file_key(file_key, is_outside)` | Reads the content of a cached file. |
| `get_file_path(file_key, is_outside)` | Returns the absolute path to a file in the project or outside. |

These methods together allow a user to run the entire documentation generation pipeline programmatically, controlling which parts of the output to include and when to trigger regeneration based on git status.
<a name="folder-system"></a>
## Cache Folder Initialization

```python
def init_folder_system(self, project_directory)
```

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `CACHE_FOLDER_NAME` | `str` | Directory name | `.auto_doc_cache` |
| `FILE_NAMES` | `dict` | Map of artefact keys to filenames | e.g. `"logs": "report.txt"` |

Creates the cache folder and writes an empty `CacheSettings` JSON file when it does not yet exist.

---
<a name="file-paths"></a>
## File Path Resolution

```python
def get_file_path(self, file_key: str, is_outside: bool = False)
```

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_key` | `str` | Artifact identifier | Must exist in `FILE_NAMES` |
| `is_outside` | `bool` | Determines subfolder | `True` ⇒ project root |

Utility used by all file I/O operations; keeps the cache layout deterministic.

---
<a name="code-mix"></a>
## Code‑Mix Generation

```python
def generate_code_file(self)
```

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `cm` | `CodeMix` | Repository‑content builder | Configures with `config.ignore_files` |
| `code_mix` | `str` | Aggregated source | Stored in `doc_info.code_mix` |

**Logic Flow**  
1. Logs start message.  
2. Instantiates `CodeMix` with project directory and ignore patterns.  
3. Calls `build_repo_content()` to read repository files.  
4. Stores result, updates progress bar.  

---
<a name="codemix-module"></a>
## CodeMix Module: Repository Snapshot Generator

### Responsibility
`CodeMix` produces a textual representation of a project's directory tree and inlined file contents, respecting a user‑defined ignore list.

### Interaction with the Rest of the Pipeline
The generated string is typically fed into the *embedding* step where each file or section receives a semantic vector.  
Other components may write this snapshot to disk as part of the global doc structure.

### Core Methods

| Method | Entity | Type | Role | Notes |
|--------|--------|------|------|-------|
| `__init__` | `root_dir`, `ignore_patterns` | `Path`, `list[str]` | Initializes state | Defaults to current directory; `ignore_patterns` are used in `should_ignore` |
| `should_ignore` | `path` | `Path` | Returns `bool` | Uses `fnmatch` against full path, basename, and individual parts |
| `build_repo_content` | — | — | Generates the repo snapshot | Emits logs for ignored items; collects file contents in a formatted string |

#### `should_ignore`

1. Convert `path` to a relative path under `root_dir`.  
2. Iterate over `ignore_patterns`.  
3. Return `True` if any pattern matches the relative path, the filename, or any component of the path.  
4. Otherwise, return `False`.

#### `build_repo_content`

1. Begin with the header `"Repository Structure:"`.  
2. Recursively walk `root_dir` (sorted) and append indented directory/file names.  
3. Append a separator line.  
4. Walk again to embed file contents:
   * For each file that is not ignored, append `<file path="relative/path">`, its decoded text, and a newline separator.  
   * Capture any exceptions while reading and append an error message.  
5. Join all entries with `"\n"` and return the final string.

### Global Ignore List

The module ships with `ignore_list`, a predefined set of glob patterns targeting compiled artifacts, virtual environments, cache directories, and other non‑source files.  
The list is applied during `should_ignore`.

---
<a name="global-info"></a>
## Global Information Compression

```python
def generate_global_info(self, compress_power: int = 4, max_symbols: int = 10000)
```

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `compress_power` | `int` | Aggressiveness of LLM compression | Default 4 |
| `max_symbols` | `int` | Chunk size for `split_data` | Default 10 k |

**Workflow**  
1. Splits `doc_info.code_mix` into symbols with `split_data`.  
2. Calls `compress_to_one()` (LLM‑powered) with `compress_power`.  
3. Writes the resulting markdown to `global_info.md`.  

The compressed text becomes a contextual backdrop for subsequent section generation.

---
<a name="custom-intro"></a>
## Custom Introduction Processor

The *Custom Introduction Processor* is a lightweight post‑processing module that builds the introductory text of a generated documentation file.  
It extracts anchor links, generates introductory paragraphs with or without link lists, and produces custom description blocks for individual sections.

### Functional Flow

1. **`get_all_html_links`**  
   Scans a markdown string for `<a name="…">` tags, collects anchor names longer than five characters, prefixes each with `#`, and returns a list.  
   *Logging:* Uses `BaseLogger` to trace extraction count.

2. **`get_links_intro`**  
   Accepts the list from `get_all_html_links`, builds a chat‑style prompt and forwards it to an LLM (`Model` interface).  
   The LLM is instructed to create a short introductory paragraph that references the provided anchors.

3. **`get_introdaction`**  
   Generates a generic introduction from a global data block (typically the entire repository summary).  
   A system prompt specifies the target language and a base introduction template (`BASE_INTRO_CREATE`).

4. **`generete_custom_discription`**  
   Iterates over a string of split data (each part representing a documentation chunk).  
   For every chunk it constructs a prompt that includes the chunk as context, a system instruction to produce a precise technical description, and a user‑supplied description template (`custom_description`).  
   The first non‑empty, non‑“no‑info” response is returned; otherwise an empty string is produced.

5. **`generete_custom_discription_without`**  
   Builds a single LLM prompt that forces a **one‑time** `<a name="CONTENT_DESCRIPTION">` header, then generates a short hyphenated summary of the supplied text.  
   The function returns the LLM answer verbatim.

### Data Contract

| Function | Entity | Type | Role | Notes |
|----------|--------|------|------|-------|
| `get_all_html_links` | `data` | `str` | Markdown source | Returns a list of `#anchor` strings |
|  | `links` | `list[str]` | Result | Exposed for further processing |
| `get_links_intro` | `links` | `list[str]` | Anchor list | Passed to LLM |
|  | `model` | `Model` | LLM wrapper | Must expose `get_answer_without_history` |
|  | `language` | `str` | Optional | Defaults to `"en"` |
|  | `intro_links` | `str` | Generated intro | Contains links in markdown |
| `get_introdaction` | `global_data` | `str` | Global summary | Text passed to LLM |
|  | `model` | `Model` | LLM wrapper | Same as above |
|  | `language` | `str` | Optional | Defaults to `"en"` |
|  | `intro` | `str` | Generated paragraph | Returned directly |
| `generete_custom_discription` | `splited_data` | `str` | Document chunks | Iterated over; should be an iterable |
|  | `model` | `Model` | LLM wrapper | As above |
|  | `custom_description` | `str` | Prompt target | Text describing what to produce |
|  | `language` | `str` | Optional | Defaults to `"en"` |
|  | `result` | `str` | Description block | Empty if no useful response |
| `generete_custom_discription_without` | `model` | `Model` | LLM wrapper | Same as above |
|  | `custom_description` | `str` | Prompt target | Full text to summarise |
|  | `language` | `str` | Optional | Defaults to `"en"` |
|  | `result` | `str` | Summary | Contains mandatory `<a name="CONTENT_DESCRIPTION">` header |

### Interaction with Other Modules

- **LLM**: All functions delegate to an instance of `Model` (often `GPTModel`) via `get_answer_without_history`.  
- **Logging**: `BaseLogger` and `InfoLog` emit debug information.  
- **Configuration**: `BASE_INTRODACTION_CREATE_LINKS`, `BASE_INTRO_CREATE`, and `BASE_CUSTOM_DISCRIPTIONS` are constant templates imported from `config`.

---
<a name="factory"></a>
## Factory‑Based Documentation Generation

```python
def factory_generate_doc(self, doc_factory: DocFactory, to_start: bool = False)
```

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `doc_factory` | `DocFactory` | Module registry | Executes `generate_doc()` on each registered `BaseModule` |
| `to_start` | `bool` | Append strategy | `True` ⇒ prepend, `False` ⇒ append |

**Procedure**  
1. Gathers `language`, `full_data`, `code_mix`, and `global_info` into a dict.  
2. Delegates to `doc_factory.generate_doc()` with the LLM and progress bar.  
3. Concatenates the returned `DocContent` with the existing `doc_info.doc`.  

---
<a name="ordering"></a>
## Document Ordering

```python
def order_doc(self)
```

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `content_orders` | `list` | Current order metadata | Updated by `get_order()` |

Calls the post‑processor `get_order()` (LLM‑driven) to compute a new sequence for the document parts and overwrites the internal ordering.

---
<a name="sorting-module"></a>
## Sorting Module: Semantic Title Reordering

### Responsibility
The **sorting** module provides utilities for extracting HTML anchors from raw documentation text, segmenting the document into title/section chunks, and ordering those titles semantically using a language model.

### Interaction with the Rest of the Pipeline
1. `split_text_by_anchors` is invoked by the post‑processor after the `CodeMix` output has been concatenated into a single markdown string.  
2. The resulting dictionary is passed to `get_order`, which contacts the `Model` instance from `autodocgenerator.engine.models.model` to produce an ordered list of section identifiers.  
3. The ordered list is then used by downstream modules to assemble the final doc schema.

### Core Functions

| Function | Entity | Type | Role | Notes |
|----------|--------|------|------|-------|
| `extract_links_from_start` | `chunks` | `list[str]` | Extracts the first anchor name from each chunk | Returns a tuple `(links, have_to_del_first)` |
| `split_text_by_anchors` | `text` | `str` | Splits a markdown document into `{anchor: content}` | Raises `Exception` if anchor count mismatches content chunks |
| `get_order` | `model`, `chanks` | `list[str]` | Requests semantic ordering from the LLM | Logs progress via `BaseLogger` |

#### `extract_links_from_start`

1. Iterate over provided `chunks`.  
2. Use regex `^<a name=["']?(.*?)["']?</a>` to capture an anchor tag at the beginning of a chunk.  
3. If an anchor name is longer than five characters, add `#<anchor>` to `links` and flag `is_find`.  
4. If a chunk does not contain a valid anchor, set `have_to_del_first = True`.  
5. Return the collected `links` and the flag.

#### `split_text_by_anchors`

1. Split `text` on the lookahead pattern `(?=<a name["']?[^"'>\s]{6,200}["']?</a>)` to preserve anchors.  
2. Strip whitespace from each resulting chunk and filter empties.  
3. Call `extract_links_from_start` on the chunk list to collect anchor references and a deletion flag.  
4. If the first anchor is not at the very start (`text.find("<a name") > 10`) or a non‑anchor was found, discard the first chunk (`result_chanks.pop(0)`).  
5. Validate that the number of anchors matches the number of content chunks; otherwise raise an exception.  
6. Build a dictionary mapping each anchor (`#name`) to its corresponding content chunk.  
7. Return the dictionary.

#### `get_order`

1. Instantiate a `BaseLogger` and log the start of ordering.  
2. Build a single‑element prompt list with a user instruction to semantically sort the provided titles (`chanks`).  
3. Call `model.get_answer_without_history(prompt)` to obtain a comma‑separated string.  
4. Strip whitespace from each title and log the final list.  
5. Return the ordered list of titles.

---
<a name="cleanup"></a>
## Cache Clearing

```python
def clear_cache(self)
```

If `config.pbc.save_logs` is `False`, removes the log file from the cache.

---

<a name="save"></a>
## Persisting Final Document

```python
def save(self) -> None
```

Writes the full markdown (`doc_info.doc.get_full_doc()`) to `output_doc.md` and serialises the entire `doc_info` schema to `info.json`.

---
<a name="dependencies"></a>
## External Dependencies

- **`CodeMix`** – Repository reader.  
- **`split_data`, `gen_doc_parts`** – Synchronous LLM chunking.  
- **`compress_to_one`** – LLM‑based compression.  
- **`get_order`, `split_text_by_anchors`** – Post‑processing utilities.  
- **`Model`, `Embedding`** – Abstract LLM and embedding interfaces.  
- **`BaseProgress`, `BaseLogger`** – UI and audit logging.  
- **`Config`, `DocInfoSchema`** – Configuration and document metadata.

---

<a name="notes"></a>
## Missing or Incomplete Information

- The internal structure of `DocInfoSchema` (fields beyond `code_mix`, `global_info`, `doc`) is not shown.  
- Implementation of `doc_info.doc.get_full_doc()` and `doc_info.doc.add_parts()` is external.  
- Error handling around file I/O is generic (`except: data = None`).  
- No explicit cleanup of temporary files beyond logs.  
- The logic that populates `config.pbc` and `config.language` is not presented.

---
<a name="embedding"></a>
## Embedding Layer Creation

```python
def create_embedding_layer(self) -> None
```

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `embedding_model` | `Embedding` | Vectorizer | Passed to each part via `init_embedding()` |

Iterates over every part in `doc_info.doc.parts`, invoking `init_embedding` to attach an embedding vector.

---
<a name="embedding-layer"></a>
## Vector Embedding Utilities

This module implements lightweight vector operations and a wrapper around the Google Gemini embedding API.  
It is used by the post‑processor to attach semantic vectors to document fragments and to order them.

### Core Functions

| Function | Entity | Type | Role | Notes |
|----------|--------|------|------|-------|
| `bubble_sort_by_dist` | `arr` | `list` | In‑place sort | Implements bubble sort on list of tuples `(identifier, distance)` |
| `get_len_btw_vectors` | `vector1`, `vector2` | `numpy.ndarray` | Distance calculator | Returns Euclidean norm (`np.linalg.norm`) |
| `sort_vectors` | `root_vector` | `list[float]` | Reference vector | `other` is a `dict[str, list[float]]`; returns sorted keys |
| `Embedding.get_vector` | `prompt` | `str` | LLM request | Returns embedding of the first token vector |

### Data Contract

| Function | Entity | Type | Role | Notes |
|----------|--------|------|------|-------|
| `bubble_sort_by_dist` | `arr` | `list[tuple]` | Sorting buffer | Mutates and returns `arr` |
| `get_len_btw_vectors` | `vector1`, `vector2` | `numpy.ndarray` | Distance | Uses `np.linalg.norm` |
| `sort_vectors` | `root_vector` | `list[float]` | Reference | `other` keys sorted by distance |
|  | `result_list` | `list[str]` | Output | Keys in ascending similarity order |
| `Embedding.__init__` | `api_key` | `str` | Auth | Instantiates `genai.Client` |
| `Embedding.get_vector` | `prompt` | `str` | Prompt text | Calls `client.models.embed_content` with a 768‑dimensional config |
|  | `text_response` | `EmbedContentResponse` | API response | Raises `Exception` if embeddings missing |
|  | `vector` | `list[float]` | Embedding | First dimension of the returned embeddings |

### Interaction with External Libraries

- **`google.genai`**: Provides `Client` and `types.EmbedContentConfig`.  
- **`numpy`**: Used for distance calculations.  
- **`typing`**: Supports type hinting of `Any`.

### Error Handling

- `Embedding.get_vector` raises a generic `Exception("promblem with embedding")` if `text_response.embeddings` is `None`.  
- No other explicit error handling; the calling code must manage exceptions.

--- 

<a name="notes"></a>
## Observations & Missing Context

- `generete_custom_discription` is typed to accept `splited_data: str` but iterated as a collection, implying the caller supplies an iterable of strings.  
- The constants (`BASE_INTRODACTION_CREATE_LINKS`, `BASE_INTRO_CREATE`, `BASE_CUSTOM_DISCRIPTIONS`) are external; their content is not available.  
- The functions rely on a `Model` interface that exposes `get_answer_without_history`, but details of its implementation are absent.  
- No explicit unit tests or error handling for malformed HTML anchors beyond a length check.  

---
<a name="compressor-component"></a>
## Compressor Component – Text Aggregation & LLM‑based Compression

The **Compressor** module provides three public helpers that wrap the LLM’s text‑summarization logic and progressively reduce a collection of raw snippets to a single compressed document.
<a name="compressor-flow"></a>
### Compression Workflow

| Step | Function | Purpose | Key Inputs | Side‑Effects |
|------|----------|---------|------------|--------------|
| 1 | `compress` | Sends a single chunk to the LLM and returns the compressed text. | `data`: raw string; `project_settings`: `ProjectSettings`; `model`: `Model`; `compress_power`: int | LLM interaction (network I/O); no mutating state |
| 2 | `compress_and_compare` | Groups a list of chunks into *compress_power*‑sized blocks, compresses each block, and emits progress updates. | `data`: `list[str]`; `model`, `project_settings`, `compress_power`; `progress_bar`: `BaseProgress` | Produces a list of compressed strings of length ⌈len(data)/compress_power⌉ |
| 3 | `compress_to_one` | Iteratively feeds the output of `compress_and_compare` back into itself until a single string remains. | `data`: `list[str]`; same model and settings; `compress_power`: int | Final compressed document as a string |

---
<a name="compress-function"></a>
## `compress(data: str, project_settings: ProjectSettings, model: Model, compress_power) → str`

* **Logic**  
  1. Builds a three‑part prompt:  
     - System message with `project_settings.prompt`.  
     - System message with base compression hint `get_BASE_COMPRESS_TEXT(len(data), compress_power)`.  
     - User message containing the raw `data`.  
  2. Calls `model.get_answer_without_history(prompt=prompt)` to obtain the compressed output.  
  3. Returns the LLM’s answer string.

* **Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Raw content chunk | Must fit within the model’s token budget |
| `project_settings` | `ProjectSettings` | Provides project‑specific context | `prompt` property concatenates base text with project metadata |
| `model` | `Model` | LLM abstraction | Exposes `get_answer_without_history` |
| `compress_power` | `int` | Influences prompt text via `get_BASE_COMPRESS_TEXT` | Value typically 4 but can be overridden |

* **Error Handling** – No explicit try/except; any exception propagates from `model.get_answer_without_history`.

---
<a name="compress-and-compare-function"></a>
## `compress_and_compare(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) → list`

1. **Chunk Allocation** – Pre‑allocates a result list sized by `ceil(len(data)/compress_power)`.  
2. **Progress Management** – Creates a sub‑task in the progress bar with the total item count.  
3. **Batch Compression** – Iterates over `data`; each element is appended to its bucket (based on integer division by `compress_power`) after compression.  
4. **Update & Finish** – Calls `progress_bar.update_task()` per element and removes the sub‑task once done.  
5. **Return** – List of compressed blocks, each potentially containing multiple original snippets concatenated.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | Source snippets | Arbitrary number of items |
| `model` | `Model` | LLM | Same as in `compress` |
| `project_settings` | `ProjectSettings` | Context prompt | Used for each compression call |
| `compress_power` | `int` | Batch size | Default 4, can be lowered for small collections |
| `progress_bar` | `BaseProgress` | UI feedback | Default instance provided |

---
<a name="compress-to-one-function"></a>
## `compress_to_one(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) → str`

1. **Iterative Reduction** – While more than one compressed block remains:  
   * Adjusts `new_compress_power`: if `len(data) < compress_power + 1`, sets it to `2`.  
   * Calls `compress_and_compare` with the current power to shrink the list.  
   * Increments an iteration counter (unused beyond debugging).  
2. **Return** – The sole remaining string after all rounds.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | List of compressed fragments | Expected to be the output of a prior `compress_and_compare` or raw data list |
| `model`, `project_settings` | same as before | LLM context | Passed unchanged through iterations |
| `compress_power` | `int` | Primary batch size | Dynamically reduced in final passes |
| `progress_bar` | `BaseProgress` | UI | Propagated to each inner call |

* **Corner Cases** – If `data` is empty, the function will raise an `IndexError` at `data[0]`. No guard is present in this fragment.

---
<a name="data-contracts"></a>
## Data Contract Summary

| Component | Entity | Type | Role | Notes |
|-----------|--------|------|------|-------|
| `extract_links_from_start` | `chunks` | `list[str]` | Input | Raw section fragments |
| `extract_links_from_start` | `links` | `list[str]` | Output | Anchor strings prefixed with `#` |
| `extract_links_from_start` | `have_to_del_first` | `bool` | Flag | Indicates whether a leading non‑anchor chunk must be dropped |
| `split_text_by_anchors` | `text` | `str` | Input | Raw documentation file |
| `split_text_by_anchors` | `result` | `dict[str, str]` | Output | Mapping from anchor to content chunk |
| `get_order` | `model` | `Model` | Input | LLM abstraction |
| `get_order` | `chanks` | `list[str]` | Input | List of section titles (anchors) |
| `get_order` | `new_result` | `list[str]` | Output | Semantically sorted titles |
| `CodeMix.build_repo_content` | `root_dir` | `Path` | Input | Project root |
| `CodeMix.build_repo_content` | `content` | `str` | Output | Textual repo snapshot |
| `CodeMix.should_ignore` | `path` | `Path` | Input | File or directory path |
| `CodeMix.should_ignore` | `bool` | Output | Determines if the path is filtered |

---
<a name="data-contract-summary"></a>
## Data Contract Summary

| Component | Entity | Type | Role | Notes |
|-----------|--------|------|------|-------|
| `compress` | `data` | `str` | Raw snippet | |
| `compress` | `project_settings` | `ProjectSettings` | Context | |
| `compress` | `model` | `Model` | LLM | |
| `compress` | `compress_power` | `int` | Prompt modifier | |
| `compress_and_compare` | `data` | `list[str]` | Input chunks | |
| `compress_and_compare` | `model` | `Model` | LLM | |
| `compress_and_compare` | `project_settings` | `ProjectSettings` | Prompt | |
| `compress_and_compare` | `compress_power` | `int` | Batch size | |
| `compress_and_compare` | `progress_bar` | `BaseProgress` | Progress UI | |
| `compress_to_one` | `data` | `list[str]` | Initial chunks | |
| `compress_to_one` | `model` | `Model` | LLM | |
| `compress_to_one` | `project_settings` | `ProjectSettings` | Prompt | |
| `compress_to_one` | `compress_power` | `int` | Initial batch size | |
| `compress_to_one` | `progress_bar` | `BaseProgress` | UI | |

---
<a name="logging-and-errors"></a>
## Logging & Error Handling

* `compress_and_compare` and `compress_to_one` rely on `BaseProgress` for progress reporting; no logging of individual LLM calls is visible.  
* No exception handling is implemented in these functions; errors from `model.get_answer_without_history` or from the progress bar surface to the caller.  
* The module assumes `get_BASE_COMPRESS_TEXT` returns a properly formatted system message; misuse may cause malformed prompts.

---
<a name="logging_component"></a>
## `logging.py` – Structured Logging Utilities

**Purpose**  
Centralizes log message creation and dispatch for the Auto Doc Generator UI.  
Logs are formatted with timestamps and severity prefixes and can be routed to the console or a file.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseLog` | Abstract class | Base log message container | Holds `message` and numeric `level` (0 = default) |
| `ErrorLog`, `WarningLog`, `InfoLog` | Subclasses | Severity‑specific loggers | Override `format` to prepend `[ERROR]`, `[WARNING]`, `[INFO]` |
| `BaseLoggerTemplate` | Interface | Dispatch layer | `log` writes, `global_log` applies level filter |
| `FileLoggerTemplate` | Concrete | File‑based logger | Appends each formatted message to a file |
| `BaseLogger` | Singleton | Public API | Stores active `BaseLoggerTemplate` and forwards `log` calls |

> *The logger’s level comparison uses `log_level < 0` to mean “unfiltered” (default).*

**Core Flow**

1. **Message Instantiation** – `ErrorLog("…")` creates an instance with the current timestamp via `_log_prefix`.
2. **Formatting** – Each subclass implements `format()` to prefix severity and timestamp.
3. **Dispatch** – `BaseLogger.log()` forwards to the set template’s `global_log()`.
4. **Filtering** – `BaseLoggerTemplate.global_log()` checks if the message `level` is allowed before calling `log()`.
5. **Output** – `BaseLoggerTemplate.log()` (or `FileLoggerTemplate.log()`) writes to stdout or a file.

---
<a name="error-handling"></a>
## Error Handling & Logging

* **`split_text_by_anchors`**: Raises a generic `Exception` if the anchor count does not match the number of content chunks, signalling malformed input.  
* **`CodeMix.build_repo_content`**: Wraps file reads in a `try/except`; any exception is appended to the output rather than terminating the process.  
* **Logging**: Uses `BaseLogger` to emit `InfoLog` messages during ordering; `CodeMix` logs ignored paths. No other explicit error handling is present.  

---
<a name="progress_component"></a>
## `progress_base.py` – Task Progress Abstractions

**Purpose**  
Provides a pluggable progress interface for both Rich‑based terminal displays and simple console prints, used during long‑running generation stages.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseProgress` | Abstract | Progress API | Stub methods for sub‑task handling |
| `LibProgress` | Rich implementation | Rich progress bar | Uses `rich.progress.Progress`; tracks base and sub‑tasks |
| `ConsoleTask` | Helper | Simple textual progress | Prints percent for each increment |
| `ConsoleGtiHubProgress` | Console wrapper | GitHub‑style console progress | Holds a default “General Progress” and optional sub‑task |

**Core Flow**

1. **Task Creation** – `create_new_subtask(name, total_len)` registers a sub‑task; `LibProgress` adds to the Rich progress container.  
2. **Progress Update** – `update_task()` advances the current sub‑task; if none, advances the base task.  
3. **Task Removal** – `remove_subtask()` clears the current sub‑task reference.  
4. **Console Fallback** – `ConsoleGtiHubProgress` emits human‑readable percentage via `ConsoleTask.progress()`.

---
<a name="split_data"></a>
## `split_data` – Adaptive Text Chunker

**Purpose**  
Takes a long string (`full_code_mix`) and a symbol limit (`max_symbols`) and produces a list of text fragments that each fit under the limit, with a safety margin of *25 %*.  
The algorithm first **iteratively halves** any fragment exceeding *150 %* of `max_symbols`, then assembles the final chunks while ensuring no single part grows beyond *125 %* of the target.  
> *This function is used by `gen_doc_parts` to feed the LLM a manageable prompt size.*

```text
def split_data(full_code_mix: str, max_symbols: int) -> list[str]
```

### Logic Flow

1. **Initialize logger** (`BaseLogger`) and emit “Starting data splitting…”.
2. **Iteratively split**:
   - While any element `el` in `splited_by_files` has length > 1.5 × `max_symbols`, split it at its half and insert the second half after the current index.
3. **Assemble final parts**:
   - Traverse `splited_by_files` and append elements to the current part until the cumulative length would exceed 1.25 × `max_symbols`, then start a new part.
4. **Log** the number of parts and return the list.

### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `full_code_mix` | `str` | Raw source code | Input to be split |
| `max_symbols` | `int` | Size threshold | Determines chunk limits |
| `splited_by_files` | `list[str]` | Intermediate list | Derived from `full_code_mix` (not shown) |
| `split_objects` | `list[str]` | Output list | Returned to caller |
| `logger` | `BaseLogger` | Logger | Emits diagnostics |

---
<a name="cache_settings"></a>
## `CacheSettings` – Commit Cache

A lightweight Pydantic model holding the SHA of the last processed commit.

```python
class CacheSettings(BaseModel):
    last_commit: str = ""
```

> *Only a single field is defined; no additional behavior.*

---
<a name="doc-parts"></a>
## Documentation Parts Generation

```python
def generete_doc_parts(self, max_symbols=5_000, with_global_file: bool = False)
```

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `max_symbols` | `int` | Size of each part | Default 5 k |
| `with_global_file` | `bool` | Whether to include global info | Overridden to `True` internally |

**Steps**  
1. Reads the cached global file.  
2. Calls `gen_doc_parts()` (synchronous LLM pipeline) to create chunked markdown.  
3. Writes output to `output_doc.md`.  
4. Splits the text at anchors with `split_text_by_anchors` and stores each part in `doc_info.doc.parts`.  

---
<a name="write_docs_by_parts"></a>
## `write_docs_by_parts` – LLM‑Driven Part Generation

**Purpose**  
Transforms a single text chunk (`part`) into a documentation fragment via a language model.  
The function builds a prompt hierarchy, calls the LLM, and strips markdown fences if present.

```text
def write_docs_by_parts(part: str,
                        model: Model,
                        project_settings: ProjectSettings,
                        prev_info: str | None = None,
                        language: str = "en",
                        global_info: str | None = None) -> str
```

### Logic Flow

1. **Initialize logger** and log “Generating documentation for a part…”.
2. **Construct prompt**:
   - System role: language selector (`language`).
   - System role: global project metadata (`project_settings.prompt`).
   - System role: base completion template (`BASE_PART_COMPLITE_TEXT`).
   - Optional system role: `global_info`.
   - Optional system role: `prev_info` indicating the last written part.
   - User role: the actual code chunk (`part`).
3. **LLM invocation**: `model.get_answer_without_history(prompt=prompt)` → `answer`.
4. **Strip leading/trailing markdown fences** (`"""``"`) if present.
5. **Return** the cleaned answer.

> *The function does not handle any LLM‑specific errors; any exception propagates to the caller.*

### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | Chunk to document | Input to LLM |
| `model` | `Model` | LLM instance | Must expose `get_answer_without_history` |
| `project_settings` | `ProjectSettings` | Context | Provides `prompt` property |
| `prev_info` | `str | None` | Tail of preceding doc | Optional |
| `language` | `str` | Target language | Defaults to `"en"` |
| `global_info` | `str | None` | Global relation notes | Optional |
| `answer` | `str` | LLM output | May contain fenced code block |
| `temp_answer` | `str` | Stripped version | Used for fence removal |
| `logger` | `BaseLogger` | Logger | Emits generation details |

---
<a name="gen_doc_parts"></a>
## `gen_doc_parts` – Multi‑Pass Documentation Builder

**Purpose**  
Orchestrates the full “split‑then‑generate” pipeline: splits the entire source mix, iteratively calls `write_docs_by_parts`, and concatenates the results.  
It also maintains a sliding window of the most recent 3 000 characters to pass as contextual `prev_info` for the next part.

```text
def gen_doc_parts(full_code_mix,
                  max_symbols,
                  model: Model,
                  project_settings: ProjectSettings,
                  language,
                  progress_bar: BaseProgress,
                  global_info=None) -> str
```

### Logic Flow

1. **Split** `full_code_mix` → `splited_data` by calling `split_data`.
2. **Log** start of part generation.
3. **Create sub‑task** in the progress bar: `"Generete doc parts"`.
4. **Iterate over `splited_data`**:
   - Call `write_docs_by_parts` with current part, `model`, `project_settings`, previous result (`result`) as `prev_info`.
   - Append returned string to `all_result`.
   - Keep only the last 3 000 chars of `result` for next iteration.
   - Update the progress bar.
5. **Finish sub‑task**, log total documentation length, and return `all_result`.

### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `full_code_mix` | `str` | Raw source | Input to be split |
| `max_symbols` | `int` | Chunk size | Used in `split_data` |
| `model` | `Model` | LLM | For generation |
| `project_settings` | `ProjectSettings` | Config | Supplies `prompt` |
| `language` | `str` | Locale | Passed to `write_docs_by_parts` |
| `progress_bar` | `BaseProgress` | UI | Tracks per‑part progress |
| `global_info` | `str | None` | Project relations | Optional |
| `splited_data` | `list[str]` | Chunks | Intermediate |
| `all_result` | `str` | Full documentation | Final output |

---
<a name="doc_content"></a>
## `DocContent` – Embedded Text Block

Encapsulates a documentation string and its optional vector embedding.

```python
class DocContent(BaseModel):
    content: str
    embedding_vector: list | None = None

    def init_embedding(self, embedding_model: Embedding):
        self.embedding_vector = embedding_model.get_vector(self.content)
```

| Method | Input | Output | Notes |
|--------|-------|--------|-------|
| `init_embedding` | `Embedding` | None | Sets `embedding_vector` in place |

---
<a name="doc_head_schema"></a>
## `DocHeadSchema` – Ordered Section Collection

Maintains an ordered list of section names and a mapping to their `DocContent`.

```python
class DocHeadSchema(BaseModel):
    content_orders: list[str] = []
    parts: dict[str, DocContent] = {}

    def add_parts(self, name, content: DocContent): ...
    def get_full_doc(self, split_el: str = "\n") -> str: ...
    def __add__(self, other: "DocHeadSchema") -> "DocHeadSchema": ...
```

### Key Operations

| Method | Role | Notes |
|--------|------|-------|
| `add_parts` | Insert a uniquely named section | Avoids name collisions by appending `_{i}` |
| `get_full_doc` | Concatenate all parts in order | Uses `split_el` separator |
| `__add__` | Merge with another `DocHeadSchema` | Preserves ordering |

---
<a name="doc_info_schema"></a>
## `DocInfoSchema` – Full Document Metadata

Root schema aggregating global info, the raw source mix, and the hierarchical sections.

```python
class DocInfoSchema(BaseModel):
    global_info: str = ""
    code_mix: str = ""
    doc: DocHeadSchema = Field(default_factory=DocHeadSchema)
```

| Field | Type | Role | Notes |
|-------|------|------|-------|
| `global_info` | `str` | Project description | Raw text |
| `code_mix` | `str` | Raw source | Used by the generator |
| `doc` | `DocHeadSchema` | Structured doc | Holds sections |

---
