class TextFile:

    def __init__ (self,filename):
        self.filename = filename
        self.lines = []
    # читаем файл - открываем, считаем строки, добавляем в список
    def read(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line= line.strip()
                self.lines.append(line)
    # считаем сколько строк в спске
    def line_count(self):
        return len(self.lines)
    # возвращаем заполненный списов
    def get_lines(self):
        return self.lines

class FileMerger:

    def __init__(self):
        self.files = []
    # добавляем файлы в список
    def add_file(self, text_file):
        self.files.append(text_file)
    # сортируем их по длине
    def sort_by_line_count(self):
        self.files.sort(key=lambda f: f.line_count())
    # записываем в общий файл
    def write_to_file(self, output_filename):
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
