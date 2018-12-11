# Token 695230871:AAEllCSIVMCT8kwYC0LPxRdsEm80Pe7qvRY

from dbt import Database

import requests

import telebot
from telebot import apihelper
from telebot import types

import pprint

import copy

TOKEN = '695230871:AAEllCSIVMCT8kwYC0LPxRdsEm80Pe7qvRY'

apihelper.proxy = {'https': 'socks5://127.0.0.1:9150'}

#Создаем объект для доступа к базе данных

db = Database('test_database')

#Создаем разметку клавиатуры для выбора одного жанра

#Получаем список жанров из базы данных
genres = db.get_genres()

#Создаем объект клавиатуры
genre_keyboard = types.InlineKeyboardMarkup(row_width = 1)
for genre in genres:
    button = types.InlineKeyboardButton(text = genre, callback_data = genre)
    genre_keyboard.add(button)

#Функция для создания клавиатуры для прослушивания песни и выбора новой
def make_listen_or_choice_keyboard(url):
    listen_or_choice_keyboard = types.InlineKeyboardMarkup(row_width = 1)
    listen_button = types.InlineKeyboardButton(text = 'Listen track!', url = url)
    new_button = types.InlineKeyboardButton(text = 'New track', callback_data = 'new_track')
    listen_or_choice_keyboard.add(listen_button, new_button)
    return(listen_or_choice_keyboard)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    chat_id = message.chat.id
    db.add_chat(chat_id)
    bot.reply_to(message, 'Pssss, man, do you want some music?', reply_markup = genre_keyboard)

@bot.callback_query_handler(func=lambda call: call.data in genres)
def genre_choice(call):
    if call.message:
        if call.data:
            genre = call.data
            chat_id = call.message.chat.id
            link = db.get_random_from_genre(genre, chat_id)
            message_id = call.message.message_id
            if link:
                listen_or_choice_keyboard = make_listen_or_choice_keyboard(link)
                bot.send_message(chat_id, 'Enjoy!', reply_markup = listen_or_choice_keyboard)
                db.add_listened(chat_id, link)
            else:
                bot.send_message(chat_id, 'you have listened all, try new genre!', reply_markup = genre_keyboard)

@bot.callback_query_handler(func = lambda call: call.data == 'new_track')
def new_genre_choice(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, 'Choose genre!', reply_markup = genre_keyboard)

if __name__ == '__main__':
    bot.polling()




