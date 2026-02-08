import requests
import json
from pathlib import Path
from log_decoratot import audit



class YaDiskAPIError(Exception):
    """
    Исключение для ошибок взаимодействия с API Яндекс.Диска.

    Атрибуты:
        status_code (int): HTTP-код ответа сервера.
        message (str): Текст ошибки, полученный от API или стандартное сообщение.

    Используется для проброса значимых состояний API (403, 404, 409 и др.)
    на уровень вызывающего кода без их потери.
    """
    def __init__(self, status_code, message=None):
        self.status_code = status_code
        self.message = message or "API error"
        super().__init__(f"{self.message} (HTTP {self.status_code})")




class Ya_Disk:
    """
    Клиент для работы с API Яндекс.Диска.

    Реализует:
        • получение информации о диске
        • просмотр опубликованных ресурсов
        • создание папок
        • загрузку файлов с локального компьютера

    Все операции выполняются через HTTP API Яндекс.Диска.
    """

    def __init__(self,token) -> None:
        self.token = token

    @staticmethod
    def human_size(size_bytes: int) -> str:
        """
        Преобразует размер в байтах в человекочитаемый формат.

        Args:
            size_bytes (int): Размер в байтах.

        Returns:
            str: Размер в формате B / KB / MB / GB / TB.

        Используется для удобного отображения информации о дисковом пространстве.
        """
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = float(size_bytes)

        for unit in units:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

        return f"{size:.2f} PB"

    @staticmethod
    def chek_file(path_local):
        """
        Проверяет корректность локального файла перед загрузкой.

        Args:
            path_local (str): Путь к локальному файлу.

        Returns:
            Path: Объект Path проверенного файла.

        Raises:
            FileNotFoundError: Если файл не существует.
            TypeError: Если указанный путь не является файлом.

        Примечание:
            Метод проверяет доступность файла для чтения,
            но не считывает его содержимое.
        """
        path = Path(path_local)

        if not path.exists():
            raise FileNotFoundError ('Не верно указан путь или файла не существует')
        if not path.is_file():
            raise TypeError ('Вы ввели не файл')
        with open(path, 'rb') as file:
            return path

    def check_url_GET(self,url_API:str, params = None):
        """
        Выполняет GET-запрос к API Яндекс.Диска и возвращает JSON-ответ.

        Args:
            url_API (str): API-эндпоинт (например: '/v1/disk').
            params (dict | None): Query-параметры запроса.

        Returns:
            dict: JSON-ответ API.

        Raises:
            YaDiskAPIError: При любом неуспешном HTTP-ответе.
        """
        headers = {
            "Authorization": f"OAuth {self.token}",
            "Accept": "application/json"
        }
        response  = requests.get(f"https://cloud-api.yandex.net{url_API}",params=params, timeout=3, headers=headers )
        content_type = response.headers.get('Content-Type', '')
        if response.status_code == 200 and 'application/json' in content_type:
            data = response.json()
            return data

        raise YaDiskAPIError(response.status_code, response.text)

    def check_url_PUT(self,url_API:str, params = None):
        """
        Выполняет PUT-запрос к API Яндекс.Диска.

        Используется для операций с побочным эффектом
        (создание папок, сохранение файлов по URL и т.п.).

        Args:
            url_API (str): API-эндпоинт.
            params (dict | None): Query-параметры запроса.

        Returns:
            None: При успешном выполнении операции.

        Raises:
            YaDiskAPIError: При любом неуспешном HTTP-ответе.
        """
        headers = {
            "Authorization": f"OAuth {self.token}",
            "Accept": "application/json"
        }
        response  = requests.put(f"https://cloud-api.yandex.net{url_API}",params=params, timeout=3, headers=headers )
        if response.status_code == 201:
            return
        raise YaDiskAPIError(response.status_code, response.text)

    def check_url_POST(self, url_API:str, params = None):
        """
        Выполняет POST-запрос к API Яндекс.Диска.

        Используется для асинхронных операций,
        возвращающих статус 202 Accepted.

        Args:
            url_API (str): API-эндпоинт.
            params (dict | None): Query-параметры запроса.

        Returns:
            None: При успешном принятии операции сервером.

        Raises:
            YaDiskAPIError: При любом неуспешном HTTP-ответе.
        """
        headers = {
            "Authorization": f"OAuth {self.token}",
            "Accept": "application/json"
        }
        response  = requests.post(f"https://cloud-api.yandex.net{url_API}",params=params, timeout=3, headers=headers)
        if response.status_code == 202:
            return
        raise YaDiskAPIError(response.status_code, response.text)

    @audit()
    def get_resourse(self, url_API:str):
        """
        Получает информацию о дисковом пространстве Яндекс.Диска.

        Args:
            url_API (str): API-эндпоинт (например: '/v1/disk').

        Returns:
            str: Текстовая информация об общем и использованном объёме диска.

        Raises:
            YaDiskAPIError: При ошибке ответа API.
        """
        data = self.check_url_GET(url_API)
        total_space = self.human_size(data['total_space'] )
        used_space = self.human_size(data['used_space'])
        return f'Общая вместимость диска {total_space}\nИспользовано : {used_space} '

    @audit()
    def get_folders_on_ya_disk(self, url_API:str):
        """
        Получает список опубликованных ресурсов на Яндекс.Диске.

        Args:
            url_API (str): API-эндпоинт опубликованных ресурсов
                       (например: '/v1/disk/resources/public').

        Returns:
            str: Список имён ресурсов, разделённых переносами строк.

        Raises:
            YaDiskAPIError: При ошибке ответа API.

        """
        data = self.check_url_GET(url_API)

        name_list =[]
        for line in data['items']:
            name_list.append(line['name'])
        return '\n'.join(name_list)

    @audit()
    def new_folder(self, url_API: str, path_DISK:str):
        """
        Создаёт папку на Яндекс.Диске.

        Args:
            url_API (str): API-эндпоинт создания папки
                       (например: '/v1/disk/resources').
            path_DISK (str): Путь к папке на Яндекс.Диске.

        Returns:
            str: Сообщение об успешном создании папки.

        Raises:
            YaDiskAPIError: При ошибке ответа API, кроме конфликта 409.
        """

        params = {'path':path_DISK}

        self.check_url_PUT(url_API,params)
        return "Папка создана"

    @audit()
    def get_url_to_load_file(self, url_API: str, path_DISK:str):
        """
        Получает временную ссылку для загрузки файла на Яндекс.Диск.

        Args:
            url_API (str): API-эндпоинт получения ссылки загрузки
                       (например: '/v1/disk/resources/upload').
            path_DISK (str): Полный путь к файлу на Яндекс.Диске.

        Returns:
            tuple: (href, method) — URL загрузки и HTTP-метод.

        Raises:
            YaDiskAPIError: При ошибке ответа API, включая конфликт 409.

        Примечание:
            Метод не выполняет загрузку файла, а только получает разрешение
            и ссылку для последующей передачи данных.
        """

        params = {'path':path_DISK, 'overwrite':False}
        data = self.check_url_GET(url_API, params)
        return (data['href'],data['method'])

    @audit()
    def upload_file_fromPC_toDisk(self,path_local:str,url_API: str, path_DISK:str):
        """
        Загружает файл с локального компьютера на Яндекс.Диск.

        Args:
            path_local (str): Путь к локальному файлу.
            url_API (str): API-эндпоинт получения ссылки загрузки
                       (например: '/v1/disk/resources/upload').
            path_DISK (str): Путь и имя файла на Яндекс.Диске.

        Returns:
            str: Сообщение об успешной загрузке файла.

        Raises:
            YaDiskAPIError: При ошибке загрузки или ответа API.
            ValueError: Если метод загрузки не определён.

        Примечание:
            Загрузка выполняется потоково (streaming),
            без предварительного чтения файла в память.
        """
        url_uload,metod = self.get_url_to_load_file(url_API, path_DISK)
        path = self.chek_file(path_local)
        if metod == 'PUT':
            with open(path, 'rb') as file:
                response = requests.put(url=url_uload, data=file)
                if response.status_code in [200, 201,202]:
                    return "Файл скопирован на диск"
                raise YaDiskAPIError(response.status_code, response.text)
        else:
            raise ValueError('Метод отправки не определен')

    @audit()
    def upload_file_atURL_toDisk(self,path_local:str,url_API: str, path_DISK:str, NetURL: str):
        """
        Сохраняет файл на Яндекс.Диск по внешнему URL без загрузки на локальный компьютер.

        Args:
            url_API (str): API-эндпоинт сохранения файла по URL
                       (например: '/v1/disk/resources/upload').
            path_DISK (str): Путь и имя файла на Яндекс.Диске.
            NetURL (str): Внешний URL файла.

        Returns:
            str: Сообщение об успешном сохранении файла.

        Raises:
            YaDiskAPIError: При ошибке ответа API.
        """
        params = {'path':path_DISK, 'overwrite':False, 'url':NetURL}
        self.check_url_PUT(url_API,params)
        return "Файл сохранен на Яндекс диске"

