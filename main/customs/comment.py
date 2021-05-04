# Модуль для объекта отвечающего за создание комментариев
from traceback import format_exc
from customs.answerer import Answerer
from main.models import PatchComment

class Comment(Answerer):
    def __init__(self,*args,**kwargs):
        self.comment = ''

        self.form = kwargs.pop('form', None)
        self.patch = kwargs.pop('patch', None)
        super(Comment, self).__init__(*args, **kwargs)

    def preparation(self):
        # Подготовка и анализ запроса для последующей записи
        name, version = None, None
        if not self.form:
            self.set_status(500,'failed','Не получены данные из формы.')
            return None

        if not self.request:
            self.set_status(500,'failed','Не получено тело запроса.')
            return None

        if not hasattr(self.form, 'cleaned_data'):
            self.set_status(500, 'failed', 'Не найден объект с данными в форме.')
            return None
        self.comment = self.form.cleaned_data['comment']
        return True

    def create(self):
        PatchComment.objects.create(user=self.request.user, patch=self.patch, comment=self.comment)
        self.set_status(200, 'success', 'Комментарий успешно добавлен.')
        return True

    def processing(self):
        # Обработка создания патча
        for func in (self.preparation, self.create):
            try:
                result = func()
                if not result: break
            except:
                self.set_status(500, 'error', 'Ошибка при обработке.')
                print(format_exc())
                break