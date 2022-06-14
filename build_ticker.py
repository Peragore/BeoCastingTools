import requests
import re
import datetime
from dateutil import parser
import time
from PIL import Image, ImageDraw, ImageFont
import urllib.parse


from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle


HEADER = {'User-Agent': 'Live Match Results Ticker (beomulf@gmail.com)'}

S = requests.Session()

URL = "https://liquipedia.net/starcraft2/api.php"
HEADER = {'User-Agent': 'Live Match Results Ticker (beomulf@gmail.com)'}
TIMEZONES = {'CEST': '+02:00', 'EDT': '-04:00'}
RACELIBRARY = {'T': 'Terran', 'P': 'Protoss', 'Z': 'Zerg', 'R': 'Random'}


def build_ticker_DH_NA_groups(pageid, prepend=''):
    params = {
        'action': "parse",
        'pageid': pageid,
        'prop': 'wikitext',
        'section': 6,
        'format': "json"
    }
    """ Parse a section of a page, fetch its table data and save it to a CSV file
    """
    res = S.get(url=URL, params=params, headers=HEADER)
    data = res.json()
    wikitext = data['parse']['wikitext']['*']
    lines = wikitext.split('|-')
    matches = {}

    table = lines[0].split('{{HiddenSort')
    del table[0]
    for group in table:
        match_list = re.split('\|M[0-9]|<', group)
        group_name = group[1:8] + ' | '
        del match_list[0]
        player_names = re.split('\|p[0-9]=', group)
        del player_names[0]
        player_names_list = [x.split('|')[0].split('=') for x in player_names[0:8]]
        player_names_list = [x[0] for x in player_names_list]
        results_dict = dict.fromkeys(player_names_list)
        for key in player_names_list:
            results_dict[key] = {'Map Diff': 0, 'Map Wins': 0, 'Map Losses': 0, 'Match Wins': 0, 'Match Losses': 0}

        matches[group_name] = []
        for match in match_list:
            if 'opponent1' in match:
                if 'bestof=5' in match:
                    break
                subseries = match.split('    ')
                dateinfo = match.split('date=')[1].split('|')[0]
                date = dateinfo.split('{{')
                date = date[0] + re.sub('[a-z |{|}|\/]', '', date[1]).replace('\n', '')
                for zone, offset in TIMEZONES.items():
                    try:
                        date = date.replace(zone, offset)
                    except:
                        print('Invalid Timezone')

                date = parser.parse(date)
                currentTime = datetime.datetime.now(datetime.timezone.utc).astimezone()
                timeDiff = abs(currentTime-date)
                timeDiff = timeDiff.days * 24 + timeDiff.seconds // 3600
                manual_score_flag = False

                p1_score = 0
                p2_score = 0
                for line in subseries:
                    if 'opponent1' in line:
                        if re.search('\|1=', line):
                            p1 = line.split('|1=')[-1].split('|')[0].replace('}}\n', '')
                        else:
                            p1 = line.split('|')[2].replace('}}\n', '').split('p1=')[0]
                        if 'score' in line:
                            p1_score = line.split('score=')[1].split('}')[0]
                        else:
                            manual_score_flag = True
                    elif 'opponent2' in line:
                        if re.search('\|1=', line):
                            p2 = line.split('|1=')[-1].split('|')[0].replace('}}\n', '')
                        else:
                            p2 = line.split('|')[2].replace('}}\n', '').split('p1=')[0]
                        if 'score' in line:
                            p2_score = line.split('score=')[1].split('}')[0]
                        else:
                            manual_score_flag = True
                    if 'walkover=1' in line:
                        p1_score = 'W'
                        p2_score = 'L'
                    elif 'walkover=2' in line:
                        p1_score = 'L'
                        p2_score = 'W'
                    elif manual_score_flag and 'winner' in line:
                        winner_id = line.split('winner=')[1].split('}')[0].partition('|')
                        winner_id = winner_id[0]
                        if winner_id == '1':
                            p1_score += 1
                        elif winner_id == '2':
                            p2_score += 1

                if p1_score == '':
                    p1_score = '0'
                if p2_score == '':
                    p2_score = '0'
                if p1 not in results_dict:
                    results_dict[p1] = {'Map Diff': 0, 'Map Wins': 0, 'Map Losses': 0, 'Match Wins': 0,
                                         'Match Losses': 0}
                if p2 not in results_dict:
                    results_dict[p2] = {'Map Diff': 0, 'Map Wins': 0, 'Map Losses': 0, 'Match Wins': 0,
                                         'Match Losses': 0}
                results_dict[p1]['Map Wins'] += p1_score
                results_dict[p2]['Map Wins'] += p2_score
                results_dict[p1]['Map Losses'] += p2_score
                results_dict[p2]['Map Losses'] += p1_score
                results_dict[p1]['Map Diff'] += p1_score - p2_score
                results_dict[p2]['Map Diff'] += p2_score - p1_score
                if p1_score >= 2 or p2_score >= 2:
                    if p1_score > p2_score:
                        results_dict[p1]['Match Wins'] += 1
                        results_dict[p2]['Match Losses'] += 1
                    if p2_score > p1_score:
                        results_dict[p2]['Match Wins'] += 1
                        results_dict[p1]['Match Losses'] += 1

                if timeDiff < 10:
                    if p1 != '':
                        if p1 != 'BYE' and p2 != 'BYE':
                            matches[group_name].append(
                                ' ' + p1 + ' ' + str(p1_score) + '-' + str(p2_score) + ' ' + p2 + '    ')
                        elif p1 == 'BYE':
                            matches[group_name].append(' ' + p2 + ' (Bye) ')
                        elif p2 == 'BYE':
                            matches[group_name].append(' ' + p1 + ' (Bye) ')
                    if p1 == '':
                        p1 = 'TBD'
                    if p2 == '':
                        p2 = 'TBD'

        generate_group_standings_img(group_name, results_dict)

    matchlist = []
    for key in matches.keys():
        if matches[key] != []:
            if prepend != '':
                matchlist.append('  |  ' + prepend + '  |  ')

            matchlist.append(key + ''.join(matches[key]))

    matchstr = ''.join(matchlist)
    with open('results.txt', 'w') as output:
        output.write(matchstr)
    print('Populated Results')
    time.sleep(40)


