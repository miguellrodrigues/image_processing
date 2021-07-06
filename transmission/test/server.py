import cv2

from transmission.ImageReceiver import ImageReceiver


def show_image(data):
    cv2.imshow("Receiving Video", data)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        receiver.stop()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    receiver = ImageReceiver(
        'localhost',
        8756,
        show_image
    )
