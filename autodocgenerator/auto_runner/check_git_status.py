import subprocess
from autodocgenerator.engine.config.config import GITHUB_EVENT_NAME
from autodocgenerator.manage import Manager
from autodocgenerator.schema.cache_settings import CacheSettings


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
    
def get_git_revision_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()

def check_git_status(manager: Manager) -> bool:
    print("GIT EVENT:", GITHUB_EVENT_NAME)
    if GITHUB_EVENT_NAME == "workflow_dispatch":
        return True
    
    cache_settings = CacheSettings.model_validate_json(manager.read_file_by_file_key(".auto_doc_cache_file", is_outside=True))

    if len(get_diff_by_hash(cache_settings.last_commit)) > manager.config.pbc.threshold_changes or cache_settings.last_commit == "":
        cache_settings.last_commit = get_git_revision_hash()
        with open(manager.get_file_path(".auto_doc_cache_file", is_outside=True), "w", encoding="utf-8") as file:
            file.write(cache_settings.model_dump_json())
        return True
    
    

    return False
