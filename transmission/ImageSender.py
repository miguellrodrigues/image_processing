import base64
import socket

import cv2
import imutils

from transmission.ImageGrab import ImageGrabThread


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


class ImageSender:
    def __init__(self, uri, port):
        self.uri = "ws://localhost:9002"

        print("Listening at: {}:{}".format(uri, port))

        self.running = True

        self.image = None
        self.igt = ImageGrabThread()

        self.igt.start()

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 10)
        self._socket.connect(('127.0.0.1', 25565))

        self.state = 'send_size'

        self.start()

    def start(self):
        while True:
            self.igt.run()
            frame = self.igt.join()

            frame = imutils.resize(frame, width=800, height=600)
            # frame = frame[:, :, :3]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

            _, buffer = cv2.imencode(
                '.jpg',
                frame
            )

            data = base64.b64encode(buffer)

            if self.state == 'send_data':
                if len(data) > 65535:
                    ch = chunks(data, 5)

                    for chunk in ch:
                        self._socket.sendall(chunk)
                else:
                    self._socket.sendall(data)
            elif self.state == 'send_size':
                self._socket.sendall((len(data)).to_bytes(byteorder='big', length=4))

            rec = self._socket.recv(1)

            if str(rec).__contains__("."):
                self.state = 'send_data'
            elif str(rec).__contains__("/"):
                self.state = 'send_size'

    def stop(self):
        self.running = False
        self.igt.stop()
