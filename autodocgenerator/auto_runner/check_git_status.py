import subprocess
from autodocgenerator.engine.config.config import GITHUB_EVENT_NAME


def get_diff_by_hash(target_hash):
    try:
        result = subprocess.run(
            ['git', 'diff', target_hash, 'HEAD', ':(exclude)*.md'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении git diff: {e}")
        return None

def check_git_status(max_threshold: int, manager) -> bool:
    print("GIT EVENT:", GITHUB_EVENT_NAME)
    return True
# print(len(get_diff_by_hash("fa1d73b1a2fd5a78d45db41e1c376148d9d893c4")))
