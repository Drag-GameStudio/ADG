from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn


class BaseProgress:
    def __init__(self):
        pass

    def create_new_subtask(self, name: str, total_len: int):
        print("create sub task", name, total_len)

    def update_task(self):
        print("upd")

    def remove_subtask(self):
        print("rem")

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
