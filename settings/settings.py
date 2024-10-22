import json
from typing import Final


with open('./settings/settings.json') as file:
    data = dict(json.load(file))

    API_ID: str = data['API_ID']
    API_HASH: str = data['API_HASH']
    TOKEN: str = data['TOKEN']

"""Do not change these values!!!"""
MESSAGE_SYMBOLS_LIMIT: Final[int] = 2048
MAX_MESSAGES_PER_MINUTE: Final[int] = 20