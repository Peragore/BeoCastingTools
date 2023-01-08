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

        if player_1['result'] == 'Victory' and player_1['race'] == 'Prot' or player_2['result'] == 'Victory' and \
                player_2['race'] == 'Prot':
            victory = 'Protoss'
        elif player_1['result'] == 'Victory' and player_1['race'] == 'Terr' or player_2['result'] == 'Victory' and \
                player_2['race'] == 'Terr':
            victory = 'Terran'
        elif player_1['result'] == 'Victory' and player_1['race'] == 'Zerg' or player_2['result'] == 'Victory' and \
                player_2['race'] == 'Zerg':
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


def get_sc2client_string():
    url = "http://localhost:6119/game"
    result = 'None'
    try:
        game_response = requests.get(url, timeout=30).json()
    except:
        result = 'None'

    return game_response
