# coding=utf-8

def show_debag_info(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print args, kwargs
        return result
    return wrapper



def proizvedenie(a, b):
    return a * b

proizvedenie = show_debag_info(proizvedenie)

proizvedenie(10, 20)
