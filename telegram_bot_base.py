import re
import telebot
from credentials import TG_BOT_API
from request_balance import runner

bot = telebot.TeleBot(TG_BOT_API)


@bot.message_handler(commands=['start', 'hi', 'hello'])
def start_message(message):
    bot.reply_to(message, 'Hi. Here you can check ETH and token balances of an address on Ethereum network. Please '
                          'send a valid address.')


@bot.message_handler()
def address_validity_check(message):
    pattern = re.compile(r"0x[A-Fa-f0-9]{40}")
    msg_text = message.text
    if pattern.match(msg_text):
        balance = runner(msg_text)
        bot.reply_to(message, balance[1])
        bot.reply_to(message, balance[2])
    else:
        bot.reply_to(message, 'Please enter a valid Ethereum network address')


if __name__ == '__main__':
    bot.infinity_polling()
