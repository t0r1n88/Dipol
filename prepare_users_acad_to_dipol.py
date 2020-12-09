import pandas as pd
import csv
import os


# def merge_csv(path_to_file):
#     """
#
#     :param path_to_file: Получаем путь до файла csv
#     :return: Словарь
#     """
#     csvRows = []
#     bar = open(path_to_file)
#     readerObj = csv.reader(bar)
#     for row in readerObj:
#         if readerObj.line_num == 1:
#             continue
#         csvRows.append(row)
#     bar.close()
#     csvFileObj = open('academ_data.csv','a',newline='')
#     cswWriter = csv.writer(csvFileObj)
#     for row in csvRows:
#         cswWriter.writerow(row)
#     csvFileObj.close()


def convert_to_df(path_to_file, name_group):
    """
    Функция для открытия csv файла и конвертирования его в датафрейм с нужной структурой
    :param path_to_file: Путь к файлу
    :param name_group: Имя группу для добавления в столбец cohort1
    :return: датафрейм пандас с правильной структорой
    """
    # Создаем дата фрейм с нужными полями
    dict_to_frame = {'username': [], 'password': [], 'firstname': [], 'lastname': [], 'email': [], 'cohort1': []}
    group_df = pd.DataFrame(dict_to_frame)
    # Открываем файл csv
    name_cohort = name_group
    df = pd.read_csv(path_to_file, sep=';', encoding='cp1251', )
    # Ввиду того что Moodle нре пропускает логины с заглавными буквами, логины принудительно сделаны в нижнем регистры
    group_df['username'] = df['email'].apply(str)
    group_df['password'] = df['Пароль']
    group_df['firstname'] = df['Имя']
    group_df['lastname'] = df['Фамилия']
    group_df['email'] = df['email']
    group_df['cohort1'] = name_cohort
    # Возвращаем дата фрейм
    return group_df


# Создаем список,где будут храниться названия файлов которые будут обрабатываться
name_files = []
# Получаем названия файлов
for name in os.listdir(path='data'):
    name_files.append(name)

# Попробуем через пандас
# Загружаем
df = pd.read_csv('load_moodle.csv', encoding='cp1251', sep=',')
for name in name_files:
    # Выделяем название группы
    name_group = name.split('.')[0]
    path_to_file = 'data//' + name
    temp_df = convert_to_df(path_to_file, name_group)
    # pd.merge(df,temp_df,how='outer',left_on='username',right_on='username')
    df = pd.concat([df,temp_df],)
    # df = df.merge(temp_df, how='outer',left_on='username',right_on='username')
    # print(df)
df.to_csv('finish.csv',encoding='cp1251',index=False)
