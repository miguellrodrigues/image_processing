import base64

import cv2
import websockets
import asyncio

from transmission.ImageGrab import ImageGrabThread


class ImageSender:
    def __init__(self, uri, port):
        self.uri = "ws://{}:{}".format(uri, port)

        print("Listening at: {}:{}".format(uri, port))

        self.image = None
        self.igt = ImageGrabThread()

        self.igt.start()

        asyncio.get_event_loop().run_until_complete(self.send())

    async def send(self):
        while True:
            async with websockets.connect(self.uri) as ws:
                self.igt.run()
                frame = self.igt.join()

                # frame = imutils.resize(frame, width=800, height=600)
                # frame = frame[:, :, :3]
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                encoded, buffer = cv2.imencode(
                    '.jpg',
                    frame,
                    [cv2.IMWRITE_JPEG_QUALITY, 80]
                )

                data = base64.b64encode(buffer)

                await ws.send(data)

    def stop(self):
        self.igt.stop()
