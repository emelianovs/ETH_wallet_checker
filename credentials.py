import os

WATCH_API_KEY = os.environ['API_WATCH_ETH']
WATCH_URL_ETH = f"https://ethereum.api.watchdata.io/node/jsonrpc?api_key={WATCH_API_KEY}"
CMC_API_KEY = os.environ['API_CMC']
WD_CFG = {'url': f'https://ethereum.api.watchdata.io', 'api_key': WATCH_API_KEY}
TG_BOT_API = os.environ['ETH_CHECKER_TGBOT_API']
    