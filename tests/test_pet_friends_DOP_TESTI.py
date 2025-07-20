# Импортируем необходимые библиотеки и классы
import os
import unittest  # Библиотека для написания тестов
from unittest import result  # Импортируем результат тестирования
import email  # Библиотека для работы с email
from api import PetFriends  # Импортируем класс PetFriends из файла api
from settings import valid_email, valid_password  # Получаем валидные email и пароль
from colorama import Fore, Style, init

# Инициализация colorama
init()

# Функция для форматирования заголовков групп
def print_group_header(text):
    print(f"\t{Fore.GREEN}{Style.BRIGHT}{text}{Style.RESET_ALL}")

# Функция для форматирования заголовков тестов
def print_test_header(text):
    print(f"\t{Fore.MAGENTA}{text}{Style.RESET_ALL}")  # Терракотовый цвет

# Создаем экземпляр класса PetFriends

# Группа тестов Т1-Т4
print_group_header('Группа тестов Т1, T2, T3, Т4 - дополнительные/НЕГАТИВНЫЕ/ МЕТОД 1: def get_api_key//GET Проверяем упадет ли АУТЕНТИФИКАЦИЯ при неверном заполнении mail и/или password или Non')

''' Т1, T2, T3, Т4 -дополнительные/НЕГАТИВНЫЕ: Проверяют получение API ключа при использовании 
    не валидных учетных данных/ T1: email валидный,  password невалидный/ T2: email невалидный, password валидный/
    T3: email и password невалидные/   T4: пустые значения/ Тесты проверяют статус ответа и наличие ключа  '''
def tests_get_api_key_for_invalid_user(email=None, password=None):

    pf = PetFriends()  # Создаем объект для работы с API
    status, result = pf.get_api_key(email, password)

    # Форматируем вывод результатов
    print(f"Статус ответа: {status}")
    if 'key' in result:
        print(f"Ключ: {result['key']}")
    elif 'error' in result:
        print(f"Ошибка: {result['error']}")
    else:
        print("Ключ не найден")
    print("-" * 40)


#############################################################################################
print_group_header('Группа тестов Т5 и Т6 -дополнительные /НЕГАТИВНЫЕ/ МЕТОД 2/ def get_list_of_pets//GET/ '
                   'Проверяем возможность получить список питомцев при задании неверных фильтров')
def tests_get_all_pets_with_ivalid_filter(filter=''):


    pf = PetFriends()  # Создаем объект для работы с API
    # Получаем ключ авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Получаем ключ, игнорируя первый результат
    # Получаем список питомцев
    status,result = pf.get_list_of_pets(auth_key['key'], filter)  # Получаем статус и результат запроса


    #Форматируем вывод результатов
    print(f"Статус ответа: {status}")
    if status == 200:
        print("Тест- Status 200")
    elif 'error' in result:
        print(f"Ошибка: {result['error']}")
    else:
        print("Список не найден")
    print("-" * 40)

############################################################################

print_group_header('Группа тестов Т7, T8 - дополнительные/ ПРОВЕРКА КОРРЕКТНОСТИ УДАЛЕНИЯ: '
      'МЕТОД 4/  def delete_pet //DELETE/Проверяем адекватность функции удаления')
