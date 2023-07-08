import sys

def input_error(func):
    def wraper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            print('Відсутній аргумент.')
    return wraper

def kb_interrupt_error(func):
    def wraper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('Будь ласка, користуйся командами для завершення роботи боту.')
            sys.exit()
    return wraper