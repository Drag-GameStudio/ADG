**Project Overview – Auto‑Doc Generator**  

---

### 1. Project Title  
**Auto‑Doc Generator** – A layered, orchestrated pipeline that creates a complete `README.md` (or any markdown documentation) from a source‑code repository by automatically chunking the code, prompting a large‑language model (LLM) for descriptive fragments, post‑processing the results, and enriching the output with vector embeddings.

---

### 2. Project Goal  
Develop a **hands‑free documentation tool** that can be run locally or as a GitHub Action.  
The software scans a repository, compresses and splits the source into manageable fragments, asks a Groq‑hosted LLM to produce markdown snippets for each fragment, optionally re‑orders those snippets using embeddings, caches intermediate results, and finally emits a polished `README.md`.  

The tool solves two recurring problems for developers and CI pipelines:

1. **Manual, out‑of‑date documentation** – documentation is generated directly from the current state of the code base, ensuring it never lags behind.  
2. **Time‑consuming, error‑prone doc writing** – the LLM handles the natural‑language summarisation while the pipeline guarantees reproducibility, caching and progress reporting.

---

### 3. Core Logic & Principles  

| Layer / Component | Responsibility | Core Principle |
|-------------------|----------------|----------------|
| **Entry (CLI / Action)** `autodocgenerator.auto_runner.run_file.__main__` | Parses `autodocconfig.yml`, builds configuration objects, creates the central **Manager**, and starts the pipeline. | Single entry point –‑ deterministic start‑up, works both locally (`python -m …`) and in CI. |
| **Orchestrator** `autodocgenerator.manage.Manager` | Holds `Config`, `CacheSettings`, LLM (`GPTModel`), embedding service, UI (logger & progress), and coordinates every stage. | Centralised state machine –‑ all shared objects flow through the manager, enabling incremental runs via cache. |
| **Pre‑processor** | • `CodeMix.build_repo_content()` – walks the repo, applies ignore patterns, builds a single string with file‑level markers. <br>• `compressor.compress_to_one()` – optional global summarisation. <br>• `spliter.split_data()` – chops the huge string into `≤ max_symbols` chunks. | *Chunk‑first, compress‑later* –‑ ensures the LLM never receives payloads larger than the provider limits while keeping context boundaries. |
| **Engine (LLM Wrapper)** `engine.models.gpt_model.{GPTModel, AsyncGPTModel}` | Thin wrapper around the Groq API exposing `ask` / `ask_async`. Handles multiple API keys, model fallback and request history. | Provider‑agnostic interface –‑ the rest of the code only needs `ask(prompt)`. |
| **Factory** `factory.base_factory.DocFactory` + concrete `BaseModule` subclasses | Plug‑in system that creates additional markdown sections (intro, custom modules, link tables, etc.). Each module receives the shared `info` object and the LLM instance, returns a markdown fragment. | Extensibility –‑ new documentation pieces are added by implementing a subclass and exposing it in the YAML config. |
| **Post‑processor** | • `postprocessor.custom_intro` – generates a custom introductory block. <br>• `postprocessor.sorting` – extracts anchors, asks the LLM for a CSV ordering, optionally re‑orders via vector similarity. | *Semantic ordering* –‑ the final document follows a logical flow rather than raw chunk order. |
| **Embedding Layer** `postprocessor.embedding.Embedding` | Calls the Google Gemini embedding API, stores a dense vector on each `DocContent`. The vectors are later used to compute similarity to a root vector for ordering. | Content‑driven similarity –‑ sections that talk about the same concept appear together. |
| **Schema / Cache** | Pydantic models (`CacheSettings`, `DocHeadSchema`, `DocContent`) persisted as `.auto_doc_cache_file.json`. | Incremental builds –‑ if the repository has not changed, the manager re‑uses cached fragments, saving API calls and time. |
| **UI** `ui.progress_base.ConsoleGitHubProgress` & `ui.logging.BaseLogger` | Console progress bar (Rich‑compatible) and structured logging (debug / info / error). | Visibility –‑ users see real‑time progress and detailed logs, both locally and in CI. |
| **Config** `config.config.Config` & `engine.config` constants | Holds global settings, environment‑variable validation (`GROQ_API_KEYS`, `GOOGLE_EMBEDDING_API_KEY`, `GITHUB_EVENT_NAME`), prompt templates, thresholds, feature flags. | Centralised, declarative configuration –‑ all behaviour can be toggled from `autodocconfig.yml`. |

#### Functional Flow (high‑level)

1. **Initialisation** – CLI reads the YAML, validates env‑vars, builds a `Config` object and instantiates `Manager`.  
2. **Git status check** – `Manager.check_git_status()` decides whether a fresh run is required (based on the last processed commit stored in `CacheSettings`).  
3. **Source aggregation** – `CodeMix` creates a single markdown‑ish representation of the repo (`CacheSettings.code_mix`).  
4. **Optional global compression** – `compressor.compress_to_one` summarises the whole repo into a “global info” chunk (`CacheSettings.global_info`).  
5. **Chunking** – `split_data` produces size‑bounded fragments. Each fragment is sent to the LLM (`GPTModel.ask`) and the returned markdown is stored as a `DocContent` in `DocHeadSchema`.  
6. **Factory‑driven sections** – All `BaseModule` subclasses (intro, custom links, user‑defined modules) generate additional markdown fragments that are merged into the same schema.  
7. **Ordering** – If enabled, the LLM is asked to propose a CSV order of section titles; anchors are extracted and, optionally, a vector‑based similarity sort refines the order.  
8. **Embedding** – Each `DocContent` is vectorised via the Google Embedding API; vectors are kept in memory and can be persisted for downstream tooling.  
9. **Cache clean‑up** – Mutable temporary fields in `CacheSettings` are cleared to keep the cache file small.  
10. **Persist output** – `Manager.save()` writes the final markdown to `.auto_doc_cache/output_doc.md` and updates the JSON cache; a CI step may copy the file to the repository root as `README.md`.  

All stages read and write to the shared `CacheSettings` and `DocHeadSchema` objects, guaranteeing a single source of truth throughout the run.

---

### 4. Key Features  

- **Full‑repo scan** with configurable ignore patterns (files, directories, extensions).  
- **Automatic chunking** respecting a maximum token / symbol limit for LLM calls.  
- **LLM‑driven summarisation** using Groq‑hosted models; supports key rotation and model fallback.  
- **Plug‑in factory** for custom markdown modules (intro, link tables, user‑defined sections).  
- **Optional global compression** to produce an overarching project description.  
- **Semantic re‑ordering** via LLM‑generated CSV ordering and optional vector‑similarity sorting.  
- **Embedding generation** with Google Gemini embedding API; vectors stored per section for future retrieval or similarity search.  
- **Caching layer** (`.auto_doc_cache_file.json`) that stores intermediate results, enables incremental builds, and reduces API usage.  
- **CLI & GitHub Action** entry points –‑ one command works both locally and in CI pipelines.  
- **Progress & logging UI** (Rich‑based progress bar, structured logger) for transparent execution.  
- **Extensible architecture** –‑ add new sections by subclassing `BaseModule`; swap LLM or embedding providers by implementing the same interface.  

