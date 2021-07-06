from threading import Thread

import mss
import numpy as np


class ImageGrabThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None, monitor=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        if monitor is None:
            monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

        self._return = None
        self.sct = mss.mss()

        self.monitor = monitor

    def run(self):
        self._return = np.array(self.sct.grab(self.monitor))

    def join(self, timeout=None) -> np.ndarray:
        super().join(timeout)
        return self._return

    def stop(self):
        self.sct.close()
