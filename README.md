**Project Title:** Auto Doc Generator

**Project Goal:** 
The Auto Doc Generator is a software tool designed to automate the process of generating documentation for a project by scanning a repository, processing the source code, and stitching the results into a single Markdown document. The primary goal of this project is to provide a comprehensive and accurate documentation of the codebase, making it easier for developers to understand and maintain the project.

**Core Logic & Principles:** 
The Auto Doc Generator operates on a layered architecture, comprising several key components, including the CLI/orchestrator, config, factory, modules, engine, LLM wrapper, pre-processor, post-processor, and UI. The core logic involves the following steps:
- The pre-processor walks the repository, builds a plain-text dump, splits it into size-bounded chunks, and optionally compresses the code.
- The LLM wrapper invokes a Groq-based Language Model (LLM) for each chunk, generating a Markdown response.
- The post-processor splits the final Markdown by anchors, reorders sections, and generates link/introduction blocks.
- The factory executes an ordered list of modules on a shared Doc object, allowing for custom documentation modules and intro sections.
- The engine orchestrates the entire process, including file discovery, preprocessing, LLM calls, caching, ordering, and final save.

The project utilizes several key technologies and algorithms, including:
- Groq-based LLMs for generating Markdown responses
- Pydantic models for describing the document tree
- Rich and plain console implementations for progress reporting
- A caching mechanism for storing intermediate dumps and LLM responses

**Key Features:** 
* Automated documentation generation for a project
* Support for custom documentation modules and intro sections
* Integration with Groq-based LLMs for generating Markdown responses
* Caching mechanism for storing intermediate dumps and LLM responses
* Progress reporting using Rich and plain console implementations
* Optional compression of code and global info generation
* Reordering of sections and generation of link/introduction blocks

