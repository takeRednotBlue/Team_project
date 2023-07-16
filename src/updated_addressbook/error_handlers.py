from updated_addressbook.classes import PhoneNotFoundError, PhoneAlreadyExistsError

# Lists of commads handlers sorted by argumets they take.
HAS_NO_ARGS = [
    "greet",
    "show_whole_contacts_book",
    "get_help"
]

HAS_NAME_AND_PHONE_ARGS = [
    "add_contact",
    "change_number",
]

HAS_ONLY_NAME_ARG = [
    'phone',
    "remove_contact",
    "show_contact_number",
]

HAS_NAME_AND_TWO_PHONES_ARGS = ['change_number']

def input_error(func):
    def wrapper(*args):
        try:
            func(*args)
        except IndexError as inderr:
            if func.__name__ in HAS_NAME_AND_PHONE_ARGS:
                print('Missing arguments. Please write name and phone number.')
            elif func.__name__ in HAS_NAME_AND_TWO_PHONES_ARGS:
                print('Missing arguments. Please write name, phone to be changed and new phone.')
            elif func.__name__ in HAS_ONLY_NAME_ARG:
                print('Missing argument. Plese wrinte contact\'s name.')
            else:
                print('Missing arguments.')
        except KeyError as keyerr:
            print(f'Cannot find such contact. Please check spelling and try again.')
        except ValueError as err:
            if func.__name__ == 'show_whole_contacts_book':
                print('Invalid argument. Expected number.')
            print(err)
        except PhoneNotFoundError:
            print('Phone was not found.')
        except PhoneAlreadyExistsError:
            print('Phone already exists.')
            
    return wrapper
