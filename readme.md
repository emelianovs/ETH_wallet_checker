This simple tool lets you check balance of wallets on Ethereum mainnet network.
It shows ETH and token balances.
It uses Telegram bot as a convenient front-end.

The current version is 1.0 and project is currently under development.

To run this tool:
1) clone this repository
2) build docker image:
docker build -t {name} .
3) you will also need .env file with the following env vars:
API_WATCH_ETH - for the Watch Ethereum API key
API_CMC - for CoinMarketCap API key
ETH_CHECKER_TGBOT_API - for Telegram bot API key
4) run with the following command:
docker run --env-file .env {name}
