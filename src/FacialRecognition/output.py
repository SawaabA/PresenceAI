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

import mediapipe as mp
import cv2 as cv

mp_drawing = mp.solutions.drawing_utils
my_drawing_specs = mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


def draw_face_landmarks(image, face_landmarks):
    mp_drawing.draw_landmarks(
        image=image,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
    )
    mp_drawing.draw_landmarks(
        image=image,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=my_drawing_specs,
    )


def write_results_to_frame(frame, traits, y=50):
    y = 30
    for trait, score in traits.items():
        cv.putText(
            frame,
            f"{trait}: {score}",
            (10, y),
            cv.FONT_HERSHEY_SIMPLEX,
            1.1,
            (0, 255, 255),
            2,
        )
        y += 25
    return frame
