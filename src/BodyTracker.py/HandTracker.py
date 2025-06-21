import cv2
import mediapipe as mp
import time
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime

# === Load API keys from Keys.txt ===
load_dotenv("Keys.txt")
MONGO_URI = os.getenv("MONGO_URI")

# === Connect to MongoDB ===
client = MongoClient(MONGO_URI)
db = client["presenceAI"]
collection = db["body_language_feedback"]

# === Initialize MediaPipe Hand Tracking ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_coords = None
static_frames = 0
total_frames = 0
start_time = time.time()

print("📷 Tracking started... Press ESC to stop.")

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
            if movement < 0.01:
                static_frames += 1
        prev_coords = hand_coords

    total_frames += 1
    cv2.imshow("PresenceAI - Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()

# === Final Static Ratio ===
duration = int(time.time() - start_time)
static_ratio = static_frames / total_frames if total_frames > 0 else 0.0

# === Insert result into MongoDB ===
entry = {
    "user_id": "sawaab",
    "speech_id": f"speech_{int(time.time())}",
    "timestamp": datetime.datetime.utcnow(),
    "duration_sec": duration,
    "hand_static_ratio": round(static_ratio, 3),
    "feedback": f"Hands were still {round(static_ratio*100, 1)}% of the time."
}

collection.insert_one(entry)
print(f"\n✅ Inserted to MongoDB!\nRatio: {entry['hand_static_ratio']}\nFeedback: {entry['feedback']}")
