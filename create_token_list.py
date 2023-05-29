from pathlib import Path
from requests import get
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from credentials import CMC_API_KEY




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
    tokens_file_path = Path('tokens.json')
    if tokens_file_path.exists():
        return

    token_list = create_token_list(request_tokens())
    with tokens_file_path.open('w') as write_file:
        json.dump(token_list, write_file)


if __name__ == '__main__':
    token_list_to_json()
