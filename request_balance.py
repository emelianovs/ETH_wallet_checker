import json
from requests import post
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from create_token_list import token_list_to_json
from credentials import WATCH_URL_ETH

ETH_ADDRESS = '0x1C727a55eA3c11B0ab7D3a361Fe0F3C47cE6de5d'


def address_eth_balance(url: str, address: str) -> str:
    try:
        request_address_balance = post(url, json={
            "jsonrpc": "2.0",
            "method": "eth_getBalance",
            "params": [address, "latest"],
            "id": 0
        })

        balance_wei = request_address_balance.json().get('result')
        balance_eth = round(int(balance_wei, base=16) / 10 ** 18, 8)

        return str(balance_eth)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def parse_dicts(list_of_dicts: list, address_check: str) -> str:
    for i in list_of_dicts:
        if i['contract'].lower() == address_check.lower():
            return i['ticker']


def address_token_balance(url: str, address: str) -> list:
    token_balance_list = []
    with open('tokens.json') as jsonfile:
        loaded_json = json.load(jsonfile)
        token_details_list = json.loads(loaded_json)

    try:
        request_token_balance = post(url, json={
            'jsonrpc': '2.0',
            'method': 'watch_getTokenBalances',
            'params': [address, [x['contract'] for x in token_details_list]],
            'id': 0
        })
        tokens = request_token_balance.json().get('result')
        for token in tokens['tokenBalances']:
            balance = round(int(token['tokenBalance'], base=16) / 10 ** 18, 4)
            if balance > 0.0:
                ticker = parse_dicts(token_details_list, token['contractAddress'])
                token_balance_list.append([ticker, balance])

        return token_balance_list

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def runner(api_link: str, eth_address: str) -> list:
    token_balances = str(address_token_balance(api_link, eth_address))

    address_info = ['Address: ' + eth_address,
                    'ETH balance: ' + address_eth_balance(api_link, eth_address),
                    'Token balances: ' + token_balances]

    return address_info


if __name__ == '__main__':
    token_list_to_json()
    print(runner(WATCH_URL_ETH, ETH_ADDRESS))
