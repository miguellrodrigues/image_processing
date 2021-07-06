from transmission.ImageSend import ImageSenderThread

image_sender = ImageSenderThread(
    kwargs={
        'ip': '127.0.0.1',
        'port': 25565
    }
)

if __name__ == "__main__":
    image_sender.start()
