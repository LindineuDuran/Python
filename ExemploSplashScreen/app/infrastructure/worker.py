
import threading

class Worker(threading.Thread):
    def __init__(self, task, on_progress=None, on_complete=None):
        super().__init__()
        self.task = task
        self.on_progress = on_progress
        self.on_complete = on_complete

    def run(self):
        for progress in self.task():
            if self.on_progress:
                self.on_progress(progress)
        if self.on_complete:
            self.on_complete()