def build_ticker_ept_cups(pageid, prepend=''):
    # TODO: Generalize function to all events
    # TODO: convert match_list to dictionary so we can bump less useful results
    # TODO: add gui to plug in pageid
    # TODO: loop every 30s to reduce user overhead
    params = {
        'action': "parse",
        'pageid': pageid,
        'prop': 'wikitext',
        'format': "json",
        'Accept-Encoding': 'gzip'
    }

    """ Parse a section of a page, fetch its table data and save it to a CSV file
    """
    res = S.get(url=URL, params=params, headers=HEADER)
    data = res.json()
    wikitext = data['parse']['wikitext']['*']
    lines = wikitext.split('|-')
    matches = []
    rounds = {}

    table = lines[0].split('==Results==')
    del table[0]
    table = re.split('\|R[0-9]', table[0])
    prev_series = 100
    round_tracker = 0

    for series in table:
        if '{{bracket' not in series:
            if 'header' in series:
                header = series.split('=')[1].split('({{')
                rounds[str(header[0])] = header[1].split('|')[1].replace('}})\n', '').split('\n')[0]
            elif re.search('M[0-9]', series):
                round_keys = list(rounds.keys())
                subseries = series.split('    ')
                series_num = int(subseries[0].split('M')[1].split('=')[0])
                manual_score_flag = False
                p1_score = 0
                p2_score = 0
                for line in subseries:
                    if 'opponent1' in line:
                        if re.search('\|1=', line):
                            p1 = line.split('|1=')[-1].split('|')[0].replace('}}\n', '')
                        else:
                            p1 = line.split('|')[2].replace('}}\n', '')
                        if 'score' in line:
                            p1_score = line.split('score=')[1].split('}')[0]
                        else:
                            manual_score_flag = True
                    elif 'opponent2' in line:
                        if re.search('\|1=', line):
                            p2 = line.split('|1=')[-1].split('|')[0].replace('}}\n', '')
                        else:
                            p2 = line.split('|')[2].replace('}}\n', '')
                        if 'score' in line:
                            p2_score = line.split('score=')[1].split('}')[0]
                        else:
                            manual_score_flag = True
                    if 'walkover=1' in line:
                        p1_score = 'W'
                        p2_score = 'L'
                    elif 'walkover=2' in line:
                        p1_score = 'L'
                        p2_score = 'W'
                    elif manual_score_flag and 'winner' in line:
                        winner_id = line.split('winner=')[1].split('}')[0].partition('|')
                        winner_id = winner_id[0]
                        if winner_id == '1':
                            p1_score += 1
                        elif winner_id == '2':
                            p2_score += 1
                if series_num < prev_series and p1 != '':
                    key = str(round_keys[round_tracker])
                    matches.append('| ' + key + ' (BO ' + rounds[key] + ') :')
                    round_tracker += 1
                if p1_score == '':
                    p1_score = '0'
                if p2_score == '':
                    p2_score = '0'
                if p1 == '' and p2 != '':
                    p1 = 'TBD'
                if p2 == '' and p1 != '':
                    p2 = 'TBD'
                if p1 != '':
                    if p1 != 'BYE' and p2 != 'BYE':
                        matches.append(' ' + p1 + ' ' + str(p1_score) + '-' + str(p2_score) + ' ' + p2 + '    ')
                    elif p1 == 'BYE':
                        matches.append(' ' + p2 + ' (Bye) ')
                    elif p2 == 'BYE':
                        matches.append(' ' + p1 + ' (Bye) ')

                prev_series = series_num
    matchstr = ' '.join(matches)
    if 'Quarterfinals  (BO 3)' in matchstr:
        matchstr = matchstr[matchstr.index('| Quarterfinals  (BO 3)'):]
    if prepend != '':
        prepend = '  |  ' + prepend
    matchstr = prepend + matchstr

    while len(matchstr) < 100 and len(matchstr) != 0:
        matchstr += matchstr

    with open('results.txt', 'w') as output:
        output.write(matchstr)
    print('Populated Results')
    time.sleep(40)


