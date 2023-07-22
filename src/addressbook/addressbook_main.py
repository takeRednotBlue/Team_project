from functools import wraps
import re

from email_validator import validate_email, EmailUndeliverableError
from colorama import Fore, init
from faker import Faker
from phonenumbers import is_valid_number, parse
# from tabulate import tabulate

from addressbook.addressbook_class import *
from utilities import completer_input
from data_storage import DATA_DIRECTORY

output_handler = ContactsTernminalOutput()

init()

def input_error(func):
    @wraps(func)
    def wrapper(*args):
        try:
            result = func(*args)
            return result

        except TypeError as errors:
            if func.__name__ == "add" or func.__name__ == "change":
                message = """
                Вкажіть ім'я, та номер, будь-ласка.\n
                Формат введення номеру має бути +38050*******, 050*******, або 38050*******\n
                Формат імені не може складатись лише з цифр.\n 
                """
                return message
            
            if func.__name__ == "add_birthday":
                message = """
                Вкажіть ім'я, та дату народження, будь-ласка.\n
                Формат введення дати має бути ДД.MM.РРРР або ДД/MM/РРРР\n
                Формат імені не може складатись лише з цифр.\n 
                """
                return message
            
            if func.__name__ == "add_email":
                message = """
                Вкажіть ім'я, та email, будь-ласка.\n
                Формат введення email має бути example@example.com, example@example.net, або example@example.org\n
                Формат імені не може складатись лише з цифр.\n 
                """
                return message
            return errors

        # except AttributeError:
            return "Будь-ласка, введіть коректні дані."
        
        except IndexError as errors:
            return errors

        except ValueError as errors:
            return errors
    return wrapper

@input_error
def hello(*args):
    """
    Вітає користувача, щоб скористатись просто введи 'hello'
    """
    return "Дякую, что привітався:) Чим можу допомогти?"

@input_error
def add(book: AddressBook, contact: str, phone: str = None):
    '''
    Створює контакт у книзі. Формат запиту: add *Ім'я* *Номер телефону*
    '''
    contact_new = Name(contact)
    phone_new = Phone(phone) if phone else None
    rec_new = Record(contact_new, phone_new)

    if contact not in book.keys():
        book.add_record(rec_new)
        return f'Додано контакт "{contact}" з номером телефону "{phone}"'
    else:
        book.get(contact).add_phone(phone_new)
        return f'Існуючий контакт "{contact}" оновлено з новим номером: {phone}'

@input_error
def email_add(book: AddressBook, contact: str, email: str):
    '''
    Додасть мейл до контакту. Формат запиту: email add *Ім'я* *email@email.com*
    '''
    email_new = Email(email)
    rec = book.get(contact)
    rec.add_email(email_new)
    return f'У контакті {contact} обновився email на {email}'


@input_error
def birthday_add(book: AddressBook, contact: str, birthday: str):
    '''
    Додасть дату народження. Формат запиту: birthday add *Ім'я* *ДД.ММ.РРРР*
    '''
    birth = Birthday(birthday)
    rec = book.get(contact)
    rec.add_birthday(birth)
    return f'У контакті {contact} обновилась дата народження на: {birth}'

@input_error
def home_add(book: AddressBook, contact: str, home: str):
    '''
    Додасть адресу. Формат запиту: home add *Ім'я* *Адреса*
    '''
    address = Home(home)
    rec = book.get(contact)
    rec.add_home_address(address)
    return f'У контакті {contact} обновилась адреса на: {address}'

@input_error
def change_home(book: AddressBook, contact: str, home: str):
    '''
    Змінить домашню адресу контакту. Формат запиту: change home *Ім'я* *Адреса*
    '''
    rec = book.get(contact)
    if rec.home:
        rec.edit_home_address(home)
        return f'Домашня адреса контакту {contact} змінена на: {home}'
    else:
        raise IndexError("У цього контакту немає домашньої адреси")

