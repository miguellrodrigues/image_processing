import asyncio
import base64

import cv2
import numpy as np
import websockets


class ImageReceiver:
    def __init__(self, uri, port, callback):
        self._return = None

        self.callback = callback

        self.server = websockets.serve(self.receive, uri, port)

        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    async def receive(self, ws, path):
        packet = await ws.recv()

        data = base64.b64decode(packet, b' /')

        np_data = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(np_data, 1)

        self.callback(frame)

    def stop(self):
        self.server.close()
