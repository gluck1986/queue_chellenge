import threading
import time

from app.analytics import Analytics
from app.queue import Queue


def worker(i_am: int, consumer: Queue, analytics: Analytics, stop_event: threading.Event):
    while not stop_event.is_set():
        analytics.mark_free(i_am)
        duration = consumer.pop()
        if duration is None:
            break
        analytics.mark_busy(i_am, duration)
        time.sleep(duration)
