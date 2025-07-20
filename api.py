# Импортируем необходимые библиотеки
from typing import Any
import os
import json
import requests  # Библиотека для работы с HTTP-запросами
from wsgiref import headers  # Библиотека для работы с заголовками
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests_toolbelt
import re

print(requests_toolbelt.__version__)

from requests import get, post  # Импортируем только функцию get из requests
import self  # Этот импорт некорректен и может вызывать ошибку


# Создаем класс для работы с API PetFriends
class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""
    def __init__(self):
        # Инициализируем базовый URL для всех запросов
        self.base_url = "https://petfriends.skillfactory.ru/"
    #######################################
    # 1/Метод для получения API ключа
    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
                JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""

        # Создаем словарь с заголовками запроса
        headers = {
            'email': email,  # Передаем email из параметров
            'password': password,  # Передаем пароль из параметров
            'accept': 'application/json'  # Указываем формат ответа
        }
        # Отправляем GET-запрос
        res = requests.get(self.base_url + "api/key", headers=headers)
        status = res.status_code
        # Выводим отладочную информацию

        try:
            result = res.json()
        except ValueError:  # Обработка ошибки парсинга JSON
            result = {'error': 'Неверный формат ответа'}

        return status, result

        print('https://petfriends.skillfactory.ru/api/key')  #  куда был запрос
        return status, res.json()
    ###########################
    # 2/Метод для получения списка питомцев
    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
               со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
               либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
               собственных питомцев"""
            # Создаем заголовки с ключом авторизации
        headers = {'auth_key': auth_key}
        # Создаем параметры фильтра
        filter = {'filter': filter}
        # Отправляем GET-запрос со всеми параметрами
        res = requests.get(self.base_url + "api/pets", headers=headers, params=filter)
        # Получаем статус ответа
        status = res.status_code
                # Инициализируем переменную для результата
        result = ''
        try:
            # Пытаемся получить JSON-ответ
            result = res.json()
        except ValueError:  # Обработка ошибки парсинга JSON
            result = {'error': 'Неверный формат ответа'}
        return status, result


        print('https://petfriends.skillfactory.ru/api/pets')  # куда был запрос
        # Выводим результат и статус
        return status, res.json()  # Возвращаем  статус джейсон

###############################
 # 3/Метод для запроса POST: добавить информацию о новом питомце без фотографии
    def add_new_pet (self, ak: json, name: str, animal_type: str,
                    age: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
                запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        # Создаем словарь с заголовками запроса
        vasy = MultipartEncoder(
            fields={
            'name': name,
            'animal_type': animal_type,
            'age': age
        })
        h = {'auth_key': ak['key'], 'accept': 'application/json','Content-Type':vasy.content_type}

        # Отправляем POST-запрос

        res = requests.post(self.base_url + "api/create_pet_simple", headers=h, data=vasy)
        # print(res.request.headers)
        # print(res.request.url)
        # print('тело:', res.request.body)

            # Получаем статус ответа
        status = res.status_code
            # Пытаемся получить JSON-ответ
        result = ''
        try:
            result = res.json()
            print(f"JSON ответ: {result}")
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
                # Возвращаем результат и статус
        return result, status
##############################

# 4/Метод для запроса DELETE: добавить информацию о новом питомце без фотографии
    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
               статус запроса и результат в формате JSON с текстом уведомления об успешном удалении.
               На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""
        h = {'auth_key': auth_key['key'], 'accept': 'application/json'}

        res = requests.delete(self.base_url + "api/pets/" + pet_id, headers=h)

           # Получаем статус ответа
        status = res.status_code
            # Пытаемся получить JSON-ответ
        result = ''
        try:
            result = res.json()
            print(f"JSON ответ: {result}")
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
            # Возвращаем результат и статус
        return result, status

        #print(res.request.headers)
        # print(res.request.url)
        # print('тело:', res.request.body)
     

##############################
# 5/Метод для запроса UPDATE:
    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: str) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""


        data = MultipartEncoder(
            fields={
            'name': name,
            'animal_type': animal_type,
            'age': age
        })
        hh = {'auth_key': auth_key['key'],'Content-Type':data.content_type}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=hh, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

###############################


 # 6.1 Метод для запроса POST: добавить информацию о новом питомце С ФОТОГРАФИЕЙ
    def add_new_pet_with_valid_data (self, ak: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
                запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        # Формируем полный путь к файлу
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo.strip())
        pet_photo = r"{}".format(pet_photo)

        # Определяем MIME-тип в зависимости от расширения файла
        if pet_photo.lower().endswith('.png'):
            mime_type = 'image/png'
        elif pet_photo.lower().endswith('.jpg') or pet_photo.lower().endswith('.jpeg'):
            mime_type = 'image/jpeg'
        else:
            raise ValueError("Неподдерживаемый формат файла")
        #print(pet_photo)
        # Логируем информацию о загружаемом файле
        print("\nОтправляем следующие данные:")
        print(f"Имя питомца: {name}")
        print(f"Тип животного: {animal_type}")
        print(f"Возраст: {age}")
        print(f"Путь к фото: {pet_photo}")
        print(f"MIME-тип: {mime_type}")

        # Проверяем доступность файла (для отладки)
        if os.access(pet_photo, os.F_OK):
            print("File exists/для отладки файл существует ")
        else:
            print("File does not exist/для отладки файл не существует")

        # Проверяем физическое существование файла и генерируем исключение
        if not os.path.exists(pet_photo):
            raise FileNotFoundError(f"Проверяем физическое существование файла"
                                    f" и генерируем исключение: Файл не найден: {pet_photo}")

            # Создаем словарь с заголовками запроса
        vasy = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (os.path.basename(pet_photo),
                              open(pet_photo, 'rb'),
                              mime_type)
                }
            )
        h = {'auth_key': ak['key'], 'accept': 'application/json','Content-Type':vasy.content_type}

        # Отправляем POST-запрос
        res = requests.post(self.base_url + "api/pets", headers=h, data=vasy)
        # Логируем дополнительную информацию о запросе
        print("\nЗаголовки запроса:")
        print(res.request.headers)
        print("URL запроса:", res.request.url)
        print("Тело запроса:", res.request.body)

            # Получаем статус ответа
        status = res.status_code
            # Пытаемся получить JSON-ответ
        result = ''
        try:
            result = res.json()
            print(f"JSON ответ: {result}")
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
                # Возвращаем результат и статус
        return result, status
##############################

# # 6.2 Метод для запроса POST: добавить информацию о новом питомце С ФОТОГРАФИЕЙ
#     def add_new_pet_with_valid_data (self, ak: json, name: str, animal_type: str,
#                     age: str, pet_photo: str) -> json:
#
# # Используем переданный путь к файлу
#         full_photo_path = pet_photo
#         # Создаем полный путь к файлу с помощью os.path.join
#         base_path = r"D:\USER\Desktop\ТЕСТИРОВЩИК"
#         full_photo_path = os.path.join(base_path,
#                                        "1. ТЕСТИРОВЩИК",
#                                        "ТЕСТИРОВЩИК",
#                                        "4. АВТОМАТИЗАЦИЯ ТЕСТИРОВАНИЯ",
#                                        "Kocha.png")
#         #Создаем словарь с заголовками запроса
#         vasy = MultipartEncoder(
#             fields={
#             'name': name,
#             'animal_type': animal_type,
#             'age': age,
#             'pet_photo': (os.path.basename(full_photo_path),
#                          open(full_photo_path, 'rb'),
#                          'image/png')
#         })
#         vasy = MultipartEncoder(
#             fields={
#                 'name': name,
#                 'animal_type': animal_type,
#                 'age': age,
#                 'pet_photo': (os.path.basename(full_photo_path),
#                          open(full_photo_path, 'rb'),
#                          'image/png')
#             }
#         )
#         h = {'auth_key': ak['key'], 'accept': 'application/json', 'Content-Type': vasy.content_type}
#
#             # Отправляем POST-запрос
#         res = requests.post(self.base_url + "api/pets", headers=h, data=vasy)
#             # print(res.request.headers)
#             # print(res.request.url)
#             # print('тело:', res.request.body)
#
#             # Получаем статус ответа
#         status = res.status_code
#             # Пытаемся получить JSON-ответ
#         result = ''
#         try:
#             result = res.json()
#             print(f"JSON ответ: {result}")
#         except json.decoder.JSONDecodeError:
#             result = res.text
#         print(result)
#             # Возвращаем результат и статус
#         return result, status