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

import cv2 as cv
import mediapipe as mp
import numpy as np
import math
import time


class Detector:
    def __init__(self, detection_confidence=0.5):
        self.face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=detection_confidence,
        )

        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

        self.blink_count = 0
        self.blink_state = False
        self.blink_threshold = 4.5

    def detect_face(self, frame):
        results = self.face_detection.process(cv.cvtColor(frame, cv.COLOR_BGR2RGB))

        if not results.detections:
            return None

        h, w = frame.shape[:2]
        margin = int(h * 0.1)
        face = results.detections[0].location_data.relative_bounding_box

        x = max(int(face.xmin * w) - margin, 0)
        y = max(int(face.ymin * h) - margin, 0)
        width = min(int(face.width * w) + 2 * margin, w - x)
        height = min(int(face.height * h) + 2 * margin, h - y)

        return frame[y : y + height, x : x + width]

    def process_face(self, frame):
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return self.face_mesh.process(rgb_frame)


def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def angle_between(p1, p2):
    return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))


class FrameAnalyzer:
    def __init__(
        self, ear_threshold=0.2, min_frames_between_blinks=3, head_tilt_threshold_deg=15
    ):
        # Time
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

        # Mouth openness
        self.mouth_openness_list = []

        # Engagement/Confidence heuristics
        self.eye_openness_list = []
        self.head_angle_list = []

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
        top_lip = coords[13]
        bottom_lip = coords[14]
        openness = self.compute_distance(top_lip, bottom_lip)
        self.mouth_openness_list.append(openness)

    def analyze_frame(self, landmarks, image_shape):
        h, w, _ = image_shape
        coords = [(int(l.x * w), int(l.y * h)) for l in landmarks.landmark]

        self.detect_blink(coords)
        self.detect_head_tilt(coords)
        self.measure_mouth_openness(coords)

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

        # Heuristic-based state inference (adjustable thresholds)
        confidence = (
            "High" if avg_tilt < 8 and avg_ear > 0.25 and blink_rate < 15 else "Low"
        )
        engagement = "High" if avg_ear > 0.22 and blink_rate > 10 else "Low"
        nervousness = "High" if blink_rate > 25 or avg_tilt > 20 else "Low"
        authenticity = "High" if avg_mouth > 10 and avg_ear > 0.22 else "Uncertain"

        return {
            "Confidence": confidence,
            "Engagement": engagement,
            "Nervousness": nervousness,
            "Authenticity": authenticity,
        }

    @property
    def results(self):
        state_estimates = self.estimate_states()
        return {
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


def extract_features(landmarks, image_shape):
    h, w, _ = image_shape
    coords = [(int(l.x * w), int(l.y * h)) for l in landmarks.landmark]

    # === Eyes ===
    left_eye_top = coords[159]
    left_eye_bottom = coords[145]
    right_eye_top = coords[386]
    right_eye_bottom = coords[374]

    left_eye_openness = euclidean_distance(left_eye_top, left_eye_bottom)
    right_eye_openness = euclidean_distance(right_eye_top, right_eye_bottom)

    # Eye aspect ratio (blink detection)
    left_eye_width = euclidean_distance(coords[33], coords[133])
    right_eye_width = euclidean_distance(coords[362], coords[263])
    left_ear = left_eye_openness / left_eye_width
    right_ear = right_eye_openness / right_eye_width

    # === Mouth ===
    mouth_top = coords[13]
    mouth_bottom = coords[14]
    mouth_openness = euclidean_distance(mouth_top, mouth_bottom)
    mouth_width = euclidean_distance(coords[61], coords[291])  # Corners

    # === Eyebrows ===
    left_brow_center = coords[105]
    left_eye_center = (
        (coords[159][0] + coords[145][0]) // 2,
        (coords[159][1] + coords[145][1]) // 2,
    )
    left_eyebrow_raise = euclidean_distance(left_brow_center, left_eye_center)

    # === Nose Wrinkle ===
    nose_top = coords[4]
    nose_bottom = coords[2]
    nose_length = euclidean_distance(nose_top, nose_bottom)

    # === Smile (lip corner distance) ===
    left_lip_corner = coords[61]
    right_lip_corner = coords[291]
    lip_corner_distance = euclidean_distance(left_lip_corner, right_lip_corner)

    # === Head tilt (angle of eyes) ===
    eye_angle = angle_between(coords[33], coords[263])

    features = {
        "left_eye_openness": left_eye_openness,
        "right_eye_openness": right_eye_openness,
        "left_eye_ear": left_ear,
        "right_eye_ear": right_ear,
        "mouth_openness": mouth_openness,
        "mouth_width": mouth_width,
        "left_eyebrow_raise": left_eyebrow_raise,
        "nose_length": nose_length,
        "lip_corner_distance": lip_corner_distance,
        "head_tilt_angle": eye_angle,
    }

    return features