def build_ticker_DH_EU_groups(pageid, prepend=''):
    # TODO: Generalize function to all events
    # TODO: convert match_list to dictionary so we can bump less useful results
    # TODO: add gui to plug in pageid
    # TODO: loop every 30s to reduce user overhead
    params = {
        'action': "parse",
        'pageid': pageid,
        'prop': 'wikitext',
        'format': "json",
        'Accept-Encoding': 'gzip'
    }

    """ Parse a section of a page, fetch its table data and save it to a CSV file
    """
    res = S.get(url=URL, params=params, headers=HEADER)
    data = res.json()
    wikitext = data['parse']['wikitext']['*']
    lines = wikitext.split('|-')
    matches = []
    rounds = {}

    lines = lines[-1]
    lines = lines.split('Toggle group')[1]
    group_table = lines.split('{{:')
    new_groups = group_table[0].split('{{Matchlist')
    group_names = [x.split('}')[0] for x in new_groups[1:len(new_groups)]]

    prev_series = 100
    round_tracker = 0
    matches = {}
    for group in group_names:
        print(group)
        time.sleep(40)
        HEADER_GROUPS = {'User-Agent': f'Live Match Results Ticker {group} (beomulf@gmail.com)'}


        group_params = {
            'action': "parse",
            'page': group,
            'prop': 'wikitext',
            'format': "json",
            'Accept-Encoding': 'gzip'
        }
        res = S.get(url=URL, params=group_params, headers=HEADER_GROUPS)
        data = res.json()
        wikitext = data['parse']['wikitext']['*']
        lines = wikitext.split('|-')
        group_data = lines[-1]
        player_names = re.split('\|p[0-9]=', group_data)
        del player_names[0]
        # if 'bg' in group:
        #     player_names = re.split('\|p[0-9]=', group_data)
        player_names_list = [x.split('\n')[0].split('=') for x in player_names[0:8]]
        player_names_list = [x[0] for x in player_names_list]
        results_dict = dict.fromkeys(player_names_list)
        for key in player_names_list:
            results_dict[key] = {'Map Diff': 0, 'Map Wins': 0, 'Map Losses': 0, 'Match Wins': 0, 'Match Losses': 0}

        table = re.split('\|M[0-9]|<', group_data)
        for match in table:
            if '{{HiddenSort' in match:
                group_name = match.split('|')[1].split('}}')[0] + ' | '
                matches[group_name] = []
            elif 'header' not in match and 'opponent1' in match:
                if 'bestof=5' in match:
                    break
                date_info = match.split('|')
                date = [x for x in date_info if 'date' in x]
                date = date[0].split('=')[1].split('{{')
                date = date[0] + re.sub('[a-z |{|}|\/]', '', date[1]).replace('\n', '')
                date = date.replace('A', '')
                for zone, offset in TIMEZONES.items():
                    try:
                        date = date.replace(zone, offset)
                    except:
                        print('Invalid Timezone')

                date = parser.parse(date)
                currentTime = datetime.datetime.now(datetime.timezone.utc).astimezone()
                timeDiff = abs(currentTime - date)
                timeDiff = timeDiff.days * 24 + timeDiff.seconds // 3600

                subseries = match.split('    ')
                manual_score_flag = False
                p1_score = 0
                p2_score = 0

                for line in subseries:
                    if 'opponent1' in line:
                        if re.search('\|1=', line):
                            p1 = line.split('|1=')[-1].split('|')[0].replace('}}\n', '')
                        else:
                            p1 = line.split('|')[2].replace('}}\n', '').split('p1=')[1]
                        if 'score' in line:
                            p1_score = line.split('score=')[1].split('}')[0]
                        else:
                            manual_score_flag = True
                    elif 'opponent2' in line:
                        if re.search('\|1=', line):
                            p2 = line.split('|1=')[-1].split('|')[0].replace('}}\n', '')
                        else:
                            p2 = line.split('|')[2].replace('}}\n', '').split('p1=')[1]
                        if 'score' in line:
                            p2_score = line.split('score=')[1].split('}')[0]
                        else:
                            manual_score_flag = True
                    if 'walkover=1' in line:
                        p1_score = 'W'
                        p2_score = 'L'
                    elif 'walkover=2' in line:
                        p1_score = 'L'
                        p2_score = 'W'
                    elif manual_score_flag and 'winner' in line:
                        winner_id = line.split('winner=')[1].split('}')[0].partition('|')
                        winner_id = winner_id[0]
                        if winner_id == '1':
                            p1_score += 1
                        elif winner_id == '2':
                            p2_score += 1

                if p1_score == '':
                    p1_score = '0'
                if p2_score == '':
                    p2_score = '0'
                results_dict[p1]['Map Wins'] += p1_score
                results_dict[p2]['Map Wins'] += p2_score
                results_dict[p1]['Map Losses'] += p2_score
                results_dict[p2]['Map Losses'] += p1_score
                results_dict[p1]['Map Diff'] += p1_score-p2_score
                results_dict[p2]['Map Diff'] += p2_score-p1_score
                if p1_score >= 2 or p2_score >= 2:
                    if p1_score > p2_score:
                        results_dict[p1]['Match Wins'] += 1
                        results_dict[p2]['Match Losses'] += 1
                    if p2_score > p1_score:
                        results_dict[p2]['Match Wins'] += 1
                        results_dict[p1]['Match Losses'] += 1


                if timeDiff < 8:
                    if p1 != '':
                        if p1 != 'BYE' and p2 != 'BYE':
                            matches[group_name].append(' ' + p1 + ' ' + str(p1_score) + '-' + str(p2_score) + ' ' + p2 + '    ')
                        elif p1 == 'BYE':
                            matches[group_name].append(' ' + p2 + ' (Bye) ')
                        elif p2 == 'BYE':
                            matches[group_name].append(' ' + p1 + ' (Bye) ')
                    if p1 == '':
                        p1 = 'TBD'
                    if p2 == '':
                        p2 = 'TBD'

        generate_group_standings_img(group_name, results_dict)

    matchstr = ''
    for key in matches.keys():
        if matches[key] != []:
            matchstr += key + ''.join(matches[key])
    if prepend != '':
        matchstr = '  |  ' + prepend + '  |  ' + matchstr


    with open('results.txt', 'w') as output:
        output.write(matchstr)
    print('Populated Results')

