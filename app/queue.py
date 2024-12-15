import heapq
import threading

from app.analytics import Analytics


class Queue:
    def __init__(self, analytics: Analytics):
        self.heap = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.shutdown = False
        self.insertion_counter = 0
        self.analytics = analytics

    def push(self, priority, item):
        with self.lock:
            heapq.heappush(self.heap, (priority, self.insertion_counter, item))
            self.insertion_counter += 1
            self.condition.notify()
            self.analytics.set_queue_size(len(self.heap))

    def pop(self):
        with self.lock:
            # Ждать пока не появится элемент или не будет shutdown
            while not self.heap and not self.shutdown:
                self.condition.wait()
            # Если heap пуст и shutdown установлен – вернуть None
            if not self.heap and self.shutdown:
                return None
            self.analytics.set_queue_size(len(self.heap)-1)
            # Иначе извлечь элемент
            return int(heapq.heappop(self.heap)[2])

    def set_shutdown(self):
        with self.lock:
            self.shutdown = True
            self.condition.notify_all()

