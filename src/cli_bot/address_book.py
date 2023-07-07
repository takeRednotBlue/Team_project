from pathlib import Path
from .commands_parser import commands_parser
from .handlers import *


COMMANDS = {
    'hello': greet,
    'add': add_contact,
    'remove': remove_contact,
    'change': change_number,
    'phone': show_contact_numbers,
    'show all': show_whole_contacts_book,
    'help': get_help,
    'birthday': birthday_handler,
    'find': find_contacts,
    'clear': clear_book,
    'ask': ask_ai
}

END_COMMANS = ['exit', 'good bye', 'close']


def address_book_app():

    # Handles address_book book file
    contacts_book_file = Path().home() / 'address_book.bin'          
    # contacts_book_file = Path(__file__).parent / 'address_book.bin'          
    if contacts_book_file.exists():
        address_book = AddressBook(contacts_book_file).read_from_file()
    else:
        address_book = AddressBook(contacts_book_file)

    # address_book = ab
    is_working = True

    print('Привіт, це адресна книга. Тут ти можеш зберігати свої контакти.')

    while is_working:
        user_input = input('>>> (addrbook) ')
        command, arguments = commands_parser(user_input)
        if command in COMMANDS:
            command_handler = COMMANDS[command]
            command_handler(arguments, address_book)
        elif command in END_COMMANS:
            exit_bot()
            address_book.save_to_file()
            is_working = False
        else:
            print('Command not found. Use "help" for available commands.')


if __name__ == '__main__':
    address_book_app()

