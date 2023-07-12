from prettytable import PrettyTable
from ..utilities import completer_input

def parser(string: str) -> tuple:
    string = string.strip().casefold()
    words_list = string.split(' ')

    if words_list[0] in END_COMMANDS:
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
        new_note = book.add_note(name, note)
        
        answer = input('Бажаєте додати теги до цієї нотатки? (Y/n): ')
        while answer not in ['y', 'Y', 'n', 'N']:
            answer = input('Введіть так або ні (Y/n): ')

        if answer in ['y', 'Y']:

            tags = input('Введіть теги через пробіл:  ')
            if tags:
                tags = tags.split(' ')
                tags = [t for t in tags if t] # Видаляємо пусті теги
                new_note.add_tags(tags)
            else:
                print('Не можна зберегти порожні теги')

        print(f'Нотатка "{new_note.name}" збережена, <help> - список команд')
        

    else:
        if not cheack_similar:
            print('Назва нотатки вже зайнята\nЩоб створити нову нотатку: add <назва нотатки (без пробілів)> <текст нотатки>')
        else:
            print('Не можна зберегти порожню нотатку\nЩоб створити нову нотатку: add <назва нотатки (без пробілів)> <текст нотатки>')


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
        list_of_notes.sort(key= sort_by_date, reverse= True)
    
    if mode not in ['date', 'alp', 'size'] and mode:
        print('Невірна команда')
        print('Сортувати можна за такими параметрами: <date|alp|size>\ndate - сортувати за датою \nalp - сортувати за алфавітом \nsize - сортувати за розміром')
        print('show <date|size|alp>')
    else:
        if list_of_notes:
            table = PrettyTable(['Назва', 'Теги', 'Нотатка'])

            for note in list_of_notes:
                if len(note.text) > 100: # Для великих нотаток кожні 100 символів додаємо \n (для гарного виводу)
                    note_tags = ', '.join(note.tags)
                    
                    text = ''
                    counter = 0
                    for i in note.text:
                        text += i
                        counter += 1
                        if not counter % 100:
                            text += '\n' 

                        if len(text) > 296:
                            text += '... '
                            break

                    table.add_row([note.name, note_tags, text], divider=True)        

                else:
                    note_tags = ', '.join(note.tags)
                    table.add_row([note.name, note_tags, note.text], divider=True)

            print(table)
            print('Щоб працювати з нотаткою треба обрати одну: search <назва нотатки|теги>, help - список команд')
        else:
            print('Книга нотатків порожня')

def delete(book, _, note):
    book.delete(note)
    print(f'"{note.name}" - успішно видалено')
    print('Меню редагування нотатки закрито')
    return 'close'

def change(book, new_value, note):
    
    if new_value:
        note.change_note(new_value)
        print(f'Нотатка "{note.name}" змінена на "{new_value}"')
        # search(book, note.name)
        
    
    else:
        print('Нотатка не може бути порожньою')
        

def cont(*_):
    pass

def close(*_):
    return 'close', '_', '_' 

def help(*_):
    print(HELP_TABLE)

def tags(book, command, note):
    
    if command not in ['change', 'clean', 'add']:
        return 'search', note.name

    else:
        if command == 'clean':
            if note.tags:
                print(f'Tеги {note.tags} успішно видалені')
                note.clean_tag()
                return 'search', note.name
            else:
                print(f'"{note.name}" не має тегів')
                return 'search', note.name

        elif command == 'add':
            new_tags = input('Щоб додати, введіть теги через пробіл, (натисніть Enter, щоб відмінити)\n>>> ')
            new_tags = new_tags.split(' ')
            new_tags = [t for t in new_tags if t] # Видаляє пусті теги ("")
            if new_tags:
                note.add_tags(new_tags)
                print(f'Теги {set(new_tags)} додані до "{note.name}"')
                return 'search', note.name
            else:
                print('Меню редагування нотатки закрито')
                print(HELP_TABLE)
        
        elif command == 'change':
            new_tags = input('Щоб змінити, введіть теги через пробіл, (натисніть Enter, щоб відмінити)\n>>> ')
            new_tags = new_tags.split(' ')
            new_tags = [t for t in new_tags if t] # Видаляє пусті теги ("")
            if new_tags:
                tags = note.tags
                if tags:
                    print(f'Теги {note.tags} змінені на {set(new_tags)}')

                else:
                    print(f'Теги {set(new_tags)} додані до {note.name}')
                    
                note.change_tags(new_tags)
                return 'search', note.name
            else:
                print('Меню редагування нотатки закрито')
                print(HELP_TABLE)

