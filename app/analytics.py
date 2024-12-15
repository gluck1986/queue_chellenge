import time
import threading

class Analytics:
    def __init__(self, logger):
        self._lock = threading.Lock()
        self._data = {}
        self.logger = logger

    def mark_busy(self, worker_id, number):
        with self._lock:
            self._data[worker_id] = {
                "timestamp": time.time(),
                "number": number,
                "done": False
            }
            self.logger(f"задание из очереди направлено на Сервер {worker_id}")

    def mark_free(self, worker_id):
        with self._lock:
            self._data[worker_id] = {
                "timestamp": time.time(),
                "number": None,
                "done": True
            }
            self.logger(f"Сервер {worker_id} свободен")

    def get_data(self):
        with self._lock:
            # Возвращаем копию чтобы main мог читать без блокирования
            return dict(self._data)