import os
import telebot
from telebot import types
import requests
import re


bot = telebot.TeleBot('7732064595:AAGdf5mnv1x2YfMNM89IWgfCw5TKNDsZ7z8')

# Используем словарь для хранения данных пользователя
user_data = {}

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Арабика')
    btn2 = types.KeyboardButton('Робуста')
    btn3 = types.KeyboardButton('Смесь')
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, добро пожаловать в BeanStream!!!\nДавайте оформим вашу подписку на кофе.")
    bot.send_message(message.chat.id, text="Выберите сорт кофе:", reply_markup=markup)
    
    # Инициализируем данные пользователя
    user_data[message.chat.id] = {
        'coffeeType': '',
        'coffeeFormat': '',
        'coffeeRate': '',
        'coffeeTime': '',
        'coffeeAddress': ''
    }

@bot.message_handler(func=lambda m: m.text in ["Арабика", "Робуста", "Смесь"])
def set_coffee_type(message):
    user_data[message.chat.id]['coffeeType'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('В зёрнах')
    btn2 = types.KeyboardButton('Молотый')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text='Выберите формат кофе:', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["В зёрнах", "Молотый"])
def set_coffee_format(message):
    user_data[message.chat.id]['coffeeFormat'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Еженедельный')
    btn2 = types.KeyboardButton('Ежемесячный')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text='Выберите тариф подписки:', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["Еженедельный", "Ежемесячный"])
def set_coffee_rate(message):
    user_data[message.chat.id]['coffeeRate'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('10:00')
    btn2 = types.KeyboardButton('12:00')
    btn3 = types.KeyboardButton('14:00')
    btn4 = types.KeyboardButton('16:00')
    btn5 = types.KeyboardButton('18:00')
    btn6 = types.KeyboardButton('20:00')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, text='Выберите время доставки:', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["10:00", "12:00", "14:00", "16:00", "18:00", "20:00"])
def process_time_input(message):
    user_data[message.chat.id]['coffeeTime'] = message.text
    # Убираем клавиатуру для удобства ввода адреса
    remove_markup = types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id, 
                         '📦 Теперь введите адрес доставки (улица, дом, квартира):\n\nПример: ул. Ленина, д. 10, кв. 25',
                         reply_markup=remove_markup)
    bot.register_next_step_handler(msg, process_address_input)

def process_address_input(message):
    address = message.text.strip()   
    user_data[message.chat.id]['coffeeAddress'] = address
    

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.reply_to(message, "Пожалуйста, используйте кнопки меню или введите команду /start")

bot.infinity_polling()