**Project Title**  
**AutoDoc** – A lightweight, Groq‑powered framework that turns an entire Python repository into a single, richly‑linked Markdown document.

---

## Project Goal  
AutoDoc automates the generation of high‑quality documentation for any codebase by:

1. Providing a **drop‑in LLM wrapper** that manages conversation history, model fall‑back, and synchronous/asynchronous usage.  
2. Running a **four‑stage pipeline** – repo dump → global summary → chunked documentation → intro & table of contents – that produces a self‑contained Markdown file complete with intra‑document links.

The result is a single file that can be viewed in any Markdown renderer and offers a searchable, navigable view of the project’s architecture and APIs with almost no manual effort.

---

## Core Logic & Principles

| Layer | Purpose | Key Technologies |
|-------|---------|-------------------|
| **LLM Wrapper (`engine/`)** | Normalises interaction with Groq‑hosted GPT models. | `groq` SDK, async/await, custom `History` class for chat context. |
| **Model Fallback** | Guarantees a response even if one or more models fail. | Ordered `MODELS_NAME` list, error logging, dynamic pruning (sync) or temporary skipping (async). |
| **Auto‑Documentation Pipeline (`manage.py`)** | Orchestrates the four stages that produce the final Markdown file. | File system traversal (`fnmatch`), string manipulation, `rich.Progress`, and the LLM wrapper. |

### 1. LLM Wrapper

* `History` keeps an ordered list of messages and automatically injects a default system prompt (`BASE_SYSTEM_TEXT`).  
* `Model` (sync) and `AsyncModel` expose the same public API (`get_answer`, `get_answer_without_history`).  
* Concrete subclasses (`GPTModel`, `AsyncGPTModel`) build the message payload, iterate over `MODELS_NAME`, and retry on failure. The sync variant permanently removes a broken model; the async variant simply skips it for that call.  
* The wrapper returns the first choice’s content, giving a clean, one‑liner interface: `model.get_answer("…")`.

### 2. Repository Dump

`CodeMix.build_repo_content` walks the target directory recursively, respecting a glob‑style ignore list.  
For every file it writes a *tree view* line and the raw contents wrapped in `<file path="…"> … </file>` tags to `code_mix.txt` inside a hidden `.auto_doc_cache` folder.

### 3. Chunking & Compression

1. **Splitting** – `preprocessor.spliter.split_data` divides a long string into chunks ≤ `MAX_SYMBOLS` (≈ 5 000 symbols), attempting to split on natural delimiters (file tags).  
2. **Compression** – `preprocessor.compressor.compress` repeatedly asks the LLM to produce a summary of the current chunks (`BASE_COMPRESS_TEXT`).  
   * `compress_to_one` is called until a single block remains, yielding `global_info.md`.  
3. **Chunk‑wise Documentation** – `write_docs_by_parts` builds a three‑message prompt that contains the current chunk, the global summary, and an optional tail of the previous fragment (~3 000 symbols).  
   * The LLM produces a Markdown fragment; any surrounding triple‑backtick fences are stripped automatically.  
   * The fragment is appended to `output_doc.md`, and its tail is kept as overlap for the next iteration.

### 4. Intro & Table of Contents

`preprocessor.postprocess` scans `output_doc.md` for `<a name=…>` anchors, turns them into a markdown bullet list, and then asks the LLM (with `BASE_INTRODACTION_CREATE_TEXT` and `BASE_INTRO_CREATE`) to write a short introduction and the link list.  
The two pieces are prepended to `output_doc.md`, producing the final document.

---

## Key Features

* **Synchronous and asynchronous LLM interaction** – a single, consistent API works in both blocking and non‑blocking code.  
* **Automatic model fall‑back** – a list of Groq models is tried in order; the wrapper removes broken models permanently (sync) or skips them temporarily (async).  
* **Context‑aware history** – `History` injects a default system prompt and stores all interactions for easy reuse or persistence.  
* **Repo‑wide Markdown generation** – a four‑step pipeline that produces a global summary, chunked docs with overlap, and a final intro/TOC.  
* **Configurable** – ignore patterns, chunk sizes, prompt templates, and model list are all user‑editable.  
* **Lightweight** – only the `groq`, `python-dotenv`, and `rich` packages are required.  
* **Cacheable** – intermediate artefacts (`code_mix.txt`, `global_info.md`, `output_doc.md`) live in `.auto_doc_cache`, enabling partial re‑runs.

---

## How to Run

### 1. Install the dependencies

```bash
# Create and activate a virtual environment if you wish
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate

# Install core packages
pip install --upgrade pip
pip install groq python-dotenv rich
```

### 2. Prepare the environment

Create a `.env` file in the project root containing your Groq API key:

```
API_KEY=YOUR_GROQ_API_KEY
```

### 3. Execute the documentation generator

The script contains a small CLI skeleton; modify the `__main__` block to point to your target repository.

```bash
python manage.py <path-to-repo>
```

Example:

```bash
python manage.py ../my-python-project
```

The script will:

