import asyncio
import time
import threading
import SC2ClientAPICall
import websockets
import random
from os import walk
import os
from threading import Thread


prev_race = ''
race = 'None'
gif_path = ''
protoss_dances = next(walk('Gifs/Protoss'), (None, None, []))[2]  # [] if no file
terran_dances = next(walk('Gifs/Terran'), (None, None, []))[2]  # [] if no file
zerg_dances = next(walk('Gifs/Zerg'), (None, None, []))[2]  # [] if no file

packet = {}
async def provideResults(websocket, path):
    while True:
        global prev_race
        global race
        global gif_path
        race = SC2ClientAPICall.call_victory()
        new_path = ''
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
        packet['gif_path'] = gif_path
        packet['results'] = results[0]
        print(gif_path)
        await websocket.send(gif_path)
        print(gif_path)

        print(packet)
        prev_race = race
        await asyncio.sleep(random.random() * 3)


# def server_starter(loop, server):
#     start_server = websockets.serve(provideResults, "localhost", 8766)
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()

def start_loop(loop, server):
    loop.run_until_complete(server)
    loop.run_forever()


def start_server():
    new_loop = asyncio.new_event_loop()
    start = websockets.serve(provideResults, "localhost", 8766, loop=new_loop)
    t = Thread(target=start_loop, args=(new_loop, start), daemon=True)
    t.start()

    print('Server Launched')
    time.sleep(2)




