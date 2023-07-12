from http import HTTPStatus
from typing import Optional
from retry import retry
from credentials import WATCH_API_KEY, WD_CFG
import requests


class BaseWatchDataBlockchainService:
    def __init__(self, wd_cfg: dict):
        self._url = wd_cfg["url"]
        self._session = requests.Session()
        self._session.params = {"api_key": wd_cfg["api_key"]}

    @retry(tries=3)
    def _raw_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ):
        response = self._session.request(
            method, f"{self._url}/{endpoint}", params=params, json=json
        )
        if response.status_code == HTTPStatus.OK:
            return response.json()
        raise Exception(f"Unsuccessful external request: {response.text}")

    def last_block(self) -> int:
        response = self._raw_request("get", "watch_filters/lastBlockNumber")
        return response["block_number"]

    def add_filter(
        self, address: str, contract_address: Optional[str], with_approval: bool = False
    ) -> str:
        request_json = {
            "address": address,
            "contract_address": contract_address,
            "with_approval": with_approval,
        }
        response = self._raw_request("post", "watch_filters/add", json=request_json)
        print(response)
        return response["filter_id"]

    def check_filters(self, block_number: int):
        raw_response = self._raw_request(
            "post", "watch_filters/check", json={"block_number": block_number}
        )
        print(raw_response)
        return raw_response["filters"]

    def check_eth_balance(self, address: str):
        raw_response = self._raw_request(
            "post",
            f"node/jsonrpc?api_key={WATCH_API_KEY}",
            json={
                "jsonrpc": "2.0",
                "method": "eth_getBalance",
                "params": [address, "latest"],
                "id": 0,
            },
        )
        return raw_response

    def check_token_balance(self, address: str, token_list: list):
        raw_response = self._raw_request(
            "post",
            f"node/jsonrpc?api_key={WATCH_API_KEY}",
            json={
                "jsonrpc": "2.0",
                "method": "watch_getTokenBalances",
                "params": [address, [x["contract"] for x in token_list]],
                "id": 0,
            },
        )
        return raw_response


if __name__ == "__main__":
    wd = BaseWatchDataBlockchainService(WD_CFG)
    print(wd.check_eth_balance("0x1C727a55eA3c11B0ab7D3a361Fe0F3C47cE6de5d"))
