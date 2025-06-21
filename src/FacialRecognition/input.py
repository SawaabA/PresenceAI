import cv2 as cv


def get_video_capture(index=0):
    cap = cv.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam")
    return cap
