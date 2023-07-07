def input_error(func):
    def wraper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            print('Відсутній аргумент.')
    return wraper
        