# Project Overview: Auto Doc Generator

## **Project Title**  
Auto Doc Generator

---

## **Project Goal**  
The Auto Doc Generator is a software tool designed to automate the creation of comprehensive project documentation. By analyzing codebases, leveraging advanced AI models, and processing modular configurations, it simplifies the documentation process, saving developers time and ensuring consistency. The tool addresses the common challenge of maintaining up-to-date and well-structured documentation, which is essential for collaboration, onboarding, and project scalability.

---

## **Core Logic & Principles**  
The Auto Doc Generator operates using a layered architecture, comprising several modular components that work together to analyze a codebase, generate documentation, and organize it into a structured format. The process is initiated through a central entry point and follows a systematic flow:

1. **Configuration Loading**:  
   The tool begins by parsing a configuration file (`autodocconfig.yml`) to load global settings, project-specific configurations, and user-defined modules. This is managed by the `config_reader.read_config` module.

2. **Git Repository Analysis**:  
   The tool checks the Git repository status to identify changes since the last commit. This step ensures that documentation is only regenerated when necessary, optimizing performance.

3. **Preprocessing**:  
   Input files are validated, split, and formatted to prepare them for documentation generation. This step ensures that the input data is clean and manageable.

4. **Documentation Generation**:  
   The core logic of the tool involves generating code documentation, creating global project information, and splitting the documentation into modular sections. AI models (e.g., GPT, Azure) are used to generate text, ensuring high-quality and contextually relevant content.

5. **Postprocessing**:  
   The generated documentation is finalized by embedding semantic data, handling custom introductions, and sorting sections for readability and logical flow.

6. **Output Handling**:  
   The final documentation is saved to a `README.md` file, and a detailed report is logged in `agd_report.txt`.

The tool's modular design allows for extensibility, enabling users to integrate custom modules and adapt the documentation structure to their specific needs.

---

## **Key Features**  
- **Automated Documentation Generation**: Uses AI models to create detailed and accurate project documentation.  
- **Git Integration**: Analyzes repository changes to determine if documentation updates are required.  
- **Customizable Configurations**: Supports user-defined settings and modular configurations via YAML files.  
- **Preprocessing Capabilities**: Validates, splits, and formats input files for efficient processing.  
- **Postprocessing Enhancements**: Embeds semantic data, organizes sections, and incorporates custom introductions.  
- **Multi-Model AI Integration**: Supports Azure, GPT-4o, and GPT models with fallback mechanisms for reliability.  
- **Error Handling**: Includes robust mechanisms for managing model failures and ensuring uninterrupted operation.  
- **Comprehensive Output**: Generates a `README.md` file and a detailed log report (`agd_report.txt`).  
- **Extensibility**: Allows integration of custom modules for tailored documentation needs.  
- **Structured Logging**: Provides detailed logs for errors, warnings, and informational messages.  

---

## **Dependencies**  
To run the Auto Doc Generator, the following libraries and tools are required:  

- **Programming Language**: Python  
- **Configuration Parsing**: `yaml`  
- **Git Integration**: `subprocess` for executing Git commands  
- **AI Model Integrations**:  
  - Azure AI: `ChatCompletionsClient`  
  - OpenAI GPT-4o API  
  - Groq GPT-OSS API  
- **Logging**: Custom logging modules (`BaseLogger`, `InfoLog`, `ErrorLog`, `WarningLog`)  
- **Secrets Management**:  
  - `GROQ_API_KEYS`  
  - `GH_MODEL_API_KEYS`  
  - `GOOGLE_EMBEDDING_API_KEY`  

---

The Auto Doc Generator is a powerful and flexible tool that leverages cutting-edge AI technologies to streamline the documentation process. Its modular architecture, robust error handling, and support for customization make it an invaluable resource for developers and teams looking to maintain high-quality project documentation effortlessly.
## Executive Navigation Tree

