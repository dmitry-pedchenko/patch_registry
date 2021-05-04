from datetime import datetime, timedelta
from django.contrib.auth.models import User
from publics.models import CustomFile as ModelCustomFile
from traceback import format_exc


class CustomFile():
    def __init__(self, *args, **kwargs):
        self.file = None

        self.form = kwargs.get('form')
        self.request = kwargs.get('request')
        self.message = kwargs.get('message')

    def set_status(self, code, state, messge):
        self.message['status'] = int(code)
        self.message['result'] = state
        self.message['message'] = messge

    def preparation(self):
        if not self.form:
            self.set_status(500,'failed','Не получены данные из формы.')
            return None

        if not self.request:
            self.set_status(500,'failed','Не получено тело запроса.')
            return None

        if not hasattr(self.form, 'cleaned_data'):
            self.set_status(500, 'failed', 'Не найден объект с данными в форме.')
            return None

        if not self.request.FILES.get('file'):
            self.set_status(500, 'failed', 'В запросе не найден файл.')
            return None

        return True

    def create(self):
        self.file = ModelCustomFile.objects.add_file(user=self.request.user,
                                                     filename=self.request.FILES['file'].name,
                                                     description=self.form.cleaned_data.get('description'))

        if not self.file:
            self.set_status(500, 'failed', 'Не удалось создать запись.')
            return None

        if self.file.upload_handler(self.request.FILES['file']):
            self.set_status(500, 'failed', 'Не удалось загрузить файл.')
            self.file.delete()
            return None

        self.set_status(200, 'success', 'Файл успешно загружен.')
        self.file.save()
        return True

    def processing(self):
        # Обработка создания файла
        for func in (self.preparation,self.create):
            try:
                result = func()
                if not result: break
            except:
                self.set_status(500, 'error', 'Ошибка при обработке.')
                print(format_exc())
                break


def remove_outdated_files():
    try:
        need_to_remove = ModelCustomFile.objects.filter(date__lte=datetime.now() - timedelta(7))
        [file.delete_handler() for file in need_to_remove]
        return True
    except:
        print(format_exc())
        return False