---

### 5. Dependencies  

| Category | Packages | Purpose |
|----------|----------|---------|
| **Core runtime** | `python >=3.9` | Primary interpreter. |
| **LLM access** | `groq` (or the underlying HTTP client) | Calls the Groq LLM API (`ask`, `ask_async`). |
| **Embedding** | `google-generativeai` (Gemini embedding endpoint) | Generates 768‑dimensional vectors for each markdown fragment. |
| **Data models & validation** | `pydantic` | Typed schemas (`CacheSettings`, `DocHeadSchema`, `DocContent`). |
| **CLI framework** | `cleo` (or `typer`) | Provides the `python -m autodocgenerator.auto_runner.run_file` command interface. |
| **Progress & logging** | `rich` | Console progress bar and colourful logs. |
| **File system utilities** | `pathlib`, `yaml` (`PyYAML`) | Reads `autodocconfig.yml`, traverses the repository. |
| **HTTP / async support** | `httpx` (optional, used by Groq wrapper) | Async requests to the LLM API. |
| **Testing (optional)** | `pytest`, `pytest-mock` | Unit‑test suite for the pipeline. |
| **CI integration** | No additional packages; the entry point is invoked from a reusable GitHub Action workflow (`reuseble_agd.yml`). |

*All dependencies are pure‑Python and available on PyPI. The project can be installed via a standard `pip install -e .` after cloning the repository.*

---

