import urllib.parse
import json
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import requests
from os import path
from shutil import copyfile
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
with open('keys/gsheets.txt', 'r') as f:
    google_key = f.read()

SPREADSHEET_ID = google_key
creds = None

try:
    wd = sys._MEIPASS
except:
    wd = os.getcwd()

token_path = os.path.join(wd, 'creds\\token.json')
creds_path = os.path.join(wd, 'creds\\credentials.json')

EU_player_dict = {'Serral': '../../img/ESL_Masters/Zerg_icone.png',
                  'Harstem': '../../img/ESL_Masters/Protoss_icone.png',
                  'Wayne': '../../img/ESL_Masters/Zerg_icone.png',
                  'Spirit': '../../img/ESL_Masters/Terran_icone.png',
                  'Elazer': '../../img/ESL_Masters/Zerg_icone.png',
                  'ShaDoWn': '../../img/ESL_Masters/Protoss_icone.png',
                  'Gerald': '../../img/ESL_Masters/Protoss_icone.png',
                  'Krystianer': '../../img/ESL_Masters/Protoss_icone.png',
                  'PtitDrogo': '../../img/ESL_Masters/Protoss_icone.png',
                  'BattleB': '../../img/ESL_Masters/Terran_icone.png',
                  'AqueroN': '../../img/ESL_Masters/Terran_icone.png',
                  'DnS': '../../img/ESL_Masters/Protoss_icone.png',
                  'ForJumy': '../../img/ESL_Masters/Protoss_icone.png',
                  'ShoWTimE': '../../img/ESL_Masters/Protoss_icone.png',
                  'Kas': '../../img/ESL_Masters/Terran_icone.png',
                  'Spatz': '../../img/ESL_Masters/Protoss_icone.png',
                  'Reynor': '../../img/ESL_Masters/Zerg_icone.png',
                  'HeroMarine': '../../img/ESL_Masters/Terran_icone.png',
                  'Lambo': '../../img/ESL_Masters/Zerg_icone.png',
                  'Clem': '../../img/ESL_Masters/Terran_icone.png',
                  'MaxPax': '../../img/ESL_Masters/Protoss_icone.png',
                  'SKillous': '../../img/ESL_Masters/Protoss_icone.png',
                  'MaNa': '../../img/ESL_Masters/Protoss_icone.png',
                  'GunGFuBanDa': '../../img/ESL_Masters/Protoss_icone.png',
                  'goblin': '../../img/ESL_Masters/Protoss_icone.png',
                  'Hellraiser': '../../img/ESL_Masters/Protoss_icone.png',
                  'KingCobra': '../../img/ESL_Masters/Protoss_icone.png',
                  'Bly': '../../img/ESL_Masters/Zerg_icone.png',
                  'Strange': '../../img/ESL_Masters/Protoss_icone.png',
                  'Milkicow': '../../img/ESL_Masters/Terran_icone.png',
                  'NightPhoenix': '../../img/ESL_Masters/Protoss_icone.png',
                  'YoungYakov': '../../img/ESL_Masters/Zerg_icone.png',
                  'arrogfire': '../../img/ESL_Masters/Protoss_icone.png',
                  'ArT': '../../img/ESL_Masters/Protoss_icone.png',
                  'PAPl': '../../img/ESL_Masters/Protoss_icone.png',
                  'Nicoract': '../../img/ESL_Masters/Terran_icone.png'}

ASIA_player_dict = {'Oliveira': '../../img/ESL_Masters/Terran_icone.png',
                    'XY': '../../img/ESL_Masters/Terran_icone.png',
                    'Nice': '../../img/ESL_Masters/Protoss_icone.png',
                    'Coffee': '../../img/ESL_Masters/Terran_icone.png',
                    'Has': '../../img/ESL_Masters/Protoss_icone.png',
                    'MeomaikA': '../../img/ESL_Masters/Zerg_icone.png',
                    'Cyan': '../../img/ESL_Masters/Protoss_icone.png',
                    'Rex': '../../img/ESL_Masters/Zerg_icone.png',
                    'Jieshi': '../../img/ESL_Masters/Protoss_icone.png',
                    'Firefly': '../../img/ESL_Masters/Protoss_icone.png',
                    'Nanami Chiaki': '../../img/ESL_Masters/Protoss_icone.png',
                    'MacSed': '../../img/ESL_Masters/Protoss_icone.png',
                    'GogojOey': '../../img/ESL_Masters/Zerg_icone.png',
                    'Oriana': '../../img/ESL_Masters/Terran_icone.png',
                    'TeebuL': '../../img/ESL_Masters/Protoss_icone.png',
                    'SCV': '../../img/ESL_Masters/Protoss_icone.png',
                    'Silky': '../../img/ESL_Masters/Zerg_icone.png'}

