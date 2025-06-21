import cv2                      # we need this library when working with videos
import mediapipe as mp          # we need this to track pose, hands and facial expressions in each frame of the video
import math
import os

# Import Gemini client and types
from google.ai.generativelanguage_v1 import TextServiceClient
from google.ai.generativelanguage_v1.types import GenerateContentRequest, TextCompletionPrompt


def calculate_angle(a, b, c):
    """
    Calculate the angle (in degrees) between points a, b, and c
    where b is the vertex point.
    Each point is (x, y).
    """
    ab = (a[0] - b[0], a[1] - b[1])
    cb = (c[0] - b[0], c[1] - b[1])

    dot = ab[0]*cb[0] + ab[1]*cb[1]
    mag_ab = math.sqrt(ab[0]**2 + ab[1]**2)
    mag_cb = math.sqrt(cb[0]**2 + cb[1]**2)

    if mag_ab * mag_cb == 0:
        return 0

    angle_rad = math.acos(dot / (mag_ab * mag_cb))
    angle_deg = math.degrees(angle_rad)
    return angle_deg


def generate_ai_suggestions(text_prompt: str) -> str:
    """Call Gemini AI to generate suggestions based on the input prompt."""
    client = TextServiceClient()

    request = GenerateContentRequest(
        model="models/text-bison-001",
        prompt=TextCompletionPrompt(text=text_prompt),
        temperature=0.7,
        max_tokens=300
    )

    response = client.generate_content(request=request)
    return response.candidates[0].content


def main():
    mp_drawing = mp.solutions.drawing_utils  # Utility to draw landmarks on images/frames
    mp_pose = mp.solutions.pose              # Pose tracking model
    mp_hands = mp.solutions.hands            # Hand tracking model

    cap = cv2.VideoCapture('./ps-mini.mp4')

    posture_scores = []
    gesture_scores = []

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
         mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            pose_results = pose.process(image)
            hand_results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    pose_results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

            cv2.imshow('Body Language Tracker', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            # Analyze posture and gestures, collect scores
            if pose_results.pose_landmarks:
                landmarks = pose_results.pose_landmarks.landmark

                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

                shoulder_mid = ((left_shoulder.x + right_shoulder.x) / 2,
                                (left_shoulder.y + right_shoulder.y) / 2)
                hip_mid = ((left_hip.x + right_hip.x) / 2,
                           (left_hip.y + right_hip.y) / 2)
                point_above_shoulders = (shoulder_mid[0], shoulder_mid[1] - 0.1)

                posture_angle = calculate_angle(hip_mid, shoulder_mid, point_above_shoulders)

                # Convert posture angle to numeric score (0-100)
                if posture_angle > 160:
                    posture_scores.append(100)
                elif posture_angle > 140:
                    posture_scores.append(70)
                else:
                    posture_scores.append(30)

                # Hand gesture score
                hand_raised = False
                if hand_results.multi_hand_landmarks:
                    for hand_landmarks in hand_results.multi_hand_landmarks:
                        wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST.value]
                        if wrist.y < shoulder_mid[1]:
                            hand_raised = True
                            break
                gesture_scores.append(100 if hand_raised else 30)

    cap.release()
    cv2.destroyAllWindows()

    # Calculate average scores
    avg_posture_score = sum(posture_scores) / len(posture_scores) if posture_scores else 0
    avg_gesture_score = sum(gesture_scores) / len(gesture_scores) if gesture_scores else 0

    final_score = (avg_posture_score + avg_gesture_score) / 2

    print(f"Average Posture Score: {avg_posture_score:.1f}")
    print(f"Average Gesture Score: {avg_gesture_score:.1f}")
    print(f"Final Body Language Score: {final_score:.1f}")

    # Prepare prompt for Gemini AI suggestions
    prompt_text = f"""
    I just analyzed a public speaking video and scored the speaker's body language:
    - Posture Score: {avg_posture_score:.1f}/100
    - Gesture Score: {avg_gesture_score:.1f}/100
    Please provide detailed suggestions on how to improve posture and gestures to be a better public speaker.
    """

    suggestions = generate_ai_suggestions(prompt_text)
    print("\nAI Suggestions:\n", suggestions)


if __name__ == "__main__":
    main()
