import os
import telebot
from telebot import types
import requests
import re


bot = telebot.TeleBot('7732064595:AAGdf5mnv1x2YfMNM89IWgfCw5TKNDsZ7z8')

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
        'coffeeAddress': '',
        'coffeeCost': 0,
        'awaiting_address': False
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
    btn1 = types.KeyboardButton('Еженедельный - 800 руб.')
    btn2 = types.KeyboardButton('Ежемесячный - 2700 руб.')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text='Выберите тариф подписки:', reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["Еженедельный - 800 руб.", "Ежемесячный - 2700 руб."])
def set_coffee_rate(message):
    if '800' in message.text: user_data[message.chat.id]['coffeeCost'] = 800
    else: user_data[message.chat.id]['coffeeCost'] = 2700
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
def ask_for_address(message):
    chat_id = message.chat.id
    user_data[chat_id]['coffeeTime'] = message.text
    user_data[chat_id]['awaiting_address'] = True
    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, '📍 Пожалуйста, введите адрес доставки в формате "/[адрес доставки]":', reply_markup=remove_markup)


@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id in user_data and user_data[chat_id].get('awaiting_address'):
        user_data[chat_id]['coffeeAddress'] = text.replace('/','',1)
        user_data[chat_id]['awaiting_address'] = False

        summary = f"""☕️ Ваш заказ:
• Сорт: <b>{user_data[chat_id]['coffeeType']}</b>
• Формат: <b>{user_data[chat_id]['coffeeFormat']}</b>
• Тариф: <b>{user_data[chat_id]['coffeeRate']}</b>
• Время доставки: <b>{user_data[chat_id]['coffeeTime']}</b>
• Адрес: <b>{user_data[chat_id]['coffeeAddress']}</b>"""

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Подтвердить", "Изменить адрес")
        bot.send_message(chat_id, summary, reply_markup=markup, parse_mode="HTML")
        return

    if text == "Подтвердить":
        bot.send_message(chat_id, f"✅ Ваш заказ принят! Спасибо за подписку на BeanStream ☕️ \n💳К оплате: <b>{user_data[message.chat.id]['coffeeCost']}</b>₽\nПерейдите по ссылке для оплаты:\nhttps://sbp.nspk.ru/", reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    elif text == "Изменить адрес":
        user_data[chat_id]['awaiting_address'] = True
        bot.send_message(chat_id, '📍 Пожалуйста, введите адрес доставки в формате "/[адрес доставки]')
    else:
        bot.reply_to(message, "Пожалуйста, используйте кнопки или начните с /start")
    
bot.infinity_polling()