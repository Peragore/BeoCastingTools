import time

import requests
import headtohead
import build_ticker
import threading
import PySimpleGUI as sg
from os import path
import ticker_server

if path.exists('results.txt'):
    f = open('results.txt', 'rt')
    text = f.read()
else:
    text = ''
col_1 = [[sg.Text('Enter Tournament pageid')],
         [sg.Text('Page ID'), sg.InputText(key='pageid')],
         [sg.Submit()]]

textbox = [[sg.Multiline(text, size=(100, 30), key='viewer')]]

layout = [
            [sg.Column(col_1),
             sg.Column(textbox)]
]

if __name__ == '__main__':

    window = sg.Window(title='BeoCastingTools', layout=layout, margins=(50, 50))

    has_clicked = False
    while True:
        event, values = window.read(timeout=60000)
        if event == sg.WIN_CLOSED:
            break
        if values['pageid'] != '' and has_clicked:
            build_ticker.build_ticker_ept_cups(values['pageid'])
        if event == 'Submit':
            build_ticker.build_ticker_ept_cups(values['pageid'])
            has_clicked = True
        if path.exists('results.txt'):
            f = open('results.txt', 'rt')
            text = f.read()
            window['viewer'].update(text)

    window.close()
    # test = headtohead.get_main_images('Lambo')
