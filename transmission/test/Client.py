import cv2

from transmission.ImageReceive import ImageReceiverThread

image_receiver = ImageReceiverThread(
    kwargs={
        'ip': '127.0.0.1',
        'port': 25565
    }
)

if __name__ == '__main__':
    image_receiver.start()

    while True:
        image_receiver.run()
        img = image_receiver.join()

        cv2.imshow("Receiving Video", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            image_receiver.stop()
            cv2.destroyAllWindows()
            break
