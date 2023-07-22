from collections import UserDict
from datetime import datetime
from itertools import islice
from email_validator import validate_email
import phonenumbers
import pickle
from prettytable import PrettyTable, DOUBLE_BORDER

from abstraction import TerminalOutput


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if validate_email(value):
            self.__value = value
        else:
            raise ValueError("Невірно вказаний email")
        
class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not value.isnumeric():
            self.__value = value
        else:
            raise ValueError('Ім\'я не може бути лише з цифр.')


class Phone(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        parsed_number = phonenumbers.parse(value, "UA")
        if phonenumbers.is_valid_number(parsed_number):
            self.__value = value
        else:
            raise ValueError("Невірно вказаний телефонний номер")


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d.%m.%Y")          
        except ValueError:
            return "Невірно вказано дату народження, використовуйте формат ДД.MM.РРРР"

    def __str__(self) -> str:
        return datetime.strftime(self.value, "%d.%m.%Y")


class Home(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return self.value


class Record:
    def __init__(
        self,
        name: Name,
        phone: Phone = None,
        email: Email = None,
        birthday: Birthday = None,
        home: Home = None,
    ):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.email = email
        self.birthday = birthday
        self.home = home

    def __str__(self):
        num = ", ".join([str(phone) for phone in self.phones])
        line = f"{self.name}: Номер телефону: {num}; Email: {self.email}; День народження: {self.birthday}; Адреса: {self.home}\n"
        return line
    
    def __repr__(self):
        num = ", ".join([str(phone) for phone in self.phones])
        line = f"{self.name}: Номер телефону: {num}; Email: {self.email}; День народження: {self.birthday}; Адреса: {self.home}\n"
        return line

    def days_to_birthday(self):
        if not self.birthday:
            return "Ви не вказувати дату народження цього контакту"
        today = datetime.today()
        compare = self.birthday.value.replace(year=today.year)
        days = int((compare - today).days)
        if days >= 0:
            return f"{days} днів до дня народження"
        else:
            days = int((compare.replace(year=today.year + 1) - today).days)
            return f"{days} днів до дня народження"

    def add_email(self, email: Email):
        if not self.email:
            self.email = email
        else:
            raise IndexError("E-mail вже був доданий")

    def add_phone(self, phone: Phone):
        if phone in self.phones:
            raise IndexError("Номер телефону вже був доданий")
        self.phones.append(phone)

    def add_birthday(self, birthday: Birthday):
        if not self.birthday:
            self.birthday = birthday
        else:
            raise IndexError("День народження вже був вказаний")

    def show_phones(self):
        if not self.phones:
            return "У цього контакту немає номеру"
        elif len(self.phones) == 1:
            return f"Поточний номер {self.phones[0]}"
        else:
            output = "Цей контакт має декілька номерів:\n"
            for i, phone in enumerate(self.phones, 1):
                output += f"{i}: {phone} "
            return output

    def del_phone(self, num=1):
        if not self.phones:
            raise IndexError("У цього контакту немає номеру")
        else:
            return self.phones.pop(num - 1)

    def edit_phone(self, phone_new: Phone, num=1):
        if not self.phones:
            raise IndexError("У цього контакту немає номеру")
        else:
            self.phones.pop(num - 1)
            self.phones.insert(num - 1, phone_new)
            
    def add_home_address(self, home: str):
        if not self.home:
            self.home = home
        else:
            raise IndexError("Домашня адреса вже була додана")


class AddressBook(UserDict):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename


    def load_from_file(self):
        with open(self.filename, "rb") as file:
            book = pickle.load(file)
        return book

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)
    
    def search(self, sample: str) -> list:
        searching = []
        for contact in self.data.values():
            if sample.lower() in str(contact).lower():
                searching.append(contact)
        return searching

    def remove_record(self, contact):
        return self.data.pop(contact)

    def add_record(self, record: Record):
        self.data.update({record.name.value: record})

    def show_all(self):
        return self.data.values()
    
class ContactsTernminalOutput(TerminalOutput):
    def output_table_format(self, headers: list[str], data: list[Record]) -> PrettyTable:
        '''In order to display data in right column please place headers in the same sequence as class Record attributes were declared'''
        table = PrettyTable(headers)
        table.align = 'c'
        table.set_style(DOUBLE_BORDER)

        for contact in data:
            row_data = []
            for value in contact.__dict__.values():
                if isinstance(value, (list, tuple, set)):
                    value = '\n'.join(map(str, value))
                if value is None:
                    value = '-'
                row_data.append(str(value))

            if len(row_data) != len(headers):
                raise ValueError('Amount of headers doesn\'t match amount of data in a row.')
            
            table.add_row(row_data)
            
        # for contact in data:
        #     name = str(contact.name)
        #     phones = "\n".join([str(phone) for phone in contact.phones])
        #     email = str(contact.email)
        #     birthday = str(contact.birthday)
        #     home = str(contact.home)
        #     table.add_row([name, phones, email, birthday, home])
        return table
    
    def output_help_msg(self, headers: list[str], data: list[list[str]]) -> None:
        table = PrettyTable(headers)
        table.set_style(DOUBLE_BORDER)
        table.align = 'l'
        table.add_rows(list(data))
        return table

    
if __name__ == '__main__':
    record = Record('John', '380934454458')
    # record = Record('John', '380934454458', '10.08.1999', 'john@gmail.com', 'Kyiv')
    print(record.__dict__)
    # test_list = ['test']
    # test_result = '\n'.join(test_list)
    # print(test_result)

