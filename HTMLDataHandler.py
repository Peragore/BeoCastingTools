import time
import SC2ClientAPICall
import random
from os import walk
from threading import Thread
import json
import glob
import AligulacDataGrabber


prev_race = ''
race = 'None'
gif_path = ''
p1 = ''
p2 = ''
disp_time = ''
scores = {}
prev_result = ''
prev_time = 0.0
p1_wins = p2_wins = p1_form = p2_form = p1_wc = p2_wc = mean_result = 0
images = glob.glob('img/Player_images/*.png')
protoss_dances = next(walk('Gifs/Protoss'), (None, None, []))[2]  # [] if no file
terran_dances = next(walk('Gifs/Terran'), (None, None, []))[2]  # [] if no file
zerg_dances = next(walk('Gifs/Zerg'), (None, None, []))[2]  # [] if no file
problem_dict = {'DKZDark': 'Dark', 'DKZherO': 'herO', 'DKZCure': 'Cure', 'LiquidClem': 'Clem', 'LiquidSKill': 'SKillous',
                'marcj': 'uThermal'}
packet = {}
with open('keys/aligulac.txt', 'r') as f:
    aligulac_key = f.read()


class HTMLDataHandler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            global prev_race
            global race
            global gif_path
            global p1, p2, disp_time, scores, prev_result, p1_wins, p2_wins, p1_form, p2_form, p1_wc, p2_wc, mean_result, prev_time
            # try:
            race = SC2ClientAPICall.call_victory()
            full_string = SC2ClientAPICall.get_sc2client_string()
            p1 = full_string['players'][0]['name']
            p2 = full_string['players'][1]['name']
            if p1 in problem_dict.keys():
                p1 = problem_dict[p1]
            if p2 in problem_dict.keys():
                p2 = problem_dict[p2]

            new_path = gif_path

            prev_names = list(scores.keys())
            if p1 not in prev_names or p2 not in prev_names:
                scores = {p1: 0, p2: 0}
                try:
                    [p1_wins, p2_wins, p1_form, p2_form, winvals] = \
                        AligulacDataGrabber.get_aligulac_data(p1, p2, scores[p1], scores[p2], aligulac_key)
                except:
                    print('Aligulac Down')

            if full_string['players'][0]['result'] != prev_result and full_string['displayTime'] != prev_time:
                if full_string['players'][0]['result'] == 'Victory':
                    scores[p1] += 1
                    try:
                        [p1_wins, p2_wins, p1_form, p2_form, winvals] = \
                            AligulacDataGrabber.get_aligulac_data(p1, p2, scores[p1], scores[p2], aligulac_key)
                    except:
                        print('Aligulac Down')
                elif full_string['players'][1]['result'] == 'Victory':
                    scores[p2] += 1
                    try:
                        [p1_wins, p2_wins, p1_form, p2_form, winvals] = \
                            AligulacDataGrabber.get_aligulac_data(p1, p2, scores[p1], scores[p2], aligulac_key)
                    except:
                        print('Aligulac Down')
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
                p1_safe = [x.split('\\')[1].split('_')[0] for x in image_p1 if x.split('\\')[1].split('_')[0].casefold()
                           == p1.casefold()][0]
                if (image_p1[0].split('\\')[1].split('_')[0] + '_L.png').casefold() in image_p1:
                    p1_image = 'url(../img/Player_images/' + p1_safe + '_L.png)'
                else:
                    p1_image = 'url(../img/Player_images/' + p1_safe + '_Pose.png)'
            else:
                p1_image = ''
            if (p2.casefold() in x.casefold() for x in images) and len(image_p2) > 0:
                p2_safe = [x.split('\\')[1].split('_')[0] for x in image_p2 if x.split('\\')[1].split('_')[0].casefold()
                           == p2.casefold()][0]
                if (image_p2[0].split('\\')[1].split('_')[0] + '_R.png').casefold() in image_p1:
                    p2_image = 'url(../img/Player_images/' + p2_safe + '_R.png)'
                else:
                    p2_image = 'url(../img/Player_images/' + p2_safe + '_Pose.png)'
            else:
                p2_image = ''
            p1_race = 'url(../img/Player_images/' + full_string['players'][0]['race'] + '.png)'
            p2_race = 'url(../img/Player_images/' + full_string['players'][1]['race'] + '.png)'
            packet['gif_path'] = gif_path
            packet['results'] = results[0]
            packet['scores'] = scores
            packet['images'] = [p1_image, p2_image, p1_race, p2_race]
            try:
                packet['aligulac_bo3'] = [p1_wins, p2_wins, p1_form, p2_form, winvals['bo3']]
                packet['aligulac_bo5'] = [p1_wins, p2_wins, p1_form, p2_form, winvals['bo5']]
                packet['aligulac_bo7'] = [p1_wins, p2_wins, p1_form, p2_form, winvals['bo7']]
            except:
                print('Unable to Populate Aligulac')
            with open('json/datastream.json', 'w') as f:
                json.dump(packet, f)
            f.close()

            prev_race = race
            disp_time = full_string['displayTime']
            prev_result = full_string['players'][0]['result']
            prev_time = full_string['displayTime']
            # except:
            #     print('Bad API')
            time.sleep(1)
