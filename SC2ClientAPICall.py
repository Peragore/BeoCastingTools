import requests
import urllib

def call_victory():
    url = "http://localhost:6119/game"

    victory = 'None'
    try:
        game_response = requests.get(url, timeout=30).json()
        player_1 = game_response['players'][0]
        player_2 = game_response['players'][1]
        p1_name = player_1['name']
        p2_name = player_2['name']

        if player_1['result'] == 'Victory' and player_1['race'] == 'Prot' or player_2['result'] == 'Victory' and player_2['race'] == 'Prot':
            victory = 'Protoss'
        elif player_1['result'] == 'Victory' and player_1['race'] == 'Terr' or player_2['result'] == 'Victory' and player_2['race'] == 'Terr':
            victory = 'Terran'
        elif player_1['result'] == 'Victory' and player_1['race'] == 'Zerg' or player_2['result'] == 'Victory' and player_2['race'] == 'Zerg':
            victory = 'Zerg'
        else:
            victory = 'None'

        with open('player1_name.txt', 'w') as output:
            output.write(p1_name)
        with open('player2_name.txt', 'w') as output:
            output.write(p2_name)
    except:
        victory = 'None'

    return victory

def track_score():
    url = "http://localhost:6119/game"
    result = 'None'
    try:
        game_response = requests.get(url, timeout=30).json()
        player_1 = game_response['players'][0]
        player_2 = game_response['players'][1]
        p1_name = player_1['name']
        p2_name = player_2['name']

        result = game_response
    except:
        result = 'None'

    return result

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

    params_h2h['pla__in'] = str(id1_data)+','+str(id2_data)
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
    api_form_url = 'http://aligulac.com/api/v1/player/set/'+str(id1_data)+';'+str(id2_data)+'/'
    form_data = requests.get(api_form_url, params_form).json()
    p1_form = form_data['objects'][0]['form'][form_data['objects'][1]['race']]
    p2_form = form_data['objects'][1]['form'][form_data['objects'][0]['race']]
    print(p1_form)
    p1_form = p1_form[0]/(p1_form[1]+p1_form[0])*100
    p2_form = p2_form[0]/(p2_form[1]+p2_form[0])*100

    p1_form = '{:.2f}%'.format(p1_form)
    p2_form = '{:.2f}%'.format(p2_form)
    return [str(player1_wins), str(player2_wins), p1_form, p2_form]
