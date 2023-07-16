import threading
import time
from updated_addressbook.classes import *
from updated_addressbook.openai_logic import gpt_response
from updated_addressbook.error_handlers import input_error
from updated_addressbook.table_constructor import table_header, print_contact, table_row


def greet(*_, **__):
    print('How can I help you?')

@input_error
def add_contact(args: list, address_book: AddressBook) -> None:
    name, phone = Name(args[0]), Phone(args[1])
    birthday = Birthday(args[2]) if len(args) > 2 else None

    if name.value in address_book:
        if phone not in address_book[name.value].phones:
            address_book[name.value].add_phone(phone)
            if not birthday:
                print(f'Phone number \'{phone}\' was successfully added.')
            else:
                print(f'Phone number \'{phone}\' was successfully added.')
                print('To change or set birthday date for an existing contact use \'birthday\' command.')
        else:
            raise PhoneAlreadyExistsError
    else:
        record = Record(name, phone, birthday)
        address_book.add_record(record)
        print(f'Contact was successfully added.')

@input_error
def birthday_handler(args: list, address_book: AddressBook) -> None:
    name = args[0]
    if len(args) >= 2:
        birthday = Birthday(args[1])
        if address_book[name].birthday:
            user_input = input(f'Do you wanna chage birthday date for \'{name}\'? (y/N) ')
            if user_input == 'y':
                address_book[name].birthday = birthday
                print('Birthday date was successfully changed.')
        else:
            address_book[name].birthday = birthday
            print('Birthday date was successfully set.')
    else:
        days_to_birthday = address_book[name].days_to_birthday()
        print(f'{days_to_birthday} days to \'{name}\'s birthday.')

@input_error
def remove_contact(args: list, address_book: AddressBook) -> None:
    name = args[0]
    # takes phone as second argument to remove it from contact
    if len(args) >= 2:
        phone = Phone(args[1])
        address_book[name].remove_phone(phone)
        print(f'Phone number \'{phone}\' was successfully removed.')
    else:
        user_input = input(f'Do you realy want to delete contact \'{name}\'? (y/N) ')
        if user_input == 'y':
            address_book.remove_record(name)
            print(f'Contact \'{name}\' was successfully removed.')
    
    
@input_error
def change_number(args: list, address_book: AddressBook) -> None:
    name, phone, new_phone = args[0], Phone(args[1]), Phone(args[2])
    address_book[name].change_phone(phone, new_phone)
    print(f'Phone number \'{phone}\' was successfully changed to \'{new_phone}\'.')
    

@input_error
def show_contact_numbers(args: list, address_book: AddressBook) -> None:
    name = args[0]
    phones = address_book[name].get_phones()
    phones_str = ', '.join(phones)
    if not phones:
        print(f'\'{name}\' doesn\'t have phone numbers.')
    elif len(phones) == 1:
        print(f'\'{name}\'s phone number: \'{phones_str}\'.')
    else:
        print(f'\'{name}\'s phone numbers: \'{phones_str}\'.')

@input_error
def find_contacts(args: list, address_book: AddressBook) -> None:
    search_string = args[0]
    search_result = sorted(address_book.find(search_string))

    row_length = table_header()
    count = 1
    if search_result:
        for name, record in search_result:
            print_contact(count, name, record, row_length)
            count += 1
    else:
        print(table_row(phone='No matches'))
        print('='*row_length)


@input_error
def show_whole_contacts_book(args: list, address_book: AddressBook) -> None:
    contacts_per_time = int(args[0]) if args else 5
    row_length = table_header()
    count = 1

    if address_book:
        for page in address_book.iterator(contacts_per_time):
            for name, record in page:
                print_contact(count, name, record, row_length)
                count += 1
            if len(address_book.keys()) >= count:
                user_input = input('Do you wanna see the next page? (Y/n) ')
                if user_input == 'n':
                    break
                print('='*row_length)
    else:
        print(table_row(phone='No entries'))
        print('='*row_length)

@input_error
def clear_book(_, address_book: AddressBook) -> None:
    user_input = input('Do you realy want to delete all contacts? (y/N) ')
    if user_input == 'y':
        address_book.clear()
        print('\nAddress book was successfully cleared.')

response_received = False

def show_loading_animation():
    global response_received
    animation = "|/-\\"
    i = 0
    while True:
        print("Waiting for model response... " + animation[i % len(animation)], end="\r")
        i += 1
        time.sleep(0.1)

        # Break the loop when response is received
        if response_received:
            break

def ask_ai(args: list, _):
    global response_received 
    prompt = ' '.join(args)
    animation_thread = threading.Thread(target=show_loading_animation)
    animation_thread.start()
    response = gpt_response(prompt)
    response_received = True
    animation_thread.join()
    print(f'(Valera) {response}')


    
def exit_bot():
    print('I\'ll miss you so much!')
   

def get_help(*_, **__) -> None:
    print(
    """Important! Divide command and arguments only with white spaces in the other case it can lead to errors 
or data coruption. Don't terminate bot with CTRL+C combination because all unsaved changes will be lost.

Available commands:
    - hello                                 Greet user
    - add <name> <phone> <birthday>(opt)    Add new contact wirh number and birhtday(optional)
    - birthday <date>(opt)                  Shows how many days to birthday left or set birthday date 
    - change <name> <phone> <new_phone>     Change the phone number of an existing contact
    - remove <name> <phone>(opt)            Remove contact or phone number
    - phone <name>                          Get contact's phone numbers
    - find <search_string>                  Display contacts which contain search string (phone, name)
    - show all                              Display whole contacts book
    - clear                                 Empty address book
    - help                                  Show this help message
    - good bye, close, exit                 End the bot
    """
    )