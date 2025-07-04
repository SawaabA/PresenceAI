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
from FacialRecognition.feature_extraction import Detector
from FacialRecognition.feature_extraction import extract_features
from FacialRecognition.output import draw_face_landmarks
from FacialRecognition.output import write_results_to_frame
from FacialRecognition.inference import FrameAnalyzer
from FacialRecognition.Logger import CSVLogger
import cv2 as cv


def main(cap):
    detector = Detector()
    analyzer = FrameAnalyzer()
    logger = CSVLogger()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Frame capture failed.")
            continue

        face = detector.detect_face(frame)

        if face is not None:
            results = detector.process_face(face)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    draw_face_landmarks(face, face_landmarks)
                    analyzer.analyze_frame(face_landmarks, face.shape)
                    frame = resize_frame(face, 1000, 1000)
                    frame = write_results_to_frame(cv.flip(frame, 1), analyzer.results)
                    logger.log_results(analyzer.results)
        cv.imshow("FaceMesh Feed", frame)

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    cap = get_video_capture(0)
    main(cap)
