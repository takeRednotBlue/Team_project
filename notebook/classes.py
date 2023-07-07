

class Note():

    def __init__(self, text, *tags):
        self.text = text
        self.tags = []
        self.tags.extend(tags)

    def __repr__(self) -> str:
        return self.text
    
    def add_tags(self, tags):
        self.tags.extend(tags)


class NoteBook():

    def __init__(self):
        self.data = []

    def add_note(self, value):
        note = Note(value)

        answer = input('Бажаєте додати теги до цієї нотатки? Y/N: ')
        while answer not in ['y', 'Y', 'n', 'N']:
            answer = input('Введіть так або ні (Y/N): ')


        if answer in ['y', 'Y']:

            tags = input('Введіть теги: ')
            if tags:
                tags = tags.split(' ')
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
            
            if value in note.text or value in note.tags:

                result.append(note)

        return result if value else []
    
    def delete(self, note):
        for i in self.data:
            if i == note:
                del self.data[self.data.index(note)]

    def change(self, new_value, note):
        self.delete(note) 
        self.add_note(new_value)

    def change_tag(self, new_tags, note):
        for n in self.data:
            if n == note:
                index_note = self.data.index(n)
                old_note = self.data[index_note]
                new_note = Note(old_note.text, new_tags)
                
                self.delete(old_note)
                self.add(new_note)
        

