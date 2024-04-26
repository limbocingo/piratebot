from enum import Enum


class Color(Enum):
    """
    Colors used for makeing styled console logs.
    """

    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    DARK_GRAY = '\033[90m'
    BOLD_BLACK = '\033[1;30m'
    BOLD_RED = '\033[1;31m'
    BOLD_GREEN = '\033[1;32m'
    BOLD_YELLOW = '\033[1;33m'
    BOLD_BLUE = '\033[1;34m'
    BOLD_MAGENTA = '\033[1;35m'
    BOLD_CYAN = '\033[1;36m'
    BOLD_WHITE = '\033[1;37m'

class Log:
    """
    Send styled logs into the console.
    """

    def __init__(self, message) -> None:
        self.message = message

    def __prefix(self, value: str) -> str:
        return f'{Color.DARK_GRAY.value}[{value}{Color.DARK_GRAY.value}]{Color.RESET}'

    def information(self) -> None:
        """
        Information log.
        """

        print(
            self.__prefix(f'{Color.BOLD_BLUE}INFO'),
        )
