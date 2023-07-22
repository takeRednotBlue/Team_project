from colorama import init, Fore
import pickle
from pathlib import Path

from utilities import completer_input
from data_storage import DATA_DIRECTORY

from notebook.classes import NoteBook
from notebook.handler import * 

init()


def input_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            
            return func(*args, **kwargs)
        
        except KeyError as key_error:
            print(f"Невірна команда: {key_error}")
            note_book(*args, **kwargs)

        except TypeError as type_error:
            print(f"Цю команду можна використовувати тільки для нотатки\nЩоб обрати нотатку: <search> <тег/текс нотатки>")
            note_book(*args, **kwargs)

    return wrapper


def close(path, note_book):
            
    with open(path, 'wb') as file:
        pickle.dump(note_book, file)

first_start = True
@input_error_handler
def note_book():
    
    try:
        global first_start
        if first_start:
            print()
            print('{:<116}'.format(Fore.BLUE + f'{" "*5}Вас вітає додаток НОТАТКИ 📖'))
            print('{:<116}'.format(Fore.YELLOW + f'{" "*5}Тут ви можете зберігати свої нотатки та керувати ними' + Fore.WHITE))
            print()
            first_start = False

        path = DATA_DIRECTORY / 'notebook_data.bin'
        help()
        with open(path, 'ab+') as file:
            if not file.read(): #empty file (first start)
                
                note_book = NoteBook()
                pickle.dump(note_book, file)

        with open(path, 'rb') as file:
            note_book = pickle.load(file)

        while True:
            string = completer_input('>>> ', COMMAND_INPUT)
            command, value = parser(string)

            if command == 'close':
                close(path, note_book)
                first_start = True
                break

            result = COMMAND_DICT[command](note_book, value)
            with open(path, 'wb') as file:
                pickle.dump(note_book, file)

            if command == 'close':
                close(path, note_book)
                first_start = True
                break
            
            if result:
                menu_command, menu_value, note = result

                while menu_command != 'close':
                    res = COMMAND_DICT[menu_command](note_book, menu_value, note)
                    
                    if res == 'close':
                        with open(path, 'wb') as file:
                            pickle.dump(note_book, file)
                        break

                    menu_command, menu_value, note = COMMAND_DICT[command](note_book, value, search_result=False)

                    with open(path, 'wb') as file:
                        pickle.dump(note_book, file)

    except KeyboardInterrupt:
        print('Будь ласка, користуйся командами для завершення роботи')
        with open(path, 'wb') as file:
            pickle.dump(note_book, file)