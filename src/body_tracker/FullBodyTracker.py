import cv2
import mediapipe as mp
import numpy as np
import datetime

# === Initialize MediaPipe Pose ===
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

ignore_indices = set(range(0, 11))  # ignore face & wrist landmarks

# === Tracking Vars ===
static_frame_count = 0
total_frames = 0
bounce_score = 0
prev_positions = None
sway_score = 0
lean_score = 0
arm_expressiveness = 0
arm_cross_frames = 0

print("Tracking started... Press ESC to stop.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark
        frame_h, frame_w = image.shape[:2]

        keypoints = []
        for i, point in enumerate(lm):
            if i in ignore_indices:
                continue
            keypoints.append((int(point.x * frame_w), int(point.y * frame_h)))

        for x, y in keypoints:
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

        keypoints_array = np.array(keypoints)
        if prev_positions is not None:
            movement = np.linalg.norm(keypoints_array - prev_positions)
            if movement < 5.0:
                static_frame_count += 1
        prev_positions = keypoints_array

        l_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        r_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        mid_y = (l_shoulder.y + r_shoulder.y) / 2
        bounce_score += abs(mid_y - 0.5)

        mid_x = (l_shoulder.x + r_shoulder.x) / 2
        sway_score += abs(mid_x - 0.5)

        l_hip = lm[mp_pose.PoseLandmark.LEFT_HIP.value]
        r_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP.value]
        torso_y = (l_hip.y + r_hip.y + l_shoulder.y + r_shoulder.y) / 4
        lean_score += abs(torso_y - 0.5)

        l_elbow = lm[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        r_elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        arm_expressiveness += abs(l_elbow.y - r_elbow.y)

        if (l_elbow.x > l_shoulder.x) and (r_elbow.x < r_shoulder.x):
            arm_cross_frames += 1

    total_frames += 1
    cv2.imshow('PresenceAI - Full Body Tracking', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# === Final Metrics ===
static_ratio = static_frame_count / total_frames if total_frames else 0
bounce_avg = bounce_score / total_frames if total_frames else 0
sway_avg = sway_score / total_frames if total_frames else 0
lean_avg = lean_score / total_frames if total_frames else 0
arm_express_avg = arm_expressiveness / total_frames if total_frames else 0
arm_cross_ratio = arm_cross_frames / total_frames if total_frames else 0

# === Print the results ===
print("\n--- Full Body Tracking Summary ---")
print(f"Total Duration (s): {round(total_frames / 30, 2)}")
print(f"Stillness Ratio: {round(static_ratio * 100, 2)}%")
print(f"Posture Bounce Score: {round(bounce_avg, 3)}")
print(f"Body Sway Score: {round(sway_avg, 3)}")
print(f"Lean Score: {round(lean_avg, 3)}")
print(f"Arm Expressiveness: {round(arm_express_avg, 3)}")
print(f"Arm Cross Ratio: {round(arm_cross_ratio * 100, 2)}%")
