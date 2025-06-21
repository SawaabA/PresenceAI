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


def analyze_behavior(features):
    traits = {
        "Confidence": 1.0 if features["eye_openness"] > 5 else 0.3,
        "Engagement": 1.0 if features["eye_openness"] > 4 else 0.5,
        "Nervousness": 1.0 if features["mouth_openness"] > 10 else 0.2,
        "Authenticity": 1.0 if 0.5 < features["smile_score"] < 2.0 else 0.3,
    }
    return traits
