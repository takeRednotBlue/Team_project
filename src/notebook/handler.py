from prettytable import PrettyTable


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
    if len(note) > 120:
        print('Нотатка не може бути більше 120 символів')
        return

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
        table = PrettyTable(['Name', 'Tags', 'Note'])

        for note in list_of_notes:
            note_tags = ', '.join(note.tags)
            table.add_row([note.name, note_tags, note.text])

        print(table)

    else:
        print('Книга нотатків порожня')

def delete(book, _, note):
    book.delete(note)
    print(f'"{note.name}" - успішно видалено')

def change(book, new_value, note):
    if len(new_value) > 120:
        print('Нотатка не може бути більше 120 символів')
        return
    
    if new_value:
        book.change(new_value, note)
        print(f'нотатка "{note.text}" змінена на "{new_value}"')

    else:
        print('Нотатка не може бути порожньою')

def cont(*_):
    pass

def close(*_):
    return 'close', '_', '_' 

def help(*_):
    print(HELP_TABLE)

def tags(book, new_tags, note):
    if new_tags:
        new_tags = new_tags.split(' ')
        book.change_tag(new_tags, note)
        print(f'Теги {new_tags} були додані до "{note.name}"')
    else:
        print('Не можна додавати порожні теги')


def search(book, value):
    result = book.search(value)

    table = PrettyTable(['Назва', 'Теги', 'Нотатка'])
    for note in result:
        note_tags = ', '.join(note.tags)
        table.add_row([note.name, note_tags, note.text])
    
    print(table) 

    if not result:
        print('Нічого не знайдено')

    elif len(result) == 1:

        input_2 = ''
        while not input_2.startswith(('delete', 'change', 'tags', 'cont', 'close')) :
            input_2 = input(f'{HELP_NOTE_TABLE}\n: ')   

            if not input_2.startswith(('delete', 'change', 'tags', 'cont', 'close')):
                print('Невірна команда, оберіть команду з списку:')

        if input_2 == 'close':
            return 'close', '_', '_'
        
        command, value = parser(input_2)
        return command, value, note 
        
    else:
        choose_note_name = input('Щоб працювати з нотаткою, терба обрати одну\nНапишіть назву нотатки\n: ')

        while choose_note_name not in [note.name for note in result] and choose_note_name != 'close':

            print(table)
            choose_note_name = input('Щоб працювати з нотаткою, терба вибрати одну\nНапишіть назву нотатки\n: ')

        if choose_note_name == 'close':
            return 'close', '_', '_'
        
        
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

HELP_TABLE = PrettyTable(['Команди', 'Пояснення'])
HELP_TABLE.add_row(['add <назва нотатки> <текс нотатки>', 'створити нову нотатку',], divider=True)
HELP_TABLE.add_row(['show <date|alp|size>', "вивести всі нотатки, сортувати за датою|алфавітом|розміром (не обов'язково)"], divider=True)
HELP_TABLE.add_row(['search <тег/текст нотатки>', 'пошук нотатки'], divider=True)
HELP_TABLE.add_row(['close', 'завершити роботу',], divider=True)

HELP_NOTE_TABLE = PrettyTable(['Команда', 'Пояснення']) 
HELP_NOTE_TABLE.add_row(['delete', 'видалити'], divider=True)
HELP_NOTE_TABLE.add_row(['change <новий текст>', 'змінити нотатку'], divider=True)
HELP_NOTE_TABLE.add_row(['tags <нові теги>', 'змінити теги'], divider=True)
HELP_NOTE_TABLE.add_row(['cont', 'пропустити'], divider=True)
HELP_NOTE_TABLE.add_row(['close', 'Завершити роботу'], divider=True)
