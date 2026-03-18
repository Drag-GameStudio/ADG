**Project Title**  
Auto‑Doc Generator

---

### 1. Project Goal  
To automate the creation of comprehensive, Markdown‑style documentation for any codebase.  
Given a repository, the tool asks a Groq LLM to generate natural‑language sections, optionally enriches those sections with vector embeddings, and emits a single, ready‑to‑publish document. It supports custom sections, ordering, and fine‑grained control over the output through a YAML configuration file.

---

### 2. Core Logic & Principles  
| Layer | Responsibility | How It Works |
|-------|-----------------|--------------|
| **CLI / UI** | Entry point (`run_file.py`) and progress display (`ConsoleGitHubProgress`) | Parses arguments, loads the configuration file (`autodocconfig.yml`), and starts a `Manager`. |
| **Configuration** | `Config`, `StructureSettings`, and custom module imports | Defines ignore lists, language, metadata, chunk sizes, and which introductory modules to render. |
| **Manager** | Orchestrates the whole pipeline | 1️⃣ Pre‑processes source code: splits and compresses into ≤ *max_symbols* chunks. 2️⃣ Uses the LLM wrapper (`GPTModel`) to summarise or render each chunk. 3️⃣ Passes the resulting text through a `DocFactory` that creates an ordered list of `BaseModule` subclasses, each rendering a Markdown fragment into a shared `DocSchema`. 4️⃣ Optionally produces embeddings with the Google Gemini API. 5️⃣ Re‑orders and finalises the document before writing `output_doc.md` or returning the string. |
| **Factory** | `DocFactory` | Instantiates `BaseModule` objects (e.g., `IntroText`, `IntroLinks`, user‑supplied modules) and calls their `render()` methods in a defined sequence. |
| **LLM Layer** | `GPTModel` / `AsyncGPTModel` | Thin wrapper around the Groq API that handles key rotation, request batching, and history‑based conversation context. |
| **Post‑processing** | Embedding, semantic re‑ordering, anchor splitting | Stores 768‑dim vectors per doc part and can reorder sections based on semantic similarity. |
| **Schema** | `DocSchema` | A typed in‑memory representation of the document (headers, parts, global sections) that all modules manipulate before final output. |
| **Utilities** | Splitters, compressors, settings helpers | Deterministic text chunking (`split_text_by_anchors`) and iterative LLM compression (`compress_to_one`). |

The architecture follows a **Layered + Factory** pattern: UI → Service (Manager) → Model → Post‑processor, ensuring that every component has a single, well‑defined responsibility and can be swapped independently.

---

### 3. Key Features  

* **CLI and API Entry Points** – run the generator from the command line or import `gen_doc` in Python code.  
* **Configurable Workflow** – `autodocconfig.yml` controls ignore patterns, language, metadata, chunk size, and custom module injection.  
* **Dynamic Sectioning** – `DocFactory` creates any number of markdown sections; users can add new `BaseModule` subclasses for bespoke documentation blocks.  
* **LLM‑Driven Content** – utilizes Groq for natural‑language generation; supports both synchronous and asynchronous operation.  
* **Embedding Layer** – optional vector embeddings via Google Gemini API for semantic indexing or future search features.  
* **Compression and Chunking** – source files are split into manageable chunks, optionally compressed using iterative LLM summarisation.  
* **Progress Reporting** – Rich progress bars (`ConsoleGitHubProgress`) provide real‑time feedback during long runs.  
* **Extensibility** – easy addition of new modules, change of LLM provider, or disabling embeddings without touching the core pipeline.  

---

### 4. Dependencies  

| Category | Package / Tool | Purpose |
|----------|----------------|---------|
| **LLM** | `groq` (Python SDK) | Communicates with Groq APIs. |
| **Embeddings** | `googleai` (or relevant Google Gemini SDK) | Generates 768‑dim vector embeddings. |
| **CLI/Progress** | `rich`, `typer` | Rich console output and progress bars. |
| **Configuration** | `pyyaml` | Reads `autodocconfig.yml`. |
| **Data Structures** | `pydantic` / `typing` | Defines schema types (`DocSchema`, `DocContent`, etc.). |
| **Utilities** | `tqdm`, `textwrap` | Optional progress helpers and text formatting. |
| **Environment** | `dotenv` (optional) | Loads API keys from `.env`. |

> **Environment Variables**  
> * `GROQ_API_KEYS` – comma‑separated list of Groq API keys.  
> * `GOOGLE_EMBEDDING_API_KEY` – key for the Google Gemini embedding endpoint.

> **Python ≥ 3.10** is required for type annotations and pattern matching used in the code.

---

**In short**, Auto‑Doc Generator is a modular, LLM‑powered tool that turns raw source code into a polished, Markdown README‑style document, all driven by a clear, layered architecture and a user‑configurable pipeline.
## Executive Navigation Tree

