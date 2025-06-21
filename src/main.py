from FacialRecognition.input import get_video_capture
from FacialRecognition.feature_extraction import FaceMeshProcessor
from FacialRecognition.output import draw_face_landmarks
from FacialRecognition.inference import extract_features, analyze_behavior
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
                features = extract_features(face_landmarks, frame.shape)
                traits = analyze_behavior(features)

                # Display traits on frame

                frame = cv.flip(frame, 1)
                y = 30
                for trait, score in traits.items():
                    cv.putText(
                        frame,
                        f"{trait}: {score:.2f}",
                        (10, y),
                        cv.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 255),
                        2,
                    )
                    y += 25

        cv.imshow("FaceMesh Feed", frame)

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    cap = get_video_capture(1)
    main(cap)