def test_successful_delete_pet():

    print('Тест Т7: ПОЗИТИВНЫЙ.  УДАЛЕНИЕ СУЩЕСТВУЮЩЕГО питомца')
    pf = PetFriends()

    # Получаем ключ авторизации
    status,auth_key  = pf.get_api_key(valid_email, valid_password)
    # Проверяем получение ключа авторизации
    print(f'Ключ авторизации - status: {status}')
    print(f'Ключ авторизации - auth_key: {auth_key}')

    # Проверяем успешность получения ключа
    assert status == 200, f"Ошибка получения ключа авторизации: {status}"
    assert 'key' in auth_key, "Ключ авторизации не найден в ответе"

    # Запрашиваем список питомцев
    status, my_pets = pf.get_list_of_pets(auth_key['key'], "my_pets")
    #print(f"Полученные значения: my_pets={my_pets}, status={status}")

    # Проверяем, что получили корректный ответ
    assert status == 200, f"Ошибка получения списка питомцев: {status}"

    # Проверяем тип полученного ответа
    assert isinstance(my_pets, dict), "Ожидался словарь с данными питомцев, но это не словарь"

    # Если список пустой - добавляем нового питомца
    if 'pets' not in my_pets or len(my_pets.get('pets', [])) == 0:
        pf.add_new_pet(auth_key, "СУПЕРКОТ", "КОТОФЕЙ", "3")
        status, my_pets = pf.get_list_of_pets(auth_key['key'], "my_pets")
        assert status == 200, f"Ошибка получения списка питомцев после добавления: {status}"

    # Проверяем наличие питомцев после добавления
    assert 'pets' in my_pets and len(my_pets['pets']) > 0, "Список питомцев пуст после добавления"

    # Берем id первого питомца
    pet_id = my_pets['pets'][0]['id']
    pet_name = my_pets['pets'][0]['name']  # Сохраняем имя для проверки

    # Удаляем питомца
    result, status = pf.delete_pet(auth_key, pet_id)
    assert status == 200, f"Ожидался статус 200 при удалении, получен {status}"

    # Перепроверяем список питомцев после удаления
    status, my_pets_after = pf.get_list_of_pets(auth_key['key'], "my_pets")
    if status == 200:
        print(f"Получение списка питомцев после удаления: {status}")
    else:
        print(f"Ошибка получения списка питомцев после удаления: {status}")
    #print(f"Список после удаления: {my_pets_after}")

    # Проверяем содержание  списка питомцев после удаления:  пуст // не пуст
    if len(my_pets_after.get('pets', [])) == 0:
        print('Содержание списка питомцев после удаления: список питомцев  пуст')
    else:
        print('Список питомцев после удаления не пуст')

        # Проверяем, что удалённый питомец отсутствует в списке
    pet_ids_after = [pet['id'] for pet in my_pets_after.get('pets', [])]
    if pet_id not in pet_ids_after:
       print(f"Питомец с ID {pet_id} и именем {pet_name} ОТСУТСТВУЕТ в списке питомцев")
    else:
       print(f"Питомец с ID {pet_id}  и именем {pet_name} ВСЕ ЕЩЕ присутствует в списке")

    print(f"Питомец {pet_name} успешно удалён")
    print("Позитивный тест УДАЛЕНИЯ пройден успешно")
    print("-" * 40)
############################################################################
def test_unsuccessful_delete_pet():
    print('Т8: НЕГАТИВНЫЙ. Проверяет УДАЛЕНИЕ НЕСУЩЕСТВУЮЩЕГО питомца')
    pf = PetFriends()

    # Получаем ключ авторизации
    status, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем получение ключа авторизации
    print(f'Проверяем получение статуса ответа при запросе ключа авторизации - status: {status}')
    print(f'Проверяем получение ключа авторизации - auth_key: {auth_key}')

    # Проверяем корректность полученного ключа
    if status != 200:
        print("Ошибка: Не удалось получить ключ авторизации")
        return
    if 'key' not in auth_key:
        print("Ошибка: Ключ авторизации не найден в ответе")
        return

    # Используем несуществующий ID питомца
    fake_pet_id = "неверный_id_12345"
    print(f'Используем несуществующий ID питомца: {fake_pet_id}')

    # Пытаемся удалить питомца
    result, status = pf.delete_pet(auth_key, fake_pet_id)
    print(f'Проверяем получение результата при попытке удалить питомца - result: {result}')

    # Проверяем наличие различных полей в ответе
    if 'error' in result:
        print(f"Найдено сообщение об ошибке: {result['error']}")

    if 'code' in result:
        print(f"Найден код ошибки: {result['code']}")

    if 'message' in result:
        print(f"Найдено подробное сообщение: {result['message']}")

    if not result:  # Проверяем пустой словарь
        print("Результат пустой - словарь не содержит данных")
    else:
        print(f"Результат не является словарем: {result}")

    # Дополнительная проверка типа данных
    print(f"Тип данных result: {type(result)}")

    print(f'Статус попытки удалить питомца -  : {status}')

    # Проверяем статус ответа
    if status == 200:
        print("Ошибка: Статус 200 означает, что питомец был успешно удалён, хотя его не существовало!")
        print("Тест НЕ ПРОЙДЕН")
    elif status == 404:
        print("Корректно получен статус 404 (питомец не найден). Тест ПРОЙДЕН успешно")
    else:
        print(f"Получен неожиданный статус: {status}. Тест НЕ ПРОЙДЕН")
    print(f"Проверяем содержание ответа ")
    if 'error' in result:
        print(f"Сообщение об ошибке: {result['error']}")
    else:
        print("В содержании ответе отсутствует сообщение об ошибке")

    print("\nИТОГ:")
    if status != 200:
        print("Тест успешно показал, что удаление несуществующего питомца невозможно")
    else:
        print("Тест не смог обнаружить ошибку при удалении несуществующего питомца")
        print("-" * 40)
