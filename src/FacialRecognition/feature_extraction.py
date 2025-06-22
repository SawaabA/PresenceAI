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
from collections import deque, Counter


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
    mouth_width = euclidean_distance(coords[61], coords[291])

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
