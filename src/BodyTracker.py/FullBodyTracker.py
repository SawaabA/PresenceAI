import cv2
import mediapipe as mp
import numpy as np
import os
import datetime
from pymongo import MongoClient

# === Connect to MongoDB ===
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["presenceAI"]
sessions = db["sessions"]

# === Create a new session with unique session_id ===
USER_ID = "sawaab"
SESSION_ID = f"session_{int(datetime.datetime.now().timestamp())}"
sessions.insert_one({
    "session_id": SESSION_ID,
    "user_id": USER_ID,
    "timestamp": datetime.datetime.now(datetime.timezone.utc),
    "duration_sec": 0,
    "hand_tracking": {},
    "body_tracking": {},
    "facial_tracking": {},
    "speech_analysis": {}
})

# === Initialize MediaPipe Pose ===
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# === Landmark indices to ignore (face and wrists) ===
ignore_indices = set(range(0, 11))  # 0-10 includes face + wrists + hands

# === Tracking Variables ===
static_frame_count = 0
total_frames = 0
bounce_score = 0
prev_positions = None

print("📷 Tracking started... Press ESC to stop.")

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

        # Extract relevant landmark positions
        keypoints = []
        for i, point in enumerate(lm):
            if i in ignore_indices:
                continue
            keypoints.append((int(point.x * frame_w), int(point.y * frame_h)))

        # Draw filtered landmarks
        for x, y in keypoints:
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

        # Track movement to detect static frames
        keypoints_array = np.array(keypoints)
        if prev_positions is not None:
            movement = np.linalg.norm(keypoints_array - prev_positions)
            if movement < 5.0:
                static_frame_count += 1
        prev_positions = keypoints_array

        # Shoulder bounce
        l_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        r_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        mid_y = (l_shoulder.y + r_shoulder.y) / 2
        bounce = abs(mid_y - 0.5)  # 0.5 is arbitrary center
        bounce_score += bounce

    total_frames += 1
    cv2.imshow('PresenceAI - Full Body Tracking', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# === Feedback Logic ===
static_ratio = static_frame_count / total_frames if total_frames else 0
bounce_avg = bounce_score / total_frames if total_frames else 0

# === Update session document ===
sessions.update_one(
    {"session_id": SESSION_ID},
    {"$set": {
        "duration_sec": round(total_frames / 30, 2),
        "body_tracking": {
            "body_static_ratio": round(static_ratio, 3),
            "posture_score": round(bounce_avg, 3)
        }
    }}
)

print(f"✅ Body tracking data added to MongoDB (session_id: {SESSION_ID})")
