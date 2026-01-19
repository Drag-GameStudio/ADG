## Executive Navigation Tree
* 📂 **Core Engine**
  * [Core Logic](#logic-flow)
  * [Manager Class](#manager-class)
  * [Base Module](#basemodule)
  * [Progress Base Module](#progress_base_module)
  * [Base Progress Class](#baseprogress_class)
  * [Lib Progress Class](#libprogress_class)
* ⚙️ **Integration and Utilities**
  * [Integration](#integration)
  * [Usage Example](#usage-example)
  * [Usage Notes](#usage-notes)
  * [Postprocess](#postprocess)
  * [Splitter](#spliter)
* 📄 **Documentation and Settings**
  * [Documentation](#documentation)
  * [Settings](#settings)
  * [Introduction](#get_links_intro)
  * [Introduction to Global Data](#get_introdaction)

**Auto Doc Generator** – *Project‑Wide Overview*  
*(Activated by the project name “Auto Doc Generator”)*  

---  

## 1. Project Title  
**Auto Doc Generator**  

---  

## 2. Project Goal  
The purpose of **Auto Doc Generator** is to **automatically produce high‑quality documentation for any software project**.  
Developers no longer need to write lengthy READMEs, API references, or architecture overviews by hand; the tool extracts source‑code, feeds it to a large‑language model (LLM), and assembles the model’s responses into a coherent, ready‑to‑publish document.  

Key problems it solves  

| Problem | How Auto Doc Generator solves it |
|---------|----------------------------------|
| **Time‑consuming manual writing** | Generates the whole documentation in a few minutes. |
| **Inconsistent style & missing sections** | Centralised prompt templates enforce a uniform tone and guarantee the presence of intro, links, and section headings. |
| **Keeping docs in sync with code** | The pre‑processor walks the repository, captures every file (except ignored ones), and feeds the latest source to the LLM each run. |
| **Scalability for large codebases** | A “compression” pipeline groups file fragments, repeatedly summarises them with the LLM, and reduces the whole repository to a single markdown string. |

---  

## 3. Core Logic & Principles  

### 3.1 High‑level data flow  

```
Repository → CodeMix (tree + raw files) → Split into per‑file blocks
      → Compressor (iterative LLM summarisation) → Single markdown document
      → Post‑processor (heading extraction, intro generation) → Final output
```

### 3.2 Main layers  

| Layer | Responsibility | Principal modules |
|-------|----------------|-------------------|
| **Configuration** | Stores static prompt fragments, environment variables, model identifiers. | `engine/config/config.py` |
| **Model Layer** | Wraps the LLM (Groq) – provides synchronous (`GPTModel`) and asynchronous (`AsyncGPTModel`) interfaces. | `engine/models/model.py`, `engine/models/gpt_model.py` |
| **History** | Keeps the conversation context (system prompt + previous Q/A) that is sent to the LLM. | `History` class in `engine/models/model.py` |
| **Factory / Modules** | Orchestrates several LLM‑generated fragments (intro links, intro paragraph, etc.) into a full documentation string. | `factory/base_factory.py`, `factory/modules/intro.py` |
| **Pre‑processor** | Walks the project directory, writes a single “code‑mix” file that contains a file‑tree header and the raw source of each file. | `preprocessor/code_mix.py` |
| **Compressor** | Repeatedly groups a configurable number of text blocks (`compress_power`), asks the LLM to summarise them, and replaces the group with the summary until only one block remains. | `preprocessor/compressor.py` |
| **Post‑processor** | Parses the final markdown, extracts headings, optionally asks the LLM for section introductions, and builds a table of contents. | `preprocessor/postprocess.py` |
| **UI / Progress** | Optional visual feedback (plain console or Rich‑based progress bar). | `ui/progress_base.py` |

### 3.3 Core algorithms  

* **Repository dump (`CodeMix`)** – Recursively walks the directory, respects an `ignore_list`, and writes each file wrapped in `<file path="…">` markers. This deterministic format makes later splitting trivial.  
* **Iterative compression** – The compressor works like a *divide‑and‑conquer* summariser:  
  1. Split the list of file blocks into chunks of size `compress_power`.  
  2. Send each chunk to the LLM with a system prompt that explains the “compress‑to‑one” task.  
  3. Replace the chunk with the LLM’s answer.  
  4. Repeat until the list length is 1.  
  This approach keeps token usage within model limits while still producing a global view of the whole codebase.  
* **History handling** – Every call to `get_answer()` appends the user message and the model’s reply to the `History` object, guaranteeing context continuity for multi‑turn interactions (e.g., when the factory asks for intro links then for the intro paragraph).  
* **Factory pattern** – `DocFactory` receives an ordered collection of *module* objects (`IntroLinks`, `IntroText`, …). Each module implements a `run(info: dict) -> str` method that internally calls the model. The factory concatenates the returned strings, producing the final documentation.  

---  

## 4. Key Features  

- **Full‑project code ingestion** – Automatic tree generation and source extraction for every non‑ignored file.  
- **Sync & async LLM wrappers** – Choose `GPTModel` for simple scripts or `AsyncGPTModel` for high‑throughput pipelines.  
- **Prompt‑driven, configurable documentation style** – All system prompts live in `engine/config/config.py`; swapping a constant changes the tone for every run.  
- **Iterative compression** – Handles arbitrarily large repositories while staying inside model token limits.  
- **Modular documentation factory** – Plug‑in new modules (e.g., “API reference”, “Installation guide”) without touching the core pipeline.  
- **Progress feedback** – Optional Rich‑based progress bar or a no‑op fallback.  
- **Environment‑first design** – `.env` file automatically loaded; API keys never hard‑coded.  
- **Extensible settings object** – `ProjectSettings` lets you add arbitrary metadata (target audience, tech stack, etc.) that the LLM can use when drafting the docs.  

---  

## 5. How to Run  

Below is a **step‑by‑step guide** that works on any platform with Python 3.10+.

### 5.1 Prerequisites  

1. **Python** (≥ 3.10) installed and available on `PATH`.  
2. **Git** (optional, only if you clone the repo).  
3. **Groq API key** – sign up at https://groq.com and obtain a key.  

### 5.2 Installation  

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your‑org/auto-doc-generator.git
cd auto-doc-generator

# 2️⃣ Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# 3️⃣ Install required packages
pip install -r requirements.txt
```

`requirements.txt` typically contains:

```
python-dotenv
groq
rich               # optional, for the fancy progress bar
```

### 5.3 Configure environment variables  

Create a `.env` file in the project root:

```
API_KEY=YOUR_GROQ_API_KEY
```

If you prefer not to use a `.env` file, you can pass the key directly when constructing the model (see the usage example).

### 5.4 Run a **synchronous** documentation generation  

```bash
python examples/sync_demo.py
```

`sync_demo.py` contains the exact snippet from the documentation (see the “Strict Usage Example” section). It:

1. Builds a `History` with the system prompt.  
2. Instantiates `GPTModel`.  
3. Sends a single question and prints the answer.  
4. Uses `DocFactory` with `IntroLinks` and `IntroText` to produce a short markdown page.

### 5.5 Run an **asynchronous** documentation generation  

```bash
python examples/async_demo.py
```

The script mirrors the synchronous version but uses `AsyncGPTModel` and `await`‑s the call.

### 5.6 Full‑pipeline (code‑mix → compression → post‑process)  

If you want to generate documentation for an entire repository:

```bash
python -m preprocessor.pipeline \
    --repo-path /path/to/your/project \
    --output documentation.md \
    --compress-power 4          # number of blocks merged per LLM call
```

The `pipeline` module (provided in `preprocessor/__main__.py`) orchestrates:

1. `CodeMix` → `codemix.txt`  
2. Split into per‑file blocks  
3. `compress_to_one` (sync by default; add `--async` for async)  
4. Optional post‑processing (headings, TOC)  
5. Write the final markdown to the path you supplied.

### 5.7 Verify the result  

Open the generated file (`documentation.md` or `documentation.txt`) in any markdown viewer or IDE. You should see a table of contents, introductory paragraph, and concise summaries of each major component of the source code.

---  

## 6. Dependencies  

| Category | Package | Minimum version | Purpose |
|----------|---------|----------------|---------|
| **Core** | `python-dotenv` | 1.0.0 | Loads `.env` files automatically. |
|          | `groq` | 0.5.0 | Official client for the Groq LLM API. |
| **Optional UI** | `rich` | 13.0.0 | Fancy console progress bars (`LibProgress`). |
| **Testing (if you run the test suite)** | `pytest` | 7.0.0 | Unit‑test runner. |
| **Type checking** | `mypy` | 1.0.0 | Static type analysis (dev dependency). |
| **Formatting** | `black` | 23.0.0 | Code formatter (dev dependency). |

All runtime dependencies are listed in `requirements.txt`; dev‑only packages are in `requirements-dev.txt`.

---  

### Quick Recap  

1. **Install** → create a virtual environment → `pip install -r requirements.txt`.  
2. **Set** `API_KEY` in `.env` (or pass it manually).  
3. **Run** either the synchronous demo, the asynchronous demo, or the full pipeline command.  
4. **Read** the generated markdown – you now have up‑to‑date documentation for your project, generated automatically by an LLM.  

Feel free to extend the factory with new modules, tweak the prompts in `engine/config/config.py`, or swap the Groq model identifier (`MODELS_NAME`) for a different LLM that better fits your budget or latency requirements. Happy documenting!

 

## <a name="overview"></a> Overview
The provided code snippet is part of a larger system responsible for generating documentation. This section focuses on the `engine/models` module, specifically the `gpt_model.py` and `model.py` files.

## <a name="responsibility"></a> Responsibility
The `engine/models` module is responsible for handling communication with the LLM (Large Language Model) using the Groq API. The `GPTModel` and `AsyncGPTModel` classes encapsulate the logic for interacting with the LLM, including sending requests and processing responses.

## <a name="interaction"></a> Interaction with Other Components
The `engine/models` module interacts with other components of the system as follows:

*   **Config**: The `config.py` file provides configuration settings, such as API keys and model names, which are used by the `GPTModel` and `AsyncGPTModel` classes.
*   **Factory**: The `factory` module is responsible for combining LLM-generated fragments into a full documentation string. The `GPTModel` and `AsyncGPTModel` classes provide the necessary functionality for the factory to generate documentation.
*   **History**: The `History` class, defined in `model.py`, stores the conversation context that is sent to the LLM. This context is used to generate answers to user queries.

## <a name="key-functions"></a> Key Functions and Classes
The key functions and classes in the `engine/models` module are:

*   **`GPTModel`**: A synchronous class that interacts with the LLM using the Groq API.
*   **`AsyncGPTModel`**: An asynchronous class that interacts with the LLM using the Groq API.
*   **`Model`**: A parent class that provides a basic implementation for interacting with the LLM.
*   **`AsyncModel`**: A parent class that provides a basic asynchronous implementation for interacting with the LLM.
*   **`History`**: A class that stores the conversation context sent to the LLM.

## <a name="logic-flow"></a> Logic Flow
The logic flow of the `engine/models` module is as follows:

1.  **Initialization**: The `GPTModel` or `AsyncGPTModel` class is initialized with an API key and a `History` object.
2.  **Generating Answers**: The `generate_answer` method is called with a user query and optional history. The method sends a request to the LLM and processes the response to generate an answer.
3.  **Error Handling**: If an error occurs during the request, the method will retry with a different model until a successful response is received.

## <a name="assumptions"></a> Assumptions and Inputs
The `engine/models` module assumes that:

*   **API Key**: A valid API key is provided for authentication with the Groq API.
*   **Model Names**: A list of valid model names is provided in the configuration settings.
*   **User Query**: A user query is provided as input to the `generate_answer` method.
*   **History**: A `History` object is provided to store the conversation context.

The `engine/models` module produces the following outputs:

*   **Answer**: A generated answer to the user query.
*   **Error**: An error message if the request to the LLM fails.

## <a name="side-effects"></a> Side Effects
The `engine/models` module has the following side effects:

*   **Conversation Context**: The conversation context is updated with the user query and the generated answer.
*   **API Requests**: The module sends requests to the Groq API to generate answers.

By following the provided documentation and code structure, developers can effectively utilize the `engine/models` module to generate high-quality documentation using the LLM.

**Factory Core – Documentation**  

<a name="overview"></a>
## Overview
The *factory* package builds the final documentation page by chaining **modules** that each generate a fragment of markdown/HTML.  
`DocFactory` receives any number of objects that inherit from `BaseModule`.  
During `generate_doc(info)` every module is called with the same `info` dictionary, its result is concatenated, and the combined string is returned to the caller (e.g., the CLI or the high‑level `DocFactory.generate_doc` used in the usage example).

---

<a name="basemodule"></a>
## `BaseModule` (abstract)

```python
class BaseModule(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, info: dict):
        ...
```

* **Responsibility** – Define the contract for a documentation fragment generator.  
* **Key method** – `generate(info) → str` must return a string that will be inserted into the final document.  
* **Assumptions** – Implementations may read any key from `info`; they must never mutate the dictionary.  
* **Side‑effects** – None (pure function).

All concrete modules (e.g., `IntroLinks`, `IntroText`) inherit from this class.

---

<a name="docfactory"></a>
## `DocFactory`

```python
class DocFactory:
    def __init__(self, *modules):
        self.modules: list[BaseModule] = modules

    def generate_doc(self, info: dict) -> str:
        output = ""
        for module in self.modules:
            module_result = module.generate(info)
            output += module_result + "\n\n"
        return output
```

* **Responsibility** – Orchestrate the ordered execution of modules and concatenate their outputs.  
* **Interaction** –  
  * Receives pre‑instantiated module objects (any subclass of `BaseModule`).  
  * Calls each module’s `generate` method, passing the *same* `info` payload.  
* **Inputs** – `info: dict` containing the data required by the modules (e.g., `full_data`, `global_data`, `language`).  
* **Outputs** – A single markdown/HTML string where each fragment is separated by a blank line.  
* **Side‑effects** – None; the method is pure apart from the module implementations.

> **Note** – The `if __name__ == "__main__":` block demonstrates a naïve call with abstract classes; in production you would pass concrete module instances.

---

<a name="intro-modules"></a>
## Intro Modules (`factory.modules.intro`)

```python
from ..base_factory import BaseModule
from preprocessor.postprocess import (
    get_all_html_links,
    get_links_intro,
    get_introdaction,
)

class IntroLinks(BaseModule):
    def generate(self, info: dict):
        links = get_all_html_links(info.get("full_data"))
        intro_links = get_links_intro(links, info.get("language"))
        return intro_links

class IntroText(BaseModule):
    def generate(self, info: dict):
        intro = get_introdaction(info.get("global_data"), info.get("language"))
        return intro
```

### IntroLinks
* **Purpose** – Extract every `<a href=…>` tag from the raw HTML (`full_data`) and transform the list into a language‑specific introductory list.  
* **Dependencies** – `preprocessor.postprocess.get_all_html_links` and `get_links_intro`.  
* **Inputs** – `info["full_data"]` (HTML string), `info["language"]` (e.g., `"en"`).  
* **Output** – Formatted markdown list of links.

### IntroText
* **Purpose** – Produce a short paragraph that introduces the whole project using the high‑level description (`global_data`).  
* **Dependency** – `preprocessor.postprocess.get_introdaction`.  
* **Inputs** – `info["global_data"]` (project summary), `info["language"]`.  
* **Output** – A single paragraph of introductory text.

Both modules are pure and rely exclusively on the `info` dict; they do not modify external state.

---

<a name="integration"></a>
## Integration with the Rest of the System
1. **Pre‑processing** – `preprocessor` components generate the `full_data` and `global_data` fields that the intro modules consume.  
2. **Factory construction** – In user code (see the global usage example) a `DocFactory` is instantiated with the desired modules, e.g.:

   ```python
   factory = DocFactory(IntroLinks(), IntroText())
   doc = factory.generate_doc(info)
   ```

3. **Output** – The resulting string can be written to a markdown file, displayed in the UI, or further post‑processed.

---

<a name="usage-example"></a>
## Quick Usage Example

```python
from factory.base_factory import DocFactory
from factory.modules.intro import IntroLinks, IntroText

info = {
    "full_data": "<html>…</html>",        # raw HTML of the project page
    "global_data": "Auto Doc Generator …",  # short project description
    "language": "en"
}

factory = DocFactory(IntroLinks(), IntroText())
documentation = factory.generate_doc(info)
print(documentation)
```

The example produces an introductory links block followed by a concise project paragraph, each separated by a blank line.

---

**Key Take‑aways**

* `BaseModule` enforces a simple *generate‑only* contract.  
* `DocFactory` is the orchestrator – order of modules matters.  
* Intro modules are thin adapters around post‑processing utilities, keeping the factory layer agnostic of HTML parsing details.  

This design makes it trivial to add new sections (e.g., `APIReference`, `Changelog`) – simply implement a new `BaseModule` subclass and include it in the factory’s constructor.

<a name="manager-class"></a>
## Manager Class
The `Manager` class is responsible for orchestrating the documentation generation process. It takes in several parameters during initialization:
* `project_directory`: The path to the project directory.
* `project_settings`: An instance of `ProjectSettings` containing project metadata.
* `ignore_files`: A list of file patterns to ignore during the documentation generation process.
* `language`: The language of the project (defaults to "en").
* `progress_bar`: An instance of `BaseProgress` for displaying progress (defaults to `BaseProgress`).

### Methods
The `Manager` class has several methods that perform the following tasks:
* `read_file_by_file_key`: Reads a file from the cache directory based on a file key.
* `get_file_path`: Returns the file path for a given file key.
* `generate_code_file`: Generates a code mix file by walking the repository and concatenating file contents.
* `generate_global_info_file`: Generates a global info file by compressing the code mix file using an LLM.
* `generete_doc_parts`: Generates documentation parts by splitting the code mix file and using an LLM to generate text.
* `factory_generate_doc_intro`: Generates a documentation intro using a `DocFactory` instance.

### Usage Example
The `Manager` class is used in the `if __name__ == "__main__":` block to generate documentation for a project. The example demonstrates how to create a `Manager` instance, generate a code mix file, global info file, documentation parts, and finally, a documentation intro using a `DocFactory` instance.

```python
with Progress(
    SpinnerColumn(),          
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),               
    TaskProgressColumn(),     
) as progress:
    project_settings = ProjectSettings("Auto Doc Generator")
    project_settings.add_info(
        "global idea",
        """This project was created to help developers make documentations for them projects"""
    )
    manager = Manager(r"C:\Users\huina\Python Projects\Impotant projects\AutoDocGenerateGimini", project_settings, ignore_list, progress_bar=LibProgress(progress), language="en")

    manager.generate_code_file()
    manager.generate_global_info_file(use_async=True, max_symbols=5000)
    manager.generete_doc_parts(use_async=True, max_symbols=4000)
    manager.factory_generate_doc_intro(
        DocFactory(
            IntroLinks(),
            IntroText(),
        )
    )
```

### Key Points
* The `Manager` class is designed to be flexible and reusable for different projects.
* The `generate_code_file`, `generate_global_info_file`, and `generete_doc_parts` methods can be used asynchronously by passing `use_async=True`.
* The `factory_generate_doc_intro` method uses a `DocFactory` instance to generate a documentation intro.
* The `Manager` class uses a `BaseProgress` instance to display progress during the documentation generation process.

<a name="code_mix"></a>
## `preprocessor/code_mix.py` – Repository‑Mixer Component  

**Purpose in the Auto Doc Generator**  
`CodeMix` is the first step of the documentation pipeline. It walks a project's source tree, writes a **human‑readable directory listing** followed by the raw contents of every non‑ignored file into a single text blob. This blob (`codemix.txt`) is later consumed by the **compressor** (`preprocessor/compressor.py`) which splits it on the `<file path="…">` markers and feeds the fragments to the LLM for progressive summarisation.

### Core Class: `CodeMix`

| Method | Responsibility | Key Behaviour |
|--------|----------------|----------------|
| `__init__(root_dir=".", ignore_patterns=None)` | Initialise the mixer. <br> * `root_dir` → absolute `Path` of the repository root. <br> * `ignore_patterns` → list of glob patterns (e.g., `*.pyc`, `venv`) that define files/folders to skip. |
| `should_ignore(path: str) -> bool` | Decide whether a given `Path` should be excluded. <br> * Computes the path relative to `root_dir`. <br> * Checks the relative string, its basename, and every path component against all glob patterns using `fnmatch`. |
| `build_repo_content(output_file="repomix-output.txt")` | Generate the mixed repository file. <br> * Writes a **tree view** (`Repository Structure:`) with indentation reflecting directory depth. <br> * Inserts a separator line (`====================`). <br> * For each file that passes `should_ignore`, writes a marker `<file path="relative/path">` followed by the file's text (UTF‑8, errors ignored). <br> * On read errors, logs a line `Error reading <path>: <exception>` instead of aborting. |

### Interaction with Other Modules  

1. **Input** – The component receives the absolute path to the project (`root_dir`) and a list of ignore patterns (`ignore_list` defined at the bottom of the file).  
2. **Output** – A plain‑text file (by default `repomix-output.txt`, commonly renamed to `codemix.txt`). Its format is:  

   ```
   Repository Structure:
   src/
     main.py
     utils/
       helpers.py
   ====================

   <file path="src/main.py">
   <file contents …>

   <file path="src/utils/helpers.py">
   <file contents …>
   ```
3. **Downstream consumption** – `preprocessor/compressor.compress_to_one` reads this file, splits on `<file path="` to obtain a list of *per‑file blocks*, and then iteratively asks the LLM to compress them. The `ProjectSettings` object supplies the system prompt that guides the LLM, while the `History` object tracks the conversation.  

### Assumptions & Side Effects  

* **Assumptions** – The repository fits in memory when split into fragments; all source files are UTF‑8‑compatible (binary files are ignored via patterns).  
* **Side effects** – Writes (or overwrites) `output_file`. May produce additional lines for files that raise exceptions during reading (e.g., permission errors).  

### Typical Usage  

```python
from preprocessor.code_mix import CodeMix, ignore_list

mixer = CodeMix(root_dir="path/to/project", ignore_patterns=ignore_list)
mixer.build_repo_content("codemix.txt")   # creates the mixed dump
print("Repository dump ready for compression.")
```

The generated `codemix.txt` becomes the **single source of truth** for the rest of the Auto Doc Generator, enabling the system to turn an entire codebase into concise, LLM‑crafted documentation.

<a name="compressor-overview"></a>
## 📦 compressor – Core Compression Engine  

The **compressor** module implements the *iterative reduction* stage of the Auto Doc Generator pipeline.  
After `preprocessor.code_mix` has emitted a list of per‑file text blocks, this module repeatedly sends groups of those blocks to the LLM (via `GPTModel` / `AsyncGPTModel`) and merges the returned summaries until a single, project‑wide documentation string remains.

It is the bridge between raw source‑code blobs and the final markdown/HTML that downstream *post‑process* modules consume.

---

<a name="compress"></a>
### `compress(data: str, project_settings: ProjectSettings, model: Model, compress_power) -> str`  

* **Responsibility** – Build a three‑message prompt (system + system + user) and ask the model to *compress* the supplied `data`.  
* **Inputs**  
  * `data` – raw text of a single file (or a concatenated chunk).  
  * `project_settings` – provides `prompt` (project‑specific system prompt).  
  * `model` – an instantiated `GPTModel` (sync) or `AsyncGPTModel` (async) that implements `get_answer_without_history`.  
  * `compress_power` – integer controlling the “detail level” that is baked into the system prompt via `get_BASE_COMPRESS_TEXT`.  
* **Outputs** – The model’s answer string, i.e. a concise summary of `data`.  
* **Side‑effects** – None (the model call is stateless; no history is updated).  

---

<a name="compress_and_compare"></a>
### `compress_and_compare(data: list, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) -> list`  

* **Responsibility** – Synchronously compress a *list* of file blocks, grouping `compress_power` consecutive elements, appending their compressed results into a new list (`compress_and_compare_data`).  
* **Workflow**  
  1. Initialise a result list sized `ceil(len(data)/compress_power)`.  
  2. Create a sub‑task on the supplied `progress_bar`.  
  3. Reuse a single `GPTModel` instance for all calls (reduces API overhead).  
  4. For each element `el` in `data` compute its chunk index `i // compress_power` and concatenate `compress(el, …) + "\n"` to the appropriate bucket.  
  5. Update the progress bar after each compression.  
  6. Remove the sub‑task and return the bucket list.  

* **Assumptions** – `compress_power` ≥ 2; `data` contains non‑empty strings.  

---

<a name="async_compress"></a>
### `async_compress(data: str, project_settings: ProjectSettings, model: AsyncModel, compress_power, semaphore, progress_bar: BaseProgress) -> str`  

* **Responsibility** – Async counterpart of `compress`.  
* **Key Details**  
  * The coroutine acquires the supplied `semaphore` (default limit 4) to bound concurrent LLM calls.  
  * Builds the same three‑message prompt and awaits `model.get_answer_without_history`.  
  * Updates the progress bar once the LLM response arrives.  

---

<a name="async_compress_and_compare"></a>
### `async_compress_and_compare(data: list, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) -> list`  

* **Responsibility** – Parallel‑execute `async_compress` for every element of `data`.  
* **Logic Flow**  
  1. Create a semaphore (max 4 concurrent requests) and a single `AsyncGPTModel`.  
  2. Queue a coroutine for each element (`tasks`).  
  3. `await asyncio.gather(*tasks)` → `compressed_elements`.  
  4. Re‑assemble the elements into chunks of size `compress_power`, joining them with newline characters to mimic the synchronous bucket layout.  
  5. Return the list of combined strings.  

* **Side‑effects** – Progress bar sub‑task is created/removed; LLM calls are performed concurrently.

---

<a name="compress_to_one"></a>
### `compress_to_one(data: list, project_settings: ProjectSettings, compress_power: int = 4, use_async: bool = False, progress_bar: BaseProgress = BaseProgress()) -> str`  

* **Responsibility** – Orchestrate the *iterative* compression loop until only one document remains.  
* **Algorithm**  
  ```text
  while len(data) > 1:
      if len(data) < compress_power + 1:
          new_compress_power = 2            # fall‑back for small tails
      else:
          new_compress_power = compress_power

      if use_async:
          data = async_compress_and_compare(..., new_compress_power)
      else:
          data = compress_and_compare(..., new_compress_power)

      count_of_iter += 1
  return data[0]
  ```  
* **Inputs** – Same as the helper functions; `use_async` toggles the sync vs async pipeline.  
* **Outputs** – A single string containing the fully compressed project documentation.  
* **Side‑effects** – Progress bar updates; multiple LLM calls (sync or async) are issued; internal counters (`count_of_iter`) are for debugging/metrics only.  

---

<a name="integration"></a>
## 🔗 Interaction with the Rest of the System  

| Component | How it uses *compressor* |
|-----------|--------------------------|
| **preprocessor.code_mix** | Generates the initial `list[str]` (raw file blocks) that is fed into `compress_to_one`. |
| **preprocessor.settings** | Supplies `ProjectSettings.prompt`, which is merged into every LLM request. |
| **engine.models.gpt_model** | Provides `GPTModel` / `AsyncGPTModel` with the `get_answer_without_history` method used throughout. |
| **ui.progress_base** | Optional visual feedback; the compressor creates and updates sub‑tasks but works without it (defaults to a no‑op implementation). |
| **postprocess** | Receives the final single string from `compress_to_one` for heading extraction, intro generation, etc. |

---

<a name="usage-notes"></a>
## 🚀 Typical Usage Pattern  

```python
from preprocessor.compressor import compress_to_one
from preprocessor.settings import ProjectSettings
from ui.progress_base import BaseProgress

# `file_blocks` is the list produced by CodeMix (raw per‑file text)
project_settings = ProjectSettings(project_name="MyApp", info={...})

final_doc = compress_to_one(
    data=file_blocks,
    project_settings=project_settings,
    compress_power=4,          # tune for token budget
    use_async=True,           # leverage async for speed
    progress_bar=BaseProgress()
)
```

The function will automatically shrink the list, respect the token limits (via `get_BASE_COMPRESS_TEXT`), and return the ready‑to‑post‑process documentation.

--- 

*All symbols and behaviours described are aligned with the global architecture of the **Auto Doc Generator** project.*

## <a name="postprocess"></a> Post-processing Module
The post-processing module is responsible for generating markdown anchors, extracting topics and links, and creating introductions for the documentation.

### Functions

*   **`generate_markdown_anchor(header: str) -> str`**: This function generates a markdown anchor from a given header. It converts the header to lowercase, replaces spaces with hyphens, and removes any non-alphanumeric characters.
*   **`get_all_topics(data: str) -> list[str]`**: This function extracts all topics from a given data string. It finds all occurrences of "\n## " followed by a topic name and returns a list of topics along with their corresponding markdown anchors.
*   **`get_all_html_links(data: str) -> list[str]`**: This function extracts all HTML links from a given data string. It finds all occurrences of "<a name=" followed by a link name and returns a list of links.
*   **`get_links_intro(links: list[str], language: str = "en")`**: This function generates an introduction for a list of links using a GPT model. It creates a prompt with the language and links, and returns the model's response.
*   **`get_introdaction(global_data: str, language: str = "en") -> str`**: This function generates an introduction for a given global data string using a GPT model. It creates a prompt with the language and global data, and returns the model's response.

### Example Usage

```python
topics, links = get_all_topics(data)
print(topics)  # Output: ["Topic 1", "Topic 2", ...]
print(links)  # Output: ["#topic-1", "#topic-2", ...]

html_links = get_all_html_links(data)
print(html_links)  # Output: ["link-1", "link-2", ...]

intro = get_links_intro(links)
print(intro)  # Output: "Introduction to links..."

intro = get_introdaction(global_data)
print(intro)  # Output: "Introduction to global data..."
```

## <a name="settings"></a> Project Settings
The project settings class is responsible for storing project metadata and generating a prompt for the GPT model.

### Class

*   **`ProjectSettings`**: This class has the following properties and methods:
    *   **`__init__(project_name: str)`**: Initializes the project settings with a project name.
    *   **`add_info(key, value)`**: Adds a key-value pair to the project info dictionary.
    *   **`prompt`**: A property that returns the prompt for the GPT model.

### Example Usage

```python
project_settings = ProjectSettings("My Project")
project_settings.add_info("author", "John Doe")
print(project_settings.prompt)  # Output: "Project Name: My Project\nauthor: John Doe\n"
```

## <a name="spliter"></a> Data Splitter
The data splitter module is responsible for splitting a large data string into smaller chunks.

### Functions

*   **`split_data(data: str, max_symbols: int) -> list[str]`**: This function splits a data string into chunks of a maximum size.

### Example Usage

```python
chunks = split_data(data, 1000)
print(chunks)  # Output: ["chunk-1", "chunk-2", ...]
```

<a name="documentation"></a>
## Documentation

The provided code snippet appears to be part of a larger system responsible for generating documentation for a given codebase. The system utilizes a combination of natural language processing (NLP) and machine learning models to produce high-quality documentation.

### Component Overview

The code snippet is comprised of several key components:

*   `split_data`: A function responsible for splitting the input code mix into smaller, manageable parts based on a maximum symbol limit.
*   `write_docs_by_parts` and `async_write_docs_by_parts`: Functions that generate documentation for each part of the split code mix using a model (either synchronous or asynchronous).
*   `gen_doc_parts` and `async_gen_doc_parts`: Functions that orchestrate the generation of documentation for the entire code mix by splitting the data, generating documentation for each part, and combining the results.

### Key Functions and Classes

*   `split_data`: Splits the input code mix into smaller parts based on a maximum symbol limit.
*   `write_docs_by_parts`: Generates documentation for a given part of the code mix using a synchronous model.
*   `async_write_docs_by_parts`: Generates documentation for a given part of the code mix using an asynchronous model.
*   `gen_doc_parts`: Generates documentation for the entire code mix by splitting the data and using a synchronous model.
*   `async_gen_doc_parts`: Generates documentation for the entire code mix by splitting the data and using an asynchronous model.

### Logic Flow

The logic flow of the system can be summarized as follows:

1.  The input code mix is split into smaller parts using the `split_data` function.
2.  For each part, the `write_docs_by_parts` or `async_write_docs_by_parts` function is called to generate documentation using a model.
3.  The generated documentation for each part is combined to produce the final documentation for the entire code mix.

### Important Assumptions and Inputs

*   The input code mix is expected to be a string containing the codebase to be documented.
*   The maximum symbol limit is used to determine the size of each part of the split code mix.
*   The model used for generating documentation is assumed to be a natural language processing (NLP) or machine learning model capable of understanding the input code mix and producing high-quality documentation.

### Outputs and Side Effects

*   The final output of the system is a string containing the generated documentation for the entire code mix.
*   The system may have side effects, such as creating temporary files or updating progress bars, depending on the implementation of the `progress_bar` component.

### Example Usage

```python
# Example usage of the gen_doc_parts function
full_code_mix = "Example code mix"
global_info = "Example global information"
max_symbols = 1000
language = "en"
progress_bar = BaseProgress()

result = gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar)
print(result)
```

```python
# Example usage of the async_gen_doc_parts function
import asyncio

full_code_mix = "Example code mix"
global_info = "Example global information"
max_symbols = 1000
language = "en"
progress_bar = BaseProgress()

async def main():
    result = await async_gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar)
    print(result)

asyncio.run(main())
```

## <a name="progress_base_module"></a> Progress Base Module
The `progress_base` module provides a foundation for creating progress bars in the application. It defines two classes: `BaseProgress` and `LibProgress`.

### <a name="baseprogress_class"></a> BaseProgress Class
The `BaseProgress` class serves as a base class for progress bar implementations. It defines the following methods:
* `__init__`: Initializes the progress bar.
* `create_new_subtask`: Creates a new subtask in the progress bar. This method should be implemented by subclasses.
* `update_task`: Updates the progress bar. This method should be implemented by subclasses.
* `remove_subtask`: Removes a subtask from the progress bar. This method should be implemented by subclasses.

### <a name="libprogress_class"></a> LibProgress Class
The `LibProgress` class is a concrete implementation of the `BaseProgress` class. It uses the `rich.progress` library to create a progress bar. The class has the following attributes:
* `progress`: An instance of `rich.progress.Progress`.
* `_base_task`: The main task in the progress bar.
* `_cur_sub_task`: The current subtask in the progress bar.

The `LibProgress` class implements the following methods:
* `__init__`: Initializes the progress bar with a main task and an optional total number of tasks.
* `create_new_subtask`: Creates a new subtask in the progress bar with a given name and total length.
* `update_task`: Updates the progress bar by advancing the current subtask or the main task if no subtask is active.
* `remove_subtask`: Removes the current subtask from the progress bar.

### Example Usage
```python
from ui.progress_base import LibProgress
from rich.progress import Progress

# Create a progress bar
progress = Progress()
lib_progress = LibProgress(progress, total=10)

# Create a new subtask
lib_progress.create_new_subtask("Subtask 1", 5)

# Update the progress bar
lib_progress.update_task()

# Remove the subtask
lib_progress.remove_subtask()
```
This code creates a progress bar with a main task and a subtask, updates the progress bar, and then removes the subtask.

