import time


class Timer:
    start_time: float
    stop_time: float

    def __init__(self):
        self.start_time = time.time()

    def start(self):
        self.start_time = time.time()

    def stop(self) -> float:
        self.stop_time = time.time()
        return self.stop_time

    def elapsed(self):
        return self.stop() - self.start_time

    def elapsed_str(self):
        return f'{self.elapsed_minutes():.2f} minutes'

    def elapsed_minutes(self):
        return self.elapsed() / 60

    def __str__(self):
        return self.elapsed_str()
