from datetime import datetime

class Note():

    def __init__(self, name, text, tags=None):
        self.createde_time = datetime.now()
        self.name = name
        self.text = text
        self.tags = []
        if tags:
            self.tags.extend(tags)

    # def __repr__(self) -> str:
    #     return f'.{self.name}.'
    
    def add_tags(self, tags):
        self.tags.extend(tags)

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
        note = Note(name, value)

        answer = input('Бажаєте додати теги до цієї нотатки? Y/N: ')
        while answer not in ['y', 'Y', 'n', 'N']:
            answer = input('Введіть так або ні (Y/N): ')


        if answer in ['y', 'Y']:

            tags = input('Введіть теги: ')
            if tags:
                tags = tags.split(' ')
                tags = [t for t in tags if t] # Видаляємо пусті теги
                note.add_tags(tags)
            else:
                print('Не можна зберегти порожні теги')

        self.data.append(note)

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
        

