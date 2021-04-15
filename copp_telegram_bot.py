# -*- coding: utf-8 -*-
import telebot
from telebot import types  # кнопки
from string import Template

# Создаем бота
bot = telebot.TeleBot('1706799536:AAGsQL4vxc3hum-mqi37mgXn9iHxBoGCYBw')


#
# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Центр опережающей профессиональной подготовки Республики Бурятия приветствует вас!')

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/reg')
    itembtn3 = types.KeyboardButton('/reg2')
    markup.add(itembtn1, itembtn2, itembtn3)


# /about
@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, "Целью создания Центра опережающей профессиональной подготовки Республики Бурятия"
                                      " является формирование системы непрерывного опережающего профессионального обучения "
                                      "граждан и приобретение ими новых профессиональных навыков и компетенций, включая область цифровой экономики.")


bot.polling(none_stop=True, interval=0)
