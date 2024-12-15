import time
import threading

class Analytics:
    def __init__(self, logger):
        self._lock = threading.Lock()
        self._data = {}
        self._queue_size = 0
        self.logger = logger

    def mark_busy(self, worker_id, number):
        with self._lock:
            self._data[worker_id] = {
                "timestamp": time.time(),
                "number": number,
                "done": False
            }
            self.logger(f"задание {number} из очереди направлено на Сервер {worker_id}")

    def mark_free(self, worker_id):
        with self._lock:
            self._data[worker_id] = {
                "timestamp": time.time(),
                "number": None,
                "done": True
            }
            self.logger(f"Сервер {worker_id} свободен")

    def set_queue_size(self, size):
        with self._lock:
            self._queue_size = size

    def get_data(self) -> (dict, int):
        with self._lock:
            return dict(self._data), self._queue_size