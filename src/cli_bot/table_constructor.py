def table_header():
    header = table_row('N', 'Name', 'Phone numbers', 'Birthday')
    row_length = len(header)
    print('='*row_length)
    print(header)
    print('='*row_length)
    return row_length

def table_row(count='', name='', phone='', birthday='') -> None:
    row = '|{:^5}|{:^20}|{:^30}|{:^12}|'.format(count, name, phone, birthday)
    return row

def print_contact(count, name, record, row_length):
    phones = record.get_phones()
    birthday = str(record.birthday.value) if record.birthday else 'No entry'
    # handle contact's multiple phones
    if len(phones) == 1: 
        print(table_row(count, name, phones[0], birthday))
    elif  len(phones) > 1:
        print(table_row(count, name, phones[0], birthday))
        for phone in phones[1:]:
            print(table_row(phone=phone))
    else:
        print(table_row(count, name, 'No phones', birthday))
    print('='*row_length)