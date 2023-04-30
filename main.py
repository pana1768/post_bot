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

def get_users():
    connect = sqlite3.connect('rassilka.db')
    cursor = connect.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    return users

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id,'Напишите свое имя для регистрации')
    bot.register_next_step_handler(msg,get_name)

def get_name(msg):
    users = get_users()
    if msg.chat.id not in users:
        connect = sqlite3.connect('rassilka.db')
        cursor = connect.cursor()
        user_id = msg.chat.id
        name = msg.text
        cursor.execute('INSERT INTO users(user_id, name) VALUES (?, ?)', (user_id, name))
        connect.commit()
        bot.send_message(msg.chat.id, 'Отлично, вы зарегестрировались на курс!')
    else:
        bot.send_message(msg.chat.id, 'Вы уже зарегестрированы!')


@bot.message_handler(commands=['admin'])
def admin_panel(msg):
    if is_admin(msg):
        bot.send_message(msg.chat.id,'Вы в админ панеле')
        bot.register_next_step_handler(msg,msg_to_reply)
    else:
        bot.send_message(msg.chat.id, 'Простите, но вы не являетесь администратором данного телеграм бота')
def msg_to_reply(msg):
    users = get_users()
    for user in users:
        try:
            bot.send_message(user, msg.text)
            time.sleep(1)
        except Exception as e:
            print(f'Ошибка отправки сообщения пользователю {user[0]}: {str(e)}')

@bot.message_handler(commands=['new_post'])
def per(msg):
    bot.send_message(msg.chat.id, 'Что вы хотите запостить?')
    bot.register_next_step_handler(msg,new_post)
def new_post(msg):
    bot.send_message(chat_id=-1001954010898,text=msg.text)


if __name__ == "__main__":
    bot.polling(none_stop=True)