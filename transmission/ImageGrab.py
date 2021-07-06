from threading import Thread
import mss
import numpy as np


class GrabImageThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        self._return = None
        self.sct = mss.mss()

        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

    def run(self):
        self._return = np.array(self.sct.grab(self.monitor))

    def join(self, timeout=None) -> np.ndarray:
        super().join(timeout)
        return self._return
