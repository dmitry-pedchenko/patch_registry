# Модуль для работы с базой SFTP
# Django имеет доступ к таблицам SFTP
# TODO: Реализовать сбор и обработку логов, создание пользователей, добавление и удаление прав пользователям
import os
import hashlib
import MySQLdb as mc
from pytz import timezone
from datetime import datetime
from traceback import format_exc
from user_logs.models import LogEntry
from django.contrib.auth.models import User
from main.models import PatchMeta, Patch

def mysql_connector(query,return_data=False,
                    host=os.environ.get('MYSQL_HOST'),
                    port=int(os.environ.get('MYSQL_PORT')),
                    user=os.environ.get('MYSQL_USERNAME'),
                    passwd=os.environ.get('MYSQL_PASSWORD'),
                    db=os.environ.get('MYSQL_DBAUTH_NAME')):
    # Функция для соединения с базой данных SFTP
    result = None
    try:
        connection = mc.connect(host=host,port=port,user=user,passwd=passwd,db=db)
        cursor = connection.cursor()
        cursor.execute(query)
        if return_data:
            result = cursor.fetchall()
        connection.commit()

        connection.close()
    except:
        print(format_exc())
    return result


class LogCollector():
    # Класс для сбора и сравнения логов из SFTP
    # TODO: Пока предполагается полное сравнение всего журнала - это очень неэффективно. Нужно как минимум реализовать метку времени и сравнивать в ее пределах
    pass


class SftpUser():
    # Класс релизующий интерфейс django user -> sftp user
    # TODO: Возможно стоит реализовать обратную связь? sftp -> django
    def __init__(self,username,password,ssh_key=None):
        self.username = username
        self.password = password
        self.ssh_key = ssh_key

    def _get_last_uid(self):
        # Возвращает максимальный UID в таблице пользователей
        raw = mysql_connector('SELECT MAX(uid) FROM users',return_data=True)
        return raw and len(raw) and raw[0] and len(raw[0]) and raw[0][0]

    def _get_uid(self):
        # Возвращает допустимый UID для нового пользователя
        uid = self._get_last_uid()
        if uid is None or not int(uid):
            uid = 5500
        else:
            uid = int(uid) + 1
        self.uid = uid
        return self.uid

    def create(self):
        # Создает нового пользователя на SFTP
        uid = self._get_uid()
        passwd_hash = hashlib.md5(self.password.encode('utf-8')).hexdigest()
        try:
            template = "INSERT INTO users (username,password,uid,gid,homedir,shell) VALUES ('{name}','{password}',{uid},{uid},'{home}','{shell}')"
            mysql_connector(template.format(name=self.username, password=passwd_hash,uid=uid,home='/home/{}'.format(self.username),shell='/bin/sh'))
        except:
            print(format_exc())
            return False
        return True


class SftpLogsArray():
    # Класс релизующий интерфейс sftp logs -> Django logentry
    # TODO: Почти уверен, что можно сделать через тригеры в базе данных, но не работает.
    def __init__(self, date_time_from_db:datetime):
        self.start_search = date_time_from_db
        self.template = "SELECT * FROM {table_name} WHERE UNIX_TIMESTAMP(time) > {start_search}"

    def create_from_logs():
        logs_list = LogEntry.objects.filter(source='SFTP').order_by('-date')
        start_search = datetime(1970, 1, 1) if not logs_list or not len(logs_list) else logs_list[0].date
        return SftpLogsArray(start_search)

    def _get_log(self, table_name):
        result = []
        try:
            result = mysql_connector(self.template.format(table_name=table_name,start_search=str(self.start_search.timestamp())),
                            return_data=True)
        except:
            print(format_exc())
        return result

    def _get_patch_from_name(self, name):
        name = os.path.dirname(name).split(sep='/')[-1]
        patch = None
        try:
            patch = PatchMeta.objects.get(meta_value=name,meta_key='eng_name').patch
        except:
            try:
                patch = Patch.objects.get(name=name)
            except:
                pass
        return patch


    def get(self):
        file_log = self._get_log('history')
        # Получение логов об операциях с файлами
        for log_entry in file_log:
            try:
                db_id, file_path, action_bytes, user_name, date_time, action_name = log_entry
                patch = self._get_patch_from_name(file_path)
                date_time = date_time.replace(tzinfo=timezone('UTC'))
                kwargs = {}
                if patch: kwargs['patch'] = patch
                if user_name: kwargs['user'] = User.objects.get(username=user_name)
                LogEntry.objects.add_entry(date=date_time,type='DWLOAD',source='SFTP',level=2,
                                           message='User download file.', **kwargs)

            except Exception as e:
                print(format_exc())
                LogEntry.objects.add_entry(type='ERROR',source='CODE',level=0,message=str(e))
                LogEntry.objects.add_entry(type='ERROR', source='SFTP', level=0, message='Can not get logs from SFTP.')
        error_log = self._get_log('error_log')
        # Получение логов об ошибках
        for log_entry in error_log:
            try:
                db_id, user_name, date_time, file_path, status_code, command, action_name = log_entry
                date_time = date_time.replace(tzinfo=timezone('UTC'))
                kwargs = {}
                patch = self._get_patch_from_name(file_path)
                if patch: kwargs['patch'] = patch
                if user_name: kwargs['user'] = User.objects.get(username=user_name)
                LogEntry.objects.add_entry(date=date_time, type='ERROR', source='SFTP', level=0,
                                           message='Error in SFTP. Code is: "{}". Command is: "{}". Action is: "{}"'.format(
                                               str(status_code), str(command), str(action_name)
                                           ), **kwargs)
            except Exception as e:
                print(format_exc())
                LogEntry.objects.add_entry(type='ERROR',source='CODE',level=0,message=str(e))
                LogEntry.objects.add_entry(type='ERROR', source='SFTP', level=0, message='Can not get logs from SFTP.')
        login_log = self._get_log('login_log')
        # Получение логов о входах-выходах
        for log_entry in login_log:
            try:
                db_id, user_name, date_time, action_name = log_entry
                date_time = date_time.replace(tzinfo=timezone('UTC'))
                if user_name:
                    user =  User.objects.get(username=user_name)
                    action_type = 'LOGIN' if action_name.lower() == 'login' else 'LOGOUT'
                    message = 'Login Successfully.' if action_name.lower() == 'login' else 'Logout Successfully.'
                    LogEntry.objects.add_entry(date=date_time, type=action_type, source='SFTP', level=2, user=user,
                                               message=message)
                else:
                    action_type = 'LOGIN' if action_name.lower() == 'login' else 'LOGOUT'
                    LogEntry.objects.add_entry(date=date_time, type=action_type, source='SFTP', level=1,
                                               message='Unknown user {}'.format(action_type))
            except Exception as e:
                print(format_exc())
                LogEntry.objects.add_entry(type='ERROR',source='CODE',level=0, message=str(e))
                LogEntry.objects.add_entry(type='ERROR', source='SFTP', level=0, message='Can not get logs from SFTP.')
        return {'file_log': file_log, 'error_log': error_log, 'login_log': login_log}