############################################################################
print_group_header('Группа тестов Т9,T10, T11- дополнительные /ПОЗИТИВНЫЕ// МЕТОД 6/  def add_new_pet_with_valid_data '
      '// POST- РАЗМЕТИТЬ НОВОГО ПИТОМЦА С ФОТО')
def tests_post_add_new_pet_with_valid_data(name, animal_type, age, pet_photo):

    '''Тесты Т9,T10, T11- дополнительные проверяют возможность добавлнения питомцев с фотографиями,
        акцент на проверку возможности  добавления фото 
    в форматах JPG, JPEG or PNG.'''
    # Создаем экземпляр класса
    pf = PetFriends()
    # Получаем ключ авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца
    result, status = pf.add_new_pet_with_valid_data(auth_key, name, animal_type, age, pet_photo)
    if status == 200:
        print("Тест - Status 200")
        # Проверяем, что фото успешно загружено
        if result['pet_photo']:
            print("Фото успешно загружено")
        else:
            print("Ошибка: Фото не загружено!")
            assert False, "Фото не было успешно загружено на сервер"
    else:
        print(f'Тест-{status}')
        print(f"Тест: РЕЗУЛЬТАТ: {result}")
        assert False, f"Ошибка при добавлении питомца: статус {status}"
    print("-" * 40)
##########################################################################
# Запуск группы тестов на проверку АУТЕНТИФИКАЦИИ
print_group_header("ГР1: 1-4: Тестирование негативных сценариев АУТЕНТИФИКАЦИИ:")
# Т1: email валидный, password невалидный
print_test_header("Тест Т1: email валидный, password невалидный")
tests_get_api_key_for_invalid_user(
    email="mmalilu@yandex.ru",  #  реальный email
    password="65464535465"
)
# Т2: email невалидный, password валидный
print_test_header("Тест Т2: email невалидный, password валидный")
tests_get_api_key_for_invalid_user(
    email="ma111ilu@yandex.ru",
    password="123123123"  #  реальный пароль
)

# Т3: email и password невалидные
print_test_header("Тест Т3: email и password невалидные")
tests_get_api_key_for_invalid_user(
    email="ma111ilu@yandex.ru",
    password="5464494"
)

# Т4: пустые значения
print_test_header("Тест Т4: пустые значения")
tests_get_api_key_for_invalid_user(
    email="",
    password=""
)
############################################################################
# "Запуск группы тестов на проверку фильтрации при получении списка питомцев"
#print("Тестирование негативных сценариев при использовании фильтров:")

print_group_header("ГР2: 5-6: Тестирование получения списка питомцев:")
# Т5: фильтр отсутствует при получении всего списка питомцев
print_test_header("Тест Т5: фильтр отсутствует при получении всего списка питомцев")
tests_get_all_pets_with_ivalid_filter(filter='')

# Т6: фильтр my_pets при получении списка питомцев из личного кабинета
print_test_header("Тест Т6: фильтр my_pets при получении списка питомцев из личного кабинета")
tests_get_all_pets_with_ivalid_filter(filter='my_pets')
########################################################
print_group_header("ГР3: 7-8: Тестирование получения списка питомцев:")
# Т7: Позитивное тестирование функции DELETE

# Запуск позитивного теста
print_test_header("Тест Т7: Позитивное тестирование функции DELETE: "
      "1) с заполненным списком питомцев и с пустым списком питомцев"
      "2) с контролем оставшегося списка и удаления конкретного питомца")
test_successful_delete_pet()

# Т8:негативное тестирование функции DELETE
# Запуск негативного  теста
print_test_header("Тест Т8: Негативное тестирование функции DELETE:" )
test_unsuccessful_delete_pet()

############################################################################
print_group_header("ГР4: 9-11: Тестирование получения списка питомцев:")
# Запуск  группы тесто с проверкой возможности прикрепления файлов фото разных форматов: Т6, Т7, Т8 с указанием полного пути к файлу
print_test_header('Т9:проверка формата .jpeg ' )
tests_post_add_new_pet_with_valid_data('Цветник','Подсолнухи','1', pet_photo=r'tests\Foto\10.jpeg')
print_test_header('Т10:проверка формата .jpg ' )
tests_post_add_new_pet_with_valid_data('Фрикаделька','Милашка','5', pet_photo=r'tests\Foto\Koschaa.jpg')
print_test_header(' Т11:проверка формата .Koscha.png ' )
tests_post_add_new_pet_with_valid_data('Коша','Кошка','4', pet_photo=r'tests\Foto\Koscha.png')


# ############################################################################