AM_player_dict = {'SpeCial': '../../img/ESL_Masters/Terran_icone.png',
                  'Astrea': '../../img/ESL_Masters/Protoss_icone.png',
                  'Cham': '../../img/ESL_Masters/Zerg_icone.png',
                  'Scarlett': '../../img/ESL_Masters/Zerg_icone.png',
                  'Kelazhur': '../../img/ESL_Masters/Terran_icone.png',
                  'trigger': '../../img/ESL_Masters/Protoss_icone.png',
                  'Vindicta': '../../img/ESL_Masters/Terran_icone.png',
                  'DisK': '../../img/ESL_Masters/Protoss_icone.png',
                  'Future': '../../img/ESL_Masters/Terran_icone.png',
                  'Dolan': '../../img/ESL_Masters/Terran_icone.png',
                  'MaSa': '../../img/ESL_Masters/Terran_icone.png',
                  'Nina': '../../img/ESL_Masters/Protoss_icone.png',
                  'PattyMac': '../../img/ESL_Masters/Protoss_icone.png',
                  'eGGz': '../../img/ESL_Masters/Zerg_icone.png',
                  'Erik': '../../img/ESL_Masters/Zerg_icone.png',
                  'Ukko': '../../img/ESL_Masters/Zerg_icone.png',
                  'MCanning': '../../img/ESL_Masters/Protoss_icone.png',
                  'FoxeR': '../../img/ESL_Masters/Terran_icone.png'}
if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'creds\\credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('creds\\token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('sheets', 'v4', credentials=creds)
except:
    DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = build('sheets', 'v4', credentials=creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)




