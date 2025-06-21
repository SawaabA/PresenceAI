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

from FacialRecognition.preprocessing import resize_frame
from FacialRecognition.input import get_video_capture
from FacialRecognition.feature_extraction import FaceMeshProcessor
from FacialRecognition.output import draw_face_landmarks
from FacialRecognition.inference import extract_features, analyze_behavior
from FacialRecognition.output import write_results_to_frame
import cv2 as cv


def main(cap):
    face_mesh_processor = FaceMeshProcessor()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Frame capture failed.")
            continue
        frame = resize_frame(frame)

        results = face_mesh_processor.process_frame(frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                draw_face_landmarks(frame, face_landmarks)
                features = extract_features(face_landmarks, frame.shape)
                traits = analyze_behavior(features)

                frame = write_results_to_frame(cv.flip(frame, 1), traits)

        cv.imshow("FaceMesh Feed", frame)

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    cap = get_video_capture(1)
    main(cap)
