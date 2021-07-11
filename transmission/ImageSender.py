import base64
import socket
import cv2
import imutils
import struct
import ctypes
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

    def update_state(self):
        rec = self._socket.recvfrom(1)

        if str(rec).__contains__("."):
            self.state = 'send_data'
        elif str(rec).__contains__("/"):
            self.state = 'wait'

    def send_data(self, data):
        length = len(data)

        if length > 65535:
            _data = split_data(data, 1024 * 64)

            for i in range(len(_data)):
                _d = _data[i]

                self._socket.sendall(
                    struct.pack('I', i) + _d
                )

            self._socket.sendall(b'EOF')
        else:
            self._socket.sendall(
                struct.pack('I', 1 & 0xffffffff) + data
            )

            self._socket.sendall(b'EOF')

    def start(self):
        while True:
            print(self.state)

            if self.state == 'send_data':
                self.igt.run()
                frame = self.igt.join()

                frame = imutils.resize(frame, width=512, height=512)
                # frame = frame[:, :, :3]
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

                _, buffer = cv2.imencode(
                    '.jpg',
                    frame
                )

                data = base64.b64encode(buffer)

                self.send_data(data)

            self.update_state()

    def stop(self):
        self.running = False
        self.igt.stop()
