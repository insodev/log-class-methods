from functools import wraps
from abc import ABC, abstractmethod, ABCMeta


def method_logger(func, store_result=False):
    @wraps(func)
    def decorator(self, *args, **kwargs):
        print((self, func))
        print('\tself.memory before', self.memory)
        result = func(self, *args, **kwargs)
        print('\tself.memory after', self.memory)

        if store_result:
            print('\tresult', result)

        return result

    return decorator


class MemoryLogger(ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):

        print('__new__', mcs, name, bases, namespace, kwargs)

        cls = super().__new__(mcs, name, bases, namespace, **kwargs)

        if '_build' in namespace:
            print(cls._build)
            cls._build = method_logger(cls._build, store_result=True)

        if 'parse' in namespace:
            print(cls.parse)
            cls.parse = method_logger(cls.parse)
        return cls


class BaseComposite(ABC, metaclass=MemoryLogger):
    def __init__(self, memory: dict, params: dict = None):
        self.memory = memory
        self.params = params

    @abstractmethod
    def _build(self) -> dict:
        pass

    @abstractmethod
    def parse(self):
        pass


class FooComposite(BaseComposite):
    def _build(self):
        return {
            'foo': self.memory.get('foo')
        }

    def parse(self):
        self.memory['foo'] = self.params.get('foo')


class BarComposite(FooComposite):
    def _build(self):
        return {
            'bar': self.memory.get('bar')
        }


if __name__ == '__main__':
    _memory = {'foo': 'foo', 'bar': 'bar'}
    _params = {'foo': 'bar'}

    foo = FooComposite(memory=_memory, params=_params)

    foo._build()
    foo.parse()

    bar = BarComposite(memory=_memory, params=_params)

    bar._build()
    bar.parse()
