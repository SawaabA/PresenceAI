import cv2
import mediapipe as mp
import time
import os
import datetime
from pymongo import MongoClient

# === Connect to MongoDB ===
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["presenceAI"]
sessions = db["sessions"]

# === Set session ID (must match the one used by FullBodyTracker) ===
SESSION_ID = os.getenv("SESSION_ID")  # Recommended: pass this from SessionManager
USER_ID = "sawaab"

# === Initialize MediaPipe Hand Tracking ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_coords = None
static_frames = 0
total_frames = 0
total_movement = 0
high_activity_frames = 0
start_time = time.time()

print("Hand Tracking started... Press ESC to stop.")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    hand_coords = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            x = sum([lm.x for lm in hand_landmarks.landmark]) / 21
            y = sum([lm.y for lm in hand_landmarks.landmark]) / 21
            hand_coords.append((x, y))

        if prev_coords:
            movement = sum([
                abs(x1 - x2) + abs(y1 - y2)
                for (x1, y1), (x2, y2) in zip(hand_coords, prev_coords)
            ])
            total_movement += movement
            if movement < 0.01:
                static_frames += 1
            if movement > 0.1:
                high_activity_frames += 1
        prev_coords = hand_coords

    total_frames += 1
    cv2.imshow("PresenceAI - Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()

# === Final Metrics ===
duration = int(time.time() - start_time)
static_ratio = static_frames / total_frames if total_frames > 0 else 0.0
total_movement = round(total_movement, 3)
high_activity_ratio = high_activity_frames / total_frames if total_frames > 0 else 0.0

# === Update MongoDB document ===
sessions.update_one(
    {"session_id": SESSION_ID},
    {"$set": {
        "hand_tracking": {
            "static_ratio": round(static_ratio, 3),
            "total_movement": total_movement,
            "high_activity_ratio": round(high_activity_ratio, 3)
        }
    }}
)

print(f" Hand tracking data added to MongoDB (session_id: {SESSION_ID})")
