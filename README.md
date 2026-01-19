## Executive Navigation Tree
- 📂 Core Engine
  - [entrypoint](#)
  - [model‑core](#)
  - [basefactory](#)
  - [manager‑class](#)
- ⚙️ Integration Layer
  - [integration](#)
  - [compressor](#)
  - [postprocess](#)

**Auto Doc Generator – Project Overview**

---

### 1. Project Title  
**Auto Doc Generator**

---

### 2. Project Goal  
Auto Doc Generator automates the creation of concise, high‑level documentation for software projects. By ingesting an entire codebase, summarising its structure and key components with GPT‑based compression, it delivers a single, human‑readable description that can be used as a README, project overview, or internal knowledge base. The tool eliminates manual documentation effort and ensures that the resulting text stays up‑to‑date with the source code.

---

### 3. Core Logic & Principles  

| Stage | What Happens | Key Techniques |
|-------|--------------|----------------|
| **Repository Ingestion** | `CodeMix` walks the directory tree, filters files using `ignore_patterns`, and writes a single UTF‑8 text file (`repo_mix.txt`). Each file’s content is wrapped in `<file path="…"> … </file>` tags, preserving the file hierarchy in a linear format. | Recursive directory traversal, pattern‑based filtering, XML‑style tagging for structural context. |
| **GPT Compression** | The `compress_to_one` routine repeatedly feeds chunks of the repository text to a language model. Each round reduces the number of strings by summarising pairs of chunks until only one summary remains. | Iterative pair‑wise summarisation, configurable `compress_power` (number of tokens or depth), optional asynchronous execution with a semaphore (max 4 concurrent calls). |
| **Settings & Prompting** | `ProjectSettings` holds a base prompt, project name, and arbitrary metadata. Each compression call prefixes the prompt with this context, ensuring consistent output across stages. | Simple data‑class, `add_info` helper for dynamic metadata injection. |
| **Progress Reporting** | `BaseProgress` is a no‑op stub; UI‑specific progress bars can be swapped in without changing the core logic. | Dependency injection of a progress handler. |
| **Utilities** | Internal helpers (`ignore_list`, `async_compress`, `async_compress_and_compare`) manage file filtering and concurrent API calls. Optional post‑processing helpers (`get_introdaction`, `get_links_intro`) can further refine the final text. | Modular design, clear separation of concerns. |

The pipeline is intentionally lightweight: it requires only a single text file and a GPT model, making it easy to integrate into CI/CD or local workflows.

---

### 4. Key Features  

- **Full‑tree ingestion** – converts an entire repository into a single, structured text file.  
- **Pattern‑based file exclusion** – customizable ignore list (e.g., `.git`, `node_modules`).  
- **Iterative GPT summarisation** – compresses large texts into a single coherent description.  
- **Synchronous & asynchronous modes** – choose between simple serial execution or parallel API calls (4‑way concurrency).  
- **Progress hooks** – plug in any progress bar implementation.  
- **Extensible settings** – add custom metadata or modify prompts on the fly.  
- **Modular architecture** – clear separation between pre‑processing, compression, and UI layers.  

---

### 5. How to Run  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-org/autodocgenerator.git
   cd autodocgenerator
   ```

2. **Create a virtual environment** (recommended)  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your GPT API key**  
   The compressor uses an OpenAI‑compatible client. Export the key as an environment variable:  
   ```bash
   export OPENAI_API_KEY="sk-…"
   ```

5. **Run the example script**  
   ```bash
   python examples/run_autodoc.py
   ```
   (The script follows the strict usage example provided in the project profile.)

6. **Inspect the output**  
   The final compressed string is printed to stdout. You can redirect it to a file if desired:  
   ```bash
   python examples/run_autodoc.py > summary.txt
   ```

---

### 6. Dependencies  

| Library | Purpose | Version (as of project release) |
|---------|---------|---------------------------------|
| `openai` | GPT‑model API client | `>=0.27.0` |
| `tqdm` | Optional progress bar (if you replace `BaseProgress`) | `>=4.50.0` |
| `aiohttp` | Async HTTP requests for concurrent compression | `>=3.8.0` |
| `pathlib` | File system abstraction (standard library) | – |
| `typing` | Type hints (standard library) | – |
| `dataclasses` | Simple data containers | – |

*All dependencies are listed in `requirements.txt` and can be installed with `pip`. The project is compatible with Python 3.8+.*

---

**Next Steps**  
Feel free to extend the pipeline: add new pre‑processing modules, integrate a different LLM provider, or expose a CLI interface. If you need design recommendations or code snippets for such extensions, just let me know!

 

<a name="docs-yml"></a>
### `.github/workflows/docs.yml` – Auto-Documentation CI

**Purpose**  
Fully-automated pipeline that regenerates the project README from source code on every push or pull-request to `main`.

**Interaction with the system**  
1. Checks out the repository.  
2. Installs the published `autodocgenerator` package (the same code-base it is running in).  
3. Executes the user-supplied configuration script (`autodocconfig.py`), which internally:  
   - invokes `CodeMix` → creates `repo_mix.txt`  
   - calls `compress_to_one` → produces `.auto_doc_cache/output_doc.md`  
4. Overwrites `README.md` with the freshly generated documentation.  
5. Commits & pushes the change back to the repository (if any).

**Key inputs/outputs**  
| Input | Source |  
|-------|--------|  
| `API_KEY` | GitHub secret (`GROCK_API_KEY`) – passed as env var to the config script so the GPT model can authenticate. |  
| `autodocconfig.py` | Must live in repository root and respect the API_KEY env var. |  

| Output | Destination |  
|--------|-------------|  
| `.auto_doc_cache/output_doc.md` | Created by the tool, later copied to `README.md`. |  

**Assumptions / gotchas**  
- The job holds `contents: write` permission – mandatory for the bot commit.  
- If nothing changed, the `git diff` guard prevents an empty commit.  
- The workflow uses the *released* package from PyPI, **not** the local source; therefore changes to the generator itself must first be published before they appear in the docs.

<a name="overview"></a>
## Overview

`autodocconfig.py` is the entry‑point script that orchestrates a full **Auto Doc Generator** run.  
It constructs a `ProjectSettings` instance, configures an ignore list, and calls `gen_doc()` which drives the pipeline via a `Manager` object.  
The script also contains a small helper to print the repository tree for quick visual verification.

<a name="dependencies"></a>
## Core Dependencies

| Module | Role |
|--------|------|
| `Manager` | Orchestrates all preprocessing and generation steps. |
| `DocFactory` & modules | Build the introductory sections of the output docs. |
| `LibProgress` | Bridges `rich.Progress` with the UI‑agnostic `BaseProgress` interface used by the manager. |
| `ProjectSettings` | Holds prompt text, project name and arbitrary key/value metadata. |
| `AsyncGPTModel` | GPT model interface (not instantiated here, but expected by the manager). |
| `split_data`, `gen_doc_parts`, `async_gen_doc_parts`, `compress_to_one`, `post‑process` helpers | Internal utilities for chunking, compression and formatting. |

<a name="gen_doc"></a>
## `gen_doc(project_settings, ignore_list, project_path)`

```python
def gen_doc(project_settings: ProjectSettings, ignore_list: list[str], project_path: str):
```

1. **Progress Setup** – Creates a `rich.Progress` instance with a spinner, text, bar and task progress.  
2. **Manager Construction** – `Manager(project_path, project_settings, ignore_list, progress_bar=LibProgress(progress), language="en")`  
   * `project_path`: root of the source tree.  
   * `ignore_list`: patterns that `CodeMix` will exclude.  
   * `progress_bar`: forwards UI feedback to the manager.  
   * `language`: fixed to English for prompts and output.  
3. **Pipeline Execution** – Sequentially invokes the manager’s high‑level helpers:  
   * `generate_code_file()` – emits a single `<repo_mix.txt>` containing the entire file tree wrapped in `<file path="…">`.  
   * `generate_global_info_file(use_async=True, max_symbols=5000)` – compresses the repo mix into a global summary using GPT, with async batching.  
   * `generete_doc_parts(use_async=True, max_symbols=4000)` – splits the global summary into logical sections, compresses each part, and writes them to temporary files.  
   * `factory_generate_doc_intro(DocFactory(IntroLinks(), IntroText()))` – stitches together an intro section containing hyperlinks and a brief text intro generated by GPT.  
4. **Result Retrieval** – Returns the concatenated document stored under the key `"output_doc"` via `manager.read_file_by_file_key("output_doc")`.

The function is deliberately synchronous; all heavy lifting (model calls, file I/O) happens inside the manager.

<a name="project_settings"></a>
## Project Settings Configuration

```python
project_settings = ProjectSettings("Auto Doc Generator")
project_settings.add_info(
    "global idea",
    """This project was created to help developers make documentations for them projects"""
)
```

* `ProjectSettings` encapsulates prompt wording, project name, and a dictionary of metadata.  
* `add_info` stores arbitrary key/value pairs that the generator can embed in the final output.

<a name="ignore_list"></a>
## Ignore List

```python
ignore_list = [
    "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db", "data",
    "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore",
    ".ruff_cache", ".auto_doc_cache", "*.pyc", "__pycache__", ".git",
    ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles",
    ".mypy_cache"
]
```

Patterns are passed to `CodeMix` to skip binary, cache, environment, and documentation files during the mix generation step.

<a name="entrypoint"></a>
## Execution Flow

```python
gen_doc(project_path=".", project_settings=project_settings, ignore_list=ignore_list)
```

* Runs the whole pipeline on the current working directory (`"."`).  
* After completion, the generated documentation is available from the returned string.

<a name="utility"></a>
## `print_tree` Helper

```python
def print_tree(startpath):
    ...
```

A quick directory visualizer that walks `startpath`, skips hidden folders, and prints a tree‑like structure to stdout.  
Not part of the main generation flow but handy for debugging.

<a name="related"></a>
## Related Minimal Modules

* `autodocgenerator/__init__.py` – merely prints `"ADG"`; placeholder for package initialization.  
* `autodocgenerator/engine/__init__.py` – contains a stray `'l'` character; likely incomplete.

These files do not influence the core logic but illustrate the package layout.

---  

**Key takeaways for newcomers**

1. The script wires together configuration, progress UI, and the `Manager` orchestrator.  
2. All heavy GPT interaction is abstracted inside `Manager` methods.  
3. The result is a single concatenated documentation string accessible via the manager’s key‑based file system.  
4. The `ignore_list` ensures irrelevant files are omitted early.  

Feel free to modify `project_settings` or `ignore_list` to tune the output for other projects.

<a name="model-core"></a>
# Model Layer – Core LLM Abstraction

## Responsibility  
Provide a **single interface** to any Groq-hosted LLM used by the compression stage.  
The layer is split into a **stateless** synchronous client (`GPTModel`) and an **asyncio-ready** client (`AsyncGPTModel`).  
Both clients implement automatic **fail-over**: if the current model returns an error they drop it from the internal list and retry until a successful response arrives or the list is exhausted.

## How it fits the pipeline  
The *compressor* (`compress_to_one`) instantiates either the sync or the async variant depending on `use_async`.  
Each compression round sends a prompt (or full conversation history) through `generate_answer` and receives the assistant reply that becomes the next chunk summary.

## Key Classes  

| Class | File | Purpose |
|-------|------|---------|
| `History` | `model.py` | Thin wrapper around `list[dict]` that prepends an optional system prompt. |
| `ParentModel` | `model.py` | Base container: stores API key, conversation history and a **shuffled** list of model names read from `MODELS_NAME` (`config.py`). |
| `Model` / `AsyncModel` | `model.py` | Define the public surface (`get_answer`, `get_answer_without_history`) and delegate the actual call to the subclass. |
| `GPTModel` / `AsyncGPTModel` | `gpt_model.py` | Concrete implementation using the Groq SDK (`Groq` / `AsyncGroq`). |

## Important Data Flow  

1. **Entry points**  
   - `get_answer(prompt: str)` – appends user message, calls model, stores assistant reply, returns string.  
   - `get_answer_without_history(prompt: list[dict])` – one-shot request, history ignored.

2. **Low-level method**  
   - `generate_answer(with_history, prompt)` – builds `messages`, loops over `self.regen_models_name`, invokes `chat.completions.create`.  
   - On `Exception` the faulty model is removed and the next index is tried (`current_model_index` is reset to 0 after removal).  
   - When no model remains an exception `"all models do not work"` is raised.

3. **Conversation state**  
   History is **shared** across calls inside the same instance; compressing a new file therefore requires a fresh model instance (cheap).

## Configuration Assumptions  

- `API_KEY` and `MODELS_NAME` are populated from `autodocgenerator.engine.config.config`.  
- `BASE_SYSTEM_TEXT` is injected into every fresh `History`.  
- `temperature` is hard-coded to `0.3` for the sync client; the async client currently omits it (commented out).

## Inputs / Outputs  

| Name | Type | Description |
|------|------|-------------|
| `prompt` | `str` or `list[dict]` | User question or ready-made message list. |
| `with_history` | `bool` | Whether to prepend the conversation history. |
| return | `str` | Assistant response text only. |

## Side Effects  

- Network calls to Groq.  
- History mutated on every `get_answer`.  
- Faulty models removed from the **instance-specific** list (does not affect global config).

<a name="basefactory"></a>
## `autodocgenerator.factory.base_factory`

### Purpose
Defines the core **factory pattern** used to assemble the final documentation string from a set of interchangeable **module generators**.  
The factory is independent of the specific content type, so any module that implements `BaseModule.generate()` can be plugged in.

### Key Components
| Class | Responsibility |
|-------|----------------|
| `BaseModule` | Abstract base class for all modules. Exposes a single `generate(info: dict)` method that must return a string. |
| `DocFactory` | Holds an ordered list of `BaseModule` instances and concatenates their outputs into a single document. |

### Interaction with the System
1. **Factory instantiation** is done in higher‑level orchestration code (e.g., after the compressor produces `info` dict).  
2. Each module receives the same `info` dictionary that contains pre‑processed data (`full_data`, `global_data`, `language`, …).  
3. The factory iterates over modules, collects their results, and joins them with double newlines for readability.  
4. The resulting document is returned to the caller, typically written to disk or displayed.

### Usage

```python
from autodocgenerator.factory.base_factory import DocFactory, IntroLinks, IntroText

# Prepare modules
factory = DocFactory(
    IntroLinks(),      # Generates a markdown table of links
    IntroText(),       # Generates a short project introduction
    # ... other modules can be added here
)

# `info` is produced by the post‑processing step
doc_text = factory.generate_doc(info)
```

### Important Notes
- Modules must be subclasses of `BaseModule`; otherwise `DocFactory` will raise a `TypeError` when calling `generate()`.  
- `generate()` should be **pure**: it must not modify `info` or produce side effects.  
- The factory is intentionally synchronous; if asynchronous generation is required, an async wrapper can be built on top.

---

<a name="intro-modules"></a>
## `autodocgenerator.factory.modules.intro`

### Purpose
Provides two introductory modules that format parts of the documentation:

1. **IntroLinks** – creates a markdown section listing all extracted HTML links.  
2. **IntroText** – generates a textual introduction based on global repository data.

Both modules rely on helpers from `preprocessor.postprocess`.

### Key Functions

| Function | Source | Purpose |
|----------|--------|---------|
| `get_all_html_links(data: str)` | `preprocessor.postprocess` | Parses `full_data` string to collect URLs. |
| `get_links_intro(links: list, lang: str)` | `preprocessor.postprocess` | Builds a language‑aware markdown table of the links. |
| `get_introdaction(global_data: dict, lang: str)` | `preprocessor.postprocess` | Crafts a short description of the repo from `global_data`. |

### Module Details

```python
class IntroLinks(BaseModule):
    def generate(self, info: dict):
        # 1. Extract all URLs from the full repo dump.
        links = get_all_html_links(info.get("full_data"))
        # 2. Format them into a markdown table respecting the chosen language.
        intro_links = get_links_intro(links, info.get("language"))
        return intro_links
```

```python
class IntroText(BaseModule):
    def generate(self, info: dict):
        # Generate a concise introduction from global metadata.
        intro = get_introdaction(info.get("global_data"), info.get("language"))
        return intro
```

### Inputs & Outputs
- **Input (`info`)**: dictionary that must contain at least:
  - `full_data` – raw repository text used for link extraction.
  - `global_data` – metadata dictionary (e.g., project name, author).
  - `language` – language code for localization (`"en"`, `"ru"`, …).
- **Output**: A markdown‑formatted string (either a links table or a paragraph).  
  The factory concatenates these with blank lines.

### Assumptions
- `info` keys exist; missing keys result in `None` passed to helper functions.  
- `get_all_html_links` returns a list; `get_links_intro` handles empty lists gracefully.  

### Integration
These modules are added to `DocFactory` during pipeline construction. They represent the first two sections of the final documentation and can be reordered or extended by adding more modules following the same pattern.

<a name="overview"></a>
## Overview

`manage.py` is the orchestration layer of the **Auto Doc Generator**.  
It pulls together the preprocessing, compression, and post‑processing stages described in the global architecture:

1. **CodeMix** → creates a unified text representation of the repository.  
2. **Compressor** → recursively summarises that text into a single string.  
3. **Spliter** → partitions large strings for the LLM and stitches the resulting documentation parts.  
4. **Factory / Modules** → adds introductory links and text to the final markdown.  
5. **Progress** → feeds status updates to a UI‑specific progress bar.

The file exposes a `Manager` class that executes this pipeline in a cache directory and writes the intermediate artefacts (`code_mix.txt`, `global_info.md`, `output_doc.md`). The `__main__` block demonstrates a typical usage flow.

---

<a name="manager-class"></a>
## `Manager` Class

| Attribute | Description |
|-----------|-------------|
| `CACHE_FOLDER_NAME` | Folder name where intermediate files are stored (`.auto_doc_cache`). |
| `FILE_NAMES` | Mapping of logical keys to file names. |
| `__init__` | Creates cache dir, stores project metadata, and sets up a progress bar. |

### Methods

| Method | Purpose | Key steps |
|--------|---------|-----------|
| `read_file_by_file_key(file_key)` | Loads the text content of a cached file. | Uses `get_file_path()` and opens file UTF‑8. |
| `get_file_path(file_key)` | Resolves full path inside cache folder. | `os.path.join(project_directory, CACHE_FOLDER_NAME, FILE_NAMES[file_key])`. |
| `generate_code_file()` | Builds the `code_mix.txt` file. | Instantiates `CodeMix` with `project_directory` and `ignore_files`; calls `build_repo_content()` to write the mix. |
| `generate_global_info_file(max_symbols, use_async)` | Summarises the whole repo into `global_info.md`. | Splits the mix into ≤ `max_symbols` chunks; runs `compress_to_one` (async‑or‑sync); writes result. |
| `generete_doc_parts(max_symbols, use_async)` | Creates detailed documentation sections in `output_doc.md`. | Calls `gen_doc_parts` or its async counterpart, passing the global info and original mix. |
| `factory_generate_doc_intro(doc_factory)` | Prepends an introductory section produced by a `DocFactory`. | Reads `global_info` and `output_doc`, packages data into a dict, calls `doc_factory.generate_doc()`, then writes the combined markdown. |

> **Note:** All methods update the progress bar after completing their step (`self.progress_bar.update_task()`).

---

<a name="integration"></a>
## Interaction Flow

```text
project_root ──► CACHE_FOLDER_NAME
               │
               ├─ code_mix.txt   ← CodeMix → (repo → mixed text)
               │
               ├─ global_info.md ← compress_to_one(splitted mix)
               │
               ├─ output_doc.md  ← gen_doc_parts(full mix, global info)
               │
               └─ output_doc.md  ← factory_generate_doc_intro
```

1. **CodeMix** walks the repository tree (skipping `ignore_files`) and serialises every file within `<file path="…"> … </file>` tags into a single UTF‑8 file.  
2. **split_data** breaks that file into manageable chunks; **compress_to_one** calls GPT iteratively to reduce each chunk until a single summary remains.  
3. **gen_doc_parts** (or `async_gen_doc_parts`) uses the global summary and original mix to generate section‑by‑section markdown, optionally asynchronously.  
4. **DocFactory** (configured with `IntroLinks` and `IntroText`) prepends a document intro that can include links extracted via `get_all_html_links`, etc.  

The manager delegates heavy lifting to the preprocessor modules while handling file I/O, progress updates, and cache maintenance.

---

<a name="usage-example"></a>
## Usage Example (from `__main__`)

```python
# Initialise UI progress
with Progress(...) as progress:
    settings = ProjectSettings("Auto Doc Generator")
    settings.add_info("global idea", "This project was created to help developers ...")

    mgr = Manager(
        r"C:\path\to\repo",
        settings,
        ignore_list,
        progress_bar=LibProgress(progress),
        language="en"
    )

    mgr.generate_code_file()
    mgr.generate_global_info_file(use_async=True, max_symbols=5000)
    mgr.generete_doc_parts(use_async=True, max_symbols=4000)
    mgr.factory_generate_doc_intro(
        DocFactory(IntroLinks(), IntroText())
    )
```

After execution, the cache contains the three artefacts and `output_doc.md` holds the final documentation ready for publishing.

--- 

**Key assumptions**

- `project_directory` contains a valid Python repo.  
- GPT model is configured globally inside `AsyncGPTModel` (imported but not used directly in this file).  
- Progress bar is a `BaseProgress` subclass; `LibProgress` adapts `rich.progress.Progress`.  

This documentation covers the responsibilities of `manage.py`, its methods, and its role within the overall Auto Doc Generator pipeline.

<a name="code-mix"></a>
## CodeMix – Repository-to-Text Converter

**Purpose**  
Turns any local source tree into a single UTF-8 text file that the downstream **compressor** can summarise.  
The produced file is the *only* input that the LLM ever sees, so the quality of the ignore rules directly affects token usage and final documentation accuracy.

**Responsibility**  
- Walk the directory tree once, honouring a list of glob-style ignore patterns.  
- Emit a human-readable tree preview (for quick checks) followed by the machine-friendly block  
  `<file path="relative/path">content</file>` for every non-ignored file.  
- Guarantee that the output is deterministic (paths are sorted) and serialisable (plain text).

**Entry Points**  
`CodeMix(root_dir, ignore_patterns)` → `build_repo_content(output_file)`

**Key Methods**  
- `should_ignore(path: Path) -> bool`  
  Checks the relative path, its basename **and** every path component against the pattern list.  
  This three-way match catches folders (`__pycache__`), extensions (`*.pyc`) and composite names (`env/lib/python3.11/site-packages`).  
- `build_repo_content(output_file)`  
  Two-phase walk:  
  1. directories/files → indented tree.  
  2. files only → wrapped content blocks.  
  Any read error is captured inline instead of aborting the whole run.

**Inputs / Side Effects**  
**In:** file-system tree under `root_dir`.  
**Out:** `output_file` (default `repomix-output.txt`) overwritten atomically.  
**Side effect:** reads every non-ignored file into memory once; no other I/O.

**Interaction with the Rest of the System**  
The compressor expects a list whose single element is the text of this file; therefore  
`repo_text = Path("repomix-output.txt").read_text(encoding="utf-8")`  
is the usual next step before calling `compress_to_one(...)`.

**Default Ignore List**  
`ignore_list` is a ready-made set of binary, cache, IDE and environment folders/files.  
Pass a custom list or append to the global one to tailor ingestion per project.

**Typical Usage (inside the pipeline)**  
```python
from autodocgenerator.preprocessor.code_mix import CodeMix, ignore_list
CodeMix("~/repo", ignore_patterns=ignore_list).build_repo_content("repo_mix.txt")
```

**Assumptions / Limits**  
- File names must be representable in UTF-8; otherwise `errors="ignore"` drops bad bytes.  
- Symbolic links are *not* followed (`rglob` default).  
- Very large binaries that survive the ignore list will bloat the output; review patterns carefully.

<a name="compressor"></a>
## Compressor – GPT-driven summarisation loop

**Purpose**  
Reduce an arbitrarily long list of text chunks to a single concise summary by repeatedly asking GPT to compress *compress_power* items at a time until only one remains.

**Where it lives in the pipeline**  
After `CodeMix` has produced the monolithic `repo_mix.txt`, `compress_to_one` is invoked with that file split into a list of strings (one per file or per fixed-size block).  
The final string is the documentation that will later be written to disk or displayed in the UI.

**Key entry point**  
`compress_to_one(data, project_settings, compress_power=4, use_async=False, progress_bar)`

**Synchronous path (default)**  
1. `compress_and_compare` instantiates **one** `GPTModel`.  
2. Iterates over `data`, concatenates every `compress_power` summaries into one new chunk.  
3. Updates the shared `progress_bar` after each element.  
4. Returns the shortened list → loop repeats until `len(data) == 1`.

**Asynchronous path (`use_async=True`)**  
1. `async_compress_and_compare` spawns up to **4 concurrent** requests (`asyncio.Semaphore(4)`).  
2. Each task uses an independent `AsyncGPTModel` session.  
3. `asyncio.gather` collects answers, joins them into the next iteration list.  
4. Still respects the same progress bar interface.

**Lower-level helper**  
`compress(data, project_settings, model, compress_power)`  
Builds the prompt stack:  
- system: `project_settings.prompt` (global context)  
- system: `get_BASE_COMPRESS_TEXT(...)` (dynamic compression instructions)  
- user: the concrete chunk  
Returns the model answer string.

**Inputs / Assumptions**  
- `data`: non-empty list of UTF-8 strings.  
- `project_settings`: carries the persistent prompt prefix and project metadata.  
- `compress_power ≥ 2`; automatically lowered to 2 when the remaining list is too small.  
- `progress_bar` implements `create_new_subtask`, `update_task`, `remove_subtask`.  
- All model classes expose `get_answer_without_history(prompt:list)->str` (sync or async).

**Side effects**  
- Network calls to the GPT backend.  
- Progress-bar UI updates.  
- CPU-bound event-loop work when async.

**Outputs**  
Single summary string – the last remaining element after the loop.

<a name="postprocess"></a>
## Post-processing helpers – turning raw GPT output into a navigable document

**Purpose**  
These small utilities are executed **after** the compressor has produced a long markdown string.  
They extract headings, build anchor links, and ask the model for optional intros so the final documentation page is self-contained and easy to navigate.

**Key functions**  
- `generate_markdown_anchor(header: str) → "#some-header"`  
  Normalises Unicode, lower-cases, replaces spaces with hyphens, strips symbols, collapses dashes.  
  The anchor is **identical** to the one GitHub generates, therefore the table-of-contents links jump to the correct place.

- `get_all_topics(data: str) → (topics, links)`  
  Scans for every `## Heading` in the markdown, returns two aligned lists:  
  - human-readable topic titles  
  - generated anchors (`#topic-title`) ready to be wrapped in `[title](#topic-title)`.

- `get_all_html_links(data: str) → list[str]`  
  Returns the values of `<a name="…">` already present in the text (used when the compressor itself has inserted anchors).

- `get_links_intro(links, language="en") → markdown`  
  Calls `GPTModel` once with `BASE_INTRODACTION_CREATE_TEXT` and the list of links.  
  The model writes a short paragraph that **describes what the links represent** (e.g. “The following sections cover …”).  
  Returned markdown is injected at the top of the final file.

- `get_introdaction(global_data, language="en") → markdown`  
  Same pattern, but the prompt is `BASE_INTRO_CREATE` and the input is the **whole compressed documentation**.  
  Produces a high-level project overview that is inserted **before** the first heading.

**Interaction with the rest of the system**  
- Called by the orchestration layer **after** `compress_to_one` finishes and **before** the result is written to disk.  
- Expects the constants `BASE_INTRO_CREATE` and `BASE_INTRODACTION_CREATE_TEXT` from `engine.config.config`.  
- Uses the **synchronous** `GPTModel.get_answer_without_history`; latency is negligible because only one or two extra calls are made.

**Inputs / outputs**  
- Input: raw markdown string (possibly several thousand tokens).  
- Output: small markdown fragments (intros) or lists of strings (topics / links).  
- Side effects: none (pure functions except for the two GPT calls).

**Assumptions**  
- Markdown headings use `## ` exactly (no leading spaces, no trailing hashes).  
- Anchors are inserted **after** compression, so the compressor does **not** need to know about them.

<a name="doc-part-generator"></a>

### Responsibility  
Turn the monolithic `repo_mix.txt` produced by `CodeMix` into human-readable documentation **one chunk at a time**.  
It guarantees that no single GPT request exceeds the token limit by:

1. Splitting the input into **overlapping** parts (`split_data`).  
2. Calling GPT **serially** (`gen_doc_parts`) or **concurrently** (`async_gen_doc_parts`).  
3. Carrying a **sliding 3 kB context** (`prev_info`) from the previous part so the model keeps narrative continuity.

---

### Interaction with the rest of the system  
| Component | Relation |
|-----------|----------|
| `CodeMix` | upstream – supplies the raw text to document |
| `BaseProgress` | injected – reports progress to the active UI (CLI, GUI, web) |
| `GPTModel / AsyncGPTModel` | downstream – performs the actual summarisation |
| `compress_to_one` | orthogonal – can be used **after** this stage if further compression is required |

---

### Key functions & classes

| Name | Purpose |
|------|---------|
| `split_data(text, max_symbols)` | Greedy packer that keeps every fragment ≤ `max_symbols * 1.25`; oversize fragments are halved until they fit. Returns `List[str]` ready for GPT. |
| `write_docs_by_parts(...)` | Synchronous GPT caller. Builds the prompt stack (`BASE_PART_COMPLITE_TEXT`, `global_info`, optional `prev_info`) and strips Markdown fences from the answer. |
| `async_write_docs_by_parts(...)` | Same logic but `async`; obeys the `semaphore` (4 concurrent requests by default) and calls `update_progress` when done. |
| `gen_doc_parts(...)` | Blocking loop that walks through `split_data`, accumulates the final document and keeps the last 3000 chars as context for the next iteration. |
| `async_gen_doc_parts(...)` | Creates a list of coroutines, gathers them, concatenates the returned fragments and returns the complete documentation string. |

---

### Inputs / Outputs / Side effects

**Inputs**  
- `full_code_mix` – whole content of `repo_mix.txt`  
- `global_info` – static project header (name, purpose, language)  
- `max_symbols` – soft ceiling for one GPT request (typ. 15 000)  
- `language` – ISO code used in the system prompt  
- `progress_bar` – subclass of `BaseProgress`

**Output**  
- Single `str` – concatenated documentation sections, each separated by two newlines.

**Side effects**  
- Progress-bar tasks are created/removed.  
- GPT model is billed for `len(split_data)` requests.  
- No disk writes – the caller decides what to do with the returned string.

---

### Assumptions & limits
- GPT answers are **not** merged or diffed; continuity relies on the 3 kB sliding window.  
- `max_symbols` is counted as `len(str)` – not tokens – so keep a safety margin.  
- Concurrent mode keeps **4** open connections; raising the semaphore increases throughput **and** cost.

## <a name="progress_base"></a>Progress handling – `autodocgenerator/ui/progress_base.py`

### Overview  
`progress_base.py` provides a tiny abstraction layer that lets the **compression pipeline** (`compress_to_one`) report its work to any UI‑compatible progress bar.  
The module defines a **no‑op base class** (`BaseProgress`) used when the caller does not need visual feedback, and a concrete implementation (`LibProgress`) that wraps **Rich Progress** – the default progress UI shipped with the library.

### Why it exists  
* The compressor can run **synchronously** or **asynchronously** and may process many intermediate chunks.  
* UI code (CLI, GUI, notebooks) should not depend on the internal compression logic.  
* By passing a `BaseProgress`‑compatible object to `compress_to_one`, the pipeline can **create, update, and clean up** sub‑tasks without knowing the concrete UI library.

### Classes

| Class | Purpose | Key methods |
|------|----------|--------------|
| **`BaseProgress`** | Minimal contract – does nothing unless overridden. | `create_new_subtask(name, total_len)`, `update_task()`, `remove_subtask()` |
| **`LibProgress`** | Rich‑based visual progress bar used by the default CLI. Inherits the contract from `BaseProgress`. | `__init__(progress, total=4)`, `create_new_subtask(name, total_len)`, `update_task()`, `remove_subtask()` |

#### `BaseProgress`
```python
class BaseProgress:
    def __init__(self):
        pass

    def create_new_subtask(self, name: str, total_len: int):
        ...

    def update_task(self):
        ...

    def remove_subtask(self):
        ...
```
* **Responsibility** – Define the public API expected by the rest of the system.  
* **Assumptions** – Methods are deliberately left as `...` (Ellipsis) so that static type‑checkers recognise them as abstract; at runtime they simply do nothing.  
* **Side effects** – None.

#### `LibProgress`
```python
class LibProgress(BaseProgress):
    def __init__(self, progress: Progress, total=4):
        super().__init__()
        self.progress = progress
        self._base_task = self.progress.add_task("General progress", total=total)
        self._cur_sub_task = None

    def create_new_subtask(self, name, total_len):
        self._cur_sub_task = self.progress.add_task(name, total=total_len)

    def update_task(self):
        if self._cur_sub_task is None:
            self.progress.update(self._base_task, advance=1)
        else:
            self.progress.update(self._cur_sub_task, advance=1)

    def remove_subtask(self):
        if self._cur_sub_task is not None:
            self._cur_sub_task = None
```
* **Responsibility** – Translate the abstract progress calls into Rich operations.  
* **Interaction with the system** – Instances are passed to `compress_to_one(..., progress_bar=LibProgress(...))`.  
  * `create_new_subtask` is invoked when the compressor starts a new compression round (e.g., compressing a batch of chunks).  
  * `update_task` is called after each successful model request, advancing the appropriate Rich task.  
  * `remove_subtask` signals that the current round finished, allowing the base task to continue.  
* **Inputs**  
  * `progress` – a `rich.progress.Progress` object created by the caller (usually `Progress()` in a `with` block).  
  * `total` – expected number of top‑level steps (default 4, matching the four compression passes).  
* **Outputs** – Visual updates in the terminal; no return values.  
* **Side effects** – Mutates the internal Rich progress state and holds references to task IDs (`_base_task`, `_cur_sub_task`).  

### Typical usage pattern
```python
from rich.progress import Progress
from autodocgenerator.ui.progress_base import LibProgress
from autodocgenerator.preprocessor.compressor import compress_to_one
from autodocgenerator.preprocessor.settings import ProjectSettings

settings = ProjectSettings(prompt="Summarise repository.")
data = [...]                     # list of text chunks

with Progress() as rich_progress:
    prog = LibProgress(rich_progress, total=4)
    result = compress_to_one(
        data=data,
        project_settings=settings,
        compress_power=3,
        use_async=True,
        progress_bar=prog,
    )
```
* The `with Progress()` block ensures proper cleanup of Rich resources.  
* `compress_to_one` treats `prog` as a `BaseProgress` instance, calling the three contract methods at the appropriate moments.

### Extensibility
* **Custom UI** – Implement a new class inheriting from `BaseProgress` and override the three methods to drive a Qt progress bar, a Jupyter widget, etc.  
* **No UI** – Pass the default `BaseProgress()` (or simply omit the argument if the function supplies it) to run silently, useful for automated tests.

### Summary
`progress_base.py` decouples the core compression logic from any particular progress‑display implementation.  
`BaseProgress` defines the minimal contract; `LibProgress` supplies a ready‑to‑use Rich‑based visual feedback that integrates seamlessly with the rest of the **Auto Doc Generator** pipeline.

