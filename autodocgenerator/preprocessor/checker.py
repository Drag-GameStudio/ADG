from ..engine.models.model import ParentModel, Model
from ..engine.config.config import BASE_CHANGES_CHECK_PROMPT
from ..schema.cache_settings import CheckGitStatusResultSchema


def parse_answer(answer: str) -> CheckGitStatusResultSchema:
    splited = answer.split("|")
    change_doc = splited[0] == "true"
    change_global = splited[1] == "true"

    return CheckGitStatusResultSchema(need_to_remake=change_doc, remake_gl_file=change_global)

def have_to_change(model: Model, diff: list[dict[str, str|int|object]], global_info: str | None = None) -> CheckGitStatusResultSchema:
    prompt: list[dict[str, str]] = [
        {
            "role": "system",
            "content": BASE_CHANGES_CHECK_PROMPT
        },
        {
            "role": "system",
            "content": f"Global Info: {global_info}"
        },
        {
            "role": "user",
            "content": f"Changes: {str(diff)}"
        }
    ]

    answer = model.get_answer_without_history(prompt)

    return parse_answer(answer)