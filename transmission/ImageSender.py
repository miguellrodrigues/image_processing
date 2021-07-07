import base64

import cv2
import websockets
import asyncio

from transmission.ImageGrab import ImageGrabThread


class ImageSender:
    def __init__(self, uri, port):
        self.uri = "ws://{}:{}".format(uri, port)

        print("Listening at: {}:{}".format(uri, port))

        self.running = True

        self.image = None
        self.igt = ImageGrabThread()

        self.igt.start()

        # asyncio.get_event_loop().run_until_complete(self.send())

        q = asyncio.Queue(2)

        asyncio.get_event_loop().create_task(self.produce(q))
        asyncio.get_event_loop().create_task(self.consume(q))

        asyncio.get_event_loop().run_forever()

    # async def send(self):
    #     while True:
    #         self.igt.run()
    #         frame = self.igt.join()
    #
    #         # frame = imutils.resize(frame, width=800, height=600)
    #         # frame = frame[:, :, :3]
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    #
    #         encoded, buffer = cv2.imencode(
    #             '.jpg',
    #             frame,
    #             [cv2.IMWRITE_JPEG_QUALITY, 95]
    #         )
    #
    #         data = base64.b64encode(buffer)
    #
    #         async with websockets.connect(self.uri) as ws:
    #             await ws.send(data)

    async def produce(self, queue):
        while True:
            self.igt.run()
            frame = self.igt.join()

            # frame = imutils.resize(frame, width=800, height=600)
            # frame = frame[:, :, :3]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

            encoded, buffer = cv2.imencode(
                '.jpg',
                frame,
                [cv2.IMWRITE_JPEG_QUALITY, 95]
            )

            data = base64.b64encode(buffer)

            await queue.put(data)

    async def consume(self, queue):
        while True:
            data = await queue.get()

            async with websockets.connect(self.uri) as ws:
                await ws.send(data)
                queue.task_done()

    def stop(self):
        self.running = False
        self.igt.stop()
