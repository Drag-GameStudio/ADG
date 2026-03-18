import os
from pathlib import Path
import fnmatch
from ..ui.logging import InfoLog, BaseLogger

class CodeMix:
    def __init__(self, root_dir=".", ignore_patterns=None):
        self.root_dir = Path(root_dir).resolve()
        self.ignore_patterns = ignore_patterns or []
        self.logger = BaseLogger()

    def should_ignore(self, path: str) -> bool:
        relative_path = path.relative_to(self.root_dir) # type: ignore
        path_str = str(relative_path)
        
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(path_str, pattern) or \
               fnmatch.fnmatch(os.path.basename(path_str), pattern) or \
               any(fnmatch.fnmatch(p, pattern) for p in path.parts): # type: ignore
                return True
        return False

    def build_repo_content(self):
        content = []
        content.append("Repository Structure:")
        
        for path in sorted(self.root_dir.rglob("*")):
            if self.should_ignore(path):
                self.logger.log(InfoLog(f"Ignored: {path}", level=1))
                continue
            
            depth = len(path.relative_to(self.root_dir).parts)
            indent = "  " * (depth - 1)
            name = f"{path.name}/" if path.is_dir() else path.name
            content.append(f"{indent}{name}")
        
        content.append("\n" + "="*20 + "\n")

        for path in sorted(self.root_dir.rglob("*")):
            if path.is_file() and not self.should_ignore(path):
                try:
                    relative_path = path.relative_to(self.root_dir)
                    content.append(f'<file path="{relative_path}">')
                    content.append(path.read_text(encoding="utf-8", errors="ignore"))
                    content.append("</file>\n")
                except Exception as e:
                    content.append(f"Error reading {path}: {e}")

        return "\n".join(content)

ignore_list = [
    "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db",
    "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore", ".ruff_cache",
    "*.pyc", "__pycache__", ".git", ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles", ".mypy_cache"
]


if __name__ == "__main__":
    packer = CodeMix(root_dir=r"C:\Users\huina\Python Projects\Kwork\ClickerProject\ClickerApp", ignore_patterns=ignore_list)
    # packer.build_repo_content("codemix.txt")
    print("Файл успешно создан!")
