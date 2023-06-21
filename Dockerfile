FROM python:3.9.17-alpine
WORKDIR /eth_wallet_checker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENTRYPOINT python3 telegram_bot_base.py
