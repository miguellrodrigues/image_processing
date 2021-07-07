import cv2

from transmission.ImageReceiver import ImageReceiver
import time


class ImageProcess:
    fps, tm, last_time = (0, 0, 0)

    def show(self, data):
        self.last_time = self.tm

        frame = cv2.putText(data, 'FPS: ' + str(self.fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Receiving Video", frame)

        self.tm = time.time()
        self.fps = int(1 / (self.tm - self.last_time))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            receiver.stop()


if __name__ == '__main__':
    ip = ImageProcess()

    receiver = ImageReceiver(
        'localhost',
        8756,
        ip.show
    )