**In summary**, the Auto‑Doc Generator is a modular, cache‑aware pipeline that turns any source‑code repository into a high‑quality markdown documentation file with minimal human effort. Its layered architecture, clear separation of concerns, and plug‑in points make it easy to adapt to new LLM providers, embedding services, or custom documentation sections.
## Executive Navigation Tree
- 📂 Initialization
  - [init-welcome](#init-welcome)
  - [git-status-evaluation](#git-status-evaluation)
  - [configuration-parsing](#configuration-parsing)
  - [projectsettings-class](#projectsettings-class)
  - [pyproject-toml](#pyproject-toml)
  - [autodoc-setup-options](#autodoc-setup-options)

- ⚙️ Installation
  - [install-script](#install-script)
  - [install-sh](#install-sh)
  - [install-workflow-setup](#install-workflow-setup)

- 📂 Manager
  - [manager-class](#manager-class)
  - [manager-init-folder-system](#manager-init-folder-system)
  - [manager-class-usage](#manager-class-usage)

- 📂 Custom Modules
  - [custom-modules-implementation](#custom-modules-implementation)
  - [intro-modules-implementation](#intro-modules-implementation)

- 📂 Model
  - [model-base](#model-base)
  - [base-module-interface](#base-module-interface)
  - [gptmodel-construction](#gptmodel-construction)
  - [gptmodel-generate-answer](#gptmodel-generate-answer)

- 📂 Embedding
  - [embedding-class](#embedding-class)
  - [embedding-ordering](#embedding-ordering)
  - [vector-sort-helpers](#vector-sort-helpers)
  - [get-order](#get-order)

- 📂 Generation
  - [generate-code-file](#generate-code-file)
  - [generate-global-info](#generate-global-info)
  - [doc-factory-constructor](#doc-factory-constructor)
  - [doc-factory-generate-doc](#doc-factory-generate-doc)
  - [factory-generate-doc](#factory-generate-doc)
  - [gen_doc-function](#gen_doc-function)
  - [gen_doc-logic-flow](#gen_doc-logic-flow)
  - [gen_doc-data-contract](#gen_doc-data-contract)
  - [gen-doc-parts](#gen-doc-parts)
  - [generete-doc-parts](#generete-doc-parts)
  - [write-docs-by-parts](#write-docs-by-parts)
  - [custom-description-loop](#custom-description-loop)
  - [standalone-custom-description](#standalone-custom-description)
  - [CONTENT_DESCRIPTION](#CONTENT_DESCRIPTION)
  - [global-intro-generation](#global-intro-generation)
  - [link-intro-generation](#link-intro-generation)
  - [html-link-extraction](#html-link-extraction)

- 📂 Parsing
  - [\"\\'?(.*?)\"\\'?](#["\\\']?(.*?)["\\\']?)
  - [extract-links-from-start](#extract-links-from-start)
  - [split-text-by-anchors](#split-text-by-anchors)
  - [parse-answer](#parse-answer)
  - [spliter-function](#spliter-function)

- 📂 Compression
  - [compress-function](#compress-function)
  - [compress-and-compare](#compress-and-compare)
  - [compress-to-one](#compress-to-one)

- 📂 Schema & Utilities
  - [schema-classes](#schema-classes)
  - [codemix-class](#codemix-class)
  - [logging-infrastructure](#logging-infrastructure)
  - [progress-abstraction](#progress-abstraction)

- 📂 Finalization
  - [finalize](#finalize)
  - [have-to-change](#have-to-change)
<a name="init-welcome"></a>
## Welcome Banner & Logger Instantiation

**Functional Role**  
The module prints a colored ASCII logo and status line when the package is imported, then creates a global ``logger`` instance for the whole library.

**Visible Interactions**  
- Uses ``print`` (stdout) for the banner – no external I/O.  
- Imports ``BaseLogger`` and related classes from ``autodocgenerator.ui.logging`` to construct ``logger``.  
- Exposes ``logger`` at package level so downstream modules can ``from autodocgenerator import logger`` and share a single configured logger.

**Step‑by‑Step Logic**  

1. Define ``_print_welcome`` – local helper.  
2. Inside, set ANSI colour/format constants.  
3. Compose ``ascii_logo`` string with colour codes.  
4. Print logo and a status line showing library name, version, and ready state.  
5. Call ``_print_welcome()`` immediately on import.  
6. Import logger classes from ``.ui.logging``.  
7. Instantiate ``BaseLogger`` → ``logger``.  
8. Attach a ``BaseLoggerTemplate`` via ``logger.set_logger`` to configure format/level.

**Data Contract**

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| ``_print_welcome`` | function | Emits banner on import | No parameters, no return value |
| ``BLUE``, ``BOLD`` … | ``str`` | ANSI escape sequences | Used only inside the function |
| ``ascii_logo`` | ``str`` | Formatted logo text | Multi‑line string |
| ``logger`` | ``BaseLogger`` (instance) | Global logging object | Accessible as ``autodocgenerator.logger`` |
| ``BaseLoggerTemplate`` | class | Logging format/template | Passed to ``logger.set_logger`` |
| ``print`` | built‑in | Output side‑effect | Writes to standard output |

> **Critical Note** – The banner prints *every* time the package is imported, which may be undesirable in non‑interactive contexts (e.g., automated CI). Adjust by guarding the call with an environment flag if needed.
<a name="git-status-evaluation"></a>
## Git Status Evaluation (`autodocgenerator.auto_runner.check_git_status`)

**Functional Role** – Determines whether the repository has changed since the last documented commit and instructs the **Manager** to rebuild documentation accordingly.

### Visible Interactions
| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `Manager` | class instance | Receives `CacheSettings.last_commit`; calls `manager.check_sense_changes` | Imported from `autodocgenerator.manage` |
| `CacheSettings` | pydantic model | Stores `last_commit`; mutated in‑place | Imported from `autodocgenerator.schema.cache_settings` |
| `CheckGitStatusResultSchema` | pydantic model | Returned result (`need_to_remake`, `remake_gl_file`) | Imported from same module |
| `GITHUB_EVENT_NAME` | `str` env constant | Bypasses diff check for manual workflow runs | Imported from `engine.config.config` |
| `subprocess` | stdlib | Executes `git` commands | Used in `get_diff_by_hash`, `get_detailed_diff_stats`, `get_git_revision_hash` |

### Logic Flow
1. **Environment guard** – If `GITHUB_EVENT_NAME == "workflow_dispatch"` **or** `manager.cache_settings.last_commit` is empty, set `last_commit` to current HEAD hash and force a full rebuild (`need_to_remake=True`, `remake_gl_file=True`).  
2. Otherwise, call `get_detailed_diff_stats` with the stored hash to collect per‑file change stats.  
3. Pass the list of dicts to `manager.check_sense_changes`, which decides if a partial or full regeneration is required.  
4. Return the `CheckGitStatusResultSchema` produced by the manager.

> **Note** – The function assumes `git` is available and the working directory is the repository root; no fallback is implemented.

---
<a name="configuration-parsing"></a>
## Configuration Parsing (`autodocgenerator.auto_runner.config_reader`)

**Functional Role** – Loads `autodocconfig.yml` content, builds the runtime `Config`, a list of **custom modules**, and a `StructureSettings` object that controls downstream pipeline behavior.

### Visible Interactions
| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `yaml.safe_load` | function | Parses raw YAML string | Imported from `yaml` |
| `Config` / `ProjectBuildConfig` | classes | Hold global settings, ignore patterns, additional info | Imported from `..config.config` |
| `BaseModule`, `CustomModule`, `CustomModuleWithOutContext` | classes | Represent user‑defined documentation fragments | Imported from `autodocgenerator.factory.modules.general_modules` |
| `StructureSettings` | class (local) | Toggles features like intro links, ordering, global file usage | Instantiated per run |
| `list[BaseModule]` | runtime list | Ordered collection of modules to feed the **DocFactory** | Constructed from `custom_descriptions` |

### Logic Flow
1. `yaml.safe_load` converts the file text to a dict.  
2. Core fields (`ignore_files`, `language`, `project_name`, `project_additional_info`) populate a fresh `Config` instance via fluent setters.  
3. Each ignore pattern is registered with `config.add_ignore_file`.  
4. Project‑specific key‑value pairs are added through `config.add_project_additional_info`.  
5. `custom_descriptions` is transformed into a list of `BaseModule` subclasses: entries beginning with `%` become `CustomModuleWithOutContext`, others become `CustomModule`.  
6. `structure_settings` dict is applied to a new `StructureSettings` instance via `load_settings`.  
7. The tuple `(config, custom_modules, structure_settings_object)` is returned for the **Manager** to consume.

> **Critical Warning** – No validation is performed on the shape of `custom_descriptions`; malformed entries may raise runtime errors.
<a name="projectsettings-class"></a>
## `ProjectSettings` – Prompt Builder  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_name` | `str` (ctor) | Identifier injected into the system prompt. |
| `info` | `dict[str, str]` | Arbitrary key‑value pairs added via `add_info`. |
| **Property** `prompt` | `str` | Concatenates `BASE_SETTINGS_PROMPT`, project name, and all `info` entries (each on its own line). |

**Logic Flow**  
1. Initialise with `project_name`.  
2. `add_info(key, value)` stores custom metadata.  
3. Accessing `prompt` builds the final system‑prompt string on‑the‑fly.
<a name="pyproject-toml"></a>
## `pyproject.toml` – Package Definition  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `[project]` | metadata table | Describes the Python package (name, version, description, authors, license, readme, Python requirement). | `requires‑python = ">=3.11,<4.0"`. |
| `dependencies` | list | Runtime libraries required by **Auto‑Doc Generator**. | Includes `groq`, `google‑genai`, `rich`, etc. |
| `[tool.poetry]` | configuration table | Excludes the cache file from distribution. | `exclude = [".auto_doc_cache_file.json"]`. |
| `[build-system]` | table | Build backend specification for PEP 517. | Uses `poetry-core`. |

**Data Contract** – When the project is built, the build system reads `pyproject.toml` to resolve the exact version constraints listed under `dependencies`. No runtime code interacts with this file; it serves solely as static package metadata.
<a name="autodoc-setup-options"></a>
The file is a YAML document that defines the behavior of the documentation generator. The top‑level keys and their possible values are:

**project_name** – a string that sets the name of the project shown in the generated documentation.

**language** – the language code (e.g., `en`) used for the output text.

**ignore_files** – a list of glob patterns and directory names that the generator will skip. Typical entries include build folders (`dist`), Python byte‑code caches (`*.pyc`, `__pycache__`), virtual‑environment directories (`venv`, `.env`), IDE configuration folders (`.vscode`, `.idea`), database files, log files, coverage reports, version‑control metadata, static assets, and any markdown files you do not want to process.

**build** – a subsection containing parameters that control the generation process:
- **save_logs** – boolean (`true`/`false`) indicating whether logs should be persisted.
- **log_level** – numeric level (e.g., `2`) that sets the verbosity of logging.
- **threshold_changes** – an integer that defines the change size limit (in characters) for triggering a full regeneration.

**structure** – a subsection that shapes the layout of the final document:
- **include_intro_links** – boolean to add navigation links at the start.
- **include_intro_text** – boolean to include introductory explanatory text.
- **include_order** – boolean to preserve the order of processed files.
- **use_global_file** – boolean to merge content into a single global file.
- **max_doc_part_size** – maximum number of characters per documentation segment.

**project_additional_info** – a mapping for extra project metadata. In the example a `global idea` entry provides a short description of the project’s purpose.

**custom_descriptions** – a list of free‑form strings that the generator will incorporate as custom sections. These can be instructions, usage guides, or any other explanatory paragraphs you want to appear in the output.

When creating the file, follow standard YAML syntax: use proper indentation (two spaces per level) and enclose strings in quotes if they contain special characters. Ensure each top‑level key is present (or omitted if defaults are acceptable) and provide the desired values according to the descriptions above.
<a name="install-script"></a>
## `install.ps1` – CI Bootstrap Generator  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `.github/workflows/autodoc.yml` | file (generated) | GitHub Actions workflow that re‑uses a remote reusable workflow. | Inserts secret `GROCK_API_KEY`. |
| `autodocconfig.yml` | file (generated) | Default configuration for the Auto‑Doc Generator. | Populated with project name, language, ignore patterns, and build/structure flags. |
| PowerShell commands | script | Creates workflow directory, writes the two files, and echoes a success message. | Uses here‑strings (`@' … '@`) to avoid variable expansion. |

**Logic Flow**  
1. Ensure `.github/workflows` exists (`New-Item -Force`).  
2. Write static workflow YAML to `autodoc.yml`.  
3. Derive the current folder name, embed it in a YAML config string, and write `autodocconfig.yml`.  
4. Output a green “Done!” banner.  

> **Information not present in the provided fragment** – No validation of write permissions or error handling for I/O failures.
<a name="install-sh"></a>
## `install.sh` – CI Bootstrap Script  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `.github/workflows/autodoc.yml` | generated file | GitHub‑Actions workflow that re‑uses the remote **reuseble_agd.yml** and injects the secret `GROCK_API_KEY`. | Uses a *here‑document* (`cat <<EOF`). |
| `autodocconfig.yml` | generated file | Default configuration for the Auto‑Doc Generator; contains project name, language, ignore patterns and build/structure flags. | `project_name` is derived from `basename "$PWD"`. |
| `mkdir -p .github/workflows` | command | Guarantees the target directory exists before writing files. | Idempotent. |
| `echo "✅ Done! …"` | command | User feedback on successful creation of each file. | No error handling. |

> **Assumption** – The script runs with write permission in the repository root; any I/O error is not caught.

**Logic Flow**  
1. Ensure `.github/workflows` exists.  
2. Write a static workflow YAML to `autodoc.yml`, escaping the first `$` so the secret placeholder remains intact.  
3. Emit a success banner.  
4. Write `autodocconfig.yml` with a YAML block that populates ignore lists and flags, interpolating the current directory name.  
5. Echo a second success banner.  

The script does **not** validate the generated content, nor does it check for existing files before overwriting.
<a name="install-workflow-setup"></a>

To set up the installation workflow for both Windows PowerShell and Linux‑based environments, follow these steps:

### Windows (PowerShell)

1. **Run the remote installer**  
   Execute the following command in an elevated PowerShell session:

   ```powershell
   irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
   ```

   This command fetches the PowerShell installation script directly from the repository and pipes it to the PowerShell interpreter for immediate execution.

2. **Verification**  
   After the command completes, confirm that the required components have been installed by checking the presence of the expected binaries or by running a version check command provided by the script.

### Linux / macOS (Bash)

1. **Run the remote installer**  
   In a terminal, issue the following command:

   ```bash
   curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
   ```

   The `curl` request downloads the Bash installer script and streams it directly to `bash` for execution.

2. **Verification**  
   Once the script finishes, verify the installation by invoking any provided test commands or by confirming that the installed executables are available in your `PATH`.

### GitHub Actions Integration

To automate the installation within a GitHub Actions workflow, you must provide an API key from the Grock service as a secret:

1. **Create the secret**  
   - Navigate to your repository’s **Settings → Secrets and variables → Actions**.  
   - Add a new secret named `GROCK_API_KEY`.  
   - Paste the API key you obtained from the Grock documentation (see https://grockdocs.com).

2. **Reference the secret in the workflow**  
   In your workflow YAML, you can expose the secret to steps that need it:

   ```yaml
   env:
     GROCK_API_KEY: ${{ secrets.GROCK_API_KEY }}
   ```

   Ensure any scripts or commands that interact with the Grock API reference this environment variable.

### Summary of Commands

| Platform | Command |
|----------|---------|
| PowerShell (Windows) | `irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 \| iex` |
| Bash (Linux/macOS)   | `curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh \| bash` |

By following the above steps, you will have a reproducible installation process for both local development and CI pipelines, with the required API key securely supplied via GitHub Actions secrets.
<a name="manager-class"></a>
## `Manager` – Orchestrator Core  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_directory` | `str` | Root of the repo to document | |
| `config` | `Config` | Holds ignore patterns, language, logging flags | |
| `llm_model` | `Model` | Groq‑based LLM client used throughout the pipeline | |
| `embedding_model` | `Embedding` | Google embedding wrapper for vectorising sections | |
| `progress_bar` | `BaseProgress` | Tracks overall and sub‑task progress | |
| `logger` | `BaseLogger` | Writes info/warn/error logs to `report.txt` | |
| `doc_info` | `DocInfoSchema` | In‑memory container for `code_mix`, `global_info`, `doc` | |
| `cache_settings` | `CacheSettings` | Persistent JSON cache (`.auto_doc_cache_file.json`) | Loaded/updated in `init_folder_system` |

### `Manager.__init__` – Construction  

1. Instantiates `DocInfoSchema` and stores injected dependencies.  
2. Creates a file logger (`FileLoggerTemplate`) pointing to `report.txt`.  
3. Calls `init_folder_system` to ensure `/.auto_doc_cache` exists and loads/creates the cache JSON.
<a name="manager-init-folder-system"></a>
## `init_folder_system` – Cache Bootstrap  

* Creates cache directory if missing.  
* Writes a fresh `CacheSettings` JSON when the cache file does not exist.  
* Deserialises the file into `self.cache_settings` via `CacheSettings.model_validate_json`.
<a name="manager-class-usage"></a>!noinfo
<a name="custom-modules-implementation"></a>
## Custom Modules (`CustomModule`, `CustomModuleWithOutContext`)  

| Class | Constructor Arg | `generate` Behaviour |
|-------|----------------|----------------------|
| `CustomModule` | `discription: str` | Calls `generete_custom_discription(split_data(...), model, self.discription, language)` |
| `CustomModuleWithOutContext` | `discription: str` | Calls `generete_custom_discription_without(model, self.discription, language)` |

Both rely on external `generete_custom_discription*` helpers; the fragment supplies only the call signatures.
<a name="intro-modules-implementation"></a>
## Intro Modules (`IntroLinks`, `IntroText`)  

| Class | `generate` Steps |
|-------|-------------------|
| `IntroLinks` | Retrieves HTML links via `get_all_html_links(info["full_data"])`, then formats them with `get_links_intro(links, model, language)`. |
| `IntroText` | Produces introductory text via `get_introdaction(info["global_info"], model, language)`. |

**Data Contract Table**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `info` | `dict` | Input context (keys used: `code_mix`, `language`, `full_data`, `global_info`) | Missing keys result in `None` passed to helpers. |
| `model` | `Model` | LLM client for all helper calls | No direct usage shown here. |
| Return | `str` | Markdown fragment for the respective module | Inserted into `DocHeadSchema` by `DocFactory`. |

> **Warning** – The fragment does not validate presence of required keys; callers must ensure `info` contains them.
<a name="model-base"></a>## `Model` & `ParentModel` – Shared Contract  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `ParentModel` | abstract base | Stores `api_keys`, `history`, rotation state, and enforces abstract methods. | `models_list` shuffled if `use_random`. |
| `History` | class | Holds `system_prompt` and mutable `history` list. | `add_to_history(role, content)` appends messages. |
| `Model` | concrete subclass | Provides thin wrappers: `get_answer_without_history` → `generate_answer`; `get_answer` adds user prompt to history then calls `generate_answer`. | Default `generate_answer` returns `"answer"` (placeholder). |

> **Assumption** – All logging classes (`InfoLog`, `WarningLog`, `ErrorLog`) and the `Groq` client behave as their names imply; no internal details are inferred beyond the shown calls.
<a name="base-module-interface"></a>
## `BaseModule` Abstract Interface  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseModule` | **class** (ABC) | Blueprint for plug‑in generators | Sub‑classes must implement `generate(info: dict, model: Model)` |

> **Assumption** – The abstract method returns a *string* representing a markdown fragment; the exact format is not enforced by the snippet.
<a name="gptmodel-construction"></a>## `GPTModel` – LLM Wrapper Construction  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `GPTModel` | class (subclass of `Model`) | Instantiates a Groq client, loads API keys, prepares model rotation, attaches logger. | `api_key` defaults to `GROQ_API_KEYS`; `models_list` shuffled when `use_random=True`. |
| `self.client` | `Groq` | Performs `chat.completions.create` calls. | Re‑created on key rotation. |
| `self.logger` | `BaseLogger` | Emits `InfoLog` / `WarningLog` / `ErrorLog`. | Created per instance. |

The constructor stores `history`, `api_keys`, `regen_models_name` (shuffled model list) and sets index counters (`current_model_index`, `current_key_index`). No external I/O occurs beyond client init.
<a name="gptmodel-generate-answer"></a>## `GPTModel.generate_answer` – Prompt Execution Logic  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `with_history` | bool | Determines whether to prepend `self.history.history` to the request. | If `False` and `prompt` supplied, `messages = prompt`. |
| `messages` | `list[dict]` | Payload sent to Groq. | Contains role/content pairs. |
| `model_name` | `str` | Selected model from `regen_models_name`. | Rotated on failure. |
| `chat_completion` | Groq response | Holds `choices[0].message.content`. | Returned as `result`. |
| `result` | `str` | Final LLM answer. | Logged at level 2; empty string returned if `None`. |

**Logic flow**  
1. Log start.  
2. Choose message source based on `with_history`.  
3. Enter retry loop:  
   - Fail‑fast if `regen_models_name` empty → `ModelExhaustedException`.  
   - Attempt `self.client.chat.completions.create(messages=messages, model=model_name)`.  
   - On exception: log warning, rotate API key (`current_key_index`) and, if wrapped, rotate model index. Re‑instantiate `Groq` with new key, repeat.  
4. Extract `result`, log success and raw answer, return it (or `""` if `None`).
<a name="embedding-class"></a>
## `Embedding` – Gemini Vectoriser  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `api_key` | `str` (ctor arg) | Auth for Google GenAI | Stored in `self.client` |
| `self.client` | `genai.Client` | API wrapper |
| `get_vector(prompt)` | `list[float]` | Calls `embed_content` with model *gemini‑embedding‑2‑preview* (768‑dim) | Raises `Exception` if `embeddings` is `None` |

> **Warning** – The method returns `list(text_response.embeddings[0])[0][1]`, assuming the first embedding element is a tuple‑like structure; any format change will break the call.
<a name="embedding-ordering"></a>
## `create_embedding_layer` & `order_doc` – Vectorisation & Re‑ordering  

* Iterates over `self.doc_info.doc.parts` and calls `init_embedding(self.embedding_model)` to attach embeddings.  
* Calls `get_order` with the LLM to obtain a new ordering list, then assigns it back to `content_orders`.
<a name="vector-sort-helpers"></a>
## Helper Functions – Vector Distance & Sorting  

* `bubble_sort_by_dist(arr)` – classic bubble sort on a list of `(id, distance)` tuples.  
* `get_len_btw_vectors(v1, v2)` – Euclidean norm via `np.linalg.norm`.  
* `sort_vectors(root_vector, other)` – Computes distance from `root_vector` to each vector in `other` (dict `id → vector`), returns IDs ordered by ascending distance.

All functions are pure and return plain Python collections; they **do not** log.
<a name="get-order"></a>
## `get_order` – LLM‑Driven Title Re‑ordering  

Requests the LLM to sort a list of section titles semantically.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` (sub‑class of `ParentModel`) | LLM backend providing `get_answer_without_history` | No history retained across calls |
| `chanks` | `list[str]` | Raw titles extracted from anchors | Passed verbatim into the prompt |
| **Return** | `list[str]` | Ordered titles (comma‑separated list trimmed) | Used later to align sections |

**Logic Flow**  
1. Log start via `BaseLogger`.  
2. Build a user‑role prompt requesting a comma‑separated, *exact* list of sorted titles, preserving leading “#”.  
3. Call `model.get_answer_without_history(prompt)`.  
4. Split the LLM response on commas, strip whitespace, produce `new_result`.  
5. Log the final ordered list and return it.  

> **Assumption** – The LLM obeys the “return ONLY a comma‑separated list” instruction; any deviation will be propagated unchanged.

---
<a name="generate-code-file"></a>
## `generate_code_file` – Repo Snapshot  

* Uses `CodeMix(project_directory, config.ignore_files)` to walk the repository and produce a single string (`code_mix`).  
* Stores result in `self.doc_info.code_mix`.  
* Logs start/end and advances `progress_bar`.
<a name="generate-global-info"></a>
## `generate_global_info` – Optional Global Summary  

* If `is_reusable` and a cached `global_info` exists, re‑uses it.  
* Otherwise splits `code_mix` with `split_data(full_code_mix, max_symbols)`.  
* Calls `compress_to_one` (LLM + progress) to obtain a compressed markdown fragment.  
* Saves to `self.doc_info.global_info` and updates progress.
<a name="doc-factory-constructor"></a>
## `DocFactory.__init__` – Construction  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `modules` | `*BaseModule` | Collection of user‑provided generators | Stored as `self.modules` |
| `with_splited` | `bool` | Controls post‑generation splitting | Default `True` |
| `logger` | `BaseLogger` | Centralised logger instance | Created via `BaseLogger()` |
<a name="doc-factory-generate-doc"></a>
## `DocFactory.generate_doc` – Core Logic  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `info` | `dict` | Shared context (e.g., `code_mix`, `language`) | Passed unchanged to each module |
| `model` | `Model` | LLM client used by modules | No direct calls in this fragment |
| `progress` | `BaseProgress` | Tracks sub‑task progress | `create_new_subtask`, `update_task`, `remove_subtask` |
| `doc_head` | `DocHeadSchema` | Accumulator for generated parts | `add_parts(key, DocContent)` |

**Step‑by‑step flow**  

1. Initialise empty `DocHeadSchema`.  
2. `progress.create_new_subtask("Generate parts", len(self.modules))`.  
3. Iterate `self.modules` (index `i`, element `module`):  
   - Call `module.generate(info, model)` → `module_result`.  
   - If `self.with_splited` is `True`:  
     * `split_text_by_anchors(module_result)` → `splited_result` (dict of anchor → fragment).  
     * For each `el` in `splited_result`: `doc_head.add_parts(el, DocContent(content=splited_result[el]))`.  
   - Else: construct `task_name = f"{module.__class__.__name__}_{i}"` and add whole result.  
   - Log two **InfoLog** entries (module success, raw output).  
   - `progress.update_task()`.  
4. After loop, `progress.remove_subtask()`.  
5. Return populated `doc_head`.
<a name="factory-generate-doc"></a>
## `factory_generate_doc` – Plugin Module Execution  

* Builds `info` dict (`language`, `full_data`, `code_mix`, `global_info`).  
* Logs the module list and input keys.  
* Invokes `doc_factory.generate_doc(info, llm_model, progress_bar)` – the fragment documented earlier.  
* Prepends or appends the returned `DocHeadSchema` to the existing document based on `to_start`.
<a name="gen_doc-function"></a>
## `gen_doc` – Orchestrator for Documentation Generation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_path` | `str` | Root directory of the repository to document | Passed unchanged to `Manager`. |
| `config` | `Config` (custom class) | Holds ignore patterns, language, project metadata | Created by `read_config`. |
| `custom_modules` | `list[BaseModule]` | User‑defined markdown generators | Instances of `CustomModule` or `CustomModuleWithOutContext`. |
| `structure_settings` | `StructureSettings` (local) | Flags controlling optional steps (global file, intro sections, ordering) | Populated by `read_config`. |
| **Return** | `str` | Full assembled markdown document or empty string when no rebuild needed | Obtained via `manager.doc_info.doc.get_full_doc()`. |
<a name="gen_doc-logic-flow"></a>
## Step‑by‑Step Logic Flow  

1. **Model Instantiation** – `GPTModel` receives `GROQ_API_KEYS`; `Embedding` receives `GOOGLE_EMBEDDING_API_KEY`.  
2. **Manager Construction** – `Manager(project_path, config, llm_model, embedding_model, progress_bar)` creates the central orchestrator, storing all supplied objects.  
3. **Git Status Check** – `check_git_status(manager)` returns a `CheckGitStatusResultSchema` with booleans `need_to_remake` / `remake_gl_file`.  
4. **Early Exit** – If both flags are `False`, the function returns `""` (no documentation rebuild).  
5. **Source Extraction** – `manager.generate_code_file()` builds the raw code snapshot (`code_mix`).  
6. **Global Info (optional)** – If `structure_settings.use_global_file` is true, `manager.generate_global_info` compresses the snapshot; the `is_reusable` flag is the inverse of `remake_gl_file`.  
7. **Chunked Documentation** – `manager.generete_doc_parts` splits the code into chunks (size limited by `structure_settings.max_doc_part_size`) and queries the LLM for markdown fragments.  
8. **Custom Module Generation** – `manager.factory_generate_doc(DocFactory(*custom_modules))` runs each user‑provided `BaseModule` to produce additional markdown sections.  
9. **Optional Ordering** – If `structure_settings.include_order` is true, `manager.order_doc()` re‑orders sections via an LLM‑driven pass.  
10. **Intro Sections (optional)** – `IntroText` and/or `IntroLinks` are instantiated based on flags and injected at the document start via a second `factory_generate_doc` call (`with_splited=False`, `to_start=True`).  
11. **Embedding Layer** – `manager.create_embedding_layer()` computes vector embeddings for all markdown parts.  
12. **Cache Cleanup** – `manager.clear_cache()` resets mutable cache fields.  
13. **Persist & Return** – `manager.save()` writes the final markdown and cache files; the assembled document string is returned.
<a name="gen_doc-data-contract"></a>
## Data Contract Summary  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `manager` | `Manager` | Core pipeline controller | Holds `CacheSettings`, `DocHeadSchema`, progress logger, etc. |
| `change_info` | `CheckGitStatusResultSchema` | Result of Git diff analysis | Attributes `need_to_remake: bool`, `remake_gl_file: bool`. |
| `structure_settings.use_global_file` | `bool` | Toggles global‑file generation | Determines step 6. |
| `structure_settings.max_doc_part_size` | `int` | Maximum symbols per chunk for LLM calls | Controls step 7. |
| `structure_settings.include_order` | `bool` | Enables LLM‑based re‑ordering | Controls step 9. |
| `structure_settings.include_intro_text` / `include_intro_links` | `bool` | Controls inclusion of intro modules | Affects step 10. |
| `manager.doc_info.doc` | `DocHeadSchema` (contains `DocContent` parts) | Aggregated markdown fragments | `get_full_doc()` concatenates all parts. |

> **Critical Assumption** – The function assumes all imported classes behave as their names suggest; no internal details are inferred beyond what is visible in the snippet.
<a name="gen-doc-parts"></a>
## `gen_doc_parts` – Pipeline Driver for Chunked Documentation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `full_code_mix` | `str` | Whole repository snapshot produced by `CodeMix`. | |
| `max_symbols` | `int` | Maximum characters per chunk for `split_data`. | |
| `model` | `Model` | LLM used throughout the pipeline. | |
| `project_settings` | `ProjectSettings` | Shared prompt context. | |
| `language` | `str` | Desired output language. | |
| `progress_bar` | `BaseProgress` | UI feedback for chunk processing. | |
| `global_info` | `Any` | Forwarded to `write_docs_by_parts`. | |
| **Return** | `str` | Concatenated markdown of the entire repository. | |

**Logic Flow**  
1. **Chunk** the repo via `split_data(full_code_mix, max_symbols)`.  
2. Initialise a sub‑task on `progress_bar`.  
3. Iterate chunks, calling `write_docs_by_parts` for each; accumulate results in `all_result`.  
4. After each chunk, keep a **3000‑character tail** of the current result to feed as `prev_info` for the next call (preserves context).  
5. Update progress bar, finally remove sub‑task and log completion.  

---
<a name="generete-doc-parts"></a>
## `generete_doc_parts` – Chunked Documentation  

* Calls `gen_doc_parts` (LLM per chunk) with language and optional `global_info`.  
* Splits the concatenated result into anchor sections via `split_text_by_anchors`.  
* Inserts each section into `self.doc_info.doc` as `DocContent`.
<a name="write-docs-by-parts"></a>
## `write_docs_by_parts` – Part‑wise LLM Documentation Generator  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | Source code fragment to document. | |
| `model` | `Model` | LLM used for generation (`get_answer_without_history`). | |
| `project_settings` | `ProjectSettings` | Supplies global system prompt. | |
| `prev_info` | `str \| None` | Previous fragment output, used to keep continuity. | |
| `language` | `str` | Target language for the generated text (default **en**). | |
| `global_info` | `str \| None` | Optional additional project‑wide context. | |
| **Return** | `str` | Generated markdown for the fragment. | |

**Logic Flow**  
1. Log start via `BaseLogger`.  
2. Build a **system‑message list**: language, global project info, static part template (`BASE_PART_COMPLITE_TEXT`), optional `global_info` and `prev_info`.  
3. Append the **user message** containing `part`.  
4. Call `model.get_answer_without_history(prompt)`.  
5. Strip surrounding markdown fences (```` ``` ````) if present and return the clean answer.  

> **Assumption** – `model.get_answer_without_history` always returns a string; no error handling is shown in the fragment.

---
<a name="custom-description-loop"></a>
## `generete_custom_discription` – Conditional Chunk Description  

Iterates over `splited_data` (iterable of strings). For each chunk it sends a detailed prompt containing the chunk, a custom description request, and **`BASE_CUSTOM_DISCRIPTIONS`**. The loop stops when the LLM returns a result that does **not** contain `!noinfo` or “No information found”, or when such markers appear after position 30.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `splited_data` | `Iterable[str]` | Source fragments |
| `model` | `Model` | LLM |
| `custom_description` | `str` | Task description supplied by the caller |
| `language` | `str` | Language selector |
| Return | `str` | First satisfactory description, empty if none |
<a name="standalone-custom-description"></a>
## `generete_custom_discription_without` – Stand‑Alone Description  

Creates a single‑anchor response (mandatory `
<a name="CONTENT_DESCRIPTION"></a>` tag) that rewrites `custom_description`. No source context is given.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | LLM |
| `custom_description` | `str` | Text to be rewritten |
| `language` | `str` | Language selector |
| Return | `str` | LLM answer respecting strict tag rules |
<a name="global-intro-generation"></a>
## `get_introdaction` – Global Documentation Intro  

Builds a prompt using **`BASE_INTRO_CREATE`** and asks the LLM for a high‑level introduction based on `global_data`.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `global_data` | `str` | Full repository summary (or similar) |
| `model` | `Model` | LLM backend |
| `language` | `str` | Language selector |
| Return | `str` | Intro markdown fragment |
<a name="link-intro-generation"></a>
## `get_links_intro` – LLM‑Driven Links Intro  

Calls a **`Model`** (typically `GPTModel`) with a three‑message prompt to create an introductory paragraph that lists the supplied links.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `links` | `list[str]` | Input list of anchor strings |
| `model` | `Model` | LLM provider | Must implement `get_answer_without_history` |
| `language` | `str` | System‑prompt language selector (default `"en"`) |
| Return | `str` | Generated markdown intro | Logged before and after the call |
<a name="html-link-extraction"></a>
## `get_all_html_links` – HTML Anchor Collector  

Extracts **anchor names** from a markdown string.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Source documentation | Expected to contain `<a name="…"></a>` tags |
| `links` | `list[str]` | Return value | Each entry is prefixed with `#` and filtered to length > 5 |
| `logger` | `BaseLogger` | Side‑effect | Logs start, count, and list at level 1 |
| `pattern` | `str` (regex) | Internal | `r'<a name=["\']?(.*?)["\']?></a>'` |

> **Assumption** – The function does **not** validate duplicate anchors.
<a name="extract-links-from-start"></a>
## `extract_links_from_start` – Anchor Detection in Chunk List  

Identifies leading `<a name=…></a>` tags and returns a list of markdown links plus a flag indicating whether the first non‑anchor chunk must be discarded.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `chunks` | `list[str]` | Raw text fragments supplied by the caller | Each element is stripped before inspection |
| **Return** | `tuple[list[str], bool]` | (`links`, `have_to_del_first`) | `links` are `#anchor` strings; flag is *True* when any chunk lacks a valid anchor |

**Logic Flow**  
1. Initialise `links = []`, `have_to_del_first = False`.  
2. Iterate over `chunks`.  
3. Use regex `^<a name=["']?(.*?)["']?</a>` to capture the anchor name.  
4. If a name longer than 5 characters is found → prepend “#” and append to `links`.  
5. If a chunk yields no anchor → set `have_to_del_first = True`.  
6. Return the tuple.  

> **Warning** – The function assumes the first anchor appears at the very start of a chunk; otherwise `have_to_del_first` may be incorrectly set.

---
<a name="split-text-by-anchors"></a>
## `split_text_by_anchors` – Chunk Segmentation by Anchor Tags  

Splits a full markdown document into a dictionary keyed by anchor links.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `text` | `str` | Complete markdown payload containing `<a name=…></a>` markers | May include leading non‑anchor content |
| **Return** | `dict[str, str]` | Mapping `#anchor → chunk content` | Keys derived from `extract_links_from_start` |

**Logic Flow**  
1. Regex `(?=<a name=["']?[^"\'>\s]{6,200}["']?</a>)` splits `text` while retaining delimiters.  
2. Strip empty entries → `result_chanks`.  
3. Call `extract_links_from_start(result_chanks)` → `all_links`, `have_to_del_first`.  
4. If the first anchor appears far into the file (`start_link_index > 10`) **or** `have_to_del_first` is true, drop the first chunk (typically stray pre‑anchor text).  
5. Verify `len(all_links) == len(result_chanks)`; otherwise raise `Exception("Somthing with anchors")`.  
6. Build the result dict by pairing each link with its corresponding chunk.  

> **Critical** – Mismatch between detected links and chunks aborts the pipeline, ensuring anchor integrity.

---
<a name="parse-answer"></a>
## `parse_answer` – Git‑Change Check Result Parser  

Converts a pipe‑separated string into a typed schema.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `answer` | `str` | Expected format `"true|false"` etc. | Split on `|` |
| **Return** | `CheckGitStatusResultSchema` | `need_to_remake` & `remake_gl_file` booleans | Instantiated directly |

**Logic Flow**  
1. `splited = answer.split("|")`.  
2. `change_doc = splited[0] == "true"`; `change_global = splited[1] == "true"`.  
3. Return schema with those booleans.  

---
<a name="spliter-function"></a>
## `split_data` – Size‑Bound Chunker  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Full repository markdown (output of `CodeMix`). |
| `max_symbols` | `int` | Upper bound for each chunk’s character count. |
| **Return** | `list[str]` | Sequential fragments, each ≤ `max_symbols`. |

**Logic Flow** *(partial – file truncated)*  
1. Initialise `split_objects`.  
2. Split `data` on the sentinel `"
<a name="compress-function"></a>
## `compress` – Chunk‑Level LLM Compression  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Raw source fragment | May contain any file content. |
| `project_settings` | `ProjectSettings` | Supplies system prompt (`prompt` property). |
| `model` | `Model` | LLM wrapper exposing `get_answer_without_history`. |
| `compress_power` | `int` | Controls prompt‑generation intensity (passed to `BASE_COMPRESS_TEXT`). |
| **Return** | `str` | LLM‑produced summary of `data`. | Directly returned; no post‑processing. |

**Logic Flow**  
1. Assemble three messages: system → project prompt, system → compress‑size hint, user → `data`.  
2. Call `model.get_answer_without_history(prompt=prompt)`.  
3. Return the raw answer string.  

> **Assumption** – The LLM obeys the “return ONLY a comma‑separated list” instruction; any deviation will be propagated unchanged.
<a name="compress-and-compare"></a>
## `compress_and_compare` – Batch Compression & Merging  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | Ordered fragments to compress. |
| `model` | `Model` | Same LLM used by `compress`. |
| `project_settings` | `ProjectSettings` | Shared prompt context. |
| `compress_power` | `int` (default 4) | Number of fragments merged per output slot. |
| `progress_bar` | `BaseProgress` | UI feedback; default instantiated. |
| **Return** | `list[str]` | Length = ⌈len(data)/compress_power⌉, each element = merged compressed text. |

**Logic Flow**  
1. Allocate an output list sized for the target groups.  
2. Initialise a sub‑task on `progress_bar`.  
3. Iterate `data`; for each element `el` compute `curr_index = i // compress_power`.  
4. Append `compress(el, …) + "\n"` to the appropriate bucket.  
5. Update progress; after loop, remove the sub‑task and return the bucket list.
<a name="compress-to-one"></a>
## `compress_to_one` – Recursive Global Summarisation  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | Initial set of fragments (often output of `split_data`). |
| `model` | `Model` | LLM used for all compression steps. |
| `project_settings` | `ProjectSettings` | Global prompt source. |
| `compress_power` | `int` (default 4) | Base merging factor; may be reduced to 2 for small tails. |
| `progress_bar` | `BaseProgress` | UI feedback. |
| **Return** | `str` | Single markdown block representing the whole repository. |

**Logic Flow**  
1. Loop while `len(data) > 1`.  
2. If the remaining list is shorter than `compress_power + 1`, set `new_compress_power = 2`; otherwise keep the original.  
3. Replace `data` with `compress_and_compare(data, …, new_compress_power)`.  
4. Increment iteration counter.  
5. When one element remains, return `data[0]`.
<a name="schema-classes"></a>
## Schema Classes – In‑Memory / Persistent Data Model  

| Class | Key Fields | Purpose |
|-------|------------|---------|
| `CacheSettings` | `last_commit: str`, `doc: DocInfoSchema` | JSON‑persisted cache (`.auto_doc_cache_file.json`). |
| `DocInfoSchema` | `global_info: str`, `code_mix: str`, `doc: DocHeadSchema` | Holds raw repo text, optional global summary, and assembled doc parts. |
| `DocHeadSchema` | `content_orders: list[str]`, `parts: dict[str, DocContent]` | Maintains ordered collection of generated markdown fragments. |
| `DocContent` | `content: str`, `embedding_vector: list \| None` | Individual markdown block; can embed vectors via `init_embedding`. |

**Interaction Overview**  
- `Manager` (or other orchestrator) reads/writes `CacheSettings` to reuse previous runs.  
- `DocHeadSchema.add_parts(name, DocContent)` is invoked by factories or `write_docs_by_parts`‑derived results.  
- `DocHeadSchema.get_full_doc()` concatenates ordered parts for final output.  

> **Warning** – The fragment does not show persistence logic; it is assumed elsewhere that `CacheSettings` is serialized/deserialized.
<a name="codemix-class"></a>
## `CodeMix` – Repository Snapshot Builder  

Collects file‑system structure and file contents into a single markdown‑compatible string.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `root_dir` | `str` (ctor) | Base directory to walk | Resolved to absolute `Path` |
| `ignore_patterns` | `list[str]` | Glob patterns for exclusion | Defaults to `[]` or supplied list |
| **Method** `should_ignore(path)` | `bool` | Determines if `path` matches any ignore pattern | Checks full relative path, basename, and each part |
| **Method** `build_repo_content()` | `str` | Generates repository outline and file blocks | Returns a single string; logs ignored paths |

**Logic Flow**  
1. Initialise logger.  
2. Append “Repository Structure:” header.  
3. Walk `root_dir.rglob("*")` sorted; for each entry not ignored, compute depth → indentation, append directory/file name line.  
4. Insert separator line (`"="*20`).  
5. Second pass: for each file not ignored, emit `<file path="...">` tag, then file text, then a stray newline placeholder (`"\n"`). Errors are captured as inline messages.  
6. Join all pieces with newline characters and return.  

> **Critical** – The ignore logic uses `fnmatch` against the full relative path, basename, and each path component, ensuring comprehensive exclusion based on the supplied `ignore_list`.
<a name="logging-infrastructure"></a>
## `BaseLogger` & Log Templates  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseLog` | class | Holds raw `message` and numeric `level`; provides `_log_prefix`. | `format()` returns plain text; subclasses add level tags. |
| `ErrorLog`, `WarningLog`, `InfoLog` | subclasses of `BaseLog` | Format messages with **[ERROR]**, **[WARNING]**, **[INFO]** prefixes. | Use `_log_prefix` → timestamp. |
| `BaseLoggerTemplate` | class | Minimal logger; prints or writes formatted logs. | `global_log` respects `log_level`. |
| `FileLoggerTemplate` | subclass of `BaseLoggerTemplate` | Persists logs to a file path. | Opens file in append mode each call. |
| `BaseLogger` | singleton class | Central façade; holds a `logger_template` set via `set_logger`. | `log()` forwards to `global_log`. |

**Logic Flow**  
1. `BaseLogger.__new__` guarantees a single instance.  
2. Client creates a concrete template (e.g., `FileLoggerTemplate`) and registers it with `BaseLogger.set_logger`.  
3. Calls to `BaseLogger.log(ErrorLog("msg"))` invoke `logger_template.global_log`, which prints or writes the prefixed string.  

> **Assumption** – No thread‑safety mechanisms are present; concurrent writes may interleave.
<a name="progress-abstraction"></a>
## `BaseProgress` and Concrete Implementations  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `BaseProgress` | abstract class | Defines UI API: `create_new_subtask`, `update_task`, `remove_subtask`. | Methods are stubs (`...`). |
| `LibProgress` | subclass | Wraps **Rich** `Progress`; tracks a base task and an optional sub‑task. | `update_task` advances current task or base task. |
| `ConsoleGtiHubProgress` | subclass | Simple console feedback via `ConsoleTask`. | Uses two `ConsoleTask` instances for general and sub‑tasks. |
| `ConsoleTask` | helper | Prints start message and incremental percent. | No external dependencies. |

**Logic Flow**  
1. Orchestrator instantiates a concrete progress (e.g., `LibProgress`).  
2. For each pipeline stage it calls `create_new_subtask(name, total_len)`.  
3. After each unit of work `update_task()` is invoked, advancing the appropriate bar.  
4. Upon completion `remove_subtask()` discards the sub‑task reference.  

> **Warning** – If `create_new_subtask` is never paired with `remove_subtask`, the base task may never finish.
<a name="finalize"></a>
## `save` – Persist Output & Cache  

* Writes the assembled markdown (`self.doc_info.doc.get_full_doc()`) to `output_doc.md`.  
* Updates `self.cache_settings.doc` with the latest `DocInfoSchema` and rewrites the cache JSON.  

> **Warning** – The fragment does not perform explicit validation of keys inside `info`; callers must ensure required entries exist.
<a name="have-to-change"></a>
## `have_to_change` – LLM‑Based Repository Change Evaluation  

Queries the LLM whether documentation must be regenerated based on a diff and optional global info.  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | LLM interface | Uses `get_answer_without_history` |
| `diff` | `list[dict[str, str]]` | Structured diff description | Inserted verbatim into the prompt |
| `global_info` | `str \| None` | Optional repository‑wide summary | Added as a system message if present |
| **Return** | `CheckGitStatusResultSchema` | Result of `parse_answer` | Indicates doc rebuild needs |

**Logic Flow**  
1. Assemble a three‑message prompt: system prompt (`BASE_CHANGES_CHECK_PROMPT`), optional global info, and user diff.  
2. Invoke LLM, obtain raw answer string.  
3. Pass answer to `parse_answer` and return the schema.  

---
