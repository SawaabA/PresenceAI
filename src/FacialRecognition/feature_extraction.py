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
        y = max(int(face.ymin * h) - int(margin * 2), 0)
        width = min(int(face.width * w) + 2 * margin, w - x)
        height = min(int(face.height * h) + 2 * margin, h - y)

        return frame[y : y + height, x : x + width]

    def process_face(self, frame):
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return self.face_mesh.process(rgb_frame)
