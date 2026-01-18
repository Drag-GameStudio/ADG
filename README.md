## Executive Navigation Tree

- 📂 Core Engine  
  - [engine_init](#engine_init)  
  - [config-module-overview](#config-module-overview)  
  - [factory](#factory)  
  - [manager-class](#manager-class)  

- ⚙️ Documentation Processing  
  - [get_all_topics](#get_all_topics)  
  - [get_all_html_links](#get_all_html_links)  
  - [compressor](#compressor)  

- 🔧 LLM Interaction  
  - [gptmodel](#gptmodel)  
  - [get_links_intro](#get_links_intro)  
  - [get_introdaction](#get_introdaction)

**Project Overview – Code‑to‑README Documentation Generator**

---

### 1. Project Title  
**DocuSynth – Automated README Generation for Python Repositories**

---

### 2. Project Goal  
DocuSynth automatically produces a human‑readable README‑style document for any Python codebase. By traversing the repository, compressing the source tree, and leveraging a language model, it delivers a concise, well‑structured overview that can be used as a project’s main documentation or as a quick reference for new contributors.

---

### 3. Core Logic & Principles  

| Layer | Responsibility | Key Techniques |
|-------|----------------|----------------|
| **File System Walker** | Enumerates all non‑ignored files, builds an in‑memory representation (`CodeMix`) of the repository hierarchy. | Recursive directory traversal, glob/regex ignore patterns. |
| **Compression** | Serialises the `CodeMix` tree and stores a lightweight `.json.gz` “global info” file for fast look‑ups. | JSON serialization + Gzip compression. |
| **Chunking** | Splits the compressed data into token‑size‑constrained chunks that fit within the limits of the target GPT model. | `split_data()` utility, token‑count estimation. |
| **Document Generation** | For each chunk, a language model generates a short, coherent description. The `DocFactory` stitches these into a single introduction section. | Prompt engineering, iterative prompt‑response, context‑aware summarisation. |
| **Progress Reporting** | A Rich‑based progress bar (`LibProgress`) visualises the status of each heavy step (walking, compressing, chunking, LLM calls). | `rich.progress.Progress`, custom `BaseProgress` abstraction. |
| **Asynchronous Support** | Parallelises LLM calls via `async_write_docs_by_parts` to reduce wall‑clock time. | `asyncio`, `await` syntax, concurrent task management. |

The high‑level orchestration is performed by the `Manager` façade:

1. **Collect Code** – `generate_code_file()` walks the file system and serialises a `CodeMix` object.  
2. **Global Info** – `generate_global_info_file()` compresses the `CodeMix` into a `.json.gz`.  
3. **Chunking** – `generate_doc_parts()` splits the compressed data into manageable pieces.  
4. **Intro Generation** – `factory_generate_doc_intro()` delegates to `DocFactory`, which uses `IntroLinks` and `IntroText` helpers to produce the final README‑style text.

---

### 4. Key Features  

- **Automatic Repository Analysis** – Recursively walks any Python project, respecting custom ignore lists.  
- **Efficient Storage** – Compresses the entire code tree into a single, lightweight file for quick reuse.  
- **Token‑Aware Chunking** – Ensures each LLM request stays within model limits, preventing truncation or errors.  
- **Rich Progress UI** – Real‑time feedback via a terminal progress bar (supports both sync and async modes).  
- **Synchronous & Asynchronous APIs** – `gen_doc_parts()` for blocking execution, `async_gen_doc_parts()` for concurrent processing.  
- **Extensible Factories** – `DocFactory` can be swapped or extended to change the style or depth of the generated documentation.  
- **Language‑agnostic** – Optional target language parameter allows the README to be produced in any language supported by the LLM.  

---

### 5. How to Run  

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/yourorg/docusynth.git
   cd docusynth
   ```

2. **Create a Virtual Environment**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up LLM Credentials**  
   The project uses an OpenAI‑compatible API. Export your key:
   ```bash
   export OPENAI_API_KEY="sk-…"
   ```

5. **Run the Generator (Synchronous)**  
   ```python
   from ui.progress_base import LibProgress
   from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
   from manager import Manager

   # Initialise progress bar
   progress = Progress(
       SpinnerColumn(),
       TextColumn("[progress.description]{task.description}"),
       BarColumn(),
       TaskProgressColumn(),
       TimeRemainingColumn()
   )
   lib_progress = LibProgress(progress, total=5)  # adjust total as needed

   # Create manager for a target repository
   mgr = Manager(
       project_path="/path/to/your/python/project",
       ignore_list=["__pycache__", ".git", "tests"],
       progress=lib_progress,
       target_language="en"
   )

   # Execute pipeline
   mgr.generate_code_file()
   mgr.generate_global_info_file()
   mgr.generate_doc_parts()
   mgr.factory_generate_doc_intro()
   ```

6. **Run the Generator (Asynchronous)**  
   ```python
   import asyncio
   from doc_generator import async_gen_doc_parts

   async def main():
       full_code_mix = """..."""          # obtained from Manager
       global_info = "Project: Example Library. Language: English."
       max_symbols = 2000
       language = "en"

       final_doc = await async_gen_doc_parts(
           full_code_mix,
           global_info,
           max_symbols,
           language,
           lib_progress
       )
       print(final_doc)

   asyncio.run(main())
   ```

---

### 6. Dependencies  

| Library | Purpose | Version |
|---------|---------|---------|
| `rich` | Terminal progress bars and UI | `>=13.0` |
| `tqdm` | Optional fallback progress bar | `>=4.0` |
| `openai` | LLM client (or any compatible API wrapper) | `>=1.0` |
| `gzip` | Compression of the `CodeMix` JSON | Standard library |
| `json` | Serialization of repository metadata | Standard library |
| `asyncio` | Asynchronous execution | Standard library |
| `typing` | Type hints | Standard library |

> **Note**: The `requirements.txt` file contains the exact pinning used in the project. If you wish to use a different LLM provider, replace the `GPTModel` wrapper with a compatible implementation.

---

**DocuSynth** delivers a seamless, end‑to‑end solution for turning raw Python code into a polished, LLM‑generated README, making onboarding faster and documentation maintenance effortless.

 

<a name="engine_init"></a>
## Engine Initialization
The `engine` package is the core of the documentation generator, responsible for orchestrating the entire process. This module serves as the entry point for the engine, importing and exposing the necessary components.

```python
# engine/__init__.py

"""
Engine initialization module.
"""

from .config.config import Config
from .models.gpt_model import GPTModel
from .models.model import Model

__all__ = [
    'Config',
    'GPTModel',
    'Model'
]
```

This module imports the `Config`, `GPTModel`, and `Model` classes from their respective submodules, making them available for use throughout the project. The `__all__` variable specifies the classes that are exported by this module, allowing them to be imported by other parts of the project.

The `Config` class is responsible for managing the engine's configuration, while the `GPTModel` and `Model` classes represent the language models used for generating documentation. By importing these classes here, we can easily access and use them throughout the engine.

<a name="config-module-overview"></a>
## 📄 Config Module Overview  

The **`engine/config/config.py`** file centralises all static prompt‑templates and runtime constants used by the AutoDoc pipeline.  
These strings drive the behaviour of the three processing stages:

1. **System‑level instruction** – tells the LLM how to analyse each incoming code fragment.  
2. **Part‑completion instruction** – guides the LLM to produce concise, context‑aware documentation for a single snippet.  
3. **Intro‑generation instruction** – instructs a specialised “Executive Navigation Tree” creator to prune and organise Markdown links.  
4. **Project‑overview instruction** – asks the LLM to compose a full project summary (title, goal, core logic, etc.).  

Additionally, the module supplies a small helper **`get_BASE_COMPRESS_TEXT`** that builds a dynamic prompt for summarising very large code blocks, and it loads environment variables required for model selection.

---

<a name="constants-and-templates"></a>
## 🔑 Constants & Prompt Templates  

| Name | Type | Purpose |
|------|------|---------|
| `BASE_SYSTEM_TEXT` | `str` | Base system prompt. Instructs the model to *explain every function/class*, *preserve accumulated context*, and *never skip details*. |
| `BASE_PART_COMPLITE_TEXT` | `str` | Prompt for the *part‑completion* stage. Requests a ~2 k‑character documentation piece, anchored titles, and a focus on component responsibilities, interactions, and side‑effects. |
| `BASE_INTRODACTION_CREATE_TEXT` | `str` | Prompt for the *Executive Navigation Tree* generator. Enforces the “30 % rule”, exact anchor preservation, two‑level hierarchical grouping, and zero‑hallucination output. |
| `BASE_INTRO_CREATE` | `str` | Prompt for the *project overview* writer. Defines the required sections (title, goal, core logic, features, run‑instructions, dependencies). |
| `MODELS_NAME` | `list[str]` | Ordered list of model identifiers the system may select when calling the LLM backend. |
| `API_KEY` | `str` | Loaded from the environment (`.env`) – used for authenticating requests to the chosen model provider. |

These constants are imported by the **manager**, **factory**, and **UI** layers to feed the appropriate prompt to the language model at each step.

---

<a name="dynamic-compression-prompt"></a>
## 🛠️ `get_BASE_COMPRESS_TEXT(start, power)`  

```python
def get_BASE_COMPRESS_TEXT(start, power):
    return f"""
    You will receive a large code snippet (up to ~{start} characters).
    …
    Summary: No more than ~{int(start / power)} characters.
    …
    ```python
    # Real-world usage based on the code above
    """
```

* **Responsibility** – Generates a tailored prompt for handling *very large* code fragments (e.g., > 10 k characters).  
* **Inputs**  
  * `start` – Approximate maximum size of the incoming snippet (characters).  
  * `power` – Divisor that determines the allowed length of the summary (`start / power`).  
* **Outputs** – A multi‑line string containing:  
  * An instruction block describing analysis, summarisation length, and a strict usage‑example requirement.  
  * An opening Markdown code‑fence (` ```python `) that callers will later close with their concrete example.  

The function is invoked by the **compression/orchestration** component when the raw repository dump exceeds the LLM token window, ensuring the model receives a concise, well‑structured request.

---

<a name="environment-loading"></a>
## 🌍 Environment Loading  

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
```

* Loads `.env` at runtime, exposing `API_KEY` for authenticated model calls.  
* The variable is referenced by the **`GPTModel`** wrapper (outside this snippet) to configure HTTP headers or SDK credentials.

---

<a name="interaction-with-other-modules"></a>
## 🔗 Interaction with the Rest of the System  

| Component | How it uses this module |
|-----------|------------------------|
| **`manager.Manager`** | Pulls the prompt constants to build messages for the LLM during each pipeline stage (code collection → global info → doc parts → intro generation). |
| **`factory.base_factory.DocFactory`** | Receives `BASE_PART_COMPLITE_TEXT` and `BASE_INTRO_CREATE` to shape its internal templating logic. |
| **`ui.progress_base.LibProgress`** | Unrelated to prompts but shares the same import path; both live under `engine/config`. |
| **`model.wrapper.GPTModel`** | Reads `API_KEY` and selects a model from `MODELS_NAME` when constructing request payloads. |
| **`engine/compress`** (hypothetical) | Calls `get_BASE_COMPRESS_TEXT` to produce a custom prompt when splitting oversized files. |

All prompts are **static, human‑readable strings**; they are never mutated at runtime, guaranteeing deterministic behaviour across executions.

---

<a name="assumptions-and-side-effects"></a>
## ⚙️ Assumptions & Side Effects  

* **Assumptions**  
  * `.env` exists and contains a valid `API_KEY`.  
  * The LLM provider accepts the supplied prompt format (Markdown with fenced code blocks).  
  * `MODELS_NAME` ordering reflects priority; the system will fall back to the next entry if the first fails.  

* **Side Effects**  
  * Loading the environment may raise `FileNotFoundError` if `.env` is missing (handled elsewhere).  
  * The function `get_BASE_COMPRESS_TEXT` performs only string interpolation – no I/O or state changes.  

---

<a name="summary"></a>
## 📌 Summary  

`engine/config/config.py` is the *single source of truth* for every textual instruction fed to the language model and for the runtime credentials needed to access it. By separating prompts, model identifiers, and environment loading into this module, the rest of the codebase can stay focused on orchestration, file‑system traversal, and UI concerns while consistently reusing the same high‑quality, centrally‑maintained prompts. This design simplifies updates (e.g., tweaking the “30 % rule”) and ensures that all pipeline stages speak a unified language to the LLM.

<a name="overview"></a>
## Overview
The *engine* package implements a thin wrapper around the **Groq** LLM API.  The models keep a chat history, cycle through a shuffled list of available model names, and automatically retry with the next model when a request fails.  The *factory* package turns collected data into a human‑readable introduction by delegating to a set of `BaseModule` implementations (`IntroLinks`, `IntroText`).

<a name="history"></a>
## History – `engine\models\model.py`
* `History`  
  Stores a list of chat messages.  The constructor seeds the history with a system prompt (`BASE_SYSTEM_TEXT`).  `add_to_history(role, content)` appends a message dict.

* `ParentModel`  
  Common base for sync/async models: keeps the API key, the current model index, and a shuffled copy of `MODELS_NAME` (`regen_models_name`) that is used for retrying.

* `Model` & `AsyncModel`  
  Provide high‑level convenience methods  
  ```python
  get_answer(prompt)          # user → model → assistant
  get_answer_without_history(prompt)   # raw prompt list
  ```  
  The actual LLM call is delegated to `generate_answer()` which subclasses override.

<a name="gptmodel"></a>
## Groq Models – `engine\models\gpt_model.py`
Both classes inherit the retry logic from `ParentModel`.

* **`GPTModel`** (synchronous)  
  * `client` is a `groq.Groq`.  
  * `generate_answer()` builds the `messages` list from history or a supplied prompt.  
  * A `while` loop picks `self.regen_models_name[self.current_model_index]` and attempts a completion with `temperature=0.3`.  
  * On exception it resets the index and removes the failed model, looping until success or all models are exhausted.

* **`AsyncGPTModel`** (asynchronous)  
  Similar logic but uses `AsyncGroq` and `await` on `chat.completions.create`.  
  The temperature is omitted (defaults to 0.3 in Groq), and the same retry pattern applies.

Both raise `Exception("all models do not work")` if every model fails.

<a name="factory"></a>
## Document Generation – `factory` package
* **`BaseModule`** (abstract) – defines a single `generate(info: dict)` method.

* **`DocFactory`** – collects arbitrary modules and concatenates their outputs:
  ```python
  output += module.generate(info) + "\n\n"
  ```
  It is the orchestrator that builds the final intro document.

* **Modules (`factory\modules\intro.py`)**  
  * `IntroLinks` – extracts all HTML links from `info["full_data"]` with `get_all_html_links`, then formats them into a language‑specific table via `get_links_intro`.  
  * `IntroText` – builds a prose introduction from `info["global_data"]` with `get_introdaction`.

These modules rely on the `preprocessor.postprocess` helpers to transform raw data before rendering.

<a name="interaction"></a>
## Interaction Flow
1. **LLM Interaction** – `GPTModel`/`AsyncGPTModel` receive a user prompt, record it in history, call `generate_answer`, and return the assistant reply.  
2. **Documentation Pipeline** – `DocFactory` is instantiated with `IntroLinks` and `IntroText`.  
3. `DocFactory.generate_doc(info)` runs each module, gathering a link table and an introductory paragraph, which are then stitched together into a ready‑to‑use README snippet.

All classes are intentionally lightweight: the heavy lifting (token counting, chunking, compression) happens elsewhere in the project, while these files focus on *communication with the LLM* and *structured generation of intro text*.

---

## <a name="manager-class"></a> Manager Class
The `Manager` class is the high-level facade that orchestrates the entire documentation generation pipeline. It is responsible for managing the project directory, ignoring specific files, and generating the documentation.

### <a name="responsibilities"></a> Responsibilities
The `Manager` class has the following responsibilities:

* Managing the project directory and cache folder
* Ignoring specific files and directories
* Generating the code file
* Generating the global info file
* Generating the documentation parts
* Generating the documentation intro

### <a name="interactions"></a> Interactions
The `Manager` class interacts with the following components:

* `CodeMix`: used to build the repository content
* `DocFactory`: used to generate the documentation intro
* `LibProgress`: used to report progress
* `AsyncGPTModel`: used to generate documentation parts asynchronously

### <a name="key-functions"></a> Key Functions
The `Manager` class has the following key functions:

* `generate_code_file`: generates the code file
* `generate_global_info_file`: generates the global info file
* `generete_doc_parts`: generates the documentation parts
* `factory_generate_doc_intro`: generates the documentation intro

### <a name="logic-flow"></a> Logic Flow
The logic flow of the `Manager` class is as follows:

1. Initialize the project directory, ignore list, language, and progress bar
2. Create the cache folder if it does not exist
3. Generate the code file
4. Generate the global info file
5. Generate the documentation parts
6. Generate the documentation intro

### <a name="example-usage"></a> Example Usage
```python
with Progress(
    SpinnerColumn(),          
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),               
    TaskProgressColumn(),     
) as progress:
    manager = Manager(r"C:\Users\huina\Python Projects\Impotant projects\AutoDocGenerateGimini", ignore_list, progress_bar=LibProgress(progress), language="en")

    manager.generate_code_file()
    manager.generate_global_info_file(use_async=True, max_symbols=7000)
    manager.generete_doc_parts(use_async=True, max_symbols=5000)
    manager.factory_generate_doc_intro(
        DocFactory(
            IntroLinks(),
            IntroText(),
        )
    )
```
This example demonstrates how to use the `Manager` class to generate documentation for a project. The `Manager` class is initialized with the project directory, ignore list, language, and progress bar. The `generate_code_file`, `generate_global_info_file`, `generete_doc_parts`, and `factory_generate_doc_intro` methods are then called to generate the documentation.

<a name="CodeMix"></a>
## `CodeMix` – Repository‑wide source collector  

The **CodeMix** class lives in *preprocessor/code_mix.py* and is the first step of the doc‑generation pipeline.  
Its responsibility is to walk a Python (or any) project directory, filter out files that should not participate in the documentation (virtual‑env folders, caches, binary artefacts, etc.) and produce a single text file that contains:

1. **A tree view** of the repository structure (folders and file names).  
2. **The raw content of every kept file**, wrapped in a custom XML‑like tag `<file path="...">`.  

### How it fits into the system  

`Manager.generate_code_file()` (see the global description) creates a `CodeMix` instance, calls `build_repo_content()`, and stores the resulting *codemix.txt*.  
The produced file is later fed to the **compressor** module, which chunks and compresses the text with a LLM before the introduction factory builds the final README.

### Key attributes  

| Attribute | Type | Meaning |
|-----------|------|---------|
| `root_dir` | `Path` | Absolute path of the project root that will be scanned. |
| `ignore_patterns` | `list[str]` | Glob‑style patterns that tell the scanner which paths to skip. |

### Core methods  

| Method | Signature | What it does |
|--------|-----------|--------------|
| `should_ignore(self, path: Path) -> bool` | Checks a given `Path` against every pattern in `ignore_patterns`. Returns `True` if the file/folder must be omitted. |
| `build_repo_content(self, output_file: str = "repomix-output.txt")` | Writes the repository structure and file contents to `output_file`. |
| `__init__(self, root_dir=".", ignore_patterns=None)` | Normalises `root_dir` to an absolute `Path` and stores the ignore list (empty list if `None`). |

#### `should_ignore` logic  

* Computes the path relative to `root_dir`.  
* For each pattern it returns `True` when **any** of the following matches:  
  * The whole relative path (`fnmatch`).  
  * The basename of the path.  
  * Any individual component of the path (`path.parts`).  

This generous matching ensures that patterns like `"venv"` or `"*.pyc"` filter out both the folder itself and any files inside it.

#### `build_repo_content` flow  

1. Opens `output_file` for UTF‑8 writing.  
2. **Section 1 – Tree view**  
   * Iterates over `self.root_dir.rglob("*")` (recursive glob).  
   * Skips ignored items.  
   * Calculates depth (`len(relative.parts)`) to produce an indented visual tree (`"  "` per level).  
   * Writes directories with a trailing `/` and files without.  
3. Inserts a visual separator (`"="*20`).  
4. **Section 2 – Raw files**  
   * Re‑iterates the same recursive list.  
   * For each *file* that is not ignored:  
     * Writes a header `<file path="{relative_path}">`.  
     * Reads the file text (`read_text(..., errors="ignore")`) and dumps it verbatim.  
     * Adds a blank line after each file.  
   * Errors while reading (permission issues, binary files) are caught and written as `Error reading …`.  

**Side effects** – creates or overwrites the `output_file`; may produce console output if run as a script.

### Assumptions & constraints  

* All source files are UTF‑8 readable; binary data will be silently ignored by `errors="ignore"` (may produce garbled output).  
* `ignore_patterns` follow Unix‑style glob syntax; the list supplied in `ignore_list` covers typical Python project artefacts.  
* The directory tree fits in memory for the sorted iteration (reasonable for most projects).  

### Typical usage (as shown in the `__main__` block)  

```python
ignore_list = [...]   # predefined patterns
packer = CodeMix(
    root_dir=r"C:\Users\huina\Python Projects\Kwork\ClickerProject\ClickerApp",
    ignore_patterns=ignore_list
)
packer.build_repo_content("codemix.txt")
print("Файл успешно создан!")
```

The resulting *codemix.txt* is the raw input for the **compressor** step.

<a name="compressor"></a>
## `compressor` – LLM‑driven hierarchical compression  

Located in *preprocessor/compressor.py*, this module reduces the potentially huge *codemix.txt* into a compact representation that fits the token limits of the downstream LLM.  

### Role in the pipeline  

`Manager.generate_global_info_file()` calls `compress_to_one()` (exposed here).  
The function repeatedly groups text chunks, asks the LLM to summarise each group, and continues until a single compressed block remains.  
The final string is stored as the *global‑info* file, later split into parts for the introduction factory.

### Public API  

| Function | Purpose |
|----------|---------|
| `compress(data: str, model: Model, compress_power)` | Sends a single chunk to the LLM with a system prompt (generated by `get_BASE_COMPRESS_TEXT`) and returns the model’s answer. |
| `compress_and_compare(data: list, compress_power=4, progress_bar=BaseProgress())` | Synchronous version that processes a list of strings, groups them by `compress_power`, and concatenates the LLM responses per group. |
| `async_compress(... )` | Helper coroutine that compresses a single chunk under a semaphore (limits concurrent LLM calls). |
| `async_compress_and_compare(data: list, compress_power=4, progress_bar=BaseProgress())` | Asynchronous counterpart of `compress_and_compare`. |
| `compress_to_one(data: list, compress_power=4, use_async=False, progress_bar=BaseProgress())` | Orchestrator that repeatedly calls the (a)sync version until only one element remains; returns the final compressed string. |

### Interaction with other components  

* **Model layer** – imports `GPTModel` / `AsyncGPTModel` from `engine.models.gpt_model`. These wrappers expose `get_answer_without_history(prompt)` that talks to the OpenAI‑style API.  
* **Config layer** – `get_BASE_COMPRESS_TEXT` builds the system‑prompt that tells the LLM how aggressively to compress (`compress_power` influences the “compression ratio”).  
* **Progress UI** – All functions accept a `BaseProgress` (or subclass) instance to report sub‑task creation, incremental updates, and removal. This ties into the Rich‑based UI (`LibProgress`).  

### Data flow  

1. **Input** – `data` is a list of raw strings, each typically representing a file’s content (produced by `CodeMix`).  
2. **Chunking** – `compress_power` decides how many consecutive elements are merged before a compression call.  
3. **LLM call** – `compress` builds a two‑message prompt (`system` + `user`) and returns the model’s answer (a compressed summary).  
4. **Aggregation** – Results are concatenated into a new list whose length ≈ `ceil(len(data)/compress_power)`.  
5. **Iteration** – `compress_to_one` loops until the list size is `1`. The loop may adapt `compress_power` to `2` when the remaining list is small, preventing an infinite loop.  

### Side effects & assumptions  

* **Network I/O** – each `compress` call performs an HTTP request to the LLM service; failures raise exceptions upstream.  
* **Rate limiting** – the async version uses a semaphore with a hard‑coded concurrency of `4`. Adjust if the model’s rate limits differ.  
* **Deterministic ordering** – the order of chunks is preserved across iterations, ensuring that later summaries retain the original file ordering.  
* **Progress handling** – callers must provide a `BaseProgress` (or subclass) that implements `create_new_subtask`, `update_task`, and `remove_subtask`. The default `BaseProgress()` is a no‑op placeholder.  

### Example (synchronous)  

```python
from preprocessor.compressor import compress_to_one
from preprocessor.code_mix import CodeMix, ignore_list

# 1. Build raw repo text
cm = CodeMix(root_dir="my_project", ignore_patterns=ignore_list)
cm.build_repo_content("raw.txt")

# 2. Split raw file into per‑file strings (simplified)
with open("raw.txt", encoding="utf-8") as f:
    raw_sections = f.read().split("\n\n")   # each section = file header + content

# 3. Reduce to a single compressed blob
compressed = compress_to_one(raw_sections, compress_power=4, use_async=False)
print(compressed[:500])   # preview
```

The `compressed` string is later fed to `DocFactory` to generate the final README.  

<a name="preprocessor-postprocess"></a>
## `preprocessor/postprocess.py`

The **postprocess** module is a small utility layer that prepares the raw markdown/HTML fragments produced by the earlier stages of the documentation pipeline for final presentation and for feeding into the language‑model prompts.  
It lives in the *preprocessor* package because its functions are invoked right after the **spliter** has produced the chunked text but before the final README‑style document is assembled.

### Responsibilities
| What | How |
|------|-----|
|Create stable markdown anchors for section headers|`generate_markdown_anchor` normalises the header text and applies the GitHub‑flavoured anchor rules.|
|Extract a list of top‑level topics (`## …`) from a markdown string|`get_all_topics` scans the string, returns both the raw titles and their markdown anchors.|
|Extract custom HTML `<a name="…">` anchors used by the generator|`get_all_html_links` walks through the HTML markup and returns the raw name attributes.|
|Ask the LLM to write an *introduction* for a set of links|`get_links_intro` builds a system‑prompt + user‑prompt payload and calls `GPTModel.get_answer_without_history`.|
|Ask the LLM to write a *global introduction* for the whole repository|`get_introdaction` (note the historic typo) does the same, using a different system prompt template.|

### Key Functions  

| Function | Signature | Returns | Side‑effects |
|----------|-----------|---------|--------------|
|`generate_markdown_anchor(header: str) -> str`|Converts a heading into a slug|Markdown link like `#my-section`|None |
|`get_all_topics(data: str) -> tuple[list[str], list[str]]`|Parses markdown for `##` headings|`(titles, anchors)`|None |
|`get_all_html_links(data: str) -> list[str]`|Searches for `<a name="…">` blocks|List of raw anchor names|None |
|`get_links_intro(links: list[str], language: str = "en") -> str`|Calls the LLM with `BASE_INTRODACTION_CREATE_TEXT`|Generated paragraph describing the links|Network I/O via `GPTModel` |
|`get_introdaction(global_data: str, language: str = "en") -> str`|Calls the LLM with `BASE_INTRO_CREATE`|Generated global introduction|Network I/O via `GPTModel` |

### Interaction with the Rest of the System  

* **Input source** – The `data` argument for the extraction helpers is the markdown string produced by `spliter.split_data` (or a later aggregation step).  
* **Output consumption** – The lists of anchors are later fed to `DocFactory` (or a similar component) to build a Table‑of‑Contents and to pass to `get_links_intro`.  
* **LLM integration** – Both `get_links_intro` and `get_introdaction` instantiate `GPTModel` directly; they do **not** share a model instance with other parts of the pipeline, which keeps the functions stateless but may cause repeated authentication overhead.  

---

<a name="preprocessor-spliter"></a>
## `preprocessor/spliter.py`

The **spliter** module is the entry point for breaking a potentially huge markdown payload into chunks that respect the token limits of the downstream GPT model. Only the beginning of the implementation is shown, but its intent and contract are clear.

### Core Function  

```python
def split_data(data: str, max_symbols: int) -> list[str]:
    ...
```

* **Purpose** – Produce a list of strings, each ≤ `max_symbols` characters, while attempting to keep logical boundaries (e.g., file separators) intact.  
* **Parameters**  
  * `data` – The full markdown representation of the repository (usually the output of `Manager.generate_code_file`).  
  * `max_symbols` – Upper bound on the length of each chunk; derived from the token budget of the selected LLM.  
* **Return value** – `list[str]` where each element is a ready‑to‑send payload for `GPTModel`.  

### Partial Implementation Details  

* The function creates an empty `split_objects` list that will hold the final chunks.  
* It immediately splits the incoming `data` on the sentinel string `"<a name="preprocessor-postprocess"></a>
## `preprocessor/postprocess.py`

The **postprocess** module is a thin helper layer that turns the raw markdown generated by the *spliter* into a polished, link‑rich document and that asks the language model to write the introductory sections.  
It is invoked after the repository has been walked, serialized and split into chunks, but before the final README is assembled.

### Main Responsibilities  

| Responsibility | Implementation |
|----------------|----------------|
|Create deterministic markdown anchors for headings|`generate_markdown_anchor` |
|Extract top‑level markdown topics (`## …`) and their anchors|`get_all_topics` |
|Extract custom HTML anchors (`<a name="…">`)|`get_all_html_links` |
|Ask the LLM to produce a short intro that lists the extracted links|`get_links_intro` |
|Ask the LLM to produce a global project introduction|`get_introdaction` |

### Public Functions  

| Function | Signature | Returns | Side‑effects |
|----------|-----------|---------|--------------|
|`generate_markdown_anchor` | `header: str → str` | `"#my‑section"` – a GitHub‑compatible anchor | none |
|`get_all_topics` | `data: str → tuple[list[str], list[str]]` | `(titles, anchors)` where *titles* are the raw `##` headings and *anchors* are the markdown links produced by `generate_markdown_anchor` | none |
|`get_all_html_links` | `data: str → list[str]` | List of raw `<a name="…">` identifiers | none |
|`get_links_intro` | `links: list[str], language: str = "en" → str` | LLM‑generated paragraph that introduces the list of links | network call via `GPTModel.get_answer_without_history` |
|`get_introdaction` | `global_data: str, language: str = "en" → str` | LLM‑generated global project introduction | network call via `GPTModel.get_answer_without_history` |

#### `generate_markdown_anchor`
```python
def generate_markdown_anchor(header: str) -> str:
    anchor = header.lower()
    anchor = unicodedata.normalize('NFKC', anchor)
    anchor = anchor.replace(' ', '-')
    anchor = re.sub(r'[^a-z0-9\-_]', '', anchor)
    anchor = re.sub(r'-+', '-', anchor).strip('-')
    return f"#{anchor}"
```
*Normalises Unicode, replaces spaces with hyphens, strips disallowed characters, collapses repeated hyphens, and prefixes with `#`.*

#### `get_all_topics`
Walks the markdown string looking for the pattern `"\n## "` (level‑2 headings).  
For each heading it extracts the title up to the next newline, stores it, and finally builds a matching list of markdown anchors.

#### `get_all_html_links`
Searches for literal `<a name=` tags and returns the identifier that appears between the opening tag and the closing `</a>`.

#### `get_links_intro` / `get_introdaction`
Both functions instantiate a fresh `GPTModel`, construct a system‑prompt that forces the response language, inject a **template** from `engine.config.config` (`BASE_INTRODACTION_CREATE_TEXT` or `BASE_INTRO_CREATE`), and send the user payload (`links` or `global_data`).  
The model’s answer is returned unchanged.

### Interaction with the Rest of the System  

* **Input source** – The markdown string supplied to `get_all_topics`/`get_all_html_links` originates from `spliter.split_data` (or from the concatenated result of all chunks).  
* **Output consumer** – The generated lists of anchors are fed to the **DocFactory** (or similar) to build a Table‑of‑Contents. The textual introductions returned by `get_links_intro` and `get_introdaction` are concatenated with the per‑chunk documentation to form the final README.  
* **LLM coupling** – The functions directly create a `GPTModel` instance; they do not share a model object with other pipeline stages, keeping them stateless but incurring a new HTTP/SDK session per call.

---

<a name="preprocessor-spliter"></a>
## `preprocessor/spliter.py`

The **spliter** module is responsible for breaking a large markdown payload into smaller, model‑friendly pieces. Only the beginning of the implementation is shown, but its contract and intended behaviour are evident.

### Core Function  

```python
def split_data(data: str, max_symbols: int) -> list[str]:
    ...
```

| Parameter | Description |
|-----------|-------------|
|`data`|Complete markdown representation of the repository (produced by `Manager.generate_code_file`).|
|`max_symbols`|Maximum allowed character length for each chunk; derived from the token budget of the target LLM.|

| Return | Description |
|--------|-------------|
|`list[str]`|A sequence of markdown fragments, each *≤* `max_symbols` characters, ready to be sent to the language model.|

### Intended Algorithm (deduced from the partial code)

1. **Initial split** – The function first splits the whole document on the sentinel string `"

## <a name="overview"></a>Overview  
The snippet implements the *chunk‑based documentation generator* that talks to a GPT model.  
The core workflow is:  
1. **`split_data`** – divide a large string of code into token‑safe pieces.  
2. **`write_docs_by_parts`** – synchronously ask the model to generate a doc fragment for each piece.  
3. **`async_write_docs_by_parts`** – same logic but concurrently using an async model.  
4. **`gen_doc_parts` / `async_gen_doc_parts`** – orchestrators that iterate over all chunks, gather results, and report progress through a `BaseProgress` implementation.  

`BaseProgress`/`LibProgress` wrap a `rich.progress.Progress` bar so callers can track overall progress.

---

## <a name="split_data"></a>split_data(data, max_symbols)  
*Purpose:* Break `full_code_mix` into a list of strings, each ≤ `max_symbols`, while preserving file boundaries.  

*Logic flow:*  
1. Split the source by empty lines into `splited_by_files`.  
2. Re‑balance very large fragments: any element > 1.5×`max_symbols` is split in half until all fit.  
3. Greedily accumulate these fragments into `split_objects`, allowing each to grow up to 1.25×`max_symbols` to reduce the number of calls to the model.  

*Assumptions:*  
- `data` is plain text.  
- `max_symbols` is a token‑budget proxy.  

*Return:* `List[str]` – chunks ready for the LLM.

---

## <a name="write_docs_by_parts"></a>write_docs_by_parts(part, model, global_info, prev_info=None, language="en")  
Synchronous LLM invocation.  

*Prompt construction:*  
```text
system: Use language <language>
system: <BASE_PART_COMPLITE_TEXT>
system: <global_info>
user:   <part>
```
If a previous part exists, a system message references it to maintain context.  
The part is sent again as a user message to reinforce the prompt.

*Post‑processing:*  
Strips surrounding markdown fences (` ``` `) if present.  

*Returns:* Generated documentation string.

---

## <a name="async_write_docs_by_parts"></a>async_write_docs_by_parts(part, async_model, global_info, semaphore, prev_info=None, language="en", update_progress=None)  
Parallel version of `write_docs_by_parts`.  
Uses an `asyncio.Semaphore` to limit concurrent LLM calls (default 4).  
After obtaining a response it optionally updates the progress bar.

---

## <a name="gen_doc_parts"></a>gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar)  
High‑level synchronous pipeline:  

1. `split_data` to chunk the code.  
2. Create a sub‑task in the progress bar.  
3. For each chunk:  
   - call `write_docs_by_parts`;  
   - append result to `all_result`;  
   - keep only the last 3000 chars as `prev_info` for next chunk.  
4. Clean up the sub‑task and return concatenated documentation.

---

## <a name="async_gen_doc_parts"></a>async_gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar)  
Asynchronous equivalent using `asyncio.gather` over `async_write_docs_by_parts`.  
Progress is advanced inside each task via the supplied callback.  

---

## <a name="progress_base"></a>BaseProgress & LibProgress  
`BaseProgress` is a minimal interface with `create_new_subtask`, `update_task`, and `remove_subtask`.  
`LibProgress` implements it using Rich’s progress bars:  

* `create_new_subtask(name, total_len)` – adds a new sub‑task.  
* `update_task()` – advances the current sub‑task (or the base task if none).  
* `remove_subtask()` – discards the current sub‑task.

These helpers enable visual feedback during long LLM runs without tying the core logic to a specific UI library.

---

### Key Interaction Points  
- **Model objects** (`GPTModel`, `AsyncGPTModel`) provide `get_answer_without_history`.  
- **GLOBAL_INFO** (e.g., project description) is prepended to each prompt to give the LLM context.  
- **Chunking** ensures each LLM call stays within token limits; the 1.5× and 1.25× thresholds balance safety and throughput.  

### Important Notes  
- The code assumes the presence of a global constant `BASE_PART_COMPLITE_TEXT` that contains a base prompt for generating documentation.  
- Result trimming (`result = result[len(result) - 3000:]`) keeps only the trailing context for the next chunk, limiting memory usage.  
- For production, replace `print` statements in `BaseProgress` with a real progress implementation.  

This module is the *execution engine* of the documentation generator, handling chunking, LLM interaction, and progress reporting.

