import subprocess
import sys
import shutil


def paged_output(max_lines: int = 5):
    """
    Декоратор для корректного отображения длинного текстового вывода в CLI.

    Если функция возвращает строку:
    - короткий текст выводится обычным print
    - длинный текст открывается через pager (less)

    Пользователь может листать стрелками и выйти клавишей 'q',
    после чего управление возвращается в основной CLI-цикл.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)

                if not result:
                    print("Нечего показывать.")
                    return

                text = str(result)
                lines = text.count("\n") + 1

                # Если вывод короткий — просто печатаем
                if lines <= max_lines:
                    print(text)
                    input("\nНажмите Enter для возврата в меню...")
                    return

                # Проверяем, доступен ли less
                if shutil.which("less"):
                    process = subprocess.Popen(
                        ["less", "-R"],
                        stdin=subprocess.PIPE,
                        text=True
                    )
                    process.communicate(text)
                else:
                    # Fallback, если less отсутствует
                    print(text)
                    input("\nНажмите Enter для возврата в меню...")

            except KeyboardInterrupt:
                print("\nОтображение прервано пользователем.")
                return

        return wrapper

    return decorator
