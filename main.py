import time

import requests
import headtohead
import build_ticker
import threading
import PySimpleGUI as sg
from os import path
from threading import Thread
import ServerHost
if path.exists('results.txt'):
    f = open('results.txt', 'rt')
    text = f.read()
else:
    text = ''
col_1 = [[sg.Text('Enter Tournament pageid')],
         [sg.Text('Page ID'), sg.InputText(key='pageid')],
         [sg.Text('Buffer Text'), sg.InputText(key='prepend')],
         [sg.Submit(button_text='Start', key='Start'), sg.Submit(button_text='Stop', key='Stop'),
          sg.Combo(['EPT Cups', 'KRO36', 'DH EU', 'DH NA', 'KOB'], default_value='EPT Cups', key='dropdown')]]

textbox = [[sg.Multiline(text, size=(100, 30), key='viewer')]]

layout = [
            [sg.Column(col_1),
             sg.Column(textbox)]
]

if __name__ == '__main__':
    window = sg.Window(title='BeoCastingTools', layout=layout, margins=(50, 50))
    # ServerHost.start_server()
    ServerHost.ServerHost()
    has_clicked = False
    while True:
        event, values = window.read(timeout=500)
        if event == sg.WIN_CLOSED:
            break
        if event == 'Stop':
            window[event].Update(button_color='black')
            window['Start'].Update(button_color='dark blue')
            has_clicked = False
        if values['pageid'] != '' and has_clicked and values['dropdown'] == 'DH EU':
            if not t.is_alive():
                t = Thread(target=build_ticker.build_ticker_DH_EU_groups,
                           args=(values['pageid'],),
                           kwargs={'prepend': values['prepend']},
                           daemon=True)
                t.start()

        elif values['pageid'] != '' and has_clicked and values['dropdown'] == 'EPT Cups':

            if not t.is_alive():
                t = Thread(target=build_ticker.build_ticker_ept_cups,
                           args=(values['pageid'],),
                           kwargs={'prepend': values['prepend']},
                           daemon=True)
                t.start()
        elif values['pageid'] != '' and has_clicked and values['dropdown'] == 'DH NA':
            if not t.is_alive():
                t = Thread(target=build_ticker.build_ticker_DH_NA_groups,
                           args=(values['pageid'],),
                           kwargs={'prepend': values['prepend']},
                           daemon=True)
                t.start()
        elif values['pageid'] != '' and has_clicked and values['dropdown'] == 'KRO36':
            if not t.is_alive():
                t = Thread(target=build_ticker.build_ticker_Katowice_RO36,
                           args=(values['pageid'],),
                           kwargs={'prepend': values['prepend']},
                           daemon=True)
                t.start()
        if event == 'Start':

            if values['dropdown'] == 'DH EU':
                try:
                    t = Thread(target=build_ticker.build_ticker_DH_EU_groups,
                               args=(values['pageid'], ),
                               kwargs={'prepend': values['prepend']},
                               daemon=True)
                    t.start()
                    window[event].Update(button_color='black')
                    window['Stop'].Update(button_color='dark blue')
                except:
                    print('Invalid pageid')

            elif values['dropdown'] == 'EPT Cups':
                try:
                    t = Thread(target=build_ticker.build_ticker_ept_cups,
                               args = (values['pageid'],),
                               kwargs={'prepend': values['prepend']},
                               daemon=True)
                    t.start()
                    window[event].Update(button_color='black')
                    window['Stop'].Update(button_color='dark blue')
                except:
                    print('Invalid Pageid')
            elif values['dropdown'] == 'DH NA':
                try:
                    t = Thread(target=build_ticker.build_ticker_DH_NA_groups,
                               args = (values['pageid'],),
                               kwargs={'prepend': values['prepend']},
                               daemon=True)
                    t.start()
                    window[event].Update(button_color='black')
                    window['Stop'].Update(button_color='dark blue')
                except:
                    print('Invalid Pageid')
            elif values['dropdown'] == 'KRO36':
                try:
                    t = Thread(target=build_ticker.build_ticker_Katowice_RO36,
                               args=(values['pageid'],),
                               kwargs={'prepend': values['prepend']},
                               daemon=True)
                    t.start()
                    window[event].Update(button_color='black')
                    window['Stop'].Update(button_color='dark blue')
                except:
                    print('Invalid Pageid')

            elif values['dropdown'] == 'KOB':
                build_ticker.build_kob_ticker()

            has_clicked = True
        if path.exists('results.txt'):
            f = open('results.txt', 'rt')
            text = f.read()
            window['viewer'].update(text)

    window.close()
