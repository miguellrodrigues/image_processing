import base64
import socket
from threading import Thread

import cv2
import imutils

from transmission.ImageGrab import ImageGrabThread


class ImageSenderThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        self.kwargs = kwargs

        self.BUFF_SIZE = 65536

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)

        host_ip = self.kwargs['ip']
        port = self.kwargs['port']

        self.socket.bind((host_ip, port))
        print('Listening at:', (host_ip, port))

        self.image = None
        self.igt = ImageGrabThread()

        self.igt.start()

    def run(self):
        packet, client_address = self.socket.recvfrom(self.BUFF_SIZE)
        print('GOT connection from ', client_address)

        while True:
            self.igt.run()
            frame = self.igt.join()

            frame = imutils.resize(frame, width=800, height=600)
            # frame = frame[:, :, :3]
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            encoded, buffer = cv2.imencode(
                '.jpg',
                frame,
                [cv2.IMWRITE_JPEG_QUALITY, 80]
            )

            data = base64.b64encode(buffer)

            self.socket.sendto(data, client_address)

            self.igt.run()

    def stop(self):
        self.socket.close()
        self.igt.stop()
