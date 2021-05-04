# Модуль содержащий универсальный класс для возвращения ответа + дополнительные действия
from traceback import format_exc
from user_logs.customs.log_entry import LogEntry

class ResponceAbs():
    # Класс отвечающий за возвращение ответа пользователю
    pass


class LoggingAbs():
    # Класс отвечающий за за запись логов
    def entry(*args,user=None,patch=None,**kwargs):
        '''
        Создает лог-запись в базе данных
        :param args: аргументы для создания записи
        :param patch: опционально, объект к которому относится запись
        :param user: опционально, пользователь к которому относится запись
        :param kwargs: именованные аргументы для создания записи
        :return: bool
        '''
        instance = None
        try:
            if len(args):
                instance = LogEntry.from_args(*args)
            elif len(**kwargs):
                instance = LogEntry.from_kwargs(**kwargs)
            else:
                return False

            if user:
                instance.user = user
            if patch:
                instance.patch = patch

            instance.save()
        except:
            print(format_exc())
            return False
        return True