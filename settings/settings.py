import json


with open('./settings/settings.json') as file:
    data = dict(json.load(file))

    API_ID: str = data['API_ID']
    API_HASH: str = data['API_HASH']
    TOKEN: str = data['TOKEN']

