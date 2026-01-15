## Executive Navigation Tree
* 📂 Core Engine
  * [Model](#gpt_model)
  * [Base Factory](#base_factory)
  * [Manager Class](#manager-class)
  * [Key Functions and Logic Flows](#key-functions-and-logic-flows)
* ⚙️ Service Entry Points
  * [Interaction with Other Components](#interaction-with-other-components)
  * [Important Assumptions and Inputs](#important-assumptions-and-inputs)
  * [Outputs and Side Effects](#outputs-and-side-effects)
* 📄 Identity & Access
  * [Responsibility](#responsibility)
  * [Key Elements](#key-elements)
  * [Assumptions](#assumptions)


**Project Overview**

---

### 1. Project Title  
**AutoDoc — Automated Documentation Generator for Python Projects**

---

### 2. Project Goal  
AutoDoc is a lightweight, modular pipeline that automatically produces high‑quality Markdown documentation for any Python code‑base. By extracting source files, summarising their content with a language model, and stitching together a structured document (including an introductory overview and a table of contents), the tool removes the manual, error‑prone effort normally required to keep project documentation up‑to‑date.

---

### 3. Core Logic & Principles  

| Step | Description | Key Components |
|------|-------------|----------------|
| **1️⃣ Initialise** | The `Manager` class receives the project root, a list of ignore patterns, the target language (e.g., “en”), and an optional `rich.Progress` bar for visual feedback. | `manage.py → Manager.__init__` |
| **2️⃣ Code Mix Generation** | All source files that are **not** matched by the ignore list are read, concatenated, and written to `code_mix.txt`. This creates a single, searchable text representation of the repository. | `preprocessor/code_mix.py → CodeMix.build_repo_content` |
| **3️⃣ Global‑Info Compression** | `code_mix.txt` is split into manageable chunks (default ≤ 8 000 symbols). Each chunk is fed to a language model (synchronous or asynchronous) that summarises it. The summaries are then merged into a single `global_info.md` file that captures the overall structure and purpose of the code‑base. | `preprocessor/spliter.py → split_data` <br> `preprocessor/compressor.py → compress_to_one` |
| **4️⃣ Documentation Parts Generation** | Using the compressed global info and the original code mix, the system asks the model to generate the main documentation sections (e.g., module overviews, class/function descriptions). The output is stored in `doc_parts.md`. | `engine/models/model.py → Model / AsyncModel` <br> `factory/base_factory.py → DocFactory` |
| **5️⃣ Intro & TOC Creation** | A `DocFactory` instance creates an introductory paragraph and a table of contents (derived from markdown headings). This intro is prepended to `doc_parts.md`, producing the final `README.md` (or any target file). | `factory/base_factory.py → DocFactory.generate_intro` |
| **6️⃣ Optional Progress Reporting** | If a `rich.Progress` instance is supplied, each pipeline stage updates the bar, giving the user real‑time feedback on long‑running model calls. | `manage.py → progress_bar` |

**Design Principles**

* **Modularity** – Each stage lives in its own module (`engine`, `preprocessor`, `factory`). Swapping a component (e.g., using a different LLM) only requires changing the corresponding class.
* **Scalability** – Large projects are split into chunks that respect token limits of the underlying model. Both synchronous and asynchronous model calls are supported.
* **Extensibility** – The `DocFactory` can be subclassed to customise the intro, add custom sections, or change the markdown layout.
* **Transparency** – Intermediate artefacts (`code_mix.txt`, `global_info.md`, `doc_parts.md`) are persisted on disk, making debugging straightforward.

---

### 4. Key Features  

- **Automatic source‑code aggregation** – Generates a single `code_mix.txt` that contains every non‑ignored file.  
- **Intelligent summarisation** – Leverages LLMs (OpenAI, Anthropic, etc.) to compress raw code into concise, human‑readable markdown.  
- **Chunk‑aware processing** – Automatically splits large repositories to stay within model token limits.  
- **Synchronous & asynchronous execution** – Choose the mode that best fits your environment or API rate‑limit constraints.  
- **Rich progress UI** – Optional integration with `rich` to display a live progress bar.  
- **Customisable ignore patterns** – Fine‑grained control over which files/folders are excluded (e.g., virtual environments, caches, binaries).  
- **Generated table of contents & intro** – Auto‑extracted headings become a navigable TOC; an AI‑written intro summarises the project.  
- **Persisted intermediate artefacts** – All stages write their output to disk for auditability and re‑use.  
- **Plug‑and‑play model abstraction** – `Model` and `AsyncModel` base classes make it trivial to swap the underlying LLM provider.

---

### 5. How to Run  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your‑org/auto‑doc.git
   cd auto-doc
   ```

2. **Create a virtual environment (recommended)**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install required packages**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API credentials**  
   The LLM client reads the environment variable `OPENAI_API_KEY` (or the variable required by the chosen provider).  
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

5. **Define ignore patterns** *(optional)* – Edit `ignore_patterns.py` or pass a custom list when instantiating `Manager`.

6. **Run the documentation pipeline**  
   ```python
   from rich.progress import Progress
   from manage import Manager

   # Optional visual progress bar
   progress = Progress()

   # Example ignore list (feel free to adjust)
   IGNORE = [
       "*.pyo", "*.pyd", "*.pkl", "*.log", "*.sqlite3", "*.db", "data",
       "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml",
       ".gitignore", ".ruff_cache", ".auto_doc_cache", "*.pyc",
       "__pycache__", ".git", ".coverage", "htmlcov", "migrations",
       "*.md", "static", "staticfiles", ".mypy_cache"
   ]

   # Initialise the manager
   manager = Manager(
       project_directory=".",          # or absolute path to your project
       ignore_files=IGNORE,
       language="en",
       progress_bar=progress
   )

   # Execute the pipeline
   with progress:
       manager.generate_code_file()                                 # step 2
       manager.generate_global_info_file(use_async=True, max_symbols=7000)  # step 3
       manager.generete_doc_parts(max_symbols=5000, use_async=False)        # step 4
       manager.factory_generate_doc_intro()                         # step 5 (adds intro & TOC)
   ```

7. **Result**  
   After the run finishes, you will find the final documentation in the project root (default name `README.md` or the file you configured inside `DocFactory`).

---

### 6. Dependencies  

| Category | Package | Purpose |
|----------|---------|---------|
| **Core** | `python>=3.9` | Language runtime |
| **LLM Interaction** | `openai>=1.0` (or alternative provider SDK) | Calls to the language model |
| **Async Support** | `httpx>=0.24` | Async HTTP requests for LLM APIs |
| **Progress UI** | `rich>=13.0` | Terminal progress bar and styled output |
| **Markdown Utilities** | `markdown-it-py>=3.0` | Optional parsing of generated markdown |
| **Testing (optional)** | `pytest>=7.0` | Unit‑test framework |
| **Formatting** | `black`, `ruff` | Code style enforcement (dev dependencies) |

All runtime dependencies are listed in `requirements.txt`. Development‑only tools are listed in `dev-requirements.txt`.

---

**End of Overview**  


 

<a name="overview"></a>
## Overview
The **`engine.config.config`** module centralises all static prompt templates and helper functions that drive the behaviour of the language‑model‑based documentation pipeline.  
It supplies:

* **Base system prompts** (`BASE_SYSTEM_TEXT`) that instruct the LLM how to incrementally analyse code snippets.
* **Part‑completion prompts** (`BASE_PART_COMPLITE_TEXT`) that guide the generation of concise documentation for each received fragment.
* **Intro‑generation prompts** (`BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`) used by the *intro* factory module to craft project overviews and navigation trees.
* **Dynamic compression prompt builder** (`get_BASE_COMPRESS_TEXT`) that creates a size‑aware instruction for summarising large code blocks.
* **Environment bootstrap** – loading an API key from a `.env` file and exposing a list of supported model identifiers (`MODELS_NAME`).

These constants are imported by other components (e.g., `factory.modules.intro`, `preprocessor.compressor`, `manage.Manager`) to ensure a single source of truth for LLM interaction text.

<a name="responsibility"></a>
## Responsibility
* **Prompt source of truth** – All high‑level textual instructions sent to the LLM live here, making updates straightforward and guaranteeing consistency across the pipeline.
* **Dynamic prompt generation** – `get_BASE_COMPRESS_TEXT` tailors the compression prompt according to the expected input size (`start`) and the desired reduction factor (`power`).
* **Runtime configuration** – Reads the `API_KEY` from environment variables, enabling secure authentication for external model services.

<a name="interaction"></a>
## Interaction with Other Parts of the System
| Component | How it uses this module |
|-----------|------------------------|
| `factory.modules.intro` | Imports `BASE_INTRODACTION_CREATE_TEXT` and `BASE_INTRO_CREATE` to generate the introductory section of the final documentation. |
| `preprocessor.compressor` | Calls `get_BASE_COMPRESS_TEXT` to obtain a prompt that tells the LLM how to summarise a large code chunk. |
| `manage.Manager` | Uses `BASE_SYSTEM_TEXT` and `BASE_PART_COMPLITE_TEXT` when orchestrating the step‑wise analysis of source files. |
| `engine.models.*` | Reads `API_KEY` and `MODELS_NAME` to initialise model clients that will receive the prompts defined here. |

<a name="key-elements"></a>
## Key Elements

### Constants
| Name | Description |
|------|-------------|
| `BASE_SYSTEM_TEXT` | Multi‑line instruction that defines the incremental analysis workflow for each incoming code snippet. |
| `BASE_PART_COMPLITE_TEXT` | Template for generating concise documentation of a single fragment, including formatting requirements (anchor links, length limits). |
| `BASE_INTRODACTION_CREATE_TEXT` | Prompt (in Russian) that asks the LLM to produce a “50 % density” navigation tree, preserving original markdown anchors. |
| `BASE_INTRO_CREATE` | English prompt that asks the LLM to write a full project overview (title, goal, core logic, etc.). |
| `MODELS_NAME` | List of model identifiers the system can address (OpenAI and LLaMA variants). |

### Functions
* **`get_BASE_COMPRESS_TEXT(start: int, power: int) -> str`**  
  *Purpose*: Build a compression‑task prompt that reflects the maximum characters (`start`) and the desired summary length (`start / power`).  
  *Parameters*  
  - `start`: Approximate size of the raw code snippet (characters).  
  - `power`: Divider that determines how much the summary should be compressed.  
  *Return*: A formatted string ready to be sent to the LLM, containing an explicit usage‑example block placeholder.  

### Environment Loading
```python
import os
from dotenv import load_dotenv

load_dotenv()               # Populate os.environ from a .env file
API_KEY = os.getenv("API_KEY")
```
*Ensures the API key is available at import time, allowing model classes to read it without further configuration.*

<a name="assumptions"></a>
## Important Assumptions & Side Effects
* The `.env` file exists in the working directory and defines `API_KEY`; otherwise `API_KEY` will be `None`, causing downstream model initialisation to fail.
* Prompt strings are treated as immutable; they are concatenated only by the helper function (`get_BASE_COMPRESS_TEXT`), which does not modify the originals.
* All consuming modules assume UTF‑8 encoding and that the placeholders (e.g., `"""` blocks) are inserted verbatim into the request payload sent to the LLM.

<a name="usage-example"></a>
## Example Usage (Illustrative)
```python
from engine.config.config import (
    BASE_SYSTEM_TEXT,
    BASE_PART_COMPLITE_TEXT,
    get_BASE_COMPRESS_TEXT,
    API_KEY,
    MODELS_NAME,
)

print("System prompt:", BASE_SYSTEM_TEXT.strip())
print("Compression prompt (5 k chars → ~1 k):")
print(get_BASE_COMPRESS_TEXT(start=5000, power=5))
print("Available models:", MODELS_NAME)
print("Loaded API key:", bool(API_KEY))
```

*The snippet demonstrates how other parts of the codebase retrieve static prompts, generate a size‑aware compression prompt, and access the runtime configuration.*

## <a name="gpt_model"></a> GPT Model Documentation
The `GPTModel` and `AsyncGPTModel` classes are designed to interact with the Groq API for generating human-like text based on a given prompt. These models inherit from the `Model` and `AsyncModel` classes, respectively, and provide the core functionality for text generation.

### Responsibility
The primary responsibility of the `GPTModel` and `AsyncGPTModel` classes is to generate answers to user prompts using the Groq API. They handle the interaction with the API, including creating chat completions and retrieving the generated text.

### Interactions with Other Parts of the System
The `GPTModel` and `AsyncGPTModel` classes interact with the following components:

*   `History` class: Used to store the conversation history, including user prompts and model responses.
*   `Groq` and `AsyncGroq` clients: Used to interact with the Groq API for generating text.
*   `Model` and `AsyncModel` classes: Inherited from these classes, which provide the basic functionality for text generation.

### Key Functions and Classes
The key functions and classes in the `GPTModel` and `AsyncGPTModel` classes are:

*   `generate_answer`: Generates an answer to a user prompt using the Groq API.
*   `get_answer`: Adds the user prompt to the conversation history and generates an answer using the `generate_answer` method.
*   `get_answer_without_history`: Generates an answer without considering the conversation history.
*   `History` class: Stores the conversation history, including user prompts and model responses.

### Logic Flow
The logic flow of the `GPTModel` and `AsyncGPTModel` classes is as follows:

1.  The `generate_answer` method is called with a user prompt and optional conversation history.
2.  If the conversation history is provided, it is used to generate the answer. Otherwise, the user prompt is used directly.
3.  The method tries to generate an answer using the Groq API and the current model. If the model fails, it is removed from the list of available models.
4.  The process is repeated until an answer is generated or all models have been tried.
5.  The generated answer is returned to the caller.

### Important Assumptions, Inputs, Outputs, and Side Effects
The `GPTModel` and `AsyncGPTModel` classes assume that the Groq API is available and functional. The inputs to these classes include the user prompt and optional conversation history. The outputs are the generated answers, which can be used to respond to user queries. The side effects of these classes include the modification of the conversation history and the removal of failed models from the list of available models.

## <a name="model"></a> Model Documentation
The `Model` and `AsyncModel` classes provide the basic functionality for text generation. They are inherited by the `GPTModel` and `AsyncGPTModel` classes and provide the core functionality for generating answers to user prompts.

### Responsibility
The primary responsibility of the `Model` and `AsyncModel` classes is to provide a basic implementation for text generation. They handle the conversation history and provide methods for generating answers to user prompts.

### Interactions with Other Parts of the System
The `Model` and `AsyncModel` classes interact with the following components:

*   `History` class: Used to store the conversation history, including user prompts and model responses.
*   `GPTModel` and `AsyncGPTModel` classes: Inherited by these classes, which provide the specific implementation for text generation using the Groq API.

### Key Functions and Classes
The key functions and classes in the `Model` and `AsyncModel` classes are:

*   `generate_answer`: Generates an answer to a user prompt.
*   `get_answer`: Adds the user prompt to the conversation history and generates an answer using the `generate_answer` method.
*   `get_answer_without_history`: Generates an answer without considering the conversation history.
*   `History` class: Stores the conversation history, including user prompts and model responses.

### Logic Flow
The logic flow of the `Model` and `AsyncModel` classes is as follows:

1.  The `generate_answer` method is called with a user prompt and optional conversation history.
2.  If the conversation history is provided, it is used to generate the answer. Otherwise, the user prompt is used directly.
3.  The method generates an answer using the specific implementation provided by the inherited classes.
4.  The generated answer is returned to the caller.

### Important Assumptions, Inputs, Outputs, and Side Effects
The `Model` and `AsyncModel` classes assume that the conversation history is available and functional. The inputs to these classes include the user prompt and optional conversation history. The outputs are the generated answers, which can be used to respond to user queries. The side effects of these classes include the modification of the conversation history.

## <a name="base_factory"></a> Base Factory Documentation
The `BaseModule` and `DocFactory` classes provide a basic implementation for generating documentation. They are used to combine the outputs of multiple modules to generate a complete documentation.

### Responsibility
The primary responsibility of the `BaseModule` and `DocFactory` classes is to provide a basic implementation for generating documentation. They handle the combination of module outputs and provide methods for generating the final documentation.

### Interactions with Other Parts of the System
The `BaseModule` and `DocFactory` classes interact with the following components:

*   `IntroLinks` and `IntroText` classes: Used to generate the introduction and links for the documentation.
*   Other modules: Used to generate the content of the documentation.

### Key Functions and Classes
The key functions and classes in the `BaseModule` and `DocFactory` classes are:

*   `generate`: Generates the output of a module.
*   `generate_doc`: Combines the outputs of multiple modules to generate the final documentation.

### Logic Flow
The logic flow of the `BaseModule` and `DocFactory` classes is as follows:

1.  The `generate` method is called on each module to generate its output.
2.  The `generate_doc` method is called to combine the outputs of all modules.
3.  The combined output is returned as the final documentation.

### Important Assumptions, Inputs, Outputs, and Side Effects
The `BaseModule` and `DocFactory` classes assume that the modules are available and functional. The inputs to these classes include the module outputs. The outputs are the combined module outputs, which form the final documentation. The side effects of these classes include the modification of the module outputs.

## <a name="intro"></a> Intro Documentation
The `IntroLinks` and `IntroText` classes provide a specific implementation for generating the introduction and links for the documentation. They are used to generate the introduction and links based on the provided information.

### Responsibility
The primary responsibility of the `IntroLinks` and `IntroText` classes is to generate the introduction and links for the documentation. They handle the extraction of links and generation of introduction text.

### Interactions with Other Parts of the System
The `IntroLinks` and `IntroText` classes interact with the following components:

*   `BaseModule` and `DocFactory` classes: Used to generate the introduction and links as part of the documentation.
*   `get_all_html_links`, `get_links_intro`, and `get_introdaction` functions: Used to extract links and generate introduction text.

### Key Functions and Classes
The key functions and classes in the `IntroLinks` and `IntroText` classes are:

*   `generate`: Generates the introduction and links.
*   `get_all_html_links`, `get_links_intro`, and `get_introdaction` functions: Used to extract links and generate introduction text.

### Logic Flow
The logic flow of the `IntroLinks` and `IntroText` classes is as follows:

1.  The `generate` method is called to generate the introduction and links.
2.  The `get_all_html_links`, `get_links_intro`, and `get_introdaction` functions are called to extract links and generate introduction text.
3.  The generated introduction and links are returned as the output.

### Important Assumptions, Inputs, Outputs, and Side Effects
The `IntroLinks` and `IntroText` classes assume that the information is available and functional. The inputs to these classes include the information. The outputs are the generated introduction and links, which are used as part of the documentation. The side effects of these classes include the modification of the introduction and links.

## <a name="manager-class"></a> Manager Class
The `Manager` class is a crucial component of the system, responsible for orchestrating the documentation generation pipeline. It interacts with other parts of the system, including the `CodeMix` class for code extraction, the `DocFactory` class for introduction generation, and various preprocessor modules for data splitting, compression, and post-processing.

### <a name="responsibility"></a> Responsibility
The `Manager` class is responsible for:

* Initializing the project directory and cache folder
* Generating the code mix file using the `CodeMix` class
* Generating the global info file by splitting and compressing the code mix data
* Generating the documentation parts using the `gen_doc_parts` or `async_gen_doc_parts` functions
* Generating the introduction and links using the `DocFactory` class

### <a name="interaction-with-other-components"></a> Interaction with Other Components
The `Manager` class interacts with the following components:

* `CodeMix` class: used to generate the code mix file
* `DocFactory` class: used to generate the introduction and links
* Preprocessor modules: used for data splitting, compression, and post-processing

### <a name="key-functions-and-logic-flows"></a> Key Functions and Logic Flows
The key functions and logic flows of the `Manager` class are:

* `generate_code_file`: generates the code mix file using the `CodeMix` class
* `generate_global_info_file`: generates the global info file by splitting and compressing the code mix data
* `generete_doc_parts`: generates the documentation parts using the `gen_doc_parts` or `async_gen_doc_parts` functions
* `factory_generate_doc_intro`: generates the introduction and links using the `DocFactory` class

### <a name="important-assumptions-and-inputs"></a> Important Assumptions and Inputs
The `Manager` class assumes that the project directory and cache folder are properly initialized. The inputs to the `Manager` class include:

* `project_directory`: the path to the project directory
* `ignore_files`: a list of files to ignore during the documentation generation process
* `language`: the language of the documentation
* `progress_bar`: an optional progress bar object for visual feedback

### <a name="outputs-and-side-effects"></a> Outputs and Side Effects
The outputs of the `Manager` class include:

* The generated code mix file
* The generated global info file
* The generated documentation parts
* The generated introduction and links

The side effects of the `Manager` class include:

* Creating the cache folder and files
* Writing to the files generated during the documentation process

### <a name="example-usage"></a> Example Usage
```python
manager = Manager(
    project_directory=r"C:\Users\huina\Python Projects\Impotant projects\AutoDocGenerateGimini",
    ignore_files=ignore_list,
    language="en",
    progress_bar=progress
)

manager.generate_code_file()
manager.generate_global_info_file(use_async=True, max_symbols=7000)
manager.generete_doc_parts(use_async=True, max_symbols=5000)
manager.factory_generate_doc_intro(
    DocFactory(
        IntroText(),
        IntroLinks(),
    )
)
```

## CodeMix Class
### Overview
The `CodeMix` class is responsible for serializing the contents of a repository into a single text file. It recursively traverses the directory tree, ignoring files and directories that match specified patterns.

### Attributes
* `root_dir`: The root directory of the repository.
* `ignore_patterns`: A list of patterns to ignore when traversing the directory tree.

### Methods
* `__init__`: Initializes the `CodeMix` object with the specified `root_dir` and `ignore_patterns`.
* `should_ignore`: Checks if a given path should be ignored based on the specified patterns.
* `build_repo_content`: Serializes the repository contents into a single text file.

## Compressor Module
### Overview
The compressor module provides functions for compressing text data using a language model. It supports both synchronous and asynchronous compression.

### Functions
* `compress`: Compresses a single text string using a language model.
* `compress_and_compare`: Compresses a list of text strings in parallel using a language model.
* `async_compress`: Asynchronously compresses a single text string using a language model.
* `async_compress_and_compare`: Asynchronously compresses a list of text strings in parallel using a language model.
* `compress_to_one`: Recursively compresses a list of text strings until only one string remains.

### Parameters
* `data`: The text data to be compressed.
* `model`: The language model used for compression.
* `compress_power`: The compression power (default: 4).
* `progress_bar`: A progress bar object (optional).

### Returns
* The compressed text data.

## Example Usage
```python
from preprocessor.code_mix import CodeMix
from preprocessor.compressor import compress_to_one

# Create a CodeMix object
code_mix = CodeMix(root_dir=".", ignore_patterns=["*.pyc", "__pycache__"])

# Build the repository contents
code_mix.build_repo_content("repo_contents.txt")

# Compress the repository contents
with open("repo_contents.txt", "r") as f:
    data = f.read()

compressed_data = compress_to_one([data], compress_power=4)

print(compressed_data)
```

## Advice
When using the `CodeMix` class, make sure to specify the correct `root_dir` and `ignore_patterns` to ensure that the repository contents are serialized correctly. When using the compressor module, adjust the `compress_power` parameter to achieve the desired level of compression. Additionally, consider using the asynchronous compression functions for larger datasets to improve performance.

## Introduction to Preprocessing Components
The given code snippets are part of a larger system designed for automatic documentation generation. This documentation will focus on the `postprocess.py` and `spliter.py` components, explaining their responsibilities, interactions, key functions, and logic flows within the context of the entire system.

## Postprocessing Component
### Responsibilities
The `postprocess.py` component is responsible for:
- Extracting topics from the generated documentation data.
- Generating markdown anchors for the extracted topics.
- Creating introductions based on the extracted topics or the entire documentation data.
- Interacting with the `GPTModel` to generate introductions.

### Key Functions
- `generate_markdown_anchor(header: str) -> str`: This function generates a markdown anchor from a given header string. It normalizes the string, replaces spaces with hyphens, removes non-alphanumeric characters, and strips leading/trailing hyphens.
- `get_all_topics(data: str) -> list[str]`: This function extracts topics from the given data by finding all occurrences of "\n## " followed by a topic title until a newline character. It returns a list of topics and their corresponding markdown anchors.
- `get_links_intro(links: list[str], language: str = "en")`: This function uses a `GPTModel` to generate an introduction based on the provided list of links and the specified language.
- `get_introdaction(global_data: str, language: str = "en") -> str`: This function generates an introduction for the given global data using a `GPTModel` and the specified language.

### Interactions
The `postprocess.py` component interacts with the `GPTModel` class from the `engine.models.gpt_model` module to generate introductions. It also relies on configurations from the `engine.config.config` module for introduction creation.

## Splitter Component
### Responsibilities
The `spliter.py` component is responsible for splitting the generated data into smaller chunks based on a maximum symbol limit. This is crucial for preprocessing the data for further analysis or processing.

### Key Functions
- `split_data(data: str, max_symbols: int) -> list[str]`: This function splits the input data into chunks, ensuring each chunk does not exceed the specified `max_symbols` limit.

### Interactions
The `spliter.py` component interacts with the `GPTModel` and its asynchronous variants from the `engine.models.gpt_model` module, although the provided snippet does not explicitly show this interaction. It also uses the `rich` library for progress visualization.

## System Context
Both components are integral parts of a larger pipeline for automatic documentation generation. The `postprocess.py` component extracts relevant information and generates introductions, while the `spliter.py` component preprocesses the data by splitting it into manageable chunks. These components work together with other parts of the system, such as the `code_mix.py` and `manage.py` modules, to orchestrate the documentation generation process.

## Usage Example
```python
from preprocessor.postprocess import get_all_topics, get_introdaction
from preprocessor.spliter import split_data

# Assuming 'data' is the generated documentation content
topics, links = get_all_topics(data)
intro = get_introdaction(data)

# Split the data into chunks
chunks = split_data(data, max_symbols=8000)

# Further processing or analysis can be performed on 'chunks'
```

<a name="overview"></a>
## Overview  

The fragment implements the **documentation‑generation stage** of the automatic doc‑builder pipeline.  
After the source code has been merged into a single *code‑mix* string and a concise *global‑info* summary has been created, this module splits the large text into manageable chunks, sends each chunk to a language‑model backend (synchronous or asynchronous), and stitches the returned markdown pieces into the final documentation body.  

It lives under `factory/` (or a similar package) and is invoked by `Manager.generete_doc_parts` / `Manager.async_gen_doc_parts` from *manage.py*.

<a name="responsibility"></a>
## Responsibility  

* **Chunking** – `split_data` (imported from the pre‑processor) breaks the huge `full_code_mix` into pieces that respect the model‑token limit (`max_symbols`).  
* **Prompt construction** – `write_docs_by_parts` / `async_write_docs_by_parts` build a chat‑style prompt that includes:  
  * language hint,  
  * a system instruction (`BASE_PART_COMPLITE_TEXT`),  
  * the global project summary,  
  * the current code fragment,  
  * optionally the previous fragment’s output (to keep continuity).  
* **Model interaction** – Calls `Model.get_answer_without_history` (sync) or `AsyncModel.get_answer_without_history` (async) to obtain a markdown‑formatted documentation snippet.  
* **Result post‑processing** – Strips surrounding triple‑backticks that the model may add.  
* **Progress tracking** – Updates a Rich `Progress` bar for visual feedback.  
* **Aggregation** – Concatenates all generated parts into a single markdown string returned to the caller.

<a name="interaction"></a>
## Interaction with Other Components  

| Component | How this code uses it |
|-----------|----------------------|
| `split_data` (preprocessor) | Produces a list of code fragments ≤ `max_symbols`. |
| `Model` / `AsyncModel` (engine/models) | Sends the constructed prompt and receives raw model output. |
| `GPTModel` / `AsyncGPTModel` (engine/models implementation) | Concrete implementations instantiated inside `gen_doc_parts` / `async_gen_doc_parts`. |
| `Progress` (rich) | Passed from `Manager`; this module creates sub‑tasks, updates them, and removes them when done. |
| `BASE_PART_COMPLITE_TEXT` (constants) | Fixed system prompt that tells the model how a documentation part should look. |

<a name="key_functions"></a>
## Key Functions  

| Function | Purpose | Important Parameters | Returns |
|----------|---------|----------------------|---------|
| **`write_docs_by_parts(part, model, global_info, prev_info=None, language="en")`** | Synchronous generation of a documentation chunk. | `part` – code fragment; `model` – `Model` instance; `global_info` – project summary; `prev_info` – last generated snippet (optional); `language` – UI language. | Cleaned markdown string (backticks removed). |
| **`async_write_docs_by_parts(part, async_model, global_info, semaphore, prev_info=None, language="en", update_progress=None)`** | Same as above but async, respecting a semaphore to limit concurrency. | Same as sync version plus `semaphore` (concurrency limiter) and `update_progress` callback. | Cleaned markdown string (awaitable). |
| **`gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar)`** | Orchestrates the synchronous pipeline: split, iterate, call `write_docs_by_parts`, aggregate, update progress. | `full_code_mix` – merged source; `global_info` – summary; `max_symbols` – token budget; `language`; `progress_bar`. | Full documentation string. |
| **`async_gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar)`** | Asynchronous counterpart: creates tasks for each chunk, runs them concurrently, gathers results. | Same inputs; internally creates a `asyncio.Semaphore(4)` and an `AsyncGPTModel`. | Full documentation string (awaitable). |

<a name="logic_flow"></a>
## Logic Flow (Sync Example)  

1. **Chunking** – `splited_data = split_data(full_code_mix, max_symbols)`.  
2. **Progress sub‑task** – `sub_task = progress_bar.add_task(...)`.  
3. **Model loop** – For each chunk `el`:  
   * Call `write_docs_by_parts(el, model, global_info, result, language)`.  
   * Append the answer to `all_result`.  
   * Keep a sliding window (`result = result[-3000:]`) so the next call can reference recent context.  
   * Advance the progress bar.  
4. **Cleanup** – Remove the sub‑task and return the concatenated markdown.  

The async version follows the same steps but builds a list of coroutine tasks and runs them with `asyncio.gather`, allowing up to four concurrent model calls (controlled by the semaphore).

<a name="assumptions"></a>
## Assumptions, Inputs & Outputs  

* **Assumptions**  
  * `BASE_PART_COMPLITE_TEXT` is defined elsewhere and provides a complete system prompt.  
  * The language model returns markdown wrapped in triple backticks (```````), which we strip.  
  * `max_symbols` approximates the model’s token limit; the splitter guarantees each chunk stays below it.  
* **Inputs**  
  * `full_code_mix` – a long string containing the whole repository source.  
  * `global_info` – a concise overview of the project (produced by the *global‑info* step).  
  * `max_symbols` – integer token budget per request.  
  * `language` – ISO language code for the system prompt.  
  * `progress_bar` – Rich `Progress` instance for UI feedback.  
* **Outputs**  
  * A single markdown string containing the automatically generated documentation for the entire codebase.  

<a name="side_effects"></a>
## Side Effects  

* Network / API calls to the underlying LLM service (may raise exceptions).  
* Updates to the supplied `Progress` bar (visual side effect).  
* Potential rate‑limit throttling mitigated by the semaphore in async mode.

<a name="usage_example"></a>
## Usage Example (Sync)  

```python
from rich.progress import Progress
from factory.doc_parts import gen_doc_parts   # <-- this file's module
from preprocessor.compressor import compress_to_one   # produces full_code_mix
from preprocessor.spliter import split_data
from preprocessor.postprocess import get_all_topics

progress = Progress()
with progress:
    # full_code_mix already prepared earlier
    doc_md = gen_doc_parts(
        full_code_mix=full_code_mix,
        global_info=global_summary,
        max_symbols=6000,
        language="en",
        progress_bar=progress,
    )
print(doc_md)
```

The async variant is identical except that the caller `await`s `async_gen_doc_parts` inside an event loop.  

---  


