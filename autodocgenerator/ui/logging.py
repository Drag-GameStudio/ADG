
class BaseLog:
    def __init__(self, message: str, level: int = 0):
        self.message = message
        self.level = level

    def format(self) -> str:
        return self.message
    
class ErrorLog(BaseLog):
    def format(self) -> str:
        return f"[ERROR] {self.message}"
    
class WarningLog(BaseLog):
    def format(self) -> str:
        return f"[WARNING] {self.message}"
    
class InfoLog(BaseLog):
    def format(self) -> str:
        return f"[INFO] {self.message}"


class BaseLoggerTemplate:
    def log(self, log: BaseLog):
        print(log.format())


class BaseLogger:
    MESSAGE_LEVELS = {
        0: "INFO",
        1: "WARNING",
        2: "ERROR"
    }

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BaseLogger, cls).__new__(cls)
        return cls.instance
    
    def set_logger(self, logger: BaseLoggerTemplate):
        self.logger_template = logger

    def log(self, log: BaseLog):
        self.logger_template.log(log)