- 📘 Overview
  * [module-initializer](#module-initializer)
  * [project-context](#project-context)
  * [code-organization](#code-organization)
  * [key-components-and-responsibilities](#key-components-and-responsibilities)
  * [functional-flow](#functional-flow)
  * [technical-logic-flow](#technical-logic-flow)
  * [critical-constraints](#critical-constraints)
  * [next-steps](#next-steps)
  * [CONTENT_DESCRIPTION](#CONTENT_DESCRIPTION)

- ⚙️ Configuration
  * [pyproject](#pyproject)
  * [data-contract](#data-contract)
  * [gpt-model-documentation](#gpt-model-documentation)
  * [async-gpt-model-documentation](#async-gpt-model-documentation)
  * [module-documentation](#module-documentation)
  * [base-module](#base-module)
  * [doc-factory](#doc-factory)
  * [schema-doc_schema](#schema-doc_schema)
  * [autodocconfig-structure-explanation](#autodocconfig-structure-explanation)
  * [custom-module](#custom-module)
  * [custom-module-without-context](#custom-module-without-context)
  * [postprocessor-custom_intro](#postprocessor-custom_intro)
  * [custom-intro-utilities](#custom-intro-utilities)
  * [example-usage](#example-usage)
  * [integration-highlights](#integration-highlights)
  * [intro-links](#intro-links)
  * [intro-text](#intro-text)

- 🧩 Manager
  * [manager-class](#manager-class)
  * [manager-parameters](#manager-parameters)
  * [manager-methods](#manager-methods)
  * [manager-attributes](#manager-attributes)
  * [manager-data-contract](#manager-data-contract)
  * [manager-data-contract-extensions](#manager-data-contract-extensions)
  * [manager-class-methods](#manager-class-methods)

- 🔧 Preprocessor
  * [preprocessor-code-mix-module](#preprocessor-code-mix-module)
  * [preprocessor-code-mix-class](#preprocessor-code-mix-class)
  * [preprocessor-code-mix-should-ignore](#preprocessor-code-mix-should-ignore)
  * [preprocessor-code-mix-build-repo-content](#preprocessor-code-mix-build-repo-content)
  * [preprocessor-code-mix-ignore-list](#preprocessor-code-mix-ignore-list)
  * [preprocessor-code-mix-main](#preprocessor-code-mix-main)
  * [preprocessor-code-mix-data-contract](#preprocessor-code-mix-data-contract)
  * [preprocessor-settings](#preprocessor-settings)

- 📦 Postprocessor
  * [postprocessor-embedding](#postprocessor-embedding)
  * [postprocessor-sorting-module](#postprocessor-sorting-module)
  * [postprocessor-sorting-main](#postprocessor-sorting-main)
  * [postprocessor-sorting-usage](#postprocessor-sorting-usage)
  * [sorting-extract-links-from-start](#sorting-extract-links-from-start)
  * [sorting-split-text-by-anchors](#sorting-split-text-by-anchors)
  * [sorting-get-order](#sorting-get-order)

- 🛠️ Utilities
  * [embedding-helpers](#embedding-helpers)
  * [embedding-class](#embedding-class)
  * [compressor-module](#compressor-module)
  * [compressor-compress](#compressor-compress)
  * [compressor-compress-and-compare](#compressor-compress-and-compare)
  * [compressor-compress-to-one](#compressor-compress-to-one)
  * [spliter-module](#spliter-module)
  * [spliter-split-data](#spliter-split-data)
  * [spliter-write_docs_by_parts](#spliter-write_docs_by_parts)
  * [spliter-gen_doc_parts](#spliter-gen_doc_parts)

- ⚙️ Settings & Logging
  * [settings-projectsettings](#settings-projectsettings)
  * [logging-infrastructure](#logging-infrastructure)
  * [progress-tracking](#progress-tracking)

- 📦 Installation
  * [install-ps1](#install-ps1)
  * [install-bash](#install-bash)
<a name="module-initializer"></a>
## autodocgenerator Module Initializer  

**Functional Role**  
Bootstraps the *Auto‑Doc Generator* library on import. Prints a styled ASCII banner and exposes the central logging singleton (`logger`) for the entire package.

**Visible Interactions**  
- Calls `BaseLogger` from `autodocgenerator.ui.logging`.  
- Invokes `BaseLoggerTemplate` to configure log handlers.  
- No I/O beyond stdout; does not touch the filesystem or external services.

**Logic Flow**  
1. Define `_print_welcome()` – builds colour constants, assembles an ASCII logo, prints banner and version line.  
2. Immediately execute `_print_welcome()` at import time.  
3. Import `BaseLogger`, `BaseLoggerTemplate`, `InfoLog`, `ErrorLog`, `WarningLog`.  
4. Instantiate `logger = BaseLogger()`.  
5. Attach a template via `logger.set_logger(BaseLoggerTemplate())`.  
6. Export `logger` (module‑level singleton) for downstream modules.

**Data Contract**  

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `_print_welcome` | function → `None` | Side‑effect: prints banner | Executes on import; no return. |
| `logger` | `BaseLogger` instance | Central logging hub | Shared across package; configured with `BaseLoggerTemplate`. |
| `BaseLogger`, `BaseLoggerTemplate` | classes (from `ui.logging`) | Provide logging API | Imported but not instantiated beyond `logger`. |
| `InfoLog`, `ErrorLog`, `WarningLog` | classes | Log‑level helpers | Imported for external use; not instantiated here. |

> **Assumption** – The banner display is purely cosmetic; it does not affect documentation generation logic.  

**Usage**  
```python
import autodocgenerator as adg
adg.logger.info("Library loaded")
```  

The module performs no conditional checks; any import will emit the welcome banner and prepare `logger` for immediate use.

###
<a name="project-context"></a>Project Context: Auto Doc Generator

The provided code snippets are part of the **Auto Doc Generator** project, which aims to help developers generate documentation for their projects. The project utilizes a layered architecture, incorporating components such as a config reader, a manager for the documentation generation pipeline, and various modules for customizing the output.

###
<a name="code-organization"></a>Code Organization

The code is organized into several modules and submodules, including:

* `autodocgenerator.auto_runner`: Contains the `config_reader` and `run_file` modules, responsible for reading configuration files and generating documentation, respectively.
* `autodocgenerator.config`: Defines the `Config` and `ProjectBuildConfig` classes, which store project settings and build configurations.
* `autodocgenerator.engine`: Includes the `GPTModel` and `AsyncGPTModel` classes, which interact with the Groq API for language modeling tasks.
* `autodocgenerator.factory`: Contains the `DocFactory` class and various module classes (e.g., `CustomModule`, `IntroLinks`, `IntroText`) that contribute to the documentation generation process.
* `autodocgenerator.postprocessor`: Includes the `Embedding` class, which handles embedding generation for the documentation.
* `autodocgenerator.preprocessor`: Contains modules for preprocessing and splitting code files (not shown in the provided snippets).
* `autodocgenerator.ui`: Defines the `ConsoleGtiHubProgress` class, which displays progress updates during the documentation generation process.

###
<a name="key-components-and-responsibilities"></a>Key Components and Responsibilities

The following components play crucial roles in the Auto Doc Generator project:

* **Config Reader**: Reads configuration files (e.g., `autodocconfig.yml`) and populates the `Config` object with project settings.
* **Manager**: Orchestrates the documentation generation pipeline, utilizing various modules and models to produce the final output.
* **Doc Factory**: Instantiates and coordinates the rendering of custom modules, including intro text and links.
* **GPT Model**: Interacts with the Groq API to generate language model outputs for the documentation.
* **Embedding**: Generates embeddings for the documentation using the Google Gemini API.

###
<a name="functional-flow"></a>Functional Flow

The documentation generation process involves the following steps:

1. **Config Reading**: The `config_reader` module reads the configuration file and populates the `Config` object.
2. **Manager Initialization**: The `Manager` class is instantiated with the `Config` object, project path, and other necessary components (e.g., `GPTModel`, `Embedding`).
3. **Code File Generation**: The `Manager` generates code files based on the project path and configuration settings.
4. **Custom Module Rendering**: The `DocFactory` renders custom modules, including intro text and links, using the `Manager` instance.
5. **Language Model Interaction**: The `GPTModel` interacts with the Groq API to generate language model outputs for the documentation.
6. **Embedding Generation**: The `Embedding` class generates embeddings for the documentation using the Google Gemini API.
7. **Final Output**: The `Manager` saves the generated documentation to a file (e.g., `output_doc.md`).

###
<a name="technical-logic-flow"></a>Technical Logic Flow

The technical logic flow involves the following steps:

1. **Config Loading**: The `config_reader` module loads the configuration file and populates the `Config` object.
2. **Manager Initialization**: The `Manager` class is instantiated with the `Config` object, project path, and other necessary components.
3. **Code File Generation**: The `Manager` generates code files based on the project path and configuration settings.
4. **Custom Module Rendering**: The `DocFactory` renders custom modules, including intro text and links, using the `Manager` instance.
5. **Language Model Interaction**: The `GPTModel` interacts with the Groq API to generate language model outputs for the documentation.
6. **Embedding Generation**: The `Embedding` class generates embeddings for the documentation using the Google Gemini API.
7. **Final Output**: The `Manager` saves the generated documentation to a file.

###
<a name="critical-constraints"></a>Critical Constraints

The following constraints are critical to the Auto Doc Generator project:

* **Layered Architecture**: The project follows a layered architecture, with separate components for configuration, documentation generation, and embedding generation.
* **Modular Design**: The project uses a modular design, with separate modules for custom documentation components, language modeling, and embedding generation.
* **Configurability**: The project allows for configuration settings to be loaded from a file, enabling users to customize the documentation generation process.

###
<a name="next-steps"></a>Next Steps

To further develop the Auto Doc Generator project, the following steps can be taken:

* **Implement Additional Custom Modules**: Develop new custom modules for specific documentation needs, such as code snippets or diagrams.
* **Integrate with Other Tools**: Integrate the Auto Doc Generator with other development tools, such as IDEs or version control systems.
* **Enhance Configurability**: Expand the configuration settings to allow for more customization options, such as output formats or styling.

###
<a name="CONTENT_DESCRIPTION"></a>install-workflow-using-remote-scripts-and-github-secret  

To set up the project you can run a remote installer that pulls the required files straight from the repository’s main branch.  
**PowerShell (Windows)** – execute the command  

```
irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
```

This invokes the PowerShell script that performs all necessary installations and configuration steps.  
**Bash (Linux/Unix)** – run  

```
curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
```

This downloads the shell script and pipes it directly into the shell interpreter.  

Both scripts expect an API key from the Grock service. To supply this key in a GitHub Actions workflow, create a repository secret named **GROCK_API_KEY** and paste the key obtained from the Grock documentation site. The workflow can then reference this secret using `${{ secrets.GROCK_API_KEY }}` so the installer can authenticate with Grock during automated runs.
<a name="pyproject"></a>
## Pyproject.toml – Package Metadata  

### Purpose  
Defines the packaging, dependencies, and build configuration for the `autodocgenerator` project, enabling `poetry` or `pip` to install the library in an isolated environment.

### Data Contract  

| Section | Key | Value | Notes |
|---------|-----|-------|-------|
| `[project]` | `name` | `"autodocgenerator"` | Package identifier. |
| | `version` | `"1.0.3.5"` | Semantic versioning. |
| | `description` | `"This Project helps you to create docs for your projects"` | Short package description. |
| | `authors` | list | Maintainer contact. |
| | `license` | `"MIT"` | License identifier. |
| | `readme` | `"README.md"` | Documentation entry. |
| | `requires-python` | `">=3.11,<4.0"` | Python runtime constraint. |
| | `dependencies` | list | Runtime libraries (e.g., `groq`, `google-genai`, `rich`). |
| `[build-system]` | `requires` | `["poetry-core>=2.0.0"]` | Build backend requirement. |
| | `build-backend` | `"poetry.core.masonry.api"` | Build backend implementation. |

### Key Dependencies  

- **LLM & Embedding**: `groq`, `google-genai`, `openai`.  
- **I/O & Caching**: `CacheControl`, `filelock`, `zstandard`.  
- **Logging & UI**: `rich`, `rich_progress`.  
- **Configuration**: `pyyaml`, `python-dotenv`.  
- **Type Checking**: `pydantic`, `typing_extensions`.  

> **Side effect**: This file is read during packaging and installation; any missing or incompatible dependency will prevent the library from running.  

--- 

These documents provide a concise, accurate view of the installation helper script and package configuration, aligned with the Auto‑Doc Generator architecture.
<a name="data-contract"></a>Data Contract

The following data entities are exchanged between components:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `Config` | Object | Project settings | Stores project name, language, ignore files, and additional information. |
| `ProjectBuildConfig` | Object | Build settings | Stores settings for the build process, such as log level and save logs. |
| `CustomModule` | Object | Custom documentation module | Represents a custom module, such as intro text or links. |
| `GPTModel` | Object | Language model | Interacts with the Groq API for language modeling tasks. |
| `Embedding` | Object | Embedding generator | Generates embeddings for the documentation using the Google Gemini API. |
| `DocFactory` | Object | Documentation factory | Instantiates and coordinates the rendering of custom modules. |

###
<a name="gpt-model-documentation"></a>GPT Model Documentation

#### Overview of GPT Model

The GPT Model is a core component of the Auto Doc Generator project, responsible for generating answers to user prompts using the Groq API. The model is designed to handle multiple APIs and models, allowing for flexibility and fault tolerance.

#### Technical Logic Flow

The technical logic flow of the GPT Model involves the following steps:

1. **Initialization**: The GPT Model is initialized with an API key, history, and a list of models.
2. **Prompt Processing**: The model receives a prompt, which can be either a list of dictionaries or a single string.
3. **History Management**: The model checks if it should use the history or not. If it should, it retrieves the history from the `History` class.
4. **Model Selection**: The model selects a model from the list of available models. If a model fails, it tries the next one.
5. **API Call**: The model makes an API call to the selected model using the Groq API.
6. **Answer Generation**: The model generates an answer based on the API response.
7. **History Update**: The model updates the history with the user's prompt and the generated answer.

#### Data Contract

The following data entities are exchanged between the GPT Model and other components:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `api_key` | str | API key | Used to authenticate with the Groq API |
| `history` | `History` | History | Stores the conversation history |
| `models_list` | list[str] | List of models | List of available models to use |
| `prompt` | list[dict[str, str]] or str | Prompt | User's prompt to generate an answer for |
| `answer` | str | Answer | Generated answer to the user's prompt |

#### Critical Constraints

The following constraints are critical to the GPT Model:

* **Model Availability**: The model must be able to handle multiple models and APIs, allowing for flexibility and fault tolerance.
* **History Management**: The model must be able to manage the conversation history, including adding and retrieving entries.
* **API Call**: The model must be able to make API calls to the selected model using the Groq API.

#### Next Steps

To further develop the GPT Model, the following steps can be taken:

* **Improve Model Selection**: Improve the model selection logic to choose the best model based on the prompt and conversation history.
* **Add More Models**: Add more models to the list of available models, allowing for greater flexibility and fault tolerance.
* **Enhance History Management**: Enhance the history management logic to store and retrieve more context, allowing for better answer generation.

###
<a name="async-gpt-model-documentation"></a>Async GPT Model Documentation

The Async GPT Model is an asynchronous version of the GPT Model, designed to handle asynchronous API calls and improve performance.

#### Technical Logic Flow

The technical logic flow of the Async GPT Model involves the following steps:

1. **Initialization**: The Async GPT Model is initialized with an API key, history, and a list of models.
2. **Prompt Processing**: The model receives a prompt, which can be either a list of dictionaries or a single string.
3. **History Management**: The model checks if it should use the history or not. If it should, it retrieves the history from the `History` class.
4. **Model Selection**: The model selects a model from the list of available models. If a model fails, it tries the next one.
5. **API Call**: The model makes an asynchronous API call to the selected model using the Groq API.
6. **Answer Generation**: The model generates an answer based on the API response.
7. **History Update**: The model updates the history with the user's prompt and the generated answer.

#### Data Contract

The following data entities are exchanged between the Async GPT Model and other components:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `api_key` | str | API key | Used to authenticate with the Groq API |
| `history` | `History` | History | Stores the conversation history |
| `models_list` | list[str] | List of models | List of available models to use |
| `prompt` | list[dict[str, str]] or str | Prompt | User's prompt to generate an answer for |
| `answer` | str | Answer | Generated answer to the user's prompt |

#### Critical Constraints

The following constraints are critical to the Async GPT Model:

* **Model Availability**: The model must be able to handle multiple models and APIs, allowing for flexibility and fault tolerance.
* **History Management**: The model must be able to manage the conversation history, including adding and retrieving entries.
* **API Call**: The model must be able to make asynchronous API calls to the selected model using the Groq API.

#### Next Steps

To further develop the Async GPT Model, the following steps can be taken:

* **Improve Model Selection**: Improve the model selection logic to choose the best model based on the prompt and conversation history.
* **Add More Models**: Add more models to the list of available models, allowing for greater flexibility and fault tolerance.
* **Enhance History Management**: Enhance the history management logic to store and retrieve more context, allowing for better answer generation.

###
<a name="module-documentation"></a>Module Documentation

The module documentation provides an overview of the various modules used in the Auto Doc Generator project.

####
<a name="base-module"></a>Base Module

The `BaseModule` is an abstract base class that defines the interface for all modules.

##### Technical Logic Flow

The technical logic flow of the `BaseModule` involves the following steps:

1. **Initialization**: The `BaseModule` is initialized with no parameters.
2. **Generation**: The `generate` method is called with an `info` dictionary and a `model` object.
3. **Result**: The `generate` method returns a result, which is a string or a dictionary.

##### Data Contract

The following data entities are exchanged between the `BaseModule` and other components:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `info` | dict | Information | Dictionary containing information about the project |
| `model` | Model | Model | Model object used for generation |
| `result` | str or dict | Result | Result of the generation process |

####
<a name="doc-factory"></a>Doc Factory

The `DocFactory` is a class that manages the generation of documentation using multiple modules.

##### Technical Logic Flow

The technical logic flow of the `DocFactory` involves the following steps:

1. **Initialization**: The `DocFactory` is initialized with a list of modules and a boolean flag `with_splited`.
2. **Generation**: The `generate_doc` method is called with an `info` dictionary, a `model` object, and a `progress` object.
3. **Result**: The `generate_doc` method returns a `DocHeadSchema` object.

##### Data Contract

The following data entities are exchanged between the `DocFactory` and other components:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `info` | dict | Information | Dictionary containing information about the project |
| `model` | Model | Model | Model object used for generation |
| `progress` | BaseProgress | Progress | Progress object used to track the generation process |
| `result` | DocHeadSchema | Result | Result of the generation process |

####
<a name="schema-doc_schema"></a>
## `DocContent`, `DocHeadSchema`, `DocInfoSchema` – In‑Memory Document Model

**Purpose**  
Represent generated documentation as structured data, enabling embedding association, ordering, and merging.

| Class | Role | Key Methods |
|-------|------|-------------|
| `DocContent` | Leaf node | `init_embedding(Embedding)` |
| `DocHeadSchema` | Container of parts | `add_parts(name, DocContent)`, `get_full_doc()`, `__add__` |
| `DocInfoSchema` | Root schema | Holds `global_info`, `code_mix`, and `doc` |

**DocContent**

- `content: str` – Raw markdown snippet.  
- `embedding_vector: Any | None` – Optional vector produced by `Embedding.get_vector`.  
- `init_embedding` – Stores the vector for future similarity searches.

**DocHeadSchema**

- Maintains `content_orders` (preserved order) and `parts` (name → `DocContent`).  
- `add_parts` ensures unique names by suffixing incremented integers.  
- `get_full_doc` concatenates parts in order using a specified separator.  
- `__add__` merges another `DocHeadSchema`, appending its ordered parts.

**DocInfoSchema**

- Holds a consolidated view: project metadata, the raw code mix, and the final `DocHeadSchema`.

**Usage Context**

- The `Manager` builds a `DocInfoSchema` during pipeline execution.  
- After LLM generation, each part is wrapped in a `DocContent`, added to `DocHeadSchema`, and optionally embedded.

---

> **Note**: All classes reside under `autodocgenerator.schema.doc_schema`.  
> No external validation beyond Pydantic’s `BaseModel` is performed; the code relies on the correctness of upstream utilities (`Embedding`, `Model`, `ProjectSettings`).
<a name="autodocconfig-structure-explanation"></a>  
The document is organized into several top‑level fields that control different aspects of the generator:

- **project-name** – short text identifying the project.
- **language** – language code used for the generated documentation.
- **ignore-files** – list of glob patterns telling the tool which files or directories to exclude. Typical entries include build outputs, caches, virtual environments, IDE settings, binary data, and log directories.  
- **build-settings** – controls runtime behaviour:
  - **save-logs** – flag to keep the internal logs of the generation process.
  - **log-level** – numeric level controlling verbosity of output.
- **structure-settings** – dictates how the final document is assembled:
  - **include-intro-links** – whether a link to the introductory section is added.
  - **include-intro-text** – whether the introductory text itself is inserted.
  - **include-order** – whether a section order is generated.
  - **use-global-file** – whether a single global file is used for all content.
  - **max-doc-part-size** – maximum size in characters for each generated document fragment.
- **project-additional-info** – free‑text field for a high‑level description or tagline of the project.
- **custom-descriptions** – a sequence of strings that can be used to override or supplement the autogenerated text. These may reference installation scripts and instructions for using the manager class or configuring the generator.

Each of these sections is optional, but the generator expects the keys in the shown form to correctly parse the settings. Adjust the patterns in **ignore-files** and the booleans in **structure-settings** to tailor the output to the repository’s layout and documentation style.
<a name="custom-module"></a>Custom Module

The `CustomModule` is a class that generates custom documentation based on a description.

##### Technical Logic Flow

The technical logic flow of the `CustomModule` involves the following steps:

1. **Initialization**: The `CustomModule` is initialized with a description.
2. **Generation**: The `generate` method is called with an `info` dictionary and a `model` object.
3. **Result**: The `generate` method returns a result, which is a string.

##### Data Contract

The following data entities are exchanged between the `CustomModule` and other components:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `info` | dict | Information | Dictionary containing information about the project |
| `model` | Model | Model | Model object used for generation |
| `result` | str | Result | Result of the generation process |

####
<a name="custom-module-without-context"></a>Custom Module Without Context

The `CustomModuleWithOutContext` is a class that generates custom documentation without context.

##### Technical Logic Flow

The technical logic flow of the `CustomModuleWithOutContext` involves the following steps:

1. **Initialization**: The `CustomModuleWithOutContext` is initialized with a description.
2. **Generation**: The `generate` method is called with an `info` dictionary and a `model` object.
3. **Result**: The `generate` method returns a result, which is a string.

##### Data Contract

The following data entities are exchanged between the `CustomModuleWithOutContext` and other components:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `info` | dict | Information | Dictionary containing information about the project |
| `model` | Model | Model | Model object used for generation |
| `result` | str | Result | Result of the generation process |

####
<a name="postprocessor-custom_intro"></a>  
## `autodocgenerator/postprocessor/custom_intro.py`

**Purpose**  
Collects and enriches introductory documentation fragments.  
The module contains helper functions that

* extract anchor links from a markdown string,
* generate an introduction section via an LLM,
* produce link lists for a navigation header,
* create custom descriptions for arbitrary code snippets.

All interactions with the LLM are performed through the `Model` interface passed to each helper.

---
<a name="custom-intro-utilities"></a>### Core Functions

| Function | Inputs | Outputs | Notes |
| -------- | ------ | ------- | ----- |
| `get_all_html_links(data: str) -> list[str]` | `data`: markdown document | `links`: list of `#anchor` strings | Uses regex `<a name="…">` to capture anchors longer than five characters. Logs extraction steps via `BaseLogger`. |
| `get_links_intro(links: list[str], model: Model, language: str = "en") -> str` | `links`: list of anchor strings, `model`: LLM wrapper, `language`: optional | `intro_links`: generated markdown section | Builds a 3‑message prompt, sends it to `model.get_answer_without_history`. Logs before/after. |
| `get_introdaction(global_data: str, model: Model, language: str = "en") -> str` | `global_data`: project‑wide summary, `model`, `language` | `intro`: introductory markdown | Prompt contains `BASE_INTRO_CREATE` template. |
| `generete_custom_discription(splited_data: str, model: Model, custom_description: str, language: str = "en") -> str` | `splited_data`: iterable of code or text chunks, `model`, `custom_description`, `language` | `result`: description or empty string | Iterates over chunks; stops when result contains “!noinfo” or “No information found” is absent. |
| `generete_custom_discription_without(model: Model, custom_description: str, language: str = "en") -> str` | `model`, `custom_description`, `language` | `result`: tagged description | Enforces a strict tag format at the beginning of the LLM response. |

#### Internal Prompt Flow

```
system → "use language X"
system → specific instruction template
user   → data or task text
```

The LLM response is returned directly; no post‑processing occurs in this module.

---
<a name="example-usage"></a>Example Usage

```python
from autodocgenerator.manage import Manager
from autodocgenerator.config import Config
from autodocgenerator.engine.models import Model
from autodocgenerator.postprocessor.embedding import Embedding
from autodocgenerator.ui.progress_base import BaseProgress

# Create a configuration object
config = Config()

# Create an LLM model
llm_model = Model()

# Create an embedding model
embedding_model = Embedding()

# Create a progress bar
progress_bar = BaseProgress()

# Create a manager object
manager = Manager(project_directory="path/to/project", config=config, llm_model=llm_model, embedding_model=embedding_model, progress_bar=progress_bar)

# Generate the code mix file
manager.generate_code_file()

# Generate the global information file
manager.generate_global_info()

# Generate the documentation parts
manager.generete_doc_parts()

# Generate the documentation using the factory
manager.factory_generate_doc(DocFactory())

# Create the embedding layer
manager.create_embedding_layer()

# Order the documentation
manager.order_doc()

# Save the documentation
manager.save()
```

### <a name="notes"></a>Notes

* The `Manager` class is responsible for orchestrating the entire documentation generation process.
* The `Manager` class takes in several parameters, including the project directory, configuration, LLM model, embedding model, and progress bar.
* The `Manager` class has several methods that are used to perform different tasks, such as generating the code mix file, global information file, documentation parts, and documentation using the factory.
* The `Manager` class has several attributes that are used to store information, such as the documentation information, configuration, project directory, progress bar, LLM model, and embedding model.
* The `Manager` class exchanges several data entities with other components, such as the code mix, global information, documentation parts, factory documentation, and embedding.
<a name="integration-highlights"></a>  
## Interaction Flow in the Pipeline

1. **Anchor Extraction** – `manager.generete_doc_parts()` produces `doc_parts`; `get_all_html_links` pulls anchors → feeds to `get_links_intro`.
2. **Introduction Generation** – `global_info` is supplied to `get_introdaction`; custom sections are rendered via `generete_custom_discription`.
3. **Vector Embedding** – `manager.create_embedding_layer()` creates an `Embedding` instance; `get_vector` is called per doc chunk to build semantic indices.
4. **Sorting** – `sort_vectors` is used downstream in post‑processing to order sections by similarity to a root vector.

All LLM prompts are built from constants in `engine.config.config` and executed through the `Model` interface, ensuring a single point for API interaction. Logging is performed through `BaseLogger` for traceability.
<a name="intro-links"></a>Intro Links

The `IntroLinks` is a class that generates introduction links.

##### Technical Logic Flow

The technical logic flow of the `IntroLinks` involves the following steps:

1. **Generation**: The `generate` method is called with an `info` dictionary and a `model` object.
2. **Result**: The `generate` method returns a result, which is a string.

##### Data Contract

The following data entities are exchanged between the `IntroLinks` and other components:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `info` | dict | Information | Dictionary containing information about the project |
| `model` | Model | Model | Model object used for generation |
| `result` | str | Result | Result of the generation process |

####
<a name="intro-text"></a>Intro Text

The `IntroText` is a class that generates introduction text.

##### Technical Logic Flow

The technical logic flow of the `IntroText` involves the following steps:

1. **Generation**: The `generate` method is called with an `info` dictionary and a `model` object.
2. **Result**: The `generate` method returns a result, which is a string.

##### Data Contract

The following data entities are exchanged between the `IntroText` and other components:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `info` | dict | Information | Dictionary containing information about the project |
| `model` | Model | Model | Model object used for generation |
| `result` | str | Result | Result of the generation process |

###
<a name="manager-class"></a>Manager Class

The `Manager` class is responsible for orchestrating the entire documentation generation process. It takes in several parameters, including the project directory, configuration, LLM model, embedding model, and progress bar.

####
<a name="manager-parameters"></a>Manager Parameters

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `project_directory` | str | Project directory | The directory where the project is located |
| `config` | Config | Configuration | The configuration object containing project settings |
| `llm_model` | Model | LLM model | The LLM model used for generation |
| `embedding_model` | Embedding | Embedding model | The embedding model used for generating embeddings |
| `progress_bar` | BaseProgress | Progress bar | The progress bar used to track the generation process |

####
<a name="manager-methods"></a>Manager Methods

The `Manager` class has several methods that are used to perform different tasks:

1. **`generate_code_file`**: Generates the code mix file.
2. **`generate_global_info`**: Generates the global information file.
3. **`generete_doc_parts`**: Generates the documentation parts.
4. **`factory_generate_doc`**: Generates the documentation using the factory.
5. **`create_embedding_layer`**: Creates the embedding layer.
6. **`order_doc`**: Orders the documentation.
7. **`clear_cache`**: Clears the cache.
8. **`save`**: Saves the documentation.

####
<a name="manager-attributes"></a>Manager Attributes

The `Manager` class has several attributes that are used to store information:

1. **`doc_info`**: Stores the documentation information.
2. **`config`**: Stores the configuration.
3. **`project_directory`**: Stores the project directory.
4. **`progress_bar`**: Stores the progress bar.
5. **`llm_model`**: Stores the LLM model.
6. **`embedding_model`**: Stores the embedding model.
7. **`logger`**: Stores the logger.

####
<a name="manager-data-contract"></a>Manager Data Contract

The following data entities are exchanged between the `Manager` and other components:

| Entity | Type | Role | Notes |
| --- | --- | --- | --- |
| `code_mix` | str | Code mix | The code mix generated by the `CodeMix` class |
| `global_info` | str | Global information | The global information generated by the `compress_to_one` function |
| `doc_parts` | str | Documentation parts | The documentation parts generated by the `gen_doc_parts` function |
| `factory_doc` | str | Factory documentation | The documentation generated by the factory |
| `embedding` | Embedding | Embedding | The embedding generated by the `Embedding` class |

###
<a name="manager-data-contract-extensions"></a>  
### Manager Data Contract – Relevance to Custom Intro & Embedding

The `Manager` orchestration layer passes the following entities to the functions described above:

| Entity | Type | Role | Notes |
| ------ | ---- | ---- | ----- |
| `code_mix` | `str` | Source mix | Handed to `generete_custom_discription` for content extraction. |
| `global_info` | `str` | Project overview | Used with `get_introdaction`. |
| `doc_parts` | `str` | Chunked docs | Input for `get_all_html_links` and `get_links_intro`. |
| `factory_doc` | `str` | Rendered intro blocks | May contain anchor tags extracted by `get_all_html_links`. |
| `embedding` | `Embedding` | Vector provider | Created by Manager for `sort_vectors` usage. |

> **Warning**  
> The `generete_custom_discription` function assumes that `splited_data` is iterable over chunk strings; passing a single string will iterate character‑by‑character, causing erroneous prompts. Ensure `splited_data` is a list of meaningful code or documentation fragments.

---
<a name="manager-class-methods"></a>  
The **Manager** class is the central orchestrator for generating documentation.  
Its constructor requires a project root path and a set of dependencies – a language‑model instance (`llm_model`), an embedding model (`embedding_model`), a progress bar object, and a `Config` instance that holds ignore patterns, language, project name, and additional metadata.

```python
# Example: basic Manager instantiation and workflow
from autodocgenerator.manage import Manager
from autodocgenerator.engine.models.gpt_model import GPTModel
from autodocgenerator.postprocessor.embedding import Embedding
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress

# create required sub‑systems
llm = GPTModel(GROQ_API_KEYS, use_random=False)
embedder = Embedding(GOOGLE_EMBEDDING_API_KEY)

# project path and configuration supplied elsewhere
project_path = "./myproject"
config = ...          # Config instance produced by read_config

manager = Manager(
    project_path,
    config=config,
    llm_model=llm,
    embedding_model=embedder,
    progress_bar=ConsoleGtiHubProgress()
)
```

After the object is created, the following public methods can be called in the order shown below (the order is dictated by the typical documentation‑generation pipeline):

| Method | Purpose | Key parameters |
|--------|---------|----------------|
| `generate_code_file()` | Walks the project, collects source files, and builds an internal representation of the code structure. | None |
| `generate_global_info(compress_power=4)` | Aggregates global project information (e.g., README, package metadata) and optionally compresses the data using the supplied power. | `compress_power` – integer compression factor |
| `generete_doc_parts(max_symbols, with_global_file)` | Splits large documents into parts not exceeding `max_symbols`. If `with_global_file` is true, global information is included. | `max_symbols` – int, `with_global_file` – bool |
| `factory_generate_doc(factory, to_start=False, with_splited=False)` | Uses a `DocFactory` instance to produce documentation sections from custom or built‑in modules. The `to_start` flag indicates whether the generated content should be prepended to the document. `with_splited` controls whether content should be split. | `factory` – `DocFactory` instance, `to_start` – bool, `with_splited` – bool |
| `order_doc()` | Reorders the document sections according to a predefined or custom sequence. | None |
| `create_embedding_layer()` | Builds an embedding representation for the entire document, useful for semantic search or summarization. | None |
| `clear_cache()` | Removes temporary files and caches created during processing. | None |
| `save()` | Persists the generated documentation to disk (e.g., writes a markdown file). | None |

Once all transformations are complete, the full rendered document is accessible via:

```python
full_text = manager.doc_info.doc.get_full_doc()
```

**Typical usage pattern (as shown in `run_file.py`):**

```python
manager.generate_code_file()
if structure_settings.use_global_file:
    manager.generate_global_info(compress_power=4)

manager.generete_doc_parts(
    max_symbols=structure_settings.max_doc_part_size,
    with_global_file=structure_settings.use_global_file
)

manager.factory_generate_doc(DocFactory(*custom_modules))

if structure_settings.include_order:
    manager.order_doc()

# Add introductory sections if requested
extra_modules = []
if structure_settings.include_intro_text:
    extra_modules.append(IntroText())
if structure_settings.include_intro_links:
    extra_modules.append(IntroLinks())

manager.factory_generate_doc(
    DocFactory(*extra_modules, with_splited=False),
    to_start=True
)

manager.create_embedding_layer()
manager.clear_cache()
manager.save()

# retrieve the final document
document = manager.doc_info.doc.get_full_doc()
```

This workflow shows how the `Manager` interacts with custom modules, global file handling, ordering, and post‑processing steps to produce the final documentation output.
<a name="preprocessor-code-mix-module"></a>## Pre‑processor: CodeMix

**Purpose** – `CodeMix` compiles a repository’s file tree and content into a single markdown string suitable for LLM ingestion.

---
<a name="preprocessor-code-mix-class"></a>### `CodeMix` Class

| Attribute | Type | Role | Notes |
|-----------|------|------|-------|
| `root_dir` | `Path` | Base directory | Resolved absolute path. |
| `ignore_patterns` | `list[str]` | Wildcards to skip | Default empty; can be overridden. |
| `logger` | `BaseLogger` | Logging instance | Reports ignored paths. |

#### Methods

| Method | Parameters | Returns | Notes |
|--------|------------|---------|-------|
| `__init__(self, root_dir=".", ignore_patterns=None)` | `root_dir`, `ignore_patterns` | – | Stores state; creates a `BaseLogger`. |
| `should_ignore(self, path: str) -> bool` | `path` | `bool` | Determines if a file/dir matches any ignore pattern. |
| `build_repo_content(self) -> str` | – | `str` | Concatenates a tree view and file contents. |

---
<a name="preprocessor-code-mix-should-ignore"></a>#### `should_ignore`

*Logic*

1. Compute `relative_path` from `root_dir`.  
2. For each `pattern` in `ignore_patterns` check:
   - `fnmatch` against the full relative string,
   - against the file/directory name,
   - against any part of the path.
3. Return `True` on first match.

---
<a name="preprocessor-code-mix-build-repo-content"></a>#### `build_repo_content`

*Logic Flow*

1. Start with `"Repository Structure:"`.  
2. Recursively walk `root_dir` sorted by name.  
3. For each item that is **not** ignored, append an indented name (`/` for directories).  
4. Append a separator of 20 `"="`.  
5. Second traversal: for every file (non‑ignored), append a `<file path="...">` tag, the file’s UTF‑8 content, and a newline.  
6. If file reading fails, capture the exception string.  
7. Join all lines with `"\n"` and return.

> **Side Effect** – The method logs every ignored path at level 1.

---
<a name="preprocessor-code-mix-ignore-list"></a>### `ignore_list`

A module‑level list of glob patterns and directory names to exclude, such as `*.pyc`, `__pycache__`, `.git`, `venv`, etc. It is passed to `CodeMix` when instantiated.

---
<a name="preprocessor-code-mix-main"></a>### `__main__` Demo

Instantiates `CodeMix` on a hard‑coded project directory and prints the confirmation message `"Файл успешно создан!"`. (The message is in Russian and indicates success.)

---
<a name="preprocessor-code-mix-data-contract"></a>## Data Contract – CodeMix ↔ Manager

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `repo_content` | `str` | Repository dump | Returned by `build_repo_content`. |
| `ignore_patterns` | `list[str]` | Exclusion rules | Influences traversal and logging. |
| `root_dir` | `Path` | Repository root | Determines relative paths. |

> The Manager consumes `repo_content` as the initial source mix for downstream compression and LLM prompting. No direct interaction with `ignore_list`; it is purely configuration.

---
<a name="preprocessor-settings"></a>
## settings.py – Project Prompt Builder
<a name="postprocessor-embedding"></a>  
## `autodocgenerator/postprocessor/embedding.py`

**Purpose**  
Provide vector embeddings for document parts using Google Gemini, and utility helpers to sort by semantic distance.

---
<a name="postprocessor-sorting-module"></a>## Post‑processor: Sorting Logic

**Purpose** – The *sorting* module is responsible for extracting anchor links from a markdown document, dividing the text into named chunks, and re‑ordering those chunks using an LLM.

---
<a name="postprocessor-sorting-main"></a>### `__main__` Demo

The script can be executed standalone, opening a local README and printing the anchor mapping produced by `split_text_by_anchors`.

---
<a name="postprocessor-sorting-usage"></a>## Integration Highlights

* `extract_links_from_start` feeds `split_text_by_anchors`, which yields a dictionary of anchored sections for the post‑processor.  
* `get_order` receives a `Model` instance from the Manager, re‑orders the extracted anchor titles, and the result is used for semantic re‑arrangement in later stages.  
* `CodeMix.build_repo_content` supplies the `Manager` with a single string of repository structure and file bodies, which becomes `code_mix` passed to `generete_custom_discription`.

---

**Key Dependencies**

- `engine.models.model.Model` – LLM interface for ordering.  
- `ui.logging.BaseLogger` – Unified logging for both modules.  
- `re`, `fnmatch`, `pathlib`, `os` – Standard library utilities.

All logic is strictly derived from the provided snippets; no external assumptions have been made.
<a name="sorting-extract-links-from-start"></a>### `extract_links_from_start(chunks)`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `chunks` | `list[str]` | Chunk collection | Input list of markdown sections. |
| `links` | `list[str]` | Anchor URLs | Captured from leading `<a name…>` tags. |
| `have_to_del_first` | `bool` | Indicates if the first chunk is a placeholder | Set true when no anchor is found at start of a chunk. |

**Logic Flow**

1. Iterate over each `chunk`.  
2. Strip whitespace and apply regex `^<a name=["']?(.*?)["']?</a>` to find a leading anchor.  
3. If an anchor name longer than 5 chars is found, append `#anchor` to `links`.  
4. If no anchor is found for a chunk, flag `have_to_del_first` to true.  
5. Return `(links, have_to_del_first)`.

> **Warning** – The function assumes that anchors, if present, are strictly at the beginning of the chunk. Any leading markdown or whitespace may cause a false negative.

---
<a name="sorting-split-text-by-anchors"></a>### `split_text_by_anchors(text: str)`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `text` | `str` | Full markdown document | Input to split. |
| `chunks` | `list[str]` | Preliminary split by anchor boundaries | Uses look‑ahead regex. |
| `result_chanks` | `list[str]` | Stripped, non‑empty chunks | Result of split. |
| `all_links` | `list[str]` | Anchor URLs extracted | From `extract_links_from_start`. |
| `result` | `dict[str, str]` | Mapping of anchor → chunk | Returned value. |

**Logic Flow**

1. Split `text` on the pattern that precedes an anchor (`(?=<a name…>)`).  
2. Strip each fragment, discard empty ones.  
3. Retrieve links and flag via `extract_links_from_start`.  
4. If the first anchor occurs far into the file (`start_link_index > 10`) or the flag is set, remove the first chunk (assumed placeholder).  
5. Verify that the number of links matches the number of chunks; otherwise raise `Exception`.  
6. Build a dictionary mapping each link to its corresponding chunk.  
7. Return the mapping.

> **Critical** – The function throws an exception if the anchor count diverges from the chunk count, guarding against malformed documents.

---
<a name="sorting-get-order"></a>### `get_order(model: Model, chanks: list[str]) -> list`

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `model` | `Model` | LLM wrapper | Imported from `engine.models.model`. |
| `chanks` | `list[str]` | Anchor titles | Titles to be ordered. |
| `result` | `str` | LLM response | Raw comma‑separated titles. |
| `new_result` | `list[str]` | Ordered list | Stripped titles. |

**Logic Flow**

1. Log “Start ordering” using `BaseLogger`.  
2. Build a user prompt that requests a semantic ordering of the titles.  
3. Call `model.get_answer_without_history(prompt)`.  
4. Split the response on commas, strip whitespace, and log the final list.  
5. Return the ordered list.

> **Warning** – The prompt string is hard‑coded; any changes to the LLM template require editing this file.

---
<a name="embedding-helpers"></a>### Utility Functions

| Function | Inputs | Outputs | Notes |
| -------- | ------ | ------- | ----- |
| `bubble_sort_by_dist(arr: list) -> list` | `arr`: list of tuples `(key, distance)` | Sorted list by ascending distance | Implements an O(n²) bubble sort, used only for small result sets. |
| `get_len_btw_vectors(vector1, vector2) -> float` | Two NumPy arrays | Euclidean distance | Calls `np.linalg.norm(vector1, vector2)`. |
| `sort_vectors(root_vector, other: dict[str, Any]) -> list[str]` | `root_vector`: reference vector, `other`: mapping `id → vector` | List of keys sorted by proximity to `root_vector` | Builds a distance list, bubble sorts it, and extracts keys. |

---
<a name="embedding-class"></a>### `Embedding` Class

| Attribute | Type | Role | Notes |
| --------- | ---- | ---- | ----- |
| `client` | `genai.Client` | Google GenAI client | Initialized with an API key. |

#### Methods

| Method | Parameters | Returns | Notes |
| ------ | ---------- | ------- | ----- |
| `__init__(api_key: str)` | `api_key`: Gemini API key | – | Stores client instance. |
| `get_vector(prompt: str)` | `prompt`: text to embed | `np.ndarray` of shape `(768,)` | Calls `self.client.models.embed_content` with model `gemini-embedding-2-preview`. Raises if embeddings are missing. |

**Usage Pattern**

```python
embed = Embedding(api_key="YOUR_KEY")
vec = embed.get_vector("sample document text")
```

---
<a name="compressor-module"></a>
## compressor.py – Text Compression Pipeline
<a name="compressor-compress"></a>
### `compress(data: str, project_settings: ProjectSettings, model: Model, compress_power) -> str`

*Purpose* – Off‑load a single large text chunk to the LLM, requesting a compressed summary of the specified *power*.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Raw source chunk | Input to the LLM |
| `project_settings` | `ProjectSettings` | System‑level prompt builder | Supplies `project_settings.prompt` |
| `model` | `Model` | LLM client | Must expose `get_answer_without_history` |
| `compress_power` | `int` | Compression factor | Influences the base prompt length |

**Logic**

1. Build a three‑step prompt list: system instruction from `project_settings.prompt`, a base compression hint `get_BASE_COMPRESS_TEXT(len(data), compress_power)`, then the raw `data` as user content.
2. Call `model.get_answer_without_history(prompt=prompt)` – no history retained for this operation.
3. Return the LLM answer as a string.
<a name="compressor-compress-and-compare"></a>
### `compress_and_compare(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress()) -> list`

*Purpose* – Batch‑compress a list of text fragments, concatenating every *compress_power* items into one compressed block while tracking progress.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | Collection of fragments | Each element is compressed independently |
| `model` | `Model` | LLM client | Same as in `compress` |
| `project_settings` | `ProjectSettings` | Prompt source | |
| `compress_power` | `int` | Chunk grouping size | Defaults to 4 |
| `progress_bar` | `BaseProgress` | UI progress helper | Instantiated with default if not supplied |

**Logic**

1. Pre‑allocate `compress_and_compare_data` with a size equal to `ceil(len(data)/compress_power)`.
2. Create a sub‑task in `progress_bar` titled “Compare all files”.
3. For each element `el` in `data`:
   * Determine its destination index `curr_index = i // compress_power`.
   * Append the compressed result of `el` plus a newline to the corresponding slot.
   * Update progress.
4. Remove the sub‑task after iteration and return the list of compressed blocks.
<a name="compressor-compress-to-one"></a>
### `compress_to_one(data: list, model: Model, project_settings: ProjectSettings, compress_power: int = 4, progress_bar: BaseProgress = BaseProgress())`

*Purpose* – Iteratively reduce a list of fragments into a single string by repeatedly applying `compress_and_compare`.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `list[str]` | Initial fragments | Will be mutated each iteration |
| `model` | `Model` | LLM client | |
| `project_settings` | `ProjectSettings` | Prompt source | |
| `compress_power` | `int` | Base grouping factor | If remaining items < `compress_power+1`, the power is lowered to 2 |
| `progress_bar` | `BaseProgress` | Progress indicator | |

**Logic**

1. Loop while `len(data) > 1`:
   * If the current list length is less than `compress_power+1`, set `new_compress_power=2` to force final merge.
   * Call `compress_and_compare` with the current `data` and `new_compress_power`.
   * Replace `data` with the returned list.
2. Return the lone string once only one item remains.

---
<a name="spliter-module"></a>
## spliter.py – Text Partitioning
<a name="spliter-split-data"></a>
## `split_data` – Text Partitioning

**Purpose**  
Break a single source string into a list of smaller chunks that respect an upper symbol limit.  
The algorithm first trims overly long fragments by repeatedly halving any piece that exceeds `max_symbols * 1.5`.  
After that, it greedily packs fragments into *split_objects* ensuring each does not grow beyond `max_symbols * 1.25`.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `data` | `str` | Raw source code | The text that will be partitioned |
| `max_symbols` | `int` | Size threshold | Maximum allowed length for a chunk |
| `split_objects` | `list[str]` | Resulting chunks | Returned to the caller |
| `logger` | `BaseLogger` | Diagnostics | Emits split progress |

**Step‑by‑Step Flow**

1. **Initial split** – `splited_by_files = data.split("\n")`.  
2. **Recursive halving** – While any fragment exceeds 150 % of `max_symbols`, it is split in half and re‑inserted.  
3. **Packing** – Fragments are appended to the current chunk until adding one would exceed 125 % of `max_symbols`; a new chunk is started.  
4. **Logging** – Reports the number of parts produced.

**Critical Assumptions**

> The algorithm assumes line‑based splitting is a suitable approximation for logical code boundaries.  
> No external token counting is performed; length is measured in raw characters.
<a name="spliter-write_docs_by_parts"></a>
## `write_docs_by_parts` – LLM Chunk Documentation

**Purpose**  
Send a single code fragment (`part`) to the LLM and receive its markdown documentation, optionally attaching contextual information from preceding or global sections.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `part` | `str` | Chunk to document | The text produced by `split_data` |
| `model` | `Model` | LLM client | Uses `get_answer_without_history` |
| `project_settings` | `ProjectSettings` | Prompt base | Supplies `prompt` property |
| `prev_info` | `str | None` | Tail of previous docs | Sent as a system instruction |
| `language` | `str` | Localization | Prepends language instruction |
| `global_info` | `str | None` | Project‑wide context | Added as an extra system message |
| `logger` | `BaseLogger` | Logging | Records start/end and output length |

**Logic**

1. Assemble a system prompt hierarchy:
   * Language directive.
   * Project meta‑information (`project_settings.prompt`).
   * Base template `BASE_PART_COMPLITE_TEXT`.
   * Optional global relations or prior documentation snippet.
2. Append the user message containing the code `part`.  
3. Call `model.get_answer_without_history`.  
4. Strip leading and trailing Markdown fences (` ``` `) if present.  
5. Return the cleaned answer string.

**Warning**

> The function *mutates* `answer` only when fence delimiters are detected.  
> If the LLM returns a string without fences, it is returned unchanged.
<a name="spliter-gen_doc_parts"></a>
## `gen_doc_parts` – Full‑Project Documentation Assembly

**Purpose**  
Coordinate splitting and LLM generation for an entire source mix, producing a contiguous markdown document.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `full_code_mix` | `str` | Aggregated source | Input from pre‑processor |
| `max_symbols` | `int` | Chunk size | Passed to `split_data` |
| `model` | `Model` | LLM client | Shared with `write_docs_by_parts` |
| `project_settings` | `ProjectSettings` | Prompt source | Provides context |
| `language` | `str` | Localization | e.g., `"en"` |
| `progress_bar` | `BaseProgress` | UI helper | Optional; defaults to empty instance |
| `global_info` | `str | None` | Project relations | Passed to each part request |
| `logger` | `BaseLogger` | Diagnostics | Reports progress and total length |

**Flow**

1. **Split** `full_code_mix` via `split_data`.  
2. **Sub‑task creation** – `progress_bar.create_new_subtask`.  
3. **Iterative generation** – For each `el` in `splitted_data`:
   * Call `write_docs_by_parts(el, ...)`.  
   * Append result to `all_result`, separated by two newlines.  
   * Truncate `result` to the last 3000 characters to preserve context for the next part.  
   * Update progress bar.  
4. **Cleanup** – Remove sub‑task.  
5. **Return** the concatenated markdown string `all_result`.

**Side Effects**

- Emits detailed `InfoLog` entries (lengths, per‑part content at level 2).  
- Progress bar state changes do not affect the content.
<a name="settings-projectsettings"></a>
### `ProjectSettings(project_name: str)`

*Purpose* – Assemble a dynamic system prompt incorporating project metadata.

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_name` | `str` | Identifier for the target repo | Passed at construction |
| `info` | `dict` | Arbitrary key/value pairs | Added via `add_info` |

**Methods**

- `add_info(key, value)` – Stores a new metadata entry.
- `prompt` (property) – Generates a full prompt string by concatenating `BASE_SETTINGS_PROMPT`, the project name line, and every key/value pair from `info`. Each entry ends with a newline.

---
<a name="logging-infrastructure"></a>
## Logging Infrastructure – `BaseLogger` & Templates  

### Purpose
Provide a lightweight, level‑aware logging façade that can be swapped between console and file output without affecting downstream code.

#### Component Overview

| Class | Responsibility | Key Methods |
|-------|-----------------|-------------|
| `BaseLog` | Base log message holder | `format()` – string representation |
| `ErrorLog / WarningLog / InfoLog` | Sub‑class with severity prefix | `format()` overrides |
| `BaseLoggerTemplate` | Strategy for output (console / file) | `log()`, `global_log()` |
| `FileLoggerTemplate` | Appends logs to a file | `log()` |
| `BaseLogger` | Singleton façade for the rest of the system | `set_logger()`, `log()` |

#### Interaction Flow

1. **Instantiate** a concrete `BaseLoggerTemplate` (`Console` via `print` or `FileLoggerTemplate`).  
2. **Inject** it into the singleton `BaseLogger` (`set_logger`).  
3. **Generate** a log instance (`ErrorLog(...)`, etc.).  
4. **Route** through `BaseLogger.log()` → `logger_template.global_log()` → `print` or file write.  

> **Note:** `global_log` enforces the configured `log_level`.  
> If `log_level < 0`, all messages are printed.

#### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `log` | `BaseLog` | Input to `BaseLogger.log` | `message: str`, `level: int` |
| `log_level` | `int` | Configurable threshold | `>=` message level triggers output |
| `file_path` | `str` | Destination for file logs | Optional; defaults to console |

#### Example Usage

```python
logger = BaseLogger()
logger.set_logger(FileLoggerTemplate("my.log"))
logger.log(InfoLog("Process started", level=1))
```

---
<a name="progress-tracking"></a>
## Progress Tracking – Rich and Console Back‑ends  

### Purpose
Offer a minimal progress interface that can be replaced by a rich terminal bar or a simple console printout, enabling UI‑agnostic task progress reporting.

#### Component Overview

| Class | Responsibility | Key Methods |
|-------|-----------------|-------------|
| `BaseProgress` | Abstract progress interface | `create_new_subtask`, `update_task`, `remove_subtask` |
| `LibProgress` | Rich‑based implementation | Overrides all abstract methods |
| `ConsoleTask` | Lightweight console counter | `progress()` prints percent |
| `ConsoleGtiHubProgress` | Console fallback with a default “General” task | Overrides progress methods |

#### Interaction Flow

1. **Create** a concrete progress instance (`LibProgress` or `ConsoleGtiHubProgress`).  
2. **Create** a sub‑task: `create_new_subtask(name, total_len)`.  
3. **Advance** with `update_task()` per iteration.  
4. **Remove** sub‑task once done: `remove_subtask()`.  

If no sub‑task exists, the *General* task advances.

> **Assumption:** The `Progress` object passed to `LibProgress` is a `rich.progress.Progress` instance; its `add_task` returns a task ID used by `update_task`.

#### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `name` | `str` | Sub‑task identifier | Displayed in console or progress bar |
| `total_len` | `int` | Total units of work | Determines progress percentage |
| `progress` | `rich.progress.Progress` | Rich progress bar instance | Only used by `LibProgress` |

---
<a name="install-ps1"></a>
## Installation Helper – PowerShell Script (`install.ps1`)  

### Purpose
Automate the creation of a GitHub Actions workflow and a default `autodocconfig.yml` file for a project, ensuring the Auto‑Doc Generator is ready to run without manual setup.

#### Key Steps

1. **Create** `.github/workflows` directory if missing.  
2. **Write** `autodoc.yml` workflow that references the reusable `reuseble_agd.yml` template.  
3. **Generate** a YAML configuration file containing:
   - Project name (derived from current folder)
   - Language
   - Ignored file patterns
   - Build and structure settings

> **Side effect:** Emits a green “✅ Done!” message to the console upon completion.

#### Data Contract

| Entity | Type | Role | Notes |
|--------|------|------|-------|
| `project_name` | `str` | Derived from current folder | Used for configuration metadata |
| `language` | `str` | Localization setting | Default `en` |
| `ignore_files` | `list[str]` | File glob patterns to skip | Passed to `Config` |
| `build_settings` | `dict` | Runtime flags | e.g., `save_logs`, `log_level` |
| `structure_settings` | `dict` | Document layout flags | e.g., `include_intro_text` |

---
<a name="install-bash"></a>
## Install.sh Script – Workflow Automation  

### Purpose  
Creates a minimal CI setup for Auto‑Doc Generator in an existing repository by:

1. Generating a GitHub Actions workflow that re‑uses the shared `reuseble_agd.yml` template.  
2. Writing a default `autodocconfig.yml` that captures project metadata, ignore patterns, and build/structure settings.  

This eliminates manual configuration steps, enabling immediate `autodocgenerator` runs from the command line or within CI.  

### Data Contract  

| Entity          | Type | Role | Notes |
|-----------------|------|------|-------|
| `project_name`  | `str` | Derived from the current working directory | Populates `project_name` in `autodocconfig.yml`. |
| `language`      | `str` | Localization flag | Defaults to `"en"` in the config. |
| `ignore_files`  | `list[str]` | File glob patterns to skip | Directly copied into the config. |
| `build_settings`| `dict` | Runtime flags for the generator | e.g., `save_logs`, `log_level`. |
| `structure_settings` | `dict` | Document layout flags | e.g., `include_intro_*`, `use_global_file`. |
| `workflow_path` | `str` | Target path for GitHub Action | `.github/workflows/autodoc.yml`. |
| `config_path`   | `str` | Target path for config | `autodocconfig.yml`. |

> **Side effect**: prints a green “✅ Done!” message once each file is written.  

### Step‑by‑Step Logic  

1. **Create workflow directory**  
   ```bash
   mkdir -p .github/workflows
   ```
   *Creates `.github/workflows` if missing, ensuring GitHub can discover the workflow.*

2. **Write GitHub Actions workflow**  
   ```bash
   cat <<EOF > .github/workflows/autodoc.yml
   name: AutoDoc
   on: [workflow_dispatch]
   jobs:
     run:
       permissions:
         contents: write
       uses: Drag-GameStudio/ADG/.github/workflows/reuseble_agd.yml@main
       secrets:
         GROCK_API_KEY: \${{ secrets.GROCK_API_KEY }}
   EOF
   ```
   *A single‑file workflow that triggers manually and forwards the `GROCK_API_KEY` secret to the reusable template.*

3. **Emit completion message**  
   ```bash
   echo "✅ Done! .github/workflows/autodoc.yml has been created."
   ```
   *Immediate visual confirmation for the user.*

4. **Write default `autodocconfig.yml`**  
   ```bash
   cat <<EOF > autodocconfig.yml
   project_name: "$(basename "$PWD")"
   language: "en"
   ...
   EOF
   ```
   *The file is populated with:*

   - **Project metadata** – name, language.  
   - **`ignore_files`** – a comprehensive list covering Python bytecode, caches, virtualenvs, logs, VCS data, etc.  
   - **`build_settings`** – flags controlling log persistence and verbosity.  
   - **`structure_settings`** – toggles for intro sections, ordering, and global file generation, plus `max_doc_part_size`.  

5. **Emit second completion message**  
   ```bash
   echo "✅ Done! autodocconfig.yml has been created."
   ```

### Outputs  

- File **`.github/workflows/autodoc.yml`**: ready to run the Auto‑Doc Generator in a CI context.  
- File **`autodocconfig.yml`**: initial configuration that can be edited to suit a particular project.  
- Console output: two success messages indicating successful file creation.  

> **Note**: The script assumes a POSIX‑compatible shell (Bash) and that the current directory is a valid repository root.

---
