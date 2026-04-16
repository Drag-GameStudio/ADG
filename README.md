
### 🚀 Powered by ADG System
The original version of this document offers a superior layout and faster navigation. 
**Check it out here:** [Full Documentation Interface](https://draggame-adg-frontend.hf.space/docs/adg_doc_b5537f9587545d8238d33b840c30f58b)
---

# Project Overview: Auto Doc Generator

## Project Title:
**Auto Doc Generator**

---

## Project Goal:
The **Auto Doc Generator** is designed to automate the creation of comprehensive project documentation by analyzing codebases, extracting relevant information, and generating structured documentation using AI models. This tool addresses the common challenge of maintaining up-to-date and detailed documentation for software projects, streamlining the process and reducing manual effort for developers and technical writers.

---

## Core Logic & Principles:
The **Auto Doc Generator** operates on a layered architecture, with each layer contributing to a specific aspect of the documentation generation process. The core logic is as follows:

1. **Initialization**: The `Manager` component orchestrates the workflow, initializing core components such as configuration management, logging, progress tracking, and folder structures. It ensures that all necessary resources are prepared before processing begins.

2. **Codebase Analysis**: The `CodeMix` module aggregates the content of the repository into a unified structure, filtering out unnecessary files based on predefined ignore patterns.

3. **Documentation Generation**:
   - The `DocFactory` module uses a modular approach to generate documentation. It employs predefined templates and modules, such as `IntroLinks` and `IntroText`, to create structured and context-aware documentation.
   - The `GPTModel` leverages AI to analyze code and generate descriptive text, summaries, and introductions.

4. **Postprocessing**: The `Embedding` module creates embeddings for document sections, enabling semantic sorting and organization. Postprocessing utilities refine the documentation by sorting, splitting, and compressing text.

5. **Cache and Persistence**: The system uses caching mechanisms to store intermediate states, allowing for efficient reprocessing and incremental updates. The `Manager` component handles file management, cache settings, and persistence.

6. **Custom Logic**: The tool includes specialized logic for extracting and summarizing HTML links, generating global introductions, and creating tailored descriptions based on specific contexts.

7. **Error Handling and Constraints**: The system incorporates robust error handling for embedding failures, file reading issues, and token limits. It also filters files based on project-specific ignore patterns.

8. **Key Algorithms**:
   - **Semantic Sorting**: Orders document sections based on semantic relevance using AI-generated prompts.
   - **Compression**: Reduces large text data into concise summaries through iterative compression.
   - **Vector Operations**: Sorts and compares vectors for efficient organization of content.

By combining these components, the **Auto Doc Generator** delivers a scalable, efficient, and intelligent solution for generating high-quality documentation.

---

## Key Features:
- **Automated Codebase Analysis**: Aggregates and processes project files while respecting ignore patterns.
- **AI-Powered Documentation**: Utilizes GPT-based models to generate descriptive text, summaries, and introductions.
- **Modular Documentation System**: Supports reusable and customizable documentation modules.
- **Semantic Sorting and Compression**: Organizes and condenses documentation content for clarity and conciseness.
- **HTML Link Extraction**: Summarizes and incorporates relevant links into the documentation.
- **Progress and Logging**: Tracks execution progress and logs errors or informational messages.
- **Cache Management**: Efficiently stores and retrieves intermediate states for faster processing.
- **Customizable Configurations**: Centralized settings for project-specific customization.
- **Error Handling**: Robust mechanisms to handle embedding failures, file reading errors, and token limits.

---

## Dependencies:
To run the **Auto Doc Generator**, the following libraries and tools are required:

1. **Python** (Version 3.x)
2. **AI Models**:
   - GPT-based models (e.g., GPT-4, Azure GPT)
   - Embedding models for vector operations
3. **Python Libraries**:
   - `regex` (for HTML link extraction)
   - `os` and `pathlib` (for file and folder management)
   - `json` (for configuration and cache handling)
   - `logging` (for progress and error tracking)
4. **Custom Modules**:
   - `CodeMix` for repository content aggregation
   - `DocFactory` for modular documentation generation
   - `Embedding` for embedding generation
5. **Token Limit Management**:
   - Supports models with token limits (e.g., AzureModel: 10,000 tokens, GPT4oModel: 16,384 tokens)

---

The **Auto Doc Generator** is a powerful tool for automating the documentation process, leveraging advanced AI capabilities and modular design principles. It is ideal for developers, technical writers, and organizations looking to streamline their documentation workflows and maintain high-quality project documentation.
## Executive Navigation Tree

### 📂 CI/CD & Workflow
- [GitHub Actions Setup](#github-actions-setup)
- [Install Scripts and GitHub Action Setup](#install-scripts-and-github-action-setup)
- [AutoDoc Workflow](#autodoc-workflow)
- [CI/CD Workflow](#cicd-workflow)
- [Reusable Workflow](#reusable-workflow)
- [Workflow Comparison](#workflow-comparison)
- [Key Points](#key-points)
- [Change Analysis](#change-analysis)
- [Task 1](#task-1)
- [Task 2](#task-2)

### 📄 Configuration & Core Files
- [AutoDocConfig.yml](#autodocconfig-yml)
- [AutoDocConfig Options](#autodocconfig-options)
- [Init.py](#init-py)
- [Check Git Status](#check-git-status)
- [Config Reader](#config-reader)
- [Post to Server](#post-to-server)
- [Gen Doc Function](#gen-doc-function)
- [Token Auth Main](#token-auth-main)
- [Config Management](#config-management)

### ⚙️ Azure Integration
- [Azure Model Class](#azure-model-class)
- [Azure Model Methods](#azure-model-methods)
- [Init Method](#init-method)
- [Clean DeepSeek Response](#clean-deepseek-response)
- [Parse Prompt](#parse-prompt)
- [Generate Answer](#generate-answer)
- [Parse Answer](#parse-answer)

### 📄 Models & Classes
- [ParentModel Class](#parentmodel-class)
- [Model Class](#model-class)
- [AsyncModel Class](#asyncmodel-class)
- [DocFactory Class](#docfactory-class)
- [BaseModule Class](#basemodule-class)
- [CustomModule Class](#custommodule-class)
- [CustomModuleWithoutContext Class](#custommodulewithoutcontext-class)
- [IntroLinks Class](#introlinks-class)
- [IntroText Class](#introtext-class)
- [Custom Intro Functions](#custom-intro-functions)

### 📂 Embedding & Sorting
- [Embedding Module](#embedding-module)
- [Get Len Btw Vectors](#get-len-btw-vectors)
- [Sort Vectors](#sort-vectors)
- [Embedding Class](#embedding-class)
- [Async Embedding Class](#async-embedding-class)
- [Sorting Module](#sorting-module)

### 📄 Code Mix & Compression
- [CodeMix Class](#codemix-class)
- [Have to Change](#have-to-change)
- [Should Ignore](#should-ignore)
- [Build Repo Content](#build-repo-content)
- [Ignore List](#ignore-list)
- [Compress Method](#compress-method)
- [Compress and Compare Method](#compress-and-compare-method)
- [Compress to One Method](#compress-to-one-method)

### ⚙️ Project Settings & Documentation
- [Project Settings Class](#project-settings-class)
- [Split Data Method](#split-data-method)
- [Write Docs by Parts Method](#write-docs-by-parts-method)
- [Gen Doc Parts Method](#gen-doc-parts-method)
- [Doc Schema](#doc-schema)
- [Base Logger](#base-logger)
- [Progress Management](#progress-management)

### 📄 Installation & Build Files
- [Install.sh](#install-sh)
- [PyProject.toml](#pyproject-toml)
- [Manager Class Description](#manager-class-description)
<a name="github-actions-setup"></a>
## GitHub Actions Workflow for Auto Doc Generator

This section provides a detailed breakdown of the GitHub Actions workflows defined in the repository. These workflows automate the Continuous Integration (CI), Continuous Deployment (CD), and documentation generation processes for the **Auto Doc Generator** project.

---
<a name="install-scripts-and-github-action-setup"></a> To install the workflow using the provided scripts and configure the GitHub Action with the required secret variable, follow these steps:

### Installation Instructions

1. **For PowerShell (Windows):**
   - Open a PowerShell terminal.
   - Execute the following command to download and run the installation script:
     ```powershell
     irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
     ```

2. **For Linux-based Systems:**
   - Open a terminal.
   - Execute the following command to download and run the installation script:
     ```bash
     curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
     ```

### GitHub Action Configuration

To ensure the workflow functions correctly, you need to add a secret variable to your GitHub repository:

1. Navigate to your repository on GitHub.
2. Go to **Settings** > **Secrets and variables** > **Actions**.
3. Click on **New repository secret**.
4. Set the name of the secret as `GROCK_API_KEY`.
5. Retrieve your API key from the documentation and enter it as the value for the secret. Refer to the official documentation for obtaining the API key.

By following these steps, the installation scripts will configure the workflow, and the GitHub Action will have access to the required API key for proper operation.
<a name="autodoc-workflow"></a>
### AutoDoc Workflow (`.github/workflows/autodoc.yml`)

This workflow is triggered on:
- **Push events** to the `main` branch.
- **Manual dispatch** via the GitHub Actions interface.

#### Workflow Logic:
- **Job Name:** `run`
- **Permissions:** Grants write access to repository contents.
- **Reusable Workflow:** Calls the reusable workflow defined in `.github/workflows/reuseble_agd.yml` to generate documentation.
- **Secrets:**
  - `ADG_API_TOKEN`: Token required for authentication with the Auto Doc Generator API.

---
<a name="cicd-workflow"></a>
### CI/CD Workflow (`.github/workflows/main.yml`)

This workflow is triggered on:
- **Push events** to the `main` branch, specifically for changes to `pyproject.toml`.
- **Pull requests** targeting the `main` branch, specifically for changes to `pyproject.toml`.

#### Workflow Logic:
- **Job Name:** `build`
- **Runs On:** `ubuntu-latest`
- **Steps:**
  1. **Checkout Code:** Uses the `actions/checkout@v4` action to clone the repository.
  2. **Set Up Python:** Uses the `actions/setup-python@v5` action to configure Python 3.12.
  3. **Install Poetry:** Installs the Poetry dependency manager using `pip install poetry`.
  4. **Install Dependencies:** Installs project dependencies using `poetry install`.
  5. **Publish Library:** Publishes the library to PyPI using `poetry publish --build`. Requires the `PYPI_TOKEN` secret for authentication.

---
<a name="reusable-workflow"></a>
### Reusable Workflow for Documentation Generation (`.github/workflows/reuseble_agd.yml`)

This workflow is designed to be reusable and is invoked by other workflows (e.g., `autodoc.yml`) for generating documentation.

#### Workflow Logic:
- **Job Name:** `build`
- **Runs On:** `ubuntu-latest`
- **Permissions:** Grants write access to repository contents.
- **Steps:**
  1. **Checkout Code:** Clones the repository with `fetch-depth: 0` to ensure all history is available.
  2. **Set Up Python:** Configures Python 3.12 using `actions/setup-python@v5`.
  3. **Install AutoDoc Generator:** Installs the `autodocgenerator` package using `pip`.
  4. **Retrieve API Keys:** Runs `token_auth.py` to fetch API keys required for documentation generation.
     - Environment variables:
       - `ADG_API_TOKEN`: Authentication token for the Auto Doc Generator API.
       - `DEFAULT_SERVER_URL`: Base URL for the API.
       - Other environment variables for debugging and terminal output formatting.
  5. **Debug API Keys:** Outputs environment variables to verify API key presence.
  6. **Run Documentation Generation:** Executes `run_file.py` to generate documentation.
  7. **Post to Server:** If the previous step does not set `skip_next` to `true`, runs `post_to_server.py` to upload the generated documentation to the server.
  8. **Update README:** Copies the generated documentation (`output_doc.md`) to `README.md`.
  9. **Save Logs:** Copies logs from `.auto_doc_cache/report.txt` to `agd_report.txt`.
  10. **Commit and Push Changes:** Commits and pushes updates to `README.md`, `.auto_doc_cache_file.json`, and `agd_report.txt` (if they exist).

---
<a name="workflow-comparison"></a>
### Workflow Comparison

| Workflow Name       | Trigger Events                  | Purpose                          | Key Steps                                                                 |
|---------------------|---------------------------------|----------------------------------|--------------------------------------------------------------------------|
| **AutoDoc**         | Push to `main`, manual dispatch | Generate documentation          | Calls reusable workflow `reuseble_agd.yml`.                              |
| **CI/CD Workflow**  | Push/PR for `pyproject.toml`    | Build and publish the library   | Installs dependencies, builds, and publishes the library to PyPI.        |
| **Reusable Workflow** | Workflow call                 | Documentation generation logic  | Installs AutoDoc Generator, generates documentation, and pushes updates. |

---
<a name="key-points"></a>
### Key Points and Considerations

1. **Secrets Management:**
   - The workflows rely on the `ADG_API_TOKEN` secret for authentication with the Auto Doc Generator API.
   - The `PYPI_TOKEN` secret is used for publishing the library to PyPI.

2. **Reusable Workflow:**
   - The `reuseble_agd.yml` workflow centralizes the documentation generation logic, making it reusable across multiple workflows.

3. **Environment Variables:**
   - The reusable workflow uses several environment variables to configure the Auto Doc Generator and its API interactions.

4. **Automation:**
   - The workflows automate the process of generating documentation, publishing the library, and updating the repository with the latest documentation and logs.

5. **Error Handling:**
   - The reusable workflow includes error handling for missing logs and skips certain steps if the `skip_next` output is set to `true`.

This setup ensures a streamlined and automated process for both CI/CD and documentation generation, aligning with the goals of the **Auto Doc Generator** project.
<a name="change-analysis"></a>
## Change Analysis and Documentation Update Recommendations

### Analysis of Changes

| File Path                                         | Change Type | Number of Changes | Impact on Documentation | Impact on Global Info |
|--------------------------------------------------|-------------|--------------------|--------------------------|------------------------|
| `.auto_doc_cache_file.json`                      | Modified    | 2                  | None                     | None                  |
| `.github/workflows/reuseble_agd.yml`             | Added       | 2                  | None                     | None                  |
| `agd_report.txt`                                 | Deleted     | 4                  | None                     | None                  |
| `autodocgenerator/auto_runner/check_git_status.py` | Modified    | 4                  | None                     | None                  |
| `autodocgenerator/auto_runner/run_file.py`       | Modified    | 11                 | **Update Required**      | None                  |
| `autodocgenerator/config/config.py`             | Modified    | 5                  | Minor Update             | None                  |
| `autodocgenerator/config/env_config.py`         | Added       | 38                 | **Update Required**      | None                  |
| `autodocgenerator/engine/config/config.py`      | Deleted     | 17                 | **Update Required**      | None                  |
| `autodocgenerator/postprocessor/embedding.py`   | Modified    | 4                  | None                     | None                  |
| `poetry.lock`                                   | Modified    | 28                 | None                     | None                  |
| `pyproject.toml`                                | Modified    | 3                  | None                     | None                  |

---

### Recommendations

####
<a name="task-1"></a> Task 1: Rewrite Documentation (Existing Docs)
- **Reasoning**: 
  - The addition of `env_config.py` introduces a new environment-specific configuration file, which requires documentation to explain its purpose, structure, and usage.
  - Changes to `run_file.py` may impact the workflow or usage instructions, necessitating updates to reflect the new behavior.
  - The deletion of `engine/config/config.py` suggests that configuration logic has been refactored or relocated, which should be clarified in the documentation.
- **Decision**: `true`

####
<a name="task-2"></a> Task 2: Rewrite Global Info
- **Reasoning**:
  - None of the changes introduce a new core feature, architectural component, or paradigm shift.
  - The addition of `env_config.py` is an incremental update and does not alter the high-level architecture or logic described in the Global Info.
- **Decision**: `false`

---

### Final Output
`true|false`
<a name="autodocconfig-yml"></a>
## Configuration File: `autodocconfig.yml`

### Purpose
The `autodocconfig.yml` file defines the configuration settings for the **Auto Doc Generator** project. It specifies project metadata, file ignore patterns, build settings, structure settings, and additional project-specific information. This file is essential for customizing the behavior of the documentation generation process.

### Configuration Parameters

#### Project Metadata
| Parameter       | Type   | Description                                                                 |
|-----------------|--------|-----------------------------------------------------------------------------|
| `project_name`  | String | The name of the project. In this case, it is `"Auto Doc Generator"`.        |
| `language`      | String | The language used for the documentation. Set to `"en"` for English.         |

#### File Ignore Patterns
The `ignore_files` section lists files and directories that should be excluded during the documentation generation process. This includes:
- **Build artifacts:** `dist`
- **Python bytecode and cache files:** `*.pyc`, `*.pyo`, `*.pyd`, `__pycache__`, etc.
- **Environment and IDE settings:** `venv`, `.vscode`, `.idea`, etc.
- **Databases and binary data:** `*.sqlite3`, `*.db`, etc.
- **Logs and coverage reports:** `*.log`, `.coverage`, etc.
- **Version control and static assets:** `.git`, `migrations`, `static`, etc.
- **Miscellaneous files:** `*.pdb`, `*.md`

#### Build Settings
| Parameter           | Type    | Description                                                                 |
|---------------------|---------|-----------------------------------------------------------------------------|
| `save_logs`         | Boolean | Whether to save logs during the build process. Set to `false`.              |
| `log_level`         | Integer | The verbosity level of logs. Set to `2`.                                    |
| `threshold_changes` | Integer | The threshold for detecting significant changes. Set to `20000`.            |

#### Structure Settings
| Parameter             | Type    | Description                                                                 |
|-----------------------|---------|-----------------------------------------------------------------------------|
| `include_intro_links` | Boolean | Whether to include introductory links in the documentation. Set to `true`. |
| `include_intro_text`  | Boolean | Whether to include introductory text in the documentation. Set to `true`.  |
| `include_order`       | Boolean | Whether to include ordering of sections in the documentation. Set to `true`.|
| `use_global_file`     | Boolean | Whether to use a global file for documentation. Set to `true`.             |
| `max_doc_part_size`   | Integer | Maximum size of each documentation part. Set to `4000`.                    |

#### Additional Information
| Parameter               | Type    | Description                                                                 |
|-------------------------|---------|-----------------------------------------------------------------------------|
| `global idea`           | String  | The overarching purpose of the project: "This project was created to help developers make documentations for their projects." |

#### Custom Descriptions
This section provides additional context or instructions for specific use cases:
1. **Installation Workflow:** Explains how to install the project using `install.ps1` (PowerShell) or `install.sh` (Linux-based systems). Includes commands and notes about setting the `GROCK_API_KEY` GitHub secret variable.
2. **`autodocconfig.yml` File:** Describes how to write and configure the `autodocconfig.yml` file, including available options.
3. **`Manager` Class:** Explains the methods available in the `Manager` class, with code examples for better understanding.

---
<a name="autodocconfig-options"></a>
The `autodocconfig.yml` file contains various configuration options that control the behavior of the Auto Doc Generator project. Below is an explanation of its structure and the available options:

#### Structure and Options:

1. **`project_name`**:
   - Specifies the name of the project.
   - Example: `"Auto Doc Generator"`

2. **`language`**:
   - Defines the language for the documentation.
   - Example: `"en"`

3. **`ignore_files`**:
   - A list of file patterns or directories to exclude from the documentation process.
   - Examples:
     - `"dist"`: Excludes the `dist` directory.
     - `"*.pyc"`: Excludes Python bytecode files.
     - `"__pycache__"`: Excludes Python cache directories.
     - `"venv"`: Excludes virtual environment directories.

4. **`build_settings`**:
   - Controls settings related to the build process.
   - Sub-options:
     - **`save_logs`**: Boolean flag to determine whether logs should be saved.
       - Example: `false`
     - **`log_level`**: Specifies the verbosity level of logs (e.g., `2`).
     - **`threshold_changes`**: Sets the maximum number of changes before triggering specific actions.
       - Example: `20000`

5. **`structure_settings`**:
   - Configures the structure of the generated documentation.
   - Sub-options:
     - **`include_intro_links`**: Boolean flag to include introductory links in the documentation.
       - Example: `true`
     - **`include_intro_text`**: Boolean flag to include introductory text.
       - Example: `true`
     - **`include_order`**: Boolean flag to include order information.
       - Example: `true`
     - **`use_global_file`**: Boolean flag to use a global file for documentation.
       - Example: `true`
     - **`max_doc_part_size`**: Specifies the maximum size of each documentation part.
       - Example: `4000`

6. **`project_additional_info`**:
   - Provides general information about the project.
   - Example: `"This project was created to help developers make documentations for them projects"`

7. **`custom_descriptions`**:
   - A list of custom descriptions or instructions to include in the documentation.
   - Examples:
     - `"explain how install workflow with install.ps1 and install.sh scripts for install you should use links irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex for powershell and curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash for linux based systems and also you have to add secret variable to git hub action GROCK_API_KEY with your api key from grock docs grockdocs.com to make it work"`
     - `"explain how to write autodocconfig.yml file what options are available"`
     - `"explain how to use Manager class and what methods are available. Provide code examples for better understanding"`

#### Example Configuration:
```yaml
project_name: "Auto Doc Generator"
language: "en"

ignore_files:
  - "dist"
  - "*.pyc"
  - "__pycache__"
  - "venv"

build_settings:
  save_logs: false
  log_level: 2
  threshold_changes: 20000

structure_settings:
  include_intro_links: true
  include_intro_text: true
  include_order: true
  use_global_file: true
  max_doc_part_size: 4000

project_additional_info:
  global idea: "This project was created to help developers make documentations for them projects"

custom_descriptions:
  - "explain how install workflow with install.ps1 and install.sh scripts for install you should use links irm raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex for powershell and curl -sSL raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash for linux based systems and also you have to add secret variable to git hub action GROCK_API_KEY with your api key from grock docs grockdocs.com to make it work"
  - "explain how to write autodocconfig.yml file what options are available"
  - "explain how to use Manager class and what methods are available. Provide code examples for better understanding"
```
<a name="init-py"></a>
## Initialization Script: `autodocgenerator/__init__.py`

### Purpose
This script initializes the **Auto Doc Generator** library by setting up logging and displaying a welcome message.

### Functional Flow

#### `_print_welcome`
- **Description:** Displays an ASCII logo and a welcome message when the library is initialized.
- **Key Elements:**
  - **ASCII Logo:** A stylized representation of the project name.
  - **Status Message:** Indicates the library is ready to work, along with the current version (`V0.0.6`).

#### Logger Initialization
- **Description:** Initializes the `BaseLogger` with a default template (`BaseLoggerTemplate`) for tracking logs.
- **Key Components:**
  - `BaseLogger`: The core logging class.
  - `BaseLoggerTemplate`: The template used to format logs.
  - Log Types: Includes `InfoLog`, `ErrorLog`, and `WarningLog`.

---
<a name="check-git-status"></a>
## Git Status Checker: `autodocgenerator/auto_runner/check_git_status.py`

### Purpose
This module provides utilities to check the current Git repository status, detect changes, and determine whether documentation needs to be regenerated.

### Functional Flow

#### `get_diff_by_hash`
- **Description:** Retrieves the differences between a specific Git commit hash and the current `HEAD`, excluding markdown files.
- **Input:** 
  - `target_hash` (String): The Git commit hash to compare against.
- **Output:** 
  - A string containing the `git diff` output.
- **Error Handling:** If the `git diff` command fails, an error message is printed, and `None` is returned.

#### `get_detailed_diff_stats`
- **Description:** Provides detailed statistics about file changes between a specific commit hash and the current `HEAD`.
- **Input:** 
  - `target_hash` (String): The Git commit hash to compare against.
- **Output:** 
  - A list of dictionaries, each containing:
    - `path`: File path.
    - `status`: Change type (`ADDED`, `DELETED`, `MODIFIED`).
    - `added`: Number of lines added.
    - `deleted`: Number of lines deleted.
    - `total_changes`: Total number of changes (added + deleted).

#### `get_git_revision_hash`
- **Description:** Retrieves the current Git commit hash (`HEAD`).
- **Output:** 
  - A string representing the current commit hash.

#### `check_git_status`
- **Description:** Checks the Git repository status and determines whether documentation needs to be regenerated.
- **Input:** 
  - `manager` (Manager): An instance of the `Manager` class.
- **Output:** 
  - An instance of `CheckGitStatusResultSchema` containing:
    - `need_to_remake` (Boolean): Indicates if documentation needs to be regenerated.
    - `remake_gl_file` (Boolean): Indicates if the global file needs to be regenerated.
- **Logic:**
  1. If the GitHub event is `workflow_dispatch` or no previous commit exists, the current commit hash is saved, and both flags are set to `True`.
  2. Otherwise, detailed file changes are retrieved using `get_detailed_diff_stats`.
  3. The `Manager.check_sense_changes` method evaluates the changes to determine if regeneration is required.

---

### Data Flow

| Entity                      | Type       | Role                                                                 |
|-----------------------------|------------|----------------------------------------------------------------------|
| `target_hash`               | String     | The Git commit hash to compare against.                              |
| `manager`                   | Manager    | Manages cache settings and checks for significant changes.           |
| `changes`                   | List[Dict] | List of file change details (path, status, added, deleted, changes). |
| `CheckGitStatusResultSchema`| Schema     | Contains flags for documentation regeneration.                       |

---

### Key Considerations
> - **Error Handling:** Ensure proper handling of `subprocess.CalledProcessError` to avoid crashes during Git operations.
> - **File Exclusion:** Markdown files (`*.md`) are excluded from Git diff operations.
> - **GitHub Workflow:** Special handling for `workflow_dispatch` events ensures proper initialization during manual workflows.
> - **Change Detection:** The `check_sense_changes` method is critical for determining whether the documentation requires updates.
<a name="config-reader"></a>
## Configuration Reader: `read_config`

### **Description**
The `read_config` function is responsible for parsing YAML configuration data and initializing the core configuration objects for the Auto Doc Generator system. It processes project-specific settings, custom module definitions, and structure settings to return a tuple of configuration objects.

---

### **Functionality**

#### `StructureSettings` Class
- **Purpose:** Defines the default structure settings for the documentation generation process.
- **Attributes:**
  - `include_intro_links` (Boolean): Whether to include introductory links in the documentation.
  - `include_order` (Boolean): Whether to include ordered sections in the documentation.
  - `use_global_file` (Boolean): Whether to use a global file for documentation.
  - `max_doc_part_size` (Integer): Maximum size (in characters) for each documentation part.
  - `include_intro_text` (Boolean): Whether to include introductory text in the documentation.
- **Method:**
  - `load_settings(data: dict[str, Any])`: Dynamically updates the structure settings based on the provided dictionary.

#### `read_config` Function
- **Purpose:** Reads and parses YAML configuration data to initialize the `Config`, `BaseModule` list, and `StructureSettings`.
- **Logic:**
  1. Parse the YAML data using `yaml.safe_load`.
  2. Initialize a `Config` object and set its attributes:
     - `language` (default: "en").
     - `project_name` and `project_additional_info`.
     - `build_settings` via the `ProjectBuildConfig` object.
     - `ignore_files` patterns.
  3. Create a list of `BaseModule` objects (`custom_modules`) based on the `custom_descriptions` field in the YAML data.
     - If the description starts with `%`, a `CustomModuleWithOutContext` is created.
     - Otherwise, a `CustomModule` is created.
  4. Initialize a `StructureSettings` object and update its attributes using the `structure_settings` field in the YAML data.
  5. Return a tuple containing the `Config` object, `custom_modules` list, and `StructureSettings` object.

---

### **Data Flow**

| Entity                  | Type                | Role                                                                 |
|-------------------------|---------------------|----------------------------------------------------------------------|
| `file_data`             | String             | YAML-formatted configuration data.                                  |
| `Config`                | Class Instance     | Stores global configuration settings for the project.               |
| `BaseModule`            | Abstract Class     | Represents modular components for documentation generation.         |
| `StructureSettings`     | Class Instance     | Stores structural settings for documentation generation.            |
| `ignore_files`          | List[String]       | Patterns of files to ignore during documentation generation.        |
| `custom_descriptions`   | List[String]       | Custom descriptions for documentation modules.                      |
| `structure_settings`    | Dict               | Dictionary of structure-related settings for documentation.         |

---

### **Key Considerations**
> - **Error Handling:** Ensure the input YAML data is well-formed to avoid parsing errors.
> - **Dynamic Configuration:** The `StructureSettings.load_settings` method allows dynamic updates to settings, ensuring flexibility.
> - **Custom Modules:** The function supports both context-aware (`CustomModule`) and context-free (`CustomModuleWithOutContext`) modules, providing adaptability for various documentation needs.

---
<a name="post-to-server"></a>
## Documentation Upload: `main`

### **Description**
The `main` function is responsible for uploading the generated documentation and cache data to a remote server. It also appends a footer with a link to the hosted documentation interface.

---

### **Functionality**

#### `main` Function
- **Purpose:** Handles the upload of documentation and cache data to a remote server and updates the output document with a footer.
- **Logic:**
  1. Retrieve the `ADG_API_TOKEN` and `DEFAULT_SERVER_URL` environment variables.
  2. Read the cache data from `.auto_doc_cache_file.json`.
  3. Send a POST request to the server with the cache data and authorization token.
  4. Parse the server response to retrieve the `doc_id`.
  5. Read the generated documentation content from `.auto_doc_cache/output_doc.md`.
  6. Append a footer with a link to the hosted documentation interface.
  7. Overwrite the `.auto_doc_cache/output_doc.md` file with the updated content.

---

### **Data Flow**

| Entity               | Type       | Role                                                                 |
|----------------------|------------|----------------------------------------------------------------------|
| `api_key`            | String     | API token for authenticating the request to the server.              |
| `default_server_url` | String     | Base URL of the remote server.                                       |
| `cache_data`         | String     | Content of the `.auto_doc_cache_file.json` file.                     |
| `output_doc_content` | String     | Content of the `.auto_doc_cache/output_doc.md` file.                 |
| `doc_id`             | String     | Unique identifier for the uploaded documentation on the server.      |

---

### **Key Considerations**
> - **Error Handling:** Use `result.raise_for_status()` to handle HTTP errors during the POST request.
> - **Environment Variables:** Ensure `ADG_API_TOKEN` and `DEFAULT_SERVER_URL` are set before running the script.
> - **File Overwriting:** The `.auto_doc_cache/output_doc.md` file is overwritten with the updated content, including the footer.
> - **Security:** Sensitive information, such as the API token, should be securely managed and not hardcoded.

---

### **Potential Enhancements**
1. **Error Logging:** Add detailed logging for failed HTTP requests and file operations.
2. **Environment Validation:** Validate the presence of required environment variables before proceeding.
3. **Retry Mechanism:** Implement a retry mechanism for the POST request in case of transient network issues.
<a name="gen-doc-function"></a>
## Documentation Generation Function: `gen_doc`

### **Description**
The `gen_doc` function is the core workflow for generating structured documentation for a project. It integrates multiple components, including configuration management, model initialization, embedding generation, and documentation creation. The function also handles change detection and optimizes the process by skipping redundant steps when possible.

---

### **Functionality**

#### `gen_doc` Function
- **Purpose:** Automates the process of generating structured documentation for a project by orchestrating various components and modules.
- **Logic:**
  1. **Model Initialization:**
     - Selects a language model (`sync_model`) based on the `env_config.type_of_model`.
     - Initializes the embedding model using `env_config.google_embedding_api_key`.
  2. **Manager Setup:**
     - Creates a `Manager` instance with the project path, configuration, models, and a progress bar.
  3. **Change Detection:**
     - Calls `check_git_status` to determine if documentation needs to be regenerated.
     - If no changes are detected, loads cached documentation and exits early.
  4. **Documentation Generation:**
     - Generates the code mix using `manager.generate_code_file`.
     - Optionally generates global information if `structure_settings.use_global_file` is enabled.
     - Splits the documentation into parts using `manager.generete_doc_parts`.
     - Uses `DocFactory` to generate documentation sections based on the provided custom modules.
  5. **Additional Modules:**
     - Adds introductory text and links if specified in `structure_settings`.
     - Processes these modules using `DocFactory`.
  6. **Postprocessing:**
     - Creates an embedding layer for the documentation.
     - Clears the cache and saves the final documentation.

---

### **Data Flow**

| Entity                  | Type             | Role                                                                 |
|-------------------------|------------------|----------------------------------------------------------------------|
| `project_path`          | String           | Path to the project directory.                                       |
| `config`                | `Config`         | Configuration object containing project-specific settings.           |
| `custom_modules`        | List[BaseModule] | List of custom modules for documentation generation.                 |
| `structure_settings`    | `StructureSettings` | Settings for structuring the documentation.                          |
| `sync_model`            | `Model`          | Language model used for text generation.                             |
| `embedding_model`       | `Embedding`      | Model used for generating embeddings for documentation sections.     |
| `manager`               | `Manager`        | Core orchestrator for the documentation generation process.          |
| `change_info`           | `CheckGitStatusResultSchema` | Object containing information about changes in the project.          |
| `output_doc`            | String           | The final generated documentation content.                           |

---

### **Key Considerations**
> - **Change Detection:** The function skips redundant operations if no significant changes are detected in the project files.
> - **Dynamic Configuration:** The `StructureSettings` object allows for flexible customization of the documentation structure.
> - **Error Handling:** The function gracefully exits if required environment variables or configurations are missing.
> - **Postprocessing:** Embedding generation and cache clearing ensure the documentation is optimized and up-to-date.

---

### **Potential Enhancements**
1. **Parallel Processing:** Optimize the documentation generation process by parallelizing tasks such as embedding creation and module processing.
2. **Enhanced Logging:** Add detailed logs for each step to improve debugging and monitoring.
3. **Customizable Models:** Allow users to define custom models and embedding strategies via configuration.
4. **Improved Change Detection:** Refine the `check_git_status` logic to handle edge cases and improve accuracy.

---
<a name="token-auth-main"></a>
## Token Authentication and Key Retrieval: `main`

### **Description**
The `main` function in `token_auth.py` is responsible for retrieving API keys from a remote server and storing them in the environment for subsequent use. This function is essential for securely managing authentication tokens required by the Auto Doc Generator.

---

### **Functionality**

#### `main` Function
- **Purpose:** Fetches API keys from a remote server and writes them to the environment for use in subsequent steps.
- **Logic:**
  1. Retrieve the `ADG_API_TOKEN` and `DEFAULT_SERVER_URL` environment variables.
  2. Validate the presence of the required environment variables.
  3. Send a GET request to the server to fetch API keys.
  4. Parse the server response and extract the `github_token` and `google_token`.
  5. Write the retrieved tokens to the `GITHUB_ENV` file or print them locally.

---

### **Data Flow**

| Entity               | Type   | Role                                                                 |
|----------------------|--------|----------------------------------------------------------------------|
| `api_key`            | String | API token for authenticating the request to the server.              |
| `default_server_url` | String | Base URL of the remote server.                                       |
| `url`                | String | Full URL for the API endpoint to fetch API keys.                     |
| `headers`            | Dict   | Headers for the HTTP request, including the authorization token.     |
| `response`           | Object | Server response object containing the API keys.                     |
| `github_token`       | String | GitHub token retrieved from the server response.                    |
| `google_token`       | String | Google embedding API token retrieved from the server response.       |
| `env_file`           | String | Path to the `GITHUB_ENV` file for storing environment variables.     |

---

### **Key Considerations**
> - **Error Handling:** Proper error messages and exceptions are raised for missing environment variables or failed API requests.
> - **Security:** API tokens are securely managed and not hardcoded in the script.
> - **Environment Variables:** The function ensures that required environment variables are set before proceeding.
> - **Server Response Validation:** Validates the server response to ensure successful retrieval of API keys.

---

### **Potential Enhancements**
1. **Retry Mechanism:** Add retries for the GET request to handle transient network issues.
2. **Enhanced Security:** Encrypt the API tokens before writing them to the environment file.
3. **Logging:** Implement detailed logging for debugging and monitoring API interactions.
4. **Dynamic Model Selection:** Allow the user to specify the model type dynamically based on the retrieved tokens.
<a name="config-management"></a>
## Configuration Management: `Config` and `EnvConfig`

### **Description**
The `Config` and `EnvConfig` classes are responsible for managing the configuration settings of the Auto Doc Generator. While `Config` handles project-specific configurations, `EnvConfig` focuses on environment variables and external dependencies. Together, they provide a structured and extensible way to manage both static and dynamic configurations.

---

### **Functionality**

#### `Config` Class
- **Purpose:** Manages project-specific configurations like ignored files, project metadata, and build settings.
- **Key Features:**
  1. **Ignore Files Management:** Maintains a list of file patterns to exclude during processing.
  2. **Language Settings:** Allows the specification of the project's language.
  3. **Project Metadata:** Stores the project name and additional information as key-value pairs.
  4. **Build Configuration:** Integrates with `ProjectBuildConfig` to manage build-specific settings like logging and change thresholds.
  5. **Project Settings Generation:** Converts project metadata into a `ProjectSettings` object for further processing.

#### `EnvConfig` Class
- **Purpose:** Handles environment variables and external API configurations using the `pydantic` library.
- **Key Features:**
  1. **API Key Management:** Retrieves and validates API keys from environment variables.
  2. **Model Type Normalization:** Ensures the model type is stored in lowercase for consistency.
  3. **Environment File Support:** Reads from a `.env` file and supports custom encoding.
  4. **Validation:** Ensures required environment variables are set and properly formatted.

---

### **Data Flow**

#### `Config` Class

| Entity                     | Type            | Role                                                                 |
|----------------------------|-----------------|----------------------------------------------------------------------|
| `ignore_files`             | List[str]       | Patterns of files to exclude from processing.                        |
| `language`                 | String          | Language setting for the project.                                    |
| `project_name`             | String          | Name of the project being documented.                                |
| `project_additional_info`  | Dict            | Additional metadata about the project.                               |
| `pbc`                      | ProjectBuildConfig | Build-specific configurations like logging and thresholds.          |

#### `EnvConfig` Class

| Entity                     | Type            | Role                                                                 |
|----------------------------|-----------------|----------------------------------------------------------------------|
| `models_api_keys`          | String/List[str]| API keys for external models, retrieved from environment variables.  |
| `type_of_model`            | String          | Specifies the type of model to use (e.g., "git").                    |
| `google_embedding_api_key` | String          | API key for Google Embedding services.                               |
| `github_event_name`        | String          | Name of the GitHub event triggering the process.                     |
| `output_github_file`       | String          | Path to the GitHub output file for storing results.                  |

---

### **Key Considerations**
> - **Extensibility:** Both classes are designed to be easily extended for additional configuration needs.
> - **Validation:** The use of `pydantic` ensures robust validation of environment variables in `EnvConfig`.
> - **Error Handling:** Proper error messages are raised for missing or improperly formatted environment variables.
> - **Security:** Sensitive data like API keys are managed via environment variables, reducing the risk of accidental exposure.

---

### **Potential Enhancements**
1. **Dynamic Ignore Patterns:** Allow dynamic updates to `ignore_files` based on project type or user input.
2. **Advanced Validation:** Add more granular validation for `project_additional_info` and `EnvConfig` fields.
3. **Logging Integration:** Integrate logging to track configuration loading and validation processes.
4. **Environment Variable Encryption:** Encrypt sensitive environment variables like API keys for added security.
5. **Default Fallbacks:** Provide default values for critical settings in case environment variables are missing.

---

### **Error Handling**

#### `ModelExhaustedException`
- **Purpose:** Raised when no usable models are available in the list of API keys.
- **Usage:** Ensures that the system gracefully handles scenarios where all models are exhausted, preventing unexpected crashes.
<a name="azure-model-class"></a>
## `AzureModel` Class: Azure-based AI Model Integration

The `AzureModel` class is a concrete implementation of the abstract `Model` class. It integrates with the Azure AI Inference service to generate responses to user prompts using AI models. This class manages API keys, model selection, and error handling to ensure robust and efficient communication with the Azure AI service.

---

### **Class Responsibilities**
1. **Azure AI Integration:** Connects to the Azure AI Inference service using the `ChatCompletionsClient` from the `azure.ai.inference` library.
2. **Model Management:** Handles multiple AI models with support for fallback mechanisms in case of failures.
3. **Prompt Parsing:** Converts input prompts into the format required by the Azure AI service.
4. **Response Cleaning:** Processes the AI-generated response to remove unnecessary artifacts (e.g., `<think>` blocks).
5. **Error Handling:** Implements robust error handling for scenarios such as model failures or API key exhaustion.
6. **Logging:** Uses the `BaseLogger` to log informational, warning, and error messages during the execution.

---
<a name="azure-model-methods"></a>
### **Methods**

####
<a name="init-method"></a> `__init__(self, api_key, history=History(), models_list: list[str] = ["deepseek/DeepSeek-V3-0324"], use_random: bool = True)`
Initializes the `AzureModel` instance.

| Parameter       | Type         | Role                                                                 |
|-----------------|--------------|----------------------------------------------------------------------|
| `api_key`       | String       | API key for authenticating with the Azure AI service.               |
| `history`       | `History`    | Stores the conversation history for context-aware responses.        |
| `models_list`   | List[str]    | List of model names available for use.                              |
| `use_random`    | Boolean      | Determines whether to use models in a random order.                 |

- **Side Effects:** Initializes the `ChatCompletionsClient` with the provided API key and endpoint. Sets up logging via `BaseLogger`.

---

####
<a name="clean-deepseek-response"></a> `_clean_deepseek_response(self, text: str) -> str`
Cleans the AI-generated response by removing `<think>` blocks and extra spaces.

| Parameter | Type   | Role                                     |
|-----------|--------|------------------------------------------|
| `text`    | String | The raw response text from the AI model. |

| Output    | Type   | Description                              |
|-----------|--------|------------------------------------------|
| `result`  | String | Cleaned response text.                   |

---

####
<a name="parse-prompt"></a> `_parse_prompt(self, data: list[dict[str, str]]) -> list[UserMessage | SystemMessage]`
Parses a list of dictionaries representing prompts into `UserMessage` or `SystemMessage` objects.

| Parameter | Type                     | Role                                           |
|-----------|--------------------------|------------------------------------------------|
| `data`    | List[Dict[str, str]]     | List of dictionaries containing prompt data.   |

| Output    | Type                     | Description                                    |
|-----------|--------------------------|------------------------------------------------|
| `result`  | List[UserMessage | SystemMessage] | Parsed list of messages for Azure AI.        |

---

####
<a name="generate-answer"></a> `generate_answer(self, with_history: bool = True, prompt: list[dict[str, str]] | None = None) -> str`
Generates an AI response based on the provided prompt or conversation history.

| Parameter      | Type                     | Role                                                                 |
|----------------|--------------------------|----------------------------------------------------------------------|
| `with_history` | Boolean                  | If `True`, uses the conversation history for context.               |
| `prompt`       | List[Dict[str, str]]/None| Optional custom prompt to override the conversation history.        |

| Output         | Type   | Description                                              |
|----------------|--------|----------------------------------------------------------|
| `result`       | String | The AI-generated response after cleaning and processing. |

- **Logic Flow:**
  1. Logs the start of the response generation process.
  2. Determines the input messages based on `with_history` or `prompt`.
  3. Parses the messages into the required format using `_parse_prompt`.
  4. Iterates through the available models in `models_list` to generate a response.
  5. If a model fails, logs the error and switches to the next model.
  6. Cleans the response using `_clean_deepseek_response`.
  7. Logs the final response and returns it.

- **Error Handling:** 
  - Raises `ModelExhaustedException` if no models are available for use.
  - Logs warnings for model failures.

---

### **Data Flow**

#### Inputs and Outputs

| Entity                  | Type                     | Role                                                                 |
|-------------------------|--------------------------|----------------------------------------------------------------------|
| `api_key`               | String                  | API key for authenticating with Azure AI.                           |
| `history`               | `History`               | Stores conversation history for context-aware responses.            |
| `models_list`           | List[str]               | List of model names available for use.                              |
| `messages`              | List[UserMessage/SystemMessage] | Parsed messages for Azure AI.                                       |
| `response`              | Object                  | Raw response object from Azure AI.                                  |
| `result`                | String                  | Cleaned and processed AI-generated response.                        |

---

### **Key Considerations**
> - **Model Fallback:** The class ensures that if one model fails, it switches to the next available model in the list.
> - **Response Cleaning:** The `_clean_deepseek_response` method ensures that unnecessary artifacts are removed from the AI-generated response.
> - **Logging:** Comprehensive logging is implemented for debugging and monitoring purposes.
> - **Error Handling:** The class gracefully handles errors, such as API key exhaustion or model failures, to ensure system stability.

---

### **Potential Enhancements**
1. **Dynamic Model Selection:** Implement a scoring mechanism to dynamically select the most suitable model based on past performance.
2. **Customizable Cleaning:** Allow users to define additional cleaning rules for AI-generated responses.
3. **Enhanced Error Reporting:** Provide more detailed error messages, including potential fixes or recommendations.
4. **Retry Mechanism:** Add a retry mechanism with exponential backoff for transient errors.
5. **Real-time Monitoring:** Integrate real-time monitoring for model usage and performance metrics.
<a name="parse-answer"></a>
## **`parse_answer` Function**

Parses the AI model's response into a structured schema.

### **Technical Logic Flow**
1. Accepts an `answer` string as input.
2. Splits the `answer` string by the pipe (`|`) character into a list called `splited`.
3. Checks if the first element of the split result (`splited[0]`) is `"true"` to determine if documentation needs to be updated (`change_doc`).
4. Checks if the second element of the split result (`splited[1]`) is `"true"` to determine if the global file needs to be remade (`change_global`).
5. Returns an instance of `CheckGitStatusResultSchema` with the parsed values for `need_to_remake` and `remake_gl_file`.

### **Data Contract**
| Entity          | Type                      | Role                       | Notes                          |
|------------------|---------------------------|----------------------------|--------------------------------|
| `answer`        | `str`                     | Input from AI model        | A string response from the AI model containing two pipe-separated values. |
| **Returns**     | `CheckGitStatusResultSchema` | Parsed schema             | Contains boolean flags for `need_to_remake` and `remake_gl_file`. |

---
<a name="parentmodel-class"></a>
## `ParentModel` Class: Abstract Base for AI Model Interaction

### **Functional Role**
The `ParentModel` class serves as an abstract base class for interacting with AI models. It defines the structure for generating responses, managing conversation history, and handling multiple AI models. It provides a foundation for synchronous and asynchronous implementations of AI-based response generation.

---

### **Class Components**

#### **Attributes**
| Attribute           | Type           | Role                                                                 |
|---------------------|----------------|----------------------------------------------------------------------|
| `history`           | `History`      | Stores the conversation history for context-aware AI responses.     |
| `api_keys`          | String         | API key(s) for authenticating with AI models.                       |
| `current_model_index` | Integer       | Tracks the index of the currently active model in `regen_models_name`. |
| `current_key_index` | Integer        | Tracks the index of the currently active API key.                   |
| `regen_models_name` | List[str]      | List of shuffled model names for fallback during failures.          |

#### **Methods**
| Method                     | Type       | Role                                                                 |
|----------------------------|------------|----------------------------------------------------------------------|
| `generate_answer`          | Abstract   | Generates an AI response based on input and history.                |
| `get_answer_without_history` | Abstract | Generates an AI response without considering conversation history.  |
| `get_answer`               | Abstract   | Generates an AI response and updates the conversation history.      |

---

### **Logic Flow**

1. **Initialization**:
   - Accepts an API key, a `History` object, and a list of model names.
   - Optionally shuffles the model list if `use_random` is set to `True`.

2. **Abstract Methods**:
   - `generate_answer`: Must be implemented by subclasses to handle response generation.
   - `get_answer_without_history`: Must be implemented to generate responses without historical context.
   - `get_answer`: Must be implemented to generate responses while updating the conversation history.

---
<a name="model-class"></a>
## `Model` Class: Synchronous AI Model Implementation

### **Functional Role**
The `Model` class extends `ParentModel` to provide a synchronous implementation for generating AI responses. It supports both history-based and history-free response generation.

---

### **Class Components**

#### **Methods**
| Method                     | Type       | Role                                                                 |
|----------------------------|------------|----------------------------------------------------------------------|
| `generate_answer`          | Concrete   | Returns a placeholder response (`"answer"`) for demonstration.      |
| `get_answer_without_history` | Concrete | Calls `generate_answer` with history disabled.                      |
| `get_answer`               | Concrete   | Updates history and generates a response using `generate_answer`.   |

---

### **Logic Flow**

1. **`generate_answer`**:
   - Returns a placeholder response (`"answer"`) as a demonstration.

2. **`get_answer_without_history`**:
   - Calls `generate_answer` with `with_history` set to `False`.

3. **`get_answer`**:
   - Adds the user prompt to the conversation history.
   - Calls `generate_answer` to generate a response.
   - Adds the generated response to the conversation history.

---
<a name="asyncmodel-class"></a>
## `AsyncModel` Class: Asynchronous AI Model Implementation

### **Functional Role**
The `AsyncModel` class extends `ParentModel` to provide an asynchronous implementation for generating AI responses. It supports both history-based and history-free response generation.

---

### **Class Components**

#### **Methods**
| Method                     | Type       | Role                                                                 |
|----------------------------|------------|----------------------------------------------------------------------|
| `generate_answer`          | Concrete   | Asynchronously returns a placeholder response (`"answer"`).          |
| `get_answer_without_history` | Concrete | Calls `generate_answer` asynchronously with history disabled.        |
| `get_answer`               | Concrete   | Updates history and generates a response asynchronously.             |

---

### **Logic Flow**

1. **`generate_answer`**:
   - Asynchronously returns a placeholder response (`"answer"`) for demonstration.

2. **`get_answer_without_history`**:
   - Asynchronously calls `generate_answer` with `with_history` set to `False`.

3. **`get_answer`**:
   - Adds the user prompt to the conversation history.
   - Asynchronously calls `generate_answer` to generate a response.
   - Adds the generated response to the conversation history.

---
<a name="docfactory-class"></a>
## `DocFactory` Class: Modular Documentation Generator

### **Functional Role**
The `DocFactory` class orchestrates the generation of documentation by managing a collection of modular components (`BaseModule` instances). It integrates with AI models and post-processing utilities to produce structured documentation.

---

### **Class Components**

#### **Attributes**
| Attribute       | Type                | Role                                                                 |
|-----------------|---------------------|----------------------------------------------------------------------|
| `modules`       | List[BaseModule]    | List of modules responsible for generating specific documentation parts. |
| `logger`        | `BaseLogger`        | Logs information, warnings, and errors during the documentation process. |
| `with_splited`  | Boolean             | Indicates whether to split module outputs by anchors.                |

#### **Methods**
| Method                     | Type       | Role                                                                 |
|----------------------------|------------|----------------------------------------------------------------------|
| `generate_doc`             | Concrete   | Orchestrates the documentation generation process.                   |

---

### **Logic Flow**

1. **Initialization**:
   - Accepts a list of `BaseModule` instances and a flag (`with_splited`) to determine if module outputs should be split.

2. **`generate_doc`**:
   - Initializes a `DocHeadSchema` to store the generated documentation.
   - Iterates through the list of modules:
     - Calls the `generate` method of each module with the provided `info` and `model`.
     - If `with_splited` is `True`, splits the output using `split_text_by_anchors` and adds the parts to `DocHeadSchema`.
     - Logs the module's output and progress.
   - Updates the progress tracker and removes the subtask upon completion.
   - Returns the final `DocHeadSchema`.

---
<a name="basemodule-class"></a>
## `BaseModule` Class: Abstract Base for Documentation Modules

### **Functional Role**
The `BaseModule` class defines the structure for modular documentation components. Each module is responsible for generating a specific part of the documentation.

---

### **Class Components**

#### **Methods**
| Method                     | Type       | Role                                                                 |
|----------------------------|------------|----------------------------------------------------------------------|
| `generate`                 | Abstract   | Must be implemented by subclasses to generate documentation parts.  |

---

### **Logic Flow**

1. **`generate`**:
   - Abstract method to be implemented by subclasses.
   - Accepts `info` (input data) and `model` (AI model instance) as parameters.
   - Returns the generated documentation part.

---

### **Key Considerations**
> - **Extensibility:** The modular design allows developers to create custom modules by extending `BaseModule`.
> - **Error Logging:** The `DocFactory` integrates with `BaseLogger` to ensure that errors or issues during module execution are logged.
> - **Progress Tracking:** The `generate_doc` method uses `BaseProgress` to provide real-time progress updates.
> - **Anchor Splitting:** The `split_text_by_anchors` utility ensures that module outputs are divided into logical sections for better readability.
<a name="custommodule-class"></a>
## `CustomModule` Class: Generating Custom Documentation with Context

### **Functional Role**
The `CustomModule` class is a modular component designed to generate custom documentation sections. It utilizes a description provided during initialization and processes code data with context to produce tailored documentation.

---

### **Class Components**

#### **Attributes**
| Attribute       | Type       | Role                                                                 |
|------------------|------------|----------------------------------------------------------------------|
| `discription`    | `str`      | A user-defined description that provides context for the generated documentation. |

#### **Methods**
| Method                     | Type       | Role                                                                 |
|----------------------------|------------|----------------------------------------------------------------------|
| `__init__`                 | Concrete   | Initializes the module with a specific description.                 |
| `generate`                 | Concrete   | Generates custom documentation based on the provided context.       |

---

### **Logic Flow**

1. **Initialization**:
   - Accepts a `discription` string during instantiation.
   - Calls the parent class constructor (`BaseModule.__init__`) to initialize the base module.

2. **`generate`**:
   - Extracts the `code_mix` and `language` keys from the `info` dictionary.
   - Splits the `code_mix` data into smaller chunks using the `split_data` function with a maximum symbol limit of 5000.
   - Calls the `generete_custom_discription` function with the split data, the AI `model`, the module's `discription`, and the `language`.
   - Returns the generated documentation.

---
<a name="custommodulewithoutcontext-class"></a>
## `CustomModuleWithOutContext` Class: Generating Custom Documentation without Context

### **Functional Role**
The `CustomModuleWithOutContext` class is a modular component designed to generate custom documentation sections without requiring additional context from the input data.

---

### **Class Components**

#### **Attributes**
| Attribute       | Type       | Role                                                                 |
|------------------|------------|----------------------------------------------------------------------|
| `discription`    | `str`      | A user-defined description that provides context for the generated documentation. |

#### **Methods**
| Method                     | Type       | Role                                                                 |
|----------------------------|------------|----------------------------------------------------------------------|
| `__init__`                 | Concrete   | Initializes the module with a specific description.                 |
| `generate`                 | Concrete   | Generates custom documentation without requiring input context.     |

---

### **Logic Flow**

1. **Initialization**:
   - Accepts a `discription` string during instantiation.
   - Calls the parent class constructor (`BaseModule.__init__`) to initialize the base module.

2. **`generate`**:
   - Extracts the `language` key from the `info` dictionary.
   - Calls the `generete_custom_discription_without` function with the AI `model`, the module's `discription`, and the `language`.
   - Returns the generated documentation.

---
<a name="introlinks-class"></a>
## `IntroLinks` Class: Generating Documentation with Extracted HTML Links

### **Functional Role**
The `IntroLinks` class is responsible for extracting HTML links from the input data and generating an introduction based on those links.

---

### **Class Components**

#### **Methods**
| Method                     | Type       | Role                                                                 |
|----------------------------|------------|----------------------------------------------------------------------|
| `generate`                 | Concrete   | Extracts HTML links and generates an introduction based on them.    |

---

### **Logic Flow**

1. **`generate`**:
   - Extracts the `full_data` key from the `info` dictionary.
   - Uses the `get_all_html_links` function to extract anchor links from the `full_data`.
   - Calls the `get_links_intro` function with the extracted links, the AI `model`, and the `language` from the `info` dictionary.
   - Returns the generated introduction based on the links.

---
<a name="introtext-class"></a>
## `IntroText` Class: Generating Global Introduction for Documentation

### **Functional Role**
The `IntroText` class generates a global introduction for the documentation based on the provided global information.

---

### **Class Components**

#### **Methods**
| Method                     | Type       | Role                                                                 |
|----------------------------|------------|----------------------------------------------------------------------|
| `generate`                 | Concrete   | Generates a global introduction for the documentation.              |

---

### **Logic Flow**

1. **`generate`**:
   - Extracts the `global_info` and `language` keys from the `info` dictionary.
   - Calls the `get_introdaction` function with the `global_info`, the AI `model`, and the `language`.
   - Returns the generated global introduction.

---

### **Key Considerations**
> - **Extensibility:** All classes extend the `BaseModule` class, allowing for easy integration into the `DocFactory`.
> - **Input Data Requirements:** Each module relies on specific keys in the `info` dictionary (`code_mix`, `language`, `full_data`, `global_info`).
> - **AI Model Dependency:** All modules use the `Model` instance for natural language generation tasks.
> - **Utility Functions:** Functions like `split_data`, `get_all_html_links`, `get_links_intro`, and `get_introdaction` are critical for processing input data and generating outputs.
<a name="custom-intro-functions"></a>
## Custom Introduction Functions: Generating Documentation Introductions and Descriptions

### **Functional Role**
The functions in this module are designed to generate various types of introductions and custom descriptions for documentation. They leverage AI models to extract meaningful insights and create structured content based on the provided input data.

---

### **Function Components**

#### **Functions Overview**
| Function Name                          | Input Parameters                                                                 | Output                  | Role                                                                 |
|----------------------------------------|----------------------------------------------------------------------------------|-------------------------|----------------------------------------------------------------------|
| `get_all_html_links`                   | `data: str`                                                                      | `list[str]`             | Extracts HTML anchor links from the input string.                   |
| `get_links_intro`                      | `links: list[str], model: Model, language: str = "en"`                           | `str`                   | Generates an introduction based on the provided HTML links.         |
| `get_introdaction`                     | `global_data: str, model: Model, language: str = "en"`                           | `str`                   | Generates a global introduction based on the provided global data.  |
| `generete_custom_discription`          | `splited_data: str, model: Model, custom_description: str, language: str = "en"` | `str`                   | Generates a custom description based on split data and a prompt.    |
| `generete_custom_discription_without`  | `model: Model, custom_description: str, language: str = "en"`                    | `str`                   | Generates a custom description without requiring split data.        |

---

### **Logic Flow**

#### **`get_all_html_links`**
1. Initializes an empty list `links` to store extracted anchor links.
2. Logs the start of the HTML link extraction process using `BaseLogger`.
3. Uses a regex pattern (`<a name=["\']?(.*?)["\']?></a>`) to find all anchor tags in the input `data`.
4. Filters out anchor names shorter than 5 characters and appends valid links (prefixed with `#`) to the `links` list.
5. Logs the number of extracted links and their details.
6. Returns the list of extracted links.

#### **`get_links_intro`**
1. Constructs a prompt using:
   - A system message specifying the language.
   - A system message containing the `BASE_INTRODACTION_CREATE_LINKS` template.
   - A user message containing the list of links.
2. Logs the start of the introduction generation process.
3. Calls the `model.get_answer_without_history` method with the constructed prompt.
4. Logs the generated introduction and its content.
5. Returns the generated introduction.

#### **`get_introdaction`**
1. Constructs a prompt using:
   - A system message specifying the language.
   - A system message containing the `BASE_INTRO_CREATE` template.
   - A user message containing the `global_data`.
2. Calls the `model.get_answer_without_history` method with the constructed prompt.
3. Returns the generated global introduction.

#### **`generete_custom_discription`**
1. Iterates through the `splited_data`.
2. Constructs a prompt for each split data segment using:
   - A system message specifying the language.
   - A system message containing a technical analysis instruction.
   - A system message providing the context (`sp_data`).
   - A system message containing the `BASE_CUSTOM_DISCRIPTIONS` template.
   - A user message specifying the `custom_description`.
3. Calls the `model.get_answer_without_history` method with the constructed prompt.
4. If the result does not contain specific error markers (`!noinfo` or "No information found"), returns the result.
5. If the result contains error markers, continues to the next segment.
6. Returns the first valid result or an empty string if no valid result is found.

#### **`generete_custom_discription_without`**
1. Constructs a prompt using:
   - A system message specifying the language.
   - A system message containing a technical analysis and rewriting instruction.
   - A system message specifying strict rules for the output format.
   - A user message specifying the `custom_description`.
2. Calls the `model.get_answer_without_history` method with the constructed prompt.
3. Returns the generated custom description.

---

### **Key Considerations**
> - **Regex for HTML Links:** The regex pattern used in `get_all_html_links` assumes a specific format for anchor tags (`<a name="..."></a>`). If the format changes, the function may need updates.
> - **AI Model Dependency:** All functions rely on the `Model` instance for generating outputs. The accuracy and quality of the generated content depend on the model's capabilities.
> - **Error Handling in `generete_custom_discription`:** The function checks for specific error markers (`!noinfo` and "No information found") in the model's response and continues processing until a valid result is found.
> - **Output Format Rules:** The `generete_custom_discription_without` function enforces strict rules for the output format, ensuring consistency and clarity in the generated documentation.
<a name="embedding-module"></a>
## **Embedding Module**

### **`bubble_sort_by_dist`**
This function implements the Bubble Sort algorithm to sort a list of tuples based on the second element (distance) in ascending order.

#### **Technical Logic Flow**
1. The function accepts a list of tuples `arr`, where each tuple contains an identifier and a distance value.
2. It iterates through the list multiple times using nested loops.
3. For each pair of adjacent elements, it swaps them if the distance of the first element is greater than the second.
4. Returns the sorted list.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `arr`           | `list`     | Input list of tuples  | Each tuple contains an identifier and a distance value. |
| **Returns**     | `list`     | Sorted list           | List sorted in ascending order based on distance values. |

---
<a name="get-len-btw-vectors"></a>
## **`get_len_btw_vectors`**
This function calculates the Euclidean distance between two vectors.

#### **Technical Logic Flow**
1. Accepts two vectors (`vector1` and `vector2`) as input.
2. Converts the input vectors into NumPy arrays.
3. Computes the Euclidean distance using `np.linalg.norm`.
4. Returns the calculated distance as a float.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `vector1`       | `list`     | Input vector          | First vector for distance calculation. |
| `vector2`       | `list`     | Input vector          | Second vector for distance calculation. |
| **Returns**     | `float`    | Distance              | Euclidean distance between the two vectors. |

---
<a name="sort-vectors"></a>
## **`sort_vectors`**
This function sorts a dictionary of vectors based on their Euclidean distance from a root vector.

#### **Technical Logic Flow**
1. Accepts a `root_vector` and a dictionary `other` where keys are identifiers and values are vectors.
2. Iterates through the dictionary, calculating the Euclidean distance between the `root_vector` and each vector in `other` using `get_len_btw_vectors`.
3. Appends each identifier and its distance as a tuple to a list `sort_list`.
4. Sorts the list using `bubble_sort_by_dist`.
5. Extracts and returns a list of identifiers in ascending order of their distances.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `root_vector`   | `list`     | Reference vector      | The vector to compare distances against. |
| `other`         | `dict`     | Dictionary of vectors | Keys are identifiers, values are vectors. |
| **Returns**     | `list[str]`| Sorted identifiers    | List of keys sorted by their distance to `root_vector`. |

---
<a name="embedding-class"></a>
## **`Embedding` Class**
This class provides methods to generate embeddings for text content using the `genai` library.

### **`__init__`**
Initializes the `Embedding` class with an API key.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `api_key`       | `str`      | API Key               | API key for authenticating with the `genai` client. |

---

### **`get_vector`**
Generates a vector embedding for a given text prompt.

#### **Technical Logic Flow**
1. Accepts a `prompt` string as input.
2. Calls the `genai.Client.models.embed_content` method to generate embeddings.
3. Specifies the model (`gemini-embedding-2-preview`) and configuration (`output_dimensionality=768`).
4. Checks if embeddings are returned. If not, raises an exception.
5. Returns the first embedding vector.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `prompt`        | `str`      | Input text            | Text content to generate embeddings for. |
| **Returns**     | `list`     | Embedding vector      | First embedding vector from the response. |

> **Warning:** If the `embed_content` method fails to generate embeddings, an exception is raised with the message `"problem with embedding"`.

---
<a name="async-embedding-class"></a>
## **`AsyncEmbedding` Class**
This class extends `EmbeddingParent` and provides asynchronous methods for generating embeddings.

### **`__init__`**
Initializes the `AsyncEmbedding` class with an API key.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `api_key`       | `str`      | API Key               | API key for authenticating with the `genai` client. |

---

### **`get_vector`**
Asynchronously generates a vector embedding for a given text prompt.

#### **Technical Logic Flow**
1. Accepts a `prompt` string as input.
2. Calls the asynchronous `genai.Client.aio.models.embed_content` method to generate embeddings.
3. Specifies the model (`gemini-embedding-2-preview`) and configuration (`output_dimensionality=768`).
4. Checks if embeddings are returned. If not, raises an exception.
5. Returns the first embedding vector.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `prompt`        | `str`      | Input text            | Text content to generate embeddings for. |
| **Returns**     | `list`     | Embedding vector      | First embedding vector from the response. |

> **Warning:** If the `embed_content` method fails to generate embeddings, an exception is raised with the message `"problem with embedding"`.

---
<a name="sorting-module"></a>
## **Sorting Module**

### **`extract_links_from_start`**
Extracts anchor links from the start of text chunks.

#### **Technical Logic Flow**
1. Accepts a list of text `chunks`.
2. Defines a regex pattern to match anchor tags in the format `<a name="..."></a>`.
3. Iterates through the chunks, searching for matches with the regex pattern.
4. Appends valid anchor links (with length > 5) to the `links` list.
5. Sets `have_to_del_first` to `True` if no valid anchor is found in a chunk.
6. Returns the list of extracted links and the `have_to_del_first` flag.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `chunks`        | `list[str]`| Input text chunks     | List of text chunks to search for anchor links. |
| **Returns**     | `tuple`    | Links and flag        | A tuple containing a list of extracted links and a boolean flag. |

---

### **`split_text_by_anchors`**
Splits text into sections based on anchor tags.

#### **Technical Logic Flow**
1. Accepts a `text` string as input.
2. Defines a regex pattern to match anchor tags (`<a name="..."></a>`).
3. Splits the text into chunks using the regex pattern.
4. Calls `extract_links_from_start` to extract anchor links and determine if the first chunk should be removed.
5. Removes the first chunk if it does not contain a valid anchor or if the first anchor is not at the beginning of the text.
6. Maps each anchor link to its corresponding text chunk.
7. Raises an exception if the number of links does not match the number of text chunks.
8. Returns a dictionary mapping anchor links to text chunks.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `text`          | `str`      | Input text            | Text content containing anchor tags. |
| **Returns**     | `dict`     | Anchor-text mapping   | Dictionary mapping anchor links to text chunks. |

> **Warning:** If the number of extracted links does not match the number of text chunks, an exception is raised with the message `"Something with anchors"`.

---

### **`get_order`**
Sorts a list of text chunks semantically using an AI model.

#### **Technical Logic Flow**
1. Accepts a `model` instance and a list of `chanks` (text chunks).
2. Initializes a `BaseLogger` instance to log the process.
3. Logs the start of the ordering process and the input chunks.
4. Constructs a prompt instructing the AI model to sort the titles semantically.
5. Calls the `model.get_answer_without_history` method with the prompt.
6. Processes the result into a list of sorted titles.
7. Logs the sorted result and returns it.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `model`         | `Model`    | AI model instance     | Used for semantic sorting of titles. |
| `chanks`        | `list[str]`| Input text chunks     | List of titles to be sorted.   |
| **Returns**     | `list`     | Sorted titles         | List of titles sorted semantically. |

> **Note:** The function relies on the AI model's ability to interpret and semantically sort the input titles.
<a name="codemix-class"></a>
## **`CodeMix` Class**

Handles repository content aggregation and filtering based on ignore patterns.

### **`__init__` Method**

Initializes the `CodeMix` class with the root directory and ignore patterns.

#### **Data Contract**
| Entity          | Type                      | Role                       | Notes                          |
|------------------|---------------------------|----------------------------|--------------------------------|
| `root_dir`      | `str`                     | Root directory path        | Default is the current directory (`"."`). |
| `ignore_patterns` | `list[str]` or `None`   | Ignore patterns            | List of patterns to ignore. Defaults to `None`. |

---
<a name="have-to-change"></a>
## **`have_to_change` Function**

Determines whether documentation or global files need to be updated based on code changes.

### **Technical Logic Flow**
1. Accepts the following inputs:
   - `model`: An instance of the `Model` class, used for AI-based decision-making.
   - `diff`: A list of dictionaries representing code changes.
   - `global_info`: An optional string containing global information about the project.
2. Constructs a `prompt` list containing:
   - A system message with the base prompt (`BASE_CHANGES_CHECK_PROMPT`).
   - A system message with the `global_info` (if provided).
   - A user message with the stringified `diff` data.
3. Sends the `prompt` to the AI model using the `model.get_answer_without_history` method.
4. Parses the response from the AI model using the `parse_answer` function.
5. Returns an instance of `CheckGitStatusResultSchema` containing the parsed results.

### **Data Contract**
| Entity          | Type                      | Role                       | Notes                          |
|------------------|---------------------------|----------------------------|--------------------------------|
| `model`         | `Model`                   | AI model instance          | Used to generate a response based on the provided prompt. |
| `diff`          | `list[dict[str, str]]`    | Code changes               | A list of dictionaries representing file changes. |
| `global_info`   | `str` or `None`           | Global project information | Optional. Provides context for the AI model. |
| **Returns**     | `CheckGitStatusResultSchema` | Parsed schema             | Contains boolean flags for `need_to_remake` and `remake_gl_file`. |

---
<a name="should-ignore"></a>
### **`should_ignore` Method**

Determines if a file or directory should be ignored based on the provided ignore patterns.

#### **Technical Logic Flow**
1. Accepts a `path` as input.
2. Converts the `path` to a relative path with respect to the `root_dir`.
3. Checks if the relative path matches any of the `ignore_patterns` using `fnmatch`.
4. Returns `True` if the path matches any pattern; otherwise, returns `False`.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| `path`          | `str`      | File or directory path | The path to check against the ignore patterns. |
| **Returns**     | `bool`     | Ignore flag           | `True` if the path matches any ignore pattern, `False` otherwise. |

---
<a name="build-repo-content"></a>
### **`build_repo_content` Method**

Generates a structured representation of the repository's content.

#### **Technical Logic Flow**
1. Initializes an empty `content` list and appends a "Repository Structure:" header.
2. Iterates through all files and directories in the repository (recursively).
3. For each path:
   - Checks if the path should be ignored using the `should_ignore` method.
   - Logs ignored paths using `BaseLogger`.
   - If not ignored:
     - Appends the path to the `content` list, formatted with indentation based on its depth in the directory tree.
4. Appends a separator (`"="*20`) to the `content` list.
5. Iterates through all files in the repository again:
   - If the file is not ignored, reads its content and appends it to the `content` list.
   - Logs an error if the file cannot be read.
6. Joins the `content` list into a single string and returns it.

#### **Data Contract**
| Entity          | Type       | Role                  | Notes                          |
|------------------|------------|-----------------------|--------------------------------|
| **Returns**     | `str`      | Repository content    | A structured string representation of the repository's content. |

> **Warning:** If a file cannot be read, an error message is appended to the content instead of the file's content.

---
<a name="ignore-list"></a>
### **`ignore_list`**

A predefined list of file and directory patterns to ignore during repository content aggregation.

#### **Patterns**
- File extensions: `*.pyo`, `*.pyd`, `*.pdb`, `*.pkl`, `*.log`, `*.sqlite3`, `*.db`, `*.pyc`, etc.
- Directories: `venv`, `env`, `.venv`, `.env`, `.vscode`, `.idea`, `.git`, etc.

> **Note:** The ignore patterns are used by the `should_ignore` method to filter out unwanted files and directories.
<a name="compress-method"></a>
## **`compress` Method**

This method compresses a given data string using a specified AI model and project settings. It generates a prompt based on the project settings and compression parameters, then retrieves a compressed version of the data.

### **Technical Logic Flow**
1. Constructs a prompt with:
   - The project settings' `prompt`.
   - A compression-specific prompt generated by `get_BASE_COMPRESS_TEXT`.
   - The input data to be compressed.
2. Sends the prompt to the AI model via `model.get_answer_without_history`.
3. Returns the compressed result.

### **Data Contract**
| Entity            | Type               | Role                          | Notes                                  |
|--------------------|--------------------|-------------------------------|----------------------------------------|
| `data`            | `str`              | Input data to compress        | The raw data to be compressed.         |
| `project_settings`| `ProjectSettings`  | Project-specific settings     | Provides context for the compression. |
| `model`           | `Model`            | AI model instance             | Used to process the compression prompt.|
| `compress_power`  | `int`              | Compression level             | Determines the degree of compression. |
| **Returns**       | `str`              | Compressed data               | The compressed version of the input.  |

---
<a name="compress-and-compare-method"></a>
## **`compress_and_compare` Method**

This method compresses a list of data chunks iteratively and combines them into fewer chunks. It uses a progress bar to track the compression process.

### **Technical Logic Flow**
1. Initializes an empty list to store compressed results, dividing the input data into groups based on `compress_power`.
2. Creates a progress bar to monitor the compression task.
3. Iterates through each data chunk:
   - Determines the current group index.
   - Compresses the chunk using the `compress` method.
   - Appends the compressed result to the corresponding group.
   - Updates the progress bar.
4. Removes the progress bar after processing all chunks.
5. Returns the list of compressed data groups.

### **Data Contract**
| Entity                  | Type               | Role                          | Notes                                  |
|--------------------------|--------------------|-------------------------------|----------------------------------------|
| `data`                  | `list[str]`        | List of data chunks           | The input data to be compressed.       |
| `model`                 | `Model`            | AI model instance             | Used to process the compression prompt.|
| `project_settings`      | `ProjectSettings`  | Project-specific settings     | Provides context for the compression. |
| `compress_power`        | `int`              | Compression level             | Determines the number of chunks per group. |
| `progress_bar`          | `BaseProgress`     | Progress bar instance         | Tracks the progress of the task.       |
| **Returns**             | `list[str]`        | Compressed data groups        | List of compressed data chunks.        |

---
<a name="compress-to-one-method"></a>
## **`compress_to_one` Method**

This method compresses a list of data chunks into a single compressed string through iterative compression.

### **Technical Logic Flow**
1. Initializes an iteration counter.
2. While the input data list contains more than one chunk:
   - Adjusts the `compress_power` if the number of chunks is less than `compress_power + 1`.
   - Compresses and combines the data chunks using `compress_and_compare`.
   - Increments the iteration counter.
3. Returns the final compressed string (the only remaining element in the list).

### **Data Contract**
| Entity                  | Type               | Role                          | Notes                                  |
|--------------------------|--------------------|-------------------------------|----------------------------------------|
| `data`                  | `list[str]`        | List of data chunks           | The input data to be compressed.       |
| `model`                 | `Model`            | AI model instance             | Used to process the compression prompt.|
| `project_settings`      | `ProjectSettings`  | Project-specific settings     | Provides context for the compression. |
| `compress_power`        | `int`              | Compression level             | Determines the number of chunks per group. |
| `progress_bar`          | `BaseProgress`     | Progress bar instance         | Tracks the progress of the task.       |
| **Returns**             | `str`              | Compressed data               | The final compressed version of the input. |

> **Note:** This method performs iterative compression until the data is reduced to a single chunk.

---
<a name="project-settings-class"></a>
## **`ProjectSettings` Class**

This class manages project-specific settings, including the project name and additional metadata. It also generates a formatted prompt based on the stored settings.

### **Attributes**
| Attribute       | Type               | Role                          | Notes                                  |
|------------------|--------------------|-------------------------------|----------------------------------------|
| `project_name`  | `str`              | Name of the project           | Provided during initialization.        |
| `info`          | `dict[str, str]`   | Metadata dictionary           | Stores additional project-specific information. |

### **Methods**
#### **`__init__`**
Initializes the `ProjectSettings` instance with a project name and an empty metadata dictionary.

| Parameter        | Type               | Role                          | Notes                                  |
|------------------|--------------------|-------------------------------|----------------------------------------|
| `project_name`  | `str`              | Name of the project           | Required during initialization.        |

#### **`add_info`**
Adds a key-value pair to the metadata dictionary.

| Parameter        | Type               | Role                          | Notes                                  |
|------------------|--------------------|-------------------------------|----------------------------------------|
| `key`           | `str`              | Metadata key                  | Key for the metadata entry.            |
| `value`         | `str`              | Metadata value                | Value for the metadata entry.          |

#### **`prompt`**
Generates a formatted string containing the project name and metadata.

| **Returns**     | Type               | Role                          | Notes                                  |
|------------------|--------------------|-------------------------------|----------------------------------------|
| **Returns**     | `str`              | Formatted prompt              | Includes project name and metadata.    |

---
<a name="split-data-method"></a>
## **`split_data` Method**

This method splits a large string into smaller chunks, ensuring that each chunk does not exceed a specified maximum character limit (`max_symbols`). It uses a recursive approach to split oversized chunks further until all chunks meet the size constraint.

### **Technical Logic Flow**
1. **Initialization**:
   - A logger instance (`BaseLogger`) is created to track the process.
   - Logs the start of the data splitting process.

2. **Splitting Logic**:
   - Iterates through the list of strings (`splited_by_files`).
   - If a string exceeds 1.5 times the `max_symbols` limit, it is split into two parts:
     - The first half is kept in the current position.
     - The second half is inserted into the next position in the list.
   - The process repeats until no further splitting is required.

3. **Chunk Assignment**:
   - Iterates through the split strings and assigns them to `split_objects`.
   - Ensures that each chunk in `split_objects` does not exceed 1.25 times the `max_symbols` limit.

4. **Logging**:
   - Logs the total number of parts generated and the maximum symbol limit used.

5. **Return**:
   - Returns the list of split chunks (`split_objects`).

### **Inputs and Outputs**
| Entity                | Type               | Role                          | Notes                                  |
|-----------------------|--------------------|-------------------------------|----------------------------------------|
| `splited_by_files`    | `list[str]`        | Input data to be split        | List of strings to be processed.       |
| `max_symbols`         | `int`              | Maximum character limit       | Defines the size limit for each chunk. |
| **Returns**           | `list[str]`        | Split data chunks             | List of strings adhering to size limit.|

> **Note:** The method ensures that no chunk exceeds the specified size limit, making it suitable for further processing.

---
<a name="write-docs-by-parts-method"></a>
## **`write_docs_by_parts` Method**

This method generates documentation for a specific part of the input data by interacting with the AI model.

### **Technical Logic Flow**
1. **Initialization**:
   - A logger instance (`BaseLogger`) is created to track the process.
   - Logs the start of documentation generation for the provided part.

2. **Prompt Construction**:
   - Constructs a prompt for the AI model, including:
     - Language specification.
     - Global project information from `project_settings`.
     - A predefined system prompt (`BASE_PART_COMPLITE_TEXT`).
     - Optional global information (`global_info`).
     - Optional previous documentation part (`prev_info`).
     - The current part of the input data.

3. **AI Model Interaction**:
   - Sends the constructed prompt to the AI model using `model.get_answer_without_history`.
   - Removes any Markdown code block formatting (e.g., backticks) from the AI's response.

4. **Logging**:
   - Logs the length of the generated documentation and the content of the response.

5. **Return**:
   - Returns the processed documentation string.

### **Inputs and Outputs**
| Entity                | Type               | Role                          | Notes                                  |
|-----------------------|--------------------|-------------------------------|----------------------------------------|
| `part`                | `str`              | Input data chunk              | The specific part of the input data to document. |
| `model`               | `Model`            | AI model instance             | Used to generate the documentation.    |
| `project_settings`    | `ProjectSettings`  | Project settings instance     | Provides global project information.   |
| `prev_info`           | `str` or `None`    | Previous documentation part   | Optional; used for context.            |
| `language`            | `str`              | Language for the documentation| Defaults to English (`"en"`).          |
| `global_info`         | `str` or `None`    | Global project relations      | Optional; provides additional context. |
| **Returns**           | `str`              | Generated documentation       | The AI-generated documentation for the input part. |

> **Note:** The method ensures that the AI-generated documentation is free of Markdown code block formatting.

---
<a name="gen-doc-parts-method"></a>
## **`gen_doc_parts` Method**

This method orchestrates the generation of documentation for a large input by splitting it into smaller parts and processing each part sequentially.

### **Technical Logic Flow**
1. **Data Splitting**:
   - Calls `split_data` to divide the input (`full_code_mix`) into smaller chunks based on the `max_symbols` limit.

2. **Initialization**:
   - Creates a logger instance (`BaseLogger`) to track the process.
   - Logs the start of the documentation generation process.
   - Initializes a progress bar (`BaseProgress`) to track progress.

3. **Documentation Generation**:
   - Iterates through the split chunks (`splited_data`).
   - For each chunk:
     - Calls `write_docs_by_parts` to generate documentation.
     - Appends the result to the cumulative documentation (`all_result`).
     - Retains the last 3000 characters of the result for context in the next iteration.

4. **Progress Tracking**:
   - Updates the progress bar after processing each chunk.
   - Removes the progress bar subtask upon completion.

5. **Logging**:
   - Logs the total length of the generated documentation and the final content.

6. **Return**:
   - Returns the complete documentation (`all_result`).

### **Inputs and Outputs**
| Entity                | Type               | Role                          | Notes                                  |
|-----------------------|--------------------|-------------------------------|----------------------------------------|
| `full_code_mix`       | `str`              | Full input data               | The complete code mix to document.     |
| `max_symbols`         | `int`              | Maximum character limit       | Defines the size limit for each chunk. |
| `model`               | `Model`            | AI model instance             | Used to generate documentation.        |
| `project_settings`    | `ProjectSettings`  | Project settings instance     | Provides global project information.   |
| `language`            | `str`              | Language for the documentation| Specifies the language (default: `"en"`). |
| `progress_bar`        | `BaseProgress`     | Progress bar instance         | Tracks the progress of the task.       |
| `global_info`         | `str` or `None`    | Global project relations      | Optional; provides additional context. |
| **Returns**           | `str`              | Complete documentation        | The AI-generated documentation for the entire input. |

> **Note:** This method ensures that large inputs are processed efficiently by splitting them into manageable parts and generating documentation iteratively.
<a name="doc-schema"></a>
## **`DocSchema` Classes**

The `DocSchema` module defines the structure and behavior of documentation-related data, including content management, embedding initialization, and document assembly.

---

### **`DocContent` Class**

The `DocContent` class represents a single documentation section, including its content and an optional embedding vector.

#### **Attributes**
| Attribute          | Type           | Description                                                                 |
|--------------------|----------------|-----------------------------------------------------------------------------|
| `content`          | `str`          | The textual content of the documentation section.                          |
| `embedding_vector` | `list` or `None` | Optional; stores the embedding vector generated for the content.           |

#### **Methods**
1. **`init_embedding(embedding_model: Embedding)`**
   - Initializes the `embedding_vector` for the content using the provided `Embedding` model.
   - **Inputs and Outputs**:
     | Entity            | Type         | Role                          | Notes                                  |
     |-------------------|--------------|-------------------------------|----------------------------------------|
     | `embedding_model` | `Embedding` | Embedding model instance      | Used to generate the embedding vector. |
     | **Returns**       | `None`      | N/A                           | Updates the `embedding_vector` in place. |

---

### **`DocHeadSchema` Class**

The `DocHeadSchema` class manages the structure of a documentation head, including the order of content sections and their associated data.

#### **Attributes**
| Attribute          | Type           | Description                                                                 |
|--------------------|----------------|-----------------------------------------------------------------------------|
| `content_orders`   | `list[str]`    | Ordered list of section names.                                              |
| `parts`            | `dict[str, DocContent]` | Mapping of section names to their `DocContent` instances.                  |

#### **Methods**
1. **`add_parts(name: str, content: DocContent)`**
   - Adds a new section to the documentation. If the section name already exists, appends a numeric suffix to ensure uniqueness.
   - **Inputs and Outputs**:
     | Entity       | Type         | Role                          | Notes                                  |
     |--------------|--------------|-------------------------------|----------------------------------------|
     | `name`       | `str`        | Section name                  | Name of the documentation section.     |
     | `content`    | `DocContent` | Section content               | Instance of `DocContent`.              |
     | **Returns**  | `None`       | N/A                           | Updates `content_orders` and `parts`.  |

2. **`get_full_doc(split_el: str = "\n") -> str`**
   - Assembles the full documentation by concatenating all sections in the order specified by `content_orders`.
   - **Inputs and Outputs**:
     | Entity       | Type         | Role                          | Notes                                  |
     |--------------|--------------|-------------------------------|----------------------------------------|
     | `split_el`   | `str`        | Separator                     | Default separator between sections.    |
     | **Returns**  | `str`        | Full documentation            | Concatenated content of all sections.  |

3. **`__add__(other: DocHeadSchema) -> DocHeadSchema`**
   - Merges the current `DocHeadSchema` with another, appending all sections from the other schema.
   - **Inputs and Outputs**:
     | Entity       | Type         | Role                          | Notes                                  |
     |--------------|--------------|-------------------------------|----------------------------------------|
     | `other`      | `DocHeadSchema` | Another `DocHeadSchema` instance | Sections are appended to the current schema. |
     | **Returns**  | `DocHeadSchema` | Updated schema               | The merged `DocHeadSchema` instance.  |

---

### **`DocInfoSchema` Class**

The `DocInfoSchema` class serves as the top-level container for all documentation-related data, including global information, code mix, and the documentation head.

#### **Attributes**
| Attribute          | Type           | Description                                                                 |
|--------------------|----------------|-----------------------------------------------------------------------------|
| `global_info`      | `str`          | Global information about the project.                                       |
| `code_mix`         | `str`          | Aggregated code content for documentation.                                  |
| `doc`              | `DocHeadSchema` | Instance of `DocHeadSchema` containing the documentation structure.         |

---
<a name="base-logger"></a>
## **`BaseLogger` Module**

The `BaseLogger` module provides logging utilities for tracking application events, errors, and informational messages.

---

### **`BaseLog` Class**

The `BaseLog` class serves as the base for all log types, encapsulating a message and its severity level.

#### **Attributes**
| Attribute          | Type           | Description                                                                 |
|--------------------|----------------|-----------------------------------------------------------------------------|
| `message`          | `str`          | The log message.                                                            |
| `level`            | `int`          | The severity level of the log (default: `0`).                               |

#### **Methods**
1. **`format() -> str`**
   - Formats the log message for output.
   - **Returns**: A formatted string containing the log message.

2. **`_log_prefix` (Property)**
   - Generates a timestamped prefix for the log message.
   - **Returns**: A string containing the current timestamp.

---

### **Log Subclasses**
1. **`ErrorLog`**
   - Represents error-level logs.
   - **`format()`**: Prepends `[ERROR]` to the log message.

2. **`WarningLog`**
   - Represents warning-level logs.
   - **`format()`**: Prepends `[WARNING]` to the log message.

3. **`InfoLog`**
   - Represents informational logs.
   - **`format()`**: Prepends `[INFO]` to the log message.

---

### **`BaseLoggerTemplate` Class**

The `BaseLoggerTemplate` class defines a template for logging systems, supporting both console and file-based logging.

#### **Attributes**
| Attribute          | Type           | Description                                                                 |
|--------------------|----------------|-----------------------------------------------------------------------------|
| `log_level`        | `int`          | Minimum severity level for logs to be recorded.                             |

#### **Methods**
1. **`log(log: BaseLog)`**
   - Logs a message to the console or file.
   - **Inputs**:
     | Entity       | Type         | Role                          | Notes                                  |
     |--------------|--------------|-------------------------------|----------------------------------------|
     | `log`        | `BaseLog`    | Log message                   | Instance of a `BaseLog` subclass.      |

2. **`global_log(log: BaseLog)`**
   - Logs a message if its severity level meets the `log_level` threshold.

---

### **`FileLoggerTemplate` Class**

The `FileLoggerTemplate` class extends `BaseLoggerTemplate` to support file-based logging.

#### **Attributes**
| Attribute          | Type           | Description                                                                 |
|--------------------|----------------|-----------------------------------------------------------------------------|
| `file_path`        | `str`          | Path to the log file.                                                       |

#### **Methods**
1. **`log(log: BaseLog)`**
   - Writes the log message to the specified file.

---

### **`BaseLogger` Singleton**

The `BaseLogger` class provides a singleton interface for logging, ensuring a single logger instance is used throughout the application.

#### **Methods**
1. **`set_logger(logger: BaseLoggerTemplate)`**
   - Sets the logger template to be used by the singleton.
   - **Inputs**:
     | Entity       | Type                 | Role                          | Notes                                  |
     |--------------|----------------------|-------------------------------|----------------------------------------|
     | `logger`     | `BaseLoggerTemplate` | Logger template instance      | Instance of a logger template class.   |

2. **`log(log: BaseLog)`**
   - Logs a message using the configured logger template.

---

> **Note:** The `BaseLogger` singleton ensures consistent logging behavior across the application, while the `DocSchema` classes provide a structured approach to managing documentation data.
<a name="progress-management"></a>
## **Progress Management Classes**

This section describes the implementation of progress tracking and task management within the Auto Doc Generator system. It includes the `BaseProgress` abstract class and its concrete implementations: `LibProgress` and `ConsoleGtiHubProgress`. These classes provide mechanisms for monitoring and updating the progress of tasks, either through a console-based interface or using the `rich.progress` library.

---

### **`BaseProgress` Class**

The `BaseProgress` class serves as an abstract base class for progress tracking. It defines the interface for creating, updating, and removing subtasks.

#### **Methods**
1. **`create_new_subtask(name: str, total_len: int)`**
   - Abstract method to create a new subtask with a specific name and total length.

2. **`update_task()`**
   - Abstract method to update the progress of the current task or subtask.

3. **`remove_subtask()`**
   - Abstract method to remove the current subtask.

---

### **`LibProgress` Class**

The `LibProgress` class extends `BaseProgress` and integrates with the `rich.progress` library for advanced progress tracking. It supports both general progress tracking and subtask-specific progress.

#### **Attributes**
| Attribute         | Type          | Description                                                                 |
|-------------------|---------------|-----------------------------------------------------------------------------|
| `progress`        | `Progress`    | Instance of the `rich.progress.Progress` class for managing progress bars.  |
| `_base_task`      | `TaskID`      | Identifier for the general progress task.                                   |
| `_cur_sub_task`   | `TaskID` or `None` | Identifier for the current subtask, if any.                                |

#### **Methods**
1. **`__init__(progress: Progress, total=5)`**
   - Initializes the `LibProgress` instance with a `Progress` object and sets up the general progress task.
   - **Inputs**:
     | Entity       | Type         | Role                          | Notes                                  |
     |--------------|--------------|-------------------------------|----------------------------------------|
     | `progress`   | `Progress`   | Progress manager              | Instance of `rich.progress.Progress`.  |
     | `total`      | `int`        | Total steps for general task  | Defaults to 5.                         |

2. **`create_new_subtask(name: str, total_len: int)`**
   - Creates a new subtask with the specified name and total length.
   - **Inputs**:
     | Entity       | Type         | Role                          | Notes                                  |
     |--------------|--------------|-------------------------------|----------------------------------------|
     | `name`       | `str`        | Subtask name                  | Name of the subtask.                   |
     | `total_len`  | `int`        | Subtask total length          | Total number of steps for the subtask. |

3. **`update_task()`**
   - Updates the progress of the current subtask. If no subtask is active, updates the general progress task.

4. **`remove_subtask()`**
   - Removes the current subtask by setting `_cur_sub_task` to `None`.

---

### **`ConsoleTask` Class**

The `ConsoleTask` class provides a simple console-based implementation for tracking the progress of individual tasks. It is used within the `ConsoleGtiHubProgress` class.

#### **Attributes**
| Attribute          | Type           | Description                                                                 |
|--------------------|----------------|-----------------------------------------------------------------------------|
| `name`             | `str`          | Name of the task.                                                           |
| `total_len`        | `int`          | Total number of steps for the task.                                         |
| `current_len`      | `int`          | Current progress of the task.                                               |

#### **Methods**
1. **`__init__(name: str, total_len: int)`**
   - Initializes a new console task and starts it.
   - **Inputs**:
     | Entity       | Type         | Role                          | Notes                                  |
     |--------------|--------------|-------------------------------|----------------------------------------|
     | `name`       | `str`        | Task name                     | Name of the task to be tracked.        |
     | `total_len`  | `int`        | Total task length             | Total number of steps for the task.    |

2. **`start_task()`**
   - Initializes the task's progress and prints a starting message.

3. **`progress()`**
   - Updates the task's progress and prints the current percentage.

---

### **`ConsoleGtiHubProgress` Class**

The `ConsoleGtiHubProgress` class extends `BaseProgress` and provides a console-based implementation for tracking progress. It uses `ConsoleTask` to manage individual tasks and a general progress task.

#### **Attributes**
| Attribute          | Type           | Description                                                                 |
|--------------------|----------------|-----------------------------------------------------------------------------|
| `curr_task`        | `ConsoleTask`  | The current subtask being tracked.                                          |
| `gen_task`         | `ConsoleTask`  | The general progress task.                                                  |

#### **Methods**
1. **`__init__()`**
   - Initializes the `ConsoleGtiHubProgress` instance and sets up the general progress task.

2. **`create_new_subtask(name: str, total_len: int)`**
   - Creates a new console-based subtask.
   - **Inputs**:
     | Entity       | Type         | Role                          | Notes                                  |
     |--------------|--------------|-------------------------------|----------------------------------------|
     | `name`       | `str`        | Subtask name                  | Name of the subtask.                   |
     | `total_len`  | `int`        | Subtask total length          | Total number of steps for the subtask. |

3. **`update_task()`**
   - Updates the progress of the current subtask. If no subtask is active, updates the general progress task.

4. **`remove_subtask()`**
   - Removes the current subtask by setting `curr_task` to `None`.

---

> **Note:** The `BaseProgress` and its derived classes provide a flexible framework for tracking progress in different environments, whether using a rich graphical interface or a simple console-based approach. These classes are essential for monitoring the execution of long-running tasks in the Auto Doc Generator system.
<a name="install-sh"></a>
## **`install.sh` Script**

The `install.sh` script is a setup script designed to initialize the necessary configuration files and GitHub Actions workflow for the **Auto Doc Generator** project. It ensures that the required directory structure and configuration files are created and populated with the appropriate content.

---

### **Script Functionality**

1. **Create Workflow Directory**
   - Ensures the existence of the `.github/workflows` directory using the `mkdir -p` command.

2. **Generate GitHub Actions Workflow (`autodoc.yml`)**
   - Creates a GitHub Actions workflow file (`autodoc.yml`) in the `.github/workflows` directory.
   - The workflow is configured to use a reusable workflow located in the `Drag-GameStudio/ADG` repository.
   - The workflow is triggered manually using the `workflow_dispatch` event.
   - Injects the `GROCK_API_KEY` secret into the workflow, escaping the `$` symbol to ensure proper syntax.

3. **Generate AutoDoc Configuration File (`autodocconfig.yml`)**
   - Creates a configuration file (`autodocconfig.yml`) in the root directory.
   - The configuration file includes:
     - **Project Metadata:** Project name and language.
     - **Ignore Files:** A list of file patterns and directories to exclude from the documentation process.
     - **Build Settings:** Options for saving logs and setting log verbosity levels.
     - **Structure Settings:** Options for including introduction links, text, order, and global file settings. Also specifies the maximum size for documentation parts.

4. **Completion Messages**
   - Prints success messages after creating the `autodoc.yml` and `autodocconfig.yml` files.

---

### **Key Components**

#### **GitHub Actions Workflow (`autodoc.yml`)**
The workflow is designed to integrate with the **Auto Doc Generator** repository and execute a reusable workflow. Below is the content of the generated `autodoc.yml` file:

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

#### **AutoDoc Configuration File (`autodocconfig.yml`)**
The configuration file defines the behavior and settings for the Auto Doc Generator. Below is a breakdown of its sections:

- **Project Metadata:**
  - `project_name`: Automatically set to the name of the current directory.
  - `language`: Default language for the documentation (`en`).

- **Ignore Files:**
  - Specifies patterns for files and directories to exclude from the documentation process. Examples include Python bytecode files, cache directories, environment folders, logs, and version control files.

- **Build Settings:**
  - `save_logs`: Boolean flag to enable or disable saving logs.
  - `log_level`: Integer value to set the verbosity of logs (e.g., 2 for warnings and errors).

- **Structure Settings:**
  - `include_intro_links`: Boolean flag to include introductory links in the documentation.
  - `include_intro_text`: Boolean flag to include introductory text in the documentation.
  - `include_order`: Boolean flag to include ordering of documentation sections.
  - `use_global_file`: Boolean flag to enable the use of a global file for documentation.
  - `max_doc_part_size`: Integer value specifying the maximum size (in characters) for each documentation part.

---
<a name="pyproject-toml"></a>
## **`pyproject.toml` File**

The `pyproject.toml` file defines the metadata, dependencies, and build configuration for the **Auto Doc Generator** project. It adheres to the [PEP 621](https://peps.python.org/pep-0621/) standard.

---

### **Key Sections**

#### **[project]**
| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| `name`             | `autodocgenerator`                                                  |
| `version`          | `1.6.6.3`                                                           |
| `description`      | "This Project helps you to create docs for your projects"           |
| `authors`          | `[{name = "dima-on", email = "sinica911@gmail.com"}]`               |
| `license`          | `MIT`                                                               |
| `readme`           | `README.md`                                                         |
| `requires-python`  | `>=3.11,<4.0`                                                       |
| `dependencies`     | List of required Python packages (see below).                       |

- **Dependencies:**
  - Includes a comprehensive list of Python libraries required for the project, such as `pydantic`, `openai`, `pyyaml`, and `rich`.

#### **[tool.poetry]**
| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| `exclude`          | `[".auto_doc_cache_file.json"]`                                      |

- Specifies files to exclude during packaging.

#### **[build-system]**
| Field              | Value                                                                 |
|--------------------|-----------------------------------------------------------------------|
| `requires`         | `["poetry-core>=2.0.0"]`                                             |
| `build-backend`    | `"poetry.core.masonry.api"`                                          |

- Defines the build system requirements and backend.

---

### **Key Notes**
1. **Dependencies:**
   - The project relies on several libraries for functionality, including:
     - **AI Integration:** `openai`, `google-genai`, `azure-ai-inference`.
     - **Data Handling:** `pydantic`, `pyyaml`, `numpy`.
     - **Progress Tracking:** `rich`, `rich_progress`.
     - **HTTP Requests:** `httpx`, `requests`.

2. **Exclusion Rules:**
   - The `.auto_doc_cache_file.json` file is excluded from packaging to prevent unnecessary cache files from being included in the distribution.

3. **Build System:**
   - Uses `poetry` for dependency management and building the project.

---

This setup ensures that the **Auto Doc Generator** project is properly configured for development, deployment, and integration with GitHub Actions. The `install.sh` script automates the initialization process, while the `pyproject.toml` file provides a robust foundation for managing dependencies and project metadata.
<a name="manager-class-description"></a>

The `Manager` class is used to manage the generation of documentation for a project. It interacts with models, embedding layers, progress bars, and other modules to create and organize documentation. Below is a description of its usage and available methods based on the provided context.

### Usage of `Manager` Class
The `Manager` class is instantiated with the following parameters:
- `project_path`: Path to the project directory.
- `config`: Configuration object (`Config`) containing settings for documentation generation.
- `llm_model`: A language model instance (e.g., `GPT4oModel`, `AzureModel`, or `GPTModel`).
- `embedding_model`: An embedding model instance (`Embedding`).
- `progress_bar`: A progress bar instance (`ConsoleGtiHubProgress`).

### Example Usage
```python
from autodocgenerator.manage import Manager
from autodocgenerator.engine.models.gpt_model import GPT4oModel
from autodocgenerator.postprocessor.embedding import Embedding
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.config.env_config import env_config

# Initialize models
llm_model = GPT4oModel(env_config.models_api_keys, use_random=False)
embedding_model = Embedding(env_config.google_embedding_api_key)

# Create Manager instance
manager = Manager(
    project_path="path/to/project",
    config=config_object,
    llm_model=llm_model,
    embedding_model=embedding_model,
    progress_bar=ConsoleGtiHubProgress()
)

# Example method calls
manager.load_all_info()
manager.save()
manager.generate_code_file()
manager.generate_global_info(compress_power=4, is_reusable=True)
manager.generete_doc_parts(max_symbols=1000, with_global_file=True)
manager.factory_generate_doc(custom_factory_instance)
manager.order_doc()
manager.create_embedding_layer()
manager.clear_cache()
```

### Available Methods
1. **`load_all_info()`**: Loads all necessary information for documentation generation.
2. **`save()`**: Saves the current state of the manager, including generated documentation.
3. **`generate_code_file()`**: Generates a code file based on the project structure and settings.
4. **`generate_global_info(compress_power: int, is_reusable: bool)`**: Generates global information for the documentation, with options for compression and reusability.
5. **`generete_doc_parts(max_symbols: int, with_global_file: bool)`**: Generates parts of the documentation with a specified maximum size and optional inclusion of global files.
6. **`factory_generate_doc(factory_instance)`**: Uses a factory instance (`DocFactory`) to generate documentation based on custom modules.
7. **`order_doc()`**: Orders the documentation based on predefined structure or settings.
8. **`create_embedding_layer()`**: Creates an embedding layer for the documentation.
9. **`clear_cache()`**: Clears cached data related to the documentation generation process.

### Notes
- The `Manager` class is central to the workflow and integrates multiple components to streamline the documentation generation process.
- It relies on external configurations (`Config`, `StructureSettings`) and modules (`DocFactory`, `BaseModule`) for customization and extensibility.

    