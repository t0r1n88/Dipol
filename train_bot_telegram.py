# -*- coding: utf-8 -*-
import datetime
import telebot
from telebot import types  # кнопки
# sql
import mysql.connector


def preparation_fio(msg: str):
    """
    Функция для обработки сообщения с фио
    :param msg: Строка с фио
    :return: 3 объекта строки. Вместо недостающих элементов вставляются пустые строки
    В случае если получается больше 3 элементов, то пользователя будут просить изменить написание. Также есть проверка на цифры
    """
    fio_lst = msg.split()
    length_fio_lst = len(fio_lst)
    if length_fio_lst == 3:
        return fio_lst
    elif length_fio_lst == 2:
        fio_lst.append('')
        return fio_lst
    elif length_fio_lst == 1:
        fio_lst.extend(['', ''])
        return fio_lst
    else:
        return None

def preparation_phone(msg: str):
    """
    Функция для обработки телефонных номеров
    :param msg: строка с номером телефона
    :return: Возвращает номер телефона в формате числа
    """
    # Да много условий, но так сделано чтобы код был читаемым даже для новичков да и самому чтобы легче потом было
    # Проверяем является ли msg числом состоящим из десятичных символов т.е 0-9
    if msg.isdecimal():
        # Проверяем длину строки. Номер мобильного должен состоять из 11. Короткие номера обрабатывать смысла нет.
        if len(msg) != 11:
            return None
        # Проверяем чтобы номер был из России
        if msg[0] != '7':
            return None
        # Проверяем на платные номера
        # Ориентировался на статью https://pikabu.ru/story/platnyie_nomera_besplatnyie_nomera_i_nomera_s_povyishennoy_tarifikatsiey_chast_1_4389080
        pay_number = ('7809', '7803')
        # Спутниковые номера и первые 6 цифр Абхазии и ЮО
        six_number = ('795410', '792980', '792981')
        # Номера Абхазии и Южной Осетии первые 5 цифр
        five_number = ('79409', '79407')
        if (msg[:4] in pay_number) or (msg[:6] in six_number) or (msg[:5] in five_number):
            return None
        # Если все проверки пройдены успешно то возвращаем номер телефона в формате числа
        return int(msg)

def preparation_email(msg:str):
    """
    Функция для обработки email
    :param msg: строка с email
    :return: Строку если email признан корректным, None если нет
    """
    pass

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
# mycursor.execute('CREATE DATABASE telegramdatabase')

# Создаем поля в таблице

# mycursor.execute('CREATE TABLE users (first_name VARCHAR(255), last_name VARCHAR(255), patronymic VARCHAR(255))')

# Добавляем айди таблицы и айди телеграмм юзера
# к слову айди телеграм юзера не стоит делать уникальным, поскольку человек может записываться на несколько курсов
# mycursor.execute('ALTER TABLE users ADD COLUMN (id INT AUTO_INCREMENT PRIMARY KEY, telegram_id INT )')
# Вставляем колонку для даты
# mycursor.execute('ALTER TABLE users ADD COLUMN (request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')


bot = telebot.TeleBot('1706799536:AAGsQL4vxc3hum-mqi37mgXn9iHxBoGCYBw')

# Словарь где будут хранится данные пользователей
user_data = {}


# Класс пользователя
class User:
    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.patronymic = ''
        self.request_time = None
        self.phone = 0
        self.email = ''


# Приветствие
@bot.message_handler(commands=['start'], content_types=['text'])
def send_welcome(message):
    # Создаем клавиатуру Reply
    markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_about = types.KeyboardButton('О ЦОПП')
    item_reg = types.KeyboardButton('Записаться на курс')
    item_active_courses = types.KeyboardButton('Актуальные курсы')
    item_all_courses = types.KeyboardButton('Все курсы')
    markup_start.add(item_active_courses, item_all_courses, item_reg, item_about)
    # Оптравляем сообщение
    msg = bot.send_message(message.chat.id,
                           'Вас приветствует Центр опережающей профессиональной подготовки Республики Бурятия',
                           reply_markup=markup_start)
    bot.register_next_step_handler(msg, selector_func)
    # Получаем ФИО пользователя

    # msg = bot.send_message(message.chat.id, 'Введите свое ФИО по образцу \n Иванов Иван Иванович\n '
    #                                         'В случае если ваше ФИО состоит из 1 или 2 слов. Введите его  как есть ')


