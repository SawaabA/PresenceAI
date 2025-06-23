# PresenceAI 🎤🤖  
*Master Your Presence. Speak With Confidence.*

PresenceAI is a tri-modal AI-powered communication coach that analyzes your **speech**, **body language**, and **facial expressions** to help you improve your public speaking, interview skills, and everyday communication.

🔗 [Check us out on Devpost →](https://devpost.com/software/presenceai)

---

## 🌟 Features

### 🎯 AI-Powered Analytics
Gain deep insight into your communication with real-time metrics:
- **Speech Clarity**
- **Body Language Score**
- **Eye Contact & Gaze Tracking**
- **Confidence & Engagement Ratings**
- **Emotional Tone Detection**
- **Filler Word Ratio, WPM, and More**


https://github.com/user-attachments/assets/9ffa6d15-d783-46d5-b986-5f56abcb97c0


### 🧠 Targeted Practice Modes
Choose a mode based on your communication goals:
- **Speech Practice** (1, 5, or 10 minutes – script optional)
- **Interview Prep** (Industry-specific questions)
- **Conversation Analysis** (Free-form natural conversation)
![www](https://github.com/user-attachments/assets/3a96da30-1906-4be4-91f3-59389862d36b)

### 📈 Progress Tracking
- Session history and trends
- Monthly performance gains
- Goal setting and achievements
![wwww](https://github.com/user-attachments/assets/d0070216-ad31-448d-8cfb-263aaff46cb6)

---

## 🏁 Built at SpurHacks 2025

PresenceAI was built during **SpurHacks 2025**, a 24-hour hackathon focused on pushing the limits of AI and real-world impact. Although the project is still under development and we have a long laundry list of tasks ahead, we're proud of the robust functionality we were able to deliver in such a short time.

In just 24 + 12(Procrastination) hours, we:
- Built a full-stack React + FastAPI app
- Integrated pose, facial, and voice analysis using AI
- Designed a beautiful UI and analytics dashboard
- Connected everything to MongoDB for session tracking

We’re especially proud of the teamwork, learning, and creativity that fueled this project.

Special thanks to my amazing teammates:  
 [Jashan Singh](https://www.linkedin.com/in/jashansingh65/)  
 Kole – Instagram: [@kdr47101](https://www.instagram.com/kdr47101)

This is just the beginning — more updates and polishing coming soon!

---

## 🧰 Tech Stack

| Layer              | Technology                                  |
|-------------------|----------------------------------------------|
| **Frontend**       | React, Tailwind CSS, JavaScript             |
| **Backend**        | FastAPI (Python), MongoDB                   |
| **AI & ML**        | OpenAI API, MediaPipe (Pose, Face), Whisper |
| **Speech Analysis**| Custom NLP scoring, Prosody detection       |
| **Tracking**       | Google Cloud Vision, OpenCV, NumPy          |
| **Cloud**          | Render / Railway / GCP (your choice)        |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB URI
- OpenAI API Key
- Google Cloud Vision API Key

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_key
export MONGO_URI=your_mongodb_uri
export GOOGLE_CLOUD_CREDENTIALS_JSON=path_to_json

# Run server
uvicorn main:app --reload
