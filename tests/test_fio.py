import pytest
from func_bot import *


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
