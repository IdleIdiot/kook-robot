import time
from datetime import datetime


def record(func):
    """
    decorator method none parameters
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        begin = (datetime.timestamp(datetime.now()))
        func(*args, **kwargs)
        end = int(datetime.timestamp(datetime.now()))
        print("execute time: {}".format(end - begin))

    return wrapper


def hang(delay):
    """
    decorator method more parameters
    :param delay:
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if type(delay) is int and delay > 0:
                time.sleep(delay)
            func(*args, **kwargs)

        return wrapper

    return decorator


# I think it's not good from there. You can use it by @Fly @Run(5)
class Fly:
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        """
        class decorator
        :param args:
        :param kwargs:
        :return:
        """
        print("I think I can fly!")
        time.sleep(2)
        self._func(*args, **kwargs)


class Run:
    def __init__(self, distance):
        self._distance = distance

    def __call__(self, *args, **kwargs):
        """
        class decorator with parameters.
        :param args:
        :param kwargs:
        :return:
        """
        def wrapper(func):
            print("I can run {} kilometers.".format(self._distance))
            func(*args, **kwargs)
        return wrapper