def build_kob_ticker(mainstream_group='', offstream_group=''):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '1TX2a7CHmrJaaNvytF_iVUGPAD9ALnRhIJXrVjJelTDk'
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '../KoB_Toolsuite/credentials.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
    values_input = result_input.get('values', [])
    sheets = result_input.get('sheets', '')
    sheet_names = [x.get("properties", {}).get("title") for x in sheets]
    if mainstream_group == '':
        return sheet_names

def generate_group_standings_img(group_name, results_dict):
    img = Image.new('RGBA', (1920, 1080), color=(0, 0, 0, 0))
    img2 = Image.new('RGBA', (1920, 1080), color=(0, 0, 0, 0))
    fnt = ImageFont.truetype('Roboto-Bold.ttf', size=30)
    d = ImageDraw.Draw(img)
    d2 = ImageDraw.Draw(img2)

    ordered_results = sorted(results_dict, key=lambda x: (results_dict[x]['Match Wins'] - results_dict[x]['Match Losses'],
                                                          results_dict[x]['Map Diff'],
                                                          results_dict[x]['Map Wins']))
    # Player Names
    d.text((1260, 370), ordered_results[7], font=fnt, fill=(255, 255, 255))
    d.text((1260, 415), ordered_results[6], font=fnt, fill=(255, 255, 255))
    d.text((1260, 457), ordered_results[5], font=fnt, fill=(255, 255, 255))
    d.text((1260, 501), ordered_results[4], font=fnt, fill=(255, 255, 255))
    d.text((1260, 545), ordered_results[3], font=fnt, fill=(255, 255, 255))
    d.text((1260, 590), ordered_results[2], font=fnt, fill=(255, 255, 255))
    d.text((1260, 635), ordered_results[1], font=fnt, fill=(255, 255, 255))
    d.text((1260, 675), ordered_results[0], font=fnt, fill=(255, 255, 255))

    # Match Score
    d.text((1620, 375),
           str(results_dict[ordered_results[7]]['Match Wins']) + ' - ' + str(
               results_dict[ordered_results[7]]['Match Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1620, 420),
           str(results_dict[ordered_results[6]]['Match Wins']) + ' - ' + str(
               results_dict[ordered_results[6]]['Match Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1620, 464),
           str(results_dict[ordered_results[5]]['Match Wins']) + ' - ' + str(
               results_dict[ordered_results[5]]['Match Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1620, 509),
           str(results_dict[ordered_results[4]]['Match Wins']) + ' - ' + str(
               results_dict[ordered_results[4]]['Match Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1620, 553),
           str(results_dict[ordered_results[3]]['Match Wins']) + ' - ' + str(
               results_dict[ordered_results[3]]['Match Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1620, 597),
           str(results_dict[ordered_results[2]]['Match Wins']) + ' - ' + str(
               results_dict[ordered_results[2]]['Match Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1620, 640),
           str(results_dict[ordered_results[1]]['Match Wins']) + ' - ' + str(
               results_dict[ordered_results[1]]['Match Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1620, 683),
           str(results_dict[ordered_results[0]]['Match Wins']) + ' - ' + str(
               results_dict[ordered_results[0]]['Match Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')

    # Map Scores
    d.text((1820, 375),
           str(results_dict[ordered_results[7]]['Map Wins']) + ' - ' + str(
               results_dict[ordered_results[7]]['Map Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1820, 420),
           str(results_dict[ordered_results[6]]['Map Wins']) + ' - ' + str(
               results_dict[ordered_results[6]]['Map Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1820, 464),
           str(results_dict[ordered_results[5]]['Map Wins']) + ' - ' + str(
               results_dict[ordered_results[5]]['Map Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1820, 509),
           str(results_dict[ordered_results[4]]['Map Wins']) + ' - ' + str(
               results_dict[ordered_results[4]]['Map Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1820, 553),
           str(results_dict[ordered_results[3]]['Map Wins']) + ' - ' + str(
               results_dict[ordered_results[3]]['Map Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1820, 597),
           str(results_dict[ordered_results[2]]['Map Wins']) + ' - ' + str(
               results_dict[ordered_results[2]]['Map Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1820, 640),
           str(results_dict[ordered_results[1]]['Map Wins']) + ' - ' + str(
               results_dict[ordered_results[1]]['Map Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')
    d.text((1820, 683),
           str(results_dict[ordered_results[0]]['Map Wins']) + ' - ' + str(
               results_dict[ordered_results[0]]['Map Losses']),
           font=fnt, fill=(255, 255, 255), anchor='mt')

    img.save(group_name.split('|')[0].replace(' ', '') + '.png')

    fullscreen_start = 300
    score_start = 640
    maps_start = 815
    # Player Names
    name_vert_start = 730
    num_vert_start = 735
    counter = 0
    for result in ordered_results:
        d2.text((fullscreen_start, name_vert_start-counter*50), result, font=fnt, fill=(255, 255, 255))
        d2.text((score_start, num_vert_start-counter*50),
                str(results_dict[result]['Match Wins']) + ' - ' + str(results_dict[result]['Match Losses']),
                font=fnt,
                fill=(255, 255, 255),
                anchor='mt')
        d2.text((maps_start, num_vert_start-counter*50),
                str(results_dict[result]['Map Wins']) + ' - ' + str(results_dict[result]['Map Losses']),
                font=fnt,
                fill=(255, 255, 255),
                anchor='mt')
        counter += 1

    img2.save(group_name.split('|')[0].replace(' ', '') + '_FullScreen.png')

def get_aligulac_data(player_1, player_2):
    params_h2h = {'apikey': 'tqYfLrmkYGPG4CZVjCvO'}
    api_h2h_url = 'http://aligulac.com/api/v1/match/'
    api_id_url = 'http://aligulac.com/search/json/'
    params_id1 = {'q': player_1}
    params_id2 = {'q': player_2}
    id1_json = requests.get(api_id_url, params_id1).json()['players']
    id2_json = requests.get(api_id_url, params_id2).json()['players']
    id1_data = [x['id'] for x in id1_json if x['tag'].casefold() == player_1.casefold()][0]
    id2_data = [x['id'] for x in id2_json if x['tag'].casefold() == player_2.casefold()][0]
    id1_info = [x for x in id1_json if x['tag'].casefold() == player_1.casefold()][0]
    id2_info = [x for x in id2_json if x['tag'].casefold() == player_2.casefold()][0]

    player1_data = [player_1, RACELIBRARY[id1_info['race']], id1_info['teams'][0][0]]
    player2_data = [player_2, RACELIBRARY[id2_info['race']], id2_info['teams'][0][0]]

    params_h2h['pla__in'] = str(id1_data) + ',' + str(id2_data)
    params_h2h['plb__in'] = str(id1_data) + ',' + str(id2_data)
    params_h2h['limit'] = '100'
    params_str = urllib.parse.urlencode(params_h2h, safe=',')
    h2h_data = requests.get(api_h2h_url, params=params_str).json()
    player1_wins = 0
    player2_wins = 0
    for result in h2h_data['objects']:
        if result['game'].casefold() == 'lotv':
            if int(result['sca']) > int(result['scb']):
                if result['pla']['tag'].casefold() == player_1.casefold():
                    player1_wins += 1
                else:
                    player2_wins += 1
            elif int(result['sca']) < int(result['scb']):
                if result['plb']['tag'].casefold() == player_2.casefold():
                    player2_wins += 1
                else:
                    player1_wins += 1

    params_form = {'apikey': 'tqYfLrmkYGPG4CZVjCvO'}
    api_form_url = 'http://aligulac.com/api/v1/player/set/' + str(id1_data) + ';' + str(id2_data) + '/'
    form_data = requests.get(api_form_url, params_form).json()

    p1_form = form_data['objects'][0]['form'][form_data['objects'][1]['race']]
    p2_form = form_data['objects'][1]['form'][form_data['objects'][0]['race']]

    p1_form = p1_form[0] / (p1_form[1] + p1_form[0]) * 100
    p2_form = p2_form[0] / (p2_form[1] + p2_form[0]) * 100

    p1_form = '{:.2f}%'.format(p1_form)
    p2_form = '{:.2f}%'.format(p2_form)
    player1_data.append(p1_form)
    player1_data.append(str(player1_wins))
    player2_data.append(p2_form)
    player2_data.append(str(player2_wins))

    return [player1_data, player2_data]


