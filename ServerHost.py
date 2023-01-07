import asyncio
import time
import threading
import SC2ClientAPICall
import websockets
import random
from os import walk
import os
from threading import Thread
import json
import glob

prev_race = ''
race = 'None'
gif_path = ''
p1 = ''
p2 = ''
disp_time = ''
scores = {}
prev_result = ''
images = glob.glob('img/Player_images/*.png')
protoss_dances = next(walk('Gifs/Protoss'), (None, None, []))[2]  # [] if no file
terran_dances = next(walk('Gifs/Terran'), (None, None, []))[2]  # [] if no file
zerg_dances = next(walk('Gifs/Zerg'), (None, None, []))[2]  # [] if no file
problem_dict = {'DPGDark': 'Dark', 'DPGherO': 'herO', 'DPGCure': 'Cure', 'LiquidClem': 'Clem', 'Oliveira': 'time'}
packet = {}


class ServerHost(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            global prev_race
            global race
            global gif_path
            global p1, p2, disp_time, scores, prev_result
            try:
                race = SC2ClientAPICall.call_victory()
                full_string = SC2ClientAPICall.track_score()
                p1 = full_string['players'][0]['name']
                p2 = full_string['players'][1]['name']
                if p1 in problem_dict.keys():
                    p1 = problem_dict[p1]
                if p2 in problem_dict.keys():
                    p2 = problem_dict[p2]
                print(full_string)

                new_path = gif_path

                prev_names = list(scores.keys())
                if p1 not in prev_names or p2 not in prev_names:
                    scores = {p1: 0, p2: 0}

                if full_string['players'][0]['result'] != prev_result:
                    if full_string['players'][0]['result'] == 'Victory':
                        scores[p1] += 1
                    elif full_string['players'][1]['result'] == 'Victory':
                        scores[p2] += 1
                if race != prev_race:
                    if race == 'Terran':
                        new_path = 'url(../Gifs/Terran/' + random.choice(terran_dances) + ')'
                    elif race == 'Zerg':
                        new_path = 'url(../Gifs/Zerg/' + random.choice(zerg_dances) + ')'
                    elif race == 'Protoss':
                        new_path = 'url(../Gifs/Protoss/' + random.choice(protoss_dances) + ')'
                    else:
                        print("Maintaining path")
                    gif_path = new_path
                with open('results.txt') as f:
                    results = f.readlines()
                image_p1 = [string for string in images if p1.casefold() in string.casefold()]
                image_p2 = [string for string in images if p2.casefold() in string.casefold()]
                if any(p1.casefold() in x.casefold() for x in images) and len(image_p1) > 0:
                    if (image_p1[0].split('\\')[1].split('_')[0] + '_L.png').casefold() in image_p1:
                        p1_image = 'url(../img/Player_images/' + image_p1[0].split('\\')[1].split('_')[0] + '_L.png)'
                    else:
                        p1_image = 'url(../img/Player_images/' + image_p1[0].split('\\')[1].split('_')[0] + '_Pose.png)'
                else:
                    p1_image = ''
                if (p2.casefold() in x.casefold() for x in images) and len(image_p2) > 0:
                    if (image_p2[0].split('\\')[1].split('_')[0] + '_R.png').casefold() in image_p1:
                        p2_image = 'url(../img/Player_images/' + image_p2[0].split('\\')[1].split('_')[0] + '_R.png)'
                    else:
                        p2_image = 'url(../img/Player_images/' + image_p2[0].split('\\')[1] #.split('_')[0] + '_Pose.png)'
                else:
                    p2_image = ''
                p1_race = 'url(../img/Player_images/' + full_string['players'][0]['race'] + '.png)'
                p2_race = 'url(../img/Player_images/' + full_string['players'][1]['race'] + '.png)'
                print(image_p1)
                packet['gif_path'] = gif_path
                packet['results'] = results[0]
                packet['scores'] = scores
                packet['images'] = [p1_image, p2_image, p1_race, p2_race]
                with open('json/datastream.json', 'w') as f:
                    json.dump(packet, f)
                f.close()

                prev_race = race
                disp_time = full_string['displayTime']
                prev_result = full_string['players'][0]['result']
            except:
                print('Bad API')
            time.sleep(random.random() * 3)

# def server_starter(loop, server):
#     start_server = websockets.serve(provideResults, "localhost", 8766)
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()

# def start_loop(loop, server):
#     loop.run_until_complete(server)
#     loop.run_forever()
#
#
# def start_server():
#     # new_loop = asyncio.new_event_loop()
#     # start = websockets.serve(provideResults, "localhost", 8766, loop=new_loop)
#     t = Thread(target=provideResults(), daemon=True)
#     t.start()
#
#     print('Server Launched')
#     time.sleep(2)
