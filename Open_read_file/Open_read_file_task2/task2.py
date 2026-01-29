class TextFile:
    """
    Класс TextFile предназначен для работы с текстовым файлом.

    Хранит:
    - имя файла
    - список строк, считанных из файла
    """

    def __init__ (self,filename):
        """
        Создаёт объект текстового файла.

        :param filename: Имя файла (строка)
        """
        self.filename = filename
        self.lines = []

    def read(self):
        """
        Считывает файл построчно и сохраняет строки в список self.lines.

        - файл открывается в кодировке UTF-8
        - каждая строка очищается от символов переноса строки и пробелов
        """
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line= line.strip()
                self.lines.append(line)

    def line_count(self):
        """
        Возвращает количество строк в файле.

        :return: количество строк (int)
        """
        return len(self.lines)

    def get_lines(self):
        """
        Возвращает список строк файла.

        :return: список строк (list[str])
        """
        return self.lines

class FileMerger:
    """
    Класс FileMerger объединяет несколько текстовых файлов в один.

    Файлы:
    - добавляются как объекты TextFile
    - сортируются по количеству строк
    - записываются в итоговый файл
    """

    def __init__(self):
        """
        Создаёт объект объединителя файлов.
        """
        self.files = []

    def add_file(self, text_file):
        """
        Добавляет текстовый файл в список файлов для объединения.

        :param text_file: Объект класса TextFile
        """
        self.files.append(text_file)

    def sort_by_line_count(self):
        """
        Сортирует файлы по количеству строк (по возрастанию).

        Использует метод line_count() каждого файла.
        """
        self.files.sort(key=lambda f: f.line_count())

    def write_to_file(self, output_filename):
        """
        Записывает объединённые данные в итоговый файл.

        Формат записи:
        - имя файла
        - количество строк
        - содержимое файла построчно

        :param output_filename: Имя итогового файла (строка)
        """
        with open(output_filename, "w", encoding="utf-8") as f:
            for file in self.files:
                f.write(file.filename + "\n")
                f.write(str(file.line_count()) + "\n")

                for line in file.get_lines():
                    f.write(line + "\n")


files = ["1.txt", "2.txt", "3.txt"] # определяем файлы

merger = FileMerger() # создаем объект класса

for name in files:
    tf = TextFile(name) # создаем объект класса по файлам
    tf.read()           # читаем файл
    merger.add_file(tf)

merger.sort_by_line_count()
merger.write_to_file("result.txt")
