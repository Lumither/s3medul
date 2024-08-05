class Ansi:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    def disable(self) -> None:
        self.HEADER = ''
        self.BLUE = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.BOLD = ''
        self.UNDERLINE = ''
        self.END = ''

    @staticmethod
    def blend(color: str, text: str) -> str:
        """
        blend text with ansi color.

        example: Ansi.blend(Ansi.GREEN, 'Hello World!')
        :param color: Ansi color, see implementation for more details
        :param text: text need to be colored
        :return: string with ansi information
        """
        return Ansi.list_blend([color], text)

    @staticmethod
    def list_blend(color: list[str], text: str) -> str:
        """
        blend text with a list of ansi colors.

        example: Ansi.list_blend([Ansi.GREEN, Ansi.UNDERLINE], 'Hello World!')
        :param color: Ansi color, see implementation for more details
        :param text: text need to be colored
        :return: string with ansi information
        """
        return f"{''.join(color)}{text}{Ansi.END}"
