import random
import threading


class Queue:
    def __init__(self, logger):
        self._lock = threading.Lock()

        self._data = {}
        self.logger = logger

    def ask(self):
        return random.randint(1,5)