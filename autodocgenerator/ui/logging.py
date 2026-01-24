import time
from datetime import datetime



class BaseLog:
    def __init__(self, message: str, level: int = 0):
        self.message = message
        self.level = level

    def format(self) -> str:
        return self.message
    
    @property
    def _log_prefix(self):
        return f"[{datetime.fromtimestamp(time.time())}]"
    
    
    
class ErrorLog(BaseLog):
    def format(self) -> str:
        return f"{self._log_prefix} [ERROR] {self.message}"
    
class WarningLog(BaseLog):
    def format(self) -> str:
        return f"{self._log_prefix} [WARNING] {self.message}"
    
class InfoLog(BaseLog):
    def format(self) -> str:
        return f"{self._log_prefix} [INFO] {self.message}"


class BaseLoggerTemplate:
    def __init__(self, log_level: int = -1):
        self.log_level = log_level

    def log(self, log: BaseLog):
        print(log.format())

    def global_log(self, log: BaseLog):
        if self.log_level < 0 or self.log_level >= log.level:
            self.log(log)
        

class FileLoggerTemplate(BaseLoggerTemplate):
    def __init__(self, file_path: str, log_level: int = -1):
        super().__init__(log_level)
        self.file_path = file_path

    def log(self, log: BaseLog):
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(log.format() + "\n")


class BaseLogger:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BaseLogger, cls).__new__(cls)
        return cls.instance
    
    def set_logger(self, logger: BaseLoggerTemplate):
        self.logger_template = logger

    def log(self, log: BaseLog):
        self.logger_template.global_log(log)