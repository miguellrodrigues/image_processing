import asyncio

import websockets


async def hello(ws, path):
    data = await ws.recv()

    print(type(data))


start_server = websockets.serve(hello, "localhost", 6587)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
