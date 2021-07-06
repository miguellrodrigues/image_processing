import cv2
import numpy as np
import base64
import socket
from threading import Thread


class ImageReceiverThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        self.kwargs = kwargs

        self.BUFF_SIZE = 65536

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)

        host_ip = self.kwargs['ip']
        port = self.kwargs['port']

        self.socket.sendto(b'.', (host_ip, port))

        self._return = None

    def run(self):
        packet, _ = self.socket.recvfrom(self.BUFF_SIZE)

        data = base64.b64decode(packet, b' /')

        np_data = np.frombuffer(data, dtype=np.uint8)
        frame = cv2.imdecode(np_data, 1)

        self._return = frame

    def join(self, timeout=None) -> np.ndarray:
        super().join(timeout)
        return self._return

    def stop(self):
        self.socket.close()

