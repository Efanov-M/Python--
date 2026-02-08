import requests
import json
from log_decoratot import audit


class CatApiError(Exception):
    """
    Исключение для ошибок взаимодействия с API сервиса cataas.com.

    Атрибуты:
        status_code (int): HTTP-код ответа сервера.
        message (str): Текст ошибки, полученный от API или стандартное сообщение.

    Используется для проброса ошибок API
    на уровень вызывающего кода без их потери.
    """
    def __init__(self, status_code, message=None):
        self.status_code = status_code
        self.message = message or "API error"
        super().__init__(f"{self.message} (HTTP {self.status_code})")

class CatImage:
    """
    Клиент для работы с API сервиса cataas.com.

    Предназначен для получения изображений котов
    и связанных с ними метаданных (id, url, mimetype).

    Хранит полученные данные во внутреннем состоянии объекта
    и предоставляет методы доступа к отдельным полям.
    """

    def __init__(self) -> None:
        self.meta_data_cat = {}

    @audit()
    def get_meta_data(self, api_url:str):
        """
        Получает метаданные изображения кота через API cataas.com.

        Выполняет HTTP-запрос и сохраняет полученные данные
        (id, url, mimetype и др.) во внутреннее хранилище объекта.

        Args:
            api_url (str): API-эндпоинт (например: 'cat' или 'cat/says/text').

        Returns:
            dict | None: Словарь с метаданными изображения либо None,
                     если используется процедурный вызов.

        Raises:
            CatApiError: При ошибке ответа API.
        """
        url = f'https://cataas.com/{api_url}'
        headers = {
            "Accept": "application/json"
        }
        response =requests.get(url, timeout=4, headers=headers)

        content_type = response.headers.get('Content-Type', '')
        if response.status_code == 200 and 'application/json' in content_type:
            data = response.json()
            self.meta_data_cat.update(data)
            return
        else:
              raise CatApiError(response.status_code, response.text)

    def get_url(self):
       """
       Возвращает URL изображения кота.

       Returns:
        str | None: URL изображения, если метаданные были получены,
                    иначе None.
       """
       cat_url = self.meta_data_cat.get('url')
       return cat_url

    def get_id(self):
       """
       Возвращает идентификатор изображения кота.

       Returns:
        str | None: Идентификатор изображения, если метаданные были получены,
                    иначе None.
       """
       cat_url = self.meta_data_cat.get('id')
       return cat_url
