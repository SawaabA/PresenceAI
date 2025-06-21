from FacialRecognition.input import get_video_capture
from FacialRecognition.feature_extraction import FaceMeshProcessor
from FacialRecognition.output import draw_face_landmarks
import cv2 as cv


def main(cap):
    face_mesh_processor = FaceMeshProcessor()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Frame capture failed.")
            continue

        results = face_mesh_processor.process_frame(frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                draw_face_landmarks(frame, face_landmarks)

        cv.imshow("FaceMesh Feed", cv.flip(frame, 1))

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    cap = get_video_capture(1)
    main(cap)
