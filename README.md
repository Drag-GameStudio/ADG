## Executive Navigation Tree

- 📂 Configuration  
  - [#autodocconfig.yml](#autodocconfig.yml)  
  - [#project-config-settings](#project-config-settings)  
  - [#global-generator-config](#global-generator-config)  
  - [#config-module-constants](#config-module-constants)  
  - [#configuration-loading](#configuration-loading)  
  - [#projectsettings-prompt-builder](#projectsettings-prompt-builder)  

- ⚙️ Model & Generation  
  - [#gptmodel-synchronous-generation](#gptmodel-synchronous-generation)  
  - [#asynchronousgptmodel-async-generation](#asynchronousgptmodel-async-generation)  
  - [#model-exhausted-exception](#model-exhausted-exception)  
  - [#parentmodel-state-management](#parentmodel-state-management)  

- 📄 Intro & Description  
  - [#intro-links](#intro-links)  
  - [#intro-text](#intro-text)  
  - [#html-link-extraction](#html-link-extraction)  
  - [#global-intro-generation](#global-intro-generation)  
  - [#link‑based‑intro-generation](#link‑based‑intro-generation)  
  - [#custom‑description‑generation](#custom‑description‑generation)  
  - [#code‑description‑generator](#code‑description‑generator)  
  - [#semantic‑ordering‑logic](#semantic‑ordering‑logic)  

- 📦 Compression & Pipeline  
  - [#compress-text-factory](#compress-text-factory)  
  - [#compress-function-workflow](#compress-function-workflow)  
  - [#async‑compression-pipeline](#async‑compression-pipeline)  
  - [#sync‑compare-pipeline](#sync‑compare-pipeline)  
  - [#document-generation-pipeline](#document-generation-pipeline)  
  - [#doc-generation‑pipeline](#doc-generation‑pipeline)  
  - [#docfactory-module-orchestration](#docfactory-module-orchestration)  
  - [#sync-part-documentation](#sync-part-documentation)  
  - [#async-part-documentation](#async-part-documentation)  

- 📊 Runtime & Logging  
  - [#autodocgenerator/auto_runner/run_file.py](#autodocgenerator/auto_runner/run_file.py)  
  - [#runtime-interactions](#runtime-interactions)  
  - [#history-helper](#history-helper)  
  - [#data-splitting-logic](#data-splitting-logic)  
  - [#logger-singleton-behavior](#logger-singleton-behavior)  
  - [#log-message-hierarchy](#log-message-hierarchy)  
  - [#file-logger-template](#file-logger-template)  
  - [#progress-implementations](#progress-implementations)  



 

<a name="autodocconfig.yml"></a>autodocconfig.yml Options  
The `autodocconfig.yml` file is a YAML configuration used by ADG. The available top‑level keys are:

- **project_name**: *string* – Name of the project.
- **language**: *string* – Language for the generated documentation (default `en`).
- **ignore_files**: *list of glob patterns* – Files or directories that should be excluded from processing.
- **project_settings**: *mapping* – Controls ADG behavior:
  - `save_logs`: *boolean* – Whether to save logs (`true`/`false`).
  - `log_level`: *integer* – Verbosity level (e.g., `1`).
- **project_additional_info**: *mapping* – Arbitrary key‑value pairs that become part of the project’s metadata.
- **custom_descriptions**: *list of strings* – Custom prompts or descriptions that will be turned into documentation modules.

Example structure (as shown in the repository):

```yaml
project_name: "Auto Doc Generator"
language: "en"
project_settings:
  save_logs: true
  log_level: 1
project_additional_info:
  global idea: "This project was created to help developers make documentations for them projects"
custom_descriptions:
  - "explain how install workflow with install.ps1 and install.sh scripts ..."
  - "how to use Manager class what parameters i need to give ..."
  - "explain how to write autodocconfig.yml file what options are available"
``` 
<a name="project-config-settings"></a>
## ProjectConfigSettings – Runtime configuration container  

`ProjectConfigSettings` holds transient flags used by the generation engine (e.g., `save_logs`, `log_level`).  
* **Methods** – `load_settings(data)` iterates over a dict and assigns each key/value to the instance via `setattr`, enabling dynamic injection from external sources (CLI, CI).  
* **Data flow** – Input: `dict[str, any]`; Output: the same object with updated attributes; no side‑effects beyond attribute mutation. 
<a name="global-generator-config"></a>
## Config – Core documentation‑generator settings  

`Config` aggregates all static options required by the `Manager` pipeline.  

| Attribute | Purpose |
|-----------|---------|
| `ignore_files` | Glob patterns excluded during repository scanning (e.g., byte‑code, virtual‑env folders). |
| `language` | ISO‑code passed to the LLM for localized output. |
| `project_name` | Identifier used for title generation and `ProjectSettings`. |
| `project_additional_info` | Arbitrary key/value pairs injected into `ProjectSettings`. |
| `pcs` | Instance of `ProjectConfigSettings` controlling runtime flags. |

* **Fluent setters** – `set_language`, `set_pcs`, `set_project_name`, `add_project_additional_info`, `add_ignore_file` each return `self` to allow chaining (e.g., `Config().set_language('ru').add_ignore_file('*.tmp')`).  
* **`get_project_settings()`** – Constructs a `ProjectSettings` object (from `autodocgenerator.preprocessor.settings`) with the configured `project_name` and any supplemental info, then returns it. This object is later consumed by the pre‑processor to embed project metadata into generated docs.

**Interactions**  
- `Config` is instantiated in the CI entry‑point and supplied to `Manager`.  
- `Manager` reads `ignore_files` to prune the file‑system walk, queries `language` for prompt localisation, and passes `pcs` to the logging subsystem.  
- `ProjectSettings` produced by `get_project_settings` is handed to the `Preprocessor`, which annotates source files before chunking.

**Side effects**  
All setters mutate the `Config` instance in‑place; `load_settings` may overwrite existing flags. No I/O occurs here—persistence is handled elsewhere (e.g., cache cleanup in `Manager`). 
<a name="config-module-constants"></a>
## Config Module Constants & Environment Loading  

The module defines several multi‑line string templates (`BASE_SYSTEM_TEXT`, `BASE_PART_COMPLITE_TEXT`, `BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`, `BASE_SETTINGS_PROMPT`) that drive the documentation generation workflow.  
It also loads `API_KEY` from the environment (via `dotenv`) and validates its presence, raising an exception if missing.  
`MODELS_NAME` enumerates the model identifiers used by the AI‑driven pre‑processor. 
<a name="configuration-loading"></a>
## Configuration Loading  

`read_config` parses the user‑provided *autodocconfig.yml*. It extracts:

* **ignore_files** – patterns added to `Config.ignore_files`.  
* **language**, **project_name**, **project_additional_info** – stored in a fresh `Config` instance via fluent setters.  
* **project_settings** – mapped onto a `ProjectConfigSettings` object via `load_settings`.  
* **custom_descriptions** – each string is wrapped in a `CustomModule` (from `factory.modules.general_modules`).  

The function returns a tuple **(Config, list[CustomModule])**, ready for the generation stage.

--- 
<a name="projectsettings-prompt-builder"></a>  
## ProjectSettings Prompt Builder  

`ProjectSettings` stores `project_name` and arbitrary key‑value metadata via `add_info`.  
The `prompt` property concatenates `BASE_SETTINGS_PROMPT` with the project name and each metadata entry, producing the system‑level prompt consumed by the compressor and description generators.  

--- 
<a name="autodocgenerator/auto_runner/run_file.py"></a>
Title: Using the Manager class

The `Manager` class is instantiated with the following parameters:

* **project_path** – Path to the root of the project (e.g., `"."`).
* **config** – An instance of `Config` loaded from `autodocconfig.yml`.
* **sync_model** – A synchronous `GPTModel` object (created with the API key).
* **async_model** – An asynchronous `AsyncGPTModel` object (created with the API key).
* **progress_bar** – An object implementing a progress interface, e.g., `ConsoleGtiHubProgress()`.

Example usage (mirrors the script in `autodocgenerator/auto_runner/run_file.py`):

```python
from autodocgenerator.manage import Manager
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.intro import IntroLinks
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.auto_runner.config_reader import read_config, Config
from autodocgenerator.engine.models.gpt_model import GPTModel, AsyncGPTModel
from autodocgenerator.engine.config.config import API_KEY

# Load configuration and custom modules
with open("autodocconfig.yml", "r", encoding="utf-8") as f:
    config_data = f.read()
config, custom_modules = read_config(config_data)

# Prepare GPT models
sync_model = GPTModel(API_KEY, use_random=False)
async_model = AsyncGPTModel(API_KEY)

# Create Manager instance
manager = Manager(
    project_path=".",          # path to the project
    config=config,            # Config object
    sync_model=sync_model,    # synchronous model
    async_model=async_model,  # asynchronous model
    progress_bar=ConsoleGtiHubProgress()  # progress display
)

# Generate documentation
manager.generate_code_file()                     # scans code files
manager.generete_doc_parts(max_symbols=6000)     # creates doc fragments
manager.factory_generate_doc(DocFactory(*custom_modules))  # applies custom modules
manager.order_doc()                              # orders sections
manager.factory_generate_doc(DocFactory(IntroLinks()))      # adds intro links
manager.clear_cache()                            # cleans temporary data

# Retrieve final documentation
output_doc = manager.read_file_by_file_key("output_doc")
print(output_doc)
``` 
<a name="gptmodel-synchronous-generation"></a>
## GPTModel – Synchronous Answer Generation  

`GPTModel` extends `Model` (which itself inherits `ParentModel`).  
* Instantiates a synchronous `Groq` client and a `BaseLogger`.  
* `generate_answer` builds the request payload from either the full conversation history or a single `prompt`.  
* It loops over `regen_models_name`, attempting `client.chat.completions.create`; on failure it logs a warning and advances `current_model_index`.  
* When the list is exhausted, `ModelExhaustedException` is raised.  
* The final answer is extracted from `chat_completion.choices[0].message.content` and logged at two verbosity levels before being returned. 
<a name="asynchronousgptmodel-async-generation"></a>
## AsyncGPTModel – Asynchronous Answer Generation  

Mirrors `GPTModel` but uses `AsyncGroq` and `async def generate_answer`.  
* All control flow (model rotation, error handling, logging) is identical, allowing the caller to `await` the result.  
* The method returns the generated string once the asynchronous request resolves. 
<a name="model-exhausted-exception"></a>
## `ModelExhaustedException`  

```python
class ModelExhaustedException(Exception):
    """If in list of models no one model is available for use."""
    ...
```

A lightweight sentinel exception raised by the model‑selection logic when all entries in `MODELS_NAME` are unavailable. It propagates up to the `Manager`, which catches it to trigger fallback handling. 
<a name="parentmodel-state-management"></a>
## ParentModel – Shared Model Configuration  

`ParentModel` stores the API key, a mutable `History` object, and the shuffled list `regen_models_name` that drives model rotation.  
* `current_model_index` tracks which entry in `regen_models_name` is active.  
* If `use_random` is true the order is randomized on each instance, enabling simple load‑balancing across `MODELS_NAME`. 
<a name="intro-links"></a>  
## IntroLinks – HTML Link Extraction  

**Responsibility**  
Collects every HTML anchor from the full‑document markdown (`full_data`) and produces a concise block of link references suitable for inclusion at the top of the generated documentation.  

**Interactions**  
- Receives a pre‑populated `info` dict from `DocFactory.generate_doc`.  
- Calls `get_all_html_links` (post‑processor) to parse `info["full_data"]`.  
- Passes the extracted link list, the shared `Model` instance, and the target language to `get_links_intro`, which formats the links using the LLM.  

**Technical Flow**  
1. `links = get_all_html_links(info.get("full_data"))` – regex/HTML parser returns `List[Dict]`.  
2. `intro_links = get_links_intro(links, model, info.get("language"))` – invokes the model’s `generate_answer` to craft natural‑language link introductions.  
3. Returns `intro_links` (markdown string).  

**Data Flow**  
- **Input**: `info["full_data"]` (raw doc), `info["language"]`.  
- **Output**: Markdown block containing formatted links.  
- **Side Effects**: None; model history is updated inside `get_links_intro` via `Model.get_answer`.  

--- 
<a name="intro-text"></a>  
## IntroText – Project Introduction Generation  

**Responsibility**  
Creates a high‑level introductory paragraph that summarizes the project’s purpose, using the global metadata (`global_data`).  

**Interactions**  
- Consumes `info["global_data"]` supplied by `DocFactory`.  
- Utilises the same shared `Model` instance to ask the LLM for a project‑specific intro via `get_introdaction`.  

**Technical Flow**  
1. `intro = get_introdaction(info.get("global_data"), model, info.get("language"))` – triggers an LLM call.  
2. Returns the generated paragraph as a markdown string.  

**Data Flow**  
- **Input**: `info["global_data"]`, `info["language"]`.  
- **Output**: Single‑paragraph markdown intro.  
- **Side Effects**: Model history updated inside `get_introdaction`.  

Both classes inherit from `BaseModule`, exposing a uniform `generate(info, model)` API used by `DocFactory` to stitch their outputs into the final documentation before the progress bar cleanup. 
<a name="html-link-extraction"></a>
## HTML‑Link Extraction (`get_all_html_links`)

**Responsibility** – Scans a markdown string for `<a name="…"></a>` anchors and returns a list of markdown‑style links (`#anchor`).  

**Interactions** – Called by post‑processing pipelines that need to reference generated sections; uses only the `BaseLogger` for diagnostic output.  

**Technical Details** – Compiles a regex `r'<a name=["\']?(.*?)["\']?>'`, iterates with `re.finditer`, prefixes each captured name with `#`, and logs count and content.  

**Data Flow** – *Input*: raw documentation string. *Output*: `list[str]` of `#anchor` links. No side‑effects beyond logging. 
<a name="global-intro-generation"></a>
## Global Intro Generation (`get_introdaction`)

**Responsibility** – Produces a one‑paragraph project introduction from `global_data` via the shared `Model` instance.  

**Interactions** – Consumes `info["global_data"]` supplied by `DocFactory`; uses the same `Model` (e.g., `GPTModel`) passed through the uniform `generate(info, model)` API.  

**Technical Details** – Builds a system‑prompt with `BASE_INTRO_CREATE`, injects the selected language, and calls `model.get_answer_without_history`. Returns the raw markdown paragraph.  

**Data Flow** – *Input*: `global_data: str`, `language: str`. *Output*: markdown string. *Side‑effect*: updates the model’s internal conversation history. 
<a name="link‑based‑intro-generation"></a>
## Link‑Based Intro Generation (`get_links_intro`)

**Responsibility** – Crafts an introduction that references a list of section links.  

**Interactions** – Receives the link list from `get_all_html_links`; forwards it to the LLM using `BASE_INTRODACTION_CREATE_TEXT`.  

**Technical Details** – Constructs a three‑message prompt (language system, intro template, user‑provided links) and calls `model.get_answer_without_history`.  

**Data Flow** – *Input*: `links: list[str]`, `language`. *Output*: generated intro markdown. Logs progress at level 1. 
<a name="custom‑description‑generation"></a>
## Custom Description Generation (`generete_custom_discription`)

**Responsibility** – Iterates over split documentation chunks, asking the LLM to produce a titled, anchored description for a user‑defined topic.  

**Interactions** – Uses the same `Model` instance; each iteration may break early if a satisfactory answer is returned.  

**Technical Details** – For each chunk it sends a strict system prompt (rules, context, title request) and a user prompt containing `custom_description`. The LLM’s response must start with `<a name="URL"></a>` followed by the answer or special tokens (`!noinfo`).  

**Data Flow** – *Input*: `splited_data: str`, `custom_description: str`, `language`. *Output*: the first non‑empty LLM response that satisfies the rules. Side‑effects limited to model history updates and logging. 
<a name="code‑description‑generator"></a>  
## Code Description Generator  

`generate_discribtions_for_code` sends each source file through a fixed instruction prompt that asks the model to enumerate public components, parameters, and usage examples.  
Results are collected in a list; progress is tracked with a sub‑task.  

**Output** – list of markdown‑formatted documentation strings, one per input file. 
<a name="semantic‑ordering‑logic"></a>
## Semantic Ordering (`get_order`)

**Responsibility** – Receives a dictionary mapping anchors to chunk text and returns the chunks reordered according to LLM‑determined semantic grouping.  

**Interactions** – Works after `split_text_by_anchors`; supplies the title list (`list(chanks.keys())`) to the LLM and rebuilds the final document order.  

**Technical Details** – Sends a user‑only prompt requesting a comma‑separated, `#`‑prefixed title list; parses the response, then concatenates the corresponding chunk values.  

**Data Flow** – *Input*: `chanks: dict[str, str]`. *Output*: single markdown string with reordered sections. Logs each step and the final ordering.

["#global-intro-generation", "#link‑based‑intro-generation", "#custom‑description‑generation", "#semantic‑ordering‑logic"] 
<a name="compress-text-factory"></a>
## `get_BASE_COMPRESS_TEXT` Factory  

```python
def get_BASE_COMPRESS_TEXT(start, power):
    return f"""
You will receive a large code snippet (up to ~{start} characters).
...
```

*Purpose*: Returns a formatted instruction block whose size scales with `start` and `power`.  
*Logic Flow*: Interpolates the supplied parameters into a template that specifies analysis, summary length, and a strict usage‑example clause. The returned string is later injected into prompts that guide the AI to produce concise summaries and runnable examples. 
<a name="compress-function-workflow"></a>  
## Compress Function Workflow  

The **compress** routine receives raw text, a `ProjectSettings` instance, a GPT `Model`, and a numeric `compress_power`.  
It builds a three‑message prompt: the project‑specific system prompt, a static compression template from `get_BASE_COMPRESS_TEXT`, and the user payload. The model’s `get_answer_without_history` returns a shortened version, which is returned directly to the caller.  

**Inputs** – `data: str`, `project_settings.prompt`, `compress_power`.  
**Outputs** – compressed string.  
**Side‑effects** – none (pure function).  

--- 
<a name="async‑compression-pipeline"></a>  
## Asynchronous Compression‑And‑Compare Pipeline  

`async_compress` mirrors the synchronous prompt creation but runs under an `asyncio.Semaphore` to limit concurrency.  
`async_compress_and_compare` spawns one coroutine per element, gathers results, then re‑chunks them into groups of `compress_power`.  
Progress is updated after each coroutine finishes.  

**Key parameters** – `semaphore` (max 4 concurrent calls by default).  

--- 
<a name="sync‑compare-pipeline"></a>  
## Synchronous Compression‑And‑Compare Pipeline  

`compress_and_compare` iterates over a list of file contents, groups them in batches of `compress_power`, and concatenates each batch’s compressed results.  
It uses a `BaseProgress` sub‑task to report progress. The resulting list length equals `ceil(len(data)/compress_power)`.  

**Assumptions** – `compress_power` ≥ 2; model is synchronous.  

--- 
<a name="document-generation-pipeline"></a>
## Document Generation Pipeline  

`gen_doc` orchestrates the end‑to‑end documentation flow:

1. **Model Instantiation** – creates a synchronous `GPTModel` and an asynchronous `AsyncGPTModel` using the global `API_KEY`.  
2. **Manager Construction** – passes the project root, parsed `Config`, both models, and a `ConsoleGtiHubProgress` bar to `Manager`.  
3. **Code Extraction** – `manager.generate_code_file()` scans the repository and caches source files.  
4. **Chunked AI Prompting** – `manager.generete_doc_parts(max_symbols=6000)` splits code into ≤6000‑symbol blocks and queries the GPT models.  
5. **Custom Module Injection** – `manager.factory_generate_doc(DocFactory(*custom_modules))` lets each `CustomModule` inject user‑defined sections.  
6. **Ordering & Intro Links** – `manager.order_doc()` reorders parts; a second factory call adds `IntroLinks`.  
7. **Cache Cleanup** – `manager.clear_cache()` removes temporary artifacts.  

Finally, `manager.read_file_by_file_key("output_doc")` returns the assembled markdown string, which the CI step writes to `README.md`.  

**Inputs:** project path, `Config`, list of `CustomModule`.  
**Outputs:** rendered documentation (`output_doc`).  
**Side effects:** filesystem writes to the `.auto_doc_cache` folder and progress output to the console. 
<a name="doc-generation‑pipeline"></a>
## Documentation Generation Pipeline  

`gen_doc_parts` (sync) and `async_gen_doc_parts` (async) invoke the splitter, then iterate over chunks, calling the respective part‑writer, concatenating results, and feeding a sliding “context window” (`result[-3000:]`) to preserve continuity.  
Both functions drive a `BaseProgress` sub‑task, log final length, and return the full assembled documentation. 
<a name="docfactory-module-orchestration"></a>
## DocFactory – Module‑Level Documentation Assembly  

`DocFactory` receives an ordered list of `BaseModule` instances.  
* `generate_doc` creates a sub‑task in the supplied `BaseProgress`, iterates over modules, invokes `module.generate(info, model)`, concatenates results, and logs each module’s output.  
* The final documentation string is returned after progress cleanup.

**Data Flow Summary**  
1. Caller creates a `GPTModel`/`AsyncGPTModel` with optional history.  
2. `generate_answer` → selects model name → API call → logs → returns answer.  
3. `Model.get_answer` updates history before/after the call.  
4. `DocFactory` feeds the same model instance to each documentation module, stitching their outputs into the final doc. 
<a name="sync-part-documentation"></a>
## Synchronous Part Documentation  

`write_docs_by_parts` builds a system‑role prompt containing language, part ID, `BASE_PART_COMPLITE_TEXT`, and optional `prev_info`.  
It sends the prompt to `model.get_answer_without_history`, strips surrounding ``` fences, logs the raw and trimmed answer, and returns the cleaned markdown.  
**Inputs:** `part_id`, `part`, `model`, optional `prev_info`, `language`.  
**Outputs:** formatted documentation string for that part. 
<a name="async-part-documentation"></a>
## Asynchronous Part Documentation  

`async_write_docs_by_parts` mirrors the synchronous flow but runs inside an `asyncio.Semaphore`, uses `await async_model.get_answer_without_history`, and optionally calls `update_progress`.  
It returns the same trimmed markdown. 
<a name="runtime-interactions"></a>
## Runtime Interactions with Manager & Preprocessor  

* `Config` is instantiated at CI entry‑point, then supplied to `Manager`.  
* `Manager` reads `ignore_files` from the constants, queries `language` for localisation, and forwards `pcs` to the logging subsystem.  
* The settings object produced by `get_project_settings` (built from the above templates) is handed to the `Preprocessor`, which annotates source files before chunking.  

All setters mutate the `Config` instance in‑place; `load_settings` can overwrite flags, but no I/O occurs within this fragment—the persistence layer lives elsewhere (e.g., cache cleanup in `Manager`). 
<a name="history-helper"></a>
## History – Conversation Buffer  

Provides `add_to_history(role, content)` and initializes with the system prompt (`BASE_SYSTEM_TEXT`).  
The buffer is consumed by `Model.get_answer*` helpers to maintain a turn‑based dialogue. 
<a name="data-splitting-logic"></a>
## Data Splitting Logic  

`split_data` receives the full source text and a `max_symbols` limit.  
It iteratively chops oversized fragments ( > 1.5 × limit ) in half, then packs the pieces into `split_objects` ensuring each object stays ≤ 1.25 × limit.  
**Inputs:** `full_code_mix: str`, `max_symbols: int`.  
**Outputs:** `List[str]` of code parts ready for LLM processing.  
Side‑effects: logs progress via `BaseLogger`. 
<a name="logger-singleton-behavior"></a>
## BaseLogger – Singleton Facade  

`BaseLogger` implements the *Borg*‑style singleton via `__new__`, guaranteeing a single façade instance throughout the process. The façade holds a reference to a concrete `BaseLoggerTemplate` (e.g., `FileLoggerTemplate`) set by `set_logger`. Calls to `log()` delegate to `logger_template.global_log()`, which respects the configured `log_level` before emitting the message. 
<a name="log-message-hierarchy"></a>
## Structured Log Objects  

`BaseLog` supplies the common payload (`message`, `level`) and a timestamp prefix (`_log_prefix`). Sub‑classes (`ErrorLog`, `WarningLog`, `InfoLog`) override `format()` to prepend a severity tag (`[ERROR]`, `[WARNING]`, `[INFO]`) to the timestamped text. The formatted string is what the logger templates write or print. 
<a name="file-logger-template"></a>
## File‑Based Persistence  

`FileLoggerTemplate` extends `BaseLoggerTemplate`. Its `log()` opens `file_path` in append mode and writes `log.format() + "\n"`. Because `BaseLoggerTemplate.log()` is overridden, `global_log()` still applies the level filter before persisting. 
<a name="progress-implementations"></a>
## Progress Reporting Implementations  

`LibProgress` wraps *rich*’s `Progress`, creating a base task and optional sub‑tasks; `update_task()` advances either the current sub‑task or the base task.  
`ConsoleGtiHubProgress` provides a lightweight, stdout‑only alternative using `ConsoleTask`. Both classes inherit from the abstract `BaseProgress`, which defines the required interface (`create_new_subtask`, `update_task`, `remove_subtask`).

**Data flow:** UI components invoke `BaseLogger.log(ErrorLog(...))` → `BaseLogger` forwards to the active template → formatted string written to console or file. Progress objects receive `create_new_subtask`/`update_task` calls from the documentation pipeline, emitting visual feedback without side‑effects beyond stdout or *rich* rendering. 
