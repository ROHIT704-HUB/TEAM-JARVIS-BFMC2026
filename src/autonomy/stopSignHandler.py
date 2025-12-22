Python
import time

class StopSignHandler:
    """
    Handles stopping behavior after stop sign detection.
    """

    def _init_(self, stop_duration=3):
        self.stop_duration = stop_duration
        self.stopped_once = False

    def execute(self):
        if not self.stopped_once:
            print("[AUTONOMY] Stop sign detected. Vehicle stopping.")
            time.sleep(self.stop_duration)
            print("[AUTONOMY] Stop completed.")
            self.stopped_once = True