1. Dump the repository into `.auto_doc_cache/code_mix.txt`.  
2. Compress the dump into `.auto_doc_cache/global_info.md`.  
3. Generate `output_doc.md` in the repository root, which includes the intro, table of contents, and all generated documentation fragments.

Open `output_doc.md` in any Markdown viewer to see a fully navigable, AI‑generated documentation of the entire codebase.

### 4. Using the LLM wrapper directly

#### Synchronous

```python
from engine.models.gpt_model import GPTModel

model = GPTModel()  # API key is read from .env automatically
print(model.get_answer("Explain the difference between list and tuple."))

# Stateless call
messages = [
    {"role": "system", "content": "You are a concise assistant."},
    {"role": "user",   "content": "List three sorting algorithms."}
]
print(model.get_answer_without_history(messages))
```

#### Asynchronous

```python
import asyncio
from engine.models.gpt_model import AsyncGPTModel

async def demo():
    model = AsyncGPTModel()
    answer = await model.get_answer("What is Groq?")
    print(answer)

asyncio.run(demo())
```

---

## Dependencies

| Package | Version | Notes |
|---------|---------|-------|
| **groq** | ≥ 1.0 | Official Groq SDK for chat completions. |
| **python-dotenv** | ≥ 1.0 | Loads `.env` files. |
| **rich** | ≥ 12.0 | Optional; provides progress bars and console formatting. |

> *If you wish to add a different LLM provider, create a subclass of `Model`/`AsyncModel` and implement `generate_answer`. The rest of the pipeline remains unchanged.*

---

## Extending / Customising

| What | How |
|------|-----|
| New LLM provider | Subclass `Model` or `AsyncModel`, initialise the client in `__init__`, and implement `generate_answer`. |
| System prompt | Pass `system_prompt="…"` when constructing `History`, or change `BASE_SYSTEM_TEXT` in `config.py`. |
| Conversation persistence | Serialize `history.history` to JSON and reload into a fresh `History` instance. |
| Chunk sizes | Adjust `MAX_GLOBAL_SYMBOLS` / `MAX_SYMBOLS` in `manage.py`. |
| Prompt templates | Edit the large strings in `engine/config/config.py`. |
| Partial runs | Delete or modify any file under `.auto_doc_cache/` to skip the corresponding stage. |

---

## Architectural Snapshot (textual)

```
User code ──► Manager ──► CodeMix          → .auto_doc_cache/code_mix.txt
                      │
                      ├─► Spliter → list of 5k‑symbol chunks
                      ├─► Compressor → global_info.md
                      ├─► For each chunk:
                      │     ├─► write_docs_by_parts → fragment
                      │     └─► Append to output_doc.md (keep tail)
                      └─► Postprocess → intro + TOC
                                 └─► Prepend → final output_doc.md
```

---

**Bottom line**  
AutoDoc provides a minimal, reusable LLM wrapper for Groq APIs and a fully‑automated pipeline that transforms any Python repository into a coherent, markdown‑formatted documentation file. Adjust the ignore list, chunk sizes, or prompt templates to suit your project’s scale, language, or target LLM provider, and enjoy a near‑instant, high‑quality documentation output with no manual markup required.

**Introduction**  
The following Executive Navigation Tree distills the most critical components of the LLM‑integration engine into a concise, 50 % density hierarchy. It focuses on the core modules that drive engine initialization, model handling, and orchestration logic, while omitting peripheral utilities, FAQ sections, and repetitive sub‑headings. Use this structure as a quick reference when exploring the repository or drafting documentation.

---

## 📂 Executive Navigation Tree

