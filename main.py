import time

import requests
import headtohead
import build_ticker
import threading
import PySimpleGUI as sg
from os import path

if path.exists('results.txt'):
    f = open('results.txt', 'rt')
    text = f.read()
else:
    text = ''
col_1 = [[sg.Text('Enter Tournament pageid')],
         [sg.Text('Page ID'), sg.InputText(key='pageid')],
         [sg.Text('Buffer Text'), sg.InputText(key='prepend')],
         [sg.Submit(button_text='Start', key='Start'), sg.Submit(button_text='Stop', key='Stop'), sg.Combo(['EPT Cups', 'DH EU', 'DH NA'], default_value='EPT Cups', key='dropdown')]]

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
        if event == 'Stop':
            window[event].Update(button_color='black')
            window['Start'].Update(button_color='dark blue')
            has_clicked = False
        if values['pageid'] != '' and has_clicked and values['dropdown'] == 'DH EU':
            build_ticker.build_ticker_DH_EU_groups(values['pageid'], values['prepend'])
        elif values['pageid'] != '' and has_clicked and values['dropdown'] == 'EPT Cups':
            build_ticker.build_ticker_ept_cups(values['pageid'], values['prepend'])
        elif values['pageid'] != '' and has_clicked and values['dropdown'] == 'NA Cups':
            build_ticker.build_ticker_DH_NA_groups(values['pageid'], values['prepend'])

        if event == 'Start':

            if values['dropdown'] == 'DH EU':
                try:
                    build_ticker.build_ticker_DH_EU_groups(values['pageid'], values['prepend'])
                    window[event].Update(button_color='black')
                    window['Stop'].Update(button_color='dark blue')
                except:
                    print('Invalid pageid')

            elif values['dropdown'] == 'EPT Cups':
                try:
                    build_ticker.build_ticker_ept_cups(values['pageid'], values['prepend'])
                    window[event].Update(button_color='black')
                    window['Stop'].Update(button_color='dark blue')
                except:
                    print('Invalid Pageid')
            elif values['dropdown'] == 'DH NA':
                try:
                    build_ticker.build_ticker_DH_NA_groups(values['pageid'], values['prepend'])
                    window[event].Update(button_color='black')
                    window['Stop'].Update(button_color='dark blue')
                except:
                    print('Invalid Pageid')

            has_clicked = True
        if path.exists('results.txt'):
            f = open('results.txt', 'rt')
            text = f.read()
            window['viewer'].update(text)

    window.close()
