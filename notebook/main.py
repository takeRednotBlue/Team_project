from pathlib import Path
import pickle
from classes import NoteBook
import handler as hd


def input_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            
            return func(*args, **kwargs)
        
        except KeyError as key_error:
            print(f"Невірна команда: {key_error}")
            main(*args, **kwargs)

        except TypeError as type_error:
            print(f"Цю команду можна використовувати тільки для нотатки\nЩоб обрати нотатку: <search> <тег/текс нотатки>")
            main(*args, **kwargs)

    return wrapper


def close(path, note_book):
            
    with open(path, 'wb') as file:
        pickle.dump(note_book, file)


@input_error_handler
def main(path):
    
    print('<help> - список команд')
    with open(path) as file:
        if not file.read(): #empty file (first start)
            
            with open(path, 'wb') as file:
                note_book = NoteBook()
                pickle.dump(note_book, file)

        with open(path, 'rb') as file:
            note_book = pickle.load(file)

    while True:

        string = input('Enter: ')
        command, value = hd.parser(string)

        if command == 'close':
            close(path, note_book)
            break

        result = hd.COMMAND_DICT[command](note_book, value)
        with open(path, 'wb') as file:
            pickle.dump(note_book, file)

        # Для роботи з вибраною нотаткою 
        if result: 
            new_command, new_value, note = result

            if new_command == 'close':
                close(path, note_book)
                break

            hd.COMMAND_DICT[new_command](note_book, new_value, note)
            with open(path, 'wb') as file:
                pickle.dump(note_book, file)

if __name__ == '__main__':
    path_to_notebook = Path(__file__).parent / 'note_book.txt'
    main(path_to_notebook)