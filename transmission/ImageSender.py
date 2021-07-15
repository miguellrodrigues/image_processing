import base64
import queue
import socket
import struct
from threading import Thread
import asyncio

import cv2
import imutils

from transmission.ImageGrab import ImageGrabThread


def split_data(d, n=2):
    r = []
    for index in range(0, len(d), n):
        r.append(d[index: index + n])

    return r


class SocketDataSender(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None, ssocket):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        self.data = None
        self.old_data = None

        self.socket = ssocket

        self.queue = queue.Queue(2)

    def update_data(self, i, data):
        self.queue.put((i, data))

    def run(self):
        while True:
            data = self.queue.get()

            if data is None:
                continue

            await self.socket.send(
                struct.pack('I', data[0])
                + data[1]
            )

    def join(self, timeout=None):
        super().join(timeout)

    def read_server_response(self):
        rec = self.socket.recvfrom(1)

        if str(rec).__contains__("."):
            return 'send_data'
        elif str(rec).__contains__("/"):
            return 'wait'


class ImageSender:
    def __init__(self, uri, port):
        self.running = True

        self.image = None
        self.igt = ImageGrabThread()

        self.igt.start()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
        self._socket.connect(('127.0.0.1', 25565))

        self.state = 'send_data'

        self.data_sender = SocketDataSender(ssocket=self._socket)
        self.data_sender.start()

        self.start()

    def send_data(self, data):
        _data = split_data(data, 1024 * 64)

        for i in range(len(_data)):
            print("Sending new data... {}".format(i))

            self.data_sender.update_data(
                i,
                _data[i]
            )

        self._socket.send(b'EOF')

    def start(self):
        while True:
            if self.state == 'send_data':
                self.igt.run()
                frame = self.igt.join()

                frame = imutils.resize(frame, width=1280, height=720)
                # frame = frame[:, :, :3]
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

                _, buffer = cv2.imencode(
                    '.jpg',
                    frame
                )

                data = base64.b64encode(buffer)

                self.send_data(data)

            self.state = self.data_sender.read_server_response()

    def stop(self):
        self.running = False
        self.igt.stop()
