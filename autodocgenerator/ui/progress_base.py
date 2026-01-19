from rich.progress import Progress


class BaseProgress:
    def __init__(self):
        pass

    def create_new_subtask(self, name: str, total_len: int):
        ...

    def update_task(self):
        ...

    def remove_subtask(self):
        ...

class LibProgress(BaseProgress):
    
    def __init__(self, progress: Progress, total=4):
        super().__init__()
        self.progress = progress
        self._base_task = self.progress.add_task("General progress", total=total)
        self._cur_sub_task = None

    def create_new_subtask(self, name, total_len):
        self._cur_sub_task = self.progress.add_task(name, total=total_len)

    def update_task(self):
        if self._cur_sub_task is None:
            self.progress.update(self._base_task, advance=1)
        else:
            self.progress.update(self._cur_sub_task, advance=1)

    def remove_subtask(self):
        if self._cur_sub_task is not None:
            self._cur_sub_task = None
