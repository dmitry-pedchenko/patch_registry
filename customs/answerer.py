class Answerer():
    # Базовый класс для классов возвращающих сообщения в виде словаря
    def __init__(self,*args,**kwargs):
        self.request = kwargs.get('request')
        self.message = kwargs.get('message') or {}

    def set_status(self, code, state, messge):
        self.message['status'] = int(code)
        self.message['result'] = state
        self.message['message'] = messge