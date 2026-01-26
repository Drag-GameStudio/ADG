## Executive Navigation Tree
- 📂 Configuration
  - [#configuration-loading](#configuration-loading)

- 📂 Model Management
  - [#model-initialization](#model-initialization)
  - [#manager-orchestration](#manager-orchestration)
  - [#model-generation-responsibility](#model-generation-responsibility)
  - [#model-interactions](#model-interactions)
  - [#model-technical-details](#model-technical-details)
  - [#model-data-flow](#model-data-flow)
  - [#parentmodel-initialization](#parentmodel-initialization)

- ⚙️ Execution
  - [#execution-flow](#execution-flow)

- 📜 History
  - [#history-management](#history-management)

- 🔌 Interface
  - [#synchronous-model-interface](#synchronous-model-interface)
  - [#asynchronous-model-interface](#asynchronous-model-interface)

- 🛠️ Utilities
  - [#html-link-extractor](#html-link-extractor)

- ❓ Misc
  - [#…](#…)

- 🚀 Generators
  - [#link-introduction-generator](#link-introduction-generator)
  - [#global-introduction-generator](#global-introduction-generator)

- 🧠 Engines
  - [#custom-description-engine](#custom-description-engine)
  - [#compression-engine](#compression-engine)

- 📦 Chunking
  - [#anchor-based-chunk-splitter](#anchor-based-chunk-splitter)
  - [#chunk-splitter-and-doc-generator](#chunk-splitter-and-doc-generator)

- 📦 Packaging
  - [#repository-content-packager](#repository-content-packager)

- 🛠️ Settings
  - [#project-settings-builder](#project-settings-builder)

- 📓 Logging
  - [#logging-classes](#logging-classes)
  - [#logger-template-dispatch](#logger-template-dispatch)

- 📈 Progress
  - [#progress-implementations](#progress-implementations)
  - [#data‑flow‑logging‑progress](#data‑flow‑logging‑progress)

 

<a href="autodocconfig.yml"></a>To install the workflow, run the appropriate script for your platform:

- **Windows (PowerShell)**:  
  ```powershell
  irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
  ```

- **Linux/macOS (bash)**:  
  ```bash
  curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
  ```

Additionally, add a secret variable named **GROCK_API_KEY** to your GitHub Actions settings. Set its value to your API key obtained from the Grock documentation at https://grockdocs.com. This secret is required for the documentation generation workflow to function correctly.

<a href="autodocgenerator/manage.py"></a>!noinfo

<a href="autodocconfig.yml"></a>
The `autodocconfig.yml` file is a YAML document that defines the settings for the Auto Doc Generator. The available top‑level options are:

* **project_name** – a string with the name of the project.  
  Example: `project_name: "Auto Doc Generator"`

* **language** – the language code used for the generated documentation (e.g., `en`).  

* **project_settings** – a mapping that controls generator behaviour:  
  * **save_logs** – boolean, whether to write logs to files.  
  * **log_level** – integer, the verbosity level of logging.

* **project_additional_info** – a free‑form mapping for any extra information you want to attach to the project. Each entry is a key/value pair (both strings).  
  Example:  
  ```yaml
  project_additional_info:
    global idea: "This project was created to help developers make documentations for them projects"
  ```

* **custom_descriptions** – a list of strings. Each string is a custom description that will be turned into a documentation module.  
  Example:  
  ```yaml
  custom_descriptions:
    - "explain how install workflow with install.ps1 and install.sh scripts …"
    - "how to use Manager class what parameters i need to give. give full example of usage"
    - "explain how to write autodocconfig.yml file what options are available"
  ```

When writing the file, keep the YAML indentation consistent and include only the keys you need; omitted keys will use the defaults defined in the code.

 

<a name="configuration-loading"></a>
## Configuration Loading & Factory Preparation  
`read_config` parses **autodocconfig.yml**, builds a `Config` object, and populates: language, ignore patterns, `ProjectConfigSettings`, additional info, and a list of `CustomModule` instances. It then returns two factories – a generic `doc_factory` (custom modules) and an `intro_factory` (static intro components).

<a name="model-initialization"></a>
## GPT Model Instantiation  
```python
sync_model = GPTModel(API_KEY, use_random=False)
async_model = AsyncGPTModel(API_KEY)
```  
Both models receive the API key from `engine.config`. The synchronous model is used for deterministic calls, while the async variant is prepared for future parallelism.

<a name="manager-orchestration"></a>
## Manager Orchestration & Generation Steps  
A `Manager` is created with the project root, `ProjectSettings`, `ProjectConfigSettings`, the ignore list, and a `ConsoleGtiHubProgress` bar. The subsequent calls execute the full pipeline:  

1. `generate_code_file()` – extracts source files.  
2. `generate_global_info_file(use_async=False, max_symbols=8000)` – builds a project‑wide summary.  
3. `generete_doc_parts(use_async=False, max_symbols=10000)` – splits code into doc‑ready chunks.  
4. `factory_generate_doc(doc_factory)` – runs user‑defined modules.  
5. `order_doc()` – sorts sections.  
6. `factory_generate_doc(intro_factory)` – prepends introductory material.  

Finally, `clear_cache()` removes temporary artifacts and `read_file_by_file_key("output_doc")` returns the rendered Markdown.

<a name="execution-flow"></a>
## Script Execution Flow  
When invoked as a module, the script reads *autodocconfig.yml*, resolves factories, calls `gen_doc` with the assembled parameters, and stores the result in `output_doc`. All side effects (file generation, cache cleanup, progress rendering) are confined to the `Manager` instance.

<a name="model-generation-responsibility"></a>
## Model Generation Responsibility
Implements concrete `GPTModel` (sync) and `AsyncGPTModel` (async) subclasses of the engine’s abstract `Model`/`AsyncModel`. Each class wraps a Groq client, selects a viable model from `regen_models_name`, and returns the generated text while logging progress.

<a name="model-interactions"></a>
## Interaction with Engine & UI
- Inherits shared state (`api_key`, `history`, `use_random`, `regen_models_name`, `current_model_index`) from the base classes.  
- Uses `BaseLogger` from `ui.logging` to emit `InfoLog`, `WarningLog`, and `ErrorLog`.  
- Raises `ModelExhaustedException` when no model remains usable, propagating the error to the surrounding `Manager` workflow.

<a name="model-technical-details"></a>
## Technical Details
- **`__init__`**: Instantiates `Groq` or `AsyncGroq` client with the supplied API key; sets up a logger.  
- **`generate_answer` / `async generate_answer`**:  
  1. Determines message payload (`history.history` vs. direct `prompt`).  
  2. Enters a loop selecting `model_name` from `regen_models_name`.  
  3. Calls `client.chat.completions.create`.  
  4. On exception, logs a warning and advances `current_model_index` (wrap‑around).  
  5. Upon success, extracts `content` from `chat_completion.choices[0].message`.  
  6. Logs the chosen model and final answer before returning it.

<a name="model-data-flow"></a>
## Data Flow & Side Effects
- **Inputs**: `api_key`, optional `history` object, `use_random` flag, `with_history` boolean, optional `prompt` string.  
- **Outputs**: Generated answer string.  
- **Side Effects**: Logging activity, possible modification of `current_model_index`, and raising `ModelExhaustedException` when the model pool is empty.  
- **Assumptions**: `regen_models_name` is pre‑populated with viable model identifiers; `History` provides a `history` list compatible with Groq’s chat API.

<a name="history-management"></a>
## History Management  

The `History` class records conversation turns for chat‑style LLM calls.  
- **Constructor** (`__init__(system_prompt)`) creates an empty `history` list and, if a system prompt is supplied, inserts a `"system"` role entry.  
- **add_to_history(role, content)** appends a dict `{"role": role, "content": content}` to `self.history`.  
*Assumption*: callers provide plain strings; the list format matches Groq/Chat‑ML expectations.

<a name="parentmodel-initialization"></a>
## ParentModel Initialization  

`ParentModel` supplies shared state for both sync and async models.  
- Accepts `api_key` (default from config), a `History` instance, and `use_random`.  
- Stores `self.history`, `self.api_key`, and starts `self.current_model_index = 0`.  
- Copies `MODELS_NAME`, shuffles it when `use_random=True`, and exposes the ordered list as `self.regen_models_name`.  
*Side effect*: randomisation of model selection order for subsequent calls to `generate_answer`.

<a name="synchronous-model-interface"></a>
## Synchronous Model Interface  

`Model` inherits from `ParentModel` and implements three thin wrappers around `generate_answer`.  
- `generate_answer(with_history=True, prompt=None) -> str` – placeholder returning `"answer"` (real implementation is injected elsewhere).  
- `get_answer_without_history(prompt)` forwards to `generate_answer(with_history=False, ...)`.  
- `get_answer(prompt)` records the user prompt, calls `generate_answer()`, stores the assistant reply, and returns the answer.  
*Data flow*: `prompt` → history → `generate_answer` → answer → history.

<a name="asynchronous-model-interface"></a>
## Asynchronous Model Interface  

`AsyncModel` mirrors `Model` but with `async` methods.  
- `async generate_answer(with_history=True, prompt=None) -> str` – stub returning `"answer"`.  
- `async get_answer_without_history(prompt)` awaits `generate_answer`.  
- `async get_answer(prompt)` updates history synchronously, then awaits `generate_answer` before storing and returning the result.  

Both interfaces rely on the shared `History` instance and respect the ordered `regen_models_name` list for model selection in the real `generate_answer` implementation.

<a name="html-link-extractor"></a>
## HTML Link Extractor  

**Responsibility** – Scans a documentation string for `<a name="…"></a>` anchors and returns a list of Markdown‑style fragment links (`#anchor`).  

**Interactions** – Called by the post‑processing pipeline to build a navigation index; relies only on Python’s `re` module and the internal `BaseLogger`.  

**Technical details** –  
- Compiles a simple regex `r'<a name=["\']?(.*?)["\']?>'`.  
- Iterates `re.finditer`, extracts the captured group, prefixes with `#`, logs progress and result.  

**Data flow** – Input: raw HTML/markdown `data : str` → regex search → `links : list[str]` → returned to caller; side effect: logger writes two `InfoLog` entries.

---

<a name="link-introduction-generator"></a>
## Link Introduction Generator  

**Responsibility** – Generates a natural‑language intro that references a set of extracted links.  

**Interactions** – Uses a `Model` implementation (e.g., `GPTModel`) to call `model.get_answer_without_history`. The prompt combines a language directive, a constant `BASE_INTRODACTION_CREATE_TEXT`, and the stringified link list.  

**Technical details** –  
- Builds a 3‑message system/user prompt.  
- Logs before/after the LLM call.  
- Returns the LLM‑produced `intro_links : str`.  

**Data flow** – `links → prompt → model.get_answer_without_history → intro_links`; side effect: three log entries.

---

<a name="global-introduction-generator"></a>
## Global Introduction Generator  

**Responsibility** – Produces a full introductory paragraph for the whole documentation block.  

**Interactions** – Similar to the link generator but uses `BASE_INTRO_CREATE` as the system prompt and passes the complete `global_data`.  

**Technical details** – Constructs a 3‑message prompt and returns the model’s answer unchanged.  

**Data flow** – `global_data → prompt → model.get_answer_without_history → intro`.

---

<a name="custom-description-engine"></a>
## Custom Description Engine  

**Responsibility** – Iterates over split documentation chunks, asking the LLM to create concise, anchor‑prefixed descriptions for a user‑supplied `custom_description`.  

**Interactions** – For each chunk it sends a detailed system prompt (language, role, strict rules) plus a user task to the same `Model`. Stops on the first non‑empty, non‑`!noinfo` result.  

**Technical details** –  
- Loops over `splited_data`.  
- Uses strict rule block to enforce empty output when info is missing.  
- Breaks when a valid result appears; otherwise returns an empty string.  

**Data flow** – `splited_data + custom_description → per‑chunk prompt → model.get_answer_without_history → result`.

---

<a name="anchor-based-chunk-splitter"></a>
## Anchor‑Based Chunk Splitter & Sorter  

**Responsibility** – Parses a monolithic HTML/markdown document into anchor‑delimited chunks, validates one‑to‑one anchor‑chunk mapping, and orders chunks semantically via LLM.  

**Interactions** – `extract_links_from_start` and `split_text_by_anchors` produce a dict `{anchor: chunk}`. `get_order` sends the list of titles to the `Model` for sorting, then reassembles the ordered text.  

**Technical details** –  
- Regex `^<a name=…>` extracts leading anchors.  
- `re.split` with look‑ahead splits on anchor boundaries.  
- Validation: `len(all_links) == len(chunks)` else `None`.  
- Prompt for sorting: single‑message user request, expects comma‑separated titles.  
- Reassembles via `order_output += f"{chanks.get(el)} \n"`.  

**Data flow** – `text → split_text_by_anchors → dict` → `get_order(dict) → sorted string`; logs each step.

---

<a name="repository-content-packager"></a>
## Repository Content Packager  

**Responsibility** – Traverses a project directory, writes a hierarchical tree view and in‑line file contents to a single output file (`repomix-output.txt`).  

**Interactions** – Uses `Path.rglob` to enumerate files, `should_ignore` to filter based on `ignore_patterns`, and `BaseLogger` for progress logs. No external services.  

**Technical details** –  
- `should_ignore` matches against glob patterns, file basenames, and any path component.  
- `build_repo_content` writes a “Repository Structure” block, then each non‑ignored file wrapped in `<file path="…">` tags.  
- Handles read errors with a catch‑all exception, inserting an error line.  

**Data flow** – `root_dir + ignore_patterns → file enumeration → filtered list → output file` (side effect: file creation + log entries).

<a name="compression-engine"></a>
## Compression Engine  

**Responsibility** – Reduces raw text (code or docs) to a concise form using the LLM, optionally grouping several inputs into a single compressed block for later comparison.  

**Interactions** – Calls `project_settings.prompt` and `get_BASE_COMPRESS_TEXT` to build a three‑message prompt, then invokes `model.get_answer_without_history`.  Progress is reported via a `BaseProgress` instance.  

**Technical details** –  
- `compress` builds the prompt (`system` → project prompt, `system` → compress‑text template, `user` → data).  
- `compress_and_compare` iterates over a list, concatenating every *compress_power* results; updates the progress bar.  
- Async counterparts (`async_compress`, `async_compress_and_compare`) run under a semaphore and use `await model.get_answer_without_history`.  

**Data flow** – `data (+ settings) → prompt → model → compressed string`; aggregated list → progress bar side‑effects.

<a name="project-settings-builder"></a>
## Project Settings Builder  

**Responsibility** – Generates a dynamic system prompt containing base settings and project‑specific key/value pairs.  

**Interactions** – Consumed by the compressor and splitter when they need a contextual system message.  

**Technical details** –  
- `ProjectSettings` stores `project_name` and an `info` dict.  
- `add_info(key, value)` mutates the dict.  
- The `prompt` property concatenates `BASE_SETTINGS_PROMPT`, the project name, and each `info` entry on separate lines.  

**Data flow** – `ProjectSettings` instance → `prompt` string → injected into LLM prompts.

<a name="chunk-splitter-and-doc-generator"></a>
## Chunk Splitter & Documentation Generator  

**Responsibility** – Splits a large monolithic source string into size‑constrained chunks, then drives LLM‑based documentation generation per chunk (sync or async).  

**Interactions** – Uses `BASE_PART_COMPLITE_TEXT` as a system prompt, optionally carries forward previous part output (`prev_info`).  Logs via `BaseLogger` and reports progress with `BaseProgress`.  

**Technical details** –  
- `split_data` respects `max_symbols`, recursively breaks overly long lines, and packs them into a list of chunks.  
- `write_docs_by_parts` builds a prompt (system language/id, system base text, optional previous info, user chunk) and cleans surrounding markdown fences.  
- Async versions (`async_write_docs_by_parts`, `async_gen_doc_parts`) run under a semaphore and update progress via a callback.  
- `gen_doc_parts`/`async_gen_doc_parts` orchestrate chunk processing, concatenate results, and keep a trailing context slice (≈ 3000 chars).  

**Data flow** – `full_code_mix → split_data → [chunks] → per‑chunk prompt → model → documentation string → aggregated output (side‑effect: logs & progress updates).

<a name="logging-classes"></a>  
## Logging classes hierarchy  

`BaseLog` stores a raw message and a numeric *level*. Sub‑classes (`ErrorLog`, `WarningLog`, `InfoLog`) override `format()` to prepend a timestamp (`_log_prefix`) and a severity tag.  

<a name="logger-template-dispatch"></a>  
## Logger template dispatch  

`BaseLoggerTemplate` holds a *log_level* threshold and implements `global_log()`, which forwards a `BaseLog` to `log()` only when the log’s level satisfies the threshold.  

`FileLoggerTemplate` extends the template, overriding `log()` to append formatted entries to a file path supplied at construction.  

`BaseLogger` is a **singleton** façade exposing `set_logger()` to inject any `BaseLoggerTemplate` and a `log()` method that delegates to the injected template’s `global_log()`.  

<a name="progress-implementations"></a>  
## Progress implementations  

`BaseProgress` defines the public API (`create_new_subtask`, `update_task`, `remove_subtask`).  

`LibProgress` wraps *rich.progress.Progress*: it creates a base task, optionally a sub‑task, and advances the appropriate one on `update_task()`.  

`ConsoleGtiHubProgress` provides a lightweight fallback using `ConsoleTask`, which prints simple “Starting task” and incremental percent messages to stdout.  

<a name="data‑flow‑logging‑progress"></a>  
## Data flow & side effects  

- **Logging**: `BaseLogger.log(log_obj)` → `BaseLoggerTemplate.global_log()` → (if level permitted) → `BaseLoggerTemplate.log()`.  
  - *FileLoggerTemplate*: writes a line to the configured file (side‑effect).  
  - *Console* (default `BaseLoggerTemplate`): prints to stdout.  

- **Progress**: client code calls `create_new_subtask(name, total)` → stores task identifier. Subsequent `update_task()` advances either the sub‑task or the base task; `remove_subtask()` clears the sub‑task reference.  

Both subsystems are interchangeable; the UI layer injects the desired logger or progress implementation, enabling unified progress reporting and diagnostic output throughout the documentation generation pipeline.

