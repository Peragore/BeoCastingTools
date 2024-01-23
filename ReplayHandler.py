# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sc2reader
from sc2reader.factories.plugins.replay import toJSON
import glob
import os
import matplotlib.pyplot as plt
import json
import numpy as np
import datetime

factory = sc2reader.factories.SC2Factory


# try:
#     factory.register_plugin(
#         "Replay", toJSON()
#     )  # legacy Python
# except TypeError:
#     factory.register_plugin("Replay", toJSON(indent=None))

# Press the green button in the gutter to run the script.


def get_newest_replay():
    list_of_files = glob.glob('C:/Users/pmulford/Documents/StarCraft II/Accounts/**/*.SC2Replay',
                              recursive='true')  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print('Getting File')
    return latest_file


def generate_plot_data(upgrade_list):
    packet = {}
    replay_path = get_newest_replay()
    print(replay_path)
    replay = sc2reader.load_replay(replay_path, load_level=4)
    event_names = set([event.name for event in replay.events])
    p1_supply = []
    p2_supply = []
    client_players = list(replay.client.values())
    p1 = client_players[0]
    p2 = client_players[1]
    p1_name = str(p1).split('-')[1].split('(')[0].strip()
    p2_name = str(p2).split('-')[1].split('(')[0].strip()
    p1_time = []
    p2_time = []
    p1_upgrade_time = []
    p2_upgrade_time = []
    p1_upgrades = {}
    p2_upgrades = {}
    p1_ground = {}
    p1_air = {}
    p1_misc = {}
    p2_ground = {}
    p2_air = {}
    p2_misc = {}

    for e in replay.events:

        if e.name == 'PlayerStatsEvent':
            if e.player == p1:
                p1_supply.append(e.food_used)
                p1_time.append((e.second / 60)/1.4)
            if e.player == p2:
                p2_supply.append(e.food_used)
                p2_time.append((e.second / 60)/1.4)
        if e.name == 'UpgradeCompleteEvent' and 'GameHeartActive' not in e.upgrade_type_name and 'Spray' not in e.upgrade_type_name and 'Reward' not in e.upgrade_type_name:
            # if str(datetime.timedelta(seconds=e.second/1.4)).split('0:')[0] != '':
            #     upgrade_time = #str(datetime.timedelta(seconds=e.second/1.4)).split('.')[0]
            # else:
            #     upgrade_time = str(datetime.timedelta(seconds=e.second/1.4)).split(':', 1)[1].split('.')[0]
            upgrade_time = (e.second/60)/1.4
            if e.player == p1:
                p1_upgrades['url(../img/Upgrades/' + e.upgrade_type_name + '.png)'] = upgrade_time
                p1_upgrade_time.append(upgrade_time)
            else:
                p2_upgrades['url(../img/Upgrades/' + e.upgrade_type_name + '.png)'] = upgrade_time
                p2_upgrade_time.append(upgrade_time)

            if ("Weapons" in e.upgrade_type_name):
                if e.player == p1:
                    p1_ground['url(../img/Upgrades/'+e.upgrade_type_name+'.png)'] = upgrade_time
                if e.player == p2:
                    p2_ground['url(../img/Upgrades/'+e.upgrade_type_name+'.png)'] = upgrade_time
            elif "Armors" in e.upgrade_type_name or "Shields" in e.upgrade_type_name:
                if e.player == p1:
                    p1_air['url(../img/Upgrades/'+e.upgrade_type_name+'.png)'] = upgrade_time
                if e.player == p2:
                    p2_air['url(../img/Upgrades/'+e.upgrade_type_name+'.png)'] = upgrade_time
            elif "Reward" not in e.upgrade_type_name:
                if e.player == p1:
                    p1_misc['url(../img/Upgrades/'+e.upgrade_type_name+'.png)'] = upgrade_time
                if e.player == p2:
                    p2_misc['url(../img/Upgrades/'+e.upgrade_type_name+'.png)'] = upgrade_time

            # print(e.upgrade_type_name)
    lengths = [len(p1_supply), len(p2_supply)]
    min_length = min(lengths)

    p1supply_array = np.array(p1_supply[0:min_length])
    p2supply_array = np.array(p2_supply[0:min_length])
    result = np.subtract(p1supply_array, p2supply_array)
    result_up = [0 if x < 0 else x for x in result.tolist()]
    result_down = [0 if x > 0 else x for x in result.tolist()]

    packet['supply_delta_up'] = result_up
    packet['supply_delta_down'] = result_down
    packet['p1_time'] = p1_time
    packet['p2_time'] = p2_time
    packet['p1_upgrade_time'] = p1_upgrade_time
    packet['p2_upgrade_time'] = p2_upgrade_time
    packet['p1_upgrade_stream'] = p1_upgrades
    packet['p2_upgrade_stream'] = p2_upgrades
    packet['p1_name'] = p1_name
    packet['p2_name'] = p2_name
    packet['p1_ground'] = p1_ground
    packet['p2_ground'] = p2_ground
    packet['p1_air'] = p1_air
    packet['p2_air'] = p2_air
    packet['p1_misc'] = p1_misc
    packet['p2_misc'] = p2_misc

    return packet

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
