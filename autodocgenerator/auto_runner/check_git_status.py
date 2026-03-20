import subprocess
from autodocgenerator.engine.config.config import GITHUB_EVENT_NAME
from autodocgenerator.manage import Manager
from autodocgenerator.schema.cache_settings import CacheSettings, CheckGitStatusResultSchema
from autodocgenerator.preprocessor.checker import have_to_change


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
    
def get_detailed_diff_stats(target_hash):
    cmd = ['git', 'diff', target_hash, 'HEAD', '--numstat', '--', '.', ':(exclude)*.md']
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    files_info = []
    for line in result.stdout.strip().split('\n'):
        if not line: continue
        added, deleted, filepath = line.split('\t')
        
        added = int(added) if added != '-' else 0
        deleted = int(deleted) if deleted != '-' else 0
        
        if deleted == 0 and added > 0:
            status = "ADDED"
        elif added == 0 and deleted > 0:
            status = "DELETED"
        else:
            status = "MODIFIED"
            
        files_info.append({
            "path": filepath,
            "status": status,
            "added": added,
            "deleted": deleted,
            "total_changes": added + deleted
        })
    return files_info
    
def get_git_revision_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()

def check_git_status(manager: Manager) -> CheckGitStatusResultSchema:
    if GITHUB_EVENT_NAME == "workflow_dispatch" or manager.cache_settings.last_commit == "":
        manager.cache_settings.last_commit = get_git_revision_hash()
        return CheckGitStatusResultSchema(need_to_remake=True, remake_gl_file=True)

    changes = get_detailed_diff_stats(manager.cache_settings.last_commit)
    result = have_to_change(manager.llm_model, changes, manager.cache_settings.doc.global_info)
    
    return result

