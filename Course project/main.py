from cat import CatImage
from yandex import Ya_Disk
from errors import YaDiskAPIError, CatApiError
from decorators import paged_output
import json


def run():
    """
    Точка входа в CLI-приложение.

    Инициализирует объекты API-клиентов (Яндекс.Диск, cataas),
    запрашивает OAuth-токен у пользователя
    и запускает главный цикл взаимодействия.
    """
    #Инициализируем яндекс диск
    token = input("Введите OAuth-токен Яндекс.Диска: ").strip()
    yandex = Ya_Disk(token)

    #Инициализируем котикокартинки
    cat = CatImage()


    main_loop(yandex, cat)

def main_loop(yandex, cat):
    """
    Главный цикл CLI-приложения.

    Отображает меню, принимает пользовательский ввод
    и маршрутизирует выполнение команд.

    Args:
        yandex (Ya_Disk): клиент API Яндекс.Диска
        cat (CatImage): клиент API cataas.com
    """
    while True:
        show_main_menu()
        user_choice = input('Введите выбор: ')
        if user_choice == '0':
            break

        elif user_choice =='1':
            show_disk_files(yandex)


        elif user_choice == '2':
            show_disk_info(yandex)

        elif user_choice == '3':
            create_disk_folder(yandex)

        elif user_choice == '4':
            upload_local_file(yandex)

        elif user_choice == '5':
            get_cat_image(yandex, cat)
        elif user_choice == '6':
            get_disk_files_at_json(yandex)
        else:
            print('Выбран не верный пункт меню')
            continue

def show_main_menu():
    """
    Отображает главное меню CLI.
    """
    print("\n===   ===")
    print("1. Получить список файлов")
    print("2. Получить информацию о дисковом пространстве Яндекс.Диска.")
    print("3. Создать папку на  Яндекс.Диске")
    print("4. Загрузить файл с рабочего места на Яндекс.Диск")
    print("5.  Получить(сохранить) картинку котика")
    print("6.  Сохранить список файлов на Я.Диске в файл ")
    print("0. Выход")

def show_disk_info(yandex: Ya_Disk):
    """
    Docstring для show_disk_info
    Отображает информацию о дисковом пространстве Яндекс.Диска.

    Args:
        yandex (Ya_Disk): клиент API Яндекс.Диска
    """
    try:
        info = yandex.get_resourse("/v1/disk")
        print('\nОбщая информация по диску')
        print(info)

    except YaDiskAPIError as e:
        print("❌ Ошибка Яндекс.Диска")
        print(f"Код: {e.status_code}")
        print(f"Сообщение: {e.message}")

@paged_output()
def show_disk_files(yandex: Ya_Disk):
    """
    Получает и отображает список файлов на Яндекс.Диске.

    Длинный вывод автоматически форматируется
    с использованием pager (less).
    """
    try:
        data = yandex.get_folders_on_ya_disk("/v1/disk/resources/public")
        name_list =[]
        for line in data['items']:
            name_list.append(line['name'])
        return '\n'.join(name_list)

    except YaDiskAPIError as e:
        print("❌ Ошибка Яндекс.Диска")
        print(f"Код: {e.status_code}")
        print(f"Сообщение: {e.message}")

def create_disk_folder(yandex: Ya_Disk):
    """
    Создаёт папку на Яндекс.Диске по пользовательскому вводу.
    """
    path_DISK = input('Введите название(путь) создаваемой папки на Я.Диске: ')
    try:
        info = yandex.new_folder("/v1/disk/resources", path_DISK)
        print(info)

    except YaDiskAPIError as e:
        print("❌ Ошибка Яндекс.Диска")
        print(f"Код: {e.status_code}")
        print(f"Сообщение: {e.message}")

def upload_local_file(yandex: Ya_Disk):
    """
    Загружает локальный файл пользователя на Яндекс.Диск.
    """
    path_DISK = input('Введите полный путь к файлу на Яндекс.Диске: ')
    pathDISK_local = input('Введите путь к локальному файлу: ')
    try:
        info = yandex.upload_file_fromPC_toDisk(pathDISK_local, '/v1/disk/resources/upload', path_DISK)
        print(info)

    except YaDiskAPIError as e:
        print("❌ Ошибка Яндекс.Диска")
        print(f"Код: {e.status_code}")
        print(f"Сообщение: {e.message}")

def get_cat_image(yandex: Ya_Disk, cat: CatImage):
    """
    Получает изображение кота (с текстом или без)
    через API cataas.com и сохраняет его на Яндекс.Диск.
    """
    while True:
        user = input('Вы хотите картинку-1, картинку с текстом-2 (для выхода -0): ')
        if user == '0':
            break
        elif user == '1':
            cat.get_meta_data('/cat')
            url_cat= cat.get_url()
            #сохраняем на Я.Диск
            name_cat = input('Введите путь и имя файла на Яндекс.Диске: ')
            info = yandex.upload_file_atURL_toDisk('/v1/disk/resources/upload',name_cat,url_cat)
            return info
        elif user == '2':
            text = input('Введите текст для картинки: ')
            cat.get_meta_data(f'/cat/says/{text}')
            url_cat= cat.get_url()
            #сохраняем на Я.Диск
            name_cat = input('Введите путь и имя файла на Яндекс.Диске: ')
            info = yandex.upload_file_atURL_toDisk('/v1/disk/resources/upload',name_cat,url_cat)
            return info
        else:
            print("Введено не верное значение")

def get_disk_files_at_json(yandex: Ya_Disk):
    """
    Сохраняет список файлов Яндекс.Диска в JSON-файл.

    Используется для экспорта данных.
    """
    try:
        data = yandex.get_folders_on_ya_disk("/v1/disk/resources/public")
        with open('folders.json', 'w', encoding='utf-8') as f:
            json.dump(data,f, indent=2, ensure_ascii=False)
            print("Файл folders.json успешно сохранён")
    except YaDiskAPIError as e:
        print("❌ Ошибка Яндекс.Диска")
        print(f"Код: {e.status_code}")
        print(f"Сообщение: {e.message}")


if __name__ == "__main__":
    run()

