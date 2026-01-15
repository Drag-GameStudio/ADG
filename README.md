**Project Title:** 
Language Model Framework for Text Processing and Documentation

**Project Goal:** 
This project aims to provide a lightweight and extensible framework for interacting with large language models (LLMs) hosted on Groq, enabling efficient text processing, and documentation generation. The framework solves the problem of simplifying the integration of LLMs into various natural language processing tasks, such as text summarization, question answering, and text generation.

**Core Logic & Principles:** 
The framework consists of two primary classes: `GPTModel` (synchronous) and `AsyncGPTModel` (asynchronous), which wrap Groq's chat API and provide a retry mechanism with a list of alternative models. The core logic involves the following steps:

* User input is processed by the `preprocessor` module, which handles tasks such as compression, splitting, and tokenization.
* The framework selects an LLM model from a list of alternatives, using a retry mechanism if the initial model fails.
* The selected LLM model generates a response, which is then post-processed by the `postprocess` module.
* The conversation history is updated after each response, enabling context-aware conversations.

The framework utilizes a combination of natural language processing (NLP) and machine learning algorithms to process and compress large text data. The `CodeMix` module is responsible for packing and compressing code repositories, while the `GPTModel` class interacts with the language model to generate text based on given prompts.

**Key Features:** 
* Synchronous and asynchronous interaction with LLMs
* Preprocessing and post-processing capabilities
* Conversation history management
* Retry mechanism with alternative models
* Support for compressing and documenting large text data
* Extensible architecture for integrating with various NLP tasks

**How to Run:** 
To run the framework, follow these steps:

1. Install the required dependencies, including the language model and preprocessor module.
2. Set up a valid API key for accessing the LLM models.
3. Create a `.env` file with the necessary configuration settings.
4. Run the framework using the `manage.py` script for synchronous execution or the `asyncio` library for asynchronous execution.
5. Pass in your input text data and compression power parameter to generate a compressed and documented version of your input text data.

**Dependencies:** 
* Groq's chat API
* Language model (e.g., GPT-3)
* Preprocessor module
* `asyncio` library (for asynchronous execution)
* `manage.py` script (for synchronous execution)
* `.env` file with configuration settings

Note: The specific dependencies may vary depending on the chosen language model and preprocessor module.

📂 **Core Modules**
* [engine-init](#engine-init) 
* [config_module](#config_module) 
* [gptmodel](#gptmodel) 
* [model](#model) 
* [manager-class](#manager-class) 

📂 **Data Processing**
* [code-mix-and-compressor-modules](#code-mix-and-compressor-modules) 
  + [code-mix-module](#code-mix-module) 
  + [compressor-module](#compressor-module) 
* [responsibility-and-interaction](#responsibility-and-interaction) 
* [key-functions-and-logic-flows](#key-functions-and-logic-flows) 

📄 **Important Components**
* [GPTModel](#GPTModel) 
* [engine.config.config](#engine.config.config) 

⚙️ **Services**
* [split_data](#split_data) 
* [get_introdaction](#get_introdaction) 



<a name="engine-init"></a>
## engine/__init__.py

The **`engine`** package is the core of the lightweight LLM‑interaction framework.  
`__init__.py` is the entry point that makes the package usable from the outside.  
Its responsibilities are:

1. **Exposing the public API** – imports the most frequently used classes and objects
   so that callers can simply write `from engine import GPTModel` instead of
   digging into sub‑packages.  
2. **Configuring the package** – pulls configuration defaults from
   `engine.config.config` and attaches them to the exported namespace.
3. **Setting up logging / runtime helpers** – (if present) ensures that all
   internal modules share a single logger instance and that environment variables
   such as the Groq API key are read once.

### Typical layout

```python
# engine/__init__.py
"""
Central package for the LLM‑helper framework.

The file imports the key components from the sub‑packages and defines the
public interface.  All users import from `engine` instead of the deeper
modules, keeping their code clean and making refactoring easier.

Example usage:

    from engine import GPTModel, AsyncGPTModel, config

    model = GPTModel(api_key=config.GROQ_KEY, model_list=["gpt-4o-mini"])
```

```python
# Import the configuration singleton
from .config import config

# Re‑export model classes for convenience
from .models.gpt_model import GPTModel, AsyncGPTModel

# Optional: expose utility helpers
from .models.model import ModelBase
```

```python
__all__ = [
    "config",
    "GPTModel",
    "AsyncGPTModel",
    "ModelBase",
]
```

### Interaction with the rest of the system

| Component | Role in the system | What it receives | What it returns |
|-----------|-------------------|------------------|-----------------|
| `config` | Holds API keys, model lists, token limits | read‑only | dictionary/attributes |
| `GPTModel` | Synchronous wrapper around Groq’s chat API | user prompt + optional history | raw LLM text |
| `AsyncGPTModel` | Asynchronous counterpart | same | coroutine returning LLM text |

By centralising imports here, the rest of the project (e.g. `manage.py`,
`preprocessor/*.py`) can use a single import statement while the package
maintains internal separation.  This file therefore acts as the *public
surface* of the framework.

### Important notes

* **Assumptions** – The API key is already present in `config.GROQ_KEY`.  
  If it is missing, importing this module will raise an informative
  `EnvironmentError`.
* **Side effects** – No heavy computation is performed on import.  The file
  simply binds names; all real work (model calls, preprocessing, etc.)
  occurs in the respective sub‑modules.
* **Extensibility** – Adding a new helper class only requires an extra
  import here and an update to `__all__`.  External callers remain untouched.

---

## <a name="config_module"></a>Config Module
The provided code snippet is a part of the `config` module, which appears to be responsible for storing and managing configuration settings for a larger project.

### Responsibility of this Component
The `config` module is responsible for:

* Storing API key and model names
* Providing functions to generate text for various tasks

### Interaction with other Parts of the System
The `config` module interacts with other parts of the system by providing the API key and model names to be used in the project. It also provides functions to generate text for tasks such as compressing code snippets and creating project overviews.

### Key Functions and Classes
The `config` module contains the following key functions and classes:

* `get_BASE_COMPRESS_TEXT`: a function that generates text for compressing code snippets
* `BASE_SYSTEM_TEXT`, `BASE_COMPRESS_TEXT`, `BASE_PART_COMPLITE_TEXT`, `BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`: constants that store text templates for various tasks

### Important Assumptions, Inputs, Outputs, and Side Effects
The `config` module assumes that the API key is stored in a `.env` file and can be loaded using the `load_dotenv` function. The module also assumes that the model names are predefined and stored in the `MODELS_NAME` list.

The inputs to the `config` module include the API key and model names. The outputs of the module include the generated text for various tasks.

### Side Effects
The `config` module has the side effect of loading the API key from the `.env` file, which may have security implications if not handled properly.

### Usage
To use the `config` module, you would need to import it and access the functions and constants as needed. For example:
```python
from config import get_BASE_COMPRESS_TEXT, MODELS_NAME

# Generate text for compressing a code snippet
compress_text = get_BASE_COMPRESS_TEXT(10000, 2)

# Access the model names
model_names = MODELS_NAME
```
Note that the `config` module is not a full code, but rather a part of a larger project. The functionality of the module may be extended or modified based on the requirements of the project.

<a name="gptmodel"></a>
## GPTModel / AsyncGPTModel  
**Purpose** – Concrete wrappers around the Groq chat API that provide synchronous and asynchronous LLM calls with a built‑in retry strategy.  

| Class | Base | Key fields |
|-------|------|------------|
| `GPTModel` | `Model` | `client: Groq` |
| `AsyncGPTModel` | `AsyncModel` | `client: AsyncGroq` |

### Construction
```python
model = GPTModel(api_key="sk‑…", history=History())
```
- `api_key` is pulled from `.config.config` by default.  
- `history` holds the conversation context. If omitted, a fresh `History` instance is created.

### Core logic – `generate_answer`
```python
def generate_answer(self, with_history=True, prompt=None) -> str
```
1. **Message selection** –  
   * If `with_history` is `True`, the entire chat history (`self.history.history`) is sent.  
   * Otherwise the provided `prompt` list of messages is used directly.

2. **Model retry loop** –  
   * `self.regen_models_name` contains a shuffled list of model names (`MODELS_NAME`).  
   * The loop picks the current model and attempts `client.chat.completions.create`.  
   * On any exception the model is removed from the list and the loop starts over with the next model (index reset to `0`).  
   * When all models fail an explicit `Exception("all models do not work")` is raised.

3. **Return value** – the text of the first assistant choice.

`AsyncGPTModel` implements the same logic with `await` and `AsyncGroq`.

### Interaction with other components
- **History** – records user and assistant turns so that the next call can include the conversation context.  
- **ParentModel** – provides the shared `api_key`, `history`, and the shuffled `regen_models_name` list.

---

<a name="history"></a>
## History
Manages a list of role‑content dictionaries that represent the chat history.

```python
history = History()                     # auto‑adds system prompt
history.add_to_history("user", "Hi")
```

- `history.history` is the raw list passed to the Groq API.  
- The constructor adds a single system prompt (`BASE_SYSTEM_TEXT`) if provided.

---

<a name="parentmodel"></a>
## ParentModel
A lightweight container that stores common state for both sync and async models.

- `api_key`, `history`.
- `current_model_index` (starts at `0`).
- `regen_models_name` – a shuffled copy of `MODELS_NAME` that is used by the retry logic.

---

<a name="model"></a>
## Model / AsyncModel (abstract)
Provide convenience wrappers around `generate_answer`:

| Method | Description |
|--------|-------------|
| `get_answer(prompt)` | Adds user message, calls `generate_answer`, then records assistant response. |
| `get_answer_without_history(prompt)` | Calls `generate_answer` without the full history. |
| `generate_answer` | Abstract placeholder; overridden in `GPTModel`/`AsyncGPTModel`. |

Both sync and async versions behave the same from the caller’s perspective; the async variant can be awaited.

---

<a name="usage"></a>
## Usage Example
```python
from engine.models.gpt_model import GPTModel

model = GPTModel()          # uses default API key and history
response = model.get_answer("Explain recursion in Python.")
print(response)
```

For async usage:

```python
import asyncio
from engine.models.gpt_model import AsyncGPTModel

async def run():
    async_model = AsyncGPTModel()
    print(await async_model.get_answer("Summarize the repo"))

asyncio.run(run())
```

---

### Assumptions & Side‑Effects
- The environment holds a valid Groq API key (`API_KEY`).
- `MODELS_NAME` must be a non‑empty list; otherwise the retry loop never succeeds.
- Each successful API call mutates `history` to keep the conversation state intact.

This module is the core interaction layer between the rest of the framework and the LLM, enabling retryable, stateful, and context‑aware queries.

<a name="manager-class"></a>
## Manager Class
The `Manager` class is responsible for orchestrating the pipeline of generating documentation for a repository. It handles the creation of a code mix file, global info file, and output doc file.

### Responsibilities
* Creates a cache folder to store temporary files
* Generates a code mix file using the `CodeMix` class
* Generates a global info file by compressing the code mix file
* Generates doc parts using the `gen_doc_parts` function
* Generates an intro and links for the output doc file

### Attributes
* `project_directory`: The path to the repository directory
* `ignore_files`: A list of files to ignore during the code mix generation
* `progress_bar`: A progress bar object to display progress
* `language`: The language of the repository (default is "en")

### Methods
* `__init__`: Initializes the `Manager` object with the project directory, ignore files, progress bar, and language
* `get_file_path`: Returns the path to a file in the cache folder
* `generate_code_file`: Generates a code mix file using the `CodeMix` class
* `generate_global_info_file`: Generates a global info file by compressing the code mix file
* `generete_doc_parts`: Generates doc parts using the `gen_doc_parts` function
* `generate_intro`: Generates an intro and links for the output doc file

### Interactions
* The `Manager` class interacts with the `CodeMix` class to generate a code mix file
* The `Manager` class interacts with the `gen_doc_parts` function to generate doc parts
* The `Manager` class interacts with the `generate_intro` function to generate an intro and links for the output doc file

### Key Functions
* `generate_code_file`: Generates a code mix file
* `generate_global_info_file`: Generates a global info file
* `generete_doc_parts`: Generates doc parts
* `generate_intro`: Generates an intro and links for the output doc file

### Important Assumptions
* The repository directory is a valid path
* The ignore files list is a list of strings
* The progress bar object is a valid object
* The language is a valid string (default is "en")

### Usage Guide
1. Create a `Manager` object with the project directory, ignore files, progress bar, and language
2. Call the `generate_code_file` method to generate a code mix file
3. Call the `generate_global_info_file` method to generate a global info file
4. Call the `generete_doc_parts` method to generate doc parts
5. Call the `generate_intro` method to generate an intro and links for the output doc file

### Example Use Case
```python
manager = Manager(r"C:\Users\huina\Python Projects\Impotant projects\AutoDocGenerateGimini", ignore_list, progress_bar=progress, language="en")
manager.generate_code_file()
manager.generate_global_info_file(use_async=True, max_symbols=7000)
manager.generete_doc_parts(use_async=True, max_symbols=5000)
manager.generate_intro()
```

## <a name="code-mix-and-compressor-modules"></a>
The provided code consists of two main modules: `code_mix.py` and `compressor.py`. These modules are part of a larger system that processes and compresses large amounts of text data using natural language processing (NLP) and machine learning algorithms.

### <a name="code-mix-module"></a>
#### Code Mix Module
The `code_mix.py` module contains a class `CodeMix` that is responsible for packing and compressing code repositories. The class has the following methods:

*   `__init__`: Initializes the `CodeMix` object with a root directory and a list of ignore patterns.
*   `should_ignore`: Checks if a given path should be ignored based on the ignore patterns.
*   `build_repo_content`: Builds the repository content by traversing the directory tree and writing the file structure and contents to an output file.

### <a name="compressor-module"></a>
#### Compressor Module
The `compressor.py` module contains functions for compressing text data using a language model. The module has the following functions:

*   `compress`: Compresses a given text using a language model and a compress power.
*   `compress_and_compare`: Compresses a list of texts and compares the results.
*   `async_compress`: Asynchronously compresses a given text using a language model and a compress power.
*   `async_compress_and_compare`: Asynchronously compresses a list of texts and compares the results.
*   `compress_to_one`: Compresses a list of texts to a single text using a compress power and an optional asynchronous approach.

### <a name="responsibility-and-interaction"></a>
#### Responsibility and Interaction
The `code_mix.py` module is responsible for packing and compressing code repositories, while the `compressor.py` module is responsible for compressing text data using a language model. The two modules interact by using the `CodeMix` class to generate a text representation of the repository structure and contents, which is then compressed using the `compressor.py` module.

### <a name="key-functions-and-logic-flows"></a>
#### Key Functions and Logic Flows
The key functions and logic flows in the provided code are:

*   The `build_repo_content` method in the `code_mix.py` module, which builds the repository content by traversing the directory tree and writing the file structure and contents to an output file.
*   The `compress` function in the `compressor.py` module, which compresses a given text using a language model and a compress power.
*   The `compress_to_one` function in the `compressor.py` module, which compresses a list of texts to a single text using a compress power and an optional asynchronous approach.

### <a name="important-assumptions-and-inputs"></a>
#### Important Assumptions and Inputs
The provided code assumes that the language model is capable of compressing text data and that the compress power is a positive integer. The inputs to the code include the repository structure and contents, the language model, and the compress power.

### <a name="side-effects-and-outputs"></a>
#### Side Effects and Outputs
The side effects of the provided code include the creation of an output file containing the compressed text data. The outputs of the code include the compressed text data and any error messages that may occur during processing.

### <a name="example-usage"></a>
#### Example Usage
To use the provided code, you can create a `CodeMix` object and call the `build_repo_content` method to generate a text representation of the repository structure and contents. You can then use the `compress` function in the `compressor.py` module to compress the text data using a language model and a compress power. Finally, you can use the `compress_to_one` function to compress the list of texts to a single text using a compress power and an optional asynchronous approach.

## Overview of the Code
The provided code snippet appears to be part of a larger system responsible for processing and generating text based on user input and predefined templates. The code is organized into two main files: `postprocess.py` and `spliter.py`, both located within the `preprocessor` directory.

## Postprocess Module
### Responsibilities
The `postprocess.py` file contains functions responsible for post-processing the generated text, including:

* Creating markdown anchors from header strings
* Extracting topics and links from the text
* Generating introductions based on the extracted links and global data

### Key Functions

* `generate_markdown_anchor(header: str) -> str`: This function takes a header string as input, normalizes it, replaces spaces with hyphens, and removes any non-alphanumeric characters to create a markdown anchor.
* `get_all_topics(data: str) -> list[str]`: This function extracts topics from the input text by finding all occurrences of "\n## " and extracting the text until the next newline character.
* `get_all_html_links(data: str) -> list[str]`: This function extracts HTML links from the input text by finding all occurrences of "<a name=" and extracting the link text.
* `get_introdaction(links: list[str], global_data: str, language: str = "en") -> str`: This function generates an introduction based on the extracted links and global data. It uses a `GPTModel` instance to generate the introduction.

## Spliter Module
### Responsibilities
The `spliter.py` file contains functions responsible for splitting the input text into smaller chunks, possibly for processing by a language model.

* `split_data(data: str, max_symbols: int) -> list[str]`: This function splits the input text into chunks based on a maximum symbol count.

## Interaction with Other Components
The `postprocess.py` and `spliter.py` files interact with other components of the system, including:

* `GPTModel`: A class responsible for interacting with a language model to generate text based on given prompts.
* `engine.config.config`: A module containing configuration settings, including templates for introductions and other text generation tasks.

## Important Assumptions and Inputs
The code assumes that the input text is well-formed and contains the necessary structure for topic and link extraction. The `get_introdaction` function assumes that the `GPTModel` instance is properly configured and can generate introductions based on the input prompts.

## Outputs and Side Effects
The `postprocess.py` functions generate processed text, including markdown anchors, extracted topics and links, and introductions. The `spliter.py` function splits the input text into chunks. The side effects of these functions include the creation of new text strings and the potential modification of the input text.

## Usage Guide
To use this code, you would need to:

1. Install the required dependencies, including the `GPTModel` class and the `rich` library.
2. Prepare your input text data, including the necessary structure for topic and link extraction.
3. Call the `get_introdaction` function, passing in the extracted links and global data, to generate an introduction.
4. Use the `split_data` function to split the input text into chunks, if necessary.

<a name="data_splitting_and_documentation_generation"></a>
## Data Splitting and Documentation Generation
### Overview
The provided code snippet is part of a larger system responsible for generating documentation for large text data using a language model. The code includes functions for splitting the text data into smaller chunks, generating documentation for each chunk, and assembling the final document.

### Functions

#### `split_data(full_code_mix, max_symbols)`
<a name="split_data_function"></a>
Splits the input text data into smaller chunks based on the `max_symbols` parameter.

*   **Parameters:** `full_code_mix` (str) - the input text data, `max_symbols` (int) - the maximum number of symbols per chunk
*   **Returns:** list of str - a list ofchunks split from the input text data
*   **Logic:**

    *   The function iterates over the input text data, splitting it into chunks based on the `max_symbols` parameter.
    *   If a chunk exceeds the `max_symbols * 1.5` threshold, it is further split into two smaller chunks.
    *   The function returns a list of chunks.

#### `write_docs_by_parts(part, model, global_info, prev_info=None, language="en")`
<a name="write_docs_by_parts_function"></a>
Generates documentation for a given chunk of text data using a language model.

*   **Parameters:**

    *   `part` (str) - the chunk of text data
    *   `model` (Model) - the language model used for generating documentation
    *   `global_info` (str) - global information used for context
    *   `prev_info` (str, optional) - previous information used for context, defaults to None
    *   `language` (str, optional) - the language used for generating documentation, defaults to "en"
*   **Returns:** str - the generated documentation for the given chunk
*   **Logic:**

    *   The function constructs a prompt for the language model, including the given chunk, global information, and previous information (if available).
    *   The function uses the language model to generate documentation based on the prompt.
    *   The function removes any unnecessary prefix or suffix from the generated documentation.

#### `async_write_docs_by_parts(part, async_model, global_info, semaphore, prev_info=None, language="en", update_progress=None)`
<a name="async_write_docs_by_parts_function"></a>
Asynchronously generates documentation for a given chunk of text data using a language model.

*   **Parameters:**

    *   `part` (str) - the chunk of text data
    *   `async_model` (AsyncModel) - the asynchronous language model used for generating documentation
    *   `global_info` (str) - global information used for context
    *   `semaphore` (asyncio.Semaphore) - a semaphore used for controlling concurrency
    *   `prev_info` (str, optional) - previous information used for context, defaults to None
    *   `language` (str, optional) - the language used for generating documentation, defaults to "en"
    *   `update_progress` (callable, optional) - a callback function for updating progress, defaults to None
*   **Returns:** str - the generated documentation for the given chunk
*   **Logic:**

    *   The function asynchronously constructs a prompt for the language model, including the given chunk, global information, and previous information (if available).
    *   The function uses the asynchronous language model to generate documentation based on the prompt.
    *   The function removes any unnecessary prefix or suffix from the generated documentation.

#### `gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar)`
<a name="gen_doc_parts_function"></a>
Generates documentation for the given text data by splitting it into chunks and using a language model.

*   **Parameters:**

    *   `full_code_mix` (str) - the input text data
    *   `global_info` (str) - global information used for context
    *   `max_symbols` (int) - the maximum number of symbols per chunk
    *   `language` (str) - the language used for generating documentation
    *   `progress_bar` (Progress Bar) - a progress bar used for displaying progress
*   **Returns:** str - the generated documentation for the given text data
*   **Logic:**

    *   The function splits the input text data into chunks using the `split_data` function.
    *   The function generates documentation for each chunk using the `write_docs_by_parts` function.
    *   The function assembles the generated documentation for each chunk into a single document.

#### `async_gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar)`
<a name="async_gen_doc_parts_function"></a>
Asynchronously generates documentation for the given text data by splitting it into chunks and using an asynchronous language model.

*   **Parameters:**

    *   `full_code_mix` (str) - the input text data
    *   `global_info` (str) - global information used for context
    *   `max_symbols` (int) - the maximum number of symbols per chunk
    *   `language` (str) - the language used for generating documentation
    *   `progress_bar` (Progress Bar) - a progress bar used for displaying progress
*   **Returns:** str - the generated documentation for the given text data
*   **Logic:**

    *   The function splits the input text data into chunks using the `split_data` function.
    *   The function asynchronously generates documentation for each chunk using the `async_write_docs_by_parts` function.
    *   The function assembles the generated documentation for each chunk into a single document.

### Example Usage
```python
# Split the input text data into chunks
chunks = split_data(full_code_mix, max_symbols)

# Generate documentation for each chunk
docs = []
for chunk in chunks:
    doc = write_docs_by_parts(chunk, model, global_info)
    docs.append(doc)

# Assemble the generated documentation into a single document
final_doc = "\n\n".join(docs)

# Alternatively, use the async_gen_doc_parts function for asynchronous generation
final_doc_async = await async_gen_doc_parts(full_code_mix, global_info, max_symbols, language, progress_bar)
```
Note that the `model` and `async_model` variables should be instances of the `Model` and `AsyncModel` classes, respectively, and the `global_info` variable should contain the global information used for context. Additionally, the `progress_bar` variable should be an instance of a progress bar class.