### 📂 Repository Structure
- [Repository Structure](#repository-structure)
- [Init Folder System](#init-folder-system)
- [Project Build Config](#project-build-config)
- [Project Settings Class](#project-settings-class)
- [Pyproject Toml](#pyproject-toml)

### 📂 Installation Scripts
- [Installation Script](#installation-script)
- [Bash Installation Script](#bash-installation-script)
- [Installation Workflow Scripts](#installation-workflow-scripts)

### 📂 Workflow Management
- [Workflow Analysis](#workflow-analysis)
- [CI/CD Workflow](#ci-cd-workflow)
- [Reusable Workflow](#reusable-workflow)
- [AutoDoc Workflow](#autodoc-workflow)

### 📂 AutoDoc Configuration
- [AutoDocConfig YML](#autodocconfig-yml)
- [AutoDocConfig Options](#autodocconfig-options)

### 📂 Observations & Data Flow
- [Key Observations](#key-observations)
- [Data Flow](#data-flow)
- [Check Git Status](#check-git-status)
- [Read Config](#read-config)
- [Check Sense Changes](#check-sense-changes)
- [Clear Cache](#clear-cache)
- [Have to Change](#have-to-change)

### 📂 Data Contracts
- [Data Contracts](#data-contracts)
- [Data Contract](#data-contract)

### 📂 Data Processing Functions
- [Split Data Function](#split-data-function)
- [Split Text by Anchors](#split-text-by-anchors)
- [Extract Links from Start](#extract-links-from-start)
- [Get Order](#get-order)
- [Order Doc](#order-doc)

### 📂 Embedding & Sorting
- [Embedding Generation and Sorting](#embedding-generation-and-sorting)
- [Create Embedding Layer](#create-embedding-layer)

### 📂 Response Handling
- [Response Cleaning](#response-cleaning)
- [Prompt Parsing](#prompt-parsing)
- [Parse Answer](#parse-answer)
- [Answer Generation](#answer-generation)
- [Custom Introduction Generation](#custom-introduction-generation)

### 📂 Documentation Generation
- [Custom Modules](#custom-modules)
- [Intro Modules](#intro-modules)
- [Gen Doc Function](#gen-doc-function)
- [Gen Doc Parts Function](#gen-doc-parts-function)
- [Write Docs by Parts Function](#write-docs-by-parts-function)
- [Generate Code File](#generate-code-file)
- [Generate Global Info](#generate-global-info)
- [Generate Doc Parts](#generate-doc-parts)
- [Factory Generate Doc](#factory-generate-doc)

### 📂 Documentation Factory
- [DocFactory](#docfactory)
- [DocFactory Class](#docfactory-class)
- [Doc Schema Classes](#doc-schema-classes)

### 📂 Core Classes
- [Config Class](#config-class)
- [Model Class](#model-class)
- [AsyncModel Class](#asyncmodel-class)
- [ParentModel Class](#parentmodel-class)
- [ParentModel Implementation](#parentmodel-implementation)
- [History Class](#history-class)
- [Manager Class](#manager-class)
- [Manager Class Usage and Methods](#manager-class-usage-and-methods)
- [CodeMix Class](#codemix-class)

### 📂 Compression Module
- [Compressor Module](#compressor-module)
- [Compress Method](#compress-method)
- [Compress and Compare Method](#compress-and-compare-method)
- [Compress to One Method](#compress-to-one-method)

### 📂 Exception Handling
- [Model Exhausted Exception](#model-exhausted-exception)

### 📂 GPT Models
- [GPT Models](#gpt-models)
- [GPT Model](#gpt-model)
- [GPT Init](#gpt-init)
- [GPT Generate Answer](#gpt-generate-answer)
- [GPT4o Model](#gpt4o-model)
- [GPT4o Init](#gpt4o-init)
- [GPT4o Generate Answer](#gpt4o-generate-answer)

### 📂 Azure Integration
- [Azure Model Class](#azure-model-class)
- [Azure Model Initialization](#azure-model-initialization)

### 📂 System Utilities
- [Logging System](#logging-system)
- [Progress System](#progress-system)
- [AutoDocGenerator Init](#autodocgenerator-init)
<a name="repository-structure"></a>
## Repository Structure

| **Path**                        | **Description**                                                                                   |
|----------------------------------|---------------------------------------------------------------------------------------------------|
| `.github/workflows/`            | Contains GitHub Actions workflows for CI/CD and documentation generation.                        |
| `.github/workflows/autodoc.yml` | GitHub Action workflow for running the AutoDoc documentation generation process.                 |
| `.github/workflows/main.yml`    | CI/CD workflow for building, testing, and publishing the library to PyPI.                        |
| `.github/workflows/reuseble_agd.yml` | Reusable workflow for generating documentation using the `autodocgenerator` package.          |
| `agd_report.txt`                | Log file generated during the documentation process.                                              |
| `autodocconfig.yml`             | Configuration file for the Auto Doc Generator project.                                            |
| `autodocgenerator/`             | Main source code directory containing modules for the documentation generation process.           |
| `autodocgenerator/auto_runner/` | Contains scripts for running the main documentation generation process and managing configurations. |
| `autodocgenerator/config/`      | Handles global settings and configurations for the project.                                       |
| `autodocgenerator/engine/`      | Contains AI model integrations and exception handling.                                            |
| `autodocgenerator/factory/`     | Provides modular documentation generation functionality.                                          |
| `autodocgenerator/postprocessor/` | Handles finalization of generated documentation, including embedding, sorting, and custom introductions. |
| `autodocgenerator/preprocessor/` | Prepares input files by validating, splitting, and formatting content.                           |
| `autodocgenerator/schema/`      | Defines schemas for caching and documentation structures.                                         |
| `autodocgenerator/ui/`          | Manages logging and progress tracking for user feedback.                                          |
| `install.ps1`                   | PowerShell script for installing the project.                                                    |
| `install.sh`                    | Shell script for installing the project on Linux-based systems.                                  |
| `poetry.lock`                   | Dependency lock file for the Poetry package manager.                                              |
| `pyproject.toml`                | Configuration file for the Python project and its dependencies.                                  |

---
<a name="init-folder-system"></a> `init_folder_system(project_directory)`
**Responsibility:**  
Initializes the folder and cache system for the project.

**Logic Flow:**
1. Creates a cache folder (`.auto_doc_cache`) if it doesn't exist.
2. Initializes a cache file (`.auto_doc_cache_file.json`) with default settings if absent.
3. Loads cache settings from the cache file.

---

####
<a name="project-build-config"></a>
## `ProjectBuildConfig` Class: Build Configuration

### Purpose
The `ProjectBuildConfig` class manages settings related to the build process, such as logging and change thresholds.

---

### Attributes
| **Attribute**          | **Type** | **Role**                              | **Notes**                                   |
|-------------------------|----------|---------------------------------------|---------------------------------------------|
| `save_logs`             | `bool`   | Whether to save logs during the build.| Default is `False`.                         |
| `log_level`             | `int`    | Logging level for the build process.  | Default is `-1`.                            |
| `threshold_changes`     | `int`    | Threshold for detecting significant changes. | Default is `20000`.                         |

---

### Methods
| **Method**                          | **Parameters**                          | **Purpose**                                 |
|-------------------------------------|------------------------------------------|---------------------------------------------|
| `load_settings(data: dict[str, Any])` | `data`: Dictionary of settings          | Updates the object's attributes with the provided settings. |

---
<a name="project-settings-class"></a>
## `ProjectSettings` Class

This class encapsulates project-specific settings and generates a prompt for AI models.

### Functional Role
- Stores project metadata and generates a structured prompt for AI models.

**Key Methods**:

#### `add_info`
- Adds a key-value pair to the project settings.

#### `prompt`
- Generates a structured prompt string based on the project name and additional metadata.

**Inputs and Outputs**:

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `project_name`      | `str`          | Name of the project.                        | Set during initialization.             |
| `key`               | `str`          | Metadata key to add.                        | Used in `add_info` method.             |
| `value`             | `str`          | Metadata value to add.                      | Used in `add_info` method.             |
| **Returns**         | `str`          | Structured prompt string.                   | Used as input for AI models.           |

---

### Critical Notes
> - The `compress` method relies on the AI model's ability to generate accurate summaries. Ensure the model is trained for the specific data type.
> - The `compress_to_one` method may result in data loss if the compression power is too high. Adjust the `compress_power` parameter carefully.
> - The `ProjectSettings.prompt` method assumes that `BASE_SETTINGS_PROMPT` is a valid string and that `project_name` and `info` are correctly initialized.
<a name="pyproject-toml"></a>
## Project Metadata (`pyproject.toml`)

### Functional Role
The `pyproject.toml` file defines the metadata, dependencies, and build system for the **Auto Doc Generator** project. It is essential for managing the project's environment and dependencies.

---

### Key Sections

#### `[project]`
```toml
[project]
name = "autodocgenerator"
version = "1.4.9.5"
description = "This Project helps you to create docs for your projects"
authors = [
    {name = "dima-on", email = "sinica911@gmail.com"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11,<4.0"
dependencies = [
    ...
]
```

- **`name`**: The name of the project is `autodocgenerator`.
- **`version`**: Current version is `1.4.9.5`.
- **`description`**: A brief description of the project.
- **`authors`**: Includes the name and email of the author.
- **`license`**: Specifies the license type as MIT.
- **`requires-python`**: The project requires Python version 3.11 or higher but less than 4.0.
- **`dependencies`**: Lists all required dependencies for the project.

#### `[tool.poetry]`
```toml
[tool.poetry]
exclude = [
    ".auto_doc_cache_file.json"
]
```

- **`exclude`**: Excludes specific files from being packaged with the project.

#### `[build-system]`
```toml
[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"
```

- **`requires`**: Specifies the build system requirements.
- **`build-backend`**: Defines the backend used for building the project.

---

### Key Dependencies
| **Dependency**          | **Version** | **Purpose**                                                                 |
|--------------------------|-------------|-----------------------------------------------------------------------------|
| `pyyaml`                 | 6.0.3       | For parsing YAML configuration files.                                       |
| `rich`                   | 14.2.0      | Provides rich text and progress bar rendering in the terminal.              |
| `openai`                 | 2.14.0      | Integrates with OpenAI's GPT-4 API for documentation generation.            |
| `google-genai`           | 1.56.0      | Supports AI-based text generation using Google's AI services.               |
| `groq`                   | 1.0.0       | Integrates with Groq's GPT-OSS API for AI model usage.                      |
| `azure-ai-inference`     | >=1.0.0b9,<2.0.0 | Provides integration with Azure AI inference services.                     |
| `numpy`                  | >=2.4.3,<3.0.0 | Used for numerical computations and data processing.                       |

---

### Critical Notes
> - The project relies on `poetry` for dependency management and packaging.
> - Ensure all dependencies are installed in the Python environment before running the project.
> - The `GROCK_API_KEY` is required for the `groq` dependency to function properly.
<a name="installation-script"></a>
## Installation Script (`install.ps1`)

### Functional Role
The PowerShell script automates the setup of the **Auto Doc Generator** environment by creating necessary configuration files and workflows.

---

### Key Steps

1. **Create Workflow Directory**:
   - Ensures the `.github/workflows` directory exists.
   - Uses `New-Item` with `-Force` to avoid errors if the directory already exists.

2. **Generate Workflow File**:
   - Creates a GitHub Actions workflow file (`autodoc.yml`) with predefined content.
   - Configures the workflow to trigger manually (`workflow_dispatch`) and use a reusable workflow.

3. **Generate Configuration File**:
   - Creates the `autodocconfig.yml` file with default settings.
   - Includes:
     - Project name and language.
     - Ignored files and directories (e.g., `.pyc`, `.git`, `__pycache__`).
     - Build settings (e.g., log level, save logs).
     - Documentation structure settings (e.g., intro links, max part size).

4. **Output Confirmation**:
   - Prints a success message to the console upon completion.

---

### Critical Notes
> - The script assumes the presence of a valid GitHub repository to create the `.github/workflows` directory.
> - The `autodocconfig.yml` file includes default settings that can be customized as needed.
> - The `GROCK_API_KEY` secret must be configured in the GitHub repository for the workflow to function correctly.
<a name="bash-installation-script"></a>
## Bash Installation Script (`install.sh`)

### Functional Role
This Bash script automates the setup of the **Auto Doc Generator** environment by creating essential configuration files and workflows. It is designed to work in Unix-based environments and ensures that the necessary files and directories are properly initialized.

---

### Key Steps

1. **Create Workflow Directory**:
   - Ensures the `.github/workflows` directory exists using the `mkdir -p` command.
   - This prevents errors if the directory already exists.

2. **Generate GitHub Workflow File**:
   - Creates a GitHub Actions workflow file (`autodoc.yml`) with predefined content.
   - Configures the workflow to trigger manually (`workflow_dispatch`) and use a reusable workflow from the repository `Drag-GameStudio/ADG`.

3. **Generate Configuration File**:
   - Creates the `autodocconfig.yml` file with default settings.
   - Includes:
     - `project_name`: Automatically set to the current directory name.
     - `language`: Default language for the documentation (English).
     - `ignore_files`: A comprehensive list of files and directories to exclude from documentation generation.
     - `build_settings`: Configures logging options.
     - `structure_settings`: Defines the structure and size of the generated documentation.

4. **Output Confirmation**:
   - Prints success messages to the console after creating the `autodoc.yml` and `autodocconfig.yml` files.

---

### Key Configuration Details

#### GitHub Workflow File (`autodoc.yml`)
```yaml
name: AutoDoc
on: [workflow_dispatch]
jobs:
  run:
    permissions:
      contents: write
    uses: Drag-GameStudio/ADG/.github/workflows/reuseble_agd.yml@main
    secrets:
      GROCK_API_KEY: ${{ secrets.GROCK_API_KEY }}
```

- **Purpose**: Automates the execution of the Auto Doc Generator using GitHub Actions.
- **Trigger**: The workflow is triggered manually using `workflow_dispatch`.
- **Secrets**: Requires the `GROCK_API_KEY` to be configured in the GitHub repository secrets.

#### Configuration File (`autodocconfig.yml`)
```yaml
project_name: "$(basename "$PWD")"
language: "en"

ignore_files:
  - "*.pyc"
  - "*.pyo"
  - "*.pyd"
  - "__pycache__"
  - ".ruff_cache"
  - ".mypy_cache"
  - ".auto_doc_cache"
  - ".auto_doc_cache_file.json"
  - "venv"
  - "env"
  - ".venv"
  - ".env"
  - ".vscode"
  - ".idea"
  - "*.iml"
  - "*.sqlite3"
  - "*.db"
  - "*.pkl"
  - "data"
  - "*.log"
  - ".coverage"
  - "htmlcov"
  - ".git"
  - ".gitignore"
  - "migrations"
  - "static"
  - "staticfiles"
  - "*.pdb"
  - "*.md"

build_settings:
  save_logs: false
  log_level: 2

structure_settings:
  include_intro_links: true
  include_intro_text: true
  include_order: true
  use_global_file: true
  max_doc_part_size: 5000
```

- **`project_name`**: Automatically set to the name of the current directory.
- **`ignore_files`**: Specifies patterns for files and directories to exclude from documentation.
- **`build_settings`**: Configures logging options, including whether to save logs and the log verbosity level.
- **`structure_settings`**: Defines the structure of the documentation, including intro links, text, and maximum document part size.

---

### Critical Notes
> - The script assumes it is executed in a Unix-based environment with Bash installed.
> - The `autodoc.yml` file requires the `GROCK_API_KEY` secret to be configured in the GitHub repository for the workflow to function.
> - The `autodocconfig.yml` file is pre-configured with default settings but can be customized as needed.
> - Ensure the `Drag-GameStudio/ADG` repository is accessible and contains the `reuseble_agd.yml` workflow file.

---
<a name="installation-workflow-scripts"></a> 

The installation process involves using platform-specific scripts to set up the workflow and configuring a secret variable for GitHub Actions. Below is a detailed explanation:

### Installation Scripts
1. **For PowerShell (Windows)**:
   - Use the following command to execute the installation script:
     ```powershell
     irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
     ```
   - This command fetches the PowerShell script from the specified repository and executes it directly.

2. **For Linux-based Systems**:
   - Use the following command to execute the installation script:
     ```bash
     curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
     ```
   - This command downloads the shell script from the repository and runs it using `bash`.

### GitHub Actions Configuration
To enable the workflow to function correctly, you must add a secret variable to your GitHub repository:

1. Navigate to your repository on GitHub.
2. Go to **Settings** > **Secrets and variables** > **Actions**.
3. Click **New repository secret**.
4. Set the name of the secret to `GROCK_API_KEY`.
5. Retrieve your API key from the documentation provided by Grock and paste it as the value of the secret.
6. Save the secret.

This configuration ensures that the scripts and workflows have the necessary credentials to operate seamlessly.
<a name="workflow-analysis"></a>
## Workflow Analysis

###
<a name="ci-cd-workflow"></a>**CI/CD Workflow (`main.yml`)**

This workflow is triggered on:
- **Push events** to the `main` branch, specifically when `pyproject.toml` is modified.
- **Pull requests** targeting the `main` branch with changes to `pyproject.toml`.

#### Workflow Steps:
1. **Checkout Code**: Clones the repository.
2. **Set Up Python**: Configures Python 3.12 environment.
3. **Install Poetry**: Installs the Poetry package manager.
4. **Install Dependencies**: Installs project dependencies using Poetry.
5. **Publish Library**: Publishes the library to PyPI using the `POETRY_PYPI_TOKEN_PYPI` secret.

---

###
<a name="reusable-workflow"></a>**Reusable Workflow (`reuseble_agd.yml`)**

This reusable workflow is designed to generate documentation using the `autodocgenerator` package.

#### Workflow Steps:
1. **Checkout Code**: Clones the repository with full history (`fetch-depth: 0`).
2. **Set Up Python**: Configures Python 3.12 environment.
3. **Install AutoDocGenerator**: Installs the `autodocgenerator` package via `pip`.
4. **Run Documentation Generation**:
   - Executes the `autodocgenerator.auto_runner.run_file` module to generate documentation.
   - Passes the required API keys and environment variables.
5. **Copy Output to README**:
   - Copies the generated documentation from `.auto_doc_cache/output_doc.md` to `README.md`.
6. **Copy Logs**:
   - Copies the log file (`.auto_doc_cache/report.txt`) to `agd_report.txt`.
7. **Commit and Push Changes**:
   - Commits and pushes the updated `README.md` and log files to the repository.

---
<a name="autodoc-workflow"></a>**AutoDoc Workflow (`autodoc.yml`)**

This workflow is triggered on:
- **Push events** to the `main` branch.
- **Manual dispatch** via the GitHub Actions interface.

#### Workflow Steps:
1. **Run Job**:
   - Uses the reusable workflow `reuseble_agd.yml` from the repository.
   - Passes the following secrets to the reusable workflow:
     - `GROQ_API_KEYS`
     - `GH_MODEL_API_KEYS`
     - `GOOGLE_EMBEDDING_API_KEY`

---

###
<a name="autodocconfig-yml"></a>
## Configuration File: `autodocconfig.yml`

This YAML file defines the project settings, ignored files, build settings, and structure settings for the Auto Doc Generator.

### Key Sections and Parameters

#### **Project Settings**
| **Parameter**       | **Value**                     | **Description**                                      |
|----------------------|-------------------------------|-----------------------------------------------------|
| `project_name`       | `"Auto Doc Generator"`        | The name of the project.                            |
| `language`           | `"en"`                       | The language for the generated documentation.       |

#### **Ignored Files**
Specifies files and directories to exclude from documentation generation, such as:
- Compiled Python files (`.pyc`, `.pyo`, `.pyd`)
- Cache directories (`__pycache__`, `.ruff_cache`, `.mypy_cache`)
- Virtual environments (`venv`, `.venv`)
- Logs (`*.log`)
- Version control files (`.git`, `.gitignore`)

#### **Build Settings**
| **Parameter**      | **Value** | **Description**                                                                 |
|---------------------|-----------|---------------------------------------------------------------------------------|
| `save_logs`         | `false`   | Whether to save logs during the documentation generation process.               |
| `log_level`         | `2`       | The verbosity level of logs.                                                   |
| `threshold_changes` | `20000`   | The threshold for detecting significant changes that require regeneration.      |

#### **Structure Settings**
| **Parameter**              | **Value** | **Description**                                                                 |
|-----------------------------|-----------|---------------------------------------------------------------------------------|
| `include_intro_links`       | `true`    | Whether to include introduction links in the documentation.                     |
| `include_intro_text`        | `true`    | Whether to include introductory text in the documentation.                      |
| `include_order`             | `true`    | Whether to include an ordered structure in the documentation.                   |
| `use_global_file`           | `true`    | Whether to use a global file for documentation.                                 |
| `max_doc_part_size`         | `5000`    | Maximum size (in characters) for each documentation section.                    |

#### **Custom Descriptions**
- Instructions for installing workflows using `install.ps1` and `install.sh`.
- Guidelines for writing the `autodocconfig.yml` file.
- Explanation of the `Manager` class and its methods, with code examples.

---
<a name="autodocconfig-options"></a>

The `autodocconfig.yml` file is used to configure the Auto Doc Generator project. Below are the available options and their descriptions:

#### 1. **`project_name`**
   - **Description**: Specifies the name of the project.
   - **Example**: `"Auto Doc Generator"`

#### 2. **`language`**
   - **Description**: Defines the language for the documentation.
   - **Example**: `"en"`

#### 3. **`ignore_files`**
   - **Description**: Lists files and directories to be ignored during the documentation generation process.
   - **Examples**:
     - `"dist"` (Ignore the `dist` directory)
     - `"*.pyc"` (Ignore Python bytecode files)
     - `"__pycache__"` (Ignore Python cache directories)
     - `"venv"` (Ignore virtual environment directories)
     - `"*.log"` (Ignore log files)

#### 4. **`build_settings`**
   - **Description**: Configures settings related to the build process.
   - **Options**:
     - `save_logs`: Determines whether logs should be saved.
       - **Example**: `false`
     - `log_level`: Sets the verbosity level of logs.
       - **Example**: `2`
     - `threshold_changes`: Specifies the threshold for changes to trigger documentation updates.
       - **Example**: `20000`

#### 5. **`structure_settings`**
   - **Description**: Defines how the documentation structure should be organized.
   - **Options**:
     - `include_intro_links`: Whether to include links in the introduction.
       - **Example**: `true`
     - `include_intro_text`: Whether to include introductory text.
       - **Example**: `true`
     - `include_order`: Whether to include ordering in the documentation.
       - **Example**: `true`
     - `use_global_file`: Whether to use a global file for documentation.
       - **Example**: `true`
     - `max_doc_part_size`: Maximum size of each documentation part.
       - **Example**: `5000`

#### 6. **`project_additional_info`**
   - **Description**: Provides additional information about the project.
   - **Example**: `"This project was created to help developers make documentations for them projects"`

#### 7. **`custom_descriptions`**
   - **Description**: Allows adding custom descriptions or instructions for the documentation.
   - **Examples**:
     - `"explain how to write autodocconfig.yml file what options are available"`
     - `"explain how to use Manager class and what methods are available. Provide code examples for better understanding"`
<a name="key-observations"></a>
## Key Observations

1. **GitHub Actions Integration**:
   - The project uses a modular approach with reusable workflows to streamline CI/CD and documentation generation processes.
   - Secrets are securely passed to workflows for API integrations.

2. **Documentation Pipeline**:
   - The `reuseble_agd.yml` workflow automates the process of generating documentation, saving logs, and updating the repository with the latest changes.

3. **Configuration Management**:
   - The `autodocconfig.yml` file provides a flexible way to customize the documentation generation process, including file exclusions, structure settings, and additional project-specific information.

4. **Modular Architecture**:
   - The project is organized into distinct modules (e.g., `preprocessor`, `postprocessor`, `engine`, `factory`), promoting reusability and maintainability.

5. **AI Integration**:
   - The project leverages multiple AI models (Azure, GPT-4o, GPT) for generating high-quality documentation.

6. **Output Management**:
   - Documentation is saved to `README.md`, and logs are stored in `agd_report.txt`.

---

If you would like me to document a specific file or component, please provide the file content or specify the target.
<a name="data-flow"></a>
### Data Flow

#### Inputs
| **Entity**              | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `api_key`               | `list[str]`       | List of API keys for authenticating with the respective AI model.        | Used to initialize the API client.                                        |
| `history`               | `History`         | Tracks conversation context for generating responses.                    | Used when `with_history=True`.                                            |
| `models_list`           | `list[str]`       | List of model names available for use.                                   | Used for model selection during response generation.                      |
| `prompt`                | `list[dict[str, str]]` | Optional prompt data for generating a response without history.          | Provided by the user.                                                     |

#### Outputs
| **Entity**              | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `result`                | `str`             | Cleaned AI-generated response.                                           | Extracted from the API response.                                          |

---
<a name="check-git-status"></a>
## `autodocgenerator/auto_runner/check_git_status.py` - Git Status Checker

This script provides functionality to check the status of a Git repository and determine whether documentation regeneration is required.

### Functional Responsibilities
1. **Retrieve Git Diff**: Fetches the changes between the current commit and a target commit.
2. **Analyze Changes**: Parses the differences to determine the type and magnitude of changes (e.g., added, deleted, modified).
3. **Check Git Revision**: Retrieves the current Git commit hash.
4. **Determine Regeneration Need**: Uses the `Manager` class and `CheckGitStatusResultSchema` to decide if documentation needs to be regenerated.

### Key Functions
#### `get_diff_by_hash(target_hash)`
- **Purpose**: Retrieves the Git diff between the current HEAD and a specified commit hash, excluding markdown files.
- **Error Handling**: Catches `subprocess.CalledProcessError` and logs the error message.

#### `get_detailed_diff_stats(target_hash)`
- **Purpose**: Provides detailed statistics about changes in files since a specified commit.
- **Logic**:
  1. Executes `git diff` with the `--numstat` option to get added/deleted lines for each file.
  2. Parses the output to determine the status of each file (`ADDED`, `DELETED`, `MODIFIED`).
  3. Returns a list of dictionaries containing file path, status, and change counts.

#### `get_git_revision_hash()`
- **Purpose**: Retrieves the current Git commit hash using the `git rev-parse` command.

#### `check_git_status(manager: Manager)`
- **Purpose**: Determines if documentation regeneration is needed based on Git changes.
- **Logic**:
  1. If the GitHub event is `workflow_dispatch` or no previous commit is stored, sets the current commit as the last processed commit and triggers regeneration.
  2. Otherwise, analyzes changes since the last commit using `get_detailed_diff_stats`.
  3. Uses `Manager.check_sense_changes` to determine if significant changes occurred.
  4. Returns a `CheckGitStatusResultSchema` object indicating whether regeneration is required.

---
<a name="read-config"></a>
## `autodocgenerator/auto_runner/config_reader.py` - Configuration File Parser

This script provides functionality to parse the `autodocconfig.yml` file and load project-specific settings, custom modules, and structure settings.

### Functional Responsibilities
1. **Parse YAML Configuration**: Reads and processes the `autodocconfig.yml` file.
2. **Load Project Settings**: Configures project-specific settings, including ignored files, language, and additional metadata.
3. **Initialize Custom Modules**: Loads custom modules for documentation generation.
4. **Structure Settings**: Configures settings for documentation structure (e.g., intro links, order, max section size).

### Key Classes and Methods
#### `StructureSettings`
- **Attributes**:
  - `include_intro_links`: Whether to include introduction links in the documentation.
  - `include_order`: Whether to include an ordered structure.
  - `use_global_file`: Whether to use a global file for documentation.
  - `max_doc_part_size`: Maximum size (in characters) for each documentation section.
  - `include_intro_text`: Whether to include introductory text.
- **Method**:
  - `load_settings(data: dict[str, Any])`: Updates the object's attributes based on a dictionary of settings.

#### `read_config(file_data: str)`
- **Purpose**: Parses the `autodocconfig.yml` file and returns a tuple containing:
  1. `Config`: Object with project settings and metadata.
  2. `custom_modules`: List of custom modules for documentation generation.
  3. `StructureSettings`: Object with documentation structure settings.
- **Logic**:
  1. Parses the YAML file into a dictionary.
  2. Extracts project settings, ignored files, and additional metadata.
  3. Initializes `Config` and `StructureSettings` objects with the extracted data.
  4. Processes custom descriptions into `CustomModule` or `CustomModuleWithOutContext` objects.
  5. Returns the configured objects.

---
<a name="check-sense-changes"></a> `check_sense_changes(changes)`
**Responsibility:**  
Determines if documentation regeneration is necessary based on changes in the Git repository.

**Logic Flow:**
1. Calls `have_to_change` with the AI model, detected changes, and cached global information.
2. Returns a `CheckGitStatusResultSchema` indicating whether regeneration is required.

---

####
<a name="clear-cache"></a> `clear_cache()`
**Responsibility:**  
Clears cached logs if the `save_logs` configuration is disabled.

**Logic Flow:**
1. Checks the `save_logs` setting in the configuration.
2. Deletes the log file if `save_logs` is `False`.

---

#### <a name="save"></a> `save()`
**Responsibility:**  
Saves the generated documentation and updates the cache file.

**Logic Flow:**
1. Writes the full documentation to `output_doc.md`.
2. Updates `cache_settings.doc` with the current `doc_info`.
3. Saves the updated cache settings to `.auto_doc_cache_file.json`.

---

### Data Contract

#### Inputs
| **Entity**              | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `project_directory`     | `str`            | Path to the project's root directory.                                    | Used for file and folder management.                                      |
| `config`                | `Config`         | Configuration object containing project settings.                        | Includes ignored files, project settings, and logging preferences.        |
| `llm_model`             | `Model`          | AI model used for text generation.                                       | Passed to methods for generating summaries and documentation.             |
| `embedding_model`       | `Embedding`      | Model used for generating embeddings.                                    | Used to initialize embeddings for documentation parts.                    |
| `progress_bar`          | `BaseProgress`   | Progress tracking object.                                                | Defaults to a base implementation if not provided.                        |
| `changes`               | `list[dict]`     | List of file changes in the Git repository.                              | Used to determine if regeneration is necessary.                           |

#### Outputs
| **Entity**              | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `doc_info`              | `DocInfoSchema`  | Stores the generated documentation and related metadata.                 | Includes `code_mix`, `global_info`, and `doc` attributes.                 |
| `cache_settings`        | `CacheSettings`  | Stores cache-related settings and the last processed documentation info. | Loaded from and saved to `.auto_doc_cache_file.json`.                     |
| `output_doc.md`         | `str`            | File containing the final generated documentation.                       | Generated by the `save` method.                                           |

---

### Key Dependencies
- **Preprocessing Modules:**
  - `split_data`, `gen_doc_parts`, `compress_to_one`, `CodeMix`, `have_to_change`.
- **Postprocessing Modules:**
  - `get_order`, `split_text_by_anchors`, `Embedding`.
- **Schema Definitions:**
  - `DocContent`, `DocHeadSchema`, `DocInfoSchema`, `CacheSettings`, `CheckGitStatusResultSchema`.
- **Utilities:**
  - `BaseLogger`, `BaseProgress`, `FileLoggerTemplate`.
- **Factory:**
  - `DocFactory` for modular documentation generation.

---

### Critical Notes
> - The `Manager` class is central to the Auto Doc Generator's functionality, managing the end-to-end documentation workflow.
> - The `CACHE_FOLDER_NAME` and `FILE_NAMES` constants define the structure of the cache and output files.
> - Error handling for file operations is minimal; consider enhancing exception handling for robustness.
> - The `generate_global_info` method allows for reusable global information, optimizing performance for large projects.
<a name="have-to-change"></a>
## `have_to_change` Function

This function determines if documentation or global files need to be updated based on the AI model's analysis of code changes.

### Functional Role
- Sends a prompt to an AI model with information about code changes and global project info.
- Parses the model's response to determine if updates are required.

### Logic Flow
1. Define a prompt with the base changes check message, global info, and code changes.
2. Send the prompt to the AI model using the `get_answer_without_history` method.
3. Parse the model's response using `parse_answer`.
4. Return the parsed result.

### Inputs and Outputs

| **Entity**         | **Type**       | **Role**                                    | **Notes**                              |
|--------------------|----------------|---------------------------------------------|----------------------------------------|
| `model`            | `Model`        | AI model used for analysis.                 | Instance of the `Model` class.         |
| `diff`             | `list[dict[str, str]]` | List of code changes.                      | Each item is a dictionary of changes.  |
| `global_info`      | `str | None`   | Global project information.                 | Optional input.                        |
| **Returns**        | `CheckGitStatusResultSchema` | Schema object with parsed flags. | Indicates whether regeneration is needed.|

---
<a name="data-contracts"></a>
## Data Contracts

### `get_diff_by_hash`
| **Entity** | **Type** | **Role** | **Notes** |
|------------|----------|----------|-----------|
| `target_hash` | `str` | Input | The target commit hash to compare against. |
| **Returns** | `str` or `None` | Output | The Git diff as a string, or `None` if an error occurs. |

### `get_detailed_diff_stats`
| **Entity** | **Type** | **Role** | **Notes** |
|------------|----------|----------|-----------|
| `target_hash` | `str` | Input | The target commit hash to compare against. |
| **Returns** | `list[dict[str, str]]` | Output | A list of dictionaries containing file change details. |

### `get_git_revision_hash`
| **Entity** | **Type** | **Role** | **Notes** |
|------------|----------|----------|-----------|
| **Returns** | `str` | Output | The current Git commit hash. |

### `check_git_status`
| **Entity** | **Type** | **Role** | **Notes** |
|------------|----------|----------|-----------|
| `manager` | `Manager` | Input | The `Manager` instance containing project settings and cache. |
| **Returns** | `CheckGitStatusResultSchema` | Output | Indicates whether documentation regeneration is required. |

### `read_config`
| **Entity** | **Type** | **Role** | **Notes** |
|------------|----------|----------|-----------|
| `file_data` | `str` | Input | The content of the `autodocconfig.yml` file as a string. |
| **Returns** | `tuple` | Output | A tuple containing `Config`, `custom_modules`, and `StructureSettings`. |
<a name="data-contract"></a>
### Data Contract

#### Inputs
| **Entity**              | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `info`                  | `dict`           | Project-specific information for generating documentation.               | Includes keys like `code_mix`, `language`, and `global_info`.             |
| `model`                 | `Model`          | The AI model used for content generation.                                | Passed to each module's `generate` method.                                |
| `discription`           | `str`            | Custom description provided for context.                                 | Used by `CustomModule` and `CustomModuleWithOutContext`.                  |

#### Outputs
| **Entity**              | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `doc_head`              | `DocHeadSchema`  | Contains the generated documentation parts.                              | Includes sections generated by each module.                               |
<a name="split-data-function"></a>
## `split_data` Function

### Functional Role
This function splits a given dataset into smaller parts based on a specified maximum symbol limit. It ensures that the data is divided into manageable chunks while maintaining the integrity of the content.

### Technical Logic Flow
1. **Initialization**:
   - A logger instance is created to log the process.
   - A loop iterates over the `splited_by_files` list, which contains the data to be split.
2. **Splitting Logic**:
   - If the length of an element exceeds 1.5 times the `max_symbols`, it is split into two parts:
     - The first half of the element is retained in the current position.
     - The second half is inserted into the next position.
   - The process repeats until no further splitting is required.
3. **Chunk Assignment**:
   - The split data is assigned to `split_objects` based on the `max_symbols` limit.
   - If the current chunk exceeds the limit, a new chunk is created.
4. **Logging**:
   - The logger logs the number of parts the data has been split into.

### Inputs and Outputs

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `splited_by_files`  | `list[str]`    | List of data strings to be split.           | Each string represents a data chunk.   |
| `max_symbols`       | `int`          | Maximum number of symbols per chunk.        | Determines the size of each chunk.     |
| **Returns**         | `list[str]`    | List of split data chunks.                  | Each chunk is within the size limit.   |

---
<a name="split-text-by-anchors"></a>
## `split_text_by_anchors` Function

This function splits a given text into chunks based on anchor tags and maps each anchor to its corresponding chunk.

### Functional Role
- Splits a large text into smaller sections using anchor tags as delimiters.
- Maps each anchor link to its corresponding chunk of text.

### Logic Flow
1. Define a regex pattern to match anchor tags.
2. Split the text into chunks based on the regex pattern.
3. Remove empty or whitespace-only chunks.
4. Extract all anchor links from the chunks using `extract_links_from_start`.
5. If the first chunk does not start with an anchor or if `have_to_del_first` is `True`, remove the first chunk.
6. Ensure the number of anchors matches the number of chunks. If not, raise an exception.
7. Create a dictionary mapping each anchor link to its corresponding chunk.

### Inputs and Outputs

| **Entity**         | **Type**       | **Role**                                    | **Notes**                              |
|--------------------|----------------|---------------------------------------------|----------------------------------------|
| `text`             | `str`          | Input text containing anchor tags.          | Text to be split into chunks.          |
| **Returns**        | `dict[str, str]`| A dictionary mapping anchor links to chunks.| Keys are anchor links, values are text.|

---
<a name="extract-links-from-start"></a>
## `extract_links_from_start` Function

This function extracts anchor links from the start of text chunks and determines if the first chunk should be removed.

### Functional Role
- Identifies anchor links in the provided text chunks using a regex pattern.
- Collects all valid anchor links and determines if the first chunk should be deleted based on the presence of anchors.

### Logic Flow
1. Define a regex pattern to match anchor links (`<a name="..."></a>`).
2. Iterate through each chunk:
   - Check if the chunk starts with a valid anchor link.
   - If a valid anchor is found, append it to the `links` list.
   - If no valid anchor is found in the first chunk, set `have_to_del_first` to `True`.
3. Return the list of links and the `have_to_del_first` flag.

### Inputs and Outputs

| **Entity**         | **Type**       | **Role**                                    | **Notes**                              |
|--------------------|----------------|---------------------------------------------|----------------------------------------|
| `chunks`           | `list[str]`    | List of text chunks to process.             | Each chunk is expected to be a string. |
| **Returns**        | `tuple`        | A tuple containing:                         |                                        |
| `links`            | `list[str]`    | List of extracted anchor links.             | Prefixed with `#`.                     |
| `have_to_del_first`| `bool`         | Indicates if the first chunk should be removed. |                                        |

---
<a name="get-order"></a>
## `get_order` Function

This function uses an AI model to semantically sort a list of text chunks based on their content.

### Functional Role
- Sends a prompt to an AI model to semantically sort titles.
- Returns a list of sorted titles as per the model's response.

### Logic Flow
1. Initialize a logger to track the process.
2. Log the start of the ordering process and the input chunks.
3. Define a prompt for the AI model to sort the titles semantically.
4. Use the `get_answer_without_history` method of the `Model` class to get the sorted list.
5. Parse the model's response into a list of sorted titles.
6. Log the sorted result and return it.

### Inputs and Outputs

| **Entity**         | **Type**       | **Role**                                    | **Notes**                              |
|--------------------|----------------|---------------------------------------------|----------------------------------------|
| `model`            | `Model`        | AI model used for semantic sorting.         | Instance of the `Model` class.         |
| `chanks`           | `list[str]`    | List of text chunks to be sorted.           | Each chunk is expected to be a string. |
| **Returns**        | `list[str]`    | List of sorted titles.                      | Sorted as per the AI model's response. |

---
<a name="order-doc"></a> `order_doc()`
**Responsibility:**  
Orders the documentation sections based on AI-generated recommendations.

**Logic Flow:**
1. Calls `get_order` with the AI model and current content order.
2. Updates `doc_info.doc.content_orders` with the new order.

---

####
<a name="embedding-generation-and-sorting"></a>
## Embedding Generation and Sorting (`embedding.py`)

This module handles embedding generation and sorting of vectors based on their distances. It uses Google's GenAI library for embedding generation.

### Functional Breakdown

#### `bubble_sort_by_dist`
Sorts a list of tuples based on the second element (distance) using the Bubble Sort algorithm.

- **Logic Flow**:
  1. Iterates through the list multiple times.
  2. Compares adjacent elements and swaps them if they are out of order.
  3. Returns the sorted list.

#### `get_len_btw_vectors`
Calculates the Euclidean distance between two vectors.

- **Logic Flow**:
  1. Computes the norm of the difference between `vector1` and `vector2`.
  2. Returns the calculated distance as a float.

#### `sort_vectors`
Sorts a dictionary of vectors based on their distance from a root vector.

- **Logic Flow**:
  1. Iterates through the dictionary and calculates the distance between the root vector and each vector.
  2. Stores the results as a list of tuples (`key`, `distance`).
  3. Sorts the list using `bubble_sort_by_dist`.
  4. Returns a list of keys sorted by their distances.

#### `Embedding` Class
Generates embeddings for input text using Google's GenAI library.

- **Methods**:
  - `__init__`: Initializes the `Embedding` instance with an API key and creates a GenAI client.
  - `get_vector`: Generates a vector representation of the input text using the `gemini-embedding-2-preview` model.

---

### Inputs and Outputs

#### Inputs
| **Entity**               | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|--------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `arr`                    | `list`            | List of tuples to be sorted by distance.                                 | Used in `bubble_sort_by_dist`.                                            |
| `vector1`, `vector2`     | `list`            | Input vectors for distance calculation.                                  | Used in `get_len_btw_vectors`.                                            |
| `root_vector`            | `list`            | Reference vector for sorting.                                            | Used in `sort_vectors`.                                                   |
| `other`                  | `dict[str, Any]`  | Dictionary of vectors to be sorted.                                      | Used in `sort_vectors`.                                                   |
| `api_key`                | `str`             | API key for authenticating with GenAI.                                   | Used in `Embedding.__init__`.                                             |
| `prompt`                 | `str`             | Input text for generating embeddings.                                    | Used in `Embedding.get_vector`.                                           |

#### Outputs
| **Entity**               | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|--------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `sorted_list`            | `list`            | List of tuples sorted by distance.                                       | Returned by `bubble_sort_by_dist`.                                        |
| `distance`               | `float`           | Euclidean distance between two vectors.                                  | Returned by `get_len_btw_vectors`.                                        |
| `result_list`            | `list[str]`       | List of keys sorted by vector distance.                                  | Returned by `sort_vectors`.                                               |
| `embedding`              | `list`            | Vector representation of the input text.                                 | Returned by `Embedding.get_vector`.                                       |

---

### Key Dependencies
- **Libraries**:
  - `google.genai` for embedding generation.
  - `numpy` for vector distance calculations.
- **Sorting Algorithm**:
  - Custom `bubble_sort_by_dist` for sorting by distance.

---

### Critical Notes
> - The `bubble_sort_by_dist` function is not optimized for large datasets. Consider using more efficient sorting algorithms like QuickSort or MergeSort for scalability.
> - The `Embedding.get_vector` method raises an exception if no embeddings are returned. Ensure proper error handling in the calling code.
> - The `sort_vectors` function assumes all vectors in the dictionary are of the same dimensionality as the root vector.
<a name="create-embedding-layer"></a> `create_embedding_layer()`
**Responsibility:**  
Generates embeddings for all documentation parts using the embedding model.

**Logic Flow:**
1. Iterates through `doc_info.doc.parts`.
2. Calls `init_embedding` on each part using the `embedding_model`.

---

####
<a name="response-cleaning"></a>
## Response Cleaning: `_clean_deepseek_response`

### Purpose
The `_clean_deepseek_response` method removes unnecessary blocks (e.g., `<think>...</think>`) and trims extra spaces from the raw AI response.

### Parameters
| **Parameter**          | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `text`                 | `str`             | Raw response text from the AI model.                                     | Contains the generated response, including potential unwanted blocks.     |

### Returns
A cleaned string with unnecessary blocks and extra spaces removed.

---
<a name="prompt-parsing"></a>
## Prompt Parsing: `_parse_prompt`

### Purpose
The `_parse_prompt` method converts raw input data into structured `UserMessage` and `SystemMessage` objects for use with the Azure AI API.

### Parameters
| **Parameter**          | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `data`                 | `list[dict[str, str]]` | List of dictionaries representing user/system messages.                  | Each dictionary must contain `role` (e.g., `"user"`, `"system"`) and `content`. |

### Returns
A list of `UserMessage` and `SystemMessage` objects.

---
<a name="parse-answer"></a>
## `parse_answer` Function

This function parses the AI model's response to determine if documentation needs to be regenerated.

### Functional Role
- Parses the AI model's response to extract flags indicating whether documentation or global files need to be regenerated.

### Logic Flow
1. Split the model's response string by the `|` delimiter.
2. Check if the first part of the response indicates a need to remake the documentation.
3. Check if the second part of the response indicates a need to remake the global file.
4. Return a `CheckGitStatusResultSchema` object with the parsed flags.

### Inputs and Outputs

| **Entity**         | **Type**       | **Role**                                    | **Notes**                              |
|--------------------|----------------|---------------------------------------------|----------------------------------------|
| `answer`           | `str`          | AI model's response string.                 | Expected format: `true|true` or similar. |
| **Returns**        | `CheckGitStatusResultSchema` | Schema object with parsed flags. | Indicates whether regeneration is needed.|

---
<a name="answer-generation"></a>
## Answer Generation: `generate_answer`

### Purpose
The `generate_answer` method generates an AI-driven response using Azure AI's `ChatCompletionsClient`. It supports both conversation history and ad-hoc prompts.

### Parameters
| **Parameter**          | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `with_history`         | `bool`            | Whether to use conversation history for generating the response.         | Defaults to `True`.                                                       |
| `prompt`               | `list[dict[str, str]] | None` | Optional prompt data for generating a response without history.          |

### Returns
A cleaned string containing the AI-generated response.

---

### Logic Flow
1. **Logging**: Logs the start of the answer generation process.
2. **Message Selection**:
   - If `with_history` is `True`, uses `self.history.history`.
   - Otherwise, uses the provided `prompt`.
3. **Prompt Parsing**: Converts messages into `UserMessage` and `SystemMessage` objects using `_parse_prompt`.
4. **Model Selection**:
   - Iterates through available models (`regen_models_name`).
   - If a model fails, logs the error and switches to the next model.
   - If all models fail, raises `ModelExhaustedException`.
5. **Response Generation**:
   - Calls `ChatCompletionsClient.complete` with parsed messages and model parameters.
   - Cleans the response using `_clean_deepseek_response`.
6. **Logging and Return**:
   - Logs the generated response and the model used.
   - Returns the cleaned response.

---
<a name="custom-introduction-generation"></a>
## Custom Introduction Generation (`custom_intro.py`)

This module is responsible for generating custom introductions, descriptions, and link-based summaries for the documentation. It leverages AI models to create tailored content based on input data and predefined templates.

### Functional Breakdown

#### `get_all_html_links`
Extracts all HTML anchor links (`<a>` tags) from the provided documentation string.

- **Logic Flow**:
  1. Initializes a logger instance to track the process.
  2. Defines a regex pattern to match `<a>` tags with `name` attributes.
  3. Iterates through all matches in the input string and appends valid links (with a length greater than 5) to the `links` list.
  4. Logs the number of extracted links and their content.

#### `get_links_intro`
Generates an introduction based on the extracted HTML links using an AI model.

- **Logic Flow**:
  1. Constructs a prompt with the extracted links and predefined instructions (`BASE_INTRODACTION_CREATE_LINKS`).
  2. Calls the AI model's `get_answer_without_history` method to generate the introduction.
  3. Logs the generated introduction.

#### `get_introdaction`
Creates a global introduction for the documentation using the provided global data and an AI model.

- **Logic Flow**:
  1. Constructs a prompt with the global data and predefined instructions (`BASE_INTRO_CREATE`).
  2. Uses the AI model's `get_answer_without_history` method to generate the introduction.

#### `generete_custom_discription`
Generates a custom description for specific sections of the documentation using an AI model.

- **Logic Flow**:
  1. Iterates through the provided split data (`splited_data`).
  2. Constructs a prompt with the section data and predefined instructions (`BASE_CUSTOM_DISCRIPTIONS`).
  3. Calls the AI model's `get_answer_without_history` method to generate a description.
  4. If the result contains a "no information" flag, it continues to the next section; otherwise, it returns the generated description.

#### `generete_custom_discription_without`
Generates a custom description without relying on split data, following strict formatting rules.

- **Logic Flow**:
  1. Constructs a prompt with the custom description and predefined instructions.
  2. Calls the AI model's `get_answer_without_history` method to generate the description.

---

### Inputs and Outputs

#### Inputs
| **Entity**               | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|--------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `data`                   | `str`             | Input documentation string for extracting HTML links.                    | Used in `get_all_html_links`.                                             |
| `links`                  | `list[str]`       | List of extracted HTML links.                                            | Passed to `get_links_intro` for generating link-based introductions.      |
| `global_data`            | `str`             | Global data for generating the overall introduction.                     | Used in `get_introdaction`.                                               |
| `splited_data`           | `list[str]`       | List of split documentation sections.                                    | Used in `generete_custom_discription`.                                    |
| `custom_description`     | `str`             | Task-specific description to generate.                                   | Used in both `generete_custom_discription` and `generete_custom_discription_without`. |
| `model`                  | `Model`           | AI model used for text generation.                                       | Passed to all methods for generating content.                             |
| `language`               | `str`             | Language for the AI model's responses.                                   | Defaults to "en".                                                         |

#### Outputs
| **Entity**               | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|--------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `links`                  | `list[str]`       | Extracted HTML links from the documentation.                             | Returned by `get_all_html_links`.                                         |
| `intro_links`            | `str`             | AI-generated introduction using the extracted links.                     | Returned by `get_links_intro`.                                            |
| `intro`                  | `str`             | AI-generated global introduction.                                        | Returned by `get_introdaction`.                                           |
| `result`                 | `str`             | AI-generated custom description.                                         | Returned by `generete_custom_discription` and `generete_custom_discription_without`. |

---

### Key Dependencies
- **AI Models**:
  - `GPTModel` and `Model` for generating introductions and descriptions.
- **Configuration Constants**:
  - `BASE_INTRODACTION_CREATE_LINKS`, `BASE_INTRO_CREATE`, `BASE_CUSTOM_DISCRIPTIONS` for prompt templates.
- **Logging**:
  - `BaseLogger` and `InfoLog` for structured logging.
- **Utilities**:
  - `re` for regex-based HTML link extraction.

---

### Critical Notes
> - The `get_all_html_links` function assumes that all valid anchor names are at least 6 characters long.
> - The `generete_custom_discription` function stops iterating through `splited_data` as soon as a valid description is generated.
> - The `generete_custom_discription_without` function enforces strict formatting rules for the generated description, ensuring compliance with predefined standards.

---
<a name="custom-modules"></a>
## Custom Modules for Documentation

### `CustomModule`

#### Responsibility
Generates documentation parts with context by splitting input data and using the AI model to create a custom description.

#### Key Methods
- **`generate(info: dict, model: Model)`**:
  - Splits the input data (`info["code_mix"]`) into chunks of up to 5000 symbols.
  - Calls `generete_custom_discription` to generate a custom description using the AI model and the provided `discription`.

---

### `CustomModuleWithOutContext`

#### Responsibility
Generates documentation parts without using context, relying solely on the AI model and a provided description.

#### Key Methods
- **`generate(info: dict, model: Model)`**:
  - Calls `generete_custom_discription_without` to generate a custom description using the AI model and the provided `discription`.

---
<a name="intro-modules"></a>
## Introductory Modules

### `IntroLinks`

#### Responsibility
Generates a list of HTML links as an introduction to the documentation.

#### Key Methods
- **`generate(info: dict, model: Model)`**:
  - Extracts HTML links from `info["full_data"]` using `get_all_html_links`.
  - Generates an introduction for the links using `get_links_intro`.

---

### `IntroText`

#### Responsibility
Generates an introductory text for the documentation.

#### Key Methods
- **`generate(info: dict, model: Model)`**:
  - Generates an introduction based on `info["global_info"]` using `get_introdaction`.

---
<a name="gen-doc-function"></a>
## `gen_doc` Function: Documentation Generation Workflow

### Purpose
The `gen_doc` function is the core of the documentation generation process. It orchestrates the workflow by initializing necessary components, checking for changes in the project, and generating modular documentation based on the provided configuration and structure settings.

---

### Functional Logic
1. **Model Initialization**:
   - Selects a language model (`GPTModel` or `GPT4oModel`) based on the availability of API keys (`GROQ_API_KEYS` or `GH_MODEL_API_KEYS`).
   - Initializes an embedding model using the `Embedding` class and `GOOGLE_EMBEDDING_API_KEY`.

2. **Manager Setup**:
   - Creates a `Manager` instance, passing the project path, configuration, language model, embedding model, and a progress bar (`ConsoleGtiHubProgress`).

3. **Git Status Check**:
   - Calls `check_git_status` to determine if documentation needs to be regenerated based on project changes.
   - If no significant changes are detected (`need_to_remake` and `remake_gl_file` are `False`), the function exits early.

4. **Documentation Generation**:
   - Generates code documentation using `manager.generate_code_file()`.
   - If `use_global_file` is enabled in `structure_settings`, generates global project information with compression.
   - Splits the documentation into sections based on `max_doc_part_size` and global file usage.

5. **Factory-Based Modular Documentation**:
   - Uses the `DocFactory` class to generate modular documentation from `custom_modules`.
   - If `include_order` is enabled, orders the documentation sections.

6. **Additional Modules**:
   - Adds introductory text (`IntroText`) and links (`IntroLinks`) as additional modules if specified in `structure_settings`.
   - Generates documentation for these modules and integrates them at the beginning of the document.

7. **Embedding and Cleanup**:
   - Creates an embedding layer for semantic processing.
   - Clears the manager's cache to free resources.

8. **Output**:
   - Saves the generated documentation and returns the full document as a string.

---

### Data Flow

#### Inputs
| **Entity**            | **Type**                 | **Role**                  | **Notes**                                  |
|------------------------|--------------------------|---------------------------|--------------------------------------------|
| `project_path`         | `str`                   | Input                     | Path to the project directory.             |
| `config`               | `Config`                | Input                     | Configuration object with project settings.|
| `custom_modules`       | `list[BaseModule]`      | Input                     | List of custom modules for documentation.  |
| `structure_settings`   | `StructureSettings`     | Input                     | Settings for documentation structure.      |

#### Outputs
| **Entity**             | **Type**                 | **Role**                  | **Notes**                                  |
|------------------------|--------------------------|---------------------------|--------------------------------------------|
| `output_doc`           | `str`                   | Output                    | The generated documentation as a string.   |

---
<a name="gen-doc-parts-function"></a>
## `gen_doc_parts` Function

### Functional Role
This function orchestrates the generation of documentation by dividing the input code into parts, generating documentation for each part, and combining the results into a complete document.

### Technical Logic Flow
1. **Data Splitting**:
   - Calls `split_data` to divide the input `full_code_mix` into smaller chunks based on `max_symbols`.
2. **Documentation Generation**:
   - Iterates over the split data and generates documentation for each part using `write_docs_by_parts`.
   - Maintains context by passing the last part of the previous result as `prev_info`.
3. **Progress Tracking**:
   - Uses a progress bar (`BaseProgress`) to track the progress of documentation generation.
4. **Result Compilation**:
   - Combines all generated documentation parts into a single string.
5. **Logging**:
   - Logs the total length of the generated documentation and the final output.

### Inputs and Outputs

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `full_code_mix`     | `str`          | Full code to be documented.                 | Input for splitting and documentation. |
| `max_symbols`       | `int`          | Maximum number of symbols per part.         | Determines the size of each chunk.     |
| `model`             | `Model`        | AI model used for generating documentation. | Instance of the `Model` class.         |
| `project_settings`  | `ProjectSettings` | Contains project-specific settings and prompts. | Includes project name and metadata.    |
| `language`          | `str`          | Language for the documentation.             | Defaults to "en".                      |
| `progress_bar`      | `BaseProgress` | Progress bar for tracking the process.      | Tracks progress of documentation generation. |
| `global_info`       | `str` or `None`| Global project information.                 | Optional parameter.                    |
| **Returns**         | `str`          | Complete documentation as a single string.  | Combined result of all parts.          |

---
<a name="write-docs-by-parts-function"></a>
## `write_docs_by_parts` Function

### Functional Role
This function generates documentation for a specific part of the code using an AI model. It constructs a structured prompt and retrieves the AI-generated response.

### Technical Logic Flow
1. **Initialization**:
   - A logger instance is created to log the process.
   - A structured prompt is initialized with system-level instructions, global project info, and base text.
2. **Prompt Construction**:
   - If `global_info` is provided, it is added to the prompt.
   - If `prev_info` is provided, it is appended to the prompt to maintain context.
   - The `part` content is added as the user's input to the prompt.
3. **AI Model Interaction**:
   - The prompt is passed to the `model.get_answer_without_history` method to generate a response.
   - The response is cleaned by removing any extraneous code block markers (e.g., triple backticks).
4. **Logging**:
   - Logs the length and content of the generated documentation.
5. **Return**:
   - Returns the cleaned AI-generated documentation.

### Inputs and Outputs

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `part`              | `str`          | Code part for which documentation is generated. | Input for the AI model.                |
| `model`             | `Model`        | AI model used for generating documentation. | Instance of the `Model` class.         |
| `project_settings`  | `ProjectSettings` | Contains project-specific settings and prompts. | Includes project name and metadata.    |
| `prev_info`         | `str` or `None`| Previous documentation part for context.    | Optional parameter.                    |
| `language`          | `str`          | Language for the documentation.             | Defaults to "en".                      |
| `global_info`       | `str` or `None`| Global project information.                 | Optional parameter.                    |
| **Returns**         | `str`          | AI-generated documentation for the part.    | Cleaned of extraneous markers.         |

---
<a name="generate-code-file"></a> `generate_code_file()`
**Responsibility:**  
Generates a "code mix" by aggregating and processing the project's source code.

**Logic Flow:**
1. Logs the start of the code mix generation process.
2. Uses the `CodeMix` class to build repository content, excluding ignored files.
3. Updates the `doc_info.code_mix` attribute with the generated content.
4. Logs completion and updates the progress bar.

---

####
<a name="generate-global-info"></a> `generate_global_info(compress_power=4, max_symbols=10000, is_reusable=False)`
**Responsibility:**  
Generates a global summary of the project by compressing the code mix.

**Logic Flow:**
1. Checks if reusable data exists in the cache and skips regeneration if applicable.
2. Splits the `code_mix` into manageable chunks using `split_data`.
3. Compresses the chunks into a single summary using the AI model and `compress_to_one`.
4. Updates `doc_info.global_info` and the progress bar.

---

####
<a name="generate-doc-parts"></a> `generete_doc_parts(max_symbols=5000, with_global_file=False)`
**Responsibility:**  
Generates documentation in parts by processing the code mix and optional global information.

**Logic Flow:**
1. Splits the `code_mix` into chunks of up to `max_symbols`.
2. Optionally includes global information in the generation process.
3. Calls `gen_doc_parts` to generate documentation for each chunk.
4. Splits the result into sections using `split_text_by_anchors`.
5. Adds the generated sections to `doc_info.doc`.

---

####
<a name="factory-generate-doc"></a> `factory_generate_doc(doc_factory, to_start=False)`
**Responsibility:**  
Uses a `DocFactory` to generate modular documentation.

**Logic Flow:**
1. Prepares an `info` dictionary containing the current documentation, code mix, and global information.
2. Logs the start of the factory-based generation process.
3. Calls `doc_factory.generate_doc` with the `info` dictionary and AI model.
4. Updates `doc_info.doc` with the generated documentation.
5. Updates the progress bar.

---

####
<a name="docfactory"></a>
## `DocFactory` and Modular Documentation Generation

### Functional Role
The `DocFactory` class orchestrates the generation of modular documentation by leveraging multiple `BaseModule` instances. It integrates with the `Model` class for AI-based content generation and utilizes post-processing tools to structure the output.

---
<a name="docfactory-class"></a>
### `DocFactory` Class

#### Responsibility
- Manages a collection of `BaseModule` instances.
- Generates documentation parts using the provided `Model` and `BaseModule` instances.
- Optionally splits the generated content into sections using anchors.

#### Key Attributes
- **`modules`**: A list of `BaseModule` instances responsible for generating different parts of the documentation.
- **`logger`**: An instance of `BaseLogger` for logging progress and results.
- **`with_splited`**: A flag indicating whether to split the generated content into sections.

#### Key Methods
- **`generate_doc(info: dict, model: Model, progress: BaseProgress) -> DocHeadSchema`**:
  - Iterates through the `modules` to generate documentation parts.
  - Splits the content into sections if `with_splited=True`.
  - Logs the progress and results for each module.
  - Returns a `DocHeadSchema` object containing the generated documentation.

#### Data Flow
| **Entity**              | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `info`                  | `dict`           | Contains project-specific information for documentation generation.      | Passed to each module's `generate` method.                                |
| `model`                 | `Model`          | The AI model used for content generation.                                | Passed to each module's `generate` method.                                |
| `progress`              | `BaseProgress`   | Tracks and updates progress during documentation generation.             | Used to create and update subtasks.                                       |
| `doc_head`              | `DocHeadSchema`  | Stores the generated documentation parts.                                | Returned as the final output.                                             |

---
<a name="doc-schema-classes"></a>
## `DocSchema` Classes

### Functional Role
These classes define the schema for documentation content, headers, and metadata.

#### `DocContent` Class
- Represents a single piece of documentation content.
- Can generate an embedding vector using an `Embedding` model.

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `content`           | `str`          | Content of the documentation.               | Main text of the documentation.        |
| `embedding_vector`  | `list` or `None`| Embedding vector for semantic processing.   | Generated using an `Embedding` model.  |

#### `DocHeadSchema` Class
- Manages the structure and order of documentation parts.
- Supports adding parts, retrieving the full document, and merging with other `DocHeadSchema` objects.

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `content_orders`    | `list[str]`    | Order of content parts.                     | Maintains the sequence of parts.       |
| `parts`             | `dict[str, DocContent]` | Stores content parts by name.              | Maps part names to `DocContent` objects. |

#### `DocInfoSchema` Class
- Encapsulates global information, code mix, and the documentation structure.

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `global_info`       | `str`          | Global project information.                 | Metadata for the project.              |
| `code_mix`          | `str`          | Mixed code content.                         | Input for documentation generation.    |
| `doc`               | `DocHeadSchema`| Documentation structure and content.        | Organized using `DocHeadSchema`.       |

---

### Critical Notes
> - The `split_data` function ensures that no part exceeds the `max_symbols` limit, maintaining content integrity.
> - The `write_docs_by_parts` function relies on the AI model's ability to generate accurate and context-aware documentation.
> - The `gen_doc_parts` function assumes that the `BaseProgress` instance is correctly initialized to track progress.
<a name="config-class"></a>
## `Config` Class: Project Configuration Management

### Purpose
The `Config` class encapsulates project-specific settings, such as ignored files, language preferences, project metadata, and build configurations.

---

### Attributes
| **Attribute**              | **Type**           | **Role**                              | **Notes**                                   |
|-----------------------------|--------------------|---------------------------------------|---------------------------------------------|
| `ignore_files`              | `list[str]`        | Patterns of files to ignore.          | Default patterns include temporary and cache files. |
| `language`                  | `str`              | Language for the documentation.       | Default is `"en"`.                          |
| `project_name`              | `str`              | Name of the project.                  |                                             |
| `project_additional_info`   | `dict`             | Additional metadata for the project.  |                                             |
| `pbc`                       | `ProjectBuildConfig` | Build configuration settings.         |                                             |

---

### Methods
| **Method**                          | **Parameters**                          | **Purpose**                                 |
|-------------------------------------|------------------------------------------|---------------------------------------------|
| `set_language(language: str)`       | `language`: Language code (e.g., `"en"`) | Sets the language for the documentation.    |
| `set_pcs(pcs: ProjectBuildConfig)`  | `pcs`: Project build config object       | Sets the project build configuration.       |
| `set_project_name(name: str)`       | `name`: Project name                     | Sets the name of the project.               |
| `add_project_additional_info(key: str, value: str)` | `key`: Metadata key, `value`: Metadata value | Adds additional project metadata.           |
| `add_ignore_file(pattern: str)`     | `pattern`: File pattern to ignore        | Adds a file pattern to the ignore list.     |
| `get_project_settings()`            | None                                     | Returns a `ProjectSettings` object with the current configuration. |

---
<a name="model-class"></a>
### `Model` Class (Synchronous Implementation)

#### Responsibility
Implements the `ParentModel` interface for synchronous response generation.

#### Key Methods
- **`generate_answer(with_history: bool, prompt: list[dict] | None)`**:
  - Returns a placeholder string `"answer"`.
- **`get_answer_without_history(prompt: list[dict])`**:
  - Calls `generate_answer` with `with_history=False` to generate a response without conversation context.
- **`get_answer(prompt: str)`**:
  - Adds the user's input to the history.
  - Calls `generate_answer` to get the model's response.
  - Adds the model's response to the history.
  - Returns the model's response.

---
<a name="asyncmodel-class"></a>
### `AsyncModel` Class (Asynchronous Implementation)

#### Responsibility
Implements the `ParentModel` interface for asynchronous response generation.

#### Key Methods
- **`generate_answer(with_history: bool, prompt: list[dict] | None)`**:
  - Returns a placeholder string `"answer"`.
- **`get_answer_without_history(prompt: list[dict])`**:
  - Calls `generate_answer` with `with_history=False` to generate a response without conversation context.
- **`get_answer(prompt: str)`**:
  - Adds the user's input to the history.
  - Calls `generate_answer` asynchronously to get the model's response.
  - Adds the model's response to the history.
  - Returns the model's response.

---
<a name="parentmodel-class"></a>
### `ParentModel` Class

#### Responsibility
Defines the core structure and behavior for AI models, including:
- Managing API keys and model selection.
- Providing abstract methods for response generation (`generate_answer`, `get_answer`, `get_answer_without_history`).

#### Key Attributes
- **`history`**: An instance of `History` to manage conversation context.
- **`api_keys`**: A list of API keys for authenticating with AI models.
- **`regen_models_name`**: A shuffled list of model names for fallback.
- **`current_model_index`**: Tracks the currently active model.
- **`current_key_index`**: Tracks the currently active API key.

#### Key Methods
- **`generate_answer(with_history: bool, prompt: list[dict] | None)`**:
  - Abstract method to generate an AI response.
  - Accepts a `with_history` flag to determine if conversation history should be included.
- **`get_answer_without_history(prompt: list[dict])`**:
  - Abstract method to generate a response without using conversation history.
- **`get_answer(prompt: str)`**:
  - Abstract method to generate a response using conversation history.

---
<a name="parentmodel-implementation"></a>
## `ParentModel` Implementation and Derived Classes

### Functional Role
The `ParentModel` class serves as an abstract base class for AI models, defining the foundational structure and behavior for generating responses. Derived classes, `Model` and `AsyncModel`, implement synchronous and asynchronous response generation, respectively. These models interact with a history object (`History`) to maintain conversational context and manage multiple API keys and models for fallback in case of failures.

---
<a name="history-class"></a>
### `History` Class

#### Responsibility
The `History` class maintains a record of the conversation context between the user and the AI model. It initializes with a system prompt and allows appending user and assistant messages.

#### Key Methods
- **`add_to_history(role: str, content: str)`**:
  - Appends a new message to the `history` list with the specified `role` (`system`, `user`, or `assistant`) and `content`.

#### Data Flow
| **Entity**   | **Type**     | **Role**                          | **Notes**                     |
|--------------|--------------|------------------------------------|-------------------------------|
| `role`       | `str`        | Specifies the role of the message | Can be `system`, `user`, or `assistant`. |
| `content`    | `str`        | The message content.              | Added to the history.         |
| `history`    | `list[dict]` | Stores the conversation history.  | Initialized with a system prompt. |

---
<a name="manager-class"></a>
## `Manager` Class

### Responsibility
The `Manager` class orchestrates the entire documentation generation process by integrating preprocessing, AI model-based generation, postprocessing, and caching mechanisms. It manages project-specific configurations, file handling, and progress tracking.

---

### Key Methods

####
<a name="manager-class-usage-and-methods"></a>

### Manager Class Usage and Available Methods

#### Usage:
The `Manager` class is instantiated and used to manage the process of generating documentation for a project. It integrates various components such as configuration, language models, embedding models, and progress tracking to automate the documentation generation process.

#### Constructor:
The `Manager` class is instantiated with the following parameters:
- `project_path`: The path to the project directory.
- `config`: A `Config` object that contains project-specific settings.
- `llm_model`: A language model object (e.g., `GPTModel`, `GPT4oModel`).
- `embedding_model`: An embedding model object (e.g., `Embedding`).
- `progress_bar`: A progress bar object (e.g., `ConsoleGtiHubProgress`).

#### Methods:
From the provided context, the following methods are used in the `Manager` class:
1. **`generate_code_file()`**: Generates a code file for the project.
2. **`generate_global_info(compress_power: int, is_reusable: bool)`**: Generates global information for the project. The `compress_power` parameter determines the level of compression, and `is_reusable` specifies whether the global file can be reused.
3. **`generete_doc_parts(max_symbols: int, with_global_file: bool)`**: Generates parts of the documentation. The `max_symbols` parameter specifies the maximum size of each documentation part, and `with_global_file` determines whether to include the global file in the documentation.
4. **`factory_generate_doc(factory: DocFactory, to_start: bool = False)`**: Uses the provided `DocFactory` to generate documentation. The `to_start` parameter specifies whether to add the generated documentation at the beginning.
5. **`order_doc()`**: Orders the documentation if required.
6. **`create_embedding_layer()`**: Creates an embedding layer for the documentation.
7. **`clear_cache()`**: Clears the cache used during the documentation generation process.
8. **`save()`**: Saves the generated documentation.

#### Example Usage:
```python
from autodocgenerator.manage import Manager
from autodocgenerator.engine.models.gpt_model import GPTModel
from autodocgenerator.postprocessor.embedding import Embedding
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.auto_runner.config_reader import Config

# Initialize configuration
config = Config()
config.set_project_name("MyProject").set_language("en")

# Initialize models
llm_model = GPTModel(["your_groq_api_key"], use_random=False)
embedding_model = Embedding("your_google_embedding_api_key")

# Initialize progress bar
progress_bar = ConsoleGtiHubProgress()

# Create Manager instance
manager = Manager(
    project_path="path/to/your/project",
    config=config,
    llm_model=llm_model,
    embedding_model=embedding_model,
    progress_bar=progress_bar
)

# Generate code file
manager.generate_code_file()

# Generate global information
manager.generate_global_info(compress_power=4, is_reusable=True)

# Generate documentation parts
manager.generete_doc_parts(max_symbols=5000, with_global_file=True)

# Generate documentation using a custom factory
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.factory.modules.intro import IntroText, IntroLinks

custom_modules = [IntroText(), IntroLinks()]
manager.factory_generate_doc(DocFactory(*custom_modules))

# Order the documentation
manager.order_doc()

# Create embedding layer
manager.create_embedding_layer()

# Clear cache
manager.clear_cache()

# Save the generated documentation
manager.save()
```

This example demonstrates how to initialize the `Manager` class, configure it with the necessary components, and use its methods to generate and save documentation.
<a name="codemix-class"></a>
## `CodeMix` Class

This class handles the generation of a repository's content structure while respecting ignore patterns.

### Functional Role
- Recursively traverses a directory to build a textual representation of its structure.
- Excludes files and directories matching specified ignore patterns.

### Key Methods

#### `should_ignore`
- Determines if a given path should be ignored based on the ignore patterns.

#### `build_repo_content`
- Builds a detailed textual representation of the repository's structure and content.

### Inputs and Outputs

| **Entity**         | **Type**       | **Role**                                    | **Notes**                              |
|--------------------|----------------|---------------------------------------------|----------------------------------------|
| `root_dir`         | `str`          | Root directory of the repository.           | Defaults to the current directory.     |
| `ignore_patterns`  | `list[str]`    | List of patterns to ignore.                 | Defaults to a predefined list.         |
| **Returns**        | `str`          | Textual representation of the repository.   | Includes structure and file contents.  |

---

### Critical Notes
> - The `split_text_by_anchors` function assumes that the number of anchor links matches the number of text chunks. If this assumption is violated, an exception is raised.
> - The `get_order` function relies on the AI model's ability to correctly interpret and sort the titles. Ensure the model is properly trained for this task.
> - The `CodeMix` class may encounter errors when reading files. These errors are logged but do not interrupt the process.
<a name="compressor-module"></a>
## `compressor.py` Module

This module provides functionality to compress large datasets into smaller, summarized representations using AI models. It includes methods for compressing individual data strings, comparing compressed data, and iteratively reducing multiple data chunks into a single compressed output.

---

### Functional Role
- **`compress`**: Compresses a single data string using an AI model and project-specific settings.
- **`compress_and_compare`**: Compresses multiple data strings and combines them into fewer chunks based on a specified compression power.
- **`compress_to_one`**: Iteratively compresses a list of data strings until only one compressed string remains.

---

### Key Methods
<a name="compress-method"></a>
#### `compress`

This method compresses a single data string using an AI model and project settings.

**Logic Flow**:
1. Constructs a prompt with:
   - Project-specific settings (`project_settings.prompt`).
   - A base compression text (`get_BASE_COMPRESS_TEXT`).
   - The input data.
2. Sends the prompt to the AI model using the `get_answer_without_history` method.
3. Returns the AI-generated compressed output.

**Inputs and Outputs**:

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `data`              | `str`          | The input data to be compressed.            | Large text data to be summarized.      |
| `project_settings`  | `ProjectSettings` | Contains project-specific settings and prompts. | Includes project name and metadata.    |
| `model`             | `Model`        | AI model used for compression.              | Instance of the `Model` class.         |
| `compress_power`    | `int`          | Determines the compression level.           | Affects the base compression text.     |
| **Returns**         | `str`          | Compressed version of the input data.       | AI-generated summary.                  |

---
<a name="compress-and-compare-method"></a>
#### `compress_and_compare`

This method compresses multiple data strings and combines them into fewer chunks based on a specified compression power.

**Logic Flow**:
1. Initializes an empty list to store compressed data chunks.
2. Creates a progress bar to track the compression process.
3. Iterates through the input data:
   - Divides the data into groups based on `compress_power`.
   - Compresses each data string using the `compress` method.
   - Appends the compressed output to the corresponding chunk.
4. Updates the progress bar after processing each data string.
5. Removes the progress bar after completion.
6. Returns the list of compressed data chunks.

**Inputs and Outputs**:

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `data`              | `list[str]`    | List of data strings to be compressed.      | Each string represents a data chunk.   |
| `model`             | `Model`        | AI model used for compression.              | Instance of the `Model` class.         |
| `project_settings`  | `ProjectSettings` | Contains project-specific settings and prompts. | Includes project name and metadata.    |
| `compress_power`    | `int`          | Determines the number of data strings to combine. | Defaults to 4.                         |
| `progress_bar`      | `BaseProgress` | Progress bar for tracking the process.      | Defaults to a new `BaseProgress` instance. |
| **Returns**         | `list[str]`    | List of compressed data chunks.             | Each chunk is a summarized representation. |

---
<a name="compress-to-one-method"></a>
#### `compress_to_one`

This method iteratively compresses a list of data strings until only one compressed string remains.

**Logic Flow**:
1. Initializes a counter for the number of iterations.
2. Repeatedly compresses the data using `compress_and_compare`:
   - Adjusts the compression power if the remaining data size is smaller than the default compression power.
   - Updates the data list with the compressed output.
3. Returns the final compressed string.

**Inputs and Outputs**:

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `data`              | `list[str]`    | List of data strings to be compressed.      | Each string represents a data chunk.   |
| `model`             | `Model`        | AI model used for compression.              | Instance of the `Model` class.         |
| `project_settings`  | `ProjectSettings` | Contains project-specific settings and prompts. | Includes project name and metadata.    |
| `compress_power`    | `int`          | Determines the number of data strings to combine. | Defaults to 4.                         |
| `progress_bar`      | `BaseProgress` | Progress bar for tracking the process.      | Defaults to a new `BaseProgress` instance. |
| **Returns**         | `str`          | Final compressed string.                    | Single summarized representation.      |

---
<a name="model-exhausted-exception"></a>
## `ModelExhaustedException`: Custom Exception

### Purpose
The `ModelExhaustedException` is raised when all available AI models have been exhausted and no further processing can occur.

---

### Attributes
This exception does not define any additional attributes.

---

### Usage
This exception is used in the AI model selection logic to handle cases where all available models fail or are unavailable. It ensures that the system can gracefully handle such scenarios.
<a name="gpt-models"></a>
## GPT Models: `GPT4oModel` and `GPTModel`

This file defines two classes, `GPT4oModel` and `GPTModel`, which extend the `Model` base class. These classes are responsible for generating AI-based responses using different GPT models (`GPT-4o`, `GPT-OSS`, and others). They handle API key management, model selection, error handling, and response generation.

---
<a name="gpt-model"></a>
### `GPTModel`

#### Functional Role
The `GPTModel` class is designed to interact with Groq's GPT-OSS models. It shares a similar structure and functionality with `GPT4oModel` but uses the `Groq` client for API communication.

#### Key Methods

#####
<a name="gpt-init"></a> `__init__`
Initializes the `GPTModel` with the following parameters:
- **API Keys**: A list of keys (`GROQ_API_KEYS`) for authenticating with the Groq API.
- **History**: A `History` object to manage conversation context.
- **Model List**: A list of model names, with `openai/gpt-oss-120b` as the default.
- **Randomization**: A flag (`use_random`) to determine if models should be selected randomly.

#####
<a name="gpt-generate-answer"></a> `generate_answer`
Generates a response from the AI model. The method supports both historical context and standalone prompts.

1. **Logging**: Logs the start of the response generation process.
2. **Message Preparation**:
   - If `with_history` is `True`, uses the conversation history (`self.history.history`).
   - If `prompt` is provided, uses it as the input.
3. **Model Selection**:
   - Iterates through the available models (`regen_models_name`).
   - If a model fails, logs the error and switches to the next API key or model.
   - If all models fail, raises `ModelExhaustedException`.
4. **Response Generation**:
   - Calls `Groq.chat.completions.create` with the prepared messages and model parameters.
   - Extracts the response content from the API's output.
5. **Logging and Return**:
   - Logs the generated response and the model used.
   - Returns the cleaned response.

---
<a name="gpt4o-model"></a>
### `GPT4oModel`

#### Functional Role
The `GPT4oModel` class is designed to interact with OpenAI's GPT-4o and related models via the `OpenAI` client. It manages API keys, model selection, and response generation, ensuring robust error handling and logging.

#### Key Methods

#####
<a name="gpt4o-init"></a> `__init__`
Initializes the `GPT4oModel` with the following parameters:
- **API Keys**: A list of keys (`GROQ_API_KEYS`) for authenticating with the OpenAI API.
- **History**: A `History` object to manage conversation context.
- **Model List**: A list of model names, with `openai/gpt-4o` as the default.
- **Randomization**: A flag (`use_random`) to determine if models should be selected randomly.

#####
<a name="gpt4o-generate-answer"></a> `generate_answer`
Generates a response from the AI model. The method supports both historical context and standalone prompts.

1. **Logging**: Logs the start of the response generation process.
2. **Message Preparation**:
   - If `with_history` is `True`, uses the conversation history (`self.history.history`).
   - If `prompt` is provided, uses it as the input.
3. **Model Selection**:
   - Iterates through the available models (`regen_models_name`).
   - If a model fails, logs the error and switches to the next API key or model.
   - If all models fail, raises `ModelExhaustedException`.
4. **Response Generation**:
   - Calls `OpenAI.chat.completions.create` with the prepared messages and model parameters.
   - Extracts the response content from the API's output.
5. **Logging and Return**:
   - Logs the generated response and the model used.
   - Returns the cleaned response.

---
<a name="azure-model-class"></a>
## `AzureModel` Class: AI Model Integration with Azure

### Purpose
The `AzureModel` class is a concrete implementation of the `Model` base class. It integrates with the Azure AI `ChatCompletionsClient` to generate AI-driven responses. This class manages API keys, handles model selection, and processes user prompts for generating responses.

---

### Attributes
| **Attribute**          | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `api_key`               | `list[str]`       | List of API keys for authenticating with Azure AI.                       | Defaults to `GROQ_API_KEYS`.                                              |
| `history`               | `History`         | Tracks conversation context for generating responses.                    | Defaults to an instance of `History`.                                     |
| `models_list`           | `list[str]`       | List of model names available for use.                                   | Defaults to `["deepseek/DeepSeek-V3-0324"]`.                              |
| `use_random`            | `bool`            | Whether to randomly select a model from the list.                        | Defaults to `True`.                                                       |
| `client`                | `ChatCompletionsClient` | Client for interacting with Azure AI's Chat Completions API.            | Initialized with the first API key and endpoint.                          |
| `logger`                | `BaseLogger`      | Logger instance for structured logging.                                  | Logs informational, warning, and error messages during execution.         |
| `regen_models_name`     | `list[str]`       | List of model names available for regeneration in case of failure.       | Derived from `models_list`.                                               |
| `current_model_index`   | `int`             | Index of the currently active model in `regen_models_name`.              | Tracks model switching during failures.                                   |
| `current_key_index`     | `int`             | Index of the currently active API key in `api_keys`.                     | Tracks API key switching during failures.                                 |

---

### Methods
| **Method**                          | **Parameters**                          | **Purpose**                                 |
|-------------------------------------|------------------------------------------|---------------------------------------------|
| `__init__(api_key, history, models_list, use_random)` | `api_key`: List of API keys, `history`: History object, `models_list`: List of models, `use_random`: Boolean flag | Initializes the AzureModel instance with API keys, history, and model list. |
| `_clean_deepseek_response(text: str)` | `text`: Raw response text from the model | Cleans the response by removing `<think>...</think>` blocks and extra spaces. |
| `_parse_prompt(data: list[dict[str, str]])` | `data`: List of dictionaries representing user/system messages | Converts raw input data into structured `UserMessage` and `SystemMessage` objects. |
| `generate_answer(with_history: bool = True, prompt: list[dict[str, str]] | None = None)` | `with_history`: Boolean to use conversation history, `prompt`: Optional prompt data | Generates an AI response using Azure AI's Chat Completions API. |

---
<a name="azure-model-initialization"></a>
## Initialization: `__init__`

### Purpose
The `__init__` method initializes the `AzureModel` instance with API keys, conversation history, and a list of models. It also sets up the `ChatCompletionsClient` for interacting with Azure AI.

### Parameters
| **Parameter**          | **Type**          | **Role**                                                                 | **Notes**                                                                 |
|-------------------------|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| `api_key`               | `list[str]`       | List of API keys for authenticating with Azure AI.                       | Defaults to `GROQ_API_KEYS`.                                              |
| `history`               | `History`         | Tracks conversation context for generating responses.                    | Defaults to an instance of `History`.                                     |
| `models_list`           | `list[str]`       | List of model names available for use.                                   | Defaults to `["deepseek/DeepSeek-V3-0324"]`.                              |
| `use_random`            | `bool`            | Whether to randomly select a model from the list.                        | Defaults to `True`.                                                       |

---
<a name="logging-system"></a>
## Logging System Implementation

### Functional Role
The logging system is designed to provide structured, hierarchical logging for the **Auto Doc Generator** project. It supports multiple logging levels (e.g., `INFO`, `WARNING`, `ERROR`) and allows logs to be directed to the console or written to files.

---

### Key Classes and Methods

#### `BaseLog` Class
- Represents a single log entry with a message and a logging level.
- Provides a timestamped prefix for all log messages.

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `message`           | `str`          | Log message content.                        | Required parameter.                    |
| `level`             | `int`          | Log severity level.                         | Defaults to `0`.                       |
| `_log_prefix`       | `str` (property) | Timestamp prefix for log messages.         | Uses the current system time.          |

##### Methods:
- **`format()`**: Returns the formatted log message as a string.

---

#### `ErrorLog`, `WarningLog`, and `InfoLog` Classes
- Subclasses of `BaseLog` that define specific log levels.
- Override the `format()` method to prepend the appropriate log level (`[ERROR]`, `[WARNING]`, `[INFO]`).

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `format()`          | `str`          | Formats the log message with level and time.| Overrides `BaseLog.format()`.          |

---

#### `BaseLoggerTemplate` Class
- Abstract base class for logging systems.
- Defines the `log()` and `global_log()` methods for logging messages.

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `log_level`         | `int`          | Minimum log level to display.               | Defaults to `-1` (log everything).     |

##### Methods:
- **`log(log: BaseLog)`**: Logs a message to the desired output (e.g., console or file).
- **`global_log(log: BaseLog)`**: Filters logs based on the `log_level` and delegates to `log()`.

---

#### `FileLoggerTemplate` Class
- Subclass of `BaseLoggerTemplate` that writes logs to a file.

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `file_path`         | `str`          | Path to the log file.                       | Required parameter.                    |

##### Methods:
- **`log(log: BaseLog)`**: Appends the formatted log message to the specified file.

---

#### `BaseLogger` Singleton Class
- Manages a single instance of the logger.
- Allows dynamic configuration of the logging backend (e.g., console or file).

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `logger_template`   | `BaseLoggerTemplate` | Current logging backend.                  | Configurable via `set_logger()`.       |

##### Methods:
- **`set_logger(logger: BaseLoggerTemplate)`**: Sets the active logger backend.
- **`log(log: BaseLog)`**: Delegates the log entry to the active logger backend.

---

### Critical Notes
> - The `BaseLogger` class implements the Singleton pattern to ensure a single instance of the logger is used throughout the application.
> - The `FileLoggerTemplate` enables persistent logging by writing log messages to a file, while `BaseLoggerTemplate` handles console logging.
> - The `log_level` in `BaseLoggerTemplate` and its subclasses allows filtering of log messages based on their severity.

---
<a name="progress-system"></a>
## Progress Tracking System Implementation

### Functional Role
The progress tracking system provides real-time feedback on the documentation generation process. It supports both console-based and rich progress bar-based implementations.

---

### Key Classes and Methods

#### `BaseProgress` Class
- Abstract base class for progress tracking.
- Defines the interface for managing subtasks and updating progress.

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `create_new_subtask`| `method`       | Creates a new subtask with a name and length.| Abstract method.                       |
| `update_task`       | `method`       | Updates the progress of the current task.   | Abstract method.                       |
| `remove_subtask`    | `method`       | Removes the current subtask.                | Abstract method.                       |

---

#### `LibProgress` Class
- Subclass of `BaseProgress` that uses the `rich.progress` library for visual progress bars.

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `progress`          | `Progress`     | Rich progress bar instance.                 | Required for visual feedback.          |
| `_base_task`        | `Task`         | General progress task.                      | Tracks overall progress.               |
| `_cur_sub_task`     | `Task` or `None`| Current subtask being tracked.             | Optional parameter.                    |

##### Methods:
- **`create_new_subtask(name, total_len)`**: Adds a new subtask to the progress bar.
- **`update_task()`**: Updates the progress of the current task or subtask.
- **`remove_subtask()`**: Removes the current subtask.

---

#### `ConsoleTask` Class
- Represents a single console-based task with progress tracking.

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `name`              | `str`          | Name of the task.                           | Required parameter.                    |
| `total_len`         | `int`          | Total length of the task.                   | Required parameter.                    |

##### Methods:
- **`start_task()`**: Initializes the task and prints a starting message.
- **`progress()`**: Updates the task's progress and prints the percentage completed.

---

#### `ConsoleGtiHubProgress` Class
- Subclass of `BaseProgress` that uses `ConsoleTask` for progress tracking in the console.

| **Entity**          | **Type**       | **Role**                                    | **Notes**                              |
|---------------------|----------------|---------------------------------------------|----------------------------------------|
| `curr_task`         | `ConsoleTask` or `None` | Current subtask being tracked.         | Optional parameter.                    |
| `gen_task`          | `ConsoleTask`  | General progress task.                      | Tracks overall progress.               |

##### Methods:
- **`create_new_subtask(name, total_len)`**: Creates a new console-based subtask.
- **`update_task()`**: Updates the progress of the current task or subtask.
- **`remove_subtask()`**: Removes the current subtask.

---

### Critical Notes
> - The `LibProgress` class requires the `rich` library for rendering progress bars.
> - The `ConsoleGtiHubProgress` class provides a lightweight alternative for environments where `rich` is unavailable.
> - Both progress tracking implementations support subtasks, allowing granular tracking of the documentation generation process.

---
<a name="autodocgenerator-init"></a>
## `autodocgenerator/__init__.py` - Library Initialization and Logging Setup

This script initializes the **Auto Doc Generator (ADG)** library by displaying a welcome message and setting up the logging system.

### Functional Responsibilities
1. **Welcome Message**: Displays an ASCII art logo and a status message indicating the library is ready for use.
2. **Logging Initialization**: Sets up a base logger using the `BaseLogger` and `BaseLoggerTemplate` classes from the `ui.logging` module.

### Key Components
#### `_print_welcome`
This function prints an ASCII art logo and a status message to the console.

**Logic Flow**:
1. Defines ANSI escape codes for text formatting (`BLUE`, `BOLD`, `CYAN`, `RESET`).
2. Constructs an ASCII art logo using the defined colors and formatting.
3. Prints the logo and a status message indicating the library version and readiness.

#### Logging Setup
- **`BaseLogger`**: The main logger instance for the library.
- **`BaseLoggerTemplate`**: Template used to configure the logger's output format.
- The logger is initialized and configured immediately upon import of the module.

---
