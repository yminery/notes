from PyQt5.QtWidgets import (QApplication, QWidget, QListWidget, QPushButton,
QTextEdit, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QInputDialog)

import json


notes = {"Hello" : {
        "txt" : "This is the best note in the world!!!",
        "tags" : ['welcome', 'instruct']
    }
}   
'''
with open('notes_data.json', 'w') as file:
    json.dump(notes, file)
'''
app = QApplication([])
notes_win = QWidget()
notes_win.setWindowTitle('smart notes')
notes_win.resize(900,600)
list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')

but_not_create = QPushButton('Создать заметку')
but_not_del = QPushButton('Удалить заметку')
but_not_save = QPushButton('Сохранить заметку')

list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')

but_tag_dd = QPushButton('Добавить тег')
but_tag_de  = QPushButton('Удалить тег')
but_tag_sher = QPushButton('Поиск по тегу')

field_txt = QTextEdit()
field_tag = QLineEdit()
field_tag.setPlaceholderText('Введите тег...')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()
row_1 = QHBoxLayout()
row_2 = QHBoxLayout()
row_3 = QHBoxLayout()
row_4 = QHBoxLayout()
col_1.addWidget(field_txt)
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1.addWidget(but_not_create)
row_1.addWidget(but_not_del)
row_2.addWidget(but_not_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3.addWidget(but_tag_dd)
row_3.addWidget(but_tag_de)
row_4.addWidget(but_tag_sher)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_txt.setText(notes[key]['txt'])
    list_tags.clear()
    list_tags.addItems(notes[key]['tags'])

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Add note', 'name of note')
    if ok and note_name:
        notes[note_name] = {'txt' : "", "tags": []}
        list_notes.addItem(note_name)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['txt'] = field_txt.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_txt.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)

def add_tags():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text() 
        tag = field_tag.text()
        if not tag in notes[key]['tags']:
            notes[key]['tags'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys=True)

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text() 
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys=True)

def search_tag():
    tag = field_tag.text()
    if but_tag_sher.text() == 'Поиск по тегу' and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        but_tag_sher.setText('Сбросить поиск')
        list_notes.create()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif but_tag_sher.text() == 'Сбросить поиск':
        list_notes.clear()
        field_tag.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        but_tag_sher.setText('Поиск по тегу')

but_tag_sher.clicked.connect(search_tag)

but_tag_de.clicked.connect(add_tags)                            
but_tag_dd.clicked.connect(add_tags)                            
but_not_del.clicked.connect(del_note)            
but_not_save.clicked.connect(save_note)       
but_not_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)

with open ('notes_data.json', 'r') as file:
    notes = json.load(file)
    
list_notes.addItems(notes)
notes_win.show()
app.exec_()