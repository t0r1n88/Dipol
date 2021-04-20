# -*- coding: utf-8 -*-
import datetime
import telebot
from telebot import types  # кнопки
# sql
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='claudia!',
    port='3306',
    database='telegramdatabase'
)
# Создаем базу данных
mycursor = mydb.cursor()
# Создаем базу данных
#mycursor.execute('CREATE DATABASE telegramdatabase')

# Создаем поля в таблице

# mycursor.execute('CREATE TABLE users (first_name VARCHAR(255), last_name VARCHAR(255), patronymic VARCHAR(255))')

# Добавляем айди таблицы и айди телеграмм юзера
# к слову айди телеграм юзера не стоит делать уникальным, поскольку человек может записываться на несколько курсов
#mycursor.execute('ALTER TABLE users ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY, telegram_id INT )')
# Вставляем колонку для даты
mycursor.execute('ALTER TABLE users ADD COLUMN (request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')



bot = telebot.TeleBot('1706799536:AAGsQL4vxc3hum-mqi37mgXn9iHxBoGCYBw')

# Словарь где будут хранится данные пользователей
user_data = {}


# Класс пользователя
class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.last_name = ''
        self.patronymic = ''
        self.request_time = None
        self.phone = 0
        self.email = ''


# Приветствие
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     'Вас приветствует Центр опережающей профессиональной подготовки Республики Бурятия')
    # Получаем имя пользователя

    msg = bot.send_message(message.chat.id, 'Введите свое имя')
    bot.register_next_step_handler(msg, process_firstname_step)


def process_firstname_step(message):
    """
    Функция для обработки имени пользователя
    """
    # получаем id пользователя
    try:
        user_id = message.from_user.id
        # Добавляем данные в словарь. Создаем объект пользователя
        user_data[user_id] = User(message.text)
        msg = bot.send_message(message.chat.id, 'Введите свою фамилию')
        bot.register_next_step_handler(msg, process_lasttname_step)
    except Exception as e:
        bot.reply_to(message, 'Проверьте написание')


def process_lasttname_step(message):
    """
    Функция для обработки фамилии пользователя
    """
    try:
        user_id = message.from_user.id
        # Указываем атрибут lastname экземпляра класса, который хранится в user data
        user = user_data[user_id]
        user.last_name = message.text
        msg = bot.send_message(message.chat.id, 'Введите свое отчество')
        bot.register_next_step_handler(msg, process_patronymic_step)
    except Exception as e:
        bot.reply_to(message, 'Проверьте написание')


def process_patronymic_step(message):
    """
    Функция для обработки отчества пользователя
    """
    try:
        user_id = message.from_user.id
        # Добавляем данные в словарь. Создаем объект пользователя
        user = user_data[user_id]
        user.patronymic = message.text
        # Создаем sql запрос
        sql = 'INSERT INTO users (first_name, last_name, patronymic,telegram_id) VALUES (%s,%s,%s,%s)'
        # Указываем какие данные использовать
        val = (user.first_name, user.last_name, user.patronymic ,user_id)
        # Осуществляем запрос
        mycursor.execute(sql,val)
        # Вносим изменения в базу данных
        mydb.commit()
        bot.send_message(message.chat.id,
                         f'{user.last_name} {user.first_name} {user.patronymic} \n Центр опережающей профессиональной подготовки Республики Бурятия приветствует вас!!!\n'
                         f'Вы можете узнать актуальные курсы и записаться на них\n'
                         f'Получить справочную информацию  о ЦОПП и его возможностях')
    except Exception as e:
        bot.reply_to(message, 'Проверьте написание')


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