def gen_standings(threaded=False):
    if threaded:
        time.sleep(2)

    sheet = service.spreadsheets()
    result_input = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = result_input['sheets']
    sheet_names = [x['properties']['title'] for x in sheets]
    eu1_standings = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                       range='Swiss Standings' + '!I5:N21').execute()
    eu2_standings = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                       range='Swiss Standings' + '!P5:U21').execute()
    asia_standings = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                        range='Swiss Standings' + '!B5:G21').execute()
    am_standings = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                      range='Swiss Standings' + '!W5:AB21').execute()

    eu1_values = eu1_standings['values']
    eu1_df = pd.DataFrame(eu1_values, columns=eu1_values[0])
    eu1_df = eu1_df.drop(eu1_df.index[0])

    eu2_values = eu2_standings['values']
    eu2_df = pd.DataFrame(eu2_values, columns=eu2_values[0])
    eu2_df = eu2_df.drop(eu2_df.index[0])

    asia_values = asia_standings['values']
    asia_df = pd.DataFrame(asia_values, columns=asia_values[0])
    asia_df = asia_df.drop(asia_df.index[0])

    am_values = am_standings['values']
    am_df = pd.DataFrame(am_values, columns=am_values[0])
    am_df = am_df.drop(am_df.index[0])

    eu1_results = {}
    eu2_results = {}
    asia_results = {}
    am_results = {}

    for index, row in eu1_df.iterrows():
        name = row['Player']
        series_score = row['Matches']
        map_score = row['Map W'] + '-' + row['Map L']
        pos = row['#']
        race = EU_player_dict[name]
        map_diff = int(row['Map W']) - int(row['Map L'])
        path = row['Streak']
        if map_diff >= 0:
            map_diff = '+' + str(map_diff)
        else:
            map_diff = str(map_diff)
        eu1_results[index] = {'Name': name, 'SeriesScore': series_score, 'MapScore': map_score, 'Pos': pos,
                              'Race': race, 'MapDiff': map_diff, 'Path': path}

    for index, row in eu2_df.iterrows():
        name = row['Player']
        series_score = row['Matches']
        map_score = row['Map W'] + '-' + row['Map L']
        pos = row['#']
        race = EU_player_dict[name]
        map_diff = int(row['Map W']) - int(row['Map L'])
        path = row['Streak']
        if map_diff >= 0:
            map_diff = '+' + str(map_diff)
        else:
            map_diff = str(map_diff)
        eu2_results[index] = {'Name': name, 'SeriesScore': series_score, 'MapScore': map_score, 'Pos': pos,
                              'Race': race, 'MapDiff': map_diff, 'Path': path}

    for index, row in asia_df.iterrows():
        name = row['Player']
        series_score = row['Matches']
        map_score = row['Map W'] + '-' + row['Map L']
        pos = row['#']
        race = ASIA_player_dict[name]
        map_diff = int(row['Map W']) - int(row['Map L'])
        path = row['Streak']
        if map_diff >= 0:
            map_diff = '+' + str(map_diff)
        else:
            map_diff = str(map_diff)
        asia_results[index] = {'Name': name, 'SeriesScore': series_score, 'MapScore': map_score, 'Pos': pos,
                              'Race': race, 'MapDiff': map_diff, 'Path': path}

    for index, row in am_df.iterrows():
        name = row['Player']
        series_score = row['Matches']
        map_score = row['Map W'] + '-' + row['Map L']
        pos = row['#']
        race = AM_player_dict[name]
        map_diff = int(row['Map W']) - int(row['Map L'])
        path = row['Streak']
        if map_diff >= 0:
            map_diff = '+' + str(map_diff)
        else:
            map_diff = str(map_diff)
        am_results[index] = {'Name': name, 'SeriesScore': series_score, 'MapScore': map_score, 'Pos': pos,
                              'Race': race, 'MapDiff': map_diff, 'Path': path}

    with open('json/eu1_results.json', 'w') as f:
        json.dump(eu1_results, f)
    f.close()
    with open('json/eu2_results.json', 'w') as f:
        json.dump(eu2_results, f)
    f.close()
    with open('json/asia_results.json', 'w') as f:
        json.dump(asia_results, f)
    f.close()
    with open('json/am_results.json', 'w') as f:
        json.dump(am_results, f)
    f.close()

def gen_H2H(player1, player2, race1, race2):
    player1_cut = player1.split('"')[1]
    player2_cut = player2.split('"')[1]

    sheet = service.spreadsheets()
    result_input = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = result_input['sheets']
    sheet_names = [x['properties']['title'] for x in sheets]
    eu1_standings = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                       range='Swiss Standings' + '!I5:N21').execute()
    eu2_standings = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                       range='Swiss Standings' + '!P5:U21').execute()
    asia_standings = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                        range='Swiss Standings' + '!B5:G21').execute()
    am_standings = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                      range='Swiss Standings' + '!W5:AB21').execute()

    eu1_values = eu1_standings['values']
    eu1_df = pd.DataFrame(eu1_values, columns=eu1_values[0])
    eu1_df = eu1_df.drop(eu1_df.index[0])

    eu2_values = eu2_standings['values']
    eu2_df = pd.DataFrame(eu2_values, columns=eu2_values[0])
    eu2_df = eu2_df.drop(eu2_df.index[0])

    asia_values = asia_standings['values']
    asia_df = pd.DataFrame(asia_values, columns=asia_values[0])
    asia_df = asia_df.drop(asia_df.index[0])

    am_values = am_standings['values']
    am_df = pd.DataFrame(am_values, columns=am_values[0])
    am_df = am_df.drop(am_df.index[0])
    combined_df = pd.concat([am_df, eu1_df, eu2_df, asia_df])
    h2h_gen = {}
    for index, row in combined_df.iterrows():
        if row['Player'].lower() == player1_cut.lower():
            h2h_gen['1'] = {'Name': player1, 'Streak': row['Streak'], 'Race': race1}
        if row['Player'].lower() == player2_cut.lower():
            h2h_gen['2'] = {'Name': player2, 'Streak': row['Streak'], 'Race': race2}


    with open('json/h2h.json', 'w') as f:
        json.dump(h2h_gen, f)
    f.close()
