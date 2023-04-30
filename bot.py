import json
from telebot import TeleBot
import sqlite3
import time

with open('token.json','r') as d:
    data = json.load(d)

token = data['token']
bot = TeleBot(token)


admin_list = [934478159]
def is_admin(msg):
    return msg.chat.id in admin_list

@bot.message_handler(commands=['admin'])
def admin_panel(msg):
    if is_admin(msg):
        bot.send_message(msg.chat.id,'Вы в админ панеле')
    else:
        bot.send_message(msg.chat.id, 'Простите, но вы не являетесь администратором данного телеграм бота')

@bot.message_handler(commands=['new_post'])
def per(msg):
    bot.send_message(msg.chat.id, 'Что вы хотите запостить?')
    bot.register_next_step_handler(msg,new_post)
def new_post(msg):
    bot.send_message(chat_id=-1001954010898,text=msg.text)


if __name__ == "__main__":
    bot.polling(none_stop=True)