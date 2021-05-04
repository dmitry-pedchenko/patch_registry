# Модуль содержащий универсальный декоратор для обработки ошибок
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User


def responce_handler(action,*args_v,group=None,return_page=None, uid_class=None, uid_field=None,
                     permission_level=1, permission_field=None, return_json=False, **kwargs_v):
    '''
    Декоратор для проверки прав доступа
    :param args_v:
    :param action:           Принимает число, определяет какую ситуацию надо обрабатывать
    :param group:            Принимает строку, имя группы, на принадлежность к которой надо проверить пользователя
    :param return_page:      Принимает сгенерированную страницу, которую нужно вернуть в случае ошибки
    :param uid_class:        Принимает класс-модель, проверят права в ней дополнительно по uid
    :param uid_field:        Принимает строку, определяет поле для поиска в класс-модели
    :param permission_field: Принимает строку, определяет поле для поиска в класс-доступа
    :param permission_level: Принимает число, минимальный уровень доступа на объект для предоставления прав
    :param return_json:      Флаг, если задан возвращает json
    :param kwargs_v:
    :return:
    '''
    def internal(func):
        def wrapper(*args,**kwargs):
            info = kwargs.get('info',{})
            kwargs['info'] = info
            kwargs['group'] = group
            kwargs['uid_class'] = uid_class
            kwargs['uid_field'] = uid_field
            kwargs['return_page'] = return_page
            kwargs['return_json'] = return_json
            kwargs['permission_level'] = permission_level
            kwargs['permission_field'] = permission_field

            request = get_request(*args)
            if not bool(request):
                raise RuntimeError('Critical error. No request found.')
            if not ACTIONS.get(action):
                raise RuntimeError('Critical error. Undefined action.')

            error = ACTIONS[action](*args,**kwargs)
            if error: return error

            result = func(*args,**kwargs)
            return result
        return wrapper
    return internal


def user_in_group(username, group):
    # Проверяет находится ли пользователь в группе или нет
    return bool(User.objects.filter(groups__name=group, username=username))


def get_request(*args):
    # Получаем request из args
    requests = [arg for arg in args if hasattr(arg, 'scheme')
                and hasattr(arg, 'path')
                and hasattr(arg, 'headers')]
    return (len(requests) and requests[0])


def check_action(action,info):
    if info.get('actions') and info['actions'].get(action):
        return True
    else:
        return False


def set_action(action,info):
    if not info.get('actions'):
        info['actions'] = {}
    info['actions'][action] = True


## Actions
def action_901(*args,**kwargs):
    # Запись информации об аутентификации пользователя
    info = kwargs.get('info',{})
    if check_action(901,info): return None
    group = kwargs.get('group')
    request = get_request(*args)

    info['is_authenticated'] = request.user.is_authenticated
    info['is_in_gruop'] = user_in_group(request.user.username,group)
    set_action(901,info)

def action_902(*args,**kwargs):
    # Получение инстанса объекта
    uid = kwargs.get('uid')
    info = kwargs.get('info', {})
    if check_action(902, info): return None
    uid_class = kwargs.get('uid_class')
    uid_field = kwargs.get('uid_field') or 'uid'

    instance = None
    try:
        instance = uid_class.objects.get(**{uid_field:uid})
    except:
        pass
    info['uid_instance'] = instance
    set_action(902, info)


def action_903(*args,**kwargs):
    # Получение инстанса с правами на объект
    info = kwargs.get('info', {})
    if check_action(903, info): return None
    request = get_request(*args)

    instance = info.get('uid_instance')
    permission = None
    permission_field = kwargs.get('permission_field') or 'uid'
    try:
        permission = instance.permissions_class.objects.get(user=request.user,**{permission_field:instance})
    except:
        pass
    info['permission_instance'] = permission
    set_action(903, info)


def action_904(*args,**kwargs):
    # Проверка пользователя для конкретного объекта
    info = kwargs.get('info', {})
    if check_action(904, info): return None
    permission_level = kwargs.get('permission_level')

    instance = info.get('uid_instance')
    permission = info.get('permission_instance')
    set_action(904, info)
    if instance and permission and int(permission.level) >= permission_level:
        info['is_permited'] = True
        return True
    return False


def action_403(*args,**kwargs):
    # Обработчик прав доступа
    info = kwargs.get('info', {})
    request = get_request(*args)
    return_page = kwargs.get('return_page')
    return_json = kwargs.get('return_json')
    action_901(*args, **kwargs)
    if not info.get('is_authenticated'):
        if return_json: return JsonResponse(return_json)
        return render(request, return_page)
    if not info.get('is_in_gruop'):
        action_902(*args,**kwargs)
        action_903(*args, **kwargs)
        if action_904(*args, **kwargs):
            # Пользователь прошел проверку на конкретный объект
            pass
        else:
            if return_json: return JsonResponse(return_json)
            return render(request, return_page)
    return None


def action_404(*args,**kwargs):
    # Обработчик существования страницы
    uid = kwargs.get('uid')
    info = kwargs.get('info', {})
    request = get_request(*args)
    return_page = kwargs.get('return_page')
    return_json = kwargs.get('return_json')
    if not uid:
        if return_json: return JsonResponse(return_json)
        return render(request, return_page)

    if info.get('uid_instance'):
        # Объект существует
        pass
    else:
        action_902(*args,**kwargs)
        if info.get('uid_instance'):
            # Объект существует
            pass
        else:
            if return_json: return JsonResponse(return_json)
            return render(request, return_page)
    return None

ACTIONS = {403: action_403,
           404: action_404,
           901: action_901,
           902: action_902,
           903: action_903,
           904: action_904,}