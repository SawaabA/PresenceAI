"""-------------------------------------------------------
PresenceAI: Module Description Here
-------------------------------------------------------
Author:  JD
ID:      91786
Uses:    OpenCV
Version:  1.0.9
__updated__ = Sat Jun 21 2025
-------------------------------------------------------
"""

import csv
import os
import time


class CSVLogger:
    def __init__(self, filename="emotions_log.csv"):
        self.filename = filename
        self.last_logged_time = 0

        # Write headers if file doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "Time (s)",
                        "Blink Count",
                        "Head Tilt Count",
                        "Gaze",
                        "Smiling",
                        "Confidence",
                        "Engagement",
                        "Nervousness",
                        "Authenticity",
                    ]
                )

    def maybe_log(self, metrics):
        current_time = time.time()
        if current_time - self.last_logged_time >= 1.0:
            with open(self.filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        metrics["Time"],
                        metrics["Blink Count"],
                        metrics["Head Tilt Count"],
                        metrics["Eye Gaze"],
                        metrics["Smiling"],
                        metrics["Confidence"],
                        metrics["Engagement"],
                        metrics["Nervousness"],
                        metrics["Authenticity"],
                    ]
                )
            self.last_logged_time = current_time
