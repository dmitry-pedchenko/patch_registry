# Модуль содержащий класс для записи лога
from user_logs.models import LogEntry as ModelLogEntry

class LogEntry():
    # Класс отвечающий за запись логов
    def __init__(self):
        self.type = None
        self.level = 2
        self.source = None
        self.message = ''

        self.user = None
        self.patch = None

    def from_args(*args):
        # Создать экземпляр из аргументов
        try:
            t,l,s,m,*over = args
            instance = LogEntry()
            instance.type = t
            instance.level = l
            instance.source = s
            instance.message = m
            return instance
        except:
            return None

    def from_kwargs(**kwargs):
        # Создать экземпляр из именованных аргументов
        try:
            instance = LogEntry()
            instance.type = kwargs.get('type') or None
            instance.level = kwargs.get('level') or 2
            instance.source = kwargs.get('source') or None
            instance.message = kwargs.get('message') or ''
            return instance
        except:
            return None

    def save(self):
        # Создать запись в базе данных
        kwargs = {}
        for key in ['type','source','user','patch','level','message']:
            kwargs[key] = getattr(self,key)
        ModelLogEntry.objects.add_entry(**kwargs)