import json
from glom import glom, Coalesce
from pathlib import Path




BASE_DIR = Path(__file__).resolve().parent

file_path = BASE_DIR/'newsafr.json'

def read_json(file_path):
    """
    Читает JSON-файл с новостями и возвращает список из 10 самых
    часто встречающихся слов длиной не менее 7 символов.

    Алгоритм работы функции:
    1. Проверяет существование файла по указанному пути.
    2. Загружает JSON-данные из файла.
    3. Извлекает все значения поля 'description' из новостей.
    4. Объединяет тексты описаний в одну строку.
    5. Разбивает текст на отдельные слова.
    6. Подсчитывает частоту слов длиной не менее 7 символов.
    7. Сортирует слова по убыванию частоты.
    8. Возвращает список из 10 наиболее частотных слов.

    :param file_path: Path-объект, указывающий путь к JSON-файлу с новостями
    :return: list[str] — список из 10 самых часто встречающихся слов
    :raises FileNotFoundError: если файл по указанному пути не найден
    """
    if not file_path.exists():
        raise FileNotFoundError('Файл не найден')

    with open(file_path, 'r', encoding="utf-8")as file:
        data = json.load(file)
    news = glom(data, ('rss', 'channel', 'items', ['description']))
    text_news = ','.join(news)

    word_in_text ={}
    for word in text_news.split():
        if len(word) >= 7 and word not in word_in_text:
            word_in_text[word] = 1
        elif len(word) >= 7 and word in word_in_text:
            word_in_text[word] += 1

    word_in_text_sorted=sorted(word_in_text.items(), key=lambda x: x[1],reverse=True)
    top_words =[]
    for i in word_in_text_sorted:
        top_words.append(i[0])

    return top_words[0:10]

print(read_json(file_path))
