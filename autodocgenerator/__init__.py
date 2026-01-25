print("ADG")
from .ui.logging import BaseLogger, BaseLoggerTemplate, InfoLog, ErrorLog, WarningLog

logger = BaseLogger()
logger.set_logger(BaseLoggerTemplate())