# Project Overview: Auto Doc Generator

## **Project Title**
Auto Doc Generator (ADG)

---

## **Project Goal**
The Auto Doc Generator (ADG) is a modular and extensible software solution designed to automate the creation of structured, comprehensive, and up-to-date documentation for software projects. By leveraging AI models, modular components, and text processing techniques, ADG analyzes codebases, detects changes, and dynamically generates documentation. This tool is particularly suited for integration into CI/CD pipelines, ensuring that project documentation remains current with minimal manual intervention. 

---

## **Core Logic & Principles**

The Auto Doc Generator employs a **layered architecture** to ensure modularity, scalability, and maintainability. The system is divided into multiple components, each responsible for a specific aspect of the documentation generation process. Below is an overview of the core logic and principles:

### **1. Initialization**
- The process begins with the `run_file.py` script, which serves as the main entry point.
- The `autodocconfig.yml` configuration file is parsed by the `config_reader.py` module to initialize project-specific settings, such as ignored files, language preferences, and metadata.
- API tokens and environment variables are managed by the `token_auth.py` module to enable secure communication with external services.

### **2. Change Detection**
- The `check_git_status.py` module analyzes Git repository changes by comparing the current state with the last commit. If no changes are detected, the process terminates early, saving computational resources.

### **3. Documentation Generation**
- The `Manager` class orchestrates the documentation generation lifecycle, which includes:
  - **Codebase Analysis**: The `CodeMix` module builds a structured representation of the repository's content, filtering out ignored files and directories.
  - **Global Information Generation**: The `compressor.py` and `spliter.py` modules process global project information, compressing and splitting data into manageable chunks.
  - **Modular Documentation Creation**: The `DocFactory` invokes a sequence of modular components (e.g., `CustomModule`, `IntroLinks`, `IntroText`) to generate specific sections of the documentation.
  - **Embedding and Sorting**: The `embedding.py` module generates semantic embeddings for document parts, while the `sorting.py` module organizes and reorders content for better readability.

### **4. Post-Processing**
- Generated documentation undergoes enhancement and optimization through modules such as `custom_intro.py`, `embedding.py`, and `sorting.py`. These modules ensure the documentation is well-structured, concise, and easy to navigate.

### **5. Publishing**
- The final documentation is saved locally in `.auto_doc_cache_file.json` and uploaded to a remote server using the `post_to_server.py` module. Logs are generated and saved to `agd_report.txt` for debugging and monitoring purposes.

### **6. Extensibility**
- The system is designed for flexibility, allowing developers to add new AI models by extending the `ParentModel` class or integrate new documentation components via the `DocFactory` and `BaseModule` interface.

---

## **Key Features**
- **Automated Documentation Updates**: Automatically detects changes in the codebase and updates documentation accordingly.
- **AI-Powered Content Generation**: Utilizes advanced AI models (e.g., Azure, GPT-3, GPT-4) to generate high-quality documentation.
- **Modular Design**: Supports the addition of new documentation components and AI models with minimal effort.
- **Preprocessing and Post-Processing**: Includes utilities for compressing, splitting, embedding, and organizing documentation content.
- **CI/CD Integration**: Seamlessly integrates with GitHub Actions for automated documentation generation during the CI/CD pipeline.
- **Customizable Configurations**: Allows users to define project-specific settings, such as ignored files, language preferences, and metadata, via a YAML configuration file.
- **Error Handling and Logging**: Provides robust error handling with custom exceptions and detailed logging for debugging and monitoring.
- **Semantic Search**: Adds embedding layers to documentation for enhanced search capabilities.

---

## **Dependencies**
To run the Auto Doc Generator, the following libraries and tools are required:

1. **Programming Language**:
   - Python (version 3.8 or higher)

2. **Libraries**:
   - AI model libraries (e.g., Azure, OpenAI, Groq APIs)
   - YAML parsing library (e.g., `PyYAML`)
   - Git interaction library (e.g., `GitPython`)
   - Logging utilities (e.g., `logging` module)
   - JSON handling library (e.g., `json` module)
   - Subprocess module for shell command execution

3. **External Tools**:
   - Git: For change detection and repository analysis.
   - GitHub Actions: For CI/CD pipeline integration.

4. **Configuration Files**:
   - `autodocconfig.yml`: Defines project-specific settings.
   - `.auto_doc_cache_file.json`: Stores cached documentation data.

5. **Environment Variables**:
   - `ADG_API_TOKEN`: API key for authenticating with external services.
   - `DEFAULT_SERVER_URL`: Endpoint for uploading generated documentation.
   - `GITHUB_EVENT_NAME`: GitHub event that triggers the workflow.

---

## **Conclusion**
The Auto Doc Generator is a cutting-edge tool that streamlines the documentation process for software projects. By leveraging AI-driven content generation, modular architecture, and CI/CD integration, ADG ensures that project documentation remains accurate, up-to-date, and easy to navigate. Its extensible design and robust error-handling mechanisms make it a reliable and scalable solution for modern software development teams.
## Executive Navigation Tree

