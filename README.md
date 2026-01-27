## Executive Navigation Tree
- 📂 Installation & Setup
  - [Install Workflow Guide](#install-workflow-guide)
  - [PowerShell Setup Script](#powershell-setup-script)
  - [Bash Setup Script](#bash-setup-script)
- ⚙️ Configuration & Core
  - [Autodocconfig File Options](#autodocconfig-file-options)
  - [Purpose Of Config Reader](#purpose-of-config-reader)
  - [Key Function Read Config](#key-function-read-config)
  - [Cli Bootstrap And Configuration Loading](#cli‑bootstrap‑and‑configuration‑loading)
  - [Configuration Constants](#configuration-constants)
  - [Environment Variable Loading](#environment-variable-loading)
  - [Projectsettings Class](#projectsettings-class)
  - [Project Metadata Declaration](#project-metadata-declaration)
  - [Dependency Specification](#dependency-specification)
  - [Build System Configuration](#build-system-configuration)
- 🏗️ Integration & Modules
  - [Integration With Factory Modules](#integration-with-factory-modules)
  - [Integration Points And Assumptions](#integration‑points‑and‑assumptions)
  - [Integration Points](#integration‑points)
  - [Assumptions And Side‑Effects](#assumptions-and-side-effects)
  - [Module Purpose](#module-purpose)
  - [Basemodule Abstract Contract](#basemodule‑abstract‑contract)
  - [Manager Orchestration Role](#manager‑orchestration‑role)
  - [Docfactory Module Orchestrator](#docfactory‑module‑orchestrator)
  - [Factory Doc Augmentation](#factory‑doc‑augmentation)
  - [Model Instantiation And Manager Setup](#model-instantiation-and-manager-setup)
- 🔄 Processing & Generation Pipeline
  - [Processing Steps](#processing-steps)
  - [Generation Pipeline Steps](#generation‑pipeline‑steps)
  - [Document Ordering Step](#document‑ordering‑step)
  - [Anchor Extraction And Chunk Splitting](#anchor-extraction-and-chunk-splitting)
  - [Semantic Ordering Of Chunks](#semantic-ordering-of-chunks)
  - [Data Splitting Logic](#data-splitting-logic)
  - [History Buffer Management](#history-buffer-management)
  - [Parentmodel Selection Logic](#parentmodel‑selection‑logic)
  - [Gptmodel Synchronous Wrapper](#gptmodel‑synchronous‑wrapper)
  - [Asyncgptmodel Asynchronous Wrapper](#asyncgptmodel‑asynchronous‑wrapper)
  - [Model Exhausted Exception](#model-exhausted-exception)
- 🗂️ Compression & Optimization
  - [Compress Function](#compress-function)
  - [Compress And Compare Sync](#compress-and-compare-sync)
  - [Compress To One Loop](#compress-to-one-loop)
  - [Async Compress Function](#async-compress-function)
  - [Async Compress And Compare](#async-compress-and-compare)
  - [Compression Prompt Generator](#compression-prompt-generator)
- 📄 Documentation Generation
  - [Custommodule Custom Description Generator](#custommodule‑custom‑description‑generator)
  - [Custom Description Generation](#custom‑description‑generation)
  - [Generate Descriptions](#generate-descriptions)
  - [Code Mix Generation Method](#code‑mix‑generation‑method)
  - [Repository Content Aggregation Codemix](#repository-content-aggregation-codemix)
  - [Sync Part Doc Generation](#sync-part-doc-generation)
  - [Synchronous Doc Parts Generation](#synchronous‑doc‑parts‑generation)
  - [Async Part Doc Generation](#async-part-doc-generation)
  - [Batch Doc Generation Sync](#batch-doc-generation-sync)
  - [Batch Doc Generation Async](#batch-doc-generation-async)
- 🌐 HTML Extraction & Intro Links
  - [Introlinks Html Link Extraction Intro](#introlinks‑html‑link‑extraction‑intro)
  - [Html Link Extraction](#html-link-extraction)
- 🧩 Misc Tools
  - [Regex Pattern](#["\\\']?(.*?)["\\\']?)
- 📄 Intro Generation
  - [Introtext Global Introduction Assembly](#introtext‑global‑introduction‑assembly)
  - [Global Intro Generation](#global‑intro‑generation)
  - [Link Driven Intro Generation](#link‑driven‑intro‑generation)
- 🗃️ Cache & Logging
  - [Cache Initialisation Paths](#cache‑initialisation‑paths)
  - [Cache Cleanup Routine](#cache‑cleanup‑routine)
  - [Logging Infrastructure](#logging-infrastructure)
  - [Rich Console Progress](#rich-console-progress)
  - [Console Progress](#console-progress)

 

<a name="install-workflow-guide"></a>To set up the documentation generation workflow, fetch the Windows installer script from raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 and execute it in PowerShell using `| iex`. For Linux systems, retrieve the installer from raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh and run it with `| bash`. After installing, add a secret called **GROCK_API_KEY** to your repository’s GitHub Actions secrets, inserting the API key obtained from the Grock documentation site (grockdocs.com) to enable the workflow. 
<a name="powershell-setup-script"></a>
## PowerShell Setup Script (`install.ps1`)  
**Responsibility**: Generates GitHub workflow files and a minimal `autodocconfig.yml` for the current repository.  
**Interactions**: Uses PowerShell here‑strings to write `.github/workflows/autodoc.yml` and `autodocconfig.yml`; reads the folder name via `Get-Item .`.  
**Technical Details**: Creates target directory (`New-Item -Force`), writes static YAML content with embedded secret reference, and prints a success message.  
**Data Flow**: Filesystem paths → created/overwritten YAML files. 
<a name="bash-setup-script"></a>
## Bash Setup Script (`install.sh`)  
**Responsibility**: Mirrors `install.ps1` for Unix‑like shells, creating the same workflow and config files.  
**Interactions**: Uses `mkdir -p` for directory creation, `cat <<EOF` redirection to write YAML, and `$(basename "$PWD")` to insert the project name.  
**Technical Details**: Escapes the `${{…}}` placeholder to avoid shell interpolation, then echoes a confirmation.  
**Data Flow**: Filesystem operations → generated `.github/workflows/autodoc.yml` and `autodocconfig.yml`. 
<a name="autodocconfig-file-options"></a>
The configuration file is written in YAML and may contain the following top‑level keys:

* **project_name** – a string that defines the name of the project.  
* **language** – a string indicating the documentation language (default “en”).  
* **ignore_files** – an optional list of glob patterns for files that should be excluded from processing.  
* **project_settings** – a map with optional settings:  
  * **save_logs** – boolean, when true the generation logs are persisted.  
  * **log_level** – integer specifying the verbosity of logging.  
* **project_additional_info** – a map where any custom key‑value pairs can be added to enrich the project description (e.g., a “global idea” entry).  
* **custom_descriptions** – a list of strings; each string is passed to a custom module and can contain arbitrary explanatory text, commands, or references.  

When writing the file, ensure proper indentation and use plain YAML syntax. Include only the keys you need; omitted keys will fall back to defaults defined in the generator. 
<a name="purpose-of-config-reader"></a>
## Purpose of ConfigReader  

`read_config` translates a raw YAML string into a fully‑populated `Config` instance and a list of `CustomModule` objects. It centralises all project‑wide settings, language choice, ignore patterns and custom description handling for the Auto‑Doc Generator. 
<a name="key-function-read-config"></a>
## Key Function `read_config`  

```python
def read_config(file_data: str) -> tuple[Config, list[CustomModule]]:
```

* **Parameters** – `file_data`: a YAML‑formatted string (typically the contents of `autodocconfig.yml`).  
* **Returns** – a tuple:  
  1. `Config` – holds project metadata, language, ignore patterns, and `ProjectConfigSettings`.  
  2. `list[CustomModule]` – one module per custom description. 
<a name="cli‑bootstrap‑and‑configuration‑loading"></a>
## CLI bootstrap and configuration loading

The `if __name__ == "__main__":` block acts as a tiny command‑line driver:

1. Reads `autodocconfig.yml` into a string.  
2. Calls `read_config` (from `auto_runner.config_reader`) to obtain a `Config` instance and a list of custom module objects.  
3. Invokes `gen_doc(".", config, custom_modules)` and stores the result in `output_doc`.

No external I/O occurs inside `gen_doc`; all file interactions are confined to the `Manager`’s internal cache and the final `read_file_by_file_key` call. 
<a name="configuration-constants"></a>
## Configuration constants and prompts

The module defines a set of multi‑line string constants (`BASE_SYSTEM_TEXT`, `BASE_PART_COMPLITE_TEXT`, `BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`, `BASE_SETTINGS_PROMPT`). Each constant supplies a reusable prompt fragment for the AutoDoc pipeline (system instruction, documentation style, navigation‑tree generation, project‑overview template, and persistent‑memory instruction). These literals are imported by the runner to build the full prompt passed to the LLM. 
<a name="environment-variable-loading"></a>
## Environment variable loading and API key validation

```python
load_dotenv()
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise Exception("API_KEY is not set in environment variables.")
```

The code pulls the OpenAI key from a `.env` file at runtime. Absence of the key aborts execution, guaranteeing that downstream `GPTModel` instances always receive valid credentials. 
<a name="projectsettings-class"></a>
## ProjectSettings – Prompt Builder  
**Responsibility**: Holds project‑level metadata and produces a composite system prompt.  
**Interactions**: Accessed by all compression functions via the `prompt` property.  
**Technical Details**: Starts with `BASE_SETTINGS_PROMPT`, appends project name and any key/value pairs added via `add_info`.  
**Data Flow**: `ProjectSettings` → `str` prompt used in LLM calls. 
<a name="project-metadata-declaration"></a>
## Project Metadata Declaration  

The `pyproject.toml` fragment declares the **autodocgenerator** package’s identity: name, version, description, authors, license, README, and supported Python range. This information is consumed by packaging tools (Poetry, pip, build back‑ends) to generate distribution metadata (`PKG‑INFO`, wheel tags) and to surface project details on PyPI. 
<a name="dependency-specification"></a>
## Dependency Specification  

Under `[project]` the `dependencies` array enumerates exact version pins for every runtime library (e.g., `openai==2.14.0`, `pydantic==2.12.5`). The list drives `poetry install` and `pip install .` to resolve a reproducible environment. No optional or development groups are defined here; they would be placed in separate sections (`[tool.poetry.dev-dependencies]`) if needed. 
<a name="build-system-configuration"></a>
## Build System Configuration  

The `[build-system]` table tells the Python build frontend to use **poetry-core** (`requires = ["poetry-core>=2.0.0"]`) with the entry point `poetry.core.masonry.api`. During `python -m build` or `pip install .`, this config triggers Poetry’s PEP‑517 builder, which reads the above metadata and assembles the source distribution and wheel. No custom build steps or hooks are declared, so the process is deterministic and isolated from external scripts. 
<a name="entry-point-for-doc-generation"></a>
## Entry point for documentation generation (`gen_doc`)

The `gen_doc` function is the orchestrator that ties together configuration, language models, and the `Manager` to produce a complete documentation file. It receives a filesystem root (`project_path`), a validated `Config` object, and a list of instantiated custom module objects.

**Data flow**  
- **Inputs**: `project_path` (str), `config` (Config), `custom_modules` (list[CustomModule])  
- **Outputs**: Raw markdown string returned by `manager.read_file_by_file_key("output_doc")`  

**Side effects**: Initializes two GPT model instances, creates a `Manager`, triggers a series of generation steps, and clears the internal cache. 
<a name="integration-with-factory-modules"></a>
## Integration with Factory Modules  

The function imports `CustomModule` from `autodocgenerator.factory.modules.general_modules`. Each entry in the `custom_descriptions` YAML array is wrapped in a `CustomModule`, allowing the downstream factory pipeline to treat user‑supplied snippets uniformly with built‑in modules. 
<a name="integration‑points‑and‑assumptions"></a>
## Integration points and assumptions

- **Config object** must conform to the schema defined in `autodocgenerator.auto_runner.config_reader`; malformed YAML raises `yaml.YAMLError`.  
- **Custom modules** are expected to inherit from `CustomModule` and be instantiable without arguments.  
- The global `API_KEY` is imported from `autodocgenerator.engine.config.config`; absence of a valid key will cause runtime authentication errors.  
- The function is pure from the caller’s perspective – it returns the assembled markdown and leaves the filesystem untouched after execution. 
<a name="integration‑points"></a>
## Integration with the documentation pipeline  

1. After `order_doc` produces the final markdown, `custom_intro` is imported by the post‑processor stage.  
2. `get_all_html_links` extracts navigation anchors → fed to `get_links_intro`.  
3. `get_introdaction` receives the whole document for a high‑level intro.  
4. `generete_custom_discription` may be invoked with user‑specified topics to prepend targeted sections.  
5. The returned strings are concatenated and written back to `output_doc.md`.  

All functions are pure apart from logging; they rely solely on the provided `Model` instance, making them trivially mockable for unit testing. 
<a name="assumptions-and-side-effects"></a>
## Assumptions and Side Effects  

* The YAML must be syntactically valid; malformed input raises `yaml.YAMLError`.  
* Missing optional keys default to empty collections or sensible defaults (`language` → `"en"`).  
* No external I/O occurs; the function purely transforms in‑memory data, leaving the filesystem untouched.  

This fragment is the entry point for configuration loading, feeding the rest of the ADG pipeline with a consistent, typed configuration object. 
<a name="module-purpose"></a>
## Purpose of **custom_intro** post‑processor  

The module supplies a lightweight post‑processing pipeline that enriches the automatically generated documentation with anchor‑based navigation and optional introductory sections. It operates on the final markdown produced by the core generation flow and prepares ready‑to‑display HTML‑compatible fragments. 
<a name="basemodule‑abstract‑contract"></a>
## `BaseModule` – abstract generation contract  
`BaseModule` defines the required interface for any documentation fragment generator. It inherits from `ABC` and mandates a `generate(info: dict, model: Model)` method, ensuring uniformity across plug‑in modules. Sub‑classes implement their own logic while receiving the raw `info` payload and a concrete `Model` instance. 
<a name="manager‑orchestration‑role"></a>
## `Manager` – orchestrating preprocessing, documentation generation, and post‑processing  

**Responsibility** – Coordinates the end‑to‑end documentation pipeline: builds a *code‑mix* snapshot, splits it into manageable chunks, runs factory modules (e.g., `IntroLinks`, `IntroText`), orders the final markdown, and handles cache/log housekeeping.

**Interactions** –  
- **Pre‑processors**: `CodeMix` (repo scanning), `gen_doc_parts` / `async_gen_doc_parts` (chunk‑wise generation).  
- **Post‑processors**: `split_text_by_anchors`, `get_order` (re‑ordering).  
- **Factories**: any `DocFactory` subclass supplying a list of modules that implement `generate_doc`.  
- **Models**: synchronous `Model` or asynchronous `AsyncModel` supplied at construction.  
- **UI**: `BaseProgress` updates progress bars; `BaseLogger` writes to the cache‑log file. 
<a name="docfactory‑module‑orchestrator"></a>
## `DocFactory` – orchestrator of documentation modules  
`DocFactory` aggregates a sequence of `BaseModule` objects. Its `generate_doc` method creates a progress sub‑task, iterates through each module, concatenates their outputs, logs success and module content (verbosity level 2), updates progress, and finally returns the assembled documentation string. Errors propagate from individual modules; the factory itself does not alter content. 
<a name="factory‑doc‑augmentation"></a>
## `factory_generate_doc` – applying modular enrichments  

1. Loads current `output_doc` and the original `code_mix`.  
2. Builds `info` dict (`language`, `full_data`, `code_mix`).  
3. Calls `doc_factory.generate_doc(info, sync_model, progress_bar)`.  
4. Prepends the factory result to the existing doc (`new_data = f"{result}\\n\\n{curr_doc}"`) and writes back.  

The method is model‑agnostic; any `DocFactory` with a `modules` attribute (e.g., `IntroLinks`, `IntroText`) can contribute additional sections. 
<a name="model-instantiation-and-manager-setup"></a>
## Model instantiation and manager setup

```python
sync_model = GPTModel(API_KEY, use_random=False)
async_model = AsyncGPTModel(API_KEY)

manager = Manager(
    project_path,
    config=config,
    sync_model=sync_model,
    async_model=async_model,
    progress_bar=ConsoleGtiHubProgress(),
)
```

- **GPTModel / AsyncGPTModel** – provide synchronous and asynchronous OpenAI API access, respectively.  
- **ConsoleGtiHubProgress** – concrete progress‑bar implementation displayed in the terminal.  
- **Manager** – core engine that holds state, coordinates factories, and writes the final document. 
<a name="processing-steps"></a>
## Processing Steps  

1. **Parse YAML** – `yaml.safe_load` yields a Python dict.  
2. **Instantiate Config** – default `Config()` created.  
3. **Populate core fields** – `language`, `project_name`, `project_additional_info`.  
4. **Load project settings** – `ProjectConfigSettings().load_settings(...)` then attached via `config.set_pcs`.  
5. **Register ignore patterns** – each pattern from `ignore_files` added with `config.add_ignore_file`.  
6. **Add supplemental info** – key/value pairs from `project_additional_info` stored via `config.add_project_additional_info`.  
7. **Create custom modules** – each string in `custom_descriptions` wrapped in `CustomModule`. 
<a name="generation‑pipeline‑steps"></a>
## Generation pipeline steps

| Call | Purpose |
|------|---------|
| `manager.generate_code_file()` | Scans the project, extracts source files, and stores a normalized code representation. |
| `manager.generete_doc_parts(max_symbols=5000)` | Produces raw documentation fragments (function signatures, docstrings, etc.) limited to `max_symbols` characters per chunk. |
| `manager.factory_generate_doc(DocFactory(*custom_modules))` | Runs a `DocFactory` built from user‑supplied `custom_modules` to inject bespoke sections (e.g., custom tutorials). |
| `manager.order_doc()` | Reorders fragments into a logical sequence (intro → modules → API reference). |
| `manager.factory_generate_doc(DocFactory(IntroLinks()))` | Adds a generated introductory links section using the built‑in `IntroLinks` module. |
| `manager.clear_cache()` | Purges temporary files and in‑memory caches to keep the workspace clean. | 
<a name="document‑ordering‑step"></a>
## `order_doc` – anchor‑based re‑ordering  

- Splits `output_doc` into sections via `split_text_by_anchors`.  
- Sends the list to `get_order(sync_model, sections)` which uses the LLM to compute the optimal sequence.  
- Persists the reordered markdown. 
<a name="anchor-extraction-and-chunk-splitting"></a>
## Anchor Extraction & Chunk Splitting (`extract_links_from_start`, `split_text_by_anchors`)

**Responsibility** – Isolate markdown sections that begin with an HTML anchor (`<a name="…"></a>`) and build a mapping {anchor → section text}.  
**Interactions** – Consumes raw markdown supplied by the post‑processor, emits a `dict[str,str]` used later by `get_order`. No external services; only `re` and the internal logger for debugging.  
**Technical Details** –  
* `extract_links_from_start` scans each pre‑split chunk with `^<a name=["']?(.*?)["']?</a>`; anchors shorter than six characters are discarded and a leading “#” is prefixed.  
* `split_text_by_anchors` uses a positive‑lookahead split (`(?=<a name=["']?[^"\'>\s]{6,200}["']?</a>)`) to produce clean chunks, strips whitespace, validates a one‑to‑one count between anchors and chunks, and finally assembles the result dictionary.  
**Data Flow** – Input: full markdown string. Output: `{ "#anchorName": "section markdown …" }` or `None` on mismatch. Side‑effects: optional `InfoLog` messages (not shown here). 
<a name="semantic-ordering-of-chunks"></a>
## Semantic Ordering of Documentation Chunks (`get_order`)

**Responsibility** – Ask the LLM (`model`) to reorder the extracted sections so related topics are grouped logically.  
**Interactions** – Receives the anchor‑to‑chunk map from the splitter, builds a single‑turn user prompt, calls `model.get_answer_without_history`, parses the comma‑separated title list, and concatenates the corresponding markdown blocks. Logging via `BaseLogger` records the input map, the raw LLM reply, and each block addition.  
**Technical Details** –  
* Prompt explicitly requests only a CSV list, preserving the leading “#” in titles.  
* Result string split → `new_result` list, then ordered markdown assembled in `order_output`.  
**Data Flow** – Input: `Model` instance, `dict[str,str]`. Output: a single ordered markdown string. No file I/O; side‑effects limited to logger entries. 
<a name="data-splitting-logic"></a>
## Data Splitting Logic (`split_data`)  
**Responsibility**: Breaks a large source‑code string into chunks whose length does not exceed `max_symbols`.  
**Interactions**: Relies on `BaseLogger` for progress messages; no external state.  
**Technical Details**:  
- Splits on line breaks, then iteratively halves any segment > 1.5 × `max_symbols`.  
- Packs the refined segments into `split_objects`, starting a new chunk when the current one would exceed 1.25 × `max_symbols`.  
**Data Flow**: `str` → list of `str` (chunks). 
<a name="history-buffer-management"></a>
## `History` – accumulating system‑ and conversation‑level messages  

- **Inputs:** optional `system_prompt` (defaults to `BASE_SYSTEM_TEXT`).  
- **State:** `self.history` – ordered list of `{role, content}` dicts.  
- **Side‑effects:** `add_to_history` appends new entries, used by `Model`/`AsyncModel` to build the chat payload.  
- **Assumptions:** callers respect role strings (`"system"`, `"user"`, `"assistant"`). 
<a name="parentmodel‑selection‑logic"></a>
## `ParentModel` – randomized model list preparation  

During initialization it copies `MODELS_NAME`, optionally shuffles it (`use_random`), and stores the sequence in `self.regen_models_name`. `self.current_model_index` tracks the active model. This structure enables fail‑over cycling when a model call fails. 
<a name="gptmodel‑synchronous‑wrapper"></a>
## `GPTModel` – synchronous Groq client integration  

- Constructs a `Groq` client with the supplied `api_key`.  
- `generate_answer` selects the current model, attempts `client.chat.completions.create(messages, model)`, and on exception logs a warning, advances `current_model_index`, and retries until a model succeeds or the list is exhausted (raising `ModelExhaustedException`).  
- Returns the content of the first choice and logs the result. 
<a name="asyncgptmodel‑asynchronous‑wrapper"></a>
## `AsyncGPTModel` – async counterpart using `AsyncGroq`  

Mirrors `GPTModel` logic but with `await` on `client.chat.completions.create`. Logging is identical, and the method signature is `async`. It enables non‑blocking generation in event‑driven workflows.

**Data Flow Summary**  
Prompt (either full history or raw `prompt` arg) → `History`/caller → selected model name → Groq API call → `chat_completion` object → extracted `content` → logger → returned string. All errors funnel through the retry loop or raise `ModelExhaustedException`. 
<a name="model-exhausted-exception"></a>
## `ModelExhaustedException` – signaling depletion of model pool  

`ModelExhaustedException` derives from `Exception` and is raised when `regen_models_name` becomes empty. It bubbles up to the caller, forcing upstream logic (e.g., factories or UI) to abort or retry with a different configuration. 
<a name="compress-function"></a>
## Compress – Single‑Pass Summarization  
**Responsibility**: Sends a raw text chunk to the LLM with a system prompt built from `ProjectSettings` and a configurable compression baseline.  
**Interactions**: Calls `model.get_answer_without_history`; reads `project_settings.prompt` and `get_BASE_COMPRESS_TEXT`.  
**Technical Details**: Constructs a three‑message list (`system`, `system`, `user`) and returns the LLM’s answer verbatim.  
**Data Flow**: `data: str` → LLM request → `str` answer. 
<a name="compress-and-compare-sync"></a>
## Compress & Compare (synchronous)  
**Responsibility**: Groups input strings into `compress_power`‑sized batches, compresses each element, and concatenates results per batch.  
**Interactions**: Uses `compress`; updates a `BaseProgress` sub‑task.  
**Technical Details**: Pre‑allocates a result list sized `ceil(len(data)/compress_power)`, iterates with index division, appends compressed text plus newline.  
**Data Flow**: `list[str]` → list of combined batch strings. 
<a name="compress-to-one-loop"></a>
## Compress to One – Iterative Reduction  
**Responsibility**: Repeatedly compresses the list until a single aggregated summary remains.  
**Interactions**: Switches between sync/async paths based on `use_async`; each iteration calls the appropriate batch function.  
**Technical Details**: Dynamically lowers `compress_power` when remaining items < `compress_power+1`; counts iterations for diagnostics.  
**Data Flow**: `list[str]` → final `str` summary. 
<a name="async-compress-function"></a>
## Async Compress – Concurrency‑Safe Summarization  
**Responsibility**: Same as `compress` but respects an `asyncio.Semaphore` to limit parallel LLM calls and updates progress.  
**Interactions**: Awaits `model.get_answer_without_history`; shares the same prompt structure.  
**Technical Details**: Wrapped in `async with semaphore`; returns the answer after `progress_bar.update_task()`.  
**Data Flow**: `str` → async LLM request → `str`. 
<a name="async-compress-and-compare"></a>
## Async Compress & Compare  
**Responsibility**: Parallel version of batch compression.  
**Interactions**: Spawns one `async_compress` task per element, gathers results, then re‑chunks them into batches of `compress_power`.  
**Technical Details**: Uses a fixed 4‑slot semaphore, creates a progress sub‑task, joins with `asyncio.gather`.  
**Data Flow**: `list[str]` → list of batch strings. 
<a name="compression-prompt-generator"></a>
## `get_BASE_COMPRESS_TEXT` – dynamic prompt builder

```python
def get_BASE_COMPRESS_TEXT(start, power):
    return f\"\"\"
You will receive a large code snippet (up to ~{start} characters).
...
``` 
This helper creates a size‑aware instruction block for summarising large code fragments. Parameters:
- **start** – approximate maximum character count of the incoming snippet.
- **power** – divisor controlling the length of the summary (`~start/power`).

The function interpolates these values into a template that directs the model to extract architecture, produce a concise summary, and emit a strict usage example. It returns the formatted string for later concatenation with other prompt pieces. 
<a name="custommodule‑custom‑description‑generator"></a>
## `CustomModule` – custom description generator  
Initialised with a `discription` string, `CustomModule.generate` splits the mixed code (`info["code_mix"]`) to ≤ 7000 symbols via `split_data`, then calls `generete_custom_discription` (post‑processor) with the split data, the provided `model`, the stored description, and the target language. The returned text becomes the module’s contribution. 
<a name="custom‑description‑generation"></a>
## `generete_custom_discription(splited_data: str, model: Model, custom_description: str, language: str = "en") → str`  

*Responsibility* – Iterates over pre‑split documentation fragments, asking the LLM to produce a concise, anchor‑prefixed description for a user‑defined topic (`custom_description`).  
*Logic Flow*  

1. For each `sp_data` in `splited_data` construct a multi‑system‑message prompt:
   * language directive,  
   * role description (“Technical Analyst”),  
   * strict rule block enforcing *zero‑hallucination* and mandatory single `<a name="…"></a>` tag,  
   * the fragment context,  
   * the task description.  
2. Call `model.get_answer_without_history`.  
3. If the result does **not** contain the sentinel `!noinfo` / “No information found” (or it appears after position 30), break the loop and return the answer; otherwise continue with the next fragment.  

*Side‑effects* – None; all I/O is through the LLM and logging performed implicitly by the model or caller. 
<a name="generate-descriptions"></a>
## Generate Descriptions for Code  
**Responsibility**: Queries the LLM for a structured developer‑facing description of each source file.  
**Interactions**: Sends a fixed instructional system prompt plus the code snippet; logs progress.  
**Technical Details**: Iterates over `data`, builds a two‑message prompt, collects answers in order.  
**Data Flow**: `list[str]` (code) → list of LLM‑generated markdown descriptions. 
<a name="code‑mix‑generation‑method"></a>
## `generate_code_file` – building the repository snapshot  

1. Logs start.  
2. Instantiates `CodeMix(project_directory, config.ignore_files)`.  
3. Calls `cm.build_repo_content` → writes the mixed source to `code_mix.txt`.  
4. Logs completion and advances the progress bar. 
<a name="repository-content-aggregation-codemix"></a>
## Repository Content Aggregation (`CodeMix` class)

**Responsibility** – Produce a linear textual representation of a repository’s directory tree and file contents, while respecting an ignore list.  
**Interactions** – Called by the pre‑processor stage; writes to a user‑specified output file. Relies on `BaseLogger` for ignored‑path notices; does not invoke the LLM.  
**Technical Details** –  
* `should_ignore` evaluates a `Path` against `ignore_patterns` using `fnmatch` on the full relative path, basename, and each path component.  
* `build_repo_content` iterates twice over `root_dir.rglob("*")`: first to emit the hierarchical tree (indentation based on depth), second to embed each non‑ignored file inside `<file path="…">` tags. Errors while reading files are captured and written inline.  
**Data Flow** – Input: root directory path, ignore pattern list, optional output filename. Output: side‑effect – a text file (`repomix-output.txt` by default) containing the structured dump. Logging side‑effects report ignored entries and read errors. 
<a name="sync-part-doc-generation"></a>
## Synchronous Part Documentation Generation (`write_docs_by_parts`)  
**Responsibility**: Sends a single chunk to the LLM and returns the raw markdown response.  
**Interactions**: Uses `BASE_PART_COMPLITE_TEXT`, optional `prev_info`, and a `Model` instance; logs via `BaseLogger`.  
**Technical Details**: Builds a 2‑ or 3‑message prompt (system → language/id, system → base prompt, optional system → prior info, user → code). Calls `model.get_answer_without_history`. Strips surrounding triple back‑ticks if present.  
**Data Flow**: `(part_id, part, Model, prev_info?)` → `str` (LLM answer). 
<a name="synchronous‑doc‑parts‑generation"></a>
## `generete_doc_parts` – synchronous chunked documentation  

- Reads the full code‑mix.  
- Calls `gen_doc_parts(full_code_mix, max_symbols, sync_model, config.language, progress_bar)`.  
- Writes the resulting markdown to `output_doc.md` and updates progress.  
- Provides a clear input‑output contract: **input** – raw code text; **output** – partially generated documentation limited by `max_symbols`. 
<a name="async-part-doc-generation"></a>
## Asynchronous Part Documentation Generation (`async_write_docs_by_parts`)  
**Responsibility**: Same as the sync variant but runs under an `asyncio.Semaphore` to limit concurrent LLM calls.  
**Interactions**: Accepts `AsyncModel`, optional `prev_info`, optional `update_progress` callback, and a shared `semaphore`.  
**Technical Details**: `async with semaphore` guards the request; prompt composition mirrors the sync version; result trimming identical; invokes `update_progress` after the LLM call.  
**Data Flow**: `(part, AsyncModel, semaphore, …)` → `await` → `str`. 
<a name="batch-doc-generation-sync"></a>
## Batch Documentation Generation (Synchronous) (`gen_doc_parts`)  
**Responsibility**: Orchestrates full‑code documentation by splitting the input, iterating over chunks, and concatenating the LLM outputs.  
**Interactions**: Calls `split_data`, `write_docs_by_parts`, and updates a `BaseProgress` sub‑task.  
**Technical Details**: After each part, retains the last 3000 characters as context for the next call (`prev_info`). Progress bar is incremented per chunk.  
**Data Flow**: `(full_code_mix, max_symbols, Model, language)` → `str` (complete documentation). 
<a name="batch-doc-generation-async"></a>
## Batch Documentation Generation (Asynchronous) (`async_gen_doc_parts`)  
**Responsibility**: Parallel version of `gen_doc_parts` using `asyncio.gather`.  
**Interactions**: Shares the same splitter, creates a semaphore (max 4 parallel calls), and updates `BaseProgress` via a lambda.  
**Technical Details**: Builds a list of `async_write_docs_by_parts` tasks, gathers results, and concatenates them with double newlines.  
**Data Flow**: `(full_code_mix, global_info, max_symbols, AsyncModel, language)` → `await` → `str` (full documentation). 
<a name="introlinks‑html‑link‑extraction‑intro"></a>
## `IntroLinks` – HTML link extraction and intro generation  
`IntroLinks.generate` extracts all HTML links from `info["full_data"]` using `get_all_html_links`, then produces a links‑focused introduction via `get_links_intro`, passing the link list, `model`, and language. The resulting markdown/HTML snippet is returned. 
<a name="html-link-extraction"></a>
## `get_all_html_links(data: str) → list[str]`  

*Responsibility* – Scans the supplied markdown for `<a name="…"></a>` anchors and returns a list of fragment identifiers prefixed with `#`.  
*Interactions* – Uses **BaseLogger** to emit progress messages; no external services.  
*Logic* – Compiles a regex `r'<a name=["\']?(.*?)["\']?></a>'`, iterates over `re.finditer`, keeps anchors longer than five characters, logs count and content, returns the collected list. 
<a name="introtext‑global‑introduction‑assembly"></a>
## `IntroText` – global introduction assembly  
`IntroText.generate` retrieves a high‑level description from `info["global_data"]` and creates a narrative introduction with `get_introdaction`, again using the supplied `model` and language. The final intro text is emitted for later concatenation. 
<a name="global‑intro‑generation"></a>
## `get_introdaction(global_data: str, model: Model, language: str = "en") → str`  

*Responsibility* – Generates a generic project overview based on the complete documentation text (`global_data`).  
*Interactions* – Prompt comprises `BASE_INTRO_CREATE` plus the full markdown as user content; result is obtained from the same LLM endpoint as above. No logging inside the function (caller may wrap). 
<a name="link‑driven‑intro-generation"></a>
## `get_links_intro(links: list[str], model: Model, language: str = "en") → str`  

*Responsibility* – Calls the supplied LLM (`model`) to synthesize a short introductory paragraph that references the provided link list.  
*Interactions* – Builds a system‑message prompt containing `BASE_INTRODACTION_CREATE_TEXT`, adds the link list as user content, forwards the prompt to `model.get_answer_without_history`. Logs before/after invocation.  
*Output* – Raw LLM response string intended for insertion at the top of the documentation. 
<a name="cache‑initialisation‑paths"></a>
## Cache folder and file‑path helpers  

- `CACHE_FOLDER_NAME = ".auto_doc_cache"` and `FILE_NAMES` map logical keys to filenames (`code_mix.txt`, `global_info.md`, etc.).  
- `__init__` creates the cache directory if missing, configures a file logger (`FileLoggerTemplate`) and stores injected `config`, `project_directory`, models, and progress bar.  
- `get_file_path(key)` builds an absolute path inside the cache; `read_file_by_file_key(key)` returns its UTF‑8 contents. 
<a name="cache‑cleanup‑routine"></a>
## `clear_cache` – optional log removal  

If `config.pcs.save_logs` is `False`, deletes the `report.txt` file, leaving other cached artifacts untouched.

**Data flow summary** – Input files → `CodeMix` → chunk generation → factory enrichment → ordering → final `output_doc.md`. All steps log progress, respect the user‑provided language setting, and optionally clean up temporary logs. 
<a name="logging-infrastructure"></a>
## Logging Infrastructure (`BaseLog`, `BaseLoggerTemplate`, `FileLoggerTemplate`, `BaseLogger`)  
**Responsibility**: Provides typed log objects (Error/Warning/Info) and a singleton logger that forwards messages to a configurable template (console or file).  
**Interactions**: `BaseLogger.set_logger()` injects a `BaseLoggerTemplate`; all calls route through `global_log` respecting the global `log_level`.  
**Technical Details**: `BaseLog.format()` yields the raw message; subclasses prepend a timestamp and severity. `BaseLogger.__new__` guarantees a single instance.  
**Data Flow**: `BaseLog` → `str` (formatted line) → `print` or file append. 
<a name="rich-console-progress"></a>
## Rich‑Console Progress (`LibProgress`)  
**Responsibility**: Wraps *rich*’s `Progress` to expose a generic sub‑task API used by the documentation pipeline.  
**Interactions**: Created with a shared `Progress` object; `create_new_subtask` registers a child task, `update_task` advances either the sub‑task or the main task, `remove_subtask` discards the current child.  
**Technical Details**: Maintains `_base_task` and `_cur_sub_task` IDs; advances are atomic calls to `Progress.update`.  
**Data Flow**: Calls → `Progress.update` → visual progress bar. 
<a name="console-progress"></a>
## Console‑Based Progress (`ConsoleGtiHubProgress` & `ConsoleTask`)  
**Responsibility**: Emits simple stdout progress for environments without *rich*.  
**Interactions**: `ConsoleGtiHubProgress.create_new_subtask` spawns a `ConsoleTask`; `update_task` increments either the active sub‑task or a generic “General Progress” task.  
**Technical Details**: `ConsoleTask.progress()` computes percentage and prints a line; removal clears the reference.  
**Data Flow**: Update call → printed percentage line. 
