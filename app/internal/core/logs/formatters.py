import ast
import json
import logging
import time
import traceback
from datetime import datetime


class ConsoleFormatter(logging.Formatter):
    """
    Форматтер для прокида инфы в консоль 
    """
    COLORS = {
        'DEBUG':    '\033[94m',  # Синий
        'INFO':     '\033[92m',  # Зеленый
        'WARNING':  '\033[93m',  # Желтый
        'ERROR':    '\033[91m',  # Красный
        'CRITICAL': '\033[91m\033[107m',  # Красный на белом
        'RESET':    '\033[0m'    # Сброс
    }

    def format(self, record: logging.LogRecord) -> str:
        log_color = self.COLORS.get(record.levelname, '')
        reset_color = self.COLORS["RESET"]

        msg = record.getMessage()
        msg = msg.replace("{", "").replace("}", "")
        req_id = getattr(record, "req_id", "-")
        formatted_excepiton = self.format_exception(record.exc_info)

        return f"[{datetime.now()}]{log_color} {record.name}:{record.levelname} req_id: {req_id}{reset_color} message: {msg}{log_color}{formatted_excepiton}{reset_color}"

    def format_exception(self, exc_info):
        if not exc_info:
            return ""
        exc_type, exc_value, exc_traceback = exc_info
        exception_string = f"\n{str(exc_type.__name__)} {str(exc_value)}"
        formatted_traceback = "\n" + "".join(traceback.format_tb(exc_traceback, -2))
        return f"{exception_string}{formatted_traceback}"

class JSONFormatter(logging.Formatter):
    """
    Форматтер для json логов
    """
    def format(self, record: logging.LogRecord) -> str:
        msg = record.getMessage()
        # переводит строку msg в словарь, чтобы корректно сохранялось в json
        try:
            msg = ast.literal_eval(msg)
        except (ValueError, SyntaxError):
            pass
        log_data = {
            "ts": int(time.time() * 1000),  # в мсек
            "level": record.levelname.lower(),
            "logger": record.name,
            "req_id": getattr(record, "req_id", "-"),
            "message": msg,
        }
        if hasattr(record, 'exc_info') and record.exc_info:
            exc_type, exc_value, exc_traceback = record.exc_info
            err_data = {
                "err": str(exc_value),
                "class_err": exc_type.__name__,
                "stacktrace": self.format_stacktrace(exc_traceback),
            }
            if isinstance(log_data['message'], dict):
                log_data['message'].update(err_data)
            else:
                log_data['message'] = {"message": log_data['message'], **err_data}
        return json.dumps(log_data, ensure_ascii=False)

    def format_stacktrace(self, exc_traceback):
        return ''.join(traceback.format_tb(exc_traceback)).strip()
