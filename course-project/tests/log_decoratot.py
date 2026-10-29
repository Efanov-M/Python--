from datetime import datetime
from errors import YaDiskAPIError, CatApiError

from loggerAPI import LoggerApi



logger = LoggerApi("api_audit_log.csv")
def audit():
    """
    Декоратор аудита API-взаимодействий.

    Назначение:
        Оборачивает методы, выполняющие сетевые запросы (API),
        и формирует структурированную запись аудита для каждого вызова.

    Поведение:
        • При успешном выполнении метода:
            - фиксирует дату и время вызова;
            - фиксирует имя класса и метода;
            - фиксирует статус 'SUCCESS';
            - передаёт запись в приёмник аудита.

        • При возникновении ожидаемой API-ошибки
          (YaDiskAPIError, CatApiError):
            - фиксирует дату и время вызова;
            - фиксирует имя класса и метода;
            - фиксирует статус 'ERROR';
            - сохраняет HTTP-код и сообщение ошибки;
            - передаёт запись в приёмник аудита;
            - повторно выбрасывает исключение.

        • При возникновении любой другой ошибки:
            - аудит не производится;
            - исключение пробрасывается без изменений.

    Особенности:
        • Декоратор не выполняет запись в файл и не знает
          о способе хранения данных.
        • Передача данных осуществляется через функцию
          `get_data_for_write(record)`, выступающую приёмником событий.
        • Декоратор не изменяет контракт оборачиваемых методов
          и возвращает их результат без модификации.
        • Исключения не подавляются.

    Ожидаемый контракт приёмника:
        get_data_for_write(record: list) -> None
            - принимает одну запись аудита;
            - не выбрасывает исключений наружу;
            - не изменяет структуру записи.

    Структура записи аудита:
        [
            datetime,        # время вызова
            class_name,      # имя класса
            method_name,     # имя метода
            status,          # 'SUCCESS' | 'ERROR'
            http_code,       # HTTP-код ошибки или None
            message          # текст ошибки или None
        ]
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            DateTime = datetime.now()
            log_record = []
            log_record.append(DateTime)
            log_record.append(args[0].__class__.__name__)
            log_record.append(func.__name__)
            need_log=False
            try:
                result = func(*args, **kwargs)
                log_record.append('SUCCESS')
                log_record.append(None)
                log_record.append(None)
                need_log=True
                return result
            except (YaDiskAPIError, CatApiError) as e:
                log_record.append('ERROR')
                log_record.append(e.status_code)
                log_record.append(e.message)
                need_log=True
                raise
            except Exception as d:
                need_log=False
                raise
            finally:
                if need_log:
                    logger.get_data_for_write(log_record)
        return wrapper
    return decorator