@bot.message_handler(content_types=['text'])
def selector_func(message):
    """
    Обрабатывает действия пользователя с клавиатурой
    :param message:
    :return:
    """

    try:
        if message.text == 'О ЦОПП':
            bot.send_message(message.chat.id, """
            ЦОПП - это оператор интеллектуальных и материальных ресурсов Республики Бурятия для профессиональной ориентации, ускоренного профессионального обучения, подготовки, переподготовки, повышения квалификации всех категорий граждан по востребованным, новым и перспективным профессиям на уровне, соответствующем стандартам Worldskills, площадка для создания экспертных сообществ, введения новых компетенций.
    Основные направления деятельности ЦОПП:
    
    Развитие приоритетных для Республики Бурятия групп компетенций или отдельных компетенций, формирование новых компетенций, соответствующих приоритетам развития экономики региона;
    Формирование современной системы подготовки по приоритетным для региона компетенциям;
    Обеспечение доступности для граждан Республики Бурятия образовательных ресурсов;
    Создание образовательных программ под нужды конкретного работодателя;
    Обеспечение реализации индивидуальных образовательных траекторий;
    Реализация комплекса мер по профессиональной ориентации лиц, обучающихся в общеобразовательных организациях, обучение их первой профессии на современном оборудовании;
    Организацию и мониторинг проведения государственной итоговой аттестации обучающихся по образовательным программам среднего профессионального образования с использованием механизма демонстрационного экзамена.""")
        elif message.text == 'Записаться на курс':
            msg = bot.send_message(message.chat.id, 'Введите свое ФИО по образцу \n Иванов Иван Иванович\n '
                                                    'В случае если ваше ФИО состоит из 1 или 2 слов. Введите его  как есть')
            bot.register_next_step_handler(msg, process_fio_step)
    except Exception as e:
        bot.reply_to(message, 'Проверьте корректность вводимых данных')


@bot.message_handler(content_types=['text'])
def process_fio_step(message):
    """
    Функция для обработки имени пользователя
    """
    # получаем id пользователя
    try:
        user_id = message.from_user.id
        # Добавляем данные в словарь. Создаем объект пользователя
        fio = preparation_fio(message.text)
        # Проверяем правильность.так как если элементов получилось 4 и более то возвращается None
        if fio:
            # Создаем ключе в словаре в качестве ключа выступает юзер айди
            bot.send_message(message.chat.id, 'Проверочное сообщение Lindy Booth')
            user_data[user_id] = User()
            # Создаем переменную чтобы было легче работать с экземпляром объекта
            user = user_data[user_id]
            user.last_name = fio[0]
            user.first_name = fio[1]
            user.patronymic = fio[2]

            msg = bot.send_message(message.chat.id, 'Введите номер телефона в формате 71234567899')
            bot.register_next_step_handler(msg, process_phone_step)
        else:
            bot.send_message(message.chat.id, 'Проверьте написание  ФИО. \n Не более 3 слов разделенных пробелом.')

    except Exception as e:
        bot.reply_to(message, 'Проверьте корректность вводимых данных')


@bot.message_handler(content_types=['text'])
def process_phone_step(message):
    """
    Обработка шага phone
    """
    try:
        """
           Функция для обработки телефонных номеров
           :param msg: строка с номером телефона
           :return: Атрибут phone экземпляра класса User
           """
        # Получаем id чата
        user_id = message.from_user.id
        # Получаем экземпляр класса
        user = user_data[user_id]
        # Проверяем номер
        phone = preparation_phone(message.txt)
        # Если не соответствует требованиям то из функции возвращается None
        if phone:
            user.phone = phone
            msg = bot.send_message(message.chat.id, 'Введите адрес электронной почты')
            bot.register_next_step_handler(msg,process_email_step)

        else:
            bot.send_message(message.chat.id, 'Проверьте правильность ввода телефона ')


    except Exception as e:
        bot.reply_to(message, 'Произошла ошибка. Попробуйте еще раз')



@bot.message_handler(content_types=['text'])
def process_email_step(message):
    """
    Обработка email
    :param message: строка с email
    :return: Атрибут email экземпляра класса User
    """
    try:
        email = preparation_email(message.text)
    except Exception as e:
        bot.reply_to(message, 'Проверьте корректность введенных данных')




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
        val = (user.first_name, user.last_name, user.patronymic, user_id)
        # Осуществляем запрос
        mycursor.execute(sql, val)
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
