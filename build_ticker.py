import requests
import re
import datetime
from dateutil import parser
import json
import time

HEADER = {'User-Agent': 'Live Match Results Ticker (beomulf@gmail.com)'}

S = requests.Session()

URL = "https://liquipedia.net/starcraft2/api.php"
HEADER = {'User-Agent': 'Live Match Results Ticker (beomulf@gmail.com)'}
TIMEZONES = {'CEST': '+02:00', 'EDT': '-04:00'}


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
    matches = []

    table = lines[0].split('{{HiddenSort')
    del table[0]
    for group in table:
        match_list = re.split('\|M[0-9]|<', group)
        group_name = group[1:8] + ' | '

        matches.append(group_name)
        for match in match_list[2:len(match_list)]:
            if 'header' not in match and 'opponent1' in match:
                if 'bestof=5' in match:
                    break
                match = match.split('|')
                date = [x for x in match if 'date' in x]
                date = date[0].split('=')[1].split('{{')
                date = date[0] + re.sub('[a-z |{|}|\/]', '', date[1]).replace('\n', '')
                for zone, offset in TIMEZONES.items():
                    try:
                        date = date.replace(zone, offset)
                    except:
                        print('Invalid Timezone')

                date = parser.parse(date)
                currentTime = datetime.datetime.now()
                currentTime = currentTime.replace(tzinfo=datetime.timezone.utc)
                timeDiff = abs(currentTime-date)
                timeDiff = timeDiff.days * 24 + timeDiff.seconds // 3600
                if timeDiff < 8:
                    p1 = match[4]
                    p2 = match[6]
                    p1 = p1.replace('}}\n    ', '').replace('p1=', '')
                    p2 = p2.replace('}}\n    ', '').replace('p1=', '')
                    p1_score = 0
                    p2_score = 0
                    winners = [x for x in match if 'winner' in x]
                    winners = [re.sub('[^0-9]','', x) for x in winners]
                    for i in winners:
                        if i == '1':
                            p1_score += 1
                        elif i == '2':
                            p2_score += 1

                    result = '   ' + p1 + ' ' + str(p1_score) + '-' + str(p2_score) + ' '+ p2 + '   '
                    matches.append(result)

    matchstr = ''.join(matches)
    matchstr = '  |  ' + prepend + '  |  ' + matchstr

    with open('results.txt', 'w') as output:
        output.write(matchstr)


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
            if p1 != '':
                if p1 != 'BYE' and p2 != 'BYE':
                    matches.append(' ' + p1 + ' ' + str(p1_score) + '-' + str(p2_score) + ' ' + p2 + '    ')
                elif p1 == 'BYE':
                    matches.append(' ' + p2 + ' (Bye) ')
                elif p2 == 'BYE':
                    matches.append(' ' + p1 + ' (Bye) ')
            if p1 == '':
                p1 = 'TBD'
            if p2 == '':
                p2 = 'TBD'
            prev_series = series_num
    matchstr = ' '.join(matches)
    if prepend is not '':
        prepend = '  |  ' + prepend + '  |  '
    matchstr = prepend + matchstr

    while len(matchstr) < 100 and len(matchstr) != 0:
        matchstr += matchstr

    with open('results.txt', 'w') as output:
        output.write(matchstr)
    print('Populated Results')

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
    group_names = [x.split('}')[0] for x in group_table[1:len(group_table)]]

    prev_series = 100
    round_tracker = 0
    matches = {}
    for group in group_names:
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
        player_names = re.split('\|bg[0-9]=\|', group_data)
        del player_names[0]
        player_names_list = [x.split('\n')[0].split('=')[1] for x in player_names]
        results_dict = dict.fromkeys(player_names_list)
        for key in player_names_list:
            results_dict[key] = {'Map Diff': 0, 'Map Wins': 0}

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
                for zone, offset in TIMEZONES.items():
                    try:
                        date = date.replace(zone, offset)
                    except:
                        print('Invalid Timezone')

                date = parser.parse(date)
                currentTime = datetime.datetime.now()
                currentTime = currentTime.replace(tzinfo=datetime.timezone.utc)
                timeDiff = abs(currentTime - date)
                timeDiff = timeDiff.days * 24 + timeDiff.seconds // 3600
                if timeDiff < 8:
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

                    results_dict[p1]['Map Wins'] += p1_score
                    results_dict[p2]['Map Wins'] += p2_score
                    results_dict[p1]['Map Diff'] += p1_score-p2_score
                    results_dict[p2]['Map Diff'] += p2_score-p1_score
        time.sleep(30)
    matchstr = ''
    for key in matches.keys():
        if matches[key] != []:
            matchstr += key + ''.join(matches[key])
    matchstr = '  |  ' + prepend + '  |  ' + matchstr

    while len(matchstr) < 100 and len(matchstr) != 0:
        matchstr += matchstr

    with open('results.txt', 'w') as output:
        output.write(matchstr)
    print('Populated Results')
