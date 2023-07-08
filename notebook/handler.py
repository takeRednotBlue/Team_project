
def parser(string: str) -> tuple:
    string = string.strip().casefold()
    words_list = string.split(' ')

    if words_list[0] == 'close':
        return 'close', '_'

    command = words_list[0]
    value = ' '.join(words_list[1:])

    return (command, value)

def add_note_to_book(book, value):
    value = value.split(' ')
    name = value[0]
    note = ' '.join(value[1:])

    # Перевірка назв нотаток (не можна створити дві нотатки з однією назваю)
    cheack_similar = True
    for n in book.data:
        if n.name == name:
            cheack_similar = False

    if note and cheack_similar:
        book.add_note(name, note)
        print(f'Нотатка "{note}" збережена')

    else:
        if not cheack_similar:
            print('Назва нотатки вже зайнята\nadd <назва нотатки> <текст нотатки>')
        else:
            print('Не можна зберегти порожню нотатку\nadd <назва нотатки> <текст нотатки>')


def sort_by_len(note):
    return len(note.text)

def sort_by_date(note):
    return note

def sort_by_alp(note):
    return note.name

def show(book, mode=None):
    list_of_notes = book.show_all()
    
    if mode == 'size':
        list_of_notes.sort(key= sort_by_len)

    if mode == 'alp':
        list_of_notes.sort(key= sort_by_alp)

    if mode == 'date':
        list_of_notes.sort(key= sort_by_date)
    
    if list_of_notes:
        for note in list_of_notes:
            if note.tags:
                print(f'_{note.name}_ теги: {note.tags} нотатка: "{note.text[:20]}"')
            else:
                print(f'_{note.name}_ нотатка: "{note.text[:30]}"')
    else:
        print('Книга нотатків порожня')

def delete(book, _, note):
    book.delete(note)
    print(f'"{note.name}" - успішно видалено')

def change(book, new_value, note):
    book.change(new_value, note)
    print(f'нотатка "{note.text}" змінена на "{new_value}"')

def cont(*_):
    pass

def close(*_):
    return 'close', '_', '_' 

def help(*_):
    print(HELP)

def tags(book, new_tags, note):
    if new_tags:
        new_tags = new_tags.split(' ')
        book.change_tag(new_tags, note)
        print(f'Теги {new_tags} були додані до "{note.name}"')
    else:
        print('Не можна додавати порожні теги')


def search(book, value):
    result = book.search(value)

    for note in result:
        if note.tags:
            print(f'_{note.name}_ теги: {note.tags} нотатка: "{note.text}"')
        else:
            print(f'_{note.name}_ нотатка: "{note.text}"')

    if not result:
        print('Нічого не знайдено')

    elif len(result) == 1:

        input_2 = ''
        while not input_2.startswith(('delete', 'change', 'tags', 'cont', 'close')) :
            input_2 = input(HELP_FOR_NOTE)   

            if not input_2.startswith(('delete', 'change', 'tags', 'cont', 'close')):
                print('Невірна команда, оберіть команду з списку:')

        if input_2 == 'close':
            return 'close', '_', '_'
        
        command, value = parser(input_2)
        return command, value, note 
        
    else:
        choose_note_name = input('Щоб працювати з нотаткою, терба вибрати одну\nНапишіть назву нотатки\n: ')

        while choose_note_name not in [note.name for note in result]:
            for note in result:
                if note.tags:
                    print(f'_{note.name}_ теги: {note.tags} нотатка: "{note.text}"')
                else:
                    print(f'_{note.name}_ нотатка: "{note.text}"')
            choose_note_name = input('Щоб працювати з нотаткою, терба вибрати одну\nНапишіть назву нотатки\n: ')

        search(book, choose_note_name) #рекурсивно викликаємо функцію коли обрали одну нотатку

    


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
add <назва нотатки> <текс нотатки> - створити нову нотатку
show <date|alp|size> - вивести всі нотатки, сортувати за датою|алфавітом|розміром (не обов'язково)
search <тег/текст нотатки> - пошук нотатки
close - завершити роботу
"""

HELP_FOR_NOTE = '''Видалити - delete
Змінити - change <новий текст>
Змінити теги - tags <нові теги>
Пропустити - cont
Завершити роботу - close
: '''