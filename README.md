## Executive Navigation Tree
- 📦 **Build & Packaging**
  - [Build System Configuration](#build-system-configuration)
  - [Package Initialization](#package-initialization)
  - [Package Metadata](#package-metadata)
- 📦 **Dependency Management**
  - [Dependency Declarations](#dependency-declarations)
- ⚙️ **CI/CD**
  - [GitHub Action Setup](#github-action-setup)
- 📁 **Repository & Structure**
  - [ProjectSettings Class](#projectsettings-class)
  - [Repository Structure Builder](#repository-structure-builder)
- 🪵 **Logging**
  - [Logger Instantiation Flow](#logger-instantiation-flow)
  - [Logging and Model Interaction](#logging-and-model-interaction)
  - [Logging Hierarchy](#logging-hierarchy)
- 🏭 **Factory & Orchestration**
  - [BaseFactory‑Orchestrator](#basefactory‑orchestrator)
  - [Custom‑Module‑Generation](#custom‑module‑generation)
  - [Doc‑Generation‑Orchestrator](#doc‑generation‑orchestrator)
  - [Factory Doc Assembly](#factory-doc-assembly)
- 📦 **Modules**
  - [Intro Modules Link and Text](#intro‑modules‑link‑and‑text)
  - [Inter‑Module Interactions](#inter‑module‑interactions)
  - [Manager Class Usage](#manager-class-usage)
  - [Manager Orchestration](#manager-orchestration)
- 📊 **Assumptions & Constraints**
  - [Assumptions and Constraints](#assumptions-and‑constraints)
- 🔧 **Cache & Path Resolution**
  - [Cache and Path Resolution](#cache-and-path-resolution)
- 📊 **Data Flow & Side Effects**
  - [Data Flow and Side Effects](#data‑flow-and‑side‑effects)
  - [Split Data](#split-data)
- 📄 **YAML & Runtime Objects**
  - [YAML to Runtime Objects](#yaml‑to‑runtime‑objects)
- 🤖 **Model Wrappers**
  - [AsyncGPTModel Async Wrapper](#asyncgptmodel‑async‑wrapper)
  - [GPTModel Sync Wrapper](#gptmodel‑sync‑wrapper)
- 🗂️ **History & Content**
  - [History Prompt Buffer](#history‑prompt‑buffer)
  - [CONTENT_DESCRIPTION](#CONTENT_DESCRIPTION)
- 📚 **Chunk Extraction & Description**
  - [Anchor‑Based Chunk Extraction](#anchor-based-chunk-extraction)
  - [Custom Description Synthesis](#custom-description-synthesis)
  - [Doc Chunk Behaviour](#doc‑chunk‑behaviour)
  - [Document Ordering](#document-ordering)
  - [Generate Descriptions](#generate-descriptions)
  - [Gen Doc Parts](#gen-doc-parts)
- 🔗 **Link & Introduction Generation**
  - [HTML Link Extraction Logic](#html-link-extraction-logic)
  - [Link‑Based Introduction Generation](#link-based-introduction-generation)
  - [Plain Introduction Synthesis](#plain-introduction-synthesis)
- 🌐 **Parent Model Shared State**
  - [ParentModel Shared State](#parentmodel‑shared‑state)
- 📈 **Progress & Semantic Ordering**
  - [Progress Implementations](#progress-implementations)
  - [Semantic Title Ordering](#semantic-title-ordering)
- 🔄 **Sync / Async Generation**
  - [Sync Doc Part Generation](#sync-doc-part-generation)
  - [Write Autodocfile Options](#write-autodocfile-options)
  - [Write Docs by Parts](#write-docs-by-parts)
  - [Async Gen Doc Parts](#async-gen-doc-parts)
  - [Async Write Docs by Parts](#async-write-docs-by-parts)
- 🗜️ **Compression**
  - [Async Compress](#async-compress)
  - [Async Compress and Compare](#async-compress-and-compare)
  - [Compress and Compare Sync](#compress-and-compare-sync)
  - [Compress Single Pass](#compress-single-pass)
  - [Compress to One](#compress-to-one)
- 🧩 **Code Mix Generation**
  - [Code Mix Generation](#code-mix-generation)

 

<a name="build-system-configuration"></a>
## Build‑system configuration  

**Responsibility** – Informs PEP 517 how to build the project by specifying the build backend and its minimum requirement.  

**Interactions** – When `python -m build` or `pip install .` is invoked, the build front‑end imports `poetry.core.masonry.api` and calls its `build_wheel` / `build_sdist` APIs.  

**Technical details**  
- `requires = ["poetry-core>=2.0.0"]` ensures the build backend is present.  
- `build-backend = "poetry.core.masonry.api"` points to Poetry’s PEP 517 implementation.  

**Data flow** – Input: the `pyproject.toml` file itself. Output: built distribution archives (`.whl`, `.tar.gz`) placed in `dist/`. 
<a name="dependency-declarations"></a>
## Dependency declarations  

**Responsibility** – Enumerates the exact third‑party packages required at runtime, with pinned versions to guarantee reproducible builds.  

**Interactions** – Poetry resolves these constraints, creates a lockfile, and installs the packages into a virtual environment. The application imports the listed libraries (e.g., `rich`, `pydantic`, `openai`).  

**Technical details**  
- `requires-python = ">=3.11,<4.0"` restricts interpreter compatibility.  
- Each entry follows the format `package==exact.version`.  
- Versions span utilities (e.g., `requests`), AI SDKs (`openai`, `google-genai`), and UI helpers (`rich`, `tqdm`).  

**Data flow** – Input: developer‑specified version strings. Output: a resolved dependency graph written to `poetry.lock`; at install time, the resolved packages are materialised on disk. 
<a name="github-action-setup"></a>
To set up the automation workflow, follow these steps:

1. **PowerShell‑based environment (Windows)**  
   - Use PowerShell’s *Invoke‑Expression* to fetch and execute the remote installer script in a single command:  
     ```powershell
     irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
     ```  
   - This command downloads the script directly from the project's raw content location and evaluates it on the host machine.

2. **POSIX‑compatible environment (Linux/macOS)**  
   - Retrieve and execute the installer script with a single pipeline using *curl* and *bash*:  
     ```bash
     curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
     ```  
   - The flags `-sSL` make the transfer silent, follow redirects, and display errors, while piping to *bash* runs the script immediately.

3. **GitHub Action secret**  
   - In the repository’s Actions settings, create a secret named `GROCK_API_KEY`.  
   - Obtain the required key from the documentation hosted at `grockdocs.com` and paste it into the secret field.  
   - The workflow will reference this secret to authenticate calls to the external Grock service.

By performing the two platform‑specific commands and configuring the secret, the workflow becomes fully operational across Windows and Linux‑based runners. 
<a name="package-initialization"></a>
## Package initialization and logger bootstrap  

The **autodocgenerator** package executes a short bootstrap when imported. It prints a literal *“ADG”* to standard output, then creates a singleton‑style logger instance (`logger`) based on the UI logging abstraction. This enables every sub‑module to emit structured logs without additional setup. 
<a name="package-metadata"></a>
## Package metadata  

**Responsibility** – Declares the distributable identity of the *autodocgenerator* library: name, version, brief description, author contact, licensing, and the location of the long‑form README.  

**Interactions** – Consumed by packaging tools (Poetry, pip, build) to generate `dist/` artifacts and to populate the project’s *metadata* section on PyPI. Runtime code does not import this file.  

**Technical details**  
- `name`, `version`, `description` are mandatory PEP 621 fields.  
- `authors` is a list of mappings, enabling tools to render proper author credits.  
- `license` uses a free‑text block (`MIT`).  
- `readme` points to `README.md`, allowing automatic inclusion in the wheel’s `METADATA`.  

**Data flow** – Input: static values maintained by the maintainer. Output: a TOML document parsed by build back‑ends; resulting values flow into the generated wheel/sdist metadata files. 
None 
<a name="projectsettings-class"></a>
## `ProjectSettings` – project‑wide prompt composer  

**Responsibility** – Holds the project name and an arbitrary key/value info map; renders a full system prompt by concatenating `BASE_SETTINGS_PROMPT`, the project name, and each `info` entry.  

**Key members** –  
* `__init__(self, project_name: str)` – stores name, init empty `info`.  
* `add_info(self, key, value)` – mutates `info`.  
* `prompt` property – builds and returns the composite prompt string.  

**Data flow** – No side‑effects beyond internal state mutation; `prompt` is read‑only.

---

**Mapping anchor → raw section text**

```python
{
    "#compress-single-pass": "## `compress` – single‑pass LLM compression\n\n**Responsibility** … (text of first section)",
    "#compress-and-compare-sync": "## `compress_and_compare` – batch sync compression\n\n**Responsibility** …",
    "#async-compress": "## `async_compress` – semaphore‑protected async compression\n\n**Responsibility** …",
    "#async-compress-and-compare": "## `async_compress_and_compare` – parallel batch compression\n\n**Responsibility** …",
    "#compress-to-one": "## `compress_to_one` – iterative reduction to a single summary\n\n**Responsibility** …",
    "#generate-descriptions": "## `generate_describtions_for_code` – LLM‑driven API documentation generator\n\n**Responsibility** …",
    "#projectsettings-class": "## `ProjectSettings` – project‑wide prompt composer\n\n**Responsibility** …"
}
``` 
<a name="repository-structure-builder"></a>  
## Repository Structure Builder (`CodeMix`)  

**Responsibility** – Walks a source tree, writes a concise directory tree followed by the raw content of each non‑ignored file into a single output file (`repomix-output.txt`).  

**Interactions** – Operates on the filesystem rooted at `root_dir`; uses `BaseLogger` for informational messages. It does **not** depend on other project modules.  

**Technical details** –  
* `should_ignore` applies `ignore_patterns` (glob‑style) to the relative path, filename, and any path component.  
* `build_repo_content` writes a “Repository Structure” header, then iterates twice over `Path.rglob("*")`: first to emit the indented tree, second to embed file contents wrapped in `<file path="…">` tags. Errors while reading files are captured and logged inline.  

**Data flow** – Input: optional `output_file` name, ignore list. Output: a UTF‑8 text file containing the tree and file bodies. Side‑effects: filesystem reads and a single write operation. 
<a name="logger-instantiation-flow"></a>
## Logger instantiation flow  

1. **Import logging symbols** – `BaseLogger`, `BaseLoggerTemplate`, `InfoLog`, `ErrorLog`, `WarningLog` are pulled from `autodocgenerator.ui.logging`.  
2. **Create BaseLogger** – `logger = BaseLogger()` constructs the core logger object, initializing internal handlers (e.g., Rich console).  
3. **Attach concrete template** – `logger.set_logger(BaseLoggerTemplate())` injects a concrete formatting template, defining how messages are rendered (color, level prefixes).  

The instantiated `logger` is a module‑level variable, exported as part of the package’s public API, so downstream code can simply `from autodocgenerator import logger` and start logging. 
<a name="logging-and-model-interaction"></a>## Logging and Model Interaction  
All public functions instantiate **`BaseLogger`** locally, emitting `InfoLog` messages at start, completion, and (optionally) detailed debug level 1. Model calls are performed via `model.get_answer_without_history`, guaranteeing stateless queries. Input assumptions include well‑formed Markdown anchors, valid `Model` instances, and non‑empty `custom_description` strings. Outputs are plain strings (links list, introductions, or custom descriptions) ready for downstream concatenation or insertion into the final `output_doc.md`. 
<a name="logging-hierarchy"></a>
## `BaseLogger` & log‑record classes – unified logging façade  

**Responsibility** – Provides a process‑wide singleton (`BaseLogger`) that forwards `BaseLog`‑derived messages to a configurable `BaseLoggerTemplate`. The hierarchy (`ErrorLog`, `WarningLog`, `InfoLog`) supplies level‑aware formatting with a timestamp prefix.  

**Interactions** – Other UI components (e.g. doc‑generation orchestrators) call `BaseLogger().log(<Log>)`. The logger delegates to the attached template (`FileLoggerTemplate` for file output or the default `BaseLoggerTemplate` for console). No external state is read; only the optional file is written.  

**Technical Details**  
* `BaseLog` stores `message` and `level`; `format()` returns the raw text.  
* Sub‑classes override `format()` to prepend `[_log_prefix] [LEVEL]`.  
* `_log_prefix` builds a human‑readable timestamp from `time.time()`.  
* `BaseLoggerTemplate` implements `global_log()` that respects the instance’s `log_level` filter.  
* `FileLoggerTemplate` overrides `log()` to append formatted lines to a file.  
* `BaseLogger.__new__` enforces a single shared instance (`cls.instance`).  

**Data Flow** – *Input*: a `BaseLog` instance (message + level). *Output*: side‑effect → `print()` or file write via the selected template. The method returns `None`.  

--- 
<a name="basefactory‑orchestrator"></a>  
## BaseFactory – Document Assembly Orchestrator  

**Responsibility** – Collects a configurable list of `BaseModule` subclasses, invokes each module’s `generate` method, concatenates their outputs, and reports progress.  

**Interactions** – Instantiated by the UI layer (e.g., `run_file.py`). Receives a concrete `Model` (sync or async) and a `BaseProgress` implementation. Each module may call the model’s `get_answer` APIs, while `BaseFactory` logs every step through a shared `BaseLogger`.  

**Technical Details**  
- `BaseModule` is an abstract base class defining `generate(info: dict, model: Model)`.  
- `DocFactory.__init__(*modules)` stores the supplied modules in `self.modules`.  
- `generate_doc(info, model, progress)` creates a sub‑task, iterates over `self.modules`, concatenates `module_result` with double line breaks, logs success (`InfoLog`) and verbose output (`level=2`), updates the progress bar, then removes the sub‑task.  

**Data Flow**  
```
info dict → each module.generate → model.get_answer (optional) → string fragment
→ DocFactory aggregates → final documentation string
```
Side effects: history updates inside the model, log file writes, and UI progress updates. 
<a name="custom‑module‑generation"></a>  
## CustomModule & CustomModuleWithOutContext – Tailored Intro Generation  

**Responsibility** – Produce a custom description block either with or without the source‑code context.  

**Interactions** – Both classes inherit `BaseModule`; they call post‑processor helpers `generete_custom_discription` / `generete_custom_discription_without`, passing the split source (`split_data`) and the shared `Model`.  

**Technical Details**  
- Constructor stores `self.discription`.  
- `generate` extracts `info["code_mix"]` (or skips it) and `info["language"]`, then delegates to the appropriate helper.  
- Returns the raw string produced by the helper.  

**Data Flow**  
```
info → split_data (max 5000 symbols) → generete_custom_discription → model.get_answer → description string
```
or, without context, directly `generete_custom_discription_without`. 
<a name="doc‑generation‑orchestrator"></a>  
## Orchestrator (`gen_doc` in run_file.py)

`gen_doc` wires together the core engine:

1. **Model layer** – creates a synchronous `GPTModel` and an asynchronous `AsyncGPTModel` using the global `API_KEY`.  
2. **Manager** – instantiated with the target `project_path`, the parsed `Config`, both model instances, and a console‑based progress bar (`ConsoleGtiHubProgress`). The manager centralises file scanning, caching, and doc assembly.  
3. **Pipeline** –  
   * `manager.generate_code_file()` – extracts source files respecting `Config.ignore_files`.  
   * `manager.generete_doc_parts(max_symbols=structure_settings.max_doc_part_size)` – splits generated text into manageable chunks.  
   * `manager.factory_generate_doc(DocFactory(*custom_modules))` – runs user‑defined modules through the `DocFactory`.  
   * Conditional steps based on `StructureSettings`: ordering (`manager.order_doc()`) and intro links (`DocFactory(IntroLinks())`).  
   * `manager.clear_cache()` – removes temporary artifacts, keeping the bootstrap lightweight.  
4. Returns the final document via `manager.read_file_by_file_key("output_doc")`.

--- 
<a name="factory-doc-assembly"></a>  
## Factory‑Based Document Assembly  

`factory_generate_doc(doc_factory)`  
- Loads current `output_doc` and `code_mix`.  
- Builds `info` dict (`language`, `full_data`, `code_mix`).  
- Logs the module list and input sizes.  
- Executes `doc_factory.generate_doc(info, sync_model, progress_bar)` – the orchestrator that runs each `BaseModule`.  
- Prepends the new fragment to the existing document and writes back. 
<a name="intro‑modules‑link‑and‑text"></a>  
## IntroLinks & IntroText – Automatic Intro Construction  

**Responsibility** – Create introductory sections: a list of HTML links (`IntroLinks`) and a natural‑language overview (`IntroText`).  

**Interactions** – Both modules pull data from `info` (`full_data` or `global_data`), invoke post‑processor utilities (`get_all_html_links`, `get_links_intro`, `get_introdaction`) which internally query the provided `Model`.  

**Technical Details**  
- `IntroLinks.generate` → `get_all_html_links` → `get_links_intro(model, language)`.  
- `IntroText.generate` → `get_introdaction(model, language)`.  
- Each returns a ready‑to‑insert markdown/HTML fragment.  

**Data Flow**  
```
info → extractor (links or global data) → post‑processor → model.get_answer → intro fragment
```
All fragments are later concatenated by `BaseFactory`. 
None 
<a name="inter‑module‑interactions"></a>  
## Inter‑module Interactions  

* Both wrappers import `ModelExhaustedException` (raised when no fallback model remains).  
* Logging relies on `BaseLogger` and concrete `InfoLog/WarningLog/ErrorLog` objects from the UI layer.  
* The concrete models are consumed by the **engine** (e.g., `run_file.py`’s `gen_doc`) which injects them into the `Manager` for document generation.  

**Data flow**  
```
User prompt → Model.get_answer / AsyncModel.get_answer
   ↳ History updated (user → assistant)
   ↳ generate_answer → Groq/AsyncGroq → chat_completion
   ↳ result returned → History records assistant reply
```

All side effects are confined to `self.history` and log file emission (controlled by `ProjectBuildConfig`). This fragment therefore provides the core LLM request/response loop, with deterministic fallback and full traceability for both synchronous and asynchronous execution paths. 
<a name="manager-class-usage"></a>!noinfo 
<a name="manager-orchestration"></a>  
## Manager – Orchestration of Project Pipeline  

**Responsibility** – Coordinates the end‑to‑end doc‑generation workflow for a given project directory: prepares cache, creates a mixed source view, drives part‑wise or factory‑based documentation, and finally orders the sections.  

**Interactions** – Instantiated by the CLI (`run_file.py`). Receives a `Config`, optional `Model`/`AsyncModel`, and a `BaseProgress` implementation. It logs via `BaseLogger`, writes files to `<project>/.auto_doc_cache`, and updates the UI progress bar after each step. 
<a name="assumptions-and‑constraints"></a>
## Assumptions and constraints  

- The logging classes must be importable; any failure in `autodocgenerator.ui.logging` will raise an `ImportError` and abort package import.  
- The environment must support Rich’s terminal capabilities; otherwise, fallback rendering may occur but the “ADG” banner will still print.  

By centralising logger creation here, the package guarantees a uniform logging experience across all components while keeping the bootstrap lightweight. 
<a name="cache-and-path-resolution"></a>  
## Cache Management & File Path Resolution  

- `CACHE_FOLDER_NAME` designates the hidden cache folder.  
- `FILE_NAMES` maps logical keys (`code_mix`, `global_info`, `logs`, `output_doc`) to concrete filenames.  
- `get_file_path(key)` builds an absolute path inside the cache; `read_file_by_file_key` returns its contents.  
- Constructor creates the cache directory if absent and attaches a `FileLoggerTemplate` to `BaseLogger`. 
<a name="data‑flow-and‑side‑effects"></a>
## Data flow, inputs, and side effects  

- **Input**: No external parameters; the only implicit input is the environment’s standard output stream.  
- **Output**: The literal string “ADG” is written to stdout; log records are emitted to the console (or configured Rich handlers).  
- **Side effects**: Global state mutation – the module‑level `logger` object becomes available for import, and the console receives the “ADG” banner. This side effect is intentional to give immediate visual feedback that the Auto Doc Generator package has been loaded. 
<a name="split-data"></a>
## `split_data` – token‑aware chunking of source text  

**Responsibility** – Breaks a single string into a list of fragments whose length does not exceed `max_symbols`. It first splits on newline, repeatedly bisects any piece longer than 1.5 × `max_symbols`, then recombines pieces while respecting a 1.25 × `max_symbols` limit to keep chunks balanced.  

**Interactions** – Uses `BaseLogger` to emit start/finish messages; no external state is read or written.  

**Data Flow** – *Input*: `data: str`, `max_symbols: int`. *Output*: `list[str]` of ready‑for‑LLM chunks. Side‑effects are limited to logged messages. 
<a name="yaml‑to‑runtime‑objects"></a>  
## YAML → Runtime Objects (ConfigReader)

The `read_config` function is the entry point for translating a user‑supplied `autodocconfig.yml` into three ready‑to‑use objects:

* **`Config`** – holds global ignore patterns, language, project name and a `ProjectBuildConfig` instance.  
* **`custom_modules`** – a list of `CustomModule` or `CustomModuleWithOutContext` built from the `custom_descriptions` section; the leading “%” marker selects the context‑less variant.  
* **`StructureSettings`** – controls how the final documentation is sliced (`max_doc_part_size`) and whether intro links or ordering are injected.

The function:
1. Loads YAML via `yaml.safe_load`.  
2. Instantiates `Config` and populates ignore patterns, language, and project metadata.  
3. Creates a `ProjectBuildConfig`, applies any build‑time flags (e.g., `save_logs`, `log_level` – the package’s uniform logging knobs), and attaches it to `Config`.  
4. Iterates over `ignore_files` and `project_additional_info` to extend the `Config` state.  
5. Maps `custom_descriptions` to the appropriate module class.  
6. Initializes `StructureSettings` with defaults (`include_intro_links=True`, `include_order=True`, `max_doc_part_size=5_000`) and overrides them from the YAML block.

Outputs are returned as a tuple, ready for the runner.

--- 
<a name="asyncgptmodel‑async‑wrapper"></a>  
## AsyncGPTModel – Asynchronous LLM Wrapper  

Mirrors `GPTModel` but uses **AsyncGroq** (`self.client = AsyncGroq(...)`) and async‑compatible methods.  

* `generate_answer` is declared `async`; all internal steps are identical to the sync version, except the `await` on `self.client.chat.completions.create`.  
* Logging, fallback handling, and result extraction are unchanged, ensuring parity between sync and async pipelines. 
<a name="gptmodel‑sync‑wrapper"></a>  
## GPTModel – Synchronous LLM Wrapper  

Derived from `Model`, `GPTModel` binds a **Groq** client (`self.client = Groq(api_key=self.api_key)`) and a `BaseLogger`.  

**Key flow (`generate_answer`)**  
1. Log start (`InfoLog`).  
2. Resolve `messages` from `self.history.history` or an explicit `prompt`.  
3. Loop over `self.regen_models_name` until a successful completion:  
   * Attempt `self.client.chat.completions.create(messages=messages, model=model_name)`.  
   * On exception, log a warning and advance `self.current_model_index` (wrap‑around).  
   * If the list is empty, raise `ModelExhaustedException`.  
4. Extract `result = chat_completion.choices[0].message.content`.  
5. Log the model used and the raw answer (verbosity level 2).  
6. Return `result`.  

`get_answer` enriches the history before and after the call, providing a convenient one‑step query interface. 
<a name="history‑prompt‑buffer"></a>  
## History – Prompt Context Buffer  

`History` initialises with the system prompt (`BASE_SYSTEM_TEXT`).  
* `self.history` holds a list of `{role, content}` dicts.  
* `add_to_history` appends new entries, used by the higher‑level `Model`/`AsyncModel` APIs to record user and assistant turns.  
* Exposed to callers via `Model.get_answer` and `AsyncModel.get_answer`, enabling multi‑turn interactions. 
<a name="CONTENT_DESCRIPTION"></a>` tag with strict content rules (no filenames, extensions, generic terms, or URLs). This ensures a clean, tag‑driven snippet suitable for anchor‑based navigation. 
<a name="anchor-based-chunk-extraction"></a>  
## Anchor‑Based Chunk Extraction  

**Responsibility** – Parses a Markdown document, isolates sections that begin with a well‑formed `<a name="…"></a>` anchor, and returns a mapping **anchor → raw section text**.  

**Interactions** – Consumes raw Markdown (e.g., the generated `output_doc.md`) and supplies the dictionary to the *semantic sorter* (`get_order`). No external state is touched; the function is pure.  

**Technical details** –  
* `extract_links_from_start` scans each chunk’s first line with regex `^<a name=["']?(.*?)["']?</a>`; anchors longer than five characters become `#anchor`.  
* `split_text_by_anchors` uses a look‑ahead split (`(?=<a name=…>)`) to create chunks, trims whitespace, validates a 1‑to‑1 anchor‑chunk relationship, and builds the result dict.  
* Returns `None` on mismatch, allowing callers to abort safely.  

**Data flow** – Input: full Markdown string. Output: `dict[str, str]` where keys are `#anchor` strings and values are the associated section bodies. Side‑effects: none. 
<a name="custom-description-synthesis"></a>## Custom Description Synthesis  
`generete_custom_discription` iterates over pre‑split documentation chunks. For each chunk it assembles a detailed system‑role prompt, embeds the chunk as context, adds **`BASE_CUSTOM_DISCRIPTIONS`**, and asks the model to describe a user‑provided `custom_description`. It stops on the first non‑error response (absence of “!noinfo”/“No information found”).  
`generete_custom_discription_without` skips the context step and forces the model to prepend a single ` 
<a name="doc‑chunk‑behaviour"></a>  
## Documentation Chunk Behaviour (`StructureSettings`)

* `include_intro_links` – injects a generated table‑of‑contents block (`IntroLinks`) at the document head.  
* `include_order` – sorts generated parts to respect source file order, improving readability.  
* `max_doc_part_size` – caps the character count of each generated segment; the manager respects this when calling `generete_doc_parts`.

Together these settings give developers fine‑grained control over the size, ordering, and navigation of the auto‑generated documentation while the underlying logging remains consistent across all modules. 
<a name="document-ordering"></a>  
## Document Ordering & Cleanup  

`order_doc()` splits the final markdown by anchor tags (`split_text_by_anchors`), asks the model for the correct sequence via `get_order`, and overwrites `output_doc.md`.  

`clear_cache()` removes the log file unless `config.pbc.save_logs` is true.  

**Data Flow Summary**  

```
project_dir → Manager init → cache files
→ CodeMix → code_mix.txt
→ gen_doc_parts / DocFactory → output_doc.md
→ split_text_by_anchors → get_order → reordered output_doc.md
``` 
<a name="generate-descriptions"></a>
## `generate_describtions_for_code` – LLM‑driven API documentation generator  

**Responsibility** – For each code snippet, asks the LLM to produce a markdown‑formatted description following strict guidelines (components, parameters, usage example).  

**Interactions** – Builds a fixed system prompt, adds the code as user content, calls `model.get_answer_without_history`, and tracks progress via `BaseProgress`.  

**Output** – List of description strings matching the order of `data`.

--- 
<a name="gen-doc-parts"></a>
## `gen_doc_parts` – orchestrator for synchronous batch documentation  

**Responsibility** – Splits the full source code via `split_data`, then iteratively calls `write_docs_by_parts` for each chunk, concatenating results. Keeps a sliding window of the last 3000 characters as context for the next call.  

**Interactions** – Creates a `BaseProgress` sub‑task, updates it per chunk, and logs overall progress.  

**Data Flow** – *Inputs*: `full_code_mix`, `max_symbols`, `model`, `language`, `progress_bar`. *Output*: single markdown string containing the entire documentation. Side‑effects: progress‑bar mutation and logging. 
<a name="html-link-extraction-logic"></a>## HTML Link Extraction Logic  
The function **`get_all_html_links`** scans a documentation string for Markdown‑style anchor tags (`<a name="…"></a>`). Using a compiled regex it captures the anchor name, prefixes it with “#”, and returns a list of link fragments. Logging via **`BaseLogger`** reports start, count, and the raw list (verbosity 1). The routine assumes anchors longer than five characters are meaningful and ignores shorter matches. 
<a name="link-based-introduction-generation"></a>## Link‑Based Introduction Generation  
**`get_links_intro`** builds a three‑message prompt for a **`Model`** (typically a `GPTModel`). System messages enforce language and inject the constant **`BASE_INTRODACTION_CREATE_LINKS`**; the user message supplies the extracted links. The model’s response (a prose introduction containing those links) is returned after logging the operation. The function is language‑agnostic, defaulting to English. 
<a name="plain-introduction-synthesis"></a>## Plain Introduction Synthesis  
**`get_introdaction`** (note the historic typo) follows the same prompt pattern but uses **`BASE_INTRO_CREATE`** and feeds the full documentation (`global_data`). The model returns a standalone introductory paragraph, which the caller integrates elsewhere. 
<a name="parentmodel‑shared‑state"></a>  
## ParentModel – Shared Model State  

`ParentModel` centralises configuration for every LLM client.  
* **Constructor arguments** – `api_key`, optional `History` object, `use_random` flag.  
* **State built** –  
  * `self.history` stores the rolling conversation.  
  * `self.api_key` propagates to concrete clients.  
  * `self.regen_models_name` is a shuffled (if `use_random`) copy of the global `MODELS_NAME` list, defining the fallback order when a model fails.  
  * `self.current_model_index` tracks the active candidate.  

The class is inherited by both sync (`Model`) and async (`AsyncModel`) wrappers, guaranteeing identical fallback logic across execution modes. 
<a name="progress-implementations"></a>
## `BaseProgress` & concrete progress reporters – task progress visualisation  

**Responsibility** – Defines a minimal progress‑tracking contract (`create_new_subtask`, `update_task`, `remove_subtask`). Concrete classes implement visual feedback for either Rich‑based terminal bars (`LibProgress`) or plain console prints (`ConsoleGtiHubProgress`).  

**Interactions** – Documentation generators instantiate a progress object and invoke the three methods around each chunk‑processing step. No shared mutable state beyond the Rich `Progress` instance or internal `ConsoleTask` objects.  

**Technical Details**  
* `LibProgress` wraps `rich.progress.Progress`; maintains a base task (`_base_task`) and a current sub‑task (`_cur_sub_task`). Updating advances the appropriate task.  
* `ConsoleTask` prints a start banner and a percentage on each `progress()` call.  
* `ConsoleGtiHubProgress` composes a permanent “General Progress” `ConsoleTask` and creates per‑chunk `ConsoleTask`s on demand. `update_task()` delegates to the active sub‑task or the general one.  
* Both concrete classes inherit from the empty `BaseProgress` stub, ensuring a consistent API.  

**Data Flow** – *Inputs*: `name` (string) and `total_len` (int) for sub‑task creation; subsequent calls receive no arguments. *Outputs*: visual side‑effects on stdout (Rich bar or console prints). Internally, task identifiers are stored to allow incremental updates and later removal.  

---  

These two modules together supply the UI layer’s logging and progress reporting facilities, enabling the higher‑level documentation pipeline to emit timestamped diagnostics and user‑visible progress without coupling to a specific output medium. 
<a name="semantic-title-ordering"></a>  
## Semantic Title Ordering  

**Responsibility** – Sends the extracted anchor titles to the LLM (`Model.get_answer_without_history`) and reassembles the document in the LLM‑proposed order.  

**Interactions** – Receives the anchor‑to‑section map from the extractor, logs progress via `BaseLogger`, and calls the **stateless** LLM endpoint (`model.get_answer_without_history`).  

**Technical details** –  
* Constructs a user‑role prompt asking the model to “Sort the following titles semantically … Return ONLY a comma‑separated list … leave # in title”.  
* Parses the comma‑separated response, trims entries, and iterates over the ordered list, concatenating the corresponding chunk text (`order_output`).  
* Detailed logging at three verbosity levels records input keys, raw chunk dict, and per‑chunk inclusion.  

**Data flow** – Input: `Model` instance, `dict[anchor, chunk]`. Output: single string containing the reordered document sections, ready for final concatenation. No file I/O occurs here. 
<a name="sync-doc-part-generation"></a>  
## Synchronous Documentation Part Generation  

`generete_doc_parts(max_symbols=5_000)`  
- Reads the previously stored `code_mix`.  
- Calls `gen_doc_parts(full_code_mix, max_symbols, sync_model, config.language, progress_bar)` which splits the mix, queries the model, and streams partial docs.  
- Persists the assembled output to `output_doc.md` and updates progress. 
<a name="write-autodocfile-options"></a>
The file is a simple key‑value list written in YAML.  
Top‑level keys define the project and its behavior:

- **project_name** – a short title for the documentation generator.  
- **language** – language code for generated text (e.g., “en”).

A **build** block controls execution details:
- **save_logs** – true/false to keep the generation log.  
- **log_level** – numeric level (higher means more detail).

A **structure** block influences how the output is organized:
- **include_intro_links** – include navigation links at the beginning.  
- **include_order** – keep sections in the order they appear in the source.  
- **max_doc_part_size** – maximum character count for each generated piece.

An **additional_info** block can hold free‑form data, such as a global description of the project.

A **custom_descriptions** list allows you to add specific prompts that the generator will answer, for example instructions on installation, how to write this file, or how to use particular classes. 
<a name="write-docs-by-parts"></a>
## `write_docs_by_parts` – synchronous single‑part documentation generation  

**Responsibility** – Constructs a system‑prompt (including language, part ID, optional previous output) and calls `model.get_answer_without_history` to obtain a markdown description for one code fragment. Trims surrounding markdown fences before returning.  

**Interactions** – Relies on `BASE_PART_COMPLITE_TEXT`, `BaseLogger`, and the synchronous `Model` interface.  

**Data Flow** – *Inputs*: `part_id`, `part`, `model`, optional `prev_info`, `language`. *Output*: cleaned LLM answer (`str`). Logs request/response sizes. 
<a name="async-gen-doc-parts"></a>
## `async_gen_doc_parts` – parallel orchestrator for asynchronous batch documentation  

**Responsibility** – Mirrors `gen_doc_parts` but launches an `async_write_docs_by_parts` task per chunk, limited by a semaphore of size 4, and aggregates the async results with `asyncio.gather`.  

**Interactions** – Uses the same `BaseProgress` API (sub‑task creation, per‑task updates, removal), the shared semaphore, and the asynchronous `AsyncModel`.  

**Data Flow** – *Inputs*: `full_code_mix`, `global_info`, `max_symbols`, `model`, `language`, `progress_bar`. *Output*: concatenated markdown documentation (`str`). Logs start/end and total length. 
<a name="async-write-docs-by-parts"></a>
## `async_write_docs_by_parts` – concurrent part processing  

**Responsibility** – Same logical work as `write_docs_by_parts` but runs inside an `asyncio.Semaphore` to limit parallel requests. Calls `async_model.get_answer_without_history` and optionally invokes `update_progress`.  

**Interactions** – Accepts a shared `semaphore` object, uses `BaseLogger`, and expects an `AsyncModel` that implements an async `get_answer_without_history`.  

**Data Flow** – *Inputs*: `part`, `async_model`, `global_info`, `semaphore`, optional `prev_info`, `language`, `update_progress`. *Output*: trimmed answer (`str`). Emits progress callbacks and logs. 
<a name="async-compress"></a>
## `async_compress` – semaphore‑protected async compression  

**Responsibility** – Performs the same LLM call as `compress` but within an `asyncio.Semaphore` to limit concurrency and updates the async progress bar.  

**Interactions** – Awaits `AsyncModel.get_answer_without_history`; updates `BaseProgress`.  

**Flow** – Build prompt (identical to `compress`), `await model.get_answer_without_history`, then `progress_bar.update_task()`.

**Data** – Input: `data: str`, `project_settings`, `model: AsyncModel`, `compress_power`, `semaphore`, `progress_bar`.  
Output: `str` compressed answer.

--- 
<a name="async-compress-and-compare"></a>
## `async_compress_and_compare` – parallel batch compression  

**Responsibility** – Dispatches `async_compress` for every element in `data` (default concurrency = 4), gathers results, then re‑chunks them into groups of `compress_power`.  

**Interactions** – Creates an `asyncio.Semaphore(4)`, populates `tasks`, awaits `asyncio.gather`, uses `BaseProgress` for a sub‑task.  

**Result** – Returns `list[str]` where each entry is a newline‑joined group of compressed chunks.

--- 
<a name="compress-and-compare-sync"></a>
## `compress_and_compare` – batch sync compression  

**Responsibility** – Groups input files into chunks of size `compress_power`, compresses each file with `compress`, concatenates results per chunk, and reports progress.  

**Interactions** – Uses `BaseProgress` to create/update a sub‑task; repeatedly calls `compress`.  

**Logic** –  
* Allocate result list sized to `ceil(len(data)/compress_power)`.  
* Loop over `data`, compute `curr_index = i // compress_power`, append each `compress` result plus newline.  
* Update progress bar each iteration, then remove sub‑task.  

**Data** – Input: `data: list[str]`, `model`, `project_settings`, `compress_power`, `progress_bar`.  
Output: `list[str]` where each element contains the concatenated compressed chunk.

--- 
<a name="compress-single-pass"></a>
## `compress` – single‑pass LLM compression  

**Responsibility** – Sends a raw code string to the LLM together with the project‑wide system prompt and a size‑adjusted compression prompt, returning the model’s answer.  

**Interactions** – Calls `Model.get_answer_without_history`. No filesystem or network side‑effects other than the LLM request.  

**Technical flow** –  
1. Build `prompt` list (`system` → project prompt, `system` → base compress text, `user` → `data`).  
2. Invoke `model.get_answer_without_history(prompt=prompt)`.  
3. Return the answer string.  

**Data** – Input: `data: str`, `project_settings: ProjectSettings`, `model: Model`, `compress_power: int`.  
Output: compressed `str`. No mutation of arguments.

--- 
<a name="compress-to-one"></a>
## `compress_to_one` – iterative reduction to a single summary  

**Responsibility** – Repeatedly compresses the list of strings until only one element remains, optionally using the async path.  

**Interactions** – Calls either `compress_and_compare` or `async_compress_and_compare` inside a `while len(data) > 1` loop; updates a `BaseProgress` sub‑task each iteration.  

**Data** – Input: `data: list[str]`, `model`, `project_settings`, `compress_power`, `use_async`, `progress_bar`.  
Output: final aggregated string (`data[0]`).

--- 
<a name="code-mix-generation"></a>  
## Code Mix Generation Workflow  

`generate_code_file()`  
1. Logs start.  
2. Instantiates `CodeMix(project_directory, config.ignore_files)`.  
3. Calls `build_repo_content` → writes a concatenated source snapshot to `code_mix.txt`.  
4. Logs completion and advances the progress bar. 
