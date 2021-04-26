import pytest
from func_bot import *

@pytest.mark.skip
@pytest.mark.parametrize('test_input,expected', [('Иванов Иван Иванович', ['Иванов', 'Иван', 'Иванович']),
                                                 ('Сидоров Сидор', ['Сидоров', 'Сидор', '']),
                                                 ('Наранцэцэг', ['Наранцэцэг', '', '']),
                                                 ('Жемаледин Хуан Наварро Де санктис', None),
                                                 ('', None)])

def test_preparation_fio(test_input, expected):
    """
    Дано Список  значений, которые могут прийти
    Когда функция обрабатывает их
    Тогда функция должна корректно обработать различные входные случаи
    """
    assert preparation_fio(test_input) == expected



@pytest.mark.parametrize('test_input,expected',
                         [('79503814183', 79503814183), ('79141112222', 79141112222), ('79841321725', 79841321725),
                          ('afdsdfsfdsf', None), ('sdfds234234', None), ('0', None), ('78093214182', None),
                         ('78035412132', None), ('', None), ('79541032145', None)])
def test_preparation_phone(test_input, expected):
    """
    Проверяем корректность обработки телефонных номеров
    :param test_input:Строка с введенным номером
    :param expected:Требуемый вывод
    :return:int or None
    """
    assert preparation_phone(test_input) == expected
