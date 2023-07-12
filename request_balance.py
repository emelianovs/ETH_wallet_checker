import json
from logger import logger

from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from create_token_list import token_list_to_json
from credentials import WD_CFG
from wd_adapter import BaseWatchDataBlockchainService as WData


def address_eth_balance(connection: WData, address: str) -> str:
    try:
        logger.info(msg="Getting ETH balance...")
        request_address_balance = connection.check_eth_balance(address)

        balance_wei = request_address_balance.get("result")
        balance_eth = round(int(balance_wei, base=16) / 10**18, 8)

        return str(balance_eth)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def parse_dicts(list_of_dicts: list, address_check: str) -> str:
    for i in list_of_dicts:
        if i["contract"].lower() == address_check.lower():
            return i["ticker"]


def address_token_balance(connection: WData, address: str) -> list:
    token_balance_list = []
    with open("tokens.json") as jsonfile:
        loaded_json = json.load(jsonfile)
        token_details_list = json.loads(loaded_json)

    try:
        logger.info(msg="Getting token balance...")
        request_token_balance = connection.check_token_balance(
            address, token_details_list
        )

        tokens = request_token_balance.get("result")
        for token in tokens["tokenBalances"]:
            balance = round(int(token["tokenBalance"], base=16) / 10**18, 4)
            if balance > 0.0:
                ticker = parse_dicts(token_details_list, token["contractAddress"])
                token_balance_list.append([ticker, balance])

        return token_balance_list

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def runner(eth_address: str) -> list:
    logger.info(msg="Connecting to WatchData...")
    connection_watchdata = WData(WD_CFG)
    token_balances = str(address_token_balance(connection_watchdata, eth_address))
    address_info = [
        "Address: " + eth_address,
        "ETH balance: " + address_eth_balance(connection_watchdata, eth_address),
        "Token balances: " + token_balances,
    ]

    return address_info


if __name__ == "__main__":
    token_list_to_json()
    print(runner("0x1C727a55eA3c11B0ab7D3a361Fe0F3C47cE6de5d"))
