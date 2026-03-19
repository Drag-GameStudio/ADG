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
    if GITHUB_EVENT_NAME == "workflow_dispatch" or manager.cache_settings.last_commit == "":
        manager.cache_settings.last_commit = get_git_revision_hash()

        return True


    if len(get_diff_by_hash(manager.cache_settings.last_commit)) > manager.config.pbc.threshold_changes or manager.cache_settings.last_commit == "":
        manager.cache_settings.last_commit = get_git_revision_hash()
        return True
    
    return False
