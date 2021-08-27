import asyncio
import time

import websockets


async def provideResults(websocket, path):
    while True:
        results = open("results.txt")
        await websocket.send(results.read())
        print(results.read())


start_server = websockets.serve(provideResults, "localhost", 8766)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
