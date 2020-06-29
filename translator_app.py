# -*- coding: utf-8 -*-
"""
Created on Tue Jul  30 10:49:25 2019

@author: akshay.kale
"""

import PySimpleGUI as sg
import xlrd

from googletrans import Translator
from xlwt import Workbook

src = ""
'''An desktop app to upload a source file and translate the data to English'''
def translate(src, column):
    
    filename = src.split('/')[-1]
    book = xlrd.open_workbook(src)
    wb = Workbook(encoding="UTF-8")
    translator = Translator()
    sheet1 = wb.add_sheet('Sheet 1')
    sheet1.write(0, 0, "Original Text")
    sheet1.write(0, 1, "Translated Text")
    first_sheet = book.sheet_by_index(0)
    for row_index in range(0, first_sheet.nrows):
        cell = first_sheet.cell(row_index, column)
        sheet1.write(row_index + 1, 0, cell.value)
        sheet1.write(row_index + 1, 1, str(translator.translate(cell.value).text))
        print (cell.value)
    wb.save("translated_" + filename.split('.')[0] + '.xls')

'''Creating the simple UI '''
layout = [[ sg.Text("Select path from source to destination")],
          [sg.Text("Source Folder", size=(15,1)), sg.InputText(src),
           sg.FileBrowse()],
          [sg.Text("Select column number for translation ", size=(35,1)), sg.InputCombo(['Select', 'Column 1', 'Column 2', 'Column 3', 'Column 4'], size=(20, 3))],
          [sg.Button("Translate", button_color=("white", "green"), size=(6, 1)),
           sg.Exit(button_color=("white", "red"), size=(6, 1))]]

window = sg.Window("Translation", layout, auto_size_text=True, size=(700,300), resizable=True, default_element_size=(40, 1))

while True:
    event, values = window.Read()
    column = 0
    if values[1] == 'Column 1':
        column = 0
    elif values[1] == 'Column 2':
        column = 1
    elif values[1] == 'Column 3':
        column = 2
    elif values[1] == 'Column 4':
        column = 3
    elif values[1] == 'Select':
        if values[0] != '':
            sg.PopupError("Select Proper Column Number...")
            continue
    if event in (None, 'Exit'):
        confirm = sg.PopupYesNo('Are You Sure ?')
        if confirm == 'Yes':
            break
        else:
            continue

    if event == 'Translate':
        
        translate(values[0], column)
        #sg.PopupAnimated(image_source=None)
        src_split = values[0].split('/')
        src_filename = src_split[-1]
        src_path = '/'
        src_path = "/".join(src_split[:len(src_split)-1])
        sg.PopupOK('Translation Successfully Completed. File is located at ' + src_path + "/translated_" + src_filename.split('.')[0] + '.xls')
window.Close()