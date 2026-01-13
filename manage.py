from preprocessor.spliter import split_data, write_docs_by_parts
from preprocessor.compressor import compress_to_one
from preprocessor.postprocess import get_introdaction, get_all_html_links
import os
from preprocessor.code_mix import CodeMix
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn


class Manager:
    CACHE_FOLDER_NAME = ".auto_doc_cache"

    FILE_NAMES = {
        "code_mix": "code_mix.txt",
        "global_info": "global_info.md",
        "output_doc": "output_doc.md"
    }

    MAX_GLOBAL_SYMBOLS = 10000


    def __init__(self, project_directory: str, ignore_files: list = [], progress_bar: Progress = None):
        self.project_directory = project_directory
        self.ignore_files = ignore_files
        self.progress_bar = progress_bar

        cache_path = os.path.join(self.project_directory, self.CACHE_FOLDER_NAME)

        if not os.path.isdir(cache_path):
            os.mkdir(cache_path)

    def get_file_path(self, file_key: str):
        return os.path.join(self.project_directory, self.CACHE_FOLDER_NAME, self.FILE_NAMES.get(file_key))

    def generate_code_file(self):
        cm = CodeMix(self.project_directory, self.ignore_files)
        cm.build_repo_content(self.get_file_path("code_mix"))

    def generate_global_info_file(self):
        with open(self.get_file_path("code_mix"), "r", encoding="utf-8") as file:
            data = file.read()

        splited_data = split_data(data, self.MAX_GLOBAL_SYMBOLS)
        result = compress_to_one(splited_data, 2, progress_bar=self.progress_bar)
        with open(self.get_file_path("global_info"), "w", encoding="utf-8") as file:
            file.write(result)

    def generete_doc_parts(self):
        MAX_SYMBOLS = 5000
        with open(self.get_file_path("global_info"), "r", encoding="utf-8") as file:
            global_info = file.read()

        with open(self.get_file_path("code_mix"), "r", encoding="utf-8") as file:
            full_code_mix = file.read()

        splited_data = split_data(full_code_mix, MAX_SYMBOLS)
        result = None

        sub_task = self.progress_bar.add_task(f"[green]  generete doc parts", total=len(splited_data))

        for el in splited_data:
            result = write_docs_by_parts(el, global_info, result)
            with open(self.get_file_path("output_doc"), "a", encoding="utf-8") as file:
                file.write(result)
                file.write("\n\n")

            result = result[len(result) - 3000:]
            self.progress_bar.update(sub_task, advance=1)
        
        self.progress_bar.remove_task(sub_task)



    def generate_intro(self):
        with open(self.get_file_path("global_info"), "r", encoding="utf-8") as file:
            global_info = file.read()

        with open(self.get_file_path("output_doc"), "r", encoding="utf-8") as file:
            curr_doc = file.read()

        links = get_all_html_links(curr_doc)
        intro = get_introdaction(links, global_info)

        with open(self.get_file_path("output_doc"), "r", encoding="utf-8") as file:
            old_data = file.read()

        new_data = f"{intro} \n\n{old_data}"

        with open(self.get_file_path("output_doc"), "w", encoding="utf-8") as file:
            file.write(new_data)


if __name__ == "__main__":
    ignore_list = [
        "*.pyo", "*.pyd", "*.pdb", "*.pkl", "*.log", "*.sqlite3", "*.db",
        "venv", "env", ".venv", ".env", ".vscode", ".idea", "*.iml", ".gitignore", ".ruff_cache", ".auto_doc_cache",
        "*.pyc", "__pycache__", ".git", ".coverage", "htmlcov", "migrations", "*.md", "static", "staticfiles", ".mypy_cache"
    ]



    with Progress(
        SpinnerColumn(),            # Анимация загрузки
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),                # Сам прогресс-бар
        TaskProgressColumn(),       # Процент выполнения
    ) as progress:
        manager = Manager(r"C:\Users\huina\Python Projects\Impotant projects\AutoDocGenerateGimini", ignore_list, progress_bar=progress)

        chapters = ["generete code mix file ...", "generete global info file ...", "generete doc parts ...", "generete intro and links ..."]
        main_task = progress.add_task("[bold magenta]Общий прогресс", total=len(chapters))


        progress.console.print(f"[bold blue]Start: {chapters[0]}")
        manager.generate_code_file()
        progress.update(main_task, advance=1)


        progress.console.print(f"[bold blue]Start: {chapters[1]}")
        manager.generate_global_info_file()
        progress.update(main_task, advance=1)

        progress.console.print(f"[bold blue]Start: {chapters[2]}")
        manager.generete_doc_parts()
        progress.update(main_task, advance=1)
    

        progress.console.print(f"[bold blue]Start: {chapters[3]}")
        manager.generate_intro()
        progress.update(main_task, advance=1)
    


