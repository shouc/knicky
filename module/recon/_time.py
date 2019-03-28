__sys__ = ["Darwin", "Linux", "Windows"]
__name__ = "time"
__desc__ = "Get system time"


def send():
    import time
    return time.time()
