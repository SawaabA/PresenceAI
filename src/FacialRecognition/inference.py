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

import numpy as np
import time
import math
from collections import deque, Counter


class FrameAnalyzer:
    def __init__(
        self, ear_threshold=0.2, min_frames_between_blinks=3, head_tilt_threshold_deg=15
    ):
        self.start_time = time.time()
        self.frame_counter = 0

        # Blink
        self.blink_counter = 0
        self.last_blink_frame = -min_frames_between_blinks
        self.ear_threshold = ear_threshold
        self.min_frames_between_blinks = min_frames_between_blinks

        # Head tilt
        self.head_tilt_counter = 0
        self.last_tilt_direction = None
        self.head_tilt_threshold = head_tilt_threshold_deg

        # Facial openness
        self.mouth_openness_list = []
        self.eye_openness_list = []
        self.head_angle_list = []

        # Gaze tracking
        self.gaze_history = deque(maxlen=30)  # Rolling window of recent gaze directions

    @staticmethod
    def compute_distance(p1, p2):
        return np.linalg.norm(np.array(p1) - np.array(p2))

    @staticmethod
    def compute_ear(top, bottom, left, right):
        vertical = FrameAnalyzer.compute_distance(top, bottom)
        horizontal = FrameAnalyzer.compute_distance(left, right)
        return vertical / (horizontal + 1e-6)

    @staticmethod
    def compute_head_tilt_angle(left_eye_outer, right_eye_outer):
        dx = right_eye_outer[0] - left_eye_outer[0]
        dy = right_eye_outer[1] - left_eye_outer[1]
        return math.degrees(math.atan2(dy, dx))

    def detect_blink(self, coords):
        left_ear = self.compute_ear(coords[159], coords[145], coords[33], coords[133])
        right_ear = self.compute_ear(coords[386], coords[374], coords[362], coords[263])
        avg_ear = (left_ear + right_ear) / 2
        self.eye_openness_list.append(avg_ear)

        if avg_ear < self.ear_threshold:
            if (
                self.frame_counter - self.last_blink_frame
            ) > self.min_frames_between_blinks:
                self.blink_counter += 1
                self.last_blink_frame = self.frame_counter

    def detect_head_tilt(self, coords):
        angle = self.compute_head_tilt_angle(coords[33], coords[263])
        self.head_angle_list.append(angle)

        if abs(angle) > self.head_tilt_threshold:
            current_dir = "right" if angle > 0 else "left"
            if self.last_tilt_direction != current_dir:
                self.head_tilt_counter += 1
                self.last_tilt_direction = current_dir
        else:
            self.last_tilt_direction = None

    def measure_mouth_openness(self, coords):
        openness = self.compute_distance(coords[13], coords[14])
        self.mouth_openness_list.append(openness)

    def detect_gaze_direction(self, coords):
        def classify_eye_gaze(outer, inner, iris):
            eye_width = self.compute_distance(outer, inner)
            iris_to_outer = self.compute_distance(iris, outer)
            ratio = iris_to_outer / (eye_width + 1e-6)

            if ratio < 0.35:
                return "Left"
            elif ratio > 0.65:
                return "Right"
            else:
                return "Center"

        left_gaze = classify_eye_gaze(coords[33], coords[133], coords[468])
        right_gaze = classify_eye_gaze(coords[362], coords[263], coords[473])

        # If both eyes agree, it's reliable
        if left_gaze == right_gaze:
            gaze = left_gaze
        else:
            gaze = "Uncertain"

        self.gaze_history.append(gaze)

    def analyze_frame(self, landmarks, image_shape):
        h, w, _ = image_shape
        coords = [(int(l.x * w), int(l.y * h)) for l in landmarks.landmark]

        self.detect_blink(coords)
        self.detect_head_tilt(coords)
        self.measure_mouth_openness(coords)
        self.detect_gaze_direction(coords)

        self.frame_counter += 1

    @property
    def elapsed_minutes(self):
        return (time.time() - self.start_time) / 60.0

    def estimate_states(self):
        avg_ear = np.mean(self.eye_openness_list[-30:]) if self.eye_openness_list else 0
        avg_mouth = (
            np.mean(self.mouth_openness_list[-30:]) if self.mouth_openness_list else 0
        )
        avg_tilt = (
            np.mean(np.abs(self.head_angle_list[-30:])) if self.head_angle_list else 0
        )
        blink_rate = self.blink_counter / (self.elapsed_minutes + 1e-6)

        gaze_mode = Counter(self.gaze_history).most_common(1)
        gaze = gaze_mode[0][0] if gaze_mode else "Unknown"

        confidence = (
            "High" if avg_tilt < 8 and avg_ear > 0.25 and blink_rate < 15 else "Low"
        )
        engagement = (
            "High" if avg_ear > 0.22 and blink_rate > 10 and gaze == "Center" else "Low"
        )
        nervousness = "High" if blink_rate > 25 or avg_tilt > 20 else "Low"
        authenticity = "High" if avg_mouth > 10 and avg_ear > 0.22 else "Uncertain"

        return {
            "Confidence": confidence,
            "Engagement": engagement,
            "Nervousness": nervousness,
            "Authenticity": authenticity,
            "Eye Gaze": gaze,
        }

    @property
    def results(self):
        state_estimates = self.estimate_states()
        return {
            "Time": round(time.time() - self.start_time, 2),
            "Total Frames": self.frame_counter,
            "Blink Count": self.blink_counter,
            "Head Tilt Count": self.head_tilt_counter,
            "Blink Frequency (per min)": round(
                self.blink_counter / self.elapsed_minutes, 2
            ),
            "Head Tilt Frequency (per min)": round(
                self.head_tilt_counter / self.elapsed_minutes, 2
            ),
            "Elapsed Time (min)": round(self.elapsed_minutes, 2),
            **state_estimates,
        }

    def reset(self):
        self.__init__(
            self.ear_threshold, self.min_frames_between_blinks, self.head_tilt_threshold
        )

    @property
    def history_data(self):
        return {
            "eye_openness": self.eye_openness_list,
            "mouth_openness": self.mouth_openness_list,
            "head_angle": self.head_angle_list,
            "gaze_history": list(self.gaze_history),
        }