📂 Engine
  ⚙️ [engine_init](#engine_init)
  📄 [config-module-overview](#config-module-overview)
  📄 [engine-models-overview](#engine-models-overview)
  ⚙️ [integration-with-pipeline](#integration-with-pipeline)

📂 Models
  📄 [abstract-model](#abstract-model)
  📄 [gptmodel](#gptmodel)
  📄 [asyncgptmodel](#asyncgptmodel)

📂 Manager
  ⚙️ [manager-overview](#manager-overview)
  📄 [responsibility](#responsibility)
  📄 [assumptions-and-limitations](#assumptions-and-limitations)
  📄 [extending](#extending)


> *Note:*  
> The link texts are retained verbatim; anchors are preserved exactly as generated by the script. This ensures that internal navigation remains functional without accidental link breaks.
 

<a name="engine_init"></a>
## engine/__init__.py  

**Purpose**  
`engine/__init__.py` is the public entry‑point of the **LLM wrapper package**. It makes the most frequently used classes (`History`, `Model`, `AsyncModel`, `GPTModel`, `AsyncGPTModel`) importable directly from `engine`, e.g.:

```python
from engine import GPTModel, History
```

**Responsibility within the system**  
The wrapper lives in `engine/` and provides a thin, unified API that the rest of the auto‑documentation pipeline (see `manage.py` and the `preprocessor/` helpers) uses to talk to Groq‑hosted LLMs. By re‑exporting the core symbols here, the package hides the internal folder layout and prevents callers from having to know whether a class lives in `engine.models.model` or `engine.models.gpt_model`.

**How it interacts with other components**  

| Component | Interaction |
|-----------|-------------|
| `engine/config/config.py` | Imported by the model classes; `__init__` does **not** touch it directly, but re‑exports classes that depend on the configuration (e.g., system prompts, fallback model list). |
| `engine/models/model.py` | Provides the abstract `History`, `Model`, and `AsyncModel`. These are re‑exported so external code can instantiate a `Model` without digging into the sub‑module. |
| `engine/models/gpt_model.py` | Concrete implementations (`GPTModel`, `AsyncGPTModel`) that perform the actual Groq API calls. They are also re‑exported here. |
| `manage.py` & `preprocessor/*` | Import the wrapper via `from engine import GPTModel` (or `AsyncGPTModel`) to generate documentation chunks, global summaries, and introductions. |

**Key symbols re‑exported**  

| Symbol | Origin | Brief description |
|--------|--------|-------------------|
| `History` | `engine.models.model` | Holds the message list (`role`, `content`) for a conversation; automatically seeds the system prompt. |
| `Model` | `engine.models.model` | Synchronous façade with `get_answer` and `get_answer_without_history`. |
| `AsyncModel` | `engine.models.model` | Asynchronous counterpart of `Model`. |
| `GPTModel` | `engine.models.gpt_model` | Concrete synchronous model that builds a `groq.Groq` client, handles fallback across `config.MODELS_NAME`, and updates the global failure list. |
| `AsyncGPTModel` | `engine.models.gpt_model` | Same as `GPTModel` but uses `groq.AsyncGroq` and `await`‑based calls; does **not** prune failing models. |

**Assumptions**  

* The package is imported **after** the environment variable `API_KEY` (read in `config/config.py`) has been set, otherwise the model constructors will raise a configuration error.  
* The symbols exported here are stable; internal implementation may evolve, but the public API (`History`, `Model`, `GPTModel`, …) will remain backward compatible.  

**Inputs / Outputs**  

* **Input** – Import statements; no runtime arguments.  
* **Output** – A module namespace that exposes the six classes listed above. No side‑effects occur at import time beyond the usual Python module loading (e.g., reading `.env` via `config.py`).  

**Side effects**  

* Importing `engine` triggers the import of `engine.config.config`, which reads the `.env` file to load `API_KEY`. This is the only side effect; the wrapper itself does not perform network calls until a model method is invoked.  

**Typical usage pattern**  

```python
# High‑level entry point for developers
from engine import GPTModel, History

# Create a model with default system prompt
model = GPTModel()
answer = model.get_answer("Explain how the chunk splitter works.")
print(answer)

# If you need a fresh conversation without persisting history:
custom_history = History(system_prompt="You are a terse assistant.")
model = GPTModel(history=custom_history)
```

**Why this file matters**  
Providing a clean `engine` namespace simplifies the learning curve for new contributors: they can focus on *what* the wrapper does rather than *where* the implementation lives. It also enables tools such as `pytest` or IDE auto‑completion to discover the public API in a single location.

<a name="config-module-overview"></a>
## config.py – Central configuration & prompt library  

**Location**: `engine/config/config.py`  

### Responsibility  
`config.py` centralises all static data that drives the auto‑documentation pipeline and the LLM wrapper:

* **System‑level prompts** (`BASE_SYSTEM_TEXT`, `BASE_COMPRESS_TEXT`, `BASE_PART_COMPLITE_TEXT`,
  `BASE_INTRODACTION_CREATE_TEXT`, `BASE_INTRO_CREATE`) – multi‑line strings injected into the
  message history of every LLM request.  
* **Dynamic prompt generator** – `get_BASE_COMPRESS_TEXT(start, power)` builds a size‑aware version
  of the compression prompt.  
* **Runtime configuration** – loads the Groq API key from a `.env` file and exposes the ordered
  fallback model list (`MODELS_NAME`).  

All other modules (`engine/models/*`, `manage.py`, the pre‑processor helpers) import these symbols
to keep prompt text and environment handling in a single, easily editable place.

### Interaction with the rest of the system  

| Component | How it uses `config.py` |
|-----------|------------------------|
| `engine/models/model.py` – `History` | Takes `BASE_SYSTEM_TEXT` as the default system message when a new conversation is started. |
| `engine/models/gpt_model.py` | Calls `MODELS_NAME` to iterate over candidate Groq models; on failure it removes the broken entry from this global list. |
| `preprocessor/compressor.py` | Passes the static `BASE_COMPRESS_TEXT` (or the result of `get_BASE_COMPRESS_TEXT`) as the system prompt for “compress‑to‑summary” calls. |
| `preprocessor/postprocess.py` | Uses `BASE_INTRODACTION_CREATE_TEXT` and `BASE_INTRO_CREATE` to ask the LLM to generate the navigation tree and the project introduction. |
| `manage.py` | Reads `API_KEY` indirectly via the import of `config.py`; the presence of a valid key is required before any model can be instantiated. |

### Key symbols  

| Symbol | Type | Purpose |
|--------|------|---------|
| `BASE_SYSTEM_TEXT` | `str` | Default system message that tells the model to treat each incoming snippet as part of a larger code base and to keep context across calls. |
| `BASE_COMPRESS_TEXT` | `str` | Prompt used when a large code chunk must be “compressed” into a concise summary (≈ 5 k characters). |
| `BASE_PART_COMPLITE_TEXT` | `str` | Prompt for the *per‑part* documentation stage – asks the model to write a ~2 k‑symbol description of a single code fragment. |
| `BASE_INTRODACTION_CREATE_TEXT` | `str` | Prompt that forces the model to produce a high‑level navigation tree, preserving generated anchors exactly. |
| `BASE_INTRO_CREATE` | `str` | Prompt for the final project‑level introduction (title, goal, core logic, etc.). |
| `get_BASE_COMPRESS_TEXT(start, power)` | `function` | Returns a customised compression prompt where the maximum input size (`start`) and the target output size (`start/power`) are injected dynamically. |
| `API_KEY` | `str` | Groq API token read from the environment (`.env`). Required for any network request. |
| `MODELS_NAME` | `list[str]` | Ordered list of model identifiers. The synchronous wrapper removes a model from this list permanently after a failure; the asynchronous wrapper only skips it for the current call. |

### Important assumptions  

* The `.env` file exists at the project root and contains a valid `API_KEY`.  
* Prompt strings are UTF‑8 and may contain triple‑quoted newlines; they are passed verbatim to the LLM.  
* `MODELS_NAME` order reflects preferred fall‑back hierarchy; changing the order changes which model is tried first.  
* `get_BASE_COMPRESS_TEXT` is called with `start` roughly equal to the length of the chunk being compressed; `power` determines how aggressively the output size is reduced.  

### Inputs / Outputs  

* **Inputs** – No function arguments except for `get_BASE_COMPRESS_TEXT`. All other symbols are constants read at import time.  
* **Outputs** – Exported names become module attributes that other code imports. `get_BASE_COMPRESS_TEXT` returns a formatted prompt string.  

### Side effects  

* Importing this module triggers `load_dotenv()` which reads the `.env` file and populates `os.environ`.  
* No network calls or file writes occur at import time; the only side effect is the environment variable loading.  

### Typical usage pattern  

```python
# Somewhere in the LLM wrapper
from engine import Model, GPTModel, History   # imports re‑exported symbols
from engine.config import BASE_SYSTEM_TEXT, MODELS_NAME

# Build a History with the default system prompt
hist = History()                     # uses BASE_SYSTEM_TEXT automatically
model = GPTModel(history=hist)       # will fall back through MODELS_NAME
answer = model.get_answer("Explain the chunk splitter.")
```

Or for a dynamic compression prompt:

```python
from engine.config import get_BASE_COMPRESS_TEXT

prompt = get_BASE_COMPRESS_TEXT(start=8000, power=2)
# `prompt` now contains a system message tuned for an 8 k‑char chunk,
# requesting a ~4 k‑char summary.
```

### Why this file matters  

By gathering all prompts, environment loading, and fallback model configuration in a single module, `config.py` provides a **single source of truth** for the behaviour of the entire documentation pipeline. New contributors only need to edit this file to adjust the tone, size limits, or model preferences, without touching the core wrapper or the orchestration logic. This clear separation improves maintainability, testability, and reduces the risk of accidental prompt drift across the codebase.

<a name="engine-models-overview"></a>
## engine/models – LLM Wrapper Core  

The two modules **`model.py`** and **`gpt_model.py`** implement the low‑level API that the rest of the auto‑documentation pipeline (see the global description) uses to talk to Groq‑hosted language models.  
Their responsibilities are:

* **`History`** – keep a mutable list of chat messages (`role`, `content`). The list is automatically seeded with the system prompt defined in `engine/config/config.py` (`BASE_SYSTEM_TEXT`).  
* **`Model` / `AsyncModel`** – abstract façade exposing a *synchronous* (`get_answer`, `get_answer_without_history`) and an *asynchronous* (`await get_answer`, `await get_answer_without_history`) API.  
* **`GPTModel` / `AsyncGPTModel`** – concrete subclasses that instantiate a Groq client (`Groq` or `AsyncGroq`) and implement `generate_answer` by calling the remote *chat/completions* endpoint, handling model fall‑back logic defined by `MODELS_NAME`.

These classes are the only place where network I/O occurs; everything else in the project builds prompts and hands them to `model.get_answer*()`.

---

<a name="history-class"></a>
### `History` (engine/models/model.py)

| Attribute | Meaning |
|-----------|---------|
| `history` | `list[dict]` – ordered messages `{"role": "...", "content": "..."}` |
| `__init__(system_prompt=BASE_SYSTEM_TEXT)` | Starts with an empty list; if `system_prompt` is not `None` it is added as the first *system* message. |
| `add_to_history(role, content)` | Append a new entry; used by `Model`/`AsyncModel` when a user or assistant turn occurs. |

**Assumptions**  
* The system prompt is a short string; it is stored once per `History` instance.  
* No persistence – the list lives only for the lifetime of the `Model` object.

---

<a name="abstract-model"></a>
### `Model` (synchronous) and `AsyncModel` (asynchronous)

Both expose the same public surface:

* `get_answer(prompt: str) -> str` – records the user turn, calls `generate_answer` (which may use the stored `history`), records the assistant turn, returns the answer.  
* `get_answer_without_history(prompt: list[dict]) -> str` – bypasses the internal `History` and forwards a ready‑made message list directly to `generate_answer`.  

`generate_answer` is **abstract** here; subclasses replace it with real API calls. The default implementation returns the literal string `"answer"` – a harmless placeholder that is never used in production because concrete subclasses override it.

**Side‑effects**  
* Mutates `self.history` (adds *user* and *assistant* entries).  
* Returns the raw content string from the LLM (no markdown stripping, that is handled later in the pipeline).

---

<a name="gptmodel"></a>
### `GPTModel` – synchronous concrete wrapper

```python
class GPTModel(Model):
    def __init__(self, api_key=API_KEY):
        super().__init__(api_key)
        self.client = Groq(api_key=self.api_key)
```

* **Client** – an instance of `groq.Groq`, created with the API key loaded from `.env` by `engine/config/config.py`.  
* **`generate_answer(with_history=True, prompt=None)`**  
  1. Selects the message list: `self.history.history` if `with_history` else the supplied `prompt`.  
  2. Iterates over the global `MODELS_NAME` list.  
  3. Calls `self.client.chat.completions.create(messages=…, model=model_name)`.  
  4. On **success** → returns the first choice’s `content`.  
  5. On **exception** → prints the error, records the failing model name in `models_del`.  
  6. After the loop, removes every failing model from `MODELS_NAME` (permanent fallback pruning).  
  7. If no model succeeded, raises `Exception("all models do not work")`.

**Key behaviours**  
* **Permanent fallback pruning** – ensures that subsequent calls never retry a model that has already failed in the current Python process.  
* **Single‑choice extraction** – assumes the API returns at least one `choice`.  

**Inputs / Outputs**  
* `with_history`: bool (default `True`).  
* `prompt`: optional pre‑built message list (used only when `with_history=False`).  
* Returns a plain string (`chat_completion.choices[0].message.content`).  

---

<a name="asyncgptmodel"></a>
### `AsyncGPTModel` – asynchronous counterpart

```python
class AsyncGPTModel(AsyncModel):
    def __init__(self, api_key=API_KEY):
        super().__init__(api_key)
        self.client = AsyncGroq(api_key=self.api_key)
```

* Uses `groq.AsyncGroq` and `await` for the same endpoint.  
* The fallback loop **does not modify** `MODELS_NAME`; it simply tries the next model on each exception. This keeps the list unchanged for future async calls, matching the design note in the global description.

**Signature**  

```python
async def generate_answer(self, with_history: bool = True, prompt: str = None) -> str
```

Same logic as the sync version, but:

* `await self.client.chat.completions.create(...)`  
* Returns the content after the first successful call, otherwise raises the same generic exception.  

---

<a name="integration-with-pipeline"></a>
## Interaction with the Rest of the System  

| Component | How it uses the wrapper |
|-----------|------------------------|
| **`preprocessor/compressor.py`** | Calls `GPTModel().get_answer_without_history(messages)` to compress large code chunks; relies on the fallback behaviour to keep the pipeline running even if a model is temporarily unavailable. |
| **`preprocessor/spliter.py`** | Does not call the wrapper directly – it only prepares text that will later be fed to `write_docs_by_parts`, which in turn uses the same `GPTModel` API. |
| **`manage.py → Manager`** | Instantiates `GPTModel` (or `AsyncGPTModel`) once per stage and repeatedly invokes `model.get_answer` / `model.get_answer_without_history`. The stored `History` instance automatically carries the system prompt and any earlier dialogue, providing context for the LLM throughout the four‑stage pipeline. |
| **`engine/config/config.py`** | Supplies `BASE_SYSTEM_TEXT`, `MODELS_NAME`, and `API_KEY` that drive the wrapper’s behaviour. Changing any of these constants immediately affects every model instance because they are imported at module load time. |

---

<a name="assumptions-and-limitations"></a>
## Important Assumptions & Limitations  

* **API key availability** – `API_KEY` is read once at import via `load_dotenv()` (performed in `config.py`). If the env variable is missing, the client constructors will raise an authentication error.  
* **Message format** – The wrapper expects a list of dicts matching OpenAI‑style chat schema (`role`, `content`). No validation is performed.  
* **Single‑choice responses** – If the provider returns multiple choices, only the first is used.  
* **Thread‑safety** – `MODELS_NAME` is a mutable global list; the synchronous `GPTModel` removes failing entries, which is safe only when a single thread manipulates the list. In a multi‑threaded context you should protect it or avoid the sync wrapper.  
* **Error handling** – Exceptions from the Groq client are caught, printed, and the loop continues. The final generic exception provides little diagnostic information; callers may want to wrap `model.get_answer*()` in their own try/except for richer logging.

---

<a name="extending"></a>
## Extending / Customising  

* **Add a new provider** – Subclass `Model` (or `AsyncModel`), create the appropriate client, and implement `generate_answer`.  
* **Change fallback policy** – Modify the loop in `GPTModel.generate_answer` (e.g., keep a per‑instance blacklist instead of mutating the global list).  
* **Inject custom system prompts** – Pass a `History(system_prompt="…")` instance to the model constructor; the default uses `BASE_SYSTEM_TEXT`.  
* **Support streaming** – Replace the call to `chat.completions.create` with the provider’s streaming endpoint and concatenate the streamed chunks before returning.  

---

<a name="summary"></a>
## Summary  

`engine/models/model.py` defines a lightweight conversation history and abstract base classes for sync/async LLM interaction. `engine/models/gpt_model.py` provides concrete implementations that talk to Groq, automatically handle model fall‑back, and expose a clean one‑line API (`model.get_answer(...)` or `model.get_answer_without_history(...)`). These components are the backbone of the documentation generator: every stage that needs LLM inference routes through them, benefitting from built‑in context management, fallback robustness, and a unified synchronous/asynchronous interface.

<a name="manager-overview"></a>
## `Manager` – Orchestrator of the Auto‑Documentation Pipeline  

The **`Manager`** class lives in **`manage.py`** and is the glue that ties together every component of the tiny LLM‑driven documentation framework described in the global overview.  
It is *not* a model or a tokenizer – it merely coordinates file‑system layout, chunking, LLM calls, and post‑processing, exposing a small, high‑level API that can be used from a script or from other Python code.

---

<a name="responsibility"></a>
### Responsibility  
* Create and maintain a hidden cache directory (`.auto_doc_cache`) inside the target project.  
* Run the four pipeline stages in order:  
  1. **Code dump** – generate `code_mix.txt` with `CodeMix`.  
  2. **Global summary** – split the dump, compress it repeatedly, write `global_info.md`.  
  3. **Chunk‑wise documentation** – split the original dump into ~5 k‑symbol pieces, call `write_docs_by_parts` for each piece, store the concatenated result in `output_doc.md`.  
  4. **Intro & TOC** – extract `<a name=…>` anchors, ask the LLM to create an introduction and a link list, prepend them to `output_doc.md`.  

All I/O is performed under the cache folder so that intermediate artefacts survive between runs and can be inspected manually.

---

<a name="interaction"></a>
### Interaction with Other Modules  

| Module / Function | How `Manager` uses it |
|-------------------|-----------------------|
| **`preprocessor.code_mix.CodeMix`** | Instantiated with the project root and ignore list; `build_repo_content` writes the raw repository dump to `code_mix.txt`. |
| **`preprocessor.spliter.split_data`** | Called twice – once on the full dump (global summary) with `MAX_GLOBAL_SYMBOLS = 10 000`, and once on the same dump for documentation chunks (`MAX_SYMBOLS = 5 000`). |
| **`preprocessor.compressor.compress_to_one`** | Takes the list of global‑summary chunks, repeatedly compresses them using the LLM (via `GPTModel`), and returns a single markdown block (`global_info.md`). |
| **`preprocessor.spliter.write_docs_by_parts`** | Core per‑chunk LLM call. Receives the current code chunk, the global summary, and the tail of the previous answer (≈3 k symbols) to keep continuity. Returns the generated documentation fragment. |
| **`preprocessor.postprocess.get_all_html_links` / `get_introdaction`** | After all fragments are written, these helpers scan `output_doc.md` for `<a name=…>` anchors, ask the LLM to turn them into a markdown TOC and an introductory paragraph, then prepend the result. |
| **`rich.Progress`** | Optional visual progress bar; `Manager` creates sub‑tasks for the chunk loop and updates the main task after each stage. |

All LLM interaction is performed **through the `GPTModel`/`AsyncGPTModel` wrapper**, so `Manager` never deals with the raw Groq client directly.

---

<a name="key-functions"></a>
### Key Methods  

| Method | Purpose | Important Behaviour |
|--------|---------|---------------------|
| `__init__(project_directory, ignore_files=[], progress_bar=None)` | Stores paths, creates the cache folder if missing. | No side‑effects beyond `os.mkdir` of the cache folder. |
| `get_file_path(file_key)` | Returns the absolute path of a cached artefact (`code_mix`, `global_info`, `output_doc`). | Uses the `FILE_NAMES` mapping; raises `None` if an unknown key is supplied. |
| `generate_code_file()` | Dumps the repository (respecting `ignore_files`) to `code_mix.txt`. | Relies on `CodeMix.build_repo_content`; overwrites any existing file. |
| `generate_global_info_file()` | Produces a concise project‑wide summary (`global_info.md`). | Reads `code_mix.txt`, splits with `MAX_GLOBAL_SYMBOLS`, calls `compress_to_one(..., power=2)`. |
| `generete_doc_parts()` *(sic)* | Walks the chunk list, calls `write_docs_by_parts` for each, writes results to `output_doc.md`. | After each fragment it keeps the last 3 000 characters (`result = result[-3000:]`) to feed the next call, guaranteeing overlap. Updates a `rich.Progress` sub‑task. |
| `generate_intro()` | Builds the final intro and table of contents, prepends them to `output_doc.md`. | Reads the current document, extracts anchors via `get_all_html_links`, creates intro with `get_introdaction`, then rewrites the file. |

---

<a name="assumptions-outputs"></a>
### Assumptions, Inputs & Outputs  

* **Assumptions**  
  * The supplied `project_directory` is a readable Python project.  
  * `ignore_files` follows Unix‑style glob patterns; they are applied by `CodeMix`.  
  * An environment variable `API_KEY` is present so that the underlying `GPTModel` can authenticate to Groq.  
  * The LLM token budget comfortably exceeds `MAX_GLOBAL_SYMBOLS` and `MAX_SYMBOLS`; the chunker ensures each request stays below the limit.  

* **Inputs**  
  * Filesystem tree of the target repo.  
  * Optional `Progress` object for UI feedback.  

* **Outputs (all under `.auto_doc_cache`)**  
  * `code_mix.txt` – raw repository dump with `<file>` tags.  
  * `global_info.md` – compressed project overview.  
  * `output_doc.md` – final markdown documentation, including intro and intra‑document links.  

* **Side Effects**  
  * Creates/overwrites files in the cache folder.  
  * Emits progress updates to the provided `rich.Progress` instance.  
  * Calls the LLM many times; each call may consume API credits and may raise network‑related exceptions (not caught inside `Manager`).  

---

<a name="usage-example"></a>
### Typical Usage  

```python
from manage import Manager
from rich.progress import Progress

ignore = ["*.pyc", "__pycache__", ".git", ".venv", ".auto_doc_cache"]
with Progress() as prog:
    mgr = Manager("/path/to/my/project", ignore, progress_bar=prog)
    mgr.generate_code_file()
    mgr.generate_global_info_file()
    mgr.generete_doc_parts()
    mgr.generate_intro()
```

After execution, open `<project>/.auto_doc_cache/output_doc.md` to view a fully linked, AI‑generated documentation of the whole code base.

---

<a name="extensibility"></a>
### Extensibility  

* **Custom chunk size** – modify `MAX_GLOBAL_SYMBOLS` or the local `MAX_SYMBOLS` constant in `generete_doc_parts`.  
* **Alternative storage** – replace `get_file_path` to point to a different directory (e.g., remote storage).  
* **Parallel generation** – because `write_docs_by_parts` is stateless aside from the optional overlap, you could parallelise the loop and later re‑assemble fragments, preserving order.  
* **Different LLM** – swap the underlying `GPTModel` implementation; the manager code stays unchanged because it only calls the high‑level helper functions.  

---  

**Bottom line** – `Manager` is the orchestrator that transforms a raw Python repository into a polished markdown document by stitching together the pre‑processor, the LLM wrapper, and the post‑processor, all while providing progress feedback and a cache of intermediate artefacts for debugging or incremental reruns.

## Code Documentation
### `CodeMix` Class

#### Description
The `CodeMix` class is responsible for traversing a directory tree, filtering out files and directories based on a list of ignore patterns, and generating a repository structure and content.

#### Methods

* `__init__(self, root_dir=".", ignore_patterns=None)`: Initializes the `CodeMix` object with a root directory and a list of ignore patterns.
* `should_ignore(self, path: str) -> bool`: Checks if a file or directory should be ignored based on the provided ignore patterns.
* `build_repo_content(self, output_file="repomix-output.txt")`: Generates the repository structure and content and writes it to an output file.

#### Attributes

* `root_dir`: The root directory of the repository.
* `ignore_patterns`: A list of patterns to ignore when traversing the directory tree.

### `compress` Function

#### Description
The `compress` function uses the `GPTModel` to compress a given data string.

#### Parameters

* `data: str`: The data to be compressed.
* `compress_power`: The compression power.

#### Returns
The compressed data string.

### `compress_and_compare` Function

#### Description
The `compress_and_compare` function compresses a list of data strings and compares them.

#### Parameters

* `data: list`: The list of data strings to be compressed.
* `compress_power: int = 4`: The compression power.
* `progress_bar: Progress = None`: The progress bar.

#### Returns
The list of compressed data strings.

### `async_compress` Function

#### Description
The `async_compress` function uses the `AsyncGPTModel` to asynchronously compress a given data string.

#### Parameters

* `data: str`: The data to be compressed.
* `compress_power`: The compression power.
* `semaphore`: The semaphore for asynchronous compression.

#### Returns
The compressed data string.

### `async_compress_and_compare` Function

#### Description
The `async_compress_and_compare` function asynchronously compresses a list of data strings and compares them.

#### Parameters

* `data: list`: The list of data strings to be compressed.
* `compress_power: int = 4`: The compression power.

#### Returns
The list of compressed data strings.

### `compress_to_one` Function

#### Description
The `compress_to_one` function compresses a list of data strings to a single string.

#### Parameters

* `data: list`: The list of data strings to be compressed.
* `compress_power: int = 4`: The compression power.
* `use_async: bool = False`: Whether to use asynchronous compression.
* `progress_bar: Progress = None`: The progress bar.

#### Returns
The compressed data string.

## Commit Message
```
Add CodeMix and compressor functions for repository structure and content generation

* Implemented CodeMix class for repository structure and content generation
* Added compress function for data compression using GPTModel
* Implemented compress_and_compare function for compressing and comparing data
* Added async_compress function for asynchronous data compression using AsyncGPTModel
* Implemented async_compress_and_compare function for asynchronous compressing and comparing data
* Added compress_to_one function for compressing data to a single string
```

<a name="postprocess"></a>
## 1. `preprocessor/postprocess.py`

This module gathers information from a generated Markdown document and uses the LLM to build a short intro and a table of contents.

| Function | Responsibility |
|----------|-----------------|
| `generate_markdown_anchor(header)` | Normalises a heading string into a Markdown anchor (`#anchor`). |
| `get_all_topics(data)` | Finds every `## …` heading, returns the raw titles and their Markdown anchors. |
| `get_all_html_links(data)` | Extracts custom `<a name="…">` anchors used in the repo‑dump. |
| `get_introdaction(links, global_data)` | Builds a two‑stage prompt: first, turns the list of anchors into a link list; second, writes a short introduction using the global summary. |

### 1.1 `generate_markdown_anchor`

```python
def generate_markdown_anchor(header: str) -> str
```

* Normalises to ASCII (`unicodedata.normalize('NFKC')`).  
* Lower‑cases, replaces spaces with hyphens, removes non‑alphanumerics, collapses multiple dashes, trims edges.  
* Returns a string prefixed with `#` so it can be used as a Markdown link target.

### 1.2 `get_all_topics`

* Scans the document for the pattern `"\n## "` to locate level‑2 headings.  
* For each heading extracts the title up to the next newline.  
* Returns two lists: `topics` (raw titles) and `links` (anchors via `generate_markdown_anchor`).

### 1.3 `get_all_html_links`

* Looks for `<a name=` tags.  
* Extracts the anchor value (text between `name="` and `</a>`).  
* Returns a list of all names – these are used to build the TOC.

### 1.4 `get_introdaction`

1. **Link list creation**  
   * Prompt the LLM with `BASE_INTRODACTION_CREATE_TEXT` (system) and the list of anchors (user).  
   * `GPTModel.get_answer_without_history` returns a Markdown list of links.

2. **Intro paragraph**  
   * Prompt with `BASE_INTRO_CREATE` and the `global_data` summary.  
   * Receive a concise introduction to the repo.

3. **Combine** – return `intro + "\n\n" + intro_links + "\n"`.

The function assumes `GPTModel()` is configured with a valid Groq API key and that the supplied `global_data` is a summary produced earlier by the compressor.

---

<a name="spliter"></a>
## 2. `preprocessor/spliter.py`

This module breaks a long string (the repository dump) into chunks that fit the LLM context window and then asks the model to produce a documentation fragment for each chunk.

### 2.1 `split_data`

```python
def split_data(data: str, max_symbols: int) -> list[str]
```

1. **Hard‑limit pass**  
   * Splits any fragment that is > 1.5 × `max_symbols` roughly in half until all fit.  
   * Uses `data.split("\n")` to start with a list of “lines”.

2. **Soft‑limit assembly**  
   * Greedily concatenates consecutive fragments as long as the combined length ≤ 1.25 × `max_symbols`.  
   * Returns a list of strings where each element is a chunk.

The function is deterministic but mutates the intermediate list. It is designed for a single‑threaded pipeline; no parallelism is involved.

### 2.2 `write_docs_by_parts`

```python
def write_docs_by_parts(part: str, global_info: str, prev_info: str | None = None) -> str
```

* Constructs a 3‑ or 4‑message prompt:
  * System: `BASE_PART_COMPLITE_TEXT` – “you are a documentation writer”.
  * System: `global_info` – compressed project overview.
  * Optional system: `it is last part …` + `prev_info` to maintain continuity.
  * User: the raw chunk `part`.

* Calls `GPTModel.get_answer_without_history` to get a Markdown fragment.  
* Strips surrounding triple‑backtick fences if they appear (common when the model returns a code block).

* Returns the clean fragment.

---

### Interaction with the rest of the pipeline

* `split_data` is invoked by the *Manager* when dividing `code_mix.txt` into ~5 k‑symbol pieces.  
* `write_docs_by_parts` is used to generate each fragment; the *Manager* passes the last 3 k‑symbol tail as `prev_info`.  
* After all fragments are produced, `postprocess.get_all_topics` and `get_all_html_links` parse `output_doc.md`, and `get_introdaction` writes the introductory paragraph and table of contents, which are then prepended to the final Markdown file.

These modules are the last step before the finished document is saved under `<repo>/.auto_doc_cache/output_doc.md`.

