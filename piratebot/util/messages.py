import json


class Messages:
    """
    Obtain any content from the messages
    JSON file.
    """

    # File where the messages for the bot are located.
    MESSAGES_FILE = 'resources/messages.json'

    def __init__(self, path: list[str]) -> None:
        self.path = path

    def get_string(self, format: dict = {}):
        """
        Get a string.
        ```
            > get_message(format={product: Product, interaction: interaction,...})
        ```
        """

        with open(self.MESSAGES_FILE, encoding='utf8', mode='r') as fr:
            messages = json.load(fr)

        path_transformed = ''
        for name in self.path:
            path_transformed += f'["{name}"]'

        content = eval('messages' + path_transformed)
        if isinstance(content, dict):
            return None

        message = ''
        for line in content:
            message += line + '\n'

        return message.format(**format) if format else message

    def get_content(self):
        """
        Get any content you want from the
        messages file.
        """
        with open(self.MESSAGES_FILE, encoding='utf8', mode='r') as fr:
            messages = json.load(fr)

        path_transformed = ''
        for name in self.path:
            path_transformed += f'["{name}"]'

        content = eval('messages' + path_transformed)
        if isinstance(content, dict):
            return None

        return content
