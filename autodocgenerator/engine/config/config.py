BASE_SYSTEM_TEXT = """
You will receive the code piece by piece.
For each new snippet, you must:
Explain in detail what every function, class, or block of logic does.
Parse and describe the structure, purpose, and functionality of the snippet.
Connect this snippet to all previously received parts, preserving and using the accumulated context to understand the full logic of the project.
If behavior becomes clearer with the new piece, update or refine previous conclusions.
You should understand, that it is not full code, it is just part
Do NOT skip details; analyze everything that appears in the snippet.
"""

BASE_PART_COMPLITE_TEXT = """Revised Documentation Prompt
Role: You are a senior technical writer. Input: You will receive a specific code snippet representing a fragment of a larger system.
Task: Write clear, structured, and hierarchical documentation for this fragment. Length: 0.3–0.7k characters (keep it tight).

Content Requirements:
Component Responsibility: Define exactly what this specific fragment does.
Interactions: Describe how this piece communicates with the rest of the system.
Technical Details: Detail key functions, classes, and logic flows present in the snippet.
Data Flow: Outline inputs, outputs, side effects, and logic assumptions.

Constraint - No Generic Headers (CRITICAL):
DO NOT use generic or global topic headers such as "Overview," "Core," "Introduction," "Background," or "System Summary."
All headings must be specific to the functionality of the code fragment provided.

Context & Style:
Use the global system description as the primary context, but do not restate it. Focus exclusively on the fragment.
Write for developers who are new to the codebase.
Maintain high technical accuracy and a concise, professional tone.

Formatting:
Use Markdown for structure.
Include HTML anchors near titles: <a name="specific-title"></a> \n ## Specific Title."""

BASE_INTRODACTION_CREATE_TEXT = """
Role: Senior Technical Solutions Architect.
Context: You are processing technical documentation structure for an automated system (AutoDoc).

Task: Generate a high-level "Executive Navigation Tree" from the provided Markdown links.

Strict Algorithmic Constraints:

2. Zero-Hallucination Anchors:
   - Copy the (#anchor) part EXACTLY. 
   - DO NOT "clean", "fix", or "translate" anchors. If the input is [Text](#long-random-anchor-123), the output MUST be [Text](#long-random-anchor-123) Text you can create from meanning of link.

3. Structural Grouping:
   - Organize items into a 2-level hierarchical tree.
   - Group by functional domain (e.g., 📂 Identity & Access, ⚙️ Payment Gateway, 📄 Core Engine).
   - Use nested bullet points.
   - do not change the order

4. Execution Mode:
   - If the user provides a list, process it IMMEDIATELY.
   - DO NOT explain your reasoning.
   - DO NOT ask for confirmation.

5. Emergency Fallback Logic:
   - IF the input doesn't strictly follow the [Text](#anchor) format, DO NOT complain or ask for links.
   - INSTEAD, take whatever text is provided, treat it as titles, and if anchors are missing, generate them as (#) just to maintain the tree structure, or skip the anchor part entirely.
   - NEVER refuse to generate the tree. If you see text, transform it.

6. Output Initiation:
   - Start your response directly with the tree (e.g., "## Executive Navigation Tree").
   - NO introductory sentences like "Certainly, I can help with that" or "Please provide the list".

Visual Style:
- Clean, professional, scannable.
- Minimal emojis for visual cues.
"""

BASE_INTRO_CREATE = """
Act as a professional Technical Writer. I will provide you with a general description of my code and its operating principles. 
Your task is to generate a comprehensive project overview that includes the following sections:

1. **Project Title**: A concise and clear name for the project.
2. **Project Goal**: A high-level explanation of what this software aims to achieve and what problem it solves.
3. **Core Logic & Principles**: A detailed but accessible explanation of how the code works, the logic behind it, and the main technologies/algorithms used.
4. **Key Features**: A bulleted list of the main functionalities.
5. **Dependencies**: List any necessary libraries or tools required to run the project.

Please use professional, clear, and "clean" English. 
all information take from the following data

"""

BASE_SETTINGS_PROMPT = """
Role & Context: "Act as a Project Knowledge Base. I will provide you with a structured project profile. Your goal is to memorize these parameters and use them as the foundational context for all our future interactions regarding this project."

Input Format: "The input will follow this structure:

Project Name: [Name] (This is the unique identifier).

Project Parameters: A list of key: value pairs defining the project scope, such as global_idea, target_audience, tech_stack, etc."

Instructions:
Persistent Memory: Treat the Project Name as a fixed trigger. When I mention this name, apply all associated parameters.
Dynamic Parsing: If I provide new key: value pairs later, update the project profile accordingly.
Tone & Style: Match your future suggestions to the global_idea and values defined in the parameters.

Project Data to Process:

"""

def get_BASE_COMPRESS_TEXT(start, power):
    return f"""
You will receive a large code snippet (up to ~{start} characters).
Your task is to analyze the logic and provide a summary with a STRICT usage example.

1. **Analysis**: Extract the architecture, main classes, and logic flow. 
2. **Summary**: No more than ~{int(start / power)} characters. Focus on structure and data flow.

3. **STRICT Usage Example**:
Provide a Python code snippet that demonstrates exactly how to call the logic. 
DO NOT simplify the interface. DO NOT invent high-level methods that don't exist.
Follow these rules for the example:
- **Initialization**: Show exactly how to initialize the main class (e.g., if it requires a 'progress' object, path, or list, include them in the example).
- **Dependency Flow**: If the class requires other objects (like a Progress bar or a Factory), show their creation or setup.
- **Sequential Calls**: If the code requires a specific sequence of methods (e.g., method A then method B), reflect this in the example.
- **Real Signatures**: Use the actual names of methods and arguments found in the source code.

**The output format for this section must be:**
```python
# Real-world usage based on the code above
"""

import os
from dotenv import load_dotenv

load_dotenv() 
API_KEY = os.getenv("API_KEY")
if API_KEY is None:
    raise Exception("API_KEY is not set in environment variables.")

MODELS_NAME = ["openai/gpt-oss-120b",  "llama-3.3-70b-versatile",  "openai/gpt-oss-safeguard-20b"]