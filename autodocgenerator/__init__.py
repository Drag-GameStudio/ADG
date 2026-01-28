def _print_welcome():
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    ascii_logo = f"""
    {BLUE}{BOLD}    ___     ____     ______
       /   |   / __ \   / ____/
      / /| |  / / / /  / / __  
     / ___ | / /_/ /  / /_/ /  
    /_/  |_|/_____/   \____/   
    {RESET}"""
    
    print(ascii_logo)
    print(f"{CYAN}ADG Library{RESET} | {BOLD}Status:{RESET} Ready to work")
    print(f"{'—' * 35}\n")

_print_welcome()


from .ui.logging import BaseLogger, BaseLoggerTemplate, InfoLog, ErrorLog, WarningLog

logger = BaseLogger()
logger.set_logger(BaseLoggerTemplate())