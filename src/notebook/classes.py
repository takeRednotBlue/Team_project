from datetime import datetime

from prettytable import PrettyTable, DOUBLE_BORDER

from abstraction import TerminalOutput

class Note():

    def __init__(self, name, text, tags=None):
        self.createde_time = datetime.now()
        self.name = name
        self.tags = None
        self.text = text
        if tags:
            self.add_tags(tags)


    def add_tags(self, tags):
        if self.tags is None:
            self.tags = set()
        self.tags.update(tags)

    def change_tags(self, new_tags):
        self.tags = set([*new_tags])

    def change_note(self, new_value):
        self.text = new_value

    def clean_tag(self):
        self.tags = set()

    def __eq__(self, obj: object) -> bool:
        return self.createde_time == obj.createde_time
    
    def __ge__(self, obj):
        return self.createde_time >= obj.createde_time
    
    def __le__(self, obj):
        return self.createde_time <= obj.createde_time
    
    def __lt__(self, obj):
        return self.createde_time < obj.createde_time
    
    def __gt__(self, obj):
        return self.createde_time > obj.createde_time


class NoteBook():

    def __init__(self):
        self.data = []

    def add_note(self, name, value):
        new_note = Note(name, value)
        self.data.append(new_note)
        return new_note

    def add(self, note: Note):
        self.data.append(note)

    def show_all(self):
        return self.data
    
    def search(self, value):

        result = []
        for note in self.data:
            
            if value in note.tags or value in note.name:
                result.append(note)

        for note in result:
            if note.name == value:
                result = [note]

        return result if value else []
    
    def delete(self, note):
        for i in self.data:
            if i == note:
                del self.data[self.data.index(note)]


    def change(self, new_value, note):
        self.delete(note) 
        self.add_note(note.name, new_value)

    def change_tag(self, new_tags, note):
        for n in self.data:
            if n.name == note.name:
                index_note = self.data.index(n)
                old_note = self.data[index_note]
                new_note = Note(old_note.name, old_note.text, new_tags)
                
                self.delete(old_note)
                self.add(new_note)
        
def text_normalizer(text: str) -> str:
    '''Для великих нотаток кожні 100 символів додаємо \n (для гарного виводу)'''
    if len(text) > 100: # Для великих нотаток кожні 100 символів додаємо \n (для гарного виводу)          
            normalized_text = ''
            counter = 0
            for i in text:
                normalized_text += i
                counter += 1
                if not counter % 100:
                    normalized_text += '\n'

                if len(normalized_text) > 296:
                            normalized_text += '... '
                            break
    else:
        normalized_text = text
    return normalized_text

class NotebookTerminalOutput(TerminalOutput):
    def output_table_format(self, headers: list[str], data: list[Note]) -> PrettyTable:
        '''In order to display data in right column please place headers in the same sequence as class Record attributes were declared'''
        table = PrettyTable(headers)
        table.align = 'c'
        table.set_style(DOUBLE_BORDER)

        for note in data:
            row_data = []
            for key, value in note.__dict__.items():
                if isinstance(value, (list, tuple, set)):
                    value = '\n'.join(map(str, value))
                if isinstance(value, datetime):
                    value = value.strftime('%d/%m/%Y\n%H:%M:%S')
                if key == 'text':
                    value = text_normalizer(value)
                if value is None:
                    value = '-'
                
                row_data.append(str(value))

            if len(row_data) != len(headers):
                raise ValueError('Amount of headers doesn\'t match amount of data in a row.')
            
            table.add_row(row_data, divider=True)
        return table
    
    def output_help_msg(self, headers: list[str], data: dict) -> None:
        table = PrettyTable(headers)
        table.set_style(DOUBLE_BORDER)
        table.align = 'l'
        table.add_rows(list(data.items()))
        return table