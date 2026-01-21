## Executive Navigation Tree
* 📂 Core Engine
  * [Key Functions and Logic Flows](#key-functions-and-logic-flows)
  * [Important Assumptions and Inputs](#important-assumptions-and-inputs)
  * [GPT Model Component](#gpt-model-component)
* ⚙️ Module Documentation
  * [Module Documentation](#module-documentation)
  * [Manager Class Documentation](#manager-class-documentation)
  * [Code Mixin Documentation](#code-mixin-documentation)
* 📄 Utility Components
  * [Compressor Component](#compressor-component)
  * [Postprocess Module](#postprocess-module)
  * [Split Data Function](#split-data-function)
* 📊 Data Processing
  * [Get All Topics](#get-all-topics)
  * [Get All HTML Links](#get-all-html-links)
  * [Generate Markdown Anchor](#generate-markdown-anchor)

**Project Title**: Auto Doc Generator

**Project Goal**: The Auto Doc Generator is a software tool designed to automatically generate documentation for Python projects. It aims to simplify the process of creating and maintaining documentation, making it easier for developers to focus on writing code. The tool uses a combination of natural language processing (NLP) and machine learning algorithms to analyze the codebase and produce high-quality documentation.

**Core Logic & Principles**: The Auto Doc Generator operates on the following core principles:
* It uses a Command-Line Interface (CLI) as the entry point, which parses arguments and calls the `gen_doc()` function.
* The `Manager` class acts as a high-level orchestrator, responsible for walking the repository, running pre-processing, GPT passes, and merging results.
* The pre-processing stage involves splitting source files into chunks, compressing, linking, and mixing code and comments.
* The Engine/GPT component uses an asynchronous wrapper for Large Language Models (LLMs), enforcing a maximum number of symbols per chunk.
* The Factory component builds the introductory section from module metadata.
* The UI component provides a thin wrapper around the `rich.Progress` library for progress reporting.
* The Settings component holds project metadata, including title and arbitrary key-value pairs.

The data flow of the Auto Doc Generator can be summarized as follows:
1. The user initiates the documentation generation process through the CLI.
2. The `Manager` class walks the repository, respecting the ignore list.
3. The `generate_code_file()` method creates a single "code_mix.txt" file.
4. The `generate_global_info_file()` method creates a global summary, using asynchronous processing with a maximum of 5,000 symbols per chunk.
5. The `generete_doc_parts()` method splits the project into section-level docs, using asynchronous processing with a maximum of 4,000 symbols per chunk.
6. The `factory_generate_doc_intro()` method prepares the introductory section using a custom `DocFactory`.
7. The final markdown documentation is retrieved and can be printed or persisted.

**Key Features**:
* Automatic generation of documentation for Python projects
* Support for asynchronous processing
* Customizable introductory section using a `DocFactory`
* Respect for ignore lists and project metadata
* Progress reporting using `rich.Progress`

**How to Run**:
1. Install the required dependencies, including `rich` and `transformers`.
2. Create a Python project with the necessary files and structure.
3. Run the `autodocgenerator` script, passing in the project directory and other optional arguments.
4. Follow the exact sequence of method calls as demonstrated in the usage example.

**Dependencies**:
* `rich` for progress reporting
* `transformers` for NLP and machine learning algorithms
* `pathlib` for file system operations
* `python` 3.7 or later for compatibility with the `asyncio` library

Note: The above dependencies are not exhaustive and may require additional libraries or tools to run the project.

 

The Manager class is instantiated with the following arguments (as shown in **autodocconfig.py**):

```python
Manager(
    project_path,          # str – path to the root of the project to document
    project_settings,      # ProjectSettings – object containing project metadata
    ignore_list,           # list[str] – patterns/files to exclude from processing
    progress_bar=...,      # optional – a progress‑bar object (e.g., LibProgress instance)
    language="en"          # optional – language code for the generated documentation
)
```

### Full example of usage

```python
from autodocgenerator.manage import Manager
from autodocgenerator.preprocessor.settings import ProjectSettings
from autodocgenerator.ui.progress_base import LibProgress
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

# 1. Define project settings
project_settings = ProjectSettings("Auto Doc Generator")
project_settings.add_info(
    "global idea",
    """This project was created to help developers make documentations for them projects"""
)

# 2. Define files/folders to ignore
ignore_list = [
    "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db", "data",
    "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore",
    ".ruff_cache", ".auto_doc_cache", "*.pyc", "__pycache__", ".git",
    ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles",
    ".mypy_cache"
]

# 3. Set up a Rich progress bar (optional, but used in the example)
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
) as progress:
    # 4. Create the Manager instance
    manager = Manager(
        project_path=".",               # current directory
        project_settings=project_settings,
        ignore_list=ignore_list,
        progress_bar=LibProgress(progress),  # wrap the Rich progress bar
        language="en"                  # documentation language
    )

    # 5. Run the generation steps (examples from autodocconfig.py)
    manager.generate_code_file()
    manager.generate_global_info_file(use_async=True, max_symbols=5000)
    manager.generete_doc_parts(use_async=True, max_symbols=4000)

    # 6. Create an intro using a factory (optional)
    from autodocgenerator.factory.base_factory import DocFactory
    from autodocgenerator.factory.modules.intro import IntroLinks, IntroText

    manager.factory_generate_doc_intro(
        DocFactory(
            IntroLinks(),
            IntroText(),
        )
    )

    # 7. Retrieve the final documentation
    output_md = manager.read_file_by_file_key("output_doc")
    print(output_md)
```

**Creating a custom module**

```python
# my_module.py
from autodocgenerator.factory.base_factory import BaseModule
from autodocgenerator.engine.models.model import Model

class MyModule(BaseModule):
    def __init__(self, prefix: str):
        super().__init__()
        self.prefix = prefix                     # any data you need

    def generate(self, info: dict, model: Model) -> str:
        # Example: return a simple text that uses the prefix and a value from `info`
        title = info.get("title", "Untitled")
        return f"{self.prefix} {title}"
```

**Using the module with `DocFactory`**

```python
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.engine.models.gpt_model import GPTModel
from my_module import MyModule

# 1. Create the model that will be passed to modules
model = GPTModel()                     # uses the default API key and history

# 2. Create instances of the modules you want in the documentation
intro_text   = IntroText()            # from autodocgenerator.factory.modules.intro
intro_links  = IntroLinks()           # from autodocgenerator.factory.modules.intro
custom_mod   = MyModule(prefix="##")  # your own module

# 3. Build the factory with the chosen modules (order matters)
factory = DocFactory(intro_text, intro_links, custom_mod)

# 4. Prepare the information dictionary expected by the modules
info = {
    "global_data": {"project_name": "Demo"},
    "full_data":   "<html><a href='https://example.com'>Link</a></html>",
    "language":    "en",
    "title":       "Demo Project"
}

# 5. Generate the documentation
doc_output = factory.generate_doc(info, model)

print(doc_output)
```

**What happens**

1. `DocFactory` stores the three module instances.  
2. `generate_doc` iterates over each module, calling its `generate(info, model)` method.  
3. Each module returns a string; `DocFactory` concatenates them with blank lines.  
4. The final string (`doc_output`) contains the combined documentation.

 

<a name="github-workflows"></a>
## GitHub Workflows
The provided code snippets are part of the GitHub Actions workflows for a project. There are two workflows defined: `docs.yml` and `main.yml`.

### Overview of `docs.yml`
The `docs.yml` workflow is responsible for:
* Checking out the code
* Setting up Python 3.12
* Installing the `autodocgenerator` package
* Running the documentation generation script (`autodocconfig.py`) with an API key
* Copying the generated documentation to the `README.md` file
* Committing and pushing the changes to the repository

### Overview of `main.yml`
The `main.yml` workflow is responsible for:
* Checking out the code
* Setting up Python 3.12
* Installing `poetry`
* Installing dependencies using `poetry install`
* Running `poetry publish` to build and publish the package
* Using a PyPI token for security

<a name="responsibilities-and-interactions"></a>
### Responsibilities and Interactions
These workflows interact with the following components:
* `autodocconfig.py`: the documentation generation script
* `autodocgenerator/`: the package being installed and used for documentation generation
* `poetry`: the package manager used for installing dependencies and publishing the package

<a name="key-functions-and-logic-flows"></a>
### Key Functions and Logic Flows
The key functions in these workflows are:
* `actions/checkout@v4`: checks out the code
* `actions/setup-python@v5`: sets up Python 3.12
* `pip install`: installs packages
* `poetry install`: installs dependencies
* `poetry publish`: builds and publishes the package

The logic flow is as follows:
1. Checkout the code
2. Set up Python 3.12
3. Install required packages (either `autodocgenerator` or `poetry` and dependencies)
4. Run the documentation generation script or build and publish the package
5. Commit and push changes (if applicable)

<a name="important-assumptions-and-inputs"></a>
### Important Assumptions and Inputs
* The API key and PyPI token are stored as secrets in the GitHub repository
* The `autodocconfig.py` script and `autodocgenerator` package are assumed to be functional and correctly configured
* The `poetry` package manager is assumed to be correctly configured and used for dependency management and package publishing.

## <a name="documentation_for_autodocconfigpy"></a>
### Overview
The provided code snippet is part of the `autodocconfig.py` file, which appears to be a configuration file for an auto-documentation generator. This component is responsible for generating documentation for a given project.

### Responsibility
The main responsibility of this component is to orchestrate the documentation generation process. It interacts with other parts of the system, such as the `Manager` class, to generate code files, global information files, and documentation parts.

### Key Functions and Classes
* `gen_doc`: This function takes in project settings, an ignore list, and a project path, and returns the generated documentation.
* `Manager`: This class is responsible for managing the documentation generation process. It has methods such as `generate_code_file`, `generate_global_info_file`, and `generete_doc_parts`.
* `ProjectSettings`: This class represents the project settings, which include information about the project, such as its name and description.

### Logic Flow
The logic flow of this component is as follows:

1. The `gen_doc` function is called with the project settings, ignore list, and project path.
2. The `Manager` class is instantiated with the project path, project settings, ignore list, and a progress bar.
3. The `Manager` class generates the code file, global information file, and documentation parts using its respective methods.
4. The `factory_generate_doc_intro` method is called to generate the documentation introduction.
5. The generated documentation is returned by the `read_file_by_file_key` method.

### Assumptions and Inputs
* The project settings and ignore list are assumed to be valid and correctly configured.
* The project path is assumed to be a valid directory path.
* The inputs to the `gen_doc` function are:
  + `project_settings`: An instance of the `ProjectSettings` class.
  + `ignore_list`: A list of strings representing the files and directories to ignore.
  + `project_path`: A string representing the path to the project directory.

### Outputs and Side Effects
* The output of the `gen_doc` function is the generated documentation as a string.
* The side effects of this component include the creation of files and directories in the project path, as well as the generation of documentation files.

## <a name="gpt_model_component"></a> GPT Model Component
The GPT Model component is responsible for generating answers to user prompts using the GPT model. It interacts with the `Model` and `AsyncModel` classes to provide a specific implementation of the model.

### Key Functions and Classes

* `AsyncGPTModel`: An asynchronous implementation of the GPT model.
* `GPTModel`: A synchronous implementation of the GPT model.
* `generate_answer`: A method that generates an answer to a user prompt.

### Logic Flow

1. The `generate_answer` method is called with a user prompt and an optional `with_history` parameter.
2. If `with_history` is `True`, the method uses the conversation history to generate an answer. Otherwise, it uses the provided prompt.
3. The method attempts to generate an answer using the current model. If an exception occurs, it resets the model index and tries again.
4. If all models fail, the method raises an exception.

### Important Assumptions and Inputs

* The `API_KEY` and `MODELS_NAME` variables are assumed to be defined in the `config` module.
* The `History` class is used to store conversation history.
* The `Groq` and `AsyncGroq` classes are used to interact with the GPT model API.

### Outputs and Side Effects

* The `generate_answer` method returns a generated answer to the user prompt.
* The conversation history is updated with the user prompt and the generated answer.

### Interaction with Other Components

* The GPT Model component interacts with the `Model` and `AsyncModel` classes to provide a specific implementation of the model.
* The component uses the `Groq` and `AsyncGroq` classes to interact with the GPT model API.
* The component uses the `History` class to store conversation history.

<a name="base_factory_documentation"></a>
## Base Factory Documentation
The base factory is responsible for generating documentation using various modules. It provides a foundation for creating different types of documentation.

### Class BaseModule
This abstract base class defines the interface for all modules.
*   It has an abstract method `generate` which takes in `info` and `model` as parameters.

### Class DocFactory
This class is responsible for generating documentation using multiple modules.
*   It takes in a variable number of `modules` as arguments in its constructor.
*   The `generate_doc` method iterates over each module, calls its `generate` method, and appends the result to the output string.

<a name="module_documentation"></a>
## Module Documentation
The modules are responsible for generating specific parts of the documentation.

### Class CustomModule
This module generates custom descriptions.
*   It takes in a `discription` as a parameter in its constructor.
*   The `generate` method uses the `generete_custom_discription` function to generate the custom description.

### Class IntroLinks
This module generates introduction links.
*   The `generate` method uses the `get_all_html_links` and `get_links_intro` functions to generate the introduction links.

### Class IntroText
This module generates introduction text.
*   The `generate` method uses the `get_introdaction` function to generate the introduction text.

### Key Logic Flows
1.  The `DocFactory` class is instantiated with one or more modules.
2.  The `generate_doc` method is called on the `DocFactory` instance, passing in `info` and `model` as arguments.
3.  Each module's `generate` method is called, and the results are appended to the output string.

### Important Assumptions
*   The `info` dictionary contains the necessary data for the modules to generate the documentation.
*   The `model` instance is provided to the modules for generating the documentation.

### Inputs and Outputs
*   Inputs:
    *   `info`: a dictionary containing the necessary data for the modules.
    *   `model`: an instance of the `Model` class.
*   Outputs:
    *   The generated documentation as a string.

### Side Effects
*   None, except for the potential side effects of the functions used by the modules (e.g., `generete_custom_discription`, `get_all_html_links`, etc.).

## <a name="manager-class-documentation"></a> Manager Class Documentation
The `Manager` class is a central component of the Auto Doc Generator system, responsible for orchestrating the document generation process.

### <a name="responsibility"></a> Responsibility
The `Manager` class is responsible for:

* Managing the project directory and cache folder
* Generating code files, global info files, and document parts
* Interacting with the `DocFactory` to generate document intros
* Updating the progress bar

### <a name="interactions"></a> Interactions
The `Manager` class interacts with the following components:

* `CodeMix`: used to generate code files
* `DocFactory`: used to generate document intros
* `Model` and `AsyncModel`: used to compress data and generate document parts
* `ProjectSettings`: used to store project settings and information
* `Progress` and `LibProgress`: used to display progress bars

### <a name="key-functions"></a> Key Functions
The `Manager` class has the following key functions:

* `generate_code_file()`: generates a code file using `CodeMix`
* `generate_global_info_file()`: generates a global info file using `Model` or `AsyncModel`
* `generete_doc_parts()`: generates document parts using `Model` or `AsyncModel`
* `factory_generate_doc_intro()`: generates a document intro using `DocFactory`

### <a name="inputs-outputs-side-effects"></a> Inputs, Outputs, and Side Effects
The `Manager` class has the following inputs, outputs, and side effects:

* Inputs:
  + `project_directory`: the project directory path
  + `project_settings`: the project settings object
  + `sync_model` and `async_model`: the model objects used for compression and generation
  + `ignore_files`: a list of files to ignore during code generation
  + `language`: the language code used for generation
  + `progress_bar`: the progress bar object used to display progress
* Outputs:
  + Generated code files, global info files, and document parts
  + Updated progress bar
* Side Effects:
  + Creation of cache folder and files
  + Overwriting of existing files

### <a name="assumptions"></a> Assumptions
The `Manager` class assumes that:

* The project directory and cache folder are writable
* The `Model` and `AsyncModel` objects are properly configured and authenticated
* The `DocFactory` object is properly configured and able to generate document intros

### <a name="example-usage"></a> Example Usage
The `Manager` class can be used as follows:
```python
manager = Manager(project_directory, project_settings, sync_model, async_model, ignore_files, language, progress_bar)
manager.generate_code_file()
manager.generate_global_info_file(use_async=True, max_symbols=5000)
manager.factory_generate_doc_intro(doc_factory)
```

<a name="code_mixin_documentation"></a>
## CodeMix Class Documentation
The `CodeMix` class is responsible for traversing a repository directory, ignoring specified files and directories, and generating a textual representation of the repository structure and content.

### Responsibility
This component is designed to:
* Traverse a repository directory
* Ignore files and directories based on a list of patterns
* Generate a textual representation of the repository structure and content

### Interactions with Other Parts of the System
The `CodeMix` class interacts with the following components:
* The file system: to traverse the repository directory and read file contents
* The `ignore_list`: a list of patterns to ignore when generating the repository content

### Key Functions and Logic Flows
The `CodeMix` class has two primary methods:
* `__init__`: initializes the object with a `root_dir` and an optional `ignore_patterns` list
* `should_ignore`: checks if a given path should be ignored based on the `ignore_patterns` list
* `build_repo_content`: generates the textual representation of the repository structure and content

The `build_repo_content` method:
1. Opens the output file for writing
2. Iterates over all files and directories in the repository, ignoring those that match the `ignore_patterns` list
3. Writes the repository structure to the output file
4. Iterates over all files in the repository, reading and writing their contents to the output file

### Important Assumptions, Inputs, Outputs, and Side Effects
* Assumptions:
  + The `root_dir` exists and is a directory
  + The `ignore_patterns` list contains valid glob patterns
* Inputs:
  + `root_dir`: the path to the repository directory
  + `ignore_patterns`: a list of patterns to ignore when generating the repository content
* Outputs:
  + A textual representation of the repository structure and content, written to the output file
* Side effects:
  + The output file is created or overwritten

### Example Usage
```python
packer = CodeMix(root_dir=r"C:\Users\huina\Python Projects\Kwork\ClickerProject\ClickerApp", ignore_patterns=ignore_list)
packer.build_repo_content("codemix.txt")
```

## <a name="compressor-component"></a> Compressor Component
The compressor component is responsible for reducing the size of input data using a combination of natural language processing (NLP) models and compression algorithms.

### <a name="responsibility"></a> Responsibility
The compressor component interacts with other parts of the system to:
* Receive input data to be compressed
* Utilize NLP models (e.g., GPTModel, AsyncGPTModel) to process and compress the data
* Return the compressed data

### <a name="key-functions"></a> Key Functions
The compressor component consists of the following key functions:
* `compress(data: str, project_settings: ProjectSettings, model: Model, compress_power) -> str`: Compresses a single piece of data using the provided model and compression power.
* `compress_and_compare(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) -> list`: Compresses and compares a list of data using the provided model and compression power.
* `async_compress(data: str, project_settings: ProjectSettings, model: AsyncModel, compress_power, semaphore, progress_bar: BaseProgress) -> str`: Asynchronously compresses a single piece of data using the provided model and compression power.
* `async_compress_and_compare(data: list, model: AsyncModel, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) -> list`: Asynchronously compresses and compares a list of data using the provided model and compression power.
* `compress_to_one(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, use_async: bool = False, progress_bar: BaseProgress = BaseProgress()) -> str`: Recursively compresses a list of data until only one piece of data remains.

### <a name="logic-flow"></a> Logic Flow
The compressor component's logic flow is as follows:
1. Receive input data to be compressed.
2. Determine the compression power and model to use.
3. Utilize the `compress` or `async_compress` function to compress the data.
4. If comparing multiple pieces of data, utilize the `compress_and_compare` or `async_compress_and_compare` function.
5. If necessary, recursively compress the data using the `compress_to_one` function.

### <a name="important-assumptions"></a> Important Assumptions
The compressor component assumes that:
* The input data is a string or list of strings.
* The provided model is a valid NLP model (e.g., GPTModel, AsyncGPTModel).
* The compression power is a positive integer.
* The progress bar is an instance of the `BaseProgress` class.

## <a name="postprocess_module"></a>
The `postprocess.py` module is responsible for handling various post-processing tasks, including generating markdown anchors, extracting topics and links, and creating introductions and descriptions.

### <a name="generate_markdown_anchor"></a>
The `generate_markdown_anchor` function takes a header string as input and returns a markdown anchor. It normalizes the input string, replaces spaces with hyphens, and removes any non-alphanumeric characters.

### <a name="get_all_topics"></a>
The `get_all_topics` function extracts topics from a given data string. It searches for lines starting with "## " and extracts the topic title. It also generates markdown anchors for each topic.

### <a name="get_all_html_links"></a>
The `get_all_html_links` function extracts HTML links from a given data string. It searches for lines containing "<a name=" and extracts the link text.

### <a name="get_links_intro"></a>
The `get_links_intro` function generates an introduction for a list of links. It creates a prompt for a language model, passing in the list of links and a base introduction text.

### <a name="get_introdaction"></a>
The `get_introdaction` function generates an introduction for a given data string. It creates a prompt for a language model, passing in the data string and a base introduction text.

### <a name="generete_custom_discription"></a>
The `generete_custom_discription` function generates a custom description for a given data string and description prompt. It creates a prompt for a language model, passing in the data string, description prompt, and strict rules for the model to follow.

## <a name="interactions_with_other_modules"></a>
The `postprocess.py` module interacts with other modules, including:

* `settings.py`: Uses the `BASE_SETTINGS_PROMPT` constant.
* `spliter.py`: Uses the `BASE_PART_COMPLITE_TEXT` constant.
* `gpt_model.py`: Uses the `GPTModel` and `Model` classes.

## <a name="key_functions_and_logic_flows"></a>
Key functions and logic flows in this module include:

* Generating markdown anchors and extracting topics and links from a data string.
* Creating prompts for a language model to generate introductions and descriptions.
* Passing in data strings and prompts to a language model to generate text.

## <a name="important_assumptions_and_inputs"></a>
Important assumptions and inputs for this module include:

* The input data strings are well-formatted and contain the necessary information for extracting topics and links.
* The language model is able to generate coherent and accurate text based on the prompts passed in.
* The `BASE_SETTINGS_PROMPT` and `BASE_PART_COMPLITE_TEXT` constants are correctly defined in the `settings.py` and `spliter.py` modules, respectively.

<a name="split_data_function"></a>
## Split Data Function
### Responsibility
The `split_data` function is responsible for splitting a given code mix into smaller parts based on a maximum symbol limit.

### Key Functions and Logic Flows
The function iterates through the `splited_by_files` list and checks if each element exceeds the `max_symbols * 1.5` limit. If it does, the element is split into two parts at the `max_symbols / 2` position, and the second part is inserted into the list at the next index.

After splitting the elements, the function iterates through the `splited_by_files` list again and checks if each element can be added to the existing `split_objects` list without exceeding the `max_symbols * 1.25` limit. If it can, the element is appended to the existing list; otherwise, a new list is created.

### Important Assumptions and Inputs
* `splited_by_files`: a list of code elements to be split
* `max_symbols`: the maximum number of symbols allowed in each split element
* `split_objects`: a list to store the split code elements

### Outputs and Side Effects
* The function returns the `split_objects` list containing the split code elements.
* The `splited_by_files` list is modified in-place during the splitting process.

### Context
This function is part of a larger system that generates documentation for code. The split data is used as input for the `write_docs_by_parts` function, which generates documentation for each split part. The `gen_doc_parts` function coordinates the splitting and documentation generation process.

Here is the specific code snippet with documentation:
```python
def split_data(full_code_mix, max_symbols):
    """
    Split the given code mix into smaller parts based on the maximum symbol limit.

    Args:
        full_code_mix (str): The code mix to be split.
        max_symbols (int): The maximum number of symbols allowed in each split element.

    Returns:
        list: A list of split code elements.
    """
    splited_by_files = [full_code_mix]  # Initialize the list with the full code mix
    split_objects = []  # Initialize an empty list to store the split code elements

    while True:
        have_to_change = False
        for i, el in enumerate(splited_by_files):
            if len(el) > max_symbols * 1.5:
                # Split the element into two parts at the max_symbols / 2 position
                splited_by_files.insert(i+1, el[int(max_symbols / 2):])
                splited_by_files[i] = el[:int(max_symbols / 2)]
                have_to_change = True

        if have_to_change == False:
            break

    curr_index = 0
    for el in splited_by_files:
        if len(split_objects) - 1 < curr_index:
            split_objects.append("")

        if len(split_objects[curr_index]) + len(el) > max_symbols * 1.25:
            # Create a new list if the existing list exceeds the max_symbols * 1.25 limit
            curr_index += 1
            split_objects.append(el)
            continue

        split_objects[curr_index] += "\n" + el

    return split_objects
```

**Documentation – Progress handling (ui.progress_base)**  
<a name="progress-base"></a>

---

### Overview  

`progress_base.py` defines the **progress‑display abstraction** used by the CLI UI of **autodocgenerator**.  
It wraps **Rich**’s `Progress` object, exposing a small, test‑friendly interface that the rest of the application (e.g. the documentation generation workflow) can use to report overall progress and optional sub‑tasks without depending directly on Rich’s API.

---

## Core classes  

| Class | Purpose | Key attributes |
|-------|---------|----------------|
| `BaseProgress` | Abstract contract for a progress reporter. It is never instantiated directly; concrete subclasses implement the three core operations. | – |
| `LibProgress` | Concrete implementation that forwards calls to a `rich.progress.Progress` instance. It maintains a *base* task that represents the whole operation and an optional *current sub‑task* for finer‑grained steps. | `self.progress` – the Rich `Progress` object<br>`self._base_task` – ID of the main task<br>`self._cur_sub_task` – ID of the active sub‑task (or `None`) |

---

## Detailed API  

### `BaseProgress`

```python
class BaseProgress:
    def __init__(self): ...
    def create_new_subtask(self, name: str, total_len: int): ...
    def update_task(self): ...
    def remove_subtask(self): ...
```

* **Responsibility** – Define the minimal public surface required by the rest of the system.  
* **Assumptions** – Sub‑classes will store any state needed to map a *name* → *task id* and will guarantee that `update_task` advances the *currently active* task.

---

### `LibProgress`

#### Constructor  

```python
def __init__(self, progress: Progress, total: int = 4):
```

* **Parameters**  
  * `progress` – a live `rich.progress.Progress` instance (created by the UI entry‑point).  
  * `total` – expected number of steps for the **overall** operation; defaults to 4 (the typical number of high‑level phases in the doc‑generation pipeline).  

* **Behaviour**  
  * Calls `super().__init__()` to satisfy the abstract base.  
  * Registers a *base task* with the title *“General progress”* and stores its internal ID in `_base_task`.  
  * Initializes `_cur_sub_task` to `None`, indicating that no sub‑task is active yet.

#### `create_new_subtask(name, total_len)`

```python
def create_new_subtask(self, name, total_len):
    self._cur_sub_task = self.progress.add_task(name, total=total_len)
```

* **Purpose** – Start a new sub‑task (e.g. *“Parsing source files”*).  
* **Side‑effects** – Registers a new task with Rich and replaces any previously active sub‑task ID.  
* **Assumptions** – The caller supplies a meaningful `total_len` matching the number of incremental updates expected for this phase.

#### `update_task()`

```python
def update_task(self):
    if self._cur_sub_task is None:
        self.progress.update(self._base_task, advance=1)
    else:
        self.progress.update(self._cur_sub_task, advance=1)
```

* **Purpose** – Increment the progress bar by a single unit.  
* **Logic flow** –  
  1. If a sub‑task is active, advance that task.  
  2. Otherwise, advance the *base* task.  
* **Side‑effects** – Triggers Rich to redraw the progress bar; no return value.

#### `remove_subtask()`

```python
def remove_subtask(self):
    if self._cur_sub_task is not None:
        self._cur_sub_task = None
```

* **Purpose** – Signal that the current sub‑task has finished.  
* **Behaviour** – Clears the stored sub‑task ID; the next call to `update_task` will affect the base task again.  
* **Note** – The underlying Rich task remains in the `Progress` container, allowing the UI to keep its visual entry until the overall progress finishes.

---

## Interaction with the rest of the system  

1. **UI entry point** (e.g. `autodocgenerator/ui/main.py`) creates a `Progress` object and passes it to `LibProgress`.  
2. The **documentation generation engine** (parsers, template renderers, API callers) receives the `LibProgress` instance via dependency injection.  
3. At each logical phase it calls:  
   * `create_new_subtask("Phase name", steps)` – when entering a new phase.  
   * Repeatedly `update_task()` – after completing a step.  
   * `remove_subtask()` – when the phase ends.  
4. When the whole process finishes, the UI stops the `Progress` context manager, causing Rich to clean up the terminal display.

Because the engine only relies on the abstract `BaseProgress` methods, alternative implementations (e.g. a no‑op progress reporter for unit tests) can be swapped in without touching the core logic.

---

## Important assumptions & constraints  

| Aspect | Detail |
|--------|--------|
| **Rich version** | The code assumes Rich ≥ 14.0 (as specified in `pyproject.toml`). API signatures used (`add_task`, `update`) are stable across this range. |
| **Task totals** | The caller must ensure that the number of `update_task` calls does not exceed the `total` supplied when creating a task; otherwise Rich will raise an error. |
| **Single active sub‑task** | Only one sub‑task can be active at a time. Nested sub‑tasks are not supported; a new call to `create_new_subtask` overwrites the previous one. |
| **Thread safety** | The class is **not** thread‑safe. All calls are expected to happen in the same thread that owns the Rich `Progress` context. |
| **Side‑effects** | Progress updates directly affect the terminal UI; there is no return value or logging side‑effect. |

---

### Extending / Replacing  

* To add **nested sub‑tasks**, subclass `BaseProgress` and maintain a stack of task IDs.  
* For **headless environments** (e.g., CI pipelines), provide a stub implementation that implements the abstract methods as no‑ops; inject it via the same interface used by the application’s service container.

--- 

*End of documentation for `autodocgenerator/ui/progress_base.py`.*

