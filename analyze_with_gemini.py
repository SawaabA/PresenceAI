import json
import os
import sys
from datetime import datetime

# === Gemini API Setup ===
import google.generativeai as genai

# === Load Gemini API Key from env ===
from dotenv import load_dotenv
load_dotenv("Keys.txt")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# === Helper: Load session data ===
LOG_PATH = "session_log.json"

def get_session_data(session_id):
    if not os.path.exists(LOG_PATH):
        raise FileNotFoundError("session_log.json not found")
    with open(LOG_PATH, "r") as f:
        sessions = json.load(f)
    for session in sessions:
        if session.get("session_id") == session_id:
            return session
    raise ValueError(f"Session ID '{session_id}' not found")

# === Prompt builder ===
def build_prompt(data):
    transcript = data.get("speech_analysis", {}).get("transcript", "[No response provided]")
    vocal = data.get("speech_analysis", {}).get("vocal_metrics", {})

    return f"""
You are an expert public speaking coach.

Below is a user's tracked performance data from a practice session. Please:
1. Rate their public speaking skills (1 to 10)
2. Give specific feedback on:
   - Body language
   - Hand gestures
   - Facial expressions (if available)
   - Vocal delivery
   - Content of their response

DATA:
- Session ID: {data.get("session_id")}
- Duration: {data.get("duration_sec", 0)} seconds

Body Tracking:
- Stillness Ratio: {data.get('body_tracking', {}).get('body_static_ratio')}
- Posture Score: {data.get('body_tracking', {}).get('posture_score')}
- Sway Score: {data.get('body_tracking', {}).get('sway_score')}
- Lean Score: {data.get('body_tracking', {}).get('lean_score')}
- Arm Expressiveness: {data.get('body_tracking', {}).get('arm_expressiveness')}
- Arm Cross Ratio: {data.get('body_tracking', {}).get('arm_cross_ratio')}

Hand Tracking:
- Stillness: {data.get('hand_tracking', {}).get('static_ratio')}
- High Activity: {data.get('hand_tracking', {}).get('high_activity_ratio')}
- Total Hand Movement: {data.get('hand_tracking', {}).get('total_movement')}

Facial Tracking:
- [Include if implemented]

Speech Transcript:
"""
{transcript}
"""

Vocal Metrics:
- Pitch: {vocal.get('pitch')}
- Pace: {vocal.get('pace')}

Give your full evaluation and improvement tips.
"""

# === Main function ===
def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_with_gemini.py <session_id>")
        return

    session_id = sys.argv[1]
    print(f"🔍 Loading session: {session_id}")

    try:
        session_data = get_session_data(session_id)
        prompt = build_prompt(session_data)

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        print("\n💡 AI Feedback:\n")
        print(response.text)

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()