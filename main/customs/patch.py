# Модуль для объектов описывающих взаимодействие с патчем
import io
import re
from zipfile import ZipFile
from traceback import format_exc

from django.contrib.auth.models import User

from customs.answerer import Answerer
from main.models import PatchPermissions
from main.models import Patch as ModelPatch
from main.customs.environment import *

class PatchParser():
    # Класс для обработки информации из файла с патчем
    def __init__(self, filestream):
        self.file = io.BytesIO()
        [self.file.write(chunk) for chunk in filestream.chunks()]
        self.stream = ZipFile(self.file, "r")

    def _get_zip_filebody(self, filename):
        bodys = [self.stream.read(name) for name in self.stream.namelist() if filename in name]
        if bodys and len(bodys) == 1:
            return bodys[0]
        return None

    def _convert_body_to_str(self, body:bytes):
        coding_list = ['utf-8', 'cp1251']
        for coding in coding_list:
            try: return body.decode(coding)
            except: pass
        return None

    def parser_name(self):
        # Поиск имени в файлах по паттерну
        array = [{'filename': 'setup.cfg', 'pattern': r'Название\s?=\s?(?P<target>[^\r\n]*)'}]
        for parser in array:
            try:
                stream_body = self._convert_body_to_str(self._get_zip_filebody(parser['filename']))
                if stream_body:
                    targets = re.findall(parser['pattern'],stream_body)
                    if targets and len(targets) == 1: return targets[0], ''
            except:
                pass
        return None, 'Не удалось определить название из содержимого патча.'

    def parser_version(self):
        # Поиск версии в файлах по паттерну
        array = [{'filename': 'setup.cfg', 'pattern': r'Версия\s?=\s?(?P<target>[^\r\n]*)'}]
        for parser in array:
            try:
                stream_body = self._convert_body_to_str(self._get_zip_filebody(parser['filename']))
                if stream_body:
                    targets = re.findall(parser['pattern'],stream_body)
                    if targets and len(targets) == 1: return targets[0], ''
            except:
                pass
        return None, 'Не удалось определить версию из содержимого патча.'


class Patch(Answerer):
    # Класс для обработки информации о патче
    def __init__(self, *args,**kwargs):
        self.zip = None
        self.patch = None
        self.name, self.version = None, None
        self.category, self.subcategory = None, None

        self.form = kwargs.pop('form',None)
        super(Patch,self).__init__(*args,**kwargs)

    def _search_name(self):
        if not self.zip: return None, ''
        return self.zip.parser_name()

    def _search_version(self):
        if not self.zip: return None, ''
        return self.zip.parser_version()

    def preparation(self):
        # Подготовка и анализ патча для последующей записи
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

        if not self.request.FILES.get('file'):
            self.set_status(500, 'failed', 'В запросе не найден файл.')
            return None

        self.zip = PatchParser(self.request.FILES['file'])
        if not self.form.cleaned_data.get('name'):
            name, message = self._search_name()
            if not name:
                self.set_status(500, 'failed', 'Не задано имя. {}'.format(message))
                return None
        self.name = name or self.form.cleaned_data['name']

        if not self.form.cleaned_data.get('version'):
            version, message = self._search_version()
            if not version:
                self.set_status(500, 'failed', 'Не задана версия. {}'.format(message))
                return None
        self.version = version or self.form.cleaned_data['version']

        self.category = self.form.cleaned_data.get('category')
        if self.form.cleaned_data.get('category') == '__NEW':
            if self.form.cleaned_data.get('newcategory'):
                self.category = self.form.cleaned_data.get('newcategory')
            else:
                self.set_status(500, 'failed', 'Не задана категория.')
                return None

        self.subcategory = self.form.cleaned_data.get('subcategory')
        if self.form.cleaned_data.get('subcategory') == '__NEW':
            if self.form.cleaned_data.get('newsubcategory'):
                self.subcategory = self.form.cleaned_data.get('newsubcategory')
            else:
                self.set_status(500, 'failed', 'Не задана подкатегория.')
                return None

        return True

    def create(self):
        # Создание записи о патче и запись патча на диск
        self.patch = ModelPatch.objects.add_patch(   name=self.name,
                                        developer=self.form.cleaned_data.get('developer'),
                                        description=self.form.cleaned_data.get('description'),
                                        filename=self.request.FILES['file'].name,
                                        version=self.version,
                                        category=self.category,
                                        subcategory=self.subcategory
                                     )
        if not self.patch:
            self.set_status(500, 'failed', 'Не удалось создать запись.')
            return None

        if self.patch.upload_patch_handler(self.request.FILES['file']):
            self.set_status(500, 'failed', 'Не удалось загрузить файл.')
            self.patch.delete()
            return None

        self.set_status(200, 'success', 'Патч успешно загружен.')
        self.patch.save()
        return True

    def set_permissions(self):
        # Установка прав доступа на патч
        clients = self.form.cleaned_data.get('clients')
        if not clients:
            self.set_status(201, 'warning', 'Патч успешно загружен, но права доступа не были назначены.')
            return None

        if len(clients) != 1 and ('__ALL' in clients or '__NOONE' in clients):
            self.set_status(201, 'warning', 'Патч успешно загружен, но права доступа были указаны не корректно и не были назначены.')
        elif len(clients) == 1 and '__ALL' in clients:
            for user in User.objects.filter(groups__name='clients'):
                permission_item, created = PatchPermissions.objects.get_or_create(user=user,patch=self.patch)
                permission_item.level = READ.level
                permission_item.save()
            self.set_status(200, 'success', 'Патч успешно загружен. Права установлены.')
        elif len(clients) == 1 and '__NOONE' in clients:
            for user in User.objects.filter(groups__name='clients'):
                permission_item, created = PatchPermissions.objects.get_or_create(user=user,patch=self.patch)
                permission_item.level = FORBIDDEN.level
                permission_item.save()
            self.set_status(200, 'success', 'Патч успешно загружен. Права установлены.')
        else:
            for user in User.objects.filter(groups__name='clients'):
                permission_item, created = PatchPermissions.objects.get_or_create(user=user, patch=self.patch)
                if user.username in clients:
                    permission_item.level = READ.level
                else:
                    permission_item.level = FORBIDDEN.level
                permission_item.save()
            self.set_status(200, 'success', 'Патч успешно загружен. Права установлены.')

        return True

    def processing(self):
        # Обработка создания патча
        for func in (self.preparation,self.create,self.set_permissions):
            try:
                result = func()
                if not result: break
            except:
                self.set_status(500, 'error', 'Ошибка при обработке.')
                print(format_exc())
                break