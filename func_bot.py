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