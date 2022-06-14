import requests

def call_victory():
    url = "http://localhost:6119/game"

    victory = 'None'
    try:
        game_response = requests.get(url, timeout=30).json()
        player_1 = game_response['players'][0]
        player_2 = game_response['players'][1]

        if player_1['result'] == 'Victory' and player_1['race'] == 'Prot' or player_2['result'] == 'Victory' and player_2['race'] == 'Prot':
            victory = 'Protoss'
        elif player_1['result'] == 'Victory' and player_1['race'] == 'Terr' or player_2['result'] == 'Victory' and player_2['race'] == 'Terr':
            victory = 'Terran'
        elif player_1['result'] == 'Victory' and player_1['race'] == 'Zerg' or player_2['result'] == 'Victory' and player_2['race'] == 'Zerg':
            victory = 'Zerg'
        else:
            victory = 'None'
    except:
        victory = 'None'

    return victory
