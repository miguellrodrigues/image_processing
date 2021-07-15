import base64
import socket
import struct
import time

import cv2

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

        self.state = 'send_data'

        self.start()

    def read_server_response(self):
        rec = self._socket.recvfrom(1)

        if str(rec).__contains__("."):
            return 'send_data'
        elif str(rec).__contains__("/"):
            return 'wait'

    def send_data(self, data):
        for i in range(len(data)):
            self._socket.send(
                struct.pack('I', i)
                + data[i]
            )

            time.sleep(.001)

        self._socket.send(b'EOF')

    def start(self):
        while True:
            if self.state == 'send_data':
                self.igt.run()
                frame = self.igt.join()

                # frame = imutils.resize(frame, width=512, height=512)
                # frame = frame[:, :, :3]
                # frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

                _, buffer = cv2.imencode(
                    '.jpg',
                    frame
                )

                data = base64.b64encode(buffer)

                self.send_data(split_data(data, 1024 * 32))

            self.state = self.read_server_response()

    def stop(self):
        self.running = False
        self.igt.stop()
