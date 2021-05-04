# Модуль для генератора сообщений

class Message():
    def __init__(self,status,internal_message,**kwargs):
        self.kwargs = kwargs
        self.status = int(status)
        self.message = internal_message

        self._find_status()
        self._set_opts()

    def _find_status(self):
        if self.status == 500:
            self.message['status'] = 500
            self.message['result'] = 'failed'

        if self.status == 204:
            self.message['status'] = 204
            self.message['result'] = 'success'

        if self.status == 200:
            self.message['status'] = 200
            self.message['result'] = 'success'

    def _set_opts(self):
        [ self.message.update({kwarg:self.kwargs[kwarg]}) for kwarg in self.kwargs]
