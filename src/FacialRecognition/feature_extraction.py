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


class FaceDetector:
    def __init__(self, detection_confidence=0.5):
        self.face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=detection_confidence,
        )

    def process_frame(self, frame):
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        if results.detections:
            h, w, _ = frame.shape
            margin = int(h * 0.1)
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                x = int(bboxC.xmin * w)
                y = int(bboxC.ymin * h)
                width = int(bboxC.width * w)
                height = int(bboxC.height * h)

                x1 = max(x - margin, 0)
                y1 = max(y - margin, 0)
                x2 = min(x + width + margin, w)
                y2 = min(y + height + margin, h)

                cropped_face = frame[y1:y2, x1:x2]
                return cropped_face
        return None


class FaceMeshProcessor:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def process_frame(self, frame):
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return self.face_mesh.process(rgb_frame)


def extract_features(landmarks, image_shape):
    h, w, _ = image_shape
    coords = [(int(l.x * w), int(l.y * h)) for l in landmarks.landmark]

    left_eye_top = coords[159]
    left_eye_bottom = coords[145]
    left_eye_openness = abs(left_eye_top[1] - left_eye_bottom[1])

    mouth_top = coords[13]
    mouth_bottom = coords[14]
    mouth_openness = abs(mouth_top[1] - mouth_bottom[1])

    # Simplified placeholder features
    features = {
        "eye_openness": left_eye_openness,
        "mouth_openness": mouth_openness,
        "smile_score": mouth_openness / (left_eye_openness + 1e-5),
    }
    return features
