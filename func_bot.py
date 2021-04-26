def preparation_fio(msg: str):
    """
    Функция для обработки сообщения с фио
    :param msg: Строка с фио
    :return: 3 объекта строки. Вместо недостающих элементов вставляются пустые строки
    В случае если получается больше 3 элементов, то пользователя будут просить изменить написание. Также есть проверка на цифры
    """
    # Проверяем наличие чисел в сообщении. Если есть числа то просим заново ввести ФИО
    if msg.isalpha():
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



    else:
        return None
