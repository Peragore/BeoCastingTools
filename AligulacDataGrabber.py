import requests
import urllib
import numpy


def get_aligulac_data(player_1, player_2, player1_score, player2_score, key):
    params_h2h = {'apikey': key}
    api_h2h_url = 'http://aligulac.com/api/v1/match/'
    api_id_url = 'http://aligulac.com/search/json/'
    params_id1 = {'q': player_1}
    params_id2 = {'q': player_2}
    id1_json = requests.get(api_id_url, params_id1).json()['players']
    id2_json = requests.get(api_id_url, params_id2).json()['players']
    try:
        try:
            id1_data = [x['id'] for x in id1_json if x['tag'].casefold() == player_1.casefold()][0]
        except:
            id1_data = [x['id'] for x in id1_json for y in x['aliases'] if y.casefold() == player_1.casefold()][0]
    except:
        id1_data = ''

    try:
        try:
            id2_data = [x['id'] for x in id2_json if x['tag'].casefold() == player_2.casefold()][0]
        except:
            id2_data = [x['id'] for x in id2_json for y in x['aliases'] if y.casefold() == player_2.casefold()][0]
    except:
        id2_data = ''
    if id1_data != '' and id2_data != '':
        params_h2h['pla__in'] = str(id1_data) + ',' + str(id2_data)
        params_h2h['plb__in'] = str(id1_data) + ',' + str(id2_data)
        params_h2h['limit'] = '100'
        params_str = urllib.parse.urlencode(params_h2h, safe=',')
        h2h_data = requests.get(api_h2h_url, params=params_str).json()
        player1_wins = 0
        player2_wins = 0
        print(h2h_data['objects'])
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

        params_form = {'apikey': key}
        api_form_url = 'http://aligulac.com/api/v1/player/set/' + str(id1_data) + ';' + str(id2_data) + '/'
        form_data = requests.get(api_form_url, params_form).json()

        p1_form = form_data['objects'][0]['form'][form_data['objects'][1]['race']]
        p2_form = form_data['objects'][1]['form'][form_data['objects'][0]['race']]

        p1_form = p1_form[0] / (p1_form[1] + p1_form[0]) * 100
        p2_form = p2_form[0] / (p2_form[1] + p2_form[0]) * 100

        p1_form = '{:.2f}%'.format(p1_form)
        p2_form = '{:.2f}%'.format(p2_form)

        winvals = {'bo3': get_win_chance(3, player1_score, player2_score, id1_data, id2_data, key),
                   'bo5': get_win_chance(5, player1_score, player2_score, id1_data, id2_data, key),
                   'bo7': get_win_chance(7, player1_score, player2_score, id1_data, id2_data, key)}

    else:
        player1_wins = 0
        player2_wins = 0
        p1_form = '00.00%'
        p2_form = '00.00%'
        winvals = {'bo3': ['00.00%', '00.00%', '0-0'],
                   'bo5': ['00.00%', '00.00%', '0-0'],
                   'bo7': ['00.00%', '00.00%', '0-0']}

    return [str(player1_wins), str(player2_wins), p1_form, p2_form, winvals]


def get_win_chance(bo, s1, s2, id1_data, id2_data, key):
    params_winchance = {'apikey': key,
                        'bo': bo,
                        's1': s1,
                        's2': s2}
    api_winchance_url = 'http://www.aligulac.com/api/v1/predictmatch/' + str(id1_data) + ',' + str(id2_data) + '/'
    winchance_data = requests.get(api_winchance_url, params_winchance).json()
    p1_winchance = winchance_data['proba'] * 100
    p2_winchance = winchance_data['probb'] * 100
    result_probs = [x['prob'] for x in winchance_data['outcomes']]
    most_likely_index = numpy.argmax(result_probs)
    mean_result = str(winchance_data['outcomes'][most_likely_index]['sca']) + '-' + \
                  str(winchance_data['outcomes'][most_likely_index]['scb'])
    p1_winchance = '{:.2f}%'.format(p1_winchance)
    p2_winchance = '{:.2f}%'.format(p2_winchance)
    return [p1_winchance, p2_winchance, mean_result]