def search(book, value, search_result= True):
    result = book.search(value)

    table = PrettyTable(['Назва', 'Теги', 'Нотатка'])
    for note in result:
        if len(note.text) > 100: # Для великих нотаток кожні 100 символів додаємо \n (для гарного виводу)
            note_tags = ', '.join(note.tags)
            
            text = ''
            counter = 0
            for i in note.text:
                text += i
                counter += 1
                if not counter % 100:
                    text += '\n'

                if len(text) > 296:
                            text += '... '
                            break
                 
            table.add_row([note.name, note_tags, text], divider=True)
        else:
            note_tags = ', '.join(note.tags)
            table.add_row([note.name, note_tags, note.text], divider=True)

    if not result:
        print('Нічого не знайдено, щоб знайти нотатку: search <назва|тег нотатки>')

    elif len(result) == 1:

        if search_result:
            print('Результат пошуку')
            print(table)
        input_2 = ''
        while not input_2.startswith(('change')) and input_2 not in ['delete', 'close', 'tags add', 'tags change', 'tags clean']:
            print('\t\t\t\tМеню нотатки')
            input_2 = completer_input(f'{HELP_NOTE_TABLE}\n>>> (editnote) ', COMMAND_INPUT_MENU).casefold().strip()

            if input_2.startswith(('show', 'search', 'add', 'help')):
                print(f'Команда "{input_2}" не доступна в меню нотатки')
            else:
                if not input_2.startswith(('change')) and input_2 not in ['delete', 'close', 'tags add', 'tags change', 'tags clean']:
                    print(f'Невірна команда "{input_2}", оберіть команду з списку:')

        if input_2 == 'close':
            print('Меню редагування нотатки закрито')
            print('<help> - список команд')
            return 'close', '_', '_'
        
        else:
            command, value = parser(input_2)
            return command, value, note
        
    else:
        print('Результат пошуку')
        print(table)
        choose_note_name = input('Щоб працювати з нотаткою, терба обрати одну\nБудь ласка, укажіть повну назву необхідної нотатки (cont - відмінити) \n>>> ')

        while choose_note_name not in [note.name for note in result] and choose_note_name != 'close' and choose_note_name != 'cont':
            print('Результат пошуку')
            print(table)
            choose_note_name = input('Щоб працювати з нотаткою, терба обрати одну\nБудь ласка, укажіть повну назву необхідної нотатки (cont - відмінити) \n>>> ')

        if choose_note_name == 'close':
            return 'close', '_', '_'
        
        elif choose_note_name == 'cont':
            print('Меню вибору нотатки закрито')
            print('<help> - список команд')
            return 
        
        search(book, choose_note_name) #рекурсивно викликаємо функцію коли обрали одну нотатку

    


COMMAND_DICT = {
    'add': add_note_to_book,
    'show': show,
    'search': search,
    'delete': delete,
    'change': change,
    'close': close,
    'help': help,
    'tags': tags
}

END_COMMANDS = ['exit', 'close', 'quit']

COMMAND_INPUT = ['add', 'show', 'search', 'close', 'help']
COMMAND_INPUT_MENU = ['delete', 'change', 'tags clean', 'tags change', 'tags add', 'close']

HELP_TABLE = PrettyTable(['Команди', 'Пояснення'])
HELP_TABLE.add_row(['add <назва нотатки> <текс нотатки>', 'створити нову нотатку (назва без пробілів)',], divider=True)
HELP_TABLE.add_row(['show <date|alp|size>', "вивести всі нотатки, сортувати за датою|алфавітом|розміром (не обов'язково)"], divider=True)
HELP_TABLE.add_row(['search <тег|назва нотатки>', 'пошук нотатки за тегами або назвою нотатки'], divider=True)
HELP_TABLE.add_row(['close', 'завершити роботу',], divider=True)
HELP_TABLE.add_row(['help', 'список команд',], divider=True)


HELP_NOTE_TABLE = PrettyTable(['Команда', 'Пояснення']) 
HELP_NOTE_TABLE.add_row(['delete', 'видалити'], divider=True)
HELP_NOTE_TABLE.add_row(['change <новий текст нотатки>', 'змінити нотатку'], divider=True)
HELP_NOTE_TABLE.add_row(['tags clean|change|add', 'змінити теги \n(clean - очистити, change - змінити, add - додати)'], divider=True)
HELP_NOTE_TABLE.add_row(['close', 'закрити меню нотатки'], divider=True)
