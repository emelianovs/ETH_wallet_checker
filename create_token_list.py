from requests import get
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os

CMC_API_KEY = os.environ['API_CMC']


def request_tokens() -> dict:
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
      'start': 1,
      'limit': 5000,
      'sort': 'cmc_rank',
      'aux': 'platform,is_active'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }

    try:
        response = get(url, params=parameters, headers=headers)
        info = json.loads(response.content)
        return info
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def create_token_list(raw_data: dict) -> list:
    tokens_list = []
    for i in raw_data['data']:
        if i['platform'] and i['is_active'] == 1:
            if i['platform']['id'] == 1027:
                tokens_list.append({
                    'name': i['name'],
                    'ticker': i['symbol'],
                    'contract': i['platform']['token_address']})

    return tokens_list


def token_list_to_json():
    token_list = create_token_list(request_tokens())
    jsonized = json.dumps(token_list, indent=4)
    with open("tokens.json", "w") as write_file:
        json.dump(jsonized, write_file)


if __name__ == '__main__':
    token_list_to_json()