@input_error
def change_phone(book: AddressBook, contact: str, phone: str = None):
    '''
    Змінить номер контакту. Формат запиту: add change phone *Ім'я* *Новий номер*
    '''
    rec = book.get(contact)

    print(rec.show_phones())

    if not rec.phones:
        if not phone:
            phone_new = Phone(input("Якщо Ви хочете додати номер, введіть його:"))
        else:
            phone_new = Phone(phone)
        rec.add_phone(phone_new)
        return f'Номер змінено на {phone_new} для контакту {contact}'

    else:
        if len(rec.phones) == 1:
            num = 1
        if len(rec.phones) > 1:
            num = int(input("Який номер бажаєте змінити ( введіть індекс номеру):"))
        if not phone:
            phone_new = Phone(input("Будь-ласка, введіть новий номер:"))
        else:
            phone_new = Phone(phone)
        old_phone = rec.phones[num - 1]
        rec.edit_phone(phone_new, num)
        return (f'Номер контакту {contact} з {old_phone} був змінений на {phone_new}.')


@input_error
def delete_phone(book: AddressBook, contact: str, phone=None):
    '''
    Видалить номер контакту. Формат запиту: delete phone *Ім'я*
    '''
    rec = book.get(contact)

    if phone:
        for i, p in enumerate(rec.phones):
            if p == phone:
                num = i + 1
        else:
            raise ValueError("Цей контакт не має номеру.")
    else:
        print(rec.show_phones())
        if len(rec.phones) == 1:
            ask = None
            num = 1
            while ask != "y":
                ask = input(
                    f"Контакт {rec.name} має лише один номер {rec.phones[0]}.\
                        Ви впевнені? (Y/N)").lower()
        else:
            num = int(input("Який саме номер бажаєте видалити? (Вкажіть індекс):"))
    return f"Номер {rec.del_phone(num)} видалено!"


@input_error
def delete_email(book: AddressBook, *args):
    '''
    Видалить email контакту. Формат запиту: delete email *Ім'я*
    '''
    contact = " ".join(args)
    rec = book.get(contact)
    rec.email = None
    return f"Контакт {contact}, email видалено"


@input_error
def delete_contact(book: AddressBook, *args):
    '''
    Видалить контакт повністю. Формат запиту: delete contact *Ім'я*
    '''
    contact = " ".join(args)
    rec = book.get(contact)
    if not rec:
        raise AttributeError
    ask = None
    while ask != "y":
        ask = input(f"Ви впевнені, що хочете повністю видалити контакт {contact}? (Y/N)").lower()
    return f"Контакт {book.remove_record(contact)} видалено!"


@input_error
def delete_birthday(book: AddressBook, *args):
    '''
    Видалить дату народження контакту. Формат запиту: delete birthday *Ім'я*
    '''
    contact = " ".join(args)
    rec = book.get(contact)
    rec.birthday = None
    return f"День народження контакту {contact} було видалено."


@input_error
def phone(book: AddressBook, *args):
    '''
    Нагадає тобі номер вказаного контакту. Формат запиту: phone *Ім'я*
    '''
    contact = " ".join(args)
    rec = book.get(contact)
    return f'Контакт "{contact}". {rec.show_phones()}'

# @input_error
def show_all(book: AddressBook, *args):
    """
    Виведе на екран всі контакти у колонках.
    """
    table_headers = ["Ім'я", "Телефон", "E-mail", "День народження", "Адреса"]
    return output_handler.output_table_format(table_headers, list(book.data.values()))
    # table_data = []
    # for contact in book.data.values():
    #     name = contact.name.value
    #     phone = "\n".join([str(phone) for phone in contact.phones])
    #     email = str(contact.email) if contact.email else "Не вказано"
    #     birthday = str(contact.birthday) if contact.birthday else "Не вказано"
    #     home = str(contact.home) if contact.home else "Не вказано"
    #     table_data.append([name, phone, email, birthday, home])
    # print()
    # return tabulate(table_data, headers=table_headers, tablefmt="grid")

