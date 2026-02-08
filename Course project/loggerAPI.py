from pathlib import Path
import csv


from pathlib import Path
import csv


class LoggerApi:
    """
    Класс для хранения и записи аудита API-взаимодействий в CSV-файл.
    """

    HEADER = [
        "datetime",
        "class",
        "method",
        "status",
        "http_code",
        "message"
    ]

    def __init__(self, log_path: str) -> None:
        self.log_path = Path(log_path)

    def check_log(self) -> bool:
        """
        Проверяет существование файла лога.
        """
        return self.log_path.exists()

    def new_log(self) -> None:
        """
        Создаёт новый CSV-файл лога и записывает заголовок.
        """
        with open(self.log_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(self.HEADER)

    def get_data_for_write(self, data: list) -> None:
        """
        Принимает одну запись аудита и записывает её в лог.
        """
        if not self.check_log():
            self.new_log()

        self.write_log(data)

    def write_log(self, data: list) -> None:
        """
        Добавляет одну строку в CSV-файл.
        """
        with open(self.log_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def open_log(self) -> list:
        """
        Возвращает содержимое CSV-файла в виде списка строк.
        """
        if not self.check_log():
            return []

        with open(self.log_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            return list(reader)
