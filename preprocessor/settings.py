from engine.config.config import BASE_SETTINGS_PROMPT

class ProjectSettings:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.info = {}

    def add_info(self, key, value):
        self.info[key] = value

    @property
    def prompt(self):
        result = ""
        result += BASE_SETTINGS_PROMPT
        result += f"Project Name: {self.project_name} \n"
        for key in self.info:
            result += f"{key}: {self.info[key]} \n"
        
        return result
    
