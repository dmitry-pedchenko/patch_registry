# Модуль для определения переменных
# Переменные для прав достпуа (<уровень>,<описание>)
FORBIDDEN_JSON = {'status':403,'result':'FORBIDDEN','message':'Access is denied'}

class READ:
    level = 1
    name = 'Чтение'


class FORBIDDEN:
    level = 0
    name = 'Запрещено'
