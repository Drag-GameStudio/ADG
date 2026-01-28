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


class ConsoleTask:
    def __init__(self, name, total_len):
        self.name = name
        self.total_len = total_len
        self.start_task()

    def start_task(self):
        self.current_len = 0
        print(f"Starting task: {self.name} with total length {self.total_len}")

    def progress(self):
        self.current_len += 1
        percent = (self.current_len / self.total_len) * 100
        print(f"Task: {self.name} Progress: {percent:.1f}%")

    

class ConsoleGtiHubProgress(BaseProgress):
    def __init__(self):
        super().__init__()
        self.curr_task = None
        self.gen_task = ConsoleTask("General Progress", 4)

    def create_new_subtask(self, name: str, total_len: int):
        self.curr_task = ConsoleTask(name, total_len)

    def update_task(self):
        if self.curr_task is not None:
            self.curr_task.progress()
        else:
            self.gen_task.progress()


    def remove_subtask(self):
        self.curr_task = None