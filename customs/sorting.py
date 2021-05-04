# Модуль определяющий методы сортировки контента


class Sorting():
    def __init__(self, model_class):
        self.model_class = model_class
        self.args = []
        self.kwargs = {}

    def create_from_args(model_class, direction:bool, field):
        cls = Sorting(model_class)
        direction = '' if direction else '-'
        cls.set_arg('{}{}'.format(direction,field))
        return cls

    def set_arg(self,arg):
        self.args.append(arg)

    def set_kwarg(self,key,value):
        self.kwargs.update({key:value})

    def sort(self, *args,**kwargs):
        [self.set_arg(arg) for arg in args]
        [self.set_kwarg(key,value) for key,value in kwargs.items()]
        return self.model_class.objects.all().order_by(*self.args)