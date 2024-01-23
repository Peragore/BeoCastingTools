import time

import requests

import GoogleHandler
import headtohead
import build_ticker
import threading
import PySimpleGUI as sg
from os import path
from threading import Thread
import HTMLDataHandler
if path.exists('results.txt'):
    f = open('results.txt', 'rt')
    text = f.read()
else:
    text = ''

EU_player_dict = {'Joona "Serral" Sotala': 'Zerg',
                  'Kevin "Harstem" de Koning': 'Protoss',
                  'Ivan "Wayne" Chepurnov': 'Zerg',
                  'Piotr "Spirit" Walukiewicz': 'Terran',
                  'Mikołaj "Elazer" Ogonowski': 'Zerg',
                  'Thomas "ShaDoWn" Labrousse': 'Protoss',
                  'Mateusz "Gerald" Budziak': 'Protoss',
                  'Krystian "Krystianer" Szczęsny': 'Protoss',
                  'Théo "PtitDrogo" Freydière': 'Protoss',
                  'Sven "BattleB" Kroth': 'Terran',
                  'Rubén "AqueroN" Villanueva': 'Terran',
                  'Adrien "DnS" Bouet': 'Protoss',
                  'Julian "ForJumy" Milz': 'Protoss',
                  'Tobias "ShoWTimE" Sieber': 'Protoss',
                  'Marvin "Spatz" Tiele': 'Protoss',
                  'Riccardo "Reynor" Romiti': 'Zerg',
                  'Gabriel "HeRoMaRinE" Segat': 'Terran',
                  'Julian "Lambo" Brosig': 'Zerg',
                  'Clément "Clem" Desplanches': 'Terran',
                  'Max "MaxPax" C.': 'Protoss',
                  'Nikita "SKillous" Gurevich': 'Protoss',
                  'Grzegorz "MaNa" Komincz': 'Protoss',
                  'Fabian "GunGFuBanDa" Mayer': 'Protoss',
                  'Leon "goblin" Vrhovec': 'Protoss',
                  'Aleksandr "Bly" Svysiuk': 'Zerg',
                  'Ilya "MilkiCow" Potapov': 'Terran',
                  'Oleksii "NightPhoenix" Zakharchuk': 'Protoss',
                  'Yakov "YoungYakov" Moiseenko': 'Zerg',
                  'Sylvain "Arrogfire" Joffre': 'Protoss',
                  'Tymoteusz "ArT" Makaran': 'Protoss',
                  'Michał "PAPI" Królikowski': 'Protoss',
                  'Vitaliy "Nicoract" Mishin': 'Terran'}

ASIA_player_dict = {'Li "Oliveira" Peinan': 'Terran',
                    'Xiang "XY" Yao': 'Terran',
                    'Huang "Nice" Shiang': 'Protoss',
                    'Wu "Coffee" Yishen': 'Terran',
                    'Ke "Has" Feng': 'Protoss',
                    'Tran "MeomaikA" Phuc': 'Zerg',
                    'Huang "Cyan" Min': 'Protoss',
                    'Hu "Jieshi" Jiajun': 'Protoss',
                    'Xue "Firefly" Tao': 'Protoss',
                    'Wang "Nanami" Le': 'Protoss',
                    'Hu "MacSed" Xiang': 'Protoss',
                    'Kwok "GogojOey" Yin': 'Zerg',
                    'Du "Oriana" Junhao': 'Terran',
                    'Haseeb "TeebuL" Ishaq': 'Protoss',
                    'Luan "SCV" Jiaqi': 'Protoss',
                    'Yin "Silky" Yongxin': 'Zerg'}

AM_player_dict = {'Juan "SpeCial" Lopez': 'Terran',
                  'Max "Astrea" Angel': 'Protoss',
                  'Pablo "Cham" Blanco': 'Zerg',
                  'Sasha "Scarlett" Hostyn': 'Zerg',
                  'Diego "Kelazhur" Schwimer': 'Terran',
                  'Yoon "trigger" Hong': 'Protoss',
                  'Alexandre "DisK" Corriveau': 'Protoss',
                  'Joseph "Future" Stanish': 'Terran',
                  'Paul "Dolan" Dolan': 'Terran',
                  'Maru "MaSa" Kim': 'Terran',
                  'Alison "Nina" Qual': 'Protoss',
                  'Sebastián "eGGz" Latorre': 'Zerg',
                  'Erik "Erik" Braga Bermelho': 'Zerg',
                  'Corey "Ukko" Merritt': 'Zerg',
                  'Chris "MCanning" Canning': 'Protoss',
                  'Matt "FoxeR" Harris': 'Terran'}
player_names = {**EU_player_dict, **ASIA_player_dict}
player_names_dict = {**player_names,**AM_player_dict}
player_names = list(player_names_dict.keys())
col_1 = [[sg.Text('Enter Tournament pageid')],
         [sg.Text('Page ID'), sg.InputText(key='pageid')],
         [sg.Text('Buffer Text'), sg.InputText(key='prepend')],
         [sg.Submit(button_text='Start', key='Start'), sg.Submit(button_text='Stop', key='Stop'),
          sg.Combo(['EPT Cups', 'ESL Masters'], default_value='EPT Cups', key='dropdown')],
         [sg.Text('Player A'), sg.Combo(player_names, default_value=player_names[0],
                                        size=(30, 1), key='playera_dropdown')],
          [sg.Text('Player B'), sg.Combo(player_names, default_value=player_names[0],
                                        size=(30, 1), key='playerb_dropdown')],
         [sg.Submit(button_text='Generate H2H', key='h2h')]]

textbox = [[sg.Multiline(text, size=(100, 30), key='viewer')]]

layout = [
            [sg.Column(col_1),
             sg.Column(textbox)]
]

if __name__ == '__main__':
    window = sg.Window(title='BeoCastingTools', layout=layout, margins=(50, 50))
    # ServerHost.start_server()
    HTMLDataHandler.HTMLDataHandler()
    has_clicked = False
    while True:
        event, values = window.read(timeout=500)
        if event == sg.WIN_CLOSED:
            break
        if event == 'Stop':
            window[event].Update(button_color='black')
            window['Start'].Update(button_color='dark blue')
            has_clicked = False

        if values['pageid'] != '' and has_clicked and values['dropdown'] == 'EPT Cups':

            if not t.is_alive():
                t = Thread(target=build_ticker.build_ticker_ept_cups,
                           args=(values['pageid'],),
                           kwargs={'prepend': values['prepend']},
                           daemon=True)
                t.start()

        elif values['pageid'] != '' and has_clicked and values['dropdown'] == 'ESL Masters':
            if not t.is_alive():
                t = Thread(target=GoogleHandler.gen_standings(),
                           kwargs={'threaded': True},
                           daemon=True)
                t.start()
        if event == 'Start':
            if values['dropdown'] == 'EPT Cups':
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
            elif values['dropdown'] == 'ESL Masters':
                # try:
                    t = Thread(target=GoogleHandler.gen_standings(),
                               kwargs={'threaded': True},
                               daemon=True)
                    t.start()
                    window[event].Update(button_color='black')
                    window['Stop'].Update(button_color='dark blue')
                # except:
                #     print('Invalid Pageid')

            has_clicked = True
        if event == 'h2h':
            GoogleHandler.gen_H2H(values['playera_dropdown'], values['playerb_dropdown'],
                                  player_names_dict[values['playera_dropdown']], player_names_dict[values['playerb_dropdown']])
        if path.exists('results.txt'):
            f = open('results.txt', 'rt')
            text = f.read()
            window['viewer'].update(text)

    window.close()