### 📂 Repository Structure
- [Repo Structure](#repo-structure)
- [Codemix Build Repo Content](#codemix-build-repo-content)
- [Content Description](#CONTENT_DESCRIPTION)
- [Pyproject.toml](#pyproject-toml)
- [Install Script](#install-script)
- [Install Workflow Scripts and API Key Setup](#install-workflow-scripts-and-api-key-setup)

### 📄 Configuration & Settings
- [Autodocconfig Options](#autodocconfig-options)
- [Git Status Check](#git-status-check)
- [Check Git Status Result Schema Class](#check-git-status-result-schema-class)
- [Config Reader](#config-reader)
- [Config Module](#config-module)
- [Projectsettings Class](#projectsettings-class)
- [Cache Settings Class](#cache-settings-class)
- [Token Auth](#token-auth)

### ⚙️ Logging & Exceptions
- [Exceptions Module](#exceptions-module)
- [Logging](#logging)
  - [Base Log Class](#base-log-class)
  - [Error Log Class](#error-log-class)
  - [Warning Log Class](#warning-log-class)
  - [Info Log Class](#info-log-class)
  - [Base Logger Template Class](#base-logger-template-class)
  - [File Logger Template Class](#file-logger-template-class)
  - [Base Logger Class](#base-logger-class)

### 📊 Progress Management
- [Post to Server](#post-to-server)
- [Run File](#run-file)
- [Progress Management](#progress-management)
  - [Lib Progress Class](#lib-progress-class)
  - [Console Task Class](#console-task-class)
  - [Console Github Progress Class](#console-github-progress-class)

### 🤖 AI Models
- [Azure Model](#azure-model)
- [GPT Model Class](#gpt-model-class)
- [History Class](#history-class)
- [Parentmodel Class](#parentmodel-class)
- [Model Asyncmodel Classes](#model-asyncmodel-classes)
- [Embedding Class](#embedding-class)
- [Embedding Functions](#embedding-functions)

### 🔍 Data Processing
- [Sorting Functions](#sorting-functions)
- [Checker Parse Answer](#checker-parse-answer)
- [Checker Have to Change](#checker-have-to-change)
- [Codemix Should Ignore](#codemix-should-ignore)
- [Compressor Functions](#compressor-functions)
- [Split Data Function](#split-data-function)
- [Write Docs by Parts Function](#write-docs-by-parts-function)
- [Gen Doc Parts Function](#gen-doc-parts-function)

### 📄 Documentation Factory
- [Docfactory Class](#docfactory-class)
- [Doc Content Class](#doc-content-class)
- [Doc Schema](#doc-schema)
  - [Doc Head Schema Class](#doc-head-schema-class)
  - [Doc Info Schema Class](#doc-info-schema-class)

### 🛠️ Modules
- [Basemodule Class](#basemodule-class)
- [Custommodule Class](#custommodule-class)
- [Custommodulewithoutcontext Class](#custommodulewithoutcontext-class)

### 📚 Introduction & Postprocessing
- [Intro Links Class](#intro-links-class)
- [Intro Text Class](#intro-text-class)
- [Postprocessor Custom Intro](#postprocessor-custom-intro)

### 🗂️ Manager
- [Manager Class Usage and Methods](#manager-class-usage-and-methods)
<a name="repo-structure"></a>
## Repository Structure Overview

This section outlines the hierarchical structure of the Auto Doc Generator repository, detailing the organization of files and directories that support the CI/CD workflows and the core functionality of the documentation generation system.

---

### **Directory Tree**

```plaintext
.github/
  workflows/
    autodoc.yml
    main.yml
    reuseble_agd.yml
agd_report.txt
autodocconfig.yml
autodocgenerator/
  __init__.py
  auto_runner/
    check_git_status.py
    config_reader.py
    post_to_server.py
    run_file.py
    token_auth.py
  config/
    config.py
  engine/
    __init__.py
    config/
      config.py
    exceptions.py
    models/
      azure_model.py
      gpt_model.py
      model.py
  factory/
    __init__.py
    base_factory.py
    modules/
      general_modules.py
      intro.py
  manage.py
  postprocessor/
    custom_intro.py
    embedding.py
    sorting.py
  preprocessor/
    checker.py
    code_mix.py
    compressor.py
    settings.py
    spliter.py
  schema/
    cache_settings.py
    doc_schema.py
  ui/
    __init__.py
    logging.py
    progress_base.py
install.ps1
install.sh
poetry.lock
pyproject.toml
```

---

### **Key Files and Directories**

#### **1. `.github/workflows/`**
- **Purpose:** Contains GitHub Actions workflows for CI/CD automation and documentation generation.
- **Files:**
  - `autodoc.yml`: Triggers the AutoDoc workflow on `push` events to the `main` branch or manual dispatch.
  - `main.yml`: Handles CI/CD tasks such as dependency installation and publishing the library to PyPI.
  - `reuseble_agd.yml`: A reusable workflow for generating documentation, posting it to a server, and committing changes.

#### **2. `autodocconfig.yml`**
- **Purpose:** Configuration file for the Auto Doc Generator system. Defines settings such as ignored files, language preferences, and metadata for documentation generation.

#### **3. `autodocgenerator/`**
- **Purpose:** Core directory containing the implementation of the Auto Doc Generator system.
- **Subdirectories:**
  - **`auto_runner/`:** Handles execution workflows, including Git status checks, configuration parsing, API communication, and main entry points.
  - **`config/`:** Manages project-specific configurations.
  - **`engine/`:** Implements AI models and exception handling for documentation generation.
  - **`factory/`:** Provides modular components for generating specific documentation sections.
  - **`postprocessor/`:** Enhances and organizes documentation content.
  - **`preprocessor/`:** Validates and prepares data for documentation generation.
  - **`schema/`:** Defines schemas for caching and documentation structure.
  - **`ui/`:** Contains utilities for logging and progress tracking.

#### **4. `install.ps1` & `install.sh`**
- **Purpose:** Scripts for installing dependencies and setting up the environment on Windows (`.ps1`) and Unix-based systems (`.sh`).

#### **5. `pyproject.toml` & `poetry.lock`**
- **Purpose:** Configuration files for managing Python dependencies using Poetry.

#### **6. `agd_report.txt`**
- **Purpose:** Log file generated during the documentation process, containing information about errors, warnings, and model usage.

---

### **Functional Flow of Workflows**

#### **Autodoc Workflow (`autodoc.yml`)**
- **Trigger:** Push to `main` branch or manual dispatch.
- **Steps:**
  1. **Run Job:** Executes the reusable workflow defined in `reuseble_agd.yml`.
  2. **Secrets Management:** Utilizes `ADG_API_TOKEN` for authentication.

#### **Reusable Workflow (`reuseble_agd.yml`)**
- **Trigger:** Workflow call with required secrets.
- **Steps:**
  1. **Checkout Code:** Fetches repository code with full history.
  2. **Python Setup:** Installs Python 3.12 and the `autodocgenerator` package.
  3. **API Key Retrieval:** Runs `token_auth.py` to fetch API keys for external services.
  4. **Documentation Generation:** Executes `run_file.py` to generate documentation.
  5. **Post to Server:** Sends generated documentation to a remote server using `post_to_server.py`.
  6. **Output Handling:** Copies generated documentation to `README.md` and logs to `agd_report.txt`.
  7. **Commit and Push:** Updates the repository with new documentation and logs.

#### **CI/CD Workflow (`main.yml`)**
- **Trigger:** Push or pull request to `main` branch affecting `pyproject.toml`.
- **Steps:**
  1. **Checkout Code:** Fetches repository code.
  2. **Python Setup:** Installs Python 3.12 and Poetry.
  3. **Dependency Installation:** Installs project dependencies using Poetry.
  4. **Library Publishing:** Publishes the library to PyPI using Poetry.

---

### **Key Context for Workflow Integration**

| **Entity**              | **Type**       | **Role**                                | **Notes**                                                                 |
|--------------------------|----------------|-----------------------------------------|---------------------------------------------------------------------------|
| `ADG_API_TOKEN`          | Secret         | API key for server authentication       | Required for posting documentation to the server.                        |
| `DEFAULT_SERVER_URL`     | Environment Var| URL of the documentation server         | Used by `post_to_server.py`.                                             |
| `pyproject.toml`         | File           | Defines project dependencies            | Triggers CI/CD workflow on changes.                                      |
| `README.md`              | File           | Repository documentation                | Updated with generated documentation.                                    |
| `.auto_doc_cache_file.json` | File        | Cache file for generated documentation  | Contains structured documentation data.                                  |
| `agd_report.txt`         | File           | Log file for documentation generation   | Contains logs from the documentation generation process.                 |

---

### **Critical Notes**
> - The repository is structured to support modular development, allowing for easy integration of new features and components.
> - GitHub Actions workflows are designed for seamless automation of documentation generation and library publishing.
> - The Auto Doc Generator relies heavily on external API keys and AI models for content generation and processing.

markdown
<a name="codemix-build-repo-content"></a>
## **Function: `build_repo_content`**

#### **Purpose**
Generates a structured representation of the repository's content, including directory structure and file contents.

#### **Technical Logic Flow**
1. Initializes a list with the header "Repository Structure:".
2. Iterates through all files and directories in the root directory:
   - Skips paths that match ignore patterns using `should_ignore`.
   - Logs ignored paths using `InfoLog`.
   - Adds directory names with indentation based on depth.
   - Adds file names without indentation.
3. Appends a separator line (`=`) to the content list.
4. Iterates through all files:
   - Reads file contents unless the file matches ignore patterns.
   - Handles exceptions for unreadable files and logs errors.
5. Returns the repository structure and file contents as a single string.

#### **Parameters**
| Entity         | Type                     | Role                           | Notes                                   |
|----------------|--------------------------|--------------------------------|-----------------------------------------|
| `root_dir`     | `str`                    | Root Directory Path            | Path of the repository to analyze.     |
| `ignore_patterns` | `list[str]`           | Ignore Patterns                | Patterns to exclude from the analysis. |

#### **Output**
| Entity         | Type                     | Role                           | Notes                                   |
|----------------|--------------------------|--------------------------------|-----------------------------------------|
| `content`      | `str`                    | Repository Content             | Structured representation of the repository. |

---

### **Critical Notes**
> - **Error Handling:** The `build_repo_content` function gracefully handles file read errors and logs them in the output.
> - **Ignore Patterns:** The `should_ignore` function uses `fnmatch` for pattern matching, ensuring flexibility in specifying ignore rules.
> - **Logging Integration:** Ignored paths and errors are logged using the `InfoLog` class for traceability.

---

### **Shared Observations**
1. **AI Model Dependency**:
   - The `have_to_change` function relies on the `Model` class for decision-making based on code changes and global information.
2. **Structured Output**:
   - The `build_repo_content` function provides a detailed and hierarchical view of the repository, making it suitable for documentation generation.
3. **Extensibility**:
   - The `CodeMix` class and its methods are designed to be modular, allowing customization of ignore patterns and logging behavior.
<a name="CONTENT_DESCRIPTION"></a>` tag, no filenames, extensions, or generic terms).
  - Sends the prompt to the AI model to generate a description.

---

### **Data Contract**

| Entity                      | Type               | Role                               | Notes                                                                 |
|-----------------------------|--------------------|------------------------------------|-----------------------------------------------------------------------|
| `data`                      | `str`              | Input Data                        | Raw documentation data containing HTML links.                        |
| `links`                     | `list[str]`        | Extracted Links                   | List of HTML links extracted from the input data.                    |
| `model`                     | `Model`            | AI Model                          | Used for generating introductions and descriptions.                  |
| `language`                  | `str`              | Language Setting                  | Specifies the language for generated content.                        |
| `global_data`               | `str`              | Global Project Info               | Contains reusable global documentation data.                         |
| `custom_description`        | `str`              | Custom Description Task           | User-defined task for generating specific content.                   |
| `splited_data`              | `list[str]`        | Split Data Chunks                 | Smaller chunks of data for iterative processing.                     |
| `intro_links`               | `str`              | Generated Link-Based Introduction | Final output of the link-based introduction generation.              |
| `intro`                     | `str`              | Generated Global Introduction     | Final output of the global introduction generation.                  |
| `result`                    | `str`              | Generated Custom Description      | Final output of the custom description generation process.           |

---

### **Critical Notes**
> - **Regex-Based Link Extraction:** The `get_all_html_links` function relies on regex patterns to identify anchor links. Ensure that the input data adheres to the expected format for accurate extraction.
> - **AI Model Dependency:** All introduction and description generation functions depend heavily on the `Model` class for processing prompts and generating content.
> - **Strict Formatting Rules:** The `generete_custom_discription_without` function enforces strict rules for content formatting, ensuring consistency and adherence to predefined standards.

---

### **Shared Observations**
1. **Logging Integration**:
   - All major functions use `BaseLogger` for logging progress and outputs, improving traceability during execution.

2. **Language Flexibility**:
   - Functions support multi-language outputs by accepting a `language` parameter, making the module adaptable for diverse documentation needs.

3. **Iterative Processing**:
   - The `generete_custom_discription` function processes data chunks iteratively, ensuring that valid descriptions are generated even if some chunks fail.

4. **Predefined Prompts**:
   - The module relies on predefined instructions (`BASE_INTRODACTION_CREATE_LINKS`, `BASE_INTRO_CREATE`, `BASE_CUSTOM_DISCRIPTIONS`) for consistent content generation across different tasks.

markdown
<a name="pyproject-toml"></a>
## **Python Project Configuration: `pyproject.toml`**

#### **Purpose**
Defines the metadata, dependencies, and build settings for the Auto Doc Generator project.

---

### **Key Sections**
#### **1. Project Metadata**
| Field              | Value                          | Notes                                   |
|--------------------|--------------------------------|-----------------------------------------|
| `name`             | `"autodocgenerator"`          | Name of the project.                   |
| `version`          | `"1.6.0.9"`                   | Current version of the project.        |
| `description`      | `"This Project helps you to create docs for your projects"` | Brief description of the project.      |
| `authors`          | `[{name = "dima-on", email = "sinica911@gmail.com"}]` | Author information.                    |
| `license`          | `"MIT"`                       | License type.                          |
| `readme`           | `"README.md"`                 | Path to the README file.               |
| `requires-python`  | `">=3.11,<4.0"`               | Python version compatibility.          |

---

#### **2. Dependencies**
Specifies the required Python packages for the project. Key dependencies include:
- **AI and ML Libraries**: `openai`, `azure-ai-inference`, `numpy`
- **Data Handling**: `pyyaml`, `fastjsonschema`, `pydantic`
- **Utilities**: `requests`, `tqdm`, `rich`
- **Version Control**: `dulwich`
- **Caching**: `CacheControl`

---

#### **3. Build Settings**
| Field              | Value                          | Notes                                   |
|--------------------|--------------------------------|-----------------------------------------|
| `requires`         | `["poetry-core>=2.0.0"]`      | Specifies the build system requirements. |
| `build-backend`    | `"poetry.core.masonry.api"`    | Defines the backend for building the project. |

---

#### **4. Poetry Exclusions**
| Field              | Value                          | Notes                                   |
|--------------------|--------------------------------|-----------------------------------------|
| `exclude`          | `[".auto_doc_cache_file.json"]` | Excludes specific files from the build process. |

---

### **Critical Notes**
> - **Dependency Management**: Ensures all required libraries are installed for the project to function correctly.
> - **Python Compatibility**: Restricts the project to Python versions `>=3.11` and `<4.0`.
> - **Build System**: Uses Poetry for dependency management and packaging.

---

### **Summary**
The `install.sh` script and `pyproject.toml` file together streamline the setup and configuration of the Auto Doc Generator project. The script automates the creation of essential configuration files, while the `pyproject.toml` file defines the project's dependencies, metadata, and build settings. This setup ensures a seamless and efficient initialization process for developers.
<a name="install-script"></a>
## **Bash Script: `install.sh`**

#### **Purpose**
Automates the setup of the Auto Doc Generator project by creating required configuration files and directories.

---

### **Functionality**
1. **Directory Creation**:
   - Ensures the `.github/workflows` directory exists before generating the GitHub Actions workflow file.

2. **GitHub Workflow File Generation**:
   - Creates the `autodoc.yml` file for GitHub Actions workflow.
   - Configures the workflow to use the reusable workflow `reuseble_agd.yml` from the `Drag-GameStudio/ADG` repository.
   - Includes secret handling for `GROCK_API_KEY`.

3. **Project Configuration File Generation**:
   - Generates the `autodocconfig.yml` file with project-specific settings:
     - Dynamically sets the project name based on the current folder name.
     - Configures language settings, ignored files, build settings, and structure settings.

---

### **Key Variables**
| Variable             | Type         | Role                           | Notes                                   |
|----------------------|--------------|---------------------------------|-----------------------------------------|
| `$content`           | `string`     | GitHub Workflow Configuration  | Contains the YAML configuration for the workflow. |
| `$currentFolderName` | `string`     | Current Folder Name            | Dynamically retrieves the name of the current directory. |
| `$configContent`     | `string`     | Project Configuration Content  | Contains the YAML configuration for `autodocconfig.yml`. |

---

### **Generated Files**
#### **1. `.github/workflows/autodoc.yml`**
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
> **Note**: The `$` symbol is escaped for proper interpretation in the Bash script.

#### **2. `autodocconfig.yml`**
```yaml
project_name: "<current-folder-name>"
language: "en"

ignore_files:
  # Python bytecode and cache
  - "*.pyc"
  - "*.pyo"
  - "*.pyd"
  - "__pycache__"
  - ".ruff_cache"
  - ".mypy_cache"
  - ".auto_doc_cache"
  - ".auto_doc_cache_file.json"

  # Environments and IDE settings
  - "venv"
  - "env"
  - ".venv"
  - ".env"
  - ".vscode"
  - ".idea"
  - "*.iml"

  # Databases and binary data
  - "*.sqlite3"
  - "*.db"
  - "*.pkl"
  - "data"

  # Logs and coverage reports
  - "*.log"
  - ".coverage"
  - "htmlcov"

  # Version control and assets
  - ".git"
  - ".gitignore"
  - "migrations"
  - "static"
  - "staticfiles"

  # Miscellaneous
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
> **Dynamic Project Name**: The `project_name` is automatically set to the name of the current directory using `basename "$PWD"`.

---

### **Critical Notes**
> - **Directory Creation**: Ensures the `.github/workflows` directory exists before generating the workflow file.
> - **Dynamic Project Name**: Automatically sets the project name in `autodocconfig.yml` based on the current folder name.
> - **Ignored Files**: Includes a comprehensive list of file patterns to exclude from documentation generation.
> - **Extensibility**: The script can be modified to include additional settings or configurations as needed.

---
<a name="install-workflow-scripts-and-api-key-setup"></a> The installation workflow involves using platform-specific scripts (`install.ps1` for PowerShell and `install.sh` for Linux-based systems) to set up the required environment. Below is a detailed explanation:

### Installation Process

1. **PowerShell Installation**:
   - Execute the following command in PowerShell to run the `install.ps1` script:
     ```powershell
     irm https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.ps1 | iex
     ```
     This command uses `Invoke-RestMethod` (`irm`) to fetch the script from the specified URL and pipes it to `Invoke-Expression` (`iex`) for execution.

2. **Linux-Based Systems Installation**:
   - Run the following command in the terminal to execute the `install.sh` script:
     ```bash
     curl -sSL https://raw.githubusercontent.com/Drag-GameStudio/ADG/main/install.sh | bash
     ```
     Here, `curl` fetches the script from the provided URL, and the `bash` command executes it directly.

### GitHub Actions Configuration

To ensure the workflow operates correctly, you need to add a secret variable to your GitHub Actions configuration:

1. **Secret Variable Setup**:
   - Navigate to your GitHub repository settings.
   - Under the "Secrets and variables" section, click on "Actions".
   - Add a new secret with the name `GROCK_API_KEY`.
   - Use the API key obtained from the [Grock documentation](https://grockdocs.com) as the value for this secret.

By following these steps, the installation scripts will be executed properly, and the required API key will be securely integrated into your GitHub Actions workflow.
<a name="autodocconfig-options"></a>

The `autodocconfig.yml` file is used to configure the behavior of the Auto Doc Generator project. Below are the available options and their descriptions based on the provided context:

1. **`project_name`**:  
   - Specifies the name of the project.  
   - Example: `"Auto Doc Generator"`

2. **`language`**:  
   - Defines the language of the documentation.  
   - Example: `"en"`

3. **`ignore_files`**:  
   - A list of files or directories to be ignored during the documentation generation process.  
   - Supports specific file names, file extensions (e.g., `*.pyc`), and directory names.  
   - Example:  
     ```yaml
     ignore_files:
       - "dist"
       - "*.pyc"
       - "__pycache__"
       - "venv"
       - ".git"
       ```

4. **`build_settings`**:  
   - Configures settings related to the build process.  
   - Options:  
     - `save_logs`: Boolean value to enable or disable saving logs.  
       - Example: `false`  
     - `log_level`: Integer value to set the verbosity of logs.  
       - Example: `2`  
     - `threshold_changes`: Integer value to define the maximum number of changes before triggering specific actions.  
       - Example: `20000`

5. **`structure_settings`**:  
   - Configures the structure of the generated documentation.  
   - Options:  
     - `include_intro_links`: Boolean value to include introductory links in the documentation.  
       - Example: `true`  
     - `include_intro_text`: Boolean value to include introductory text in the documentation.  
       - Example: `true`  
     - `include_order`: Boolean value to maintain the order of included sections.  
       - Example: `true`  
     - `use_global_file`: Boolean value to determine if a global file should be used.  
       - Example: `true`  
     - `max_doc_part_size`: Integer value to set the maximum size of a documentation part (in characters).  
       - Example: `4000`

6. **`project_additional_info`**:  
   - Provides a description or additional information about the project.  
   - Example:  
     ```yaml
     project_additional_info:
       global idea: "This project was created to help developers make documentations for them projects"
     ```

7. **`custom_descriptions`**:  
   - A list of custom descriptions or instructions to include in the documentation.  
   - Example:  
     ```yaml
     custom_descriptions:
       - "explain how to write autodocconfig.yml file what options are available"
       - "explain how to use Manager class and what methods are available"
     ```
<a name="git-status-check"></a>
## Git Status Check and Change Detection

This module is responsible for detecting changes in the Git repository to determine whether documentation updates are required. It analyzes the differences between the latest commit and the previous commit stored in the cache, and generates a detailed report of the changes.

---

### **Functional Role**
The `check_git_status` module performs the following tasks:
1. Retrieves the latest Git commit hash.
2. Compares the current state of the repository with the previous commit.
3. Generates a detailed report of added, deleted, and modified files.
4. Determines whether documentation updates are necessary based on the detected changes.

---

### **Technical Logic Flow**

1. **Retrieve Latest Commit Hash**:
   - The `get_git_revision_hash()` function uses the `git rev-parse HEAD` command to fetch the hash of the latest commit.

2. **Calculate Diff**:
   - The `get_diff_by_hash(target_hash)` function executes `git diff` to calculate the differences between the target commit and the current state of the repository. It excludes `.md` files from the comparison.

3. **Detailed Diff Statistics**:
   - The `get_detailed_diff_stats(target_hash)` function runs `git diff --numstat` to generate a detailed report of added, deleted, and modified files. It categorizes the changes as:
     - **ADDED**: Files added to the repository.
     - **DELETED**: Files removed from the repository.
     - **MODIFIED**: Files with both additions and deletions.

4. **Change Detection**:
   - The `check_git_status(manager)` function determines whether documentation updates are required based on the changes detected. If the GitHub event is `workflow_dispatch` or the cache does not contain a previous commit, it marks the documentation for regeneration.

---

### **Inputs, Outputs, and Parameters**

| **Entity**               | **Type**       | **Role**                                | **Notes**                                                                 |
|---------------------------|----------------|-----------------------------------------|---------------------------------------------------------------------------|
| `target_hash`             | `str`          | Target commit hash for comparison       | Used in `get_diff_by_hash` and `get_detailed_diff_stats`.                 |
| `manager.cache_settings`  | `CacheSettings`| Stores cached settings and last commit | Contains the last processed commit hash.                                  |
| `GITHUB_EVENT_NAME`       | `str`          | GitHub event triggering the workflow    | Determines if the workflow was manually triggered (`workflow_dispatch`).  |
| `changes`                 | `list[dict]`   | List of file change details             | Contains added, deleted, and modified file statistics.                    |
| `CheckGitStatusResultSchema` | `Schema`    | Result schema for change detection      | Indicates whether documentation updates are required.                     |

---

### **Function Breakdown**

#### **`get_git_revision_hash()`**
- **Purpose**: Fetches the latest Git commit hash.
- **Logic**: Executes `git rev-parse HEAD` and decodes the result.
- **Output**: Returns the commit hash as a string.

#### **`get_diff_by_hash(target_hash)`**
- **Purpose**: Retrieves the diff between the target commit and the current state.
- **Logic**: Executes `git diff` with the `HEAD` and `target_hash` arguments, excluding `.md` files.
- **Output**: Returns the diff as a string.

#### **`get_detailed_diff_stats(target_hash)`**
- **Purpose**: Generates a detailed report of file changes.
- **Logic**:
  - Executes `git diff --numstat`.
  - Parses the output to extract added, deleted, and modified file statistics.
  - Categorizes changes into `ADDED`, `DELETED`, and `MODIFIED`.
- **Output**: Returns a list of dictionaries containing file change details.

#### **`check_git_status(manager)`**
- **Purpose**: Determines if documentation updates are required.
- **Logic**:
  - Checks if the GitHub event is `workflow_dispatch` or if no previous commit is cached.
  - Fetches detailed diff statistics using `get_detailed_diff_stats`.
  - Calls `manager.check_sense_changes(changes)` to analyze the impact of changes.
- **Output**: Returns a `CheckGitStatusResultSchema` indicating whether updates are needed.

---

### **Critical Notes**
> - The module excludes `.md` files from the diff analysis to avoid unnecessary documentation regeneration.
> - If the GitHub event is `workflow_dispatch`, the documentation is always marked for regeneration.
> - File changes are categorized into `ADDED`, `DELETED`, and `MODIFIED` based on the number of lines added and deleted.



markdown
<a name="check-git-status-result-schema-class"></a>
## **Class: `CheckGitStatusResultSchema`**

### **Purpose**
Represents the result of checking the Git status to determine if documentation updates are needed.

### **Attributes**
| Attribute            | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `need_to_remake`     | `bool`             | Update Flag              | Indicates if documentation needs to be updated. |
| `remake_gl_file`     | `bool`             | Global File Update Flag  | Indicates if the global documentation file needs to be updated. |

---

### **Critical Notes**
> - **Iterative Processing:** The `gen_doc_parts` function processes chunks iteratively, ensuring scalability for large codebases.
> - **Caching:** The `CacheSettings` class enables efficient caching of documentation and commit data, reducing redundant processing.
> - **Progress Tracking:** The progress tracker provides real-time feedback during documentation generation, improving user experience.

markdown
<a name="config-reader"></a>
## `config_reader.py`: Configuration Parsing and Initialization

### **Functional Role**
The `config_reader.py` module is responsible for parsing the `autodocconfig.yml` file and initializing the core configuration objects (`Config`, `StructureSettings`, and custom modules). It serves as the entry point for setting up the documentation generation workflow based on user-defined settings.

---

### **Inputs, Outputs, and Parameters**

| **Entity**               | **Type**            | **Role**                                   | **Notes**                                                                 |
|---------------------------|---------------------|--------------------------------------------|---------------------------------------------------------------------------|
| `file_data`               | `str`               | YAML configuration file content            | Contains user-defined settings for the documentation generation process. |
| `data`                    | `dict[str, Any]`    | Parsed YAML data                           | Extracted from `file_data` using `yaml.safe_load`.                       |
| `Config`                  | `Config`            | Centralized configuration object           | Stores language, project name, ignored files, and additional info.       |
| `StructureSettings`       | `StructureSettings` | Defines structural rules for documentation | Includes settings like intro links, order, and global file usage.        |
| `custom_modules`          | `list[BaseModule]`  | List of modular components for documentation | Generated based on `custom_descriptions` in the YAML file.               |

---

### **Function Breakdown**

#### **`read_config(file_data: str)`**
- **Purpose**: Parses the YAML configuration file and initializes the core configuration objects.
- **Logic**:
  1. Loads the YAML data using `yaml.safe_load`.
  2. Initializes a `Config` object and sets its properties:
     - Language (`language`)
     - Project name (`project_name`)
     - Ignored files (`ignore_files`)
     - Project additional information (`project_additional_info`)
     - Project build settings (`build_settings`) via `ProjectBuildConfig`.
  3. Creates a list of `BaseModule` instances based on `custom_descriptions`.
     - If a description starts with `%`, a `CustomModuleWithOutContext` is created.
     - Otherwise, a `CustomModule` is created.
  4. Initializes a `StructureSettings` object and loads its properties from `structure_settings`.
- **Output**: Returns a tuple containing:
  - `Config` object
  - List of `BaseModule` instances
  - `StructureSettings` object

---

### **Class Breakdown**

#### **`StructureSettings`**
- **Purpose**: Defines structural rules for documentation generation.
- **Attributes**:
  - `include_intro_links`: Whether to include introductory links in the documentation.
  - `include_order`: Whether to sort documentation sections in a specific order.
  - `use_global_file`: Whether to use a global file for reusable documentation.
  - `max_doc_part_size`: Maximum size of a documentation part (default: 5000 characters).
  - `include_intro_text`: Whether to include introductory text in the documentation.
- **Methods**:
  - `load_settings(data: dict[str, Any])`: Dynamically loads settings from a dictionary.

---

### **Critical Notes**
> - The `read_config` function is tightly coupled with the `autodocconfig.yml` file structure. Any changes to the YAML schema must be reflected in this function.
> - The `custom_descriptions` field in the YAML file supports special syntax:
  - `%` prefix indicates a `CustomModuleWithOutContext`.
  - Without `%`, a `CustomModule` is created.
> - `StructureSettings` provides flexibility for customizing the structure and size of the generated documentation.

---
<a name="config-module"></a>
## `config.py`: Project Configuration Management

### **Functional Role**
The `config.py` module defines and manages project-specific configurations, including ignored files, language settings, project metadata, and build settings. It provides a centralized configuration object (`Config`) that can be customized and extended dynamically during runtime.

---

### **Inputs, Outputs, and Parameters**

| **Entity**                  | **Type**            | **Role**                                | **Notes**                                                                 |
|------------------------------|---------------------|-----------------------------------------|---------------------------------------------------------------------------|
| `ignore_files`              | `list[str]`         | List of file patterns to ignore         | Default patterns include common temporary files, directories, and caches. |
| `language`                  | `str`               | Language for documentation generation   | Default is `"en"`.                                                        |
| `project_name`              | `str`               | Name of the project                    | Can be dynamically set using `set_project_name()`.                        |
| `project_additional_info`   | `dict[str, str]`    | Additional metadata for the project     | Key-value pairs added via `add_project_additional_info()`.                |
| `pbc`                       | `ProjectBuildConfig` | Build configuration settings           | Includes logging and change threshold settings.                           |

---

### **Class Breakdown**

#### **`ProjectBuildConfig`**
- **Purpose**: Encapsulates build-specific settings for the project.
- **Attributes**:
  - `save_logs`: Boolean flag to enable or disable logging.
  - `log_level`: Integer representing the logging verbosity level.
  - `threshold_changes`: Integer threshold for detecting significant changes in the project.
- **Methods**:
  - `load_settings(data: dict[str, Any])`: Dynamically loads settings from a dictionary and assigns them to the corresponding attributes.

---

#### **`Config`**
- **Purpose**: Represents the main configuration object for the project.
- **Attributes**:
  - `ignore_files`: List of file patterns to exclude during processing.
  - `language`: Language setting for documentation generation.
  - `project_name`: Name of the project.
  - `project_additional_info`: Dictionary for storing additional project metadata.
  - `pbc`: Instance of `ProjectBuildConfig` for managing build settings.
- **Methods**:
  - `set_language(language: str)`: Updates the language setting.
  - `set_pcs(pcs: ProjectBuildConfig)`: Updates the project build configuration.
  - `set_project_name(name: str)`: Sets the project name.
  - `add_project_additional_info(key: str, value: str)`: Adds metadata to `project_additional_info`.
  - `add_ignore_file(pattern: str)`: Appends a new file pattern to the `ignore_files` list.
  - `get_project_settings()`: Creates and returns a `ProjectSettings` object populated with the current configuration.

---

### **Visible Interactions**
1. **Integration with `ProjectSettings`**:
   - The `get_project_settings()` method initializes a `ProjectSettings` object using the current configuration.
   - Additional project metadata is added to the `ProjectSettings` object dynamically.

2. **Interaction with Other Modules**:
   - Imports `CustomModule` and `IntroLinks` from the `factory.modules` package, indicating potential use in modular documentation generation.
   - Imports `ProjectSettings` from the `preprocessor.settings` module, suggesting integration with preprocessing workflows.
   - Imports `DocFactory` from the `factory.base_factory` module, indicating its role in modular documentation generation.

---

### **Technical Logic Flow**

1. **Initialization**:
   - The `Config` class is instantiated with default values for `ignore_files`, `language`, and `project_additional_info`.
   - A `ProjectBuildConfig` instance is created and assigned to the `pbc` attribute.

2. **Dynamic Configuration**:
   - Methods like `set_language()`, `set_project_name()`, and `add_project_additional_info()` allow dynamic customization of the configuration during runtime.
   - The `load_settings()` method in `ProjectBuildConfig` enables bulk updates to build-specific settings.

3. **Project Settings Generation**:
   - The `get_project_settings()` method creates a `ProjectSettings` object using the current configuration.
   - Additional metadata from `project_additional_info` is added to the `ProjectSettings` object.

---

### **Critical Notes**
> - The `ignore_files` list includes patterns for common temporary files, directories, and caches. These can be extended dynamically using `add_ignore_file()`.
> - The `ProjectBuildConfig` class provides flexibility for managing build-specific settings, such as logging and change thresholds.
> - The `Config` class is designed to be extensible, allowing for dynamic updates to project settings during runtime.

---
<a name="projectsettings-class"></a>
## **Class: `ProjectSettings`**

### **Purpose**
Manages project-specific metadata and generates a prompt for AI model interactions.

### **Attributes**
| Attribute         | Type            | Role                     | Notes                                   |
|-------------------|-----------------|--------------------------|-----------------------------------------|
| `project_name`    | `str`           | Project Name             | Name of the project.                   |
| `info`            | `dict[str, str]` | Project Metadata         | Key-value pairs of project-specific information. |

### **Methods**
#### **`add_info(key, value)`**
Adds a key-value pair to the `info` dictionary.

#### **`prompt` (Property)**
Generates a formatted string containing project metadata for use in AI model prompts.

---

### **Critical Notes**
> - **Dynamic Prompt Generation:** The `prompt` property dynamically constructs a string based on the project's metadata, ensuring flexibility for different projects.
> - **Extensibility:** The `ProjectSettings` class can be extended to include additional attributes or methods as needed.

---
<a name="cache-settings-class"></a>
## **Class: `CacheSettings`**

### **Purpose**
Manages caching of the last commit and previously generated documentation.

### **Attributes**
| Attribute            | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `last_commit`        | `str`              | Last Commit Hash         | Stores the hash of the last Git commit. |
| `doc`                | `DocInfoSchema`    | Documentation Schema     | Stores the structure of the generated documentation. |

---
<a name="token-auth"></a>
## `token_auth.py`: API Token Authentication

### **Functional Role**
The `token_auth.py` module retrieves API keys for external services (e.g., GitHub, Google Embedding) and writes them to the environment file (`GITHUB_ENV`) for subsequent workflow steps.

---

### **Inputs, Outputs, and Parameters**

| **Entity**              | **Type** | **Role**                              | **Notes**                                                                 |
|--------------------------|----------|---------------------------------------|---------------------------------------------------------------------------|
| `ADG_API_TOKEN`          | `str`    | API authentication token              | Retrieved from environment variables.                                     |
| `DEFAULT_SERVER_URL`     | `str`    | Base URL of the API server            | Retrieved from environment variables.                                     |
| `MODELS_API_KEYS`        | `str`    | GitHub token for AI models            | Retrieved from the API response.                                          |
| `GOOGLE_EMBEDDING_API_KEY` | `str`  | Google token for embedding operations | Retrieved from the API response.                                          |
| `TYPE_OF_MODEL`          | `str`    | Specifies the type of AI model        | Default value is `git`.                                                   |
| `GITHUB_ENV`             | `str`    | Path to the GitHub environment file   | Used to store retrieved API keys for subsequent workflow steps.           |

---

### **Function Breakdown**

#### **`main()`**
- **Purpose**: Retrieves API keys from the server and writes them to the environment file.
- **Logic**:
  1. Retrieves `ADG_API_TOKEN` and `DEFAULT_SERVER_URL` from environment variables.
  2. Constructs the API endpoint (`{DEFAULT_SERVER_URL}/github/get_api_keys`) and sends a GET request.
  3. Validates the server response:
     - Checks for successful status (`data["status"] == "success"`).
     - Extracts `github_token` and `google_token` from the response data.
  4. Writes the retrieved keys to the environment file (`GITHUB_ENV`) for use in subsequent steps.
  5. Prints success or error messages based on the outcome.
- **Output**: None (writes keys to `GITHUB_ENV` or prints them locally).

---

### **Critical Notes**
> - The module assumes the presence of environment variables (`ADG_API_TOKEN`, `DEFAULT_SERVER_URL`, `GITHUB_ENV`).
> - Failure to retrieve API keys or write to `GITHUB_ENV` results in error messages and termination (`exit(1)`).
> - The `TYPE_OF_MODEL` is set to `git` by default, but can be modified based on the retrieved keys.

---

### **Security Considerations**
> - Ensure `ADG_API_TOKEN` is securely stored and not exposed in logs or error messages.
> - Validate the server response to confirm successful retrieval of API keys.
> - Handle missing or invalid environment variables gracefully to avoid runtime errors.
<a name="exceptions-module"></a>
## `exceptions.py`: Custom Exception Handling

### **Functional Role**
The `exceptions.py` module defines custom exceptions for handling specific error scenarios within the Auto Doc Generator system.

---

### **Class Breakdown**

#### **`ModelExhaustedException`**
- **Purpose**: Raised when no AI models are available for use in the documentation generation process.
- **Attributes**: None.
- **Methods**: None.

---

### **Critical Notes**
> - The `ModelExhaustedException` is intended to signal the exhaustion of available AI models, allowing for graceful error handling and fallback mechanisms.
> - This exception can be used in workflows involving AI model selection, ensuring that the system does not proceed without a valid model.

markdown
<a name="logging"></a>
## **Module: `logging.py`**

### **Purpose**
Provides logging utilities for debugging, monitoring, and tracking application events.

---

### **Classes**
<a name="base-log-class"></a>
### **Class: `BaseLog`**

#### **Purpose**
Represents a base log message with customizable log levels.

#### **Attributes**
| Attribute            | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `message`            | `str`              | Log Message              | Stores the log message.                |
| `level`              | `int`              | Log Level                | Indicates the severity of the log.     |

#### **Methods**
| Method               | Parameters         | Return Type              | Role                                     | Notes                                   |
|----------------------|--------------------|--------------------------|------------------------------------------|-----------------------------------------|
| `format`             | None               | `str`                   | Formats the log message.                | Returns the log message as a string.   |

---
<a name="error-log-class"></a>
### **Class: `ErrorLog`**

#### **Purpose**
Represents an error-level log message.

#### **Methods**
| Method               | Parameters         | Return Type              | Role                                     | Notes                                   |
|----------------------|--------------------|--------------------------|------------------------------------------|-----------------------------------------|
| `format`             | None               | `str`                   | Formats the error log message.          | Prepends `[ERROR]` to the log message. |

---
<a name="warning-log-class"></a>
### **Class: `WarningLog`**

#### **Purpose**
Represents a warning-level log message.

#### **Methods**
| Method               | Parameters         | Return Type              | Role                                     | Notes                                   |
|----------------------|--------------------|--------------------------|------------------------------------------|-----------------------------------------|
| `format`             | None               | `str`                   | Formats the warning log message.        | Prepends `[WARNING]` to the log message. |

---
<a name="info-log-class"></a>
### **Class: `InfoLog`**

#### **Purpose**
Represents an info-level log message.

#### **Methods**
| Method               | Parameters         | Return Type              | Role                                     | Notes                                   |
|----------------------|--------------------|--------------------------|------------------------------------------|-----------------------------------------|
| `format`             | None               | `str`                   | Formats the info log message.           | Prepends `[INFO]` to the log message.  |

---
<a name="base-logger-template-class"></a>
### **Class: `BaseLoggerTemplate`**

#### **Purpose**
Provides a template for logging messages to various outputs.

#### **Attributes**
| Attribute            | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `log_level`          | `int`              | Log Level Filter         | Filters logs based on their severity.  |

#### **Methods**
| Method               | Parameters         | Return Type              | Role                                     | Notes                                   |
|----------------------|--------------------|--------------------------|------------------------------------------|-----------------------------------------|
| `log`                | `log: BaseLog`     | `None`                  | Logs the message to the console.        | Prints the formatted log message.      |
| `global_log`         | `log: BaseLog`     | `None`                  | Logs the message globally.              | Filters logs based on `log_level`.     |

---
<a name="file-logger-template-class"></a>
### **Class: `FileLoggerTemplate`**

#### **Purpose**
Extends `BaseLoggerTemplate` to log messages to a file.

#### **Attributes**
| Attribute            | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `file_path`          | `str`              | Log File Path            | Specifies the file path for logging.   |

#### **Methods**
| Method               | Parameters         | Return Type              | Role                                     | Notes                                   |
|----------------------|--------------------|--------------------------|------------------------------------------|-----------------------------------------|
| `log`                | `log: BaseLog`     | `None`                  | Logs the message to the specified file. | Appends the formatted log message to the file. |

---
<a name="base-logger-class"></a>
### **Class: `BaseLogger`**

#### **Purpose**
Provides a singleton logger instance for centralized logging.

#### **Methods**
| Method               | Parameters         | Return Type              | Role                                     | Notes                                   |
|----------------------|--------------------|--------------------------|------------------------------------------|-----------------------------------------|
| `set_logger`         | `logger: BaseLoggerTemplate` | `None`                 | Sets the logger template for the instance. | Allows customization of logging behavior. |
| `log`                | `log: BaseLog`     | `None`                  | Logs the message using the configured template. | Delegates logging to the `logger_template`. |

---

### **Critical Notes**
> - **Singleton Design**: `BaseLogger` ensures a single logger instance throughout the application.
> - **Extensibility**: `FileLoggerTemplate` and `BaseLoggerTemplate` allow flexible logging to different outputs.
> - **Log Level Filtering**: Logs can be filtered based on severity using `log_level`.


markdown
<a name="post-to-server"></a>
## `post_to_server.py`: Documentation Publishing via API

### **Functional Role**
The `post_to_server.py` module handles the final step of the documentation generation workflow by uploading the generated documentation to a remote server using an API. It reads the cached documentation file (`.auto_doc_cache_file.json`) and sends it to the server.

---

### **Inputs, Outputs, and Parameters**

| **Entity**          | **Type**   | **Role**                            | **Notes**                                                                 |
|----------------------|------------|-------------------------------------|---------------------------------------------------------------------------|
| `ADG_API_TOKEN`      | `str`      | API authentication token            | Retrieved from environment variables.                                     |
| `DEFAULT_SERVER_URL` | `str`      | Base URL of the documentation server | Retrieved from environment variables.                                     |
| `REPO_ID`            | `str`      | Repository identifier                | Used to specify the target repository for documentation upload.           |
| `.auto_doc_cache_file.json` | `str` | Cache file containing documentation | Contains the generated documentation in JSON format.                      |

---

### **Function Breakdown**

#### **`main()`**
- **Purpose**: Uploads the generated documentation to the remote server.
- **Logic**:
  1. Retrieves `ADG_API_TOKEN` and `DEFAULT_SERVER_URL` from environment variables.
  2. Reads the cached documentation file (`.auto_doc_cache_file.json`).
  3. Sends a POST request to the server API:
     - URL: `{DEFAULT_SERVER_URL}/docs/{REPO_ID}/push`
     - Headers: Includes `Authorization` with the API token.
     - Payload: Contains the cached documentation as JSON.
  4. Raises an exception if the request fails (`result.raise_for_status()`).
  5. Prints the response data from the server.
- **Output**: None (prints server response to the console).

---

### **Critical Notes**
> - The module assumes the presence of environment variables (`ADG_API_TOKEN`, `DEFAULT_SERVER_URL`, `REPO_ID`) and the cache file (`.auto_doc_cache_file.json`).
> - The server API endpoint is dynamically constructed using `DEFAULT_SERVER_URL` and `REPO_ID`.
> - Failure to authenticate or upload documentation will raise an exception (`result.raise_for_status()`).

---

### **Security Considerations**
> - Ensure that `ADG_API_TOKEN` is securely stored and not exposed in logs or error messages.
> - Validate the server response to confirm successful upload.
> - Handle missing or invalid environment variables gracefully to avoid runtime errors.
<a name="run-file"></a>
## `run_file.py`: Main Entry Point for Documentation Generation

### **Functional Role**
The `run_file.py` module serves as the primary entry point for the Auto Doc Generator system. It orchestrates the entire documentation generation workflow, including initialization, change detection, documentation creation, post-processing, and saving the final output.

---

### **Inputs, Outputs, and Parameters**

| **Entity**                | **Type**          | **Role**                              | **Notes**                                                                 |
|----------------------------|-------------------|---------------------------------------|---------------------------------------------------------------------------|
| `project_path`             | `str`             | Path to the project directory         | Specifies the root directory of the project to be documented.            |
| `config`                   | `Config`          | Configuration object                  | Parsed from `autodocconfig.yml` using the `read_config()` function.       |
| `custom_modules`           | `list[BaseModule]`| List of custom modules                | Modules for generating specific sections of documentation.               |
| `structure_settings`       | `StructureSettings` | Documentation structure settings     | Defines structural rules for documentation generation.                   |
| `MODELS_CONFIG`            | `dict`            | Mapping of model types to classes     | Specifies available AI models (`GPT4oModel`, `AzureModel`, `GPTModel`).   |
| `sync_model`               | `Model`           | AI model instance                     | Used for generating documentation content.                                |
| `embedding_model`          | `Embedding`       | Embedding model instance              | Handles embedding operations for document search functionality.           |
| `change_info`              | `CheckGitStatusResultSchema` | Change detection result         | Indicates whether documentation updates are required.                     |
| `.auto_doc_cache_file.json`| `str`             | Cache file containing documentation   | Stores the generated documentation for reuse or upload.                   |

---

### **Function Breakdown**

#### **`gen_doc()`**
- **Purpose**: Generates structured documentation for the specified project.
- **Logic**:
  1. **Initialization**:
     - Selects the AI model based on `TYPE_OF_MODEL` from `MODELS_CONFIG`.
     - Initializes the `Manager` with project path, configuration, AI model, embedding model, and progress tracker.
  2. **Change Detection**:
     - Calls `check_git_status(manager)` to determine if documentation updates are required.
     - If no changes are detected, loads cached documentation and terminates the workflow early.
  3. **Documentation Generation**:
     - Calls `manager.generate_code_file()` to create base documentation files.
     - Optionally generates global reusable documentation (`manager.generate_global_info()`) based on `structure_settings`.
     - Splits documentation into manageable parts (`manager.generete_doc_parts()`).
     - Uses `DocFactory` with `custom_modules` to generate modular documentation sections.
  4. **Post-Processing**:
     - Optionally adds introductory text and links using additional modules (`IntroText`, `IntroLinks`).
     - Reorders document content (`manager.order_doc()`).
     - Creates embedding layers for document search functionality (`manager.create_embedding_layer()`).
  5. **Finalization**:
     - Clears cache and saves the generated documentation (`manager.save()`).
  6. **Output**: Returns the full documentation content (`manager.doc_info.doc.get_full_doc()`).

---

### **Critical Notes**
> - The workflow is terminated early if no changes are detected (`sys.exit(0)`).
> - The AI model and embedding model are dynamically selected based on environment variables (`MODELS_API_KEYS`, `GOOGLE_EMBEDDING_API_KEY`).
> - `structure_settings` controls optional features such as global files, introductory sections, and document ordering.

---

### **Security Considerations**
> - Ensure sensitive keys (`MODELS_API_KEYS`, `GOOGLE_EMBEDDING_API_KEY`) are securely retrieved and stored.
> - Validate the integrity of `autodocconfig.yml` to avoid misconfigurations.
> - Handle missing or invalid environment variables gracefully to prevent runtime errors.

---
<a name="progress-management"></a>
## **Progress Management Classes**

### **Class: `BaseProgress`**

#### **Purpose**
Provides a base interface for managing progress tracking tasks. This class is designed to be extended by specific implementations for different progress tracking mechanisms.

#### **Methods**
| Method               | Parameters                     | Return Type | Role                                   | Notes                                   |
|----------------------|---------------------------------|-------------|----------------------------------------|-----------------------------------------|
| `create_new_subtask` | `name: str`, `total_len: int`  | `None`      | Creates a new subtask for tracking.   | Abstract method, implementation required in subclasses. |
| `update_task`        | None                          | `None`      | Updates the progress of the current task. | Abstract method, implementation required in subclasses. |
| `remove_subtask`     | None                          | `None`      | Removes the current subtask.          | Abstract method, implementation required in subclasses. |

---
<a name="lib-progress-class"></a>
### **Class: `LibProgress`**

#### **Purpose**
Extends `BaseProgress` to provide progress tracking using the `rich.progress` library.

#### **Attributes**
| Attribute            | Type         | Role                           | Notes                                   |
|----------------------|--------------|---------------------------------|-----------------------------------------|
| `progress`           | `Progress`   | Rich Progress Instance         | Used to manage and display progress bars. |
| `_base_task`         | `Task`       | General Progress Task          | Represents the overall progress of the operation. |
| `_cur_sub_task`      | `Task`       | Current Subtask                | Tracks progress for the current subtask. |

#### **Methods**
| Method               | Parameters                     | Return Type | Role                                     | Notes                                   |
|----------------------|---------------------------------|-------------|------------------------------------------|-----------------------------------------|
| `create_new_subtask` | `name: str`, `total_len: int`  | `None`      | Creates a new subtask with a progress bar. | Adds a task to the `rich.progress` instance. |
| `update_task`        | None                          | `None`      | Updates the progress of the current task. | Advances the progress bar for either the base task or the current subtask. |
| `remove_subtask`     | None                          | `None`      | Removes the current subtask.             | Resets the `_cur_sub_task` attribute to `None`. |

---
<a name="console-task-class"></a>
### **Class: `ConsoleTask`**

#### **Purpose**
Provides a simple console-based progress tracker for tasks.

#### **Attributes**
| Attribute            | Type         | Role                           | Notes                                   |
|----------------------|--------------|---------------------------------|-----------------------------------------|
| `name`               | `str`        | Task Name                      | Specifies the name of the task.         |
| `total_len`          | `int`        | Total Length                   | Defines the total progress length.      |
| `current_len`        | `int`        | Current Progress               | Tracks the current progress.            |

#### **Methods**
| Method               | Parameters                     | Return Type | Role                                     | Notes                                   |
|----------------------|---------------------------------|-------------|------------------------------------------|-----------------------------------------|
| `start_task`         | None                          | `None`      | Initializes the task progress.           | Prints the task name and total length.  |
| `progress`           | None                          | `None`      | Updates and displays the task progress.  | Calculates and prints the percentage of completion. |

---
<a name="console-github-progress-class"></a>
### **Class: `ConsoleGtiHubProgress`**

#### **Purpose**
Extends `BaseProgress` to provide console-based progress tracking for GitHub workflows.

#### **Attributes**
| Attribute            | Type         | Role                           | Notes                                   |
|----------------------|--------------|---------------------------------|-----------------------------------------|
| `curr_task`          | `ConsoleTask` | Current Subtask                | Tracks the current subtask progress.    |
| `gen_task`           | `ConsoleTask` | General Progress Task          | Tracks overall progress.                |

#### **Methods**
| Method               | Parameters                     | Return Type | Role                                     | Notes                                   |
|----------------------|---------------------------------|-------------|------------------------------------------|-----------------------------------------|
| `create_new_subtask` | `name: str`, `total_len: int`  | `None`      | Creates a new subtask for tracking.      | Initializes a new `ConsoleTask` instance for the subtask. |
| `update_task`        | None                          | `None`      | Updates the progress of the current task. | Updates either the current subtask or the general task. |
| `remove_subtask`     | None                          | `None`      | Removes the current subtask.             | Resets the `curr_task` attribute to `None`. |

---
<a name="azure-model"></a>
## `AzureModel`: Azure AI Integration for Documentation Generation

### **Functional Role**
The `AzureModel` class integrates Azure AI's `ChatCompletionsClient` to generate documentation content using AI models. It provides mechanisms for handling model selection, prompt parsing, and response cleaning, ensuring seamless interaction with Azure's AI inference services.

---

### **Class Breakdown**

#### **`AzureModel`**
- **Purpose**: Implements AI-driven documentation generation using Azure's DeepSeek models.
- **Attributes**:
  - `client`: Instance of `ChatCompletionsClient` for interacting with Azure AI services.
  - `logger`: Instance of `BaseLogger` for logging operations and errors.
  - `api_key`: API key for authenticating with Azure AI.
  - `history`: Instance of `History` for managing conversation history.
  - `models_list`: List of available AI models for inference.
  - `use_random`: Boolean flag to determine if models should be selected randomly.
  - `current_key_index`: Tracks the current API key in use.
  - `current_model_index`: Tracks the current AI model in use.
  - `regen_models_name`: List of models available for regeneration.

---

### **Visible Interactions**
1. **Integration with Azure AI**:
   - The `ChatCompletionsClient` is initialized with an endpoint and credentials to interact with Azure AI's inference services.
   - The `complete()` method is used to generate responses based on user/system messages.

2. **Interaction with Logging**:
   - Logs are generated using `BaseLogger` to track the progress of operations, errors, and warnings.
   - Log levels include `InfoLog`, `ErrorLog`, and `WarningLog`.

3. **Exception Handling**:
   - Raises `ModelExhaustedException` when no models are available for use, ensuring graceful error handling.

---

### **Technical Logic Flow**

#### **Initialization**
1. The `AzureModel` constructor initializes:
   - The `ChatCompletionsClient` with the provided API key and endpoint.
   - A logger instance for tracking operations.

#### **Prompt Parsing**
2. `_parse_prompt(data: list[dict[str, str]])`:
   - Converts a list of dictionaries (`data`) into a list of `UserMessage` or `SystemMessage` objects.
   - Differentiates between `system` and `user` roles based on the `role` attribute.

#### **Response Cleaning**
3. `_clean_deepseek_response(text: str)`:
   - Removes `<think>...</think>` blocks and extra whitespace from the AI-generated response using regex.

#### **Answer Generation**
4. `generate_answer(with_history: bool, prompt: list[dict[str, str]] | None)`:
   - Logs the start of the answer generation process.
   - Determines the source of messages (`history` or `prompt`).
   - Parses the messages into `UserMessage` or `SystemMessage` objects.
   - Iteratively attempts to generate a response using available models:
     - If a model fails, logs a warning and switches to the next model.
     - Updates `current_key_index` and `current_model_index` to cycle through available API keys and models.
   - Cleans the generated response using `_clean_deepseek_response`.
   - Logs the generated answer and returns it.

---

### **Data Contract**

| **Entity**              | **Type**                       | **Role**                          | **Notes**                                                                 |
|--------------------------|---------------------------------|------------------------------------|---------------------------------------------------------------------------|
| `api_key`               | `str`                          | Authentication                    | API key for Azure AI services.                                           |
| `history`               | `History`                     | Conversation Management           | Stores previous user/system messages for context.                        |
| `models_list`           | `list[str]`                   | Model Selection                   | List of available AI models for inference.                               |
| `use_random`            | `bool`                        | Model Selection Strategy          | Determines if models are selected randomly.                              |
| `messages`              | `list[dict[str, str]]`        | Input Messages                    | User/system messages for generating responses.                           |
| `response`              | `ChatRequestMessage`          | AI Response                       | Generated response from the AI model.                                    |
| `result`                | `str`                         | Cleaned Response                  | Final processed response after cleaning.                                 |
| `current_key_index`     | `int`                         | API Key Index                     | Tracks the current API key in use.                                       |
| `current_model_index`   | `int`                         | Model Index                       | Tracks the current AI model in use.                                      |
| `regen_models_name`     | `list[str]`                   | Regeneration Models               | List of models available for regeneration.                               |

---

### **Critical Notes**
> - **Error Handling**: If all models fail, the system raises a `ModelExhaustedException` to prevent further execution without a valid model.
> - **Dynamic Model Switching**: The class cycles through available API keys and models to ensure continuity in response generation.
> - **Response Cleaning**: The `_clean_deepseek_response` method ensures that unnecessary tags and whitespace are removed from the AI-generated content.
> - **Logging**: Comprehensive logging is implemented to track operations, errors, and warnings, aiding in debugging and monitoring.

---

### **Visible Interactions with Other Modules**
1. **`History`**:
   - Manages conversation history for generating context-aware responses.
2. **`ModelExhaustedException`**:
   - Ensures graceful error handling when no models are available.
3. **`BaseLogger`**:
   - Provides logging utilities for tracking operations, errors, and warnings.

---

### **Terminal Points**
- The `generate_answer()` method returns the cleaned AI-generated response as a string.
- If no models are available, the process terminates with a `ModelExhaustedException`.

---

### **Critical Assumptions**
> - The Azure AI endpoint (`https://models.github.ai/inference`) is operational and accessible.
> - The provided API keys and model names are valid and authorized for use.
> - The `History` object is correctly populated with user/system messages for context-aware response generation.


markdown
<a name="gpt-model-class"></a>
## **GPTModel and GPT4oModel: AI Model Integration and Response Generation**

### **Functional Role**
The `GPTModel` and `GPT4oModel` classes are responsible for generating AI-driven responses using different sets of models. These classes implement the core logic for interacting with external AI services (OpenAI and Groq) and managing model selection, API key rotation, and error handling.

---

### **Technical Logic Flow**

#### **Initialization**
Both classes inherit from the `Model` base class and initialize the following attributes:
- **API Key Management**:
  - `api_key`: List of API keys used for authentication with external AI services.
  - `current_key_index`: Tracks the index of the currently active API key.
- **Model Selection**:
  - `models_list`: List of available AI models for inference.
  - `regen_models_name`: Dynamically updated list of models available for regeneration.
  - `current_model_index`: Tracks the index of the currently active model.
  - `use_random`: Determines whether models are selected randomly.
- **History**:
  - `history`: Stores previous user/system messages for context-aware response generation.
- **Client Initialization**:
  - `GPT4oModel`: Uses OpenAI's `OpenAI` client for AI inference.
  - `GPTModel`: Uses Groq's `Groq` client for AI inference.
- **Logging**:
  - Both classes use `BaseLogger` for tracking operations, errors, and warnings.

---

### **Response Generation Workflow**

#### **`generate_answer()` Method**
1. **Input Handling**:
   - If `with_history` is `True`, retrieves the conversation history from the `History` object.
   - If `prompt` is provided, uses it as the input for response generation.

2. **Model Selection and API Key Rotation**:
   - Iterates through `regen_models_name` and `api_keys` to find a working model and key.
   - If all models fail, raises a `ModelExhaustedException`.

3. **AI Inference**:
   - Sends the `messages` input to the AI service (`OpenAI` or `Groq`) using the selected model.
   - Parameters for OpenAI:
     - `temperature`: Controls randomness in responses (set to 0.3).
     - `top_p`: Controls diversity in responses (set to 1.0).
     - `max_tokens`: Limits the response length (set to 16384).
   - Parameters for Groq:
     - Model name is passed directly without additional parameters.

4. **Error Handling**:
   - Logs warnings for failed models and rotates to the next available model and API key.
   - If no models are available, logs an error and raises `ModelExhaustedException`.

5. **Response Cleaning**:
   - Extracts the AI-generated response (`chat_completion.choices[0].message.content`).
   - Logs the generated response and the model used.
   - Returns the cleaned response or an empty string if the result is `None`.

---

### **Data Contract**

| **Entity**              | **Type**                      | **Role**                          | **Notes**                                                               |
|--------------------------|-------------------------------|------------------------------------|-------------------------------------------------------------------------|
| `api_key`               | `list[str]`                   | API Key Management                | List of keys for authenticating with external AI services.              |
| `current_key_index`     | `int`                         | API Key Index                     | Tracks the current API key in use.                                      |
| `models_list`           | `list[str]`                   | Model Selection                   | List of available AI models for inference.                              |
| `regen_models_name`     | `list[str]`                   | Regeneration Models               | List of models available for regeneration.                              |
| `current_model_index`   | `int`                         | Model Index                       | Tracks the current AI model in use.                                     |
| `history`               | `History`                     | Conversation Management           | Stores previous user/system messages for context.                       |
| `messages`              | `list[dict[str, str]]`        | Input Messages                    | User/system messages for generating responses.                          |
| `chat_completion`       | `dict`                        | AI Response Object                | Contains the raw response from the AI model.                            |
| `result`                | `str`                         | Cleaned Response                  | Final processed response after cleaning.                                |
| `logger`                | `BaseLogger`                  | Logging Utility                   | Tracks operations, errors, and warnings.                                |

---

### **Critical Notes**
> - **Error Handling**: If all models fail, the system raises a `ModelExhaustedException` to prevent further execution without a valid model.
> - **Dynamic Model Switching**: The class cycles through available API keys and models to ensure continuity in response generation.
> - **Response Cleaning**: Ensures that unnecessary tags and whitespace are removed from the AI-generated content.
> - **Logging**: Comprehensive logging is implemented to track operations, errors, and warnings, aiding in debugging and monitoring.

---

### **Visible Interactions with Other Modules**
1. **`History`**:
   - Manages conversation history for generating context-aware responses.
2. **`ModelExhaustedException`**:
   - Ensures graceful error handling when no models are available.
3. **`BaseLogger`**:
   - Provides logging utilities for tracking operations, errors, and warnings.

---

### **Terminal Points**
- The `generate_answer()` method returns the cleaned AI-generated response as a string.
- If no models are available, the process terminates with a `ModelExhaustedException`.

---

### **Critical Assumptions**
> - The Azure AI endpoint (`https://models.github.ai/inference`) is operational and accessible.
> - The provided API keys and model names are valid and authorized for use.
> - The `History` object is correctly populated with user/system messages for context-aware response generation.
<a name="history-class"></a>
## **`History` Class**

### **Functional Role**
The `History` class manages conversation history for AI model interactions. It stores a sequence of user and system messages, enabling context-aware responses by maintaining a structured dialogue history.

---

### **Technical Logic Flow**
1. **Initialization**:
   - The constructor (`__init__`) initializes the `history` attribute as an empty list.
   - If a `system_prompt` is provided, it is added to the history with the role `"system"`.

2. **Adding to History**:
   - The `add_to_history(role, content)` method appends a dictionary containing the `role` and `content` to the `history` list.

---

### **Data Contract**

| Entity             | Type               | Role                     | Notes                                      |
|--------------------|--------------------|--------------------------|--------------------------------------------|
| `system_prompt`    | `str`              | System Initialization    | Initial system message for context.        |
| `history`          | `list[dict[str, str]]` | Conversation History     | Stores user/system messages.               |
| `role`             | `str`              | Message Role             | Specifies the sender (`user`, `system`, `assistant`). |
| `content`          | `str`              | Message Content          | Actual message text.                       |

---

### **Critical Notes**
> - **Stateful Context**: The `History` class is essential for maintaining the context of conversations, which is critical for generating coherent responses from AI models.
> - **System Prompt**: The initial system prompt sets the tone and context for the AI model's responses.

---
<a name="parentmodel-class"></a>
## **`ParentModel` Abstract Base Class**

### **Functional Role**
The `ParentModel` class serves as an abstract base for AI model implementations. It defines the interface for generating responses and managing API keys and model selection.

---

### **Technical Logic Flow**
1. **Initialization**:
   - Accepts `api_key`, `history`, and `models_list` as parameters.
   - Randomizes the order of `models_list` if `use_random` is enabled.
   - Tracks the current API key and model indices.

2. **Abstract Methods**:
   - `generate_answer(with_history, prompt)`: Generates an AI response based on the provided prompt.
   - `get_answer_without_history(prompt)`: Generates a response without using conversation history.
   - `get_answer(prompt)`: Generates a response using conversation history.

---

### **Data Contract**

| Entity               | Type               | Role                     | Notes                                      |
|----------------------|--------------------|--------------------------|--------------------------------------------|
| `api_key`            | `list[str]`        | API Keys                 | List of API keys for authentication.       |
| `history`            | `History`          | Conversation History     | Manages context for AI responses.          |
| `models_list`        | `list[str]`        | Model Selection          | List of available AI models.               |
| `regen_models_name`  | `list[str]`        | Regeneration Models      | Randomized list of models for inference.   |
| `current_model_index`| `int`              | Model Index              | Tracks the current model in use.           |
| `current_key_index`  | `int`              | API Key Index            | Tracks the current API key in use.         |

---

### **Critical Notes**
> - **Dynamic Model Switching**: Randomized model selection ensures diverse AI responses.
> - **Error Handling**: Abstract methods enforce implementation of response generation logic in subclasses.

---
<a name="model-asyncmodel-classes"></a>
## **`Model` and `AsyncModel` Classes**

### **Functional Role**
These classes implement the `ParentModel` abstract methods to provide synchronous and asynchronous AI response generation.

---

### **Technical Logic Flow**
1. **`Model` Class**:
   - Implements synchronous methods for generating responses (`generate_answer`, `get_answer_without_history`, `get_answer`).
   - Updates the `History` object with user and assistant messages.

2. **`AsyncModel` Class**:
   - Implements asynchronous methods for generating responses (`generate_answer`, `get_answer_without_history`, `get_answer`).
   - Uses `await` for asynchronous response generation.

---

### **Data Contract**

| Entity               | Type               | Role                     | Notes                                      |
|----------------------|--------------------|--------------------------|--------------------------------------------|
| `generate_answer`    | `str` or `Coroutine` | Response Generation      | Generates AI responses based on prompts.   |
| `get_answer_without_history` | `str` or `Coroutine` | History-Free Response   | Generates responses without context.       |
| `get_answer`         | `str` or `Coroutine` | Context-Aware Response   | Generates responses using conversation history. |

---

### **Critical Notes**
> - **Stateful Context**: Both classes rely on the `History` object for managing conversation context.
> - **Async Support**: `AsyncModel` enables non-blocking response generation for scalable applications.

---
<a name="embedding-class"></a>
## `Embedding` Class: Vector Generation and Management

The `Embedding` class is responsible for generating embedding vectors for textual content using the `genai` library. These embeddings are used for semantic analysis and content organization within the Auto Doc Generator system.

### **Class: `Embedding`**
#### **Purpose**
The `Embedding` class interfaces with the `genai` library to generate high-dimensional embedding vectors for text input. These vectors are used for semantic operations such as sorting and similarity calculations.

#### **Attributes**
| Attribute   | Type       | Role                     | Notes                                      |
|-------------|------------|--------------------------|--------------------------------------------|
| `client`    | `genai.Client` | API Client              | Handles communication with the `genai` API. |

#### **Methods**
| Method       | Input Parameters                     | Output Type | Role                     | Notes                                      |
|--------------|--------------------------------------|-------------|--------------------------|--------------------------------------------|
| `__init__`   | `api_key: str`                      | `None`      | Initializes the API client | Requires a valid API key for authentication. |
| `get_vector` | `prompt: str`                       | `list`      | Generates embedding vector | Uses the `genai` API to generate a 768-dimensional embedding vector from the input prompt. |

#### **Critical Notes**
> - **API Dependency:** The `Embedding` class relies on the `genai` library and the `gemini-embedding-2-preview` model for embedding generation. Ensure the API key is valid and the model is accessible.
> - **Error Handling:** If the embedding generation fails, an exception is raised with the message `"promblem with embedding"`. This should be handled appropriately in higher-level workflows.

---
<a name="embedding-functions"></a>
## Embedding Functions: Sorting and Distance Calculation

The following functions are utility methods for processing embedding vectors and organizing content based on semantic similarity.

### **Function: `bubble_sort_by_dist`**
#### **Purpose**
Sorts a list of tuples based on the second element (distance) in ascending order using the bubble sort algorithm.

#### **Technical Logic Flow**
1. Iterate over the list multiple times.
2. Compare adjacent elements and swap them if they are out of order.
3. Return the sorted list.

#### **Parameters**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `arr`        | `list`     | Input List               | List of tuples where the second element represents distance. |

#### **Output**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `sorted_arr` | `list`     | Sorted List              | List sorted by distance in ascending order. |

---

### **Function: `get_len_btw_vectors`**
#### **Purpose**
Calculates the Euclidean distance between two embedding vectors.

#### **Technical Logic Flow**
1. Compute the difference between the vectors using `np.linalg.norm`.
2. Return the distance as a float.

#### **Parameters**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `vector1`    | `np.ndarray` | First Vector            | First embedding vector.                    |
| `vector2`    | `np.ndarray` | Second Vector           | Second embedding vector.                   |

#### **Output**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `distance`   | `float`    | Euclidean Distance       | Distance between the two vectors.          |

---

### **Function: `sort_vectors`**
#### **Purpose**
Sorts a dictionary of vectors based on their semantic distance from a root vector.

#### **Technical Logic Flow**
1. Iterate over the dictionary of vectors.
2. Calculate the distance between the root vector and each vector using `get_len_btw_vectors`.
3. Append the vector name and distance to a list.
4. Sort the list using `bubble_sort_by_dist`.
5. Extract and return the sorted vector names.

#### **Parameters**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `root_vector`| `np.ndarray` | Reference Vector         | Root vector used for distance comparison.  |
| `other`      | `dict[str, Any]` | Dictionary of Vectors | Contains vector names and their corresponding embeddings. |

#### **Output**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `sorted_names` | `list[str]` | Sorted Vector Names     | List of vector names sorted by semantic distance. |

---
<a name="sorting-functions"></a>
## Sorting Functions: Anchor Extraction and Content Organization

The following functions are responsible for extracting HTML anchor links and organizing content based on semantic relationships.

### **Function: `extract_links_from_start`**
#### **Purpose**
Extracts HTML anchor links from the start of text chunks.

#### **Technical Logic Flow**
1. Use regex to identify anchor links in each chunk.
2. Append valid links to a list.
3. Return the list of links and a flag indicating whether the first chunk should be deleted.

#### **Parameters**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `chunks`     | `list[str]` | Text Chunks              | List of text chunks to process.            |

#### **Output**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `links`      | `list[str]` | Extracted Links          | List of valid anchor links.                |
| `flag`       | `bool`      | Deletion Flag            | Indicates if the first chunk should be deleted. |

---

### **Function: `split_text_by_anchors`**
#### **Purpose**
Splits text into chunks based on HTML anchor tags and maps each chunk to its corresponding anchor link.

#### **Technical Logic Flow**
1. Use regex to split text into chunks based on anchor tags.
2. Extract links from the chunks using `extract_links_from_start`.
3. Map each link to its corresponding chunk.
4. Return the mapping as a dictionary.

#### **Parameters**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `text`       | `str`      | Input Text               | Raw text containing HTML anchor tags.      |

#### **Output**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `mapping`    | `dict[str, str]` | Anchor-Chunk Mapping | Dictionary mapping anchor links to text chunks. |

---

### **Function: `get_order`**
#### **Purpose**
Orders a list of chunk titles semantically using an AI model.

#### **Technical Logic Flow**
1. Log the start of the ordering process.
2. Generate a prompt for the AI model, instructing it to sort the titles semantically.
3. Pass the prompt to the `Model.get_answer_without_history` method.
4. Parse the AI model's response into a list of sorted titles.
5. Log the sorted titles and return them.

#### **Parameters**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `model`      | `Model`    | AI Model                 | Used for semantic sorting of titles.       |
| `chanks`     | `list[str]` | Chunk Titles             | List of titles to be sorted.               |

#### **Output**
| Entity       | Type       | Role                     | Notes                                      |
|--------------|------------|--------------------------|--------------------------------------------|
| `sorted_titles` | `list[str]` | Sorted Titles           | List of titles sorted semantically.        |

---

### **Critical Notes**
> - **Regex-Based Extraction:** Functions like `extract_links_from_start` and `split_text_by_anchors` rely on regex patterns for parsing HTML anchor tags. Ensure the input text adheres to the expected format for accurate processing.
> - **AI Model Dependency:** The `get_order` function heavily depends on the `Model` class for semantic sorting. Ensure the model is properly configured and accessible.
> - **Error Handling:** Functions like `split_text_by_anchors` raise exceptions if the number of links and chunks do not match, indicating potential issues with the input text.

---

### **Shared Observations**
1. **Modular Design**:
   - Functions are designed to be reusable and modular, allowing them to be integrated into larger workflows.
2. **Logging Integration**:
   - The `get_order` function uses `BaseLogger` for logging progress and outputs, improving traceability during execution.
3. **Iterative Processing**:
   - Functions like `sort_vectors` and `split_text_by_anchors` process data iteratively, ensuring robustness against input variations.
4. **Error Handling**:
   - Exceptions are raised for critical issues, such as mismatched anchors and chunks, ensuring early detection of errors.
<a name="checker-parse-answer"></a>
## **Function: `parse_answer`**

#### **Purpose**
Parses the AI model's response to determine whether documentation updates are required and whether global documentation files need to be regenerated.

#### **Technical Logic Flow**
1. Splits the AI model's response string using the `|` delimiter.
2. Evaluates the first segment (`splited[0]`) to determine if documentation updates are required (`change_doc`).
3. Evaluates the second segment (`splited[1]`) to determine if global documentation files need to be regenerated (`change_global`).
4. Returns a `CheckGitStatusResultSchema` object with the parsed results.

#### **Parameters**
| Entity         | Type                     | Role                           | Notes                                   |
|----------------|--------------------------|--------------------------------|-----------------------------------------|
| `answer`       | `str`                    | AI Model Response              | Raw response string from the AI model. |

#### **Output**
| Entity               | Type                          | Role                           | Notes                                   |
|----------------------|-------------------------------|--------------------------------|-----------------------------------------|
| `CheckGitStatusResultSchema` | `CheckGitStatusResultSchema` | Parsed Response Object         | Contains flags for documentation updates and global file regeneration. |

---
<a name="checker-have-to-change"></a>
## **Function: `have_to_change`**

#### **Purpose**
Determines whether documentation updates are required based on code changes and global information by querying an AI model.

#### **Technical Logic Flow**
1. Constructs a prompt for the AI model:
   - Includes a system message (`BASE_CHANGES_CHECK_PROMPT`).
   - Adds global information (`global_info`) if provided.
   - Includes a user message containing the code changes (`diff`).
2. Sends the prompt to the AI model using `model.get_answer_without_history`.
3. Parses the AI model's response using `parse_answer`.
4. Returns the parsed response as a `CheckGitStatusResultSchema` object.

#### **Parameters**
| Entity         | Type                     | Role                           | Notes                                   |
|----------------|--------------------------|--------------------------------|-----------------------------------------|
| `model`        | `Model`                  | AI Model                       | Used to query the AI for decision-making. |
| `diff`         | `list[dict[str, str]]`   | Code Changes                   | List of changes detected in the codebase. |
| `global_info`  | `str | None`             | Global Documentation Info      | Optional global information for context. |

#### **Output**
| Entity               | Type                          | Role                           | Notes                                   |
|----------------------|-------------------------------|--------------------------------|-----------------------------------------|
| `CheckGitStatusResultSchema` | `CheckGitStatusResultSchema` | Parsed Response Object         | Contains flags for documentation updates and global file regeneration. |

---
<a name="codemix-should-ignore"></a>
## **Function: `should_ignore`**

#### **Purpose**
Determines whether a given file or directory path should be ignored based on the specified ignore patterns.

#### **Technical Logic Flow**
1. Resolves the relative path of the file/directory against the root directory.
2. Converts the relative path to a string for pattern matching.
3. Iterates through the ignore patterns:
   - Matches the full relative path.
   - Matches the base name of the path.
   - Matches individual components of the path.
4. Returns `True` if any pattern matches; otherwise, returns `False`.

#### **Parameters**
| Entity         | Type                     | Role                           | Notes                                   |
|----------------|--------------------------|--------------------------------|-----------------------------------------|
| `path`         | `str`                    | File/Directory Path            | Path to check against ignore patterns. |

#### **Output**
| Entity         | Type                     | Role                           | Notes                                   |
|----------------|--------------------------|--------------------------------|-----------------------------------------|
| `ignored`      | `bool`                   | Ignore Flag                    | Indicates whether the path should be ignored. |

---
<a name="compressor-functions"></a>
## **Functions in `compressor.py`**

### **Function: `compress`**

#### **Purpose**
Compresses a given text string using an AI model and project-specific settings.

#### **Technical Logic Flow**
1. Constructs a `prompt` consisting of:
   - A system message with project-specific settings (`project_settings.prompt`).
   - A system message with compression settings (`get_BASE_COMPRESS_TEXT`).
   - A user message containing the input data.
2. Sends the `prompt` to the AI model (`model.get_answer_without_history`) for processing.
3. Returns the compressed output.

#### **Parameters**
| Entity             | Type            | Role                     | Notes                                   |
|--------------------|-----------------|--------------------------|-----------------------------------------|
| `data`             | `str`           | Input Data               | Text to be compressed.                 |
| `project_settings` | `ProjectSettings` | Project Settings         | Contains project-specific metadata.     |
| `model`            | `Model`         | AI Model                 | AI model used for text compression.    |
| `compress_power`   | `int`           | Compression Power        | Determines the strength of compression. |

#### **Output**
| Entity             | Type            | Role                     | Notes                                   |
|--------------------|-----------------|--------------------------|-----------------------------------------|
| `answer`           | `str`           | Compressed Output        | Compressed version of the input data.  |

---

### **Function: `compress_and_compare`**

#### **Purpose**
Compresses and combines multiple text strings into fewer, larger chunks, while tracking progress.

#### **Technical Logic Flow**
1. Initializes an empty list to store compressed chunks.
2. Creates a progress bar to track the compression process.
3. Iterates through the input data:
   - Divides the input into chunks based on `compress_power`.
   - Compresses each chunk using the `compress` function.
   - Appends the compressed results to the corresponding index in the output list.
   - Updates the progress bar after processing each chunk.
4. Removes the progress bar once processing is complete.
5. Returns the list of compressed chunks.

#### **Parameters**
| Entity             | Type            | Role                     | Notes                                   |
|--------------------|-----------------|--------------------------|-----------------------------------------|
| `data`             | `list[str]`     | Input Data               | List of text strings to be compressed. |
| `model`            | `Model`         | AI Model                 | AI model used for text compression.    |
| `project_settings` | `ProjectSettings` | Project Settings         | Contains project-specific metadata.     |
| `compress_power`   | `int`           | Compression Power        | Determines the strength of compression. |
| `progress_bar`     | `BaseProgress`  | Progress Tracker         | Tracks the progress of the compression task. |

#### **Output**
| Entity             | Type            | Role                     | Notes                                   |
|--------------------|-----------------|--------------------------|-----------------------------------------|
| `compress_and_compare_data` | `list[str]` | Compressed Chunks       | List of combined compressed text chunks. |

---

### **Function: `compress_to_one`**

#### **Purpose**
Iteratively compresses a list of text strings into a single compressed output.

#### **Technical Logic Flow**
1. Initializes a counter for the number of iterations.
2. While the input data contains more than one item:
   - Adjusts `compress_power` based on the size of the input data.
   - Calls `compress_and_compare` to compress and combine the data.
   - Updates the input data with the compressed results.
   - Increments the iteration counter.
3. Returns the final compressed output (a single string).

#### **Parameters**
| Entity             | Type            | Role                     | Notes                                   |
|--------------------|-----------------|--------------------------|-----------------------------------------|
| `data`             | `list[str]`     | Input Data               | List of text strings to be compressed. |
| `model`            | `Model`         | AI Model                 | AI model used for text compression.    |
| `project_settings` | `ProjectSettings` | Project Settings         | Contains project-specific metadata.     |
| `compress_power`   | `int`           | Compression Power        | Determines the strength of compression. |
| `progress_bar`     | `BaseProgress`  | Progress Tracker         | Tracks the progress of the compression task. |

#### **Output**
| Entity             | Type            | Role                     | Notes                                   |
|--------------------|-----------------|--------------------------|-----------------------------------------|
| `data[0]`          | `str`           | Final Compressed Output  | Single compressed string.              |

---

### **Critical Notes**
> - **Error Handling:** The `compress` function relies on the AI model's response and assumes valid input data.
> - **Iterative Compression:** The `compress_to_one` function reduces multiple chunks into a single compressed output, making it ideal for large datasets.
> - **Progress Tracking:** The `compress_and_compare` and `compress_to_one` functions integrate progress tracking via `BaseProgress`.

---
<a name="split-data-function"></a>
## **Function: `split_data`**

### **Purpose**
Splits a large text string into smaller chunks based on a maximum symbol limit, ensuring each chunk adheres to size constraints for further processing.

### **Technical Logic Flow**
1. **Initialization**:
   - A logger instance (`BaseLogger`) logs the start of the data splitting process.
   - The input data is split into smaller chunks (`splited_by_files`) based on file delimiters.

2. **Iterative Splitting**:
   - The function iteratively checks each chunk's size against the `max_symbols` limit.
   - If a chunk exceeds the limit, it is split into two smaller parts:
     - The first part contains the initial half of the chunk.
     - The second part contains the remaining half.
   - The process repeats until all chunks are within the size limit.

3. **Chunk Aggregation**:
   - The split chunks are aggregated into `split_objects`.
   - If the current chunk exceeds the size limit for the current object, a new object is created, and the chunk is added to it.

4. **Completion**:
   - The logger logs the total number of parts generated and their adherence to the size limit.
   - The function returns the list of split objects.

### **Inputs**
| Entity               | Type          | Role                     | Notes                                   |
|----------------------|---------------|--------------------------|-----------------------------------------|
| `splited_by_files`   | `list[str]`   | Input Data               | List of text strings to be split.      |
| `max_symbols`        | `int`         | Maximum Symbols          | Maximum allowed size for each chunk.   |

### **Outputs**
| Entity               | Type          | Role                     | Notes                                   |
|----------------------|---------------|--------------------------|-----------------------------------------|
| `split_objects`      | `list[str]`   | Split Data               | List of text chunks within size limits.|

---
<a name="write-docs-by-parts-function"></a>
## **Function: `write_docs_by_parts`**

### **Purpose**
Generates documentation for a specific chunk of text using an AI model, incorporating project settings and global context.

### **Technical Logic Flow**
1. **Initialization**:
   - A logger instance logs the start of the documentation generation process.
   - A prompt is constructed using the project's metadata (`ProjectSettings.prompt`), global relations, and the input chunk.

2. **Prompt Construction**:
   - The prompt includes:
     - Language settings.
     - Project-specific metadata.
     - Global relations (if available).
     - Previous documentation context (if available).
     - The current chunk of text.

3. **AI Interaction**:
   - The AI model (`model.get_answer_without_history`) processes the prompt and generates documentation.
   - The generated documentation is cleaned by removing any markdown formatting (e.g., triple backticks).

4. **Completion**:
   - The logger logs the length and content of the generated documentation.
   - The cleaned documentation is returned.

### **Inputs**
| Entity               | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `part`               | `str`              | Input Chunk              | Text chunk for documentation generation. |
| `model`              | `Model`            | AI Model                 | AI model used for generating documentation. |
| `project_settings`   | `ProjectSettings`  | Project Metadata         | Contains project-specific metadata.     |
| `prev_info`          | `str | None`       | Previous Context         | Previously generated documentation (optional). |
| `language`           | `str`              | Language Setting         | Language for the generated documentation. |
| `global_info`        | `str | None`       | Global Relations         | Global project information (optional). |

### **Outputs**
| Entity               | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `answer`             | `str`              | Generated Documentation  | Documentation generated by the AI model.|

---
<a name="gen-doc-parts-function"></a>
## **Function: `gen_doc_parts`**

### **Purpose**
Generates documentation for an entire codebase by splitting it into manageable chunks and processing each chunk iteratively.

### **Technical Logic Flow**
1. **Data Splitting**:
   - Calls `split_data` to divide the input codebase (`full_code_mix`) into smaller chunks based on `max_symbols`.

2. **Documentation Generation**:
   - Initializes a logger and progress tracker (`BaseProgress`).
   - Iterates over the split chunks:
     - Calls `write_docs_by_parts` to generate documentation for each chunk.
     - Appends the generated documentation to the final result (`all_result`).
     - Updates the progress tracker after each chunk.

3. **Completion**:
   - Logs the total length of the generated documentation.
   - Removes the progress tracker subtask.
   - Returns the combined documentation.

### **Inputs**
| Entity               | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `full_code_mix`      | `str`              | Input Codebase           | Full codebase to be documented.         |
| `max_symbols`        | `int`              | Maximum Symbols          | Maximum size for each chunk.            |
| `model`              | `Model`            | AI Model                 | AI model used for generating documentation. |
| `project_settings`   | `ProjectSettings`  | Project Metadata         | Contains project-specific metadata.     |
| `language`           | `str`              | Language Setting         | Language for the generated documentation. |
| `progress_bar`       | `BaseProgress`     | Progress Tracker         | Tracks the progress of the task.        |
| `global_info`        | `str | None`       | Global Relations         | Global project information (optional).  |

### **Outputs**
| Entity               | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `all_result`         | `str`              | Final Documentation      | Combined documentation for the codebase.|

---
<a name="docfactory-class"></a>
## **`DocFactory` Class**

### **Functional Role**
The `DocFactory` class orchestrates modular documentation generation by invoking `BaseModule` instances and optionally splitting results into parts.

---

### **Technical Logic Flow**
1. **Initialization**:
   - Accepts a list of `BaseModule` instances and a flag (`with_splited`) to enable splitting results into parts.

2. **Documentation Generation**:
   - Iterates over the provided modules, invoking their `generate` method.
   - Splits module results into parts using `split_text_by_anchors` if `with_splited` is enabled.
   - Logs the output of each module and updates progress.

---

### **Data Contract**

| Entity               | Type               | Role                     | Notes                                      |
|----------------------|--------------------|--------------------------|--------------------------------------------|
| `modules`            | `list[BaseModule]` | Modular Components       | List of modules for generating documentation. |
| `logger`             | `BaseLogger`       | Logging Utility          | Tracks operations, errors, and warnings.   |
| `with_splited`       | `bool`             | Splitting Flag           | Enables splitting results into parts.      |
| `doc_head`           | `DocHeadSchema`    | Documentation Schema     | Stores generated documentation parts.      |

---

### **Critical Notes**
> - **Modular Design**: The factory pattern allows for easy addition of new modules.
> - **Splitting Results**: Splits documentation into smaller parts for better organization and readability.

---
<a name="doc-content-class"></a>
### **Class: `DocContent`**

#### **Purpose**
Represents individual documentation content with optional embedding vectors for semantic analysis.

#### **Attributes**
| Attribute            | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `content`            | `str`              | Documentation Content    | Stores the textual content of the documentation. |
| `embedding_vector`   | `list | None`      | Embedding Vector         | Semantic vector representation of the content. |

#### **Methods**
| Method               | Parameters         | Return Type              | Role                                     | Notes                                   |
|----------------------|--------------------|--------------------------|------------------------------------------|-----------------------------------------|
| `init_embedding`     | `embedding_model: Embedding` | `None`                 | Initializes the `embedding_vector` using the provided embedding model. | Calls `embedding_model.get_vector(content)` to generate embeddings. |

---
<a name="doc-schema"></a>
## **Module: `doc_schema.py`**

### **Purpose**
Defines the schema for structured documentation, including content management, embedding initialization, and hierarchical organization of documentation parts.

---

### **Classes**
<a name="doc-head-schema-class"></a>
### **Class: `DocHeadSchema`**

#### **Purpose**
Manages hierarchical organization of documentation parts and provides functionality to combine them into a full document.

#### **Attributes**
| Attribute            | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `content_orders`     | `list[str]`        | Content Order            | Maintains the order of documentation parts. |
| `parts`              | `dict[str, DocContent]` | Documentation Parts    | Stores individual documentation parts as `DocContent` objects. |

#### **Methods**
| Method               | Parameters         | Return Type              | Role                                     | Notes                                   |
|----------------------|--------------------|--------------------------|------------------------------------------|-----------------------------------------|
| `add_parts`          | `name: str, content: DocContent` | `None`                 | Adds a new documentation part to the schema. | Ensures unique names by appending an index if a name conflict occurs. |
| `get_full_doc`       | `split_el: str = "\n"` | `str`                   | Combines all documentation parts into a single document. | Concatenates `content` from all parts in `content_orders`. |
| `__add__`            | `other: DocHeadSchema` | `DocHeadSchema`         | Merges two `DocHeadSchema` objects.     | Adds all parts from `other` to the current schema. |

---
<a name="doc-info-schema-class"></a>
### **Class: `DocInfoSchema`**

#### **Purpose**
Represents the complete documentation schema, including global information, code mix, and hierarchical documentation structure.

#### **Attributes**
| Attribute            | Type               | Role                     | Notes                                   |
|----------------------|--------------------|--------------------------|-----------------------------------------|
| `global_info`        | `str`              | Global Information       | Stores general information about the project. |
| `code_mix`           | `str`              | Codebase Representation  | Contains the structured representation of the codebase. |
| `doc`                | `DocHeadSchema`    | Documentation Structure  | Stores the hierarchical structure of the documentation. |

---

### **Interactions**

#### **DocContent**
1. **Embedding Initialization**:
   - `init_embedding` method interacts with the `Embedding` class from `postprocessor.embedding`.
   - Generates semantic vectors based on the content for advanced search or analysis.

#### **DocHeadSchema**
1. **Part Management**:
   - Adds parts using `add_parts` and ensures unique naming.
   - Combines parts into a single document using `get_full_doc`.
2. **Schema Merging**:
   - Supports merging multiple schemas using the `__add__` method.

#### **DocInfoSchema**
1. **Global Information**:
   - Stores project-wide metadata in `global_info`.
2. **Codebase Representation**:
   - Maintains a structured representation of the codebase in `code_mix`.
3. **Documentation Structure**:
   - Uses `DocHeadSchema` to organize documentation parts.

---

### **Critical Notes**
> - **Embedding Integration**: `DocContent` relies on the `Embedding` class for semantic vector generation, enabling advanced search and analysis capabilities.
> - **Hierarchical Organization**: `DocHeadSchema` ensures proper ordering and management of documentation parts, supporting modular and extensible documentation workflows.
> - **Schema Extensibility**: The `DocInfoSchema` class provides a centralized structure for managing global information, codebase representation, and documentation hierarchy.

---
<a name="basemodule-class"></a>
## **`BaseModule` Abstract Base Class**

### **Functional Role**
Defines the interface for modular components used in the `DocFactory`. Each module must implement the `generate(info, model)` method.

---

### **Technical Logic Flow**
1. **Initialization**:
   - Provides a base structure for modular components.
2. **Abstract Method**:
   - `generate(info, model)`: Generates documentation based on the provided `info` and `model`.

---

### **Critical Notes**
> - **Extensibility**: New modules can be created by subclassing `BaseModule` and implementing the `generate` method.

---

### **Visible Interactions**
1. **`DocFactory`**:
   - Invokes `BaseModule.generate()` for each module during documentation generation.
2. **`split_text_by_anchors`**:
   - Optionally splits module results into smaller parts.

---

### **Terminal Points**
- The `DocFactory.generate_doc()` method returns a `DocHeadSchema` object containing all generated documentation parts.
<a name="custommodule-class"></a>
## **`CustomModule` Class**

### **Functional Role**
The `CustomModule` class generates documentation with contextual descriptions by leveraging AI models and preprocessed code data.

---

### **Technical Logic Flow**
1. **Initialization**:
   - Accepts a `discription` parameter to define the contextual description for documentation generation.

2. **Documentation Generation**:
   - Preprocesses the `code_mix` data using `split_data` to divide it into manageable chunks (default `max_symbols=5000`).
   - Calls `generete_custom_discription` to generate documentation using the AI model, contextual description, and language settings.

---

### **Data Contract**

| Entity               | Type               | Role                     | Notes                                      |
|----------------------|--------------------|--------------------------|--------------------------------------------|
| `discription`        | `str`              | Contextual Description   | Defines the context for documentation generation. |
| `info["code_mix"]`   | `dict`             | Preprocessed Code Data   | Contains structured code information.      |
| `info["language"]`   | `str`              | Language Setting         | Specifies the language for documentation.  |
| `model`              | `Model`           | AI Model                 | Generates documentation content.           |
| `result`             | `str`             | Generated Documentation  | Final output of the module.                |

---

### **Critical Notes**
> - **Contextual Generation**: The `discription` parameter is central to tailoring the generated documentation.
> - **Preprocessing Dependency**: Relies on `split_data` for chunking large code data before processing.

---
<a name="custommodulewithoutcontext-class"></a>
## **`CustomModuleWithOutContext` Class**

### **Functional Role**
The `CustomModuleWithOutContext` class generates documentation without contextual descriptions, focusing solely on the provided `discription`.

---

### **Technical Logic Flow**
1. **Initialization**:
   - Accepts a `discription` parameter to define the content for documentation generation.

2. **Documentation Generation**:
   - Calls `generete_custom_discription_without` to generate documentation using the AI model, `discription`, and language settings.

---

### **Data Contract**

| Entity               | Type               | Role                     | Notes                                      |
|----------------------|--------------------|--------------------------|--------------------------------------------|
| `discription`        | `str`              | Content Description      | Defines the content for documentation generation. |
| `info["language"]`   | `str`              | Language Setting         | Specifies the language for documentation.  |
| `model`              | `Model`           | AI Model                 | Generates documentation content.           |
| `result`             | `str`             | Generated Documentation  | Final output of the module.                |

---

### **Critical Notes**
> - **Simplified Generation**: Focuses on generating documentation without requiring contextual data.
> - **Language-Specific Output**: Adapts the generated content based on the `language` parameter.

---
<a name="intro-links-class"></a>
## **`IntroLinks` Class**

### **Functional Role**
The `IntroLinks` class extracts HTML links from the provided data and generates an introduction based on those links using AI models.

---

### **Technical Logic Flow**
1. **Link Extraction**:
   - Extracts all HTML links from `info["full_data"]` using `get_all_html_links`.

2. **Introduction Generation**:
   - Calls `get_links_intro` to generate an introduction based on the extracted links, AI model, and language settings.

---

### **Data Contract**

| Entity               | Type               | Role                     | Notes                                      |
|----------------------|--------------------|--------------------------|--------------------------------------------|
| `info["full_data"]`  | `str`              | Full Project Data        | Contains raw data including HTML links.    |
| `info["language"]`   | `str`              | Language Setting         | Specifies the language for documentation.  |
| `model`              | `Model`           | AI Model                 | Generates introduction content.            |
| `links`              | `list[str]`        | Extracted Links          | List of HTML links extracted from the data.|
| `intro_links`        | `str`             | Generated Introduction   | Final output of the module.                |

---

### **Critical Notes**
> - **Link-Based Introduction**: Tailors the introduction based on the presence of HTML links in the data.
> - **Preprocessing Dependency**: Relies on `get_all_html_links` for link extraction.

---
<a name="intro-text-class"></a>
## **`IntroText` Class**

### **Functional Role**
The `IntroText` class generates an introductory section for documentation based on global project information.

---

### **Technical Logic Flow**
1. **Introduction Generation**:
   - Calls `get_introdaction` to generate an introduction using the global project information, AI model, and language settings.

---

### **Data Contract**

| Entity               | Type               | Role                     | Notes                                      |
|----------------------|--------------------|--------------------------|--------------------------------------------|
| `info["global_info"]`| `str`              | Global Project Info      | Contains reusable global documentation data.|
| `info["language"]`   | `str`              | Language Setting         | Specifies the language for documentation.  |
| `model`              | `Model`           | AI Model                 | Generates introduction content.            |
| `intro`              | `str`             | Generated Introduction   | Final output of the module.                |

---

### **Critical Notes**
> - **Global Context**: Utilizes `global_info` to create a high-level introduction for the documentation.
> - **Language-Specific Output**: Adapts the generated content based on the `language` parameter.

---

### **Shared Observations**
1. **Modular Design**:
   - All classes extend `BaseModule`, ensuring consistency and reusability within the `DocFactory`.

2. **AI Model Dependency**:
   - Each module relies heavily on the `Model` class for generating content, making it a critical component of the system.

3. **Preprocessing and Postprocessing**:
   - Modules like `CustomModule` and `IntroLinks` depend on preprocessing functions (`split_data`, `get_all_html_links`).
   - Postprocessing functions (`generete_custom_discription`, `get_links_intro`) are central to transforming raw data into structured documentation.
<a name="postprocessor-custom-intro"></a>
## **Postprocessor: Custom Intro**

### **Functional Role**
The `custom_intro.py` module is responsible for generating various types of introductory content for documentation. It uses AI models to create link-based introductions, global introductions, and custom descriptions based on the provided context.

---

### **Technical Logic Flow**

#### **1. HTML Link Extraction**
- **Function:** `get_all_html_links(data: str) -> list[str]`
  - Uses regex to extract anchor links (`<a name="..."></a>`) from the input data.
  - Filters links based on length (`> 5 characters`) and prefixes them with `#`.
  - Logs the extraction process and outputs the list of links.

#### **2. Link-Based Introduction**
- **Function:** `get_links_intro(links: list[str], model: Model, language: str = "en") -> str`
  - Constructs a prompt using the extracted links and predefined instructions (`BASE_INTRODACTION_CREATE_LINKS`).
  - Sends the prompt to the AI model (`model.get_answer_without_history`) to generate an introduction.
  - Logs the generated introduction.

#### **3. Global Introduction**
- **Function:** `get_introdaction(global_data: str, model: Model, language: str = "en") -> str`
  - Constructs a prompt using global project data and predefined instructions (`BASE_INTRO_CREATE`).
  - Sends the prompt to the AI model to generate an introduction.
  - Returns the generated introduction.

#### **4. Custom Description Generation**
- **Function:** `generete_custom_discription(splited_data: str, model: Model, custom_description: str, language: str = "en") -> str`
  - Iterates over split data chunks (`splited_data`).
  - Constructs a detailed prompt using the chunk, predefined instructions (`BASE_CUSTOM_DISCRIPTIONS`), and the custom description task.
  - Sends the prompt to the AI model to generate a description.
  - Breaks the loop if a valid description is generated; otherwise, retries with the next chunk.

#### **5. Custom Description Without Context**
- **Function:** `generete_custom_discription_without(model: Model, custom_description: str, language: str = "en") -> str`
  - Constructs a prompt using predefined instructions for rewriting and describing text.
  - Enforces strict rules for content formatting (e.g., single `
<a name="manager-class-usage-and-methods"></a>

### Manager Class Usage and Methods

The `Manager` class is instantiated and used in the `gen_doc` function. Based on the provided context, the `Manager` class is responsible for managing the documentation generation process. It interacts with various components such as configuration, models, embedding layers, and progress tracking.

#### How to Use the `Manager` Class
1. **Initialization**:
   - The `Manager` class is initialized with the following parameters:
     - `project_path`: The path to the project for which documentation is being generated.
     - `config`: A `Config` object containing project configuration details.
     - `llm_model`: A language model instance (e.g., `GPT4oModel`, `AzureModel`, etc.).
     - `embedding_model`: An embedding model instance (e.g., `Embedding`).
     - `progress_bar`: A progress bar instance (e.g., `ConsoleGtiHubProgress`).

2. **Workflow**:
   - The `Manager` class is used to perform various tasks such as loading project information, generating documentation, managing global files, creating embedding layers, and saving the final output.

#### Methods Used in the Context
The following methods of the `Manager` class are explicitly used in the provided context:
1. **`load_all_info()`**:
   - Loads all necessary information about the project.

2. **`save()`**:
   - Saves the current state of the manager, including generated documentation.

3. **`generate_code_file()`**:
   - Generates a code file as part of the documentation process.

4. **`generate_global_info(compress_power: int, is_reusable: bool)`**:
   - Generates global information for the documentation.
   - Parameters:
     - `compress_power`: Controls the level of compression for the global information.
     - `is_reusable`: Indicates whether the global information can be reused.

5. **`generete_doc_parts(max_symbols: int, with_global_file: bool)`**:
   - Generates parts of the documentation.
   - Parameters:
     - `max_symbols`: Maximum number of symbols allowed in each part.
     - `with_global_file`: Indicates whether to include global information in the documentation parts.

6. **`factory_generate_doc(factory: DocFactory, to_start: bool = False)`**:
   - Generates documentation using a factory pattern.
   - Parameters:
     - `factory`: An instance of `DocFactory` containing custom modules.
     - `to_start`: If `True`, the generated documentation is added to the start.

7. **`order_doc()`**:
   - Orders the documentation parts.

8. **`create_embedding_layer()`**:
   - Creates an embedding layer for the documentation.

9. **`clear_cache()`**:
   - Clears the cache used during the documentation generation process.

#### Code Example
Below is an example of how to use the `Manager` class based on the provided context:

```python
from autodocgenerator.manage import Manager
from autodocgenerator.factory.base_factory import DocFactory
from autodocgenerator.ui.progress_base import ConsoleGtiHubProgress
from autodocgenerator.engine.models.gpt_model import GPT4oModel
from autodocgenerator.postprocessor.embedding import Embedding
from autodocgenerator.schema.cache_settings import CheckGitStatusResultSchema

# Configuration and model setup
project_path = "path/to/your/project"
config = Config()  # Initialize Config object and set necessary configurations
llm_model = GPT4oModel(api_keys="your_api_keys", use_random=False)
embedding_model = Embedding(api_key="your_google_embedding_api_key")
progress_bar = ConsoleGtiHubProgress()

# Initialize Manager
manager = Manager(
    project_path=project_path,
    config=config,
    llm_model=llm_model,
    embedding_model=embedding_model,
    progress_bar=progress_bar,
)

# Load project information
manager.load_all_info()

# Generate code file
manager.generate_code_file()

# Generate global information
manager.generate_global_info(compress_power=4, is_reusable=True)

# Generate documentation parts
manager.generete_doc_parts(max_symbols=5000, with_global_file=True)

# Use a factory to generate documentation with custom modules
custom_modules = []  # List of custom modules
doc_factory = DocFactory(*custom_modules)
manager.factory_generate_doc(doc_factory)

# Order the documentation
manager.order_doc()

# Create embedding layer
manager.create_embedding_layer()

# Clear cache
manager.clear_cache()

# Save the documentation
manager.save()
```

This example demonstrates the initialization and usage of the `Manager` class, along with its key methods. Note that some details, such as the `Config` object setup and API keys, need to be provided based on your specific use case.
