#импорт библиотек
import time
import random
import sqlite3
import tempfile
import telebot
import requests
from inspect import getfile
from pathlib import Path
from cgitb import text
from tokenize import Token
from telebot import types
#токен
TOKEN = 'Ваш токен'
URL = 'https://api.telegram.org/bot'
bot = telebot.TeleBot(TOKEN)
#сохранение фото в БД 
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    photo_id = message.photo[-1].file_id
    photo_file = bot.get_file(photo_id)
    photo_bytes = (photo_file.file_path) 
    

    connect = sqlite3.connect('dz.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS dz_id(
            id INTEGER
    )""")    

    connect.commit()

    cursor.execute("INSERT INTO dz_id(id) VALUES(?)",[photo_id])
    bot.send_message(message.chat.id, "Фото сохранено")
    connect.commit()

#добавление пользователей в БД
@bot.message_handler(commands=['start'])
def start(message):
    

    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id TEXT
    )""")    

    connect.commit()

    people_id =  message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")   
    data = cursor.fetchone()            
    if data is None:
        users_list = [message.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", users_list)
        connect.commit()  
#кнопки комманды /start
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    item1 = types.KeyboardButton("Рандомное число 🎲")
    item2 = types.KeyboardButton("Отправить дз")
    item3 = types.KeyboardButton("Получить дз")
    item4 = types.KeyboardButton("Инфа🤖")
        
    markup.add(item1,item2, item3, item4)

    bot.send_message(message.chat.id, 'Интересненько, не правда ли, {0.first_name}?'.format(message.from_user), reply_markup=markup)
#функция кнопки рандом
@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Рандомное число 🎲':
            bot.send_message(message.chat.id, 'Ваше число:' + str(random.randint(0, 1000)))
#функция кнопки инфа
        elif message.text == 'Инфа🤖':
                markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
                item1 = types.KeyboardButton("О боте")
                item2 = types.KeyboardButton("Что в коробке?")
                back= types.KeyboardButton("Назад")
                markup.add(item1, item2, back)

                bot.send_message(message.chat.id, 'Инфа🤖', reply_markup=markup) 
#фцнкция кнопки о боте
        elif message.text == 'О боте':
                bot.send_message(message.chat.id, 'Бот создан для теста, осторожно теперь у вас вирус кстати)')

                
#функция конпки что в коробке
        elif message.text == 'Что в коробке?':
                bot.send_message(message.chat.id, 'Ничего, а ты что думал мы богатые чтобы что-то раздавать??')

#функция кнопки назад 
        elif message.text == 'Назад':
                markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
                item1 = types.KeyboardButton("Рандомное число 🎲")
                item2 = types.KeyboardButton("Отправить дз")
                item3 = types.KeyboardButton("Получить дз")
                item4 = types.KeyboardButton("Инфа🤖")

                markup.add(item1, item2, item3, item4)

                bot.send_message(message.chat.id, 'Назад', reply_markup=markup)
#функция кнопки стикер
        elif message.text == 'Стикер':
                stick = open('', 'rb')
                bot.send_sticker(message.chat.id, stick)

       #функция кнопки отправить дз
        elif message.text == 'Отправить дз':
             markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
             item1=types.KeyboardButton('Все дз(пока что только так)')
             back = types.KeyboardButton("Назад")
             markup.add(item1, back)

             bot.send_message(message.chat.id, 'Отправить дз', reply_markup=markup)

        elif message.text == 'Все дз(пока что только так)':
             bot.send_message(message.chat.id, 'Отправь фотографию готового д/з')   
             

        elif message.text == 'Получить дз':
             markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
             item1=types.KeyboardButton('Все дз, пока что только так(')
             back = types.KeyboardButton("Назад")
             markup.add(item1, back)
             connect = sqlite3.connect('dz.db')
             cursor = connect.cursor() 
             cursor.execute("""SELECT * FROM dz_id """)


bot.polling(none_stop=True)
