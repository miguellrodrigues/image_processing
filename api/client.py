import asyncio

import websockets
import numpy as np
import cv2
import base64


async def hello():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as ws:
        frame = np.zeros_like(1, shape=(9, 9))

        encoded, buffer = cv2.imencode(
            '.jpg',
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 80]
        )

        data = base64.b64encode(buffer)

        await ws.send(
            data
        )

asyncio.get_event_loop().run_until_complete(hello())
