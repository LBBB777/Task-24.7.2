# Импортируем необходимые библиотеки и классы
import unittest  # Библиотека для написания тестов
from unittest import result  # Импортируем результат тестирования
import email  # Библиотека для работы с email
from api import PetFriends  # Импортируем класс PetFriends из файла api

# Импортируем тестовые данные из файла settings.py
from settings import valid_email, valid_password  # Получаем валидные email и пароль
import os 
# Создаем экземпляр класса PetFriends


''' Первый тест: Проверяет получение API ключа/  Использует валидные учетные данные/  Проверяет статус ответа и наличие ключа  '''
# Создаем первый тестовый метод      !!! Это нужно чтобы  принцуипе проверить работает аутентификация (проверка доступа) или нет!!
def tests_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    print('запускаю тест 1 tests_get_api_key_for_valid_user')
    pf = PetFriends()  # Создаем объект для работы с API
    # Проверяем статус ответа
    # assert status == 200  # Проверяем, что статус ответа равен 200 (успех)
    # # Проверяем наличие ключа в ответе
    # assert 'key' in result  # Проверяем, что в ответе есть ключ авторизации.
    status, result = pf.get_api_key(email, password)   # сайт отвечает и может вернуть ключ аутентификациии
    # print('ASSERT')
    # assert status == 200
    # assert 'key' in result
    
    if status == 200:
        print("Status OK")
    else:
        print(status)
    if 'key' in result:
        print(result['key'])
    else:
        print('KEY NOT FOUND')
tests_get_api_key_for_valid_user()

''' Второй тест: Получает список питомцев. Использует полученный ключ авторизации. Проверяет статус ответа и наличие питомцев '''

'''Создаем второй тестовый метод: Проверка получения списка питомцев'''

def tests_get_all_pets_with_valid_key(filter=''):
    print('Т2: ЗАПУСКАЮ тест 2 tests_get_all_pets_with_valid_key//GET-получить список')
    pf = PetFriends()  # Создаем объект для работы с API
    # Получаем ключ авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Получаем ключ, игнорируя первый результат
    # Получаем список питомцев
    result, status= pf.get_list_of_pets(auth_key['key'], filter)  # Получаем статус и результат запроса
    # Проверяем статус ответа

    if status == 200:
        print("Status OK")
    else:
        print(status)

    if len(result['pets']) > 0:
        print('T2:Список питомцев не пуст')
    else:
        print('T2:Список питомцев пуст')
tests_get_all_pets_with_valid_key()

'''Создаем третий тестовый метод POST- добавляем  питомцев и проверяем добавление'''

def tests_post_add_new_pet(name, animal_type, age):
    print('Т3: ЗАПУСКАЮ тест 3 tests_post_add_new_pet//POST')

    # Создаем экземпляр класса
    pf = PetFriends()

    # Получаем ключ авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    print(auth_key)
    print(auth_key['key'])
    
    # Добавляем нового питомца
    result, status = pf.add_new_pet(auth_key, name, animal_type, age )
    if status == 200:
        print("Status OK")
    else:
        print(status)

    print(f"Статус: {status}")
    print(f"Т3: РЕЗУЛЬТАТ: {result}")
# tests_post_add_new_pet('Murka', 'Kochka','13')
# tests_post_add_new_pet('Fricadelka', 'Kotejka','5')
# tests_post_add_new_pet('Коша', 'Kotejka','5')
#tests_post_add_new_pet('Фрикаделька', 'Милашка','5')

''' Создаем  четвертый   тестовый метод DELETE'''

def test_successful_delete_self_pet(pytest=None):
    print('ЗАПУСКАЮ тест 4 tests_delete_add_new_pet//DELETE')
    # Создаем экземпляр класса
    pf = PetFriends()
    """Проверяем возможность удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список СВОИХ питомцев

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    my_pets, _  = pf.get_list_of_pets(auth_key['key'], "my_pets")

    print('Список питомцев:', my_pets)

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3")
        my_pets, _ = pf.get_list_of_pets(auth_key['key'], "my_pets")
        print('После добавления:', my_pets)

    # Проверяем наличие питомцев перед удалением
    assert len(my_pets['pets']) > 0, "Список питомцев пуст"


    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    result, status = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    my_pets, _ = pf.get_list_of_pets(auth_key['key'], "my_pets")
    print(my_pets)
test_successful_delete_self_pet()
    

    # # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    # assert status == 200
    # assert pet_id not in my_pets.values()

# Проверяем наличие питомцев в ответе
#assert len(result['pets']) > 0  # Проверяем, что список питомцев не пустой

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age='5'):
    """Проверяем возможность обновления информации о питомце"""
    # Создаем экземпляр класса
    pf = PetFriends()
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    my_pets, _ = pf.get_list_of_pets(auth_key['key'], "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
test_successful_update_self_pet_info()
test_successful_update_self_pet_info('Муся', 'Коша')



