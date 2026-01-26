## Executive Navigation Tree
- 📂 Setup & Configuration
  - [Install Workflow Setup](#install-workflow-setup)
  - [Configuration Loading And Validation](#configuration-loading-and-validation)
  - [Manager Configuration](#manager-configuration)
  - [Projectsettings Prompt Builder](#projectsettings-prompt-builder)
  - [Command Line Invocation Logic](#command-line-invocation-logic)

- ⚙️ Documentation Generation
  - [Documentation Pipeline Trigger](#documentation-pipeline-trigger)
  - [Execution Flow Summary](#execution-flow-summary)
  - [Documentation Generation Workflow](#documentation-generation-workflow)
  - [Autodocfile Parameters](#autodocfile-parameters)
  - [Docfactory Orchestration](#docfactory-orchestration)
  - [Global Introduction Generation](#global-introduction-generation)
  - [Intro With Links Generation](#intro-with-links-generation)
  - [Custom Description Generation](#custom-description-generation)
  - [Anchor‑Ordering‑Cleanup](#anchor‑ordering‑cleanup)
  - [Anchor‑Chunk‑Splitting](#anchor‑chunk‑splitting)
  - [Semantic‑Ordering](#semantic‑ordering)
  - [Html Link Extraction](#html-link-extraction)
  - [Factory‑Doc‑Assembly](#factory‑doc‑assembly)
  - [Doc‑Parts‑Generation](#doc‑parts‑generation)
  - [Custommodule Intro Modules](#custommodule-intro-modules)

- 🤖 Model Orchestration
  - [Asyncgptmodel Implementation](#asyncgptmodel-implementation)
  - [Gptmodel Synchronous Flow](#gptmodel-synchronous-flow)
  - [Parentmodel Setup And Rotation](#parentmodel-setup-and-rotation)
  - [Synchronous‑Part‑Doc‑Generator](#synchronous‑part‑doc‑generator)
  - [Asynchronous‑Part‑Doc‑Generator](#asynchronous‑part‑doc‑generator)
  - [Synchronous‑Multi‑Part‑Orchestrator](#synchronous‑multi‑part‑orchestrator)
  - [Asynchronous‑Multi‑Part‑Orchestrator](#asynchronous‑multi‑part‑orchestrator)

- 🔀 Data Splitting & Repository
  - [Spliter Entry Point](#spliter-entry-point)
  - [Data‑Splitting Loop](#data‑splitting‑loop)
  - [Repository‑Mix Builder](#repository‑mix‑builder)
  - [Code‑Mix Generation](#code‑mix‑generation)

- 🗄️ Caching & Compression
  - [Cache‑File Access](#cache‑file-access)
  - [Compress Function](#compress-function)
  - [Batch Compression Sync](#batch-compression-sync)
  - [Batch Compression Async](#batch-compression-async)

- 📊 Logging & Progress
  - [Singleton‑Logger‑Implementation](#singleton‑logger‑implementation)
  - [Log‑Message‑Hierarchy](#log‑message‑hierarchy)
  - [Progress‑Abstraction](#progress‑abstraction)
  - [Rich‑Implementation](#rich‑implementation)
  - [Console‑Task‑Helper](#console‑task‑helper)
  - [Fallback‑Console‑Progress](#fallback‑console‑progress)

 



<a name="install-workflow-setup"></a>
To set up the installation workflow, run the PowerShell script on Windows using:  
`irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex`  

On Linux‑based systems, execute the shell script with:  
`curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash`  

Additionally, add a secret variable named **GROCK_API_KEY** to your GitHub Actions configuration, containing the API key obtained from the Grock documentation site (grockdocs.com). 
<a name="configuration-loading-and-validation"></a>
## Configuration Loading and Validation  

- **`load_config()`** reads the global settings file, merges environment overrides, and returns a structured config object.  
- Immediate checks ensure required keys (e.g., `source_path`, `output_dir`, `templates`) exist; missing keys raise `ConfigurationError`.  
- The validated config is the sole input to the pipeline, guaranteeing deterministic behavior. 
<a name="manager-configuration"></a>
## Manager Class – Configuration & State  

`Manager` orchestrates the end‑to‑end documentation pipeline. It receives the project root, a `Config` object, optional LLM model instances (`Model` / `AsyncModel`), and a progress UI (`BaseProgress`). During construction it:  

* Stores configuration and progress objects.  
* Instantiates a file‑based logger that writes to **report.txt** inside a hidden cache folder (`.auto_doc_cache`).  
* Guarantees the cache directory exists, creating it if necessary. 
<a name="projectsettings-prompt-builder"></a>ProjectSettings Prompt Builder  
`ProjectSettings.prompt` concatenates the global `BASE_SETTINGS_PROMPT` with the project name and any key/value pairs added via `add_info`. The resulting string feeds the system role of every compression request.

## 
<a name="command-line-invocation-logic"></a>
## Command‑Line Invocation Logic  

The `if __name__ == "__main__":` block parses CLI arguments (if any), invokes `load_config()` from `autodocgenerator.engine.config.config`, validates the returned dictionary, and passes it to `run_documentation_pipeline()` which orchestrates the end‑to‑end doc generation. 
<a name="documentation-pipeline-trigger"></a>
## Documentation Pipeline Trigger  

`run_documentation_pipeline(config)` sequentially executes:  

1. **Source Discovery** – walks `config["source_path"]` to collect parsable modules.  
2. **Parsing Engine** – feeds each file to the parser subsystem, producing intermediate ASTs.  
3. **Renderer** – transforms ASTs into Markdown/HTML using the selected template set.  
4. **Writer** – writes rendered files into `config["output_dir"]`, optionally cleaning stale artifacts.

Side effects include filesystem writes, optional logging to `config["log_file"]`, and temporary cache creation. 
<a name="execution-flow-summary"></a>
## Execution Flow Summary  

1. CLI start → load & validate config.  
2. Valid config → `run_documentation_pipeline`.  
3. Pipeline → generated documentation persisted on disk.  

All exceptions propagate to the top level, where a concise error message is printed and the process exits with a non‑zero status. 
<a name="documentation-generation-workflow"></a>  
## Documentation Generation Workflow  

**Responsibility**  
`autodocgenerator/auto_runner/run_file.py` orchestrates the end‑to‑end generation of project documentation. It loads the user configuration, instantiates synchronous and asynchronous GPT models, creates a `Manager` that drives file parsing, doc‑part creation, factory‑based rendering, ordering, and cache cleanup, finally returning the assembled markdown.  

**Interactions**  
- **Config Reader** – imports `read_config` from `config_reader.py` to parse *autodocconfig.yml*.  
- **Model Layer** – creates `GPTModel` (blocking) and `AsyncGPTModel` (non‑blocking) using the API key from `engine/config/config.py`.  
- **Manager** – `autodocgenerator.manage.Manager` receives the project path, configuration, models, and a progress bar (`ConsoleGtiHubProgress`).  
- **Factories** – `DocFactory` builds doc sections from custom modules (`CustomModule`) and from the built‑in `IntroLinks`.  
- **UI** – progress feedback is sent to GitHub‑style console via `ConsoleGtiHubProgress`.  

**Technical Details**  
```python
def gen_doc(project_path: str, config: Config, custom_modules):
    sync_model = GPTModel(API_KEY, use_random=False)
    async_model = AsyncGPTModel(API_KEY)

    manager = Manager(
        project_path,
        config=config,
        sync_model=sync_model,
        async_model=async_model,
        progress_bar=ConsoleGtiHubProgress(),
    )
    # Core pipeline
    manager.generate_code_file()
    manager.generete_doc_parts(max_symbols=7000)
    manager.factory_generate_doc(DocFactory(*custom_modules))
    manager.order_doc()
    manager.factory_generate_doc(DocFactory(IntroLinks()))
    manager.clear_cache()
    return manager.read_file_by_file_key("output_doc")
```  

- `generate_code_file()` scans the repository, respecting `Config.ignore_files`.  
- `generete_doc_parts()` chunks source code (≤ 7000 symbols) and queries the GPT models.  
- Two `factory_generate_doc` calls render custom user‑supplied modules first, then prepend standard intro links.  
- `order_doc()` ensures a logical section order before writing the final file.  

**Data Flow**  
1. **Input** – `project_path` (root of the repo) and a fully populated `Config` object (language, ignore patterns, project info).  
2. **Processing** – Files → code extraction → GPT prompts → text fragments → module factories → ordered markdown.  
3. **Outputs** – Cached files under `.auto_doc_cache/`, and the final document string returned by `read_file_by_file_key("output_doc")`.  
4. **Side Effects** – Writes intermediate cache, updates progress UI, and may raise exceptions from model calls or file I/O.  

This module acts as the command‑line entry point (`if __name__ == "__main__":`) that ties configuration loading to the documentation pipeline. 
<a name="autodocfile-parameters"></a>
The file is a YAML document that defines the behavior of the documentation generator.  
Key sections and available options:

* **project_name** – a short title for the project.  
* **language** – language code for the generated text, default “en”.  
* **project_options** – a map of boolean and numeric controls:  
  * **save_logs** – true to keep generation logs, false otherwise.  
  * **log_level** – integer indicating the verbosity of log output.  
* **project_additional_info** – free‑form key/value pairs that are inserted into the generated material (e.g., a global idea or description).  
* **ignore_files** – list of glob patterns for files that should be skipped during analysis.  
* **custom_descriptions** – an array of strings; each string is interpreted as a custom instruction for the generator, allowing you to request specific sections or explanations.

When writing the file, list each option under its heading using proper YAML indentation. Only the sections you need are required; omitted sections will use the defaults (language “en”, empty project name, default project_options). 
<a name="docfactory-orchestration"></a>
## DocFactory Orchestration  

`DocFactory` receives an ordered list of `BaseModule` subclasses. `generate_doc` creates a progress sub‑task, invokes each module’s `generate(info, model)`, concatenates their outputs, and logs module completion. It returns the assembled documentation string. 
<a name="global-introduction-generation"></a>Global Introduction Generation  
`get_introdaction` (note spelling) builds a similar prompt using `BASE_INTRO_CREATE` and the whole documentation body, then forwards it to the model. The raw intro string is returned unchanged.

## 
<a name="intro-with-links-generation"></a>Introduction‑With‑Links Generation  
`get_links_intro` receives the link list and a **Model** implementation. It composes a three‑message prompt (system language directive, `BASE_INTRODACTION_CREATE_TEXT`, and the link payload) and calls `model.get_answer_without_history`. Logging surrounds the call, and the generated introduction text is returned.

## 
<a name="custom-description-generation"></a>Custom Description Generation  
`generete_custom_discription` iterates over split document chunks, sending each to the model with a strict system prompt that forces a single‑anchor output (`<a name="…"></a>`). It aborts on the first non‑error response, otherwise returns an empty string. The rules prevent filename, extension, or external URL leakage.

## 
<a name="anchor‑ordering‑cleanup"></a>
## Anchor‑Based Ordering & Cache Cleanup  

`order_doc` extracts anchor‑segmented sections via `split_text_by_anchors`, asks the LLM (`self.sync_model`) to compute the correct order (`get_order`), and rewrites the file.  

`clear_cache` removes **report.txt** unless `config.pcs.save_logs` is true, ensuring optional log retention.  

**Data Flow Summary** – Input files → `CodeMix` → raw mix → `gen_doc_parts` → partial doc → `DocFactory` → enriched doc → `split_text_by_anchors`/`get_order` → final ordered doc. Side effects include file writes, logger entries, and progress UI updates.

## 
<a name="anchor‑chunk‑splitting"></a>Anchor‑Based Chunk Splitting  
`split_text_by_anchors` uses a look‑ahead regex to split a full doc into sections that start with a valid anchor (`<a name="…"></a>`). It validates that each chunk yields a corresponding link via `extract_links_from_start`; mismatches return `None`. The result is a dict mapping “#anchor” keys to their text blocks.

## 
<a name="semantic‑ordering"></a>Semantic Ordering of Documentation Sections  
`get_order` receives the chunk dict and a **Model**. It logs the incoming keys, prompts the model to return a comma‑separated, semantically sorted list of titles (preserving the leading “#”). The function reassembles the final ordered document by concatenating the chunks in the returned order, logging each addition.

## 
<a name="html-link-extraction"></a>HTML Link Extraction Logic  
`get_all_html_links` scans a documentation string for anchor tags (`<a name=…></a>`). It logs start/end messages via **BaseLogger**, builds a regex pattern, iterates with `re.finditer`, and appends up‑to‑five links prefixed with “#”. The function returns the collected list, providing the first‑stage data for downstream ordering.

## 
<a name="factory‑doc‑assembly"></a>
## Factory‑Driven Documentation Assembly  

`factory_generate_doc` loads the current output and code mix, builds an `info` dict (`language`, `full_data`, `code_mix`), and logs the module chain of the supplied `DocFactory`. It then calls `doc_factory.generate_doc(info, self.sync_model, self.progress_bar)`. The factory‑produced fragment is prepended to the existing doc and persisted. 
<a name="doc‑parts‑generation"></a>
## Synchronous Documentation Chunking  

`generete_doc_parts` (typo retained) reads the code‑mix, then invokes `gen_doc_parts` with:  

* raw code mix,  
* `max_symbols` limit (default 5 000),  
* the synchronous LLM (`self.sync_model`),  
* target language (`self.config.language`),  
* the progress UI.  

The resulting Markdown is written to **output_doc.md** and progress updated. 
<a name="custommodule-intro-modules"></a>
## CustomModule & Intro Modules  

* `CustomModule` injects a user‑provided description into a generated custom intro by preprocessing code via `split_data` and delegating to `generete_custom_discription`.  
* `IntroLinks` extracts HTML links from `info["full_data"]` and builds a linked introduction using `get_links_intro`.  
* `IntroText` produces a plain introduction via `get_introdaction`.  

All modules depend on a `Model` instance for LLM calls and output plain‑text Markdown/HTML fragments. 
<a name="asyncgptmodel-implementation"></a>
## AsyncGPTModel Implementation  

`AsyncGPTModel` extends `AsyncModel` to call Groq’s async client. It builds a shuffled list of candidate model names (`regen_models_name`) from the global config, logs each step via `BaseLogger`, and retries on failure, cycling through the list. Input: optional prompt or full history; output: generated answer string. Side‑effects: async HTTP request, log entries, possible `ModelExhaustedException` if no models remain. 
<a name="gptmodel-synchronous-flow"></a>
## GPTModel Synchronous Flow  

`GPTModel` mirrors `AsyncGPTModel` but uses the synchronous `Groq` client. It follows the same retry loop, logs progress, and returns the answer. It also respects the `with_history` flag to select either the stored conversation (`self.history.history`) or a raw prompt. 
<a name="parentmodel-setup-and-rotation"></a>
## ParentModel Setup & Model Rotation  

`ParentModel` (base for both sync/async) stores the API key, a `History` instance, and prepares `regen_models_name`—a shuffled copy of `MODELS_NAME` when `use_random=True`. It tracks `current_model_index` to rotate through candidates after each failure. 
<a name="synchronous‑part‑doc‑generator"></a>Synchronous Part Documentation Generator (`write_docs_by_parts`)  
Builds a two‑message system prompt (language + part‑ID, then `BASE_PART_COMPLITE_TEXT`). If a previous part’s summary exists, it is appended as an additional system message. The user message contains the raw source fragment. The `Model`’s `get_answer_without_history` call returns a markdown block; surrounding triple‑backticks are stripped before the final string is returned. Logs start, length, and raw answer (level 2).

## 
<a name="asynchronous‑part‑doc‑generator"></a>Asynchronous Part Documentation Generator (`async_write_docs_by_parts`)  
Mirrors the synchronous flow but runs inside an `async with semaphore` to cap concurrency (default 4). Uses an `AsyncModel` for non‑blocking `await get_answer_without_history`. An optional `update_progress` callback is invoked after each answer. Logging mirrors the sync variant.

## 
<a name="synchronous‑multi‑part‑orchestrator"></a>Synchronous Multi‑Part Documentation Orchestrator (`gen_doc_parts`)  
1. Calls `split_data` to obtain `splited_data`.  
2. Creates a progress sub‑task.  
3. Sequentially invokes `write_docs_by_parts` for each chunk, concatenating results into `all_result`.  
4. Keeps a 3000‑character tail of the previous answer to provide context for the next part.  
5. Updates the progress bar after each iteration and logs final output length.

## 
<a name="asynchronous‑multi‑part‑orchestrator"></a>Asynchronous Multi‑Part Documentation Orchestrator (`async_gen_doc_parts`)  
Splits the input, creates a semaphore (max 4), and dispatches `async_write_docs_by_parts` for every chunk via `asyncio.gather`. Progress updates are wired through a lambda calling `progress_bar.update_task()`. Results are concatenated in order, progress sub‑task is removed, and the assembled documentation is logged.

## 
<a name="spliter-entry-point"></a>Spliter Entry Point (`split_data`) – Partial  
`split_data(data, max_symbols)` prepares to split a large document into sub‑strings respecting a symbol limit. The implementation continues beyond the shown snippet, but its purpose is to feed the compressor pipeline with appropriately sized chunks.

## 
<a name="data‑splitting‑loop"></a>Data Splitting Loop (`split_data`)  
Iteratively refines a list of file‑derived chunks (`splited_by_files`) so that no element exceeds 1.5 × `max_symbols`. Oversized entries are bisected at the halfway point, inserted back, and the process repeats until stability. The second phase packs these normalized fragments into `split_objects`, inserting line breaks and respecting a 1.25 × `max_symbols` buffer. Returns a list of size‑constrained text blocks ready for downstream processing.

## 
<a name="repository‑mix‑builder"></a>Repository Content Aggregation (`CodeMix`)  
`CodeMix` walks a repository rooted at `root_dir`, respecting `ignore_patterns`. `should_ignore` checks each path against glob patterns, file basenames, and any path component. `build_repo_content` writes a hierarchical tree view to `repomix-output.txt`, then appends each non‑ignored file’s relative path (`<file path="…">`) followed by its raw content. Progress is logged throughout.  

**Data Flow:**  
- Source files → `CodeMix` → mixed text file → `split_text_by_anchors` → chunk dict → `get_order` → ordered doc → optional `get_links_intro`/`get_introdaction`/`generete_custom_discription` → final documentation output.  
- Side effects: file creation (`repomix-output.txt`), logger entries, and UI progress updates.

## 
<a name="code‑mix‑generation"></a>
## Code Mix Generation Workflow  

`generate_code_file` creates a `CodeMix` instance (respecting `config.ignore_files`) and calls `build_repo_content` to serialize the entire repository into **code_mix.txt**. Logging marks start/end, and the progress bar task is advanced. 
<a name="cache‑file‑access"></a>
## Cached File Access Helpers  

* `get_file_path(file_key)` builds an absolute path inside the cache using the static `FILE_NAMES` map.  
* `read_file_by_file_key(file_key)` opens the derived path, reads UTF‑8 content and returns it. These utilities centralise path handling for all subsequent steps. 
<a name="compress-function"></a>Compress Function Logic  
`compress(data, project_settings, model, compress_power)` builds a three‑message prompt: the project‑specific system prompt, a compression directive from `get_BASE_COMPRESS_TEXT`, and the raw `data`. It forwards this prompt to `model.get_answer_without_history` and returns the model’s summary.  
*Input*: plain text, `ProjectSettings` instance, `Model`, integer power.  
*Output*: compressed string.  
*Side‑effects*: none.

## 
<a name="batch-compression-sync"></a>Synchronous Batch Compression (`compress_and_compare`)  
Partitions a list of strings into groups of `compress_power`. For each element it calls `compress`, concatenates results per group, and updates a `BaseProgress` sub‑task. Returns a list where each entry aggregates the compressed texts of one group.

## 
<a name="batch-compression-async"></a>Asynchronous Batch Compression (`async_compress_and_compare`)  
Creates a semaphore (max 4 concurrent calls) and launches `async_compress` for every element. Each coroutine builds the same three‑message prompt, awaits `model.get_answer_without_history`, and updates progress. After `asyncio.gather`, groups results into chunks of size `compress_power` and returns the aggregated list.

## 
<a name="singleton‑logger‑implementation"></a>Singleton Logger Implementation (`BaseLogger`)  
`BaseLogger.__new__` ensures a single shared instance. Clients set a concrete `BaseLoggerTemplate` (e.g., `FileLoggerTemplate`) via `set_logger`. Calls to `log` forward to the template’s `global_log`, which respects the configured log‑level filter.

## 
<a name="log‑message‑hierarchy"></a>Log Message Hierarchy (`BaseLog` & subclasses)  
`BaseLog` stores a message and level; subclasses (`InfoLog`, `WarningLog`, `ErrorLog`) override `format()` to prepend a timestamp and severity tag. The hierarchy enables uniform, level‑aware console or file output across the documentation pipeline.

## 
<a name="progress‑abstraction"></a>Progress Abstraction (`BaseProgress`)  
Defines the minimal interface for creating, updating, and removing sub‑tasks. Concrete classes implement these hooks so the documentation pipeline can switch between rich‑based UI or plain console output without code changes.

## 
<a name="rich‑implementation"></a>Rich‑Library Implementation (`LibProgress`)  
Wraps **rich.Progress**:  
* `__init__` registers a base task (`General progress`) with a configurable total (default 4).  
* `create_new_subtask(name, total_len)` adds a child task and stores its ID.  
* `update_task()` advances the current sub‑task if present, otherwise the base task.  
* `remove_subtask()` clears the reference, allowing the next chunk to start fresh.  
All calls forward to `rich.Progress.update`, guaranteeing thread‑safe visual feedback.

## 
<a name="console‑task-helper"></a>Console Task Helper (`ConsoleTask`)  
Utility that prints a simple progress line.  
* `start_task()` emits the start banner.  
* `progress()` increments an internal counter, computes a percentage, and prints it.  
Used by the fallback console progress class.

## 
<a name="fallback‑console‑progress"></a>Fallback Console Progress (`ConsoleGtiHubProgress`)  
Implements the same API as `BaseProgress` for environments lacking Rich:  
* Holds a persistent “General Progress” `ConsoleTask`.  
* `create_new_subtask` spawns a dedicated `ConsoleTask`.  
* `update_task` delegates to the active task or the general one.  
* `remove_subtask` discards the current sub‑task.  

**Data Flow** – Caller (e.g., `gen_doc_parts`) invokes `create_new_subtask` → progress updates via `update_task` → optional `remove_subtask`. No side effects beyond console/rich output. The abstraction keeps the rest of the system agnostic to the UI backend. 