@input_error
def search(book: AddressBook, *args):
    """
    Знайде контакт, та всю інформацію про нього. Формат запиту: search *Ім'я*
    """
    pattern = " ".join(args)
    result = book.search(pattern)
    if not result:
        return "Нічого не знайдено!"
    
    table_headers = ["Ім'я", "Номер телефону", "E-mail", "День народження", "Адреса"]
    table = output_handler.output_table_format(table_headers, result)
    return f"Знайдено {len(result)} співпадіння(ннь):\n{table}"
    # table_data = []
    # for contact in result:
    #     name = str(contact.name)
    #     phones = ", ".join([str(phone) for phone in contact.phones])
    #     email = str(contact.email)
    #     birthday = str(contact.birthday)
    #     home = str(contact.home)
    #     table_data.append([name, phones, email, birthday, home])
    # table = tabulate(table_data, headers=table_headers, tablefmt="grid")
    # return f"Знайдено {len(result)} співпадіння(ннь):\n{table}"

@input_error
def help_me(*args):
    '''
    Викликаєш цей список команд ще раз, якщо забув:)
    '''
    help_table_data = []
    for cmd, func in command.items():
        comment = [func.__doc__.strip() if func.__doc__ else ""]
        help_table_data.append([cmd, comment[0]])
    
    help_table_headers = ["Команда", "Коментар"]
    table = output_handler.output_help_msg(help_table_headers, help_table_data)
    return f"Доступні команди:\n{table}"

@input_error
def exit(book: AddressBook, *args):
    """
    Завершує роботу програми
    """
    global is_ended
    is_ended = True
    book.save_to_file()
    return "До зустрічі!"




command = {
    "hello": hello,
    "email add": email_add,
    "birthday add": birthday_add,
    "home add": home_add,
    "add": add,
    "change phone": change_phone,
    "phone": phone,
    "show all": show_all,
    "search": search,
    "delete phone": delete_phone,
    "delete birthday": delete_birthday,
    "delete email": delete_email,
    "delete contact": delete_contact,
    "close": exit,
    "good bye": exit,
    "exit": exit,
    "help": help_me,
}

commands_list = list(command)

@input_error
def command_parser(string: str):
    splitted_str = " ".join(string.split())
    for key, value in command.items():
        if splitted_str.lower().startswith(key + " ") or splitted_str.lower() == key:
            return value, re.sub(key, "", splitted_str, flags=re.IGNORECASE).strip().rsplit(" ", 1 )
    return no_command, []

@input_error
def no_command(*args):
    return "Нажаль, такої команди немає, скористайтесь \"help\""



def fake(book):
    fake = Faker('uk_UA')

    for _ in range(10):
        contact = fake.first_name()

        while True:
            try:
                email = fake.ascii_free_email()
                if validate_email(email):
                    break
            except EmailUndeliverableError:
                pass

        while True:
            phone = re.sub(r'\D', '', fake.phone_number())
            parsed_phone = parse(phone, 'UA')
            if len(phone) > 9 and is_valid_number(parsed_phone):
                break
        
        fake_date = fake.date()
        birthday = datetime.strptime(fake_date, '%Y-%m-%d').strftime('%d.%m.%Y')

        city = fake.city().split()
        if len(city) > 1:
            city = city[-1]


        add(book, contact, phone)
        email_add(book, contact, email)
        birthday_add(book, contact, birthday)
        home_add(book, contact, city)


is_ended = False

def main():

    global is_ended
    
    filename = DATA_DIRECTORY / 'addressbook_data.bin'
    if filename.exists():
        book1 = AddressBook(filename).load_from_file()
    else:
        book1 = AddressBook(filename)

    # fake(book1)
    
    first_lauch = True
    try:
        while not is_ended:
            if first_lauch:
                print()
                print('{:<116}'.format(Fore.BLUE + f'{" "*5}Вас вітає додаток АДРЕСНА КНИГА 📖'))
                print('{:<116}'.format(Fore.YELLOW + f'{" "*5}Тут ви можете зберігати свої контакти та керувати ними' + Fore.WHITE))
                print('{:<116}'.format(f'{" "*5}Якщо не знаєте яку команду ввести, скористайтесь командою < help > чи натисні TAB для швидкого вибору'))
                print()
                first_lauch = False

            start_text = completer_input(">>> ", commands_list)
            command, args = command_parser(start_text)
            print(command(book1, *args))
        else:
            is_ended = False
    except KeyboardInterrupt:
        print('Будь ласка, користуйся командами для завершення роботи')
        book1.save_to_file()



if __name__ == "__main__":
    main()