## Executive Navigation Tree
* 📂 **Setup & Configuration**
  * [Install Workflow Setup](#install-workflow-setup)
  * [Config Reader Responsibility](#config-reader-responsibility)
  * [Config Reader Interaction](#config-reader-interaction)
  * [Config Reader Technical Details](#config-reader-technical-details)
  * [Config Reader Data Flow](#config-reader-data-flow)
  * [Configuration Object Construction](#configuration-object-construction)
  * [Project Settings Prompt](#projectsettings-prompt)
  * [Data Splitting Algorithm](#data-splitting-algorithm)
* ⚙️ **Core Engine**
  * [Runfile Execution](#runfile-execution)
  * [Manager Orchestration Pipeline](#manager-orchestration-pipeline)
  * [Semantic Ordering Workflow](#semantic-ordering-workflow)
  * [Data Flow and Side Effects](#data-flow-and-side‑effects)
  * [Parent Model Shared Configuration](#parentmodel-shared-configuration)
  * [History Conversation State](#history-conversation-state)
* 📄 **Documentation Generation**
  * [GPT Model Synchronous Generation](#gptmodel-synchronous-generation)
  * [Async GPT Model Asynchronous Generation](#asyncgptmodel-asynchronous-generation)
  * [Doc Factory Orchestrating Documentation Generation](#docfactory-orchestrating-documentation-generation)
  * [Custom Module Context Aware Intro Generation](#custommodule-context-aware-intro-generation)
  * [Custom Module Without Context Static Intro Generation](#custommodulewithoutcontext‑static-intro-generation)
  * [Intro Links HTML Link Extraction](#introlinks‑html‑link‑extraction)
  * [Intro Text Global Context Introduction](#introtext‑global‑context‑introduction)
  * [Intro With Links Generation](#intro-with-links-generation)
  * [Basic Introduction Generation](#basic-introduction-generation)
  * [Custom Description Loop](#custom-description-loop)
  * [Standalone Custom Description](#standalone-custom-description)
  * [Content Description](#CONTENT_DESCRIPTION)
  * [Anchor Extraction Routine](#anchor-extraction-routine)
  * [Description Generation](#description-generation)
  * [HTML Link Extraction](#html-link-extraction)
* 🗂️ **Build & Deployment**
  * [Synchronous Part Doc Generation](#synchronous-part-doc-generation)
  * [Asynchronous Part Doc Generation](#asynchronous-part-doc-generation)
  * [Batch Doc Generation Sync](#batch-doc-generation-sync)
  * [Batch Doc Generation Async](#batch-doc-generation-async)
  * [Repository Mix Builder](#repository-mix-builder)
  * [Compress Function](#compress-function)
  * [Batch Compression](#batch-compression)
  * [Async Batch Compression](#async-batch-compression)
  * [Iterative Compression](#iterative-compression)
* 📊 **Logging & Monitoring**
  * [Logging Structures](#logging-structures)
  * [Runtime Logger](#runtime-logger)
  * [Progress Abstractions](#progress-abstractions)
  * [Project Metadata](#project-metadata)
  * [Runtime Dependencies](#runtime-dependencies)
  * [Build System Configuration](#build-system-configuration)

 

<a name="install-workflow-setup"></a>

**Installation workflow overview**

1. **PowerShell (Windows)**
   - Open a PowerShell terminal with elevated privileges.
   - Execute a one‑liner that downloads and runs the remote installer script:
     ```
     irm <raw‑url‑to‑powershell‑installer> | iex
     ```
   - The script will perform all required setup steps for the Windows environment.

2. **Shell (Linux/macOS)**
   - Open a terminal.
   - Run the following one‑liner to fetch and execute the installer for Unix‑like systems:
     ```
     curl -sSL <raw‑url‑to‑shell‑installer> | bash
     ```
   - The installer will handle dependency resolution and configuration automatically.

3. **GitHub Actions integration**
   - In the repository’s **Settings → Secrets and variables → Actions**, create a new secret named `GROCK_API_KEY`.
   - Populate this secret with the API key obtained from the Grock documentation.
   - The workflow file should reference this secret (e.g., `${{ secrets.GROCK_API_KEY }}`) so that the installer can authenticate with Grock services during the CI run.

4. **Verification**
   - After the script finishes, confirm that the application binaries are available and that any required services are running.
   - In CI, ensure the workflow passes the steps that rely on the `GROCK_API_KEY` secret.

**Key points**
- Use the one‑liner commands to avoid manual download steps.
- The secret must be set at the repository level; it is not exposed in logs.
- The installer scripts are designed to be idempotent, so re‑running them will not cause duplicate installations. 
<a name="runfile-execution"></a>  
## Run‑file execution flow  

`gen_doc` orchestrates the full documentation pipeline. It instantiates a **synchronous** (`GPTModel`) and an **asynchronous** (`AsyncGPTModel`) LLM client using the global `API_KEY`. These models are injected into a `Manager` together with:  

* `project_path` – root of the source tree.  
* `config` – a `Config` instance (see *Configuration object construction*).  
* `ConsoleGtiHubProgress` – CLI progress visualiser.  

The manager then performs the ordered steps:  

1. `generate_code_file()` – parses the project and creates an internal code representation.  
2. `generete_doc_parts(max_symbols=5000)` – produces raw documentation fragments, capped at 5 k symbols each.  
3. `factory_generate_doc(DocFactory(*custom_modules))` – runs user‑supplied modules (e.g., custom extractors).  
4. `order_doc()` – re‑orders fragments according to logical sections.  
5. `factory_generate_doc(DocFactory(IntroLinks()))` – adds the autogenerated introductory link block.  
6. `clear_cache()` – removes temporary artefacts.  

Finally `read_file_by_file_key("output_doc")` returns the assembled markdown document. 
<a name="manager-orchestration-pipeline"></a>
## Manager – Orchestration of Documentation Pipeline  

* **Responsibility** – Coordinates the end‑to‑end generation of documentation: builds the code‑mix cache, splits large sources, invokes the factory‑based module chain, and orders the final output.  

* **Interaction** –  
  * Accepts a project root, a `Config` object, optional synchronous (`Model`) and asynchronous (`AsyncModel`) language models, and a UI progress handler (`BaseProgress`).  
  * Utilises `BaseLogger` (file‑backed via `FileLoggerTemplate`) for all informational, warning and error logs.  
  * Calls external preprocessors (`split_data`, `gen_doc_parts`, `compress_to_one`), post‑processors (`get_introdaction`, `get_all_html_links`, …) and the injected `DocFactory` to produce the final markdown.  

* **Technical Details** –  
  * Constants `CACHE_FOLDER_NAME` and `FILE_NAMES` define persistent cache locations (`code_mix.txt`, `global_info.md`, `report.txt`, `output_doc.md`).  
  * `__init__` creates the cache folder, configures the logger, and stores references to models and progress UI.  
  * Core methods:  
    - `generate_code_file` → builds a `CodeMix` instance, writes the mixed source to cache, updates progress.  
    - `generete_doc_parts` → streams the cached mix through `gen_doc_parts`, writes the partial markdown, logs progress.  
    - `factory_generate_doc` → loads current output and code mix, assembles an `info` dict, logs the module list, invokes `doc_factory.generate_doc`, prepends the new fragment to the existing document.  
    - `order_doc` → splits the markdown by anchor markers, asks the synchronous model to reorder sections via `get_order`, and rewrites the file.  
    - `clear_cache` → optionally removes the log file based on `config.pcs.save_logs`.  

* **Data Flow** –  
  1. **Input**: project directory path, `Config`, optional models, UI progress object.  
  2. **Processing**:  
     - `CodeMix.build_repo_content` → writes raw source to `code_mix.txt`.  
     - `gen_doc_parts` → consumes the mix, returns a partial markdown string.  
     - `DocFactory.generate_doc` → receives `info` (`language`, `full_data`, `code_mix`), calls each module’s `generate`, aggregates results, updates progress.  
     - `split_text_by_anchors` / `get_order` → reorders sections.  
  3. **Side‑effects**: file system writes (cache files, final `output_doc.md`), logger entries, progress‑bar updates.  
  4. **Output**: a fully assembled `output_doc.md` containing ordered documentation ready for consumption.

** 
<a name="semantic-ordering-workflow"></a>  
## Semantic Ordering Workflow (sorting.py)

**Responsibility** – Request an LLM to reorder section titles semantically and concatenate the associated chunks in that order.  

**Interactions** – Receives the anchor‑chunk map, sends a prompt to `Model.get_answer_without_history`, then assembles `order_output`.  

**Technical Details** – Constructs a user‑role prompt containing the list of titles, parses the comma‑separated LLM response, logs each step, and iterates over the ordered titles to build the final markdown string.  

**Data Flow** – Input: `Model` instance, `chanks` dict. Output: ordered markdown string. Side‑effects: extensive logging. 
<a name="config-reader-responsibility"></a>
## Config‑Reader Responsibility
`read_config` loads a user‑supplied YAML string, transforms it into a strongly‑typed `Config` object and a list of custom documentation modules. It centralises all project‑wide settings (language, name, ignored files, additional info) and prepares module descriptors for the documentation engine. 
<a name="config-reader-interaction"></a>
## Interaction with Factory Modules
The function imports `CustomModule` and `CustomModuleWithOutContext` from `autodocgenerator.factory.modules.general_modules`.  
* When a description line starts with “%” it is wrapped in `CustomModuleWithOutContext` (context‑free).  
* Otherwise the line is turned into a regular `CustomModule`.  
These objects are later consumed by the rendering pipeline to inject user‑defined sections into the generated markdown. 
<a name="config-reader-technical-details"></a>
## Technical Details and Logic Flow
1. **YAML parsing** – `yaml.safe_load` converts the raw string to a Python dict.  
2. **Base `Config` creation** – a fresh `Config` instance is instantiated.  
3. **Core fields extraction** – `ignore_files`, `language`, `project_name`, and `project_additional_info` are read with sensible defaults.  
4. **Project settings handling** – a `ProjectConfigSettings` object (`pcs`) loads the `project_settings` mapping via `pcs.load_settings`.  
5. **Fluent configuration** – `config.set_language(...).set_project_name(...).set_pcs(pcs)` chains setters for readability.  
6. **Iterative population** – loops add ignore patterns and additional info via `config.add_ignore_file` and `config.add_project_additional_info`.  
7. **Custom description conversion** – each entry in `custom_descriptions` is examined; the leading character decides which module class to instantiate. 
<a name="config-reader-data-flow"></a>
## Input, Output, and Side Effects
| Aspect | Description |
|--------|-------------|
| **Input** | `file_data: str` – raw YAML content supplied by `autodocconfig.yml`. |
| **Output** | `Tuple[Config, List[CustomModule]]` – a ready‑to‑use configuration object and a collection of module descriptors. |
| **Side effects** | None; the function is pure aside from importing modules. It assumes the YAML schema contains the keys used above; missing optional keys fall back to defaults. |
| **Assumptions** | The YAML is well‑formed, custom description strings are non‑empty, and the imported module classes conform to the expected constructor signatures. |
| **Error handling** | Propagation of `yaml.YAMLError` or any constructor exception to the caller; the runner catches and logs them via the global logger. |

Together, `read_config` supplies the documentation engine with a complete, validated configuration snapshot and the custom module list required for the subsequent generation steps. 
<a name="configuration-object-construction"></a>  
## Configuration object construction  

`Config` aggregates global settings:  

* **ignore_files** – glob patterns excluded from scanning.  
* **language** – default `"en"`.  
* **project_name** & **project_additional_info** – descriptive metadata passed to `ProjectSettings`.  
* **pcs** – a `ProjectConfigSettings` container (log flags).  

Convenient setters (`set_language`, `set_project_name`, `add_ignore_file`, …) enable fluent building.  
`get_project_settings()` converts the stored metadata into a `ProjectSettings` instance used later by the `Manager`. 
<a name="data-flow-and-side‑effects"></a>  
## Data flow and side‑effects  

* **Input** – `project_path` (string), a parsed `Config` object, and a list of instantiated custom module objects.  
* **Processing** – manager writes intermediate code files to the hidden `.auto_doc_cache` directory, updates the console progress bar, and may create temporary log files if `ProjectConfigSettings.save_logs` is true.  
* **Output** – a single string containing the complete documentation (`output_doc`).  
* **Assumptions** – a valid `API_KEY` is available, custom modules implement the `BaseModule` interface expected by `DocFactory`, and the project directory is readable.  

These steps provide the validated configuration snapshot and the custom module list required for the downstream generation engine. 
<a name="parentmodel-shared-configuration"></a>  
## ParentModel – Shared Model Configuration  

`ParentModel` centralises authentication, history handling, and model‑selection logic. It receives an `api_key`, a `History` instance, and a `use_random` flag. The constructor shuffles the global `MODELS_NAME` list (when randomised) and stores the ordered copy in `self.regen_models_name`. Index tracking (`self.current_model_index`) enables round‑robin fallback when a model fails.

--- 
<a name="history-conversation-state"></a>  
## History – Conversation State Management  

`History` builds the message array sent to the LLM. It auto‑injects the system prompt (`BASE_SYSTEM_TEXT`) and provides `add_to_history(role, content)` to append user or assistant entries. The `self.history` list is consumed directly by the model classes.

--- 
<a name="gptmodel-synchronous-generation"></a>  
## GPTModel – Synchronous Answer Generation  

Inherits from `Model` (which extends `ParentModel`).  
* **Responsibility** – Wraps the Groq synchronous client (`Groq`) to produce a completion.  
* **Interaction** – Uses `self.client.chat.completions.create(messages, model)`; falls back through `self.regen_models_name` on exception, logging each attempt via `BaseLogger`.  
* **Data Flow** –  
  1. Chooses `messages` from `self.history.history` or a raw `prompt`.  
  2. Calls the Groq API, extracts `choices[0].message.content`.  
  3. Logs generation steps and returns the answer.

--- 
<a name="asyncgptmodel-asynchronous-generation"></a>  
## AsyncGPTModel – Asynchronous Answer Generation  

Mirrors `GPTModel` but operates with `AsyncGroq`.  
* **Responsibility** – Provides `async generate_answer` for non‑blocking calls.  
* **Interaction** – Awaits `self.client.chat.completions.create`. On failure, logs a warning and advances `self.current_model_index`.  
* **Data Flow** – Same as the synchronous variant, but returns a coroutine result and logs at level 2 for the final answer.

Both model classes rely on the shared fallback mechanism defined in `ParentModel`, ensuring resilience when a specific model endpoint is unavailable. 
<a name="docfactory-orchestrating-documentation-generation"></a>  
## DocFactory – Orchestrating Documentation Generation  

* **Responsibility** – Accepts an ordered list of `BaseModule` instances and sequentially invokes each to produce a composite documentation string.  
* **Interaction** –  
  * Receives a `Model` (or `AsyncModel`) and a `BaseProgress` UI object from the caller.  
  * Calls `module.generate(info, model)` for every injected module.  
  * Emits `InfoLog` entries via the shared `BaseLogger`, forwarding the module name and its raw output (level 2).  
* **Technical Details** –  
  * Stores modules in `self.modules: list[BaseModule]`.  
  * Initializes a simple logger (`BaseLogger()`).  
  * Uses `progress.create_new_subtask` to allocate a sub‑task sized to the module count, `progress.update_task` after each module, and `progress.remove_subtask` on completion.  
* **Data Flow** –  
  1. Input: `info` dict, `model` instance, `progress` UI.  
  2. For each module: `module.generate` returns a string → concatenated to `output`.  
  3. Side‑effects: logging, progress bar updates.  
  4. Output: the final assembled documentation string. 
<a name="custommodule-context-aware-intro-generation"></a>  
## CustomModule – Context‑Aware Intro Generation  

* **Responsibility** – Generates a custom introductory paragraph that incorporates a user‑provided description and a code‑snippet excerpt.  
* **Interaction** – Calls `split_data` to truncate `info["code_mix"]` to ≤ 5 000 symbols, then forwards the split text, the model, the description, and the target language to `generete_custom_discription`.  
* **Technical Details** –  
  * Inherits from `BaseModule`.  
  * Holds `self.discription` (typo retained from original).  
  * `generate` returns the processed string from the post‑processor.  

* **Data Flow** –  
  1. Input: `info` dict (keys `code_mix`, `language`), `model`.  
  2. Processing: `split_data → generete_custom_discription`.  
  3. Output: formatted intro paragraph. 
<a name="custommodulewithoutcontext‑static-intro-generation"></a>  
## CustomModuleWithOutContext – Static Intro Generation  

* **Responsibility** – Produces a description‑only intro, omitting any code context.  
* **Interaction** – Directly invokes `generete_custom_discription_without` with the model, stored description, and language.  
* **Data Flow** – Input: `info["language"]`, `model`; Output: static intro string; No side‑effects beyond the returned text. 
<a name="introlinks‑html‑link‑extraction"></a>  
## IntroLinks – HTML Link Extraction for Documentation  

* **Responsibility** – Extracts all HTML links from `info["full_data"]` and synthesizes a brief introductory block about those links.  
* **Interaction** – Uses `get_all_html_links` → `get_links_intro`, passing the model and language. 
<a name="introtext‑global‑context‑introduction"></a>  
## IntroText – Global Context Introduction  

* **Responsibility** – Generates a high‑level introduction based on `info["global_data"]`.  
* **Interaction** – Calls `get_introdaction` with the model and language, returning the result. 
<a name="intro-with-links-generation"></a>Intro‑With‑Links Generation**  
`get_links_intro` receives the anchor list, a `Model` implementation, and an optional language code. It composes a three‑message system‑user prompt (language hint, `BASE_INTRODACTION_CREATE_LINKS` template, and the raw link list) and calls `model.get_answer_without_history`.  

*Inputs*: `links` (list of anchors), `model` (concrete `Model`/`GPTModel`), `language`.  
*Outputs*: String containing a generated introductory paragraph that references the provided links.  
*Side‑effects*: Logs start/completion messages and the raw LLM response.  

---

** 
<a name="basic-introduction-generation"></a>Basic Introduction Generation**  
`get_introdaction` (typo intentional) builds a similar prompt using `BASE_INTRO_CREATE` and the full documentation (`global_data`). It returns the LLM‑generated introductory block.  

*Inputs*: `global_data` (full docs), `model`, `language`.  
*Outputs*: Introduction string.  

---

** 
<a name="custom-description-loop"></a>Custom Description Loop**  
`generete_custom_discription` iterates over a pre‑split collection of documentation fragments (`splited_data`). For each fragment it sends a detailed system prompt (technical analyst role, context snippet, `BASE_CUSTOM_DISCRIPTIONS`) together with the user‑requested `custom_description`. The loop breaks when the LLM returns a substantive answer (i.e., does not contain “!noinfo” or “No information found”). The final `result` is returned.  

*Inputs*: `splited_data` (iterable of strings), `model`, `custom_description`, `language`.  
*Outputs*: Custom description text for the first fragment that yields valid content.  

---

** 
<a name="standalone-custom-description"></a>Standalone Custom Description**  
`generete_custom_discription_without` builds a single‑shot prompt that forces the LLM to prepend a strict ` 
<a name="CONTENT_DESCRIPTION"></a>` tag and obey naming constraints (no filenames, extensions, generic terms, or URLs). The result is returned directly.  

*Inputs*: `model`, `custom_description`, `language`.  
*Outputs*: Tagged description string.  

---

**Interaction Summary**  
All functions rely on the shared `BaseLogger` for traceability and on the abstract `Model` interface (concretely `GPTModel`) to invoke the LLM. They do **not** perform I/O beyond logging; the calling post‑processor aggregates their outputs into the final documentation file. 
<a name="anchor-extraction-routine"></a>  
## Anchor Extraction Routine (sorting.py)

**Responsibility** – Detect HTML‑style anchors at the start of each markdown chunk and build a mapping `anchor → chunk`.  

**Interactions** – Consumes raw README text, feeds the resulting dictionary to `get_order`. Relies on `BaseLogger` for diagnostic output.  

**Technical Details** – `extract_links_from_start` uses a regex `^<a name=["']?(.*?)["']?</a>` to capture names longer than five characters, prefixing them with `#`. `split_text_by_anchors` splits the document on a look‑ahead pattern, trims empties, validates a one‑to‑one link‑chunk relationship, and returns `{anchor: chunk}` or `None`.  

**Data Flow** – Input: `text` (str). Output: `dict[str, str]` where keys are `#anchor`. Side‑effects: logging of chunk names and content; early exit if counts mismatch. 
<a name="description-generation"></a>  
## `generate_discribtions_for_code` – LLM‑driven documentation builder  

**Responsibility**  
Feeds each source file to the model with a strict instruction prompt, collects the model’s descriptive answer, and reports progress.  

**Data flow**  
- **Input:** List of code strings, `model`, `project_settings`, `progress_bar`.  
- **Output:** List of description strings (same order as input).  
- **Side‑effects:** Progress bar sub‑task updates. 
<a name="html-link-extraction"></a>HTML‑Link Extraction**  
The function `get_all_html_links` scans a markdown string for anchor tags of the form `<a name="…"></a>`. It logs the start/end of the operation, builds a list of fragment identifiers prefixed with “#”, and returns that list.  

*Inputs*: `data` – full documentation text.  
*Outputs*: `list[str]` – collected anchors (e.g., `["#section‑overview"]`).  
*Side‑effects*: Writes two `InfoLog` entries via `BaseLogger`.  

---

** 
<a name="introlinks‑html‑link‑extraction"></a>  
## IntroLinks – HTML Link Extraction for Documentation  

* **Responsibility** – Extracts all HTML links from `info["full_data"]` and synthesizes a brief introductory block about those links.  
* **Interaction** – Uses `get_all_html_links` → `get_links_intro`, passing the model and language. 
<a name="autodocfile-options"></a>
Define the top‑level keys in the file as follows:

- **project_name** – a string that identifies the project.
- **language** – language code (default “en” if omitted).
- **project_settings** – a block containing:
  - **save_logs** – boolean, true to keep generation logs.
  - **log_level** – numeric level controlling output detail.
- **project_additional_info** – map of arbitrary key/value pairs for extra context (e.g., a global idea description).
- **ignore_files** – optional list of filename patterns that should be skipped.
- **custom_descriptions** – list of strings.  
  - If a string starts with “%”, the leading character is removed and the remainder is processed without additional context.  
  - Otherwise the string is taken as‑is and processed with full context.

Each entry should be written in standard YAML syntax, preserving indentation for nested blocks. 
<a name="projectsettings-prompt"></a>  
## `ProjectSettings.prompt` – dynamic system context  

**Responsibility**  
Constructs a multi‑line system prompt by concatenating a base template (`BASE_SETTINGS_PROMPT`) with the project name and any key‑value pairs added via `add_info`.  

**Technical details**  
- `info` is a mutable dict; `add_info` inserts or overwrites entries.  
- Property accessor lazily builds the prompt each call, ensuring the latest `info` content is reflected.  

**Interactions**  
- Consumed by every compression or description function to provide project‑specific background to the LLM. 
<a name="data-splitting-algorithm"></a>  
## `split_data` – chunking source text to fit token limits  

**Responsibility**  
Breaks a monolithic code string into a list of substrings whose lengths stay below `max_symbols` while preserving line boundaries.  

**Interactions**  
Uses `BaseLogger` for progress messages; no external state is read or modified.  

**Technical details**  
1. Initial split on newline (`"\n"`).  
2. Repeatedly scans `splited_by_files`; any element exceeding `1.5 × max_symbols` is bisected at `max_symbols/2` and re‑inserted, forcing convergence.  
3. A second pass packs the trimmed fragments into `split_objects`, starting a new part whenever the accumulated length would exceed `1.25 × max_symbols`.  

**Data flow**  
- **Input:** `data: str`, `max_symbols: int`.  
- **Output:** `list[str]` – ordered chunks ready for LLM consumption.  
- **Side‑effects:** One `InfoLog` entry before and after splitting. 
<a name="synchronous-part-doc-generation"></a>  
## `write_docs_by_parts` – generate documentation for a single chunk (sync)  

**Responsibility**  
Builds a system‑user prompt, sends it to a synchronous `Model`, and returns the cleaned LLM answer.  

**Interactions**  
Relies on `BASE_PART_COMPLITE_TEXT` (static instruction), optional `prev_info` (context from the previous chunk), and `BaseLogger`.  

**Technical details**  
- Prompt composition: two mandatory system messages (language + part ID, base instruction) + optional previous‑part context + user message containing the code chunk.  
- Calls `model.get_answer_without_history`.  
- Strips surrounding Markdown fences (```), logs answer length and full content (debug level 2).  

**Data flow**  
- **Input:** `part_id: int`, `part: str`, `model: Model`, `prev_info: str | None`, `language: str`.  
- **Output:** Cleaned documentation string for the chunk.  
- **Side‑effects:** Logging; no mutation of arguments. 
<a name="asynchronous-part-doc-generation"></a>  
## `async_write_docs_by_parts` – concurrent chunk documentation (async)  

**Responsibility**  
Same prompt logic as the sync variant but executed within an `asyncio.Semaphore` to limit parallel LLM calls.  

**Interactions**  
Accepts an `AsyncModel`, optional `update_progress` callback, and shares the same logger.  

**Technical details**  
- `async with semaphore` protects the call to `async_model.get_answer_without_history`.  
- After obtaining the answer, optionally invokes `update_progress` (used by the surrounding progress bar).  
- Performs identical back‑tick stripping and logging.  

**Data flow**  
- **Input:** `part: str`, `async_model: AsyncModel`, `global_info: str`, `semaphore`, `prev_info: str | None`, `language: str`, `update_progress: Callable | None`.  
- **Output:** Cleaned documentation string (coroutine result).  
- **Side‑effects:** Logging; may update external progress bar via callback. 
<a name="batch-doc-generation-sync"></a>  
## `gen_doc_parts` – orchestrated synchronous documentation pipeline  

**Responsibility**  
Splits the full code, sequentially processes each part with `write_docs_by_parts`, aggregates results, and maintains a sub‑task on a `BaseProgress` bar.  

**Interactions**  
Calls `split_data`, creates/updates/removes a sub‑task on `progress_bar`, and logs high‑level milestones.  

**Technical details**  
- After each part, retains the last 3000 characters of the generated text as `prev_info` to provide context for the next iteration.  
- Concatenates all part outputs separated by blank lines.  

**Data flow**  
- **Input:** `full_code_mix: str`, `max_symbols: int`, `model: Model`, `language: str`, `progress_bar: BaseProgress`.  
- **Output:** Single string containing the complete documentation.  
- **Side‑effects:** Progress‑bar sub‑task lifecycle, extensive logging. 
<a name="batch-doc-generation-async"></a>  
## `async_gen_doc_parts` – orchestrated asynchronous documentation pipeline  

**Responsibility**  
Parallel version of `gen_doc_parts`; dispatches `async_write_docs_by_parts` for every split chunk, respecting a concurrency limit of four.  

**Interactions**  
Creates a semaphore, builds a list of coroutines, gathers them, and updates the same `BaseProgress` sub‑task via a lambda passed to each async worker.  

**Technical details**  
- Uses `asyncio.gather` to await all part‑level tasks.  
- Result aggregation mirrors the sync version (blank‑line separation).  

**Data flow**  
- **Input:** `full_code_mix: str`, `global_info: str`, `max_symbols: int`, `model: AsyncModel`, `language: str`, `progress_bar: BaseProgress`.  
- **Output:** Full documentation string (awaited coroutine).  
- **Side‑effects:** Progress‑bar sub‑task updates, logging, semaphore enforcement. 
<a name="repository-mix-builder"></a>  
## Repository Mix Builder (code_mix.py)

**Responsibility** – Walk a repository, emit a hierarchical file‑tree, and concatenate file contents into a single “repo mix” artifact while respecting ignore patterns.  

**Interactions** – Utilises `Path.rglob` for traversal, `should_ignore` for pattern checks, and `BaseLogger` for progress messages.  

**Technical Details** – `should_ignore` matches a path against user‑supplied glob patterns across the full relative path, basename, and individual parts. `build_repo_content` writes a tree view, inserts a delimiter, then writes each non‑ignored file wrapped in `<file path="...">` tags, handling read errors gracefully.  

**Data Flow** – Input: `root_dir` (Path), `ignore_patterns` (list). Output: `repomix-output.txt` (text file). Side‑effects: file creation, console logs, error annotations inside the output file. 
<a name="compress-function"></a>  
## `compress` – single‑pass text reduction  

**Responsibility**  
Accepts raw source `data`, builds a three‑message prompt (system settings, compression template, user payload) and returns the model’s answer, which is the compressed representation of the input.  

**Interactions**  
- Uses `ProjectSettings.prompt` for the contextual system message.  
- Calls `get_BASE_COMPRESS_TEXT` to obtain a size‑aware compression instruction.  
- Delegates the LLM request to any `Model` implementation (`GPTModel`, custom adapters).  

**Technical notes**  
- No async I/O; the model call is synchronous via `model.get_answer_without_history`.  
- Returns a plain string; callers are responsible for further aggregation. 
<a name="batch-compression"></a>  
## `compress_and_compare` – synchronous batch aggregator  

**Responsibility**  
Splits a list of file contents into groups of `compress_power` items, compresses each element with `compress`, concatenates the results per group, and tracks progress.  

**Data flow**  
- **Input:** `data` (list of strings), `model`, `project_settings`, optional `compress_power`, `progress_bar`.  
- **Output:** List of aggregated compressed chunks, length ≈ ⌈len(data)/compress_power⌉.  
- **Side‑effects:** Updates `progress_bar` (sub‑task creation, per‑item updates, removal).  

**Logic**  
1. Pre‑allocate a result list sized to the number of groups.  
2. For each element, compute its group index `i // compress_power`, append the compressed string plus newline.  
3. Progress bar reflects each processed element. 
<a name="async-batch-compression"></a>  
## `async_compress_and_compare` – parallel batch compressor  

**Responsibility**  
Performs the same grouping as `compress_and_compare` but launches up to four concurrent LLM calls using `asyncio.Semaphore`.  

**Key steps**  
- Creates a semaphore (limit = 4) and a task list.  
- Each element is wrapped in `async_compress`, which builds the identical prompt and awaits `model.get_answer_without_history`.  
- After `asyncio.gather`, results are re‑chunked according to `compress_power` and concatenated with newlines.  

**Data flow**  
- **Input/Output:** Same as the synchronous version, but returns a coroutine result.  
- **Side‑effects:** Progress bar updates inside `async_compress`; sub‑task lifecycle mirrors the sync variant. 
<a name="iterative-compression"></a>  
## `compress_to_one` – iterative reduction to a single payload  

**Responsibility**  
Repeatedly compresses the dataset until only one aggregated chunk remains, optionally using the async pipeline.  

**Algorithm**  
- While `len(data) > 1`, choose an effective `compress_power` (fallback = 2 for small lists).  
- Call either `async_compress_and_compare` (via `asyncio.run`) or `compress_and_compare`.  
- Increment iteration counter; final output is `data[0]`. 
<a name="logging-structures"></a>
## `BaseLog` hierarchy – structured log messages  

**Responsibility**  
Defines lightweight log objects (`BaseLog`, `ErrorLog`, `WarningLog`, `InfoLog`) that prepend a timestamp and level tag to a user‑supplied message.  

**Interactions**  
Instances are passed to a `BaseLoggerTemplate` via its `log` method; the template decides whether to emit the message based on its configured `log_level`.  

**Technical details**  
- `BaseLog` stores `message` and numeric `level`; its `format` returns the raw text.  
- `_log_prefix` property builds `"[YYYY‑MM‑DD HH:MM:SS]"` using `datetime.fromtimestamp(time.time())`.  
- Sub‑classes override `format` to insert `[ERROR]`, `[WARNING]`, or `[INFO]` after the prefix.  

**Data flow**  
- **Input:** `message: str`, optional `level: int`.  
- **Output:** Formatted string via `format()`.  
- **Side‑effects:** None (pure data object). 
<a name="runtime-logger"></a>
## `BaseLogger` singleton – runtime logging façade  

**Responsibility**  
Provides a globally accessible logger that delegates to a concrete `BaseLoggerTemplate` (console, file, etc.).  

**Interactions**  
- `set_logger` injects a concrete template (`BaseLoggerTemplate`, `FileLoggerTemplate`, …).  
- Calls to `log` forward the `BaseLog` instance to the template’s `global_log`, which respects the template’s `log_level`.  

**Technical details**  
- Implements the classic singleton pattern in `__new__` to guarantee a single shared instance across the process.  
- `global_log` in `BaseLoggerTemplate` checks `log_level` (`-1` disables filtering).  

**Data flow**  
- **Input:** `BaseLog` object.  
- **Output:** Printed to stdout or appended to a file, depending on the active template.  
- **Side‑effects:** I/O (stdout or file write). 
<a name="progress-abstractions"></a>
## `BaseProgress` abstraction and concrete implementations  

**Responsibility**  
Offers a minimal API (`create_new_subtask`, `update_task`, `remove_subtask`) for tracking hierarchical progress in different environments.  

**Interactions**  
- `LibProgress` wraps Rich’s `Progress` object, exposing Rich‑based visual feedback.  
- `ConsoleGtiHubProgress` uses simple `print` statements via `ConsoleTask` for environments without Rich.  

**Technical details**  
- `LibProgress` creates a base task (`General progress`) and optional sub‑tasks; `update_task` advances either the sub‑task or base task.  
- `ConsoleTask` maintains a counter and prints a percentage on each `progress` call.  
- `ConsoleGtiHubProgress` delegates to a `ConsoleTask` for sub‑tasks, falling back to a `ConsoleTask` representing the overall progress.  

**Data flow**  
- **Input:** Sub‑task name and total length.  
- **Output:** Visual progress updates on the console or Rich UI.  
- **Side‑effects:** stdout writes (or Rich UI updates).  

These components together furnish a lightweight, interchangeable logging and progress‑tracking subsystem used throughout the autodocgenerator package. 
<a name="project-metadata"></a>
## `pyproject.toml` – package identity & version constraints  

**Responsibility**  
Encapsulates the canonical package descriptor for **autodocgenerator**: name, semantic version, human‑readable description, author contact, license, and the supported Python range.  

**Interactions**  
- Read by *Poetry* (or any PEP 517‑compatible builder) to resolve the project’s identity during `poetry install`, `poetry build`, and wheel creation.  
- Exposed to downstream tools (e.g., `pip`, `build`) via the generated `dist/*.whl` metadata.  

**Technical details**  
- `name = "autodocgenerator"` and `version = "0.8.9.9"` follow PEP 621 naming rules.  
- `description` and `readme` feed the **Core Metadata** fields of the resulting distribution.  
- `authors` is a list of `{"name": "...", "email": "..."}` objects, converted to the `Author` field in the wheel.  
- `license = {text = "MIT"}` supplies an SPDX‑compatible license string.  

**Data flow**  
- **Input:** Static TOML literals edited by maintainers.  
- **Output:** Serialized metadata consumed at build time; no runtime side‑effects. 
<a name="runtime-dependencies"></a>
## Dependency enumeration – third‑party runtime requirements  

**Responsibility**  
Lists exact version pins required for the library to operate, ensuring reproducible environments across Python 3.11–3.12.  

**Interactions**  
- Resolved by Poetry’s dependency resolver; each entry becomes a `Requires-Dist` clause in the wheel metadata.  
- At installation, `pip` (via the wheel) pulls the same versions, guaranteeing API stability.  

**Technical details**  
- All entries follow the `package==major.minor.patch` syntax, e.g., `rich==14.2.0`.  
- The list covers HTTP clients (`httpx`), authentication (`google-auth`), AI SDKs (`openai`, `groq`), data handling (`pyyaml`, `msgmsg`), and utilities (`rich_progress`, `tqdm`).  
- No optional groups are defined; every line is a mandatory runtime requirement.  

**Data flow**  
- **Input:** Version‑locked strings.  
- **Output:** Dependency graph constructed by the resolver; installed files appear in `site‑packages`. 
<a name="build-system-configuration"></a>
## Build‑system stanza – PEP 517 backend specification  

**Responsibility**  
Declares the toolchain needed to produce a distributable artifact from the source.  

**Interactions**  
- `requires = ["poetry-core>=2.0.0"]` tells the build frontend to fetch *poetry‑core* before invoking the backend.  
- `build-backend = "poetry.core.masonry.api"` points to the entry‑point that implements `build_wheel`, `build_sdist`, etc.  

**Technical details**  
- The stanza is minimal; no custom build steps are injected, relying on Poetry’s default isolation and caching mechanisms.  

**Data flow**  
- **Input:** The declared backend package.  
- **Output:** A built wheel or source distribution emitted to `dist/`; no side‑effects beyond temporary build directories. 