**Dependencies:** 
* Groq API keys for LLM calls
* Pydantic for describing the document tree
* Rich and plain console libraries for progress reporting
* Cache folder for storing intermediate dumps and LLM responses
* Config file (autodocconfig.yml) for parsing project settings and custom module lists
* LLM wrapper for interacting with Groq-based LLMs
* Pre-processor and post-processor libraries for handling code and Markdown processing
* Factory and engine components for orchestrating the documentation generation process
## Executive Navigation Tree
* 📂 Configuration 
  + [Config Reader Read Config](#config-reader-read-config)
  + [Config Models](#config-models)
  + [Data Contract](#data-contract)
  + [Doc Head Schema](#doc-head-schema)
* ⚙️ Documentation Generation
  + [Docfactory Generation Pipeline](#docfactory-generation-pipeline)
  + [Gen Doc Parts](#gen-doc-parts)
  + [Write Docs By Parts](#write-docs-by-parts)
  + [CLI Orchestrator Gen Doc](#cli-orchestrator-gen-doc)
  + [Autodoc Yaml Options](#autodoc-yaml-options)
* 📄 Modules and Responsibility
  + [Custom Module Responsibility](#custommodule-responsibility)
  + [Intro Modules Responsibility](#intro-modules-responsibility)
  + [Manager Responsibility](#manager-responsibility)
  + [Custom Intro Postprocessor](#custom-intro-postprocessor)
* 📊 Technical Logic and Flow
  + [CONTENT DESCRIPTION](#CONTENT_DESCRIPTION)
  + [Sorting Anchor Extraction and Reordering](#sorting-anchor-extraction-and-reordering)
  + [Repository Structure Builder Codemix](#repository-structure-builder-codemix)
  + [GPT Model Wrapper](#gptmodel-wrapper)
  + [Parent Model Abstract](#parentmodel-abstract)
* 🔄 Interactions and Compression
  + [Visible Interactions](#visible-interactions)
  + [Technical Logic Flow](#technical-logic-flow)
  + [Compressor Module](#compressor-module)
* 📁 Project Settings and Logging
  + [Project Settings Module](#projectsettings-module)
  + [Spliter Module](#spliter-module)
  + [Split Data](#split-data)
  + [Base Logger](#base-logger)
  + [Base Log Classes](#base-log-classes)
  + [File Logger Template](#file-logger-template)
* 📈 Progress and Installation
  + [Progress Base](#progress-base)
  + [Lib Progress](#lib-progress)
  + [Console Github Progress](#console-github-progress)
  + [Install Ps1](#install-ps1)
  + [Install Sh](#install-sh)
  + [Install Workflow Setup](#install-workflow-setup)
* 💼 Manager Class
  + [Manager Class Usage and Methods](#manager-class-usage-and-methods)
<a name="config-reader-read-config"></a>
## Config Reader – `read_config` Function  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_data` | `str` | YAML source content | Must be UTF‑8 string read from *autodocconfig.yml* |
| `Config` | `class` | Holds global settings (ignore patterns, language, project name, build config) | Instantiated inside function |
| `custom_modules` | `list[BaseModule]` | User‑supplied documentation pieces | Built from `custom_descriptions` list |
| `StructureSettings` | `class` | Controls doc assembly flags (intro links, order, global file, part size) | Populated from `structure_settings` dict |

**Responsibility** – Parses YAML, populates a `Config` object, creates module instances, and returns a `StructureSettings` instance.  

**Interactions** – Imports `CustomModule`, `CustomModuleWithOutContext` (factory modules) and `Config`/`ProjectBuildConfig` (core config). No external I/O besides the supplied string.  

**Logic Flow**  
1. `yaml.safe_load` → `data`.  
2. Initialise empty `Config`.  
3. Extract `ignore_files`, `language`, `project_name`, `project_additional_info`.  
4. Load build settings into `ProjectBuildConfig` via `pcs.load_settings`.  
5. Chain setters on `config` (`set_language`, `set_project_name`, `set_pcs`).  
6. Append additional ignore patterns and project info.  
7. Build `custom_modules` list:  
   - If a description starts with `'%'` → `CustomModuleWithOutContext(custom_desc[1:])`  
   - Else → `CustomModule(custom_desc)`.  
8. Load `structure_settings` into a new `StructureSettings` instance.  
9. Return `(config, custom_modules, structure_settings_object)`.

> **Assumption** – The YAML contains the keys used; missing keys yield defaults defined in class attributes.
<a name="config-models"></a>
## Config Models – `Config` & `ProjectBuildConfig` Classes  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `ProjectBuildConfig` | `class` | Stores build‑time flags (`save_logs`, `log_level`) | `load_settings` assigns arbitrary keys |
| `Config` | `class` | Central repository configuration | Holds ignore patterns, language, project name, additional info, and a `ProjectBuildConfig` instance (`pbc`) |

**Responsibility** – Provides mutable containers for global settings accessed throughout the pipeline.  

**Interactions** – `Config` is constructed in `read_config`; its setters (`set_language`, `set_project_name`, `set_pcs`) enable fluent chaining. `Manager` receives a `Config` instance to drive file discovery and logging.  

**Logic Flow** (within `Config`)  
- `__init__` populates default `ignore_files` and defaults for language, name, etc.  
- Fluent setters modify attributes and return `self`.  
- `add_project_additional_info` and `add_ignore_file` extend internal collections.  
- `get_project_settings` builds a `ProjectSettings` object (from `preprocessor.settings`) populated with additional info.  

These three fragments constitute the configuration loading and orchestration layer of **Auto Doc Generator**.
<a name="data-contract"></a>
## Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Input markdown for link extraction | Must contain `<a name=…></a>` anchors |
| `links` | `list[str]` | Output of `get_all_html_links` | Each entry prefixed with `#` |
| `model` | `Model` | LLM client used by generation functions | Provides `get_answer_without_history(prompt)` |
| `language` | `str` | Optional language code (default `"en"`) | Inserted into system messages |
| `global_data` | `str` | Raw global summary passed to `get_introdaction` | Direct user message |
| `splited_data` | `iterable[str]` | Chunks of markdown processed by `generete_custom_discription` | Loop stops on first valid answer |
| `custom_description` | `str` | Task description for custom generation | Used in both description functions |
| `result` | `str` | LLM response returned to caller | May be empty if no info is found |

These definitions enable developers to trace the post‑processor’s behavior, replace the LLM backend, or adjust prompt constants without altering the surrounding orchestration.
<a name="doc-head-schema"></a>
## `DocHeadSchema` – Document Assembly Model  

**Responsibility** – Maintain ordered document parts and render the final markdown.  

**Visible Interactions**  
- Stores `content_orders` (list of part names).  
- Stores `parts` mapping names → `DocContent`.  
- Provides `add_parts`, `get_full_doc`, and `__add__` for merging.  

**Technical Logic Flow**  
1. `add_parts(name, content)`: ensure unique name, append to order list, store in dict.  
2. `get_full_doc(split_el)`: iterate `content_orders`, concatenate each part’s `content` with separator.  
3. `__add__(other)`: merge another `DocHeadSchema` by delegating to `add_parts`.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `content_orders` | `list[str]` | Ordered identifiers of parts | Maintains output order |
| `parts` | `dict[str, DocContent]` | Mapping from identifier to content object | Each `DocContent` holds `content: str` |
| `name` (add_parts) | `str` | Desired part identifier | Auto‑renamed on conflict |
| `content` (add_parts) | `DocContent` | Payload for the part | |
| **Return (get_full_doc)** | `str` | Complete markdown document | Joined by `split_el` (default newline) |

---  

*All descriptions are strictly derived from the supplied code; no external assumptions are introduced.*
<a name="docfactory-generation-pipeline"></a>
## DocFactory Generation Pipeline  

**Responsibility** – Executes an ordered list of `BaseModule` objects, optionally splits each module’s raw markdown into anchor‑delimited sections, aggregates them into a single `DocHeadSchema`, and drives progress‑bar updates and structured logging.  

**Visible Interactions** – Calls `module.generate(info, model)`, uses `split_text_by_anchors` (post‑processor), writes to `DocHeadSchema.add_parts`, logs via `BaseLogger`, and reports status through `BaseProgress`.  

**Logic Flow**  
1. Instantiate empty `DocHeadSchema`.  
2. `progress.create_new_subtask("Generate parts", len(self.modules))`.  
3. For each `module` (`i`):  
   - `module_result = module.generate(info, model)`.  
   - If `with_splited`: `splited_result = split_text_by_anchors(module_result)` → iterate `el` keys, `doc_head.add_parts(el, DocContent(content=splited_result[el]))`.  
   - Else: build `task_name = f"{module.__class__.__name__}_{i}"` and add whole result.  
   - Log two `InfoLog` entries, then `progress.update_task()`.  
4. After loop: `progress.remove_subtask()` and return `doc_head`.  

> **Assumption** – `split_text_by_anchors` must return a dictionary `{anchor: markdown}`; otherwise the loop silently fails.

### Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `info` | `dict` | Input context (e.g., `code_mix`, `language`, `full_data`) | Required keys accessed by modules; missing keys yield `None`. |
| `model` | `Model` (or `AsyncModel`) | LLM interface passed unchanged to modules | Only its `generate`/`get_answer` methods are used inside modules. |
| `progress` | `BaseProgress` | Progress‑bar controller | Must implement `create_new_subtask`, `update_task`, `remove_subtask`. |
| `self.modules` | `list[BaseModule]` | Ordered processing units | Supplied at `DocFactory` construction. |
| `doc_head` | `DocHeadSchema` | Output container | Holds ordered parts via `add_parts`. |
| `module_result` | `str` | Raw markdown from a module | May contain `<a name=…>` anchors for splitting. |
| `splited_result` | `dict[str, str]` | Anchor‑wise fragments | Keys are anchor identifiers; values are fragment markdown. |
<a name="gen-doc-parts"></a>
## `gen_doc_parts` – Orchestrated Multi‑Part Generation  

**Responsibility** – Split the full code dump, generate documentation per chunk, concatenate results, and report progress.  

**Visible Interactions**  
- Calls `split_data`.  
- Iterates `write_docs_by_parts`.  
- Updates a `BaseProgress` sub‑task.  
- Logs via `BaseLogger`.  

**Technical Logic Flow**  
1. `splited_data = split_data(full_code_mix, max_symbols)`.  
2. Initialise progress sub‑task with total length of `splited_data`.  
3. For each chunk `el`:  
   a. `result = write_docs_by_parts(el, …, result, …)` (passes previous answer).  
   b. Append `result` and two newlines to `all_result`.  
   c. Keep trailing 3000 characters as context for the next iteration.  
   d. `progress_bar.update_task()`.  
4. Remove the progress sub‑task.  
5. Log final length and full documentation (level 2).  
6. Return `all_result`.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `full_code_mix` | `str` | Concatenated source dump | Input to splitter |
| `max_symbols` | `int` | Chunk size limit | Used by `split_data` |
| `model` | `Model` | LLM client | Shared across parts |
| `project_settings` | `ProjectSettings` | Global prompt source | Passed to each part |
| `language` | `str` | Output language for LLM | |
| `progress_bar` | `BaseProgress` | UI progress reporter | Must implement sub‑task methods |
| `global_info` | `str | None` | Optional extra context | Forwarded to parts |
| **Return** | `str` | Full assembled documentation | Combined markdown of all parts |

---
<a name="write-docs-by-parts"></a>
## `write_docs_by_parts` – Part‑Level Documentation Generation  

**Responsibility** – Build an LLM prompt for a single code chunk, invoke the model, and return cleaned markdown.  

**Visible Interactions**  
- Logs via `BaseLogger`.  
- Reads constant `BASE_PART_COMPLITE_TEXT`.  
- Uses `ProjectSettings.prompt`.  
- Calls `model.get_answer_without_history`.  

**Technical Logic Flow**  
1. Log start.  
2. Assemble `prompt` list with system messages for language, global project info, and `BASE_PART_COMPLITE_TEXT`.  
3. Optionally append system messages for `global_info` and prior part context (`prev_info`).  
4. Append the user message containing `part`.  
5. Invoke the LLM: `answer = model.get_answer_without_history(prompt)`.  
6. Strip surrounding markdown fences ````` ```.  
7. Log result length and raw answer (level 2).  
8. Return the cleaned answer.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | Code fragment to document | Passed to user role |
| `model` | `Model` | LLM client | Must implement `get_answer_without_history` |
| `project_settings` | `ProjectSettings` | Supplies global prompt | Accessed via `.prompt` |
| `prev_info` | `str | None` | Context from previous part | Inserted if provided |
| `language` | `str` | Language for LLM instruction | Defaults to `"en"` |
| `global_info` | `str | None` | Optional extra project relations | Inserted if provided |
| **Return** | `str` | Cleaned documentation snippet | Markdown without surrounding fences |

---
<a name="cli-orchestrator-gen-doc"></a>
## CLI Orchestrator – `gen_doc` Function  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_path` | `str` | Root of source repository | Passed to `Manager` |
| `config` | `Config` | Global configuration | Produced by `read_config` |
| `custom_modules` | `list[BaseModule]` | Optional user modules | Injected into `DocFactory` |
| `structure_settings` | `StructureSettings` | Feature toggles | Drives conditional steps |
| Return | `str` | Full Markdown documentation | Obtained from `Manager.doc_info.doc` |

**Responsibility** – Coordinates the full documentation pipeline: prepares LLM model, runs the `Manager` steps, applies optional intro and ordering modules, clears cache, and returns the final doc.  

**Visible Interactions** – Instantiates `GPTModel` (Groq wrapper), creates `Manager` (engine core), invokes `Manager` methods (`generate_code_file`, `generate_global_info`, `generete_doc_parts`, `factory_generate_doc`, `order_doc`, `clear_cache`, `save`). Utilises `DocFactory` to apply both custom and intro modules.  

**Logic Flow**  
1. `sync_model = GPTModel(API_KEYS, use_random=False)`.  
2. `manager = Manager(project_path, config=config, llm_model=sync_model, progress_bar=ConsoleGtiHubProgress())`.  
3. `manager.generate_code_file()`.  
4. If `structure_settings.use_global_file` → `manager.generate_global_info(compress_power=4)`.  
5. `manager.generete_doc_parts(max_symbols=..., with_global_file=...)`.  
6. Apply user modules: `manager.factory_generate_doc(DocFactory(*custom_modules))`.  
7. If ordering enabled → `manager.order_doc()`.  
8. Build intro list based on flags, then `manager.factory_generate_doc(..., to_start=True)`.  
9. `manager.clear_cache()` and `manager.save()`.  
10. Return `manager.doc_info.doc.get_full_doc()`.

> **Warning** – Misspelled method `generete_doc_parts` is called as defined; any change requires matching the implementation.
<a name="autodoc-yaml-options"></a>
The file uses YAML format with a series of top‑level keys that define the behavior of the documentation generator.

**Project metadata**
- `project_name`: a string that sets the displayed name of the project.
- `language`: the language code for generated text (e.g., `en`).

**Files to skip**
- `ignore_files`: a list of glob patterns and directory names that the generator should omit, such as compiled Python files (`*.pyc`), cache folders (`__pycache__`), virtual‑environment directories (`venv`, `env`), IDE configuration directories (`.vscode`, `.idea`), database files, log files, coverage reports, version‑control metadata, and any other paths you want to exclude.

**Build section**
- `save_logs`: boolean flag indicating whether log output should be persisted.
- `log_level`: numeric level controlling verbosity (higher values produce more detailed logs).

**Structure section**
- `include_intro_links`: when true, adds navigation links at the beginning of the document.
- `include_intro_text`: when true, inserts introductory text.
- `include_order`: when true, preserves the order of discovered parts.
- `use_global_file`: when true, merges a global information file into the output.
- `max_doc_part_size`: integer defining the maximum character count for each generated segment.

**Additional project information**
- `project_additional_info`: a mapping where you can place free‑form notes; the example includes a `global idea` description.

**Custom prompts**
- `custom_descriptions`: an array of strings that act as explicit instructions for the generator, such as how to explain installation workflows, how to write this YAML file, or how to use a `Manager` class with code examples.

When creating the file, follow standard YAML indentation (two spaces per level) and ensure each key and value matches the expected type (string, boolean, integer, or list). This structure enables the generator to produce consistent documentation based on the supplied options.
<a name="custommodule-responsibility"></a>
## CustomModule & CustomModuleWithOutContext  

- **CustomModule** builds a description by feeding a **code chunk list** (`split_data(info["code_mix"], max_symbols=5000)`) to `generete_custom_discription`.  
- **CustomModuleWithOutContext** calls `generete_custom_discription_without` (no code context).  

Both rely on `info["language"]` and return a markdown string consumed by `DocFactory`.
<a name="intro-modules-responsibility"></a>
## IntroLinks & IntroText  

- **IntroLinks** extracts HTML links from `info["full_data"]` via `get_all_html_links`, then creates an introductory link block with `get_links_intro`.  
- **IntroText** generates a project‑level introduction using `info["global_info"]` via `get_introdaction`.  

Each module follows the `BaseModule.generate(info, model) → str` contract, enabling seamless integration in the `DocFactory` pipeline.
<a name="manager-responsibility"></a>
## `Manager` – Orchestration Core  
**Responsibility** – Coordinates all pipeline stages for a single project: repository walk, optional global summary, chunked LLM generation, module‑driven custom/introduction sections, ordering, cache handling, and final Markdown persistence.
<a name="custom-intro-postprocessor"></a>
## Custom Intro Post‑Processor Functions  

**Responsibility** – Implements the *intro* portion of the **Auto Doc Generator** pipeline. It extracts anchor links from generated markdown, asks the LLM to craft introductory text (with or without links), and creates optional custom descriptions. All functions rely on a **singleton** `BaseLogger` for structured logging and on a `Model`‑compatible LLM client (`model.get_answer_without_history`).
<a name="CONTENT_DESCRIPTION"></a>` tag and to obey strict token‑level rules (no filenames, extensions, generic terms, or protocols). Returns the raw answer.  

> **⚠️ Warning** – The `generete_custom_discription` loop stops on the first *informative* answer; if every slice yields a “no‑info” response, the function returns an empty string, potentially dropping the custom description from the final document.
<a name="sorting-anchor-extraction-and-reordering"></a>
## Sorting Anchor Extraction & Reordering  

**Component Responsibility** – Parses a full‑document markdown string, extracts `<a name="…"></a>` anchors, builds a mapping *anchor → chunk*, and optionally re‑orders the anchor list via an LLM call.

### Visible Interactions  
- **Imports** `Model` (LLM wrapper) and `BaseLogger`/log types – logging and LLM invocation.  
- **Calls** `model.get_answer_without_history` to obtain a semantically sorted title list.  
- **Raises** a generic `Exception` if the number of detected anchors does not match the number of chunks.  

### Technical Logic Flow  
1. `extract_links_from_start(chunks)` – iterates over pre‑split `chunks`; uses regex `^<a name=["']?(.*?)["']?</a>` to capture leading anchors, keeps those longer than 5 chars, records `have_to_del_first` when a chunk lacks a valid anchor.  
2. `split_text_by_anchors(text)` – splits `text` on a look‑ahead pattern `(?=<a name=["']?[^"'>\s]{6,200}["']?</a>)`, trims whitespace, feeds the list to `extract_links_from_start`.  
3. If the first chunk is not an anchor or `have_to_del_first` is true, the leading chunk is removed.  
4. Validates that `len(all_links) == len(result_chanks)`; otherwise throws *“Somthing with anchors”*.  
5. Constructs `result` dict mapping each `#anchor` to its associated markdown chunk.  
6. `get_order(model, chanks)` – logs start, builds a single‑message user prompt asking the LLM to “Sort the following titles semantically …”, calls `model.get_answer_without_history`, splits the comma‑separated response, logs the final list, and returns it.

### Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `chunks` | `list[str]` | Input to `extract_links_from_start` | Raw markdown pieces after split |
| `text` | `str` | Full markdown document for `split_text_by_anchors` | Must contain `<a name=…></a>` anchors |
| `all_links` | `list[str]` | Anchor identifiers (`#anchor`) | Produced by `extract_links_from_start` |
| `result_chanks` | `list[str]` | Corresponding markdown bodies | Trimmed, non‑empty |
| `have_to_del_first` | `bool` | Flag indicating first chunk removal | Set when first piece lacks a valid anchor |
| `model` | `Model` | LLM client for ordering | Implements `get_answer_without_history(prompt)` |
| `chanks` | `list[str]` | Titles passed to LLM for sorting | Usually anchor names without `#` prefix |
| `new_result` | `list[str]` | Ordered list of titles returned by LLM | Stripped of surrounding whitespace |

> **⚠️ Warning** – If anchor detection fails (`len(all_links) != len(result_chanks)`) the function raises a generic exception, halting the post‑processing pipeline.
<a name="repository-structure-builder-codemix"></a>
## Repository Structure Builder (CodeMix)  

**Component Responsibility** – Walks a repository tree, respects ignore patterns, and produces a plain‑text dump that lists directory hierarchy followed by the raw contents of each non‑ignored file.

### Visible Interactions  
- **Uses** `BaseLogger` for informational logging of ignored paths.  
- **Relies** on standard library `os`, `pathlib.Path`, and `fnmatch` for filesystem traversal and pattern matching.  
- **No external calls** (e.g., LLM) are made in this fragment.

### Technical Logic Flow  
1. `__init__(root_dir, ignore_patterns)` – resolves `root_dir` to an absolute `Path` and stores ignore globs.  
2. `should_ignore(path)` – converts `path` to a relative string, then checks it against each pattern via `fnmatch.fnmatch` on the whole path, its basename, and each path component. Returns `True` if any match.  
3. `build_repo_content()` –  
   a. Starts `content` with a header line.  
   b. Iterates sorted `root_dir.rglob("*")`; for each non‑ignored entry, computes depth, builds an indented line (`"  " * (depth‑1) + name/`), and appends it.  
   c. Inserts a separator line (`"="*20`).  
   d. Re‑iterates files; for each non‑ignored file, writes `<file path="relative">`, the file’s text (`read_text(..., errors="ignore")`), and a newline marker. Errors during read are captured and added as a plain string.  
   e. Joins `content` with newline characters and returns the final string.

### Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `root_dir` | `str` / `Path` | Root of the repository to pack | Resolved to absolute path |
| `ignore_patterns` | `list[str]` | Glob patterns to skip files/folders | Supplied at construction |
| `path` | `Path` | Each filesystem entry visited | Used in both hierarchy and content loops |
| `content` | `list[str]` | Accumulator for textual output | Ends as a single `str` |
| `relative_path` | `Path` | Path relative to `root_dir` for output | Inserted in `<file path="…">` tags |
| `logger` | `BaseLogger` | Logs ignored entries (level 1) | Singleton façade |
| `result` | `str` | Full repository dump returned by `build_repo_content` | Ready for downstream preprocessing |

This module provides the foundational plain‑text representation consumed later by the pre‑processor’s splitter and the LLM generation pipeline.
<a name="gptmodel-wrapper"></a>
## `GPTModel` – Groq LLM Wrapper  

**Responsibility** – Concrete implementation of `Model` that talks to the Groq API, logs activity, and rotates API keys / model names on failure.  

**Visible Interactions**  
- Instantiates a **Groq** client (`self.client = Groq(api_key=…)`).  
- Uses **`BaseLogger`** for `InfoLog`, `WarningLog`, `ErrorLog`.  
- Relies on **`API_KEYS`**, **`History`**, and the shuffled **`regen_models_name`** list inherited from `ParentModel`.  
- Raises **`ModelExhaustedException`** when no model remains usable.  

**Technical Logic Flow**  
1. Log “Generating answer…”.  
2. Select message list: `self.history.history` (if `with_history`) or supplied `prompt`.  
3. Loop until a model succeeds:  
   - Pick `model_name` from `regen_models_name[self.current_model_index]`.  
   - Call `self.client.chat.completions.create(messages=…, model=model_name)`.  
   - On exception: log a warning, rotate API key (`self.current_key_index`) and, if keys wrap, rotate model index.  
   - Re‑instantiate `Groq` with the new key and retry.  
4. After success, extract `result = chat_completion.choices[0].message.content`.  
5. Log success and the answer (level 2).  
6. Return `result` (empty string if `None`).  

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `list[str]` (via `API_KEYS`) | Source of credentials | Rotated on failure |
| `history` | `History` | Message buffer for context | Initialized with `BASE_SYSTEM_TEXT` |
| `models_list` | `list[str]` | Candidate model identifiers | Shuffled if `use_random=True` |
| `client` | `Groq` | Groq API client instance | Re‑created when key changes |
| `logger` | `BaseLogger` | Structured logger | Emits `InfoLog`, `WarningLog`, `ErrorLog` |
| `generate_answer(...)` | `with_history: bool`, `prompt: list[dict]` → `str` | Main LLM call | May raise `ModelExhaustedException`; logs steps; rotates keys/models |

> **Warning** – The method name `generete_doc_parts` (misspelled) appears elsewhere in the project and must be called exactly as defined; altering it would break callers.
<a name="parentmodel-abstract"></a>
## `ParentModel` – Abstract Base for LLM Clients  

Provides shared state (API keys, history, model rotation) and defines the abstract interface (`generate_answer`, `get_answer_without_history`, `get_answer`). Concrete subclasses (`Model`, `AsyncModel`, `GPTModel`, `AsyncGPTModel`) implement the contract.  

**Data Contract** (relevant attributes):  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_keys` | `list[str]` | Credential pool | Supplied via `API_KEYS` |
| `history` | `History` | Message history | Added to via `add_to_history` |
| `regen_models_name` | `list[str]` | Rotating model names | Shuffled if `use_random` |
| `current_model_index` / `current_key_index` | `int` | Index trackers | Updated on failures |
<a name="visible-interactions"></a>
## Visible Interactions  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseLogger` | Singleton class | Writes `InfoLog` entries to `report.txt` | Instantiated locally in each function |
| `Model` | Interface (`get_answer_without_history`) | LLM provider (Groq‑based) | Passed explicitly to every generation call |
| `BASE_INTRODACTION_CREATE_LINKS`, `BASE_INTRO_CREATE`, `BASE_CUSTOM_DISCRIPTIONS` | `str` constants | Prompt fragments imported from `engine.config.config` | Inserted into system messages |
| `re` | std‑lib module | Regex engine for anchor extraction | Pattern `<a name=["']?(.*?)["']?</a>` |
<a name="technical-logic-flow"></a>
## Technical Logic Flow  

1. **`get_all_html_links(data)`** – Scans `data` with the regex above, collects anchors longer than five characters, logs start/end, returns a list like `["#anchor1", …]`.  
2. **`get_links_intro(links, model, language)`** – Builds a three‑message prompt (`system` language, `system` intro‑link template, `user` list of links), logs the request, invokes `model.get_answer_without_history`, logs the response, returns the generated markdown block.  
3. **`get_introdaction(global_data, model, language)`** – Similar to step 2 but uses `BASE_INTRO_CREATE` and passes the raw `global_data` as the user message; returns the LLM‑generated introduction.  
4. **`generete_custom_discription(splited_data, model, custom_description, language)`** – Iterates over `splited_data`; for each slice builds a detailed prompt (language, analyst role, context, custom‑description template). Calls the LLM; if the result does **not** contain `"!noinfo"` or `"No information found"` (or the marker appears after position 30) the loop breaks and that result is returned. Otherwise the loop continues, resetting `result` to an empty string.  
5. **`generete_custom_discription_without(model, custom_description, language)`** – Sends a single prompt that forces the LLM to prepend a unique `
<a name="compressor-module"></a>
## Compressor Module – Chunk Summarization

**Component Responsibility** – Provides functions that compress raw text chunks by invoking the configured LLM and optionally aggregate/combine results.

**Visible Interactions**  
- Calls **`ProjectSettings.prompt`** for a system prompt.  
- Calls **`get_BASE_COMPRESS_TEXT`** (engine config) to embed compression parameters.  
- Uses the **`Model`** interface (`get_answer_without_history`).  
- Updates a **`BaseProgress`** instance for visual feedback.  

**Technical Logic Flow**  
1. `compress` builds a three‑message prompt (system → project settings, system → compress instruction, user → data) and returns the LLM answer.  
2. `compress_and_compare` partitions the input list into groups of `compress_power` items, concatenates each group’s compressed output, and updates the progress bar per element.  
3. `compress_to_one` repeatedly calls `compress_and_compare` until a single aggregated string remains, adjusting `compress_power` to 2 when the list becomes too small.

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` / `list[str]` | Raw text or list of chunks to compress | `compress` expects a single string; `compress_and_compare` / `compress_to_one` expect a list |
| `project_settings` | `ProjectSettings` | Supplies the base system prompt | Accessed via `.prompt` property |
| `model` | `Model` | LLM client | Must implement `get_answer_without_history(prompt)` |
| `compress_power` | `int` | Determines grouping size for aggregation | Default 4; may be reduced to 2 |
| `progress_bar` | `BaseProgress` | UI progress reporting | Uses `create_new_subtask`, `update_task`, `remove_subtask` |

> **⚠️ Warning** – The functions do not perform error handling for failed LLM calls; any exception propagates to the caller.
<a name="projectsettings-module"></a>
## `ProjectSettings` – Prompt Builder

**Component Responsibility** – Constructs the system‑prompt string used by all LLM interactions, embedding static configuration and dynamic project metadata.

**Visible Interactions**  
- Imports **`BASE_SETTINGS_PROMPT`** from the engine configuration.  
- No external I/O; purely in‑memory string assembly.

**Technical Logic Flow**  
1. Constructor stores `project_name` and initialises an empty `info` dict.  
2. `add_info(key, value)` mutates `info`.  
3. `prompt` property concatenates `BASE_SETTINGS_PROMPT`, the project name, and each `info` entry as `"key: value"` lines, returning the assembled string.

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_name` | `str` | Identifier of the target repository | Required at instantiation |
| `info` | `dict` | Arbitrary key/value metadata added via `add_info` | Rendered in prompt order of insertion |
| `prompt` | `property` → `str` | Full system prompt for LLM calls | Combines static and dynamic parts |
<a name="spliter-module"></a>
## `split_data` – Text Chunking Utility

**Component Responsibility** – Supposed to split a large string into size‑bounded fragments respecting `max_symbols`.

**Visible Interactions** – None evident in the provided fragment; the function body is omitted.

**Technical Logic Flow**  
> Information not present in the provided fragment.

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Full source dump to be partitioned | Input to the splitter |
| `max_symbols` | `int` | Upper bound for each chunk’s length | Determines split granularity |
| Return | `list[str]` | Collection of chunk strings | Produced by the missing implementation |
<a name="split-data"></a>
## `split_data` – Text Chunking Utility  

**Responsibility** – Partition a large source dump into size‑bounded fragments respecting `max_symbols`.  

**Visible Interactions** – None in the provided fragment; the implementation body is omitted.  

> **⚠️** *Information not present in the provided fragment.*  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Full source text to split | Input to the splitter |
| `max_symbols` | `int` | Upper length limit per chunk | Determines granularity |
| **Return** | `list[str]` | Collection of chunk strings | Produced by missing implementation |

---
<a name="base-logger"></a>
## `BaseLogger` – Singleton Logger Facade  

**Responsibility** – Provides a global, single‑instance logger that delegates to a configurable `BaseLoggerTemplate`.  

**Visible Interactions**  
- `set_logger(template)` stores the concrete sink.  
- `log(BaseLog)` forwards the log entry to `template.global_log`.  

**Technical Logic Flow**  
1. `__new__` creates one object per process (`cls.instance`).  
2. `set_logger` assigns `self.logger_template`.  
3. `log` calls `self.logger_template.global_log(log)`.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `instance` | `BaseLogger` | Singleton storage | Created on first access |
| `logger_template` | `BaseLoggerTemplate` | Destination for formatted logs | Must be set before `log` |
| `log` (method) | `BaseLog` → `None` | Emits log respecting level | Calls `global_log` of the template |
<a name="base-log-classes"></a>
## `BaseLog` Hierarchy – Message Formatting  

**Responsibility** – Encapsulate a log message with a severity level and render a timestamped string.  

**Visible Interactions**  
- Sub‑classes (`ErrorLog`, `WarningLog`, `InfoLog`) override `format()` to prepend `[LEVEL]`.  

**Technical Logic Flow**  
1. `BaseLog.__init__(message, level)` stores values.  
2. `_log_prefix` builds `"[YYYY‑MM‑DD HH:MM:SS]"`.  
3. Each subclass formats: `f"{prefix} [LEVEL] {message}"`.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `message` | `str` | Log text | |
| `level` | `int` | Severity index (default 0) | |
| `format()` | `-> str` | Returns ready‑to‑print line | Uses `_log_prefix` |
<a name="file-logger-template"></a>
## `FileLoggerTemplate` – File‑Based Sink  

**Responsibility** – Persist log entries to a file, one per line.  

**Visible Interactions**  
- Inherits `log` from `BaseLoggerTemplate` and overrides to open `file_path` in append mode.  

**Technical Logic Flow**  
1. `__init__(file_path, log_level)` stores path and level.  
2. `log(log)` writes `log.format() + "\n"` to the file.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `file_path` | `str` | Destination file | Created if missing |
| `log_level` | `int` | Threshold for `global_log` | Propagated from base |
| `log()` | `BaseLog` → `None` | Append formatted line | No console output |
<a name="progress-base"></a>
## `BaseProgress` – Abstract Progress Interface  

**Responsibility** – Define the contract for sub‑task progress reporting.  

**Visible Interactions**  
- Sub‑classes implement `create_new_subtask`, `update_task`, `remove_subtask`.  

**Technical Logic Flow**  
- No concrete behavior; methods are placeholders (`...`).  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `create_new_subtask(name, total_len)` | `str, int` → `None` | Start a new sub‑task | |
| `update_task()` | `→ None` | Advance current sub‑task or base task | |
| `remove_subtask()` | `→ None` | Clear current sub‑task reference | |
<a name="lib-progress"></a>
## `LibProgress` – Rich‑Based Progress Bar  

**Responsibility** – Render hierarchical progress using *rich*'s `Progress`.  

**Visible Interactions**  
- Calls `self.progress.add_task` for base and sub‑tasks.  
- `update_task` advances the active task; falls back to base.  

**Technical Logic Flow**  
1. Initialise base task with total `total`.  
2. `create_new_subtask` registers a sub‑task and stores its ID.  
3. `update_task` advances the stored sub‑task if present, else the base.  
4. `remove_subtask` clears the sub‑task ID.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `progress` | `rich.progress.Progress` | Rendering engine | Passed at construction |
| `_base_task` | `int` | ID of the overall task | |
| `_cur_sub_task` | `int | None` | Current sub‑task ID | Cleared on removal |
<a name="console-github-progress"></a>
## `ConsoleGtiHubProgress` – Simple Console Reporter  

**Responsibility** – Provide lightweight console progress without external dependencies.  

**Visible Interactions**  
- Uses `ConsoleTask` to print start and incremental percentages.  

**Technical Logic Flow**  
1. Initialise a general `ConsoleTask` (`gen_task`).  
2. `create_new_subtask` replaces `curr_task` with a new `ConsoleTask`.  
3. `update_task` calls `progress()` on the active task; defaults to `gen_task`.  
4. `remove_subtask` discards `curr_task`.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `gen_task` | `ConsoleTask` | Default progress bar | Fixed total = 4 |
| `curr_task` | `ConsoleTask | None` | Active sub‑task | Created per `create_new_subtask` |
<a name="install-ps1"></a>
## `install.ps1` – CI Workflow & Config Bootstrap  

**Responsibility** – Automate creation of a GitHub Actions workflow file and a default `autodocconfig.yml`.  

**Visible Interactions**  
- Uses PowerShell `New-Item` to ensure `.github/workflows` exists.  
- Writes a static workflow YAML (`autodoc.yml`).  
- Generates `autodocconfig.yml` populated with the current directory name and a comprehensive ignore list.  

**Technical Logic Flow**  
1. Ensure workflow directory.  
2. Define `$content` (workflow YAML) and output to `.github/workflows/autodoc.yml`.  
3. Retrieve `$currentFolderName` and embed into `$configContent`.  
4. Write `$configContent` to `autodocconfig.yml`.  
5. Print success message.  

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `.github/workflows/autodoc.yml` | file | GitHub Actions definition | References external reusable workflow |
| `autodocconfig.yml` | file | Default configuration for Auto Doc Generator | Includes ignore patterns, build and structure settings |
| `$currentFolderName` | `str` | Project name placeholder | Inserted into config |
| Success output | console | Confirmation banner | Green‑colored text |
<a name="install-sh"></a>
## `install.sh` – CI Workflow & Config Bootstrap  

**Responsibility** – Provision a GitHub Actions workflow file and a default `autodocconfig.yml` for the **Auto Doc Generator** project.  

### Visible Interactions  
- Creates directory `.github/workflows` if absent.  
- Writes a static workflow definition (`autodoc.yml`) that references a reusable workflow in the `Drag-GameStudio/ADG` repo.  
- Generates `autodocconfig.yml` populated with the current folder name and a comprehensive ignore‑list, language setting, build and structure options.  
- Prints success messages to the console.  

### Technical Logic Flow  
1. `mkdir -p .github/workflows` – ensures the target folder exists.  
2. `cat <<EOF > .github/workflows/autodoc.yml` – writes the YAML content; the only escaped character is the leading `$` in the secret reference (`\${{ secrets.GROCK_API_KEY }}`).  
3. `echo "✅ Done! .github/workflows/autodoc.yml has been created."` – confirms file creation.  
4. `cat <<EOF > autodocconfig.yml` – builds a YAML config:  
   - `project_name` set to `$(basename "$PWD")`.  
   - `language: "en"`.  
   - `ignore_files` list (pyc, cache dirs, env folders, binaries, logs, VCS, etc.).  
   - `build_settings` and `structure_settings` blocks with default flags.  
5. `echo "✅ Done! autodocconfig.yml has been created."` – final confirmation.  

### Data Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `.github/workflows` | directory | Destination for CI workflow file | Created with `mkdir -p`. |
| `.github/workflows/autodoc.yml` | file (YAML) | GitHub Actions definition | References reusable workflow; injects `${{ secrets.GROCK_API_KEY }}`. |
| `autodocconfig.yml` | file (YAML) | Default generator configuration | `project_name` derived from `basename "$PWD"`; includes ignore patterns, build & structure settings. |
| `echo` statements | stdout | User feedback | Prints ✅ messages upon successful writes. |
| `cat <<EOF … EOF` | Bash heredoc | Writes multi‑line content verbatim | Only the first `$` is escaped to preserve the secret placeholder. |

> **Assumption** – The script is executed from the root of the target repository; otherwise `$(basename "$PWD")` may not reflect the intended project name.
<a name="install-workflow-setup"></a>

**Installation Workflow Overview**

1. **PowerShell Execution (Windows)**
   - Open a PowerShell session with elevated privileges.
   - Retrieve the remote installation script using `Invoke‑RestMethod` and execute it directly:
     ```powershell
     irm <repository‑path>/install.ps1 | iex
     ```
   - This command streams the script from the repository into the current session, performing all required setup steps automatically.

2. **Shell Execution (Linux/macOS)**
   - Open a terminal.
   - Use `curl` to download the installer and pipe it to the shell interpreter:
     ```bash
     curl -sSL <repository‑path>/install.sh | bash
     ```
   - The script runs in the current environment, handling dependencies and configuration for Unix‑like systems.

3. **GitHub Actions Secret**
   - In the repository’s **Settings → Secrets** section, create a new secret named `GROCK_API_KEY`.
   - Populate the secret with the API key obtained from the Grock documentation.
   - The workflow will reference this secret to authenticate calls to the Grock service during automated runs.
<a name="manager-class-usage-and-methods"></a>
The Manager class is used to manage the generation of documentation. To use the Manager class, you need to create an instance of it, passing in the project path, config, llm_model, and progress_bar as arguments. 

Here is an example of how to create a Manager instance:
```python
manager = Manager(
    project_path, 
    config=config,
    llm_model=sync_model,
    progress_bar=ConsoleGtiHubProgress(), 
)
```
The Manager class has several methods available:

1. `generate_code_file()`: This method generates a code file.
```python
manager.generate_code_file()
```
2. `generate_global_info(compress_power)`: This method generates global information with a specified compress power.
```python
manager.generate_global_info(compress_power=4)
```
3. `generete_doc_parts(max_symbols, with_global_file)`: This method generates document parts with a specified maximum number of symbols and option to include global file.
```python
manager.generete_doc_parts(max_symbols=structure_settings.max_doc_part_size, with_global_file=structure_settings.use_global_file)
```
4. `factory_generate_doc(DocFactory, to_start)`: This method generates a document using a DocFactory instance, with an option to generate it from the start.
```python
manager.factory_generate_doc(DocFactory(*custom_modules), to_start=True)
```
5. `order_doc()`: This method orders the generated document.
```python
manager.order_doc()
```
6. `clear_cache()`: This method clears the cache.
```python
manager.clear_cache()
```
7. `save()`: This method saves the generated document.
```python
manager.save()
```
8. `doc_info.doc.get_full_doc()`: This method returns the full generated document.
```python
output_doc = manager.doc_info.doc.get_full_doc()
```
