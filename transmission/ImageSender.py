import base64
import socket
from math import ceil

import cv2
import imutils

from transmission.ImageGrab import ImageGrabThread


def split_data(d, n=2):
    r = []
    for index in range(0, len(d), n):
        r.append(d[index: index + n])

    return r


class ImageSender:
    def __init__(self, uri, port):
        self.running = True

        self.image = None
        self.igt = ImageGrabThread()

        self.igt.start()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)
        self._socket.connect(('127.0.0.1', 25565))

        self.state = 'send_size'

        self.start()

    def update_state(self):
        rec = self._socket.recv(1)

        if str(rec).__contains__("."):
            self.state = 'send_data'
        elif str(rec).__contains__("/"):
            self.state = 'send_size'

    def send_data(self, data):
        length = len(data)

        if length > 65535:
            n = int(ceil(length / 65535))

            _data = split_data(data, n)

            for _d in _data:
                self._socket.sendall(_d)
                self.update_state()

        else:
            self._socket.sendall(data)
            self.update_state()

    def start(self):
        while True:
            self.igt.run()
            frame = self.igt.join()

            # frame = imutils.resize(frame, width=512, height=600)
            # frame = frame[:, :, :3]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

            _, buffer = cv2.imencode(
                '.jpg',
                frame
            )

            data = base64.b64encode(buffer)

            if self.state == 'send_data':
                self.send_data(data)

            elif self.state == 'send_size':
                self._socket.sendall((len(data)).to_bytes(byteorder='big', length=4))
                self.update_state()

    def stop(self):
        self.running = False
        self.igt.stop()
