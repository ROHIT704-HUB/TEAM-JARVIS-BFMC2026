import time

class StopSignHandler:
    """
    Sends REAL brake command to STM32 Nucleo using BFMC protocol.
    """

    def __init__(self, queueList, stop_duration=3):
        self.queueList = queueList
        self.stop_duration = stop_duration
        self.stopped = False

    def execute(self):
        if self.stopped:
            return

        print("[AUTONOMY] Stop sign detected → BRAKE command sent")

        # ---------------- BFMC BRAKE COMMAND ----------------
        # Format: #brake:<steer>;;\r\n
        brake_command = "#brake:0;;\r\n"

        self.queueList["General"].put({
            "Owner": "Autonomy",
            "msgType": "SERIAL",
            "msgValue": brake_command
        })

        # Hold brake for required stop duration
        time.sleep(self.stop_duration)

        self.stopped = True
