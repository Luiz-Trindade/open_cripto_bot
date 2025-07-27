import os
import telebot
from agent import *
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("ACCESS_TOKEN"))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Use /ajuda para ver os comandos disponíveis.")

@bot.message_handler(commands=['bitcoin'])
def send_bitcoin_price(message):
    resposta = agent_analysis()
    bot.send_message(message.chat.id, resposta)

@bot.message_handler(commands=['ajuda', 'help'])
def send_help(message):
    comandos = """
📋 *Comandos disponíveis:*

/start - Mensagem de boas-vindas
/bitcoin - Exibe preço atual do Bitcoin (valor fictício)
/ajuda - Mostra essa lista de comandos
"""
    bot.send_message(message.chat.id, comandos, parse_mode='Markdown')

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)

print("🤖 Bot está rodando... Pressione Ctrl+C para parar.")

bot.polling()
