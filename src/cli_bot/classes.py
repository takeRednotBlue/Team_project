from typing import Generator
from collections import UserDict
from datetime import datetime
import pickle
import re
from pathlib import Path


class PhoneNotFoundError(Exception):
    pass

class PhoneAlreadyExistsError(Exception):
    pass


class Field:
    def __init__(self, value) -> None:
        self._value = None
        self.value = value

    @property
    def value(self) -> any:
        return self._value
    
    @value.setter
    def value(self, new_value: any) -> None:
        self._value = new_value

    def __eq__(self, other: 'Field') -> bool:
        if other == None:
            return False
        return str(self.value) == str(other.value)
            
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        # return f'{self.__class__.__name__}Object({self.value})'
        return str(self.value)
    
    def __len__(self) -> int:
        return len(self.value)
    
    
class Phone(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, phone: str) -> None:
        if phone.isnumeric():
            if len(phone) == 12 and phone.startswith('380'):
                self._value = '+' + phone
            elif len(phone) == 10 and phone.startswith('0'):
                self._value = '+38' + phone
            elif len(phone) == 13 and phone.startswith('+380'):
                self._value = phone
            else:
                raise ValueError(f'Phone\'s format \'{phone}\' must comply to the national phone numbers conventions.')
        else:
            raise ValueError(f'Phone\'s format \'{phone}\' must comply to the national phone numbers conventions.')
  
    def get_phone(self) -> str:
        return self.value
    

class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, name: str) -> None:
        if len(name) >= 3 and name[0].isalpha():
            self._value = name
        else:
            raise ValueError('Invalid name. Name must start from letter and has at least 3 symbols.')      

    def get_name(self) -> str:
        return self.value

    
class Birthday(Field):
    def __init__(self, value: datetime) -> None:
        super().__init__(value)
    
    @Field.value.setter
    def value(self, date: str) -> None:
        format = self.format_mapper(date)
        birthday = datetime.strptime(date, format).date()
               
        approx_age = datetime.now().year - birthday.year
        if 0 <= approx_age <= 120:
            self._value = birthday
        else:
            raise ValueError('Invalid date. Age must be in range from 0 to 120 years.')

    def format_mapper(self, date: str) -> str:
        '''
        Available formats: '12.03.2023', '12/14/2023', '12.03.23', '12/03/23', '2023-03-12'
        '''
        date_mapping = {
                r'\d{2}\.\d{2}\.\d{4}': '%d.%m.%Y',
                r'\d{2}/\d{2}/\d{4}': '%d/%m/%Y',
                r'\d{2}\.\d{2}\.\d{2}': '%d.%m.%y',
                r'\d{2}/\d{2}/\d{2}': '%d/%m/%y',
                r'\d{4}-\d{2}-\d{2}': '%Y-%m-%d',
        }
        
        for pattern, format in date_mapping.items():
            if re.match(pattern, date):
                return format
        else:
             raise ValueError('Invalid date format.')
        
    def get_birthday(self) -> str:
        return str(self.value)
    
    def __str__(self) -> str:
        return self.value.strftime('%d.%m.%Y')
    
    def __bool__(self) -> bool:
        if self.value == None:
            return False
        else:
            return True
       
    def __len__(self) -> None:
        pass
        
class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday
        if phone:
            self.add_phone(phone)

    def add_phone(self, phone: Phone) -> None:
        if phone not in self.phones:
            self.phones.append(phone)
        else:
            raise PhoneAlreadyExistsError

    def change_phone(self, phone: Phone, new_phone: Phone) -> None:      
        if phone in self.phones:
            phone_pos = self.phones.index(phone)
            self.phones.insert(phone_pos, new_phone)
            self.phones.remove(phone)
        else:
            raise PhoneNotFoundError
        
    def remove_phone(self, phone: Phone) -> None:
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise PhoneNotFoundError

    def get_phones(self) -> list:
       phones_list = [phone.value for phone in self.phones]
       return phones_list
    
    def days_to_birthday(self) -> int:
        if self.birthday != None:
            today = datetime.now().date()
            difference = self.birthday.value.replace(year=today.year) - today
            if difference.days < 0:
                difference = self.birthday.value.replace(year=today.year+1) - today
            return difference.days
        else:
            raise ValueError('Birthday is not set.')
        
    
    def __repr__(self) -> str:
        attr_dict = {
            'name': self.name,
            'phones': self.phones,
            'birthday': self.birthday,
        }
        return f'RecordObject({attr_dict})'
    
class AddressBook(UserDict):
    def __init__(self, filename: str|Path) -> None:
        super().__init__()
        self.filename = filename

    def add_record(self, record: Record) -> None:
        self.data.update({
            record.name.value: record,
        })
    
    def remove_record(self, name: str) -> None:
        self.data.pop(name)
    
    def iterator(self, number: int = 5) -> Generator[list, None, None]:
        sorted_data = sorted(self.data.items())
        index = 0
        while index < len(sorted_data):
            yield sorted_data[index:index+number]
            index += number

    def save_to_file(self) -> None:
        with open(self.filename, 'wb') as fh:
            pickle.dump(self, fh)
    
    def read_from_file(self) -> 'AddressBook':
        with open(self.filename, 'rb') as fh:
            book = pickle.load(fh)
        return book

    def find(self, lookup_string: str) -> list:
        result = []
        for name, record in self.data.items():
            if lookup_string.lower() in name.lower():
                result.append((name, record))
            else:
                for phone in record.get_phones():
                    if lookup_string.lower() in phone.lower():
                        result.append((name, record))
                        break
        return result
    

if __name__ == "__main__":
    max = Record(Name('Max'), Phone('0933434459'))
    valera = Record(Name('Valera'), Phone('0933434459'))
    anton = Record(Name('Anton'), Phone('0933434459'))
    vlad = Record(Name('Vlad'), Phone('0933434459'))
    yura = Record(Name('Yura'), Phone('0933434459'))
    sasha = Record(Name('Sasha'), Phone('0933434459'))
    bogdan = Record(Name('Bogdan'), Phone('0933434459'), Birthday("26.06.1996"))
    valentun = Record(Name('Valentun'), Phone('0933434459'))
    tolya = Record(Name('Tolya'), Phone('0933434459'))

    ab = AddressBook(Path(__file__).parent / 'address_book.bin')
    ab.add_record(max)
    ab.add_record(valera)
    ab.add_record(vlad)
    ab.add_record(yura)
    ab.add_record(sasha)
    ab.add_record(bogdan)
    ab.add_record(valentun)
    ab.add_record(tolya)

    # ab.save_to_file()
    # print('Saved')
    # loaded_ab = ab.read_from_file()
    # bd_days = loaded_ab['Bogdan'].days_to_birthday()
    # print(f'There is {bd_days} days to Bogdan\'s birthday.')
    print(ab)


    print('All Ok)')



    
