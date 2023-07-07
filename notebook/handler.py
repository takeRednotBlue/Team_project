
def parser(string: str) -> tuple:
    string = string.strip().casefold()
    words_list = string.split(' ')

    if words_list[0] == 'close':
        return 'close', '_'

    command = words_list[0]
    value = ' '.join(words_list[1:])

    return (command, value)

def add_note_to_book(book, note):
    if note:
        book.add_note(note)
        print(f'Нотатка "{note}" збережена')
    else:
        print('Не можна зберегти порожню нотатку')

def show(book, *_):
    list_of_notes = book.show_all()
    if list_of_notes:
        for note in list_of_notes:
            if note.tags:
                print(f'теги: {note.tags} нотатка: "{note}"')
            else:
                print(f'нотатка: "{note}"')
    else:
        print('Книга нотатків порожня')

def delete(book, _, note):
    book.delete(note)
    print(f'"{note}" - успішно видалено')

def change(book, new_value, note):
    book.change(new_value, note)
    print(f'нотатка "{note}" змінена на "{new_value}"')

def cont(*_):
    pass

def close(*_):
    return 'close', '_', '_' 

def help(*_):
    print(HELP)

def tags(book, new_tags, note):
    if new_tags:
        book.change_tag(new_tags, note)
        print(f'Теги "{new_tags}" були додані до "{note}"')
    else:
        print('Не можна додавати порожні теги')


def search(book, value):
    result = book.search(value)

    for note in result:
        if note.tags:
            print(f'..{value}.. теги: {note.tags} нотатка: "{note}"')
        else:
            print(f'..{value}.. нотатка: "{note}"')

    if not result:
        print('Нічого не знайдено')

    elif len(result) == 1:

        input_2 = ''
        while not input_2.startswith(('delete', 'change', 'tags', 'cont', 'close')) :
            input_2 = input('''Видалити - delete
Змінити - change <новий текст>
Змінити теги - tags <нові теги>
Пропустити - cont
Завершити роботу - close
: ''')      
        command, value = parser(input_2)
        print(command, value)
        return command, value, note 
        
    else:
        print('Щоб працювати з нотаткою, терба вибрати одну\n<search> <тег/текст нотатки>')
    


COMMAND_DICT = {
    'add': add_note_to_book,
    'show': show,
    'search': search,
    'delete': delete,
    'change': change,
    'cont': cont,
    'close': close,
    'help': help,
    'tags': tags
}

HELP = """
Команди:
add <текс нотатки> - створити нову нотатку
show - вивести всі нотатки
search <тег/текст нотатки> - пошук нотатки
close - завершити роботу
"""