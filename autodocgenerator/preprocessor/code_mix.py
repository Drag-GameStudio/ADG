import os
from pathlib import Path
import fnmatch

class CodeMix:
    def __init__(self, root_dir=".", ignore_patterns=None):
        self.root_dir = Path(root_dir).resolve()
        self.ignore_patterns = ignore_patterns or []

    def should_ignore(self, path: str) -> bool:
        relative_path = path.relative_to(self.root_dir)
        path_str = str(relative_path)
        
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(path_str, pattern) or \
               fnmatch.fnmatch(os.path.basename(path_str), pattern) or \
               any(fnmatch.fnmatch(p, pattern) for p in path.parts):
                return True
        return False

    def build_repo_content(self, output_file="repomix-output.txt"):
        with open(output_file, "w", encoding="utf-8") as out:
            out.write("Repository Structure:\n")
            for path in sorted(self.root_dir.rglob("*")):
                if self.should_ignore(path):
                    continue
                depth = len(path.relative_to(self.root_dir).parts)
                indent = "  " * (depth - 1)
                out.write(f"{indent}{path.name}/\n" if path.is_dir() else f"{indent}{path.name}\n")
            
            out.write("\n" + "="*20 + "\n\n")

            for path in sorted(self.root_dir.rglob("*")):
                if path.is_file() and not self.should_ignore(path):
                    try:
                        relative_path = path.relative_to(self.root_dir)
                        out.write(f'<file path="{relative_path}">\n')
                        out.write(path.read_text(encoding="utf-8", errors="ignore"))
                        out.write(f"\n</file>\n\n")
                    except Exception as e:
                        out.write(f"Error reading {path}: {e}\n")

ignore_list = [
    "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db",
    "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore", ".ruff_cache",
    "*.pyc", "__pycache__", ".git", ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles", ".mypy_cache"
]


if __name__ == "__main__":
    packer = CodeMix(root_dir=r"C:\Users\huina\Python Projects\Kwork\ClickerProject\ClickerApp", ignore_patterns=ignore_list)
    packer.build_repo_content("codemix.txt")
    print("Файл успешно создан!")
