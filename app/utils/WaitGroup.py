import threading


class WaitGroup(object):
    def __init__(self):
        self.count = 0
        self.condition = threading.Condition()

    def add(self):
        self.condition.acquire()
        self.count += 1
        self.condition.release()

    def done(self):
        self.condition.acquire()
        self.count -= 1
        if self.count <= 0:
            self.condition.notifyAll()
        self.condition.release()

    def wait(self):
        self.condition.acquire()
        while self.count > 0:
            self.condition.wait()
        self.condition.release()
