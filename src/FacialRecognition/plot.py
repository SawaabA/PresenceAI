import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV
df = pd.read_csv("emotions_log.csv")

# Map categorical emotional states to numbers for plotting
state_map = {"Low": 0, "Uncertain": 0.5, "High": 1}
gaze_map = {"Left": 0, "Center": 1, "Right": 2, "Uncertain": 1.5}

df["Confidence_num"] = df["Confidence"].map(state_map)
df["Engagement_num"] = df["Engagement"].map(state_map)
df["Nervousness_num"] = df["Nervousness"].map(state_map)
df["Authenticity_num"] = df["Authenticity"].map(state_map)
df["Gaze_num"] = df["Gaze"].map(gaze_map)

# For better scaling, compute blink and tilt deltas
df["Blink Delta"] = df["Blink Count"].diff().fillna(0)
df["Tilt Delta"] = df["Head Tilt Count"].diff().fillna(0)

# Setup the plot
fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
plt.suptitle("Facial Behavior Time Series Analysis")

# Blink & Head Tilt over Time
axs[0].plot(df["Time (s)"], df["Blink Delta"], label="Blink Delta", color="blue")
axs[0].plot(df["Time (s)"], df["Tilt Delta"], label="Tilt Delta", color="orange")
axs[0].set_ylabel("Activity Count")
axs[0].legend()
axs[0].grid(True)

# Gaze Direction
axs[1].plot(
    df["Time (s)"],
    df["Gaze_num"],
    label="Gaze Direction",
    color="purple",
    linestyle="--",
    marker="o",
)
axs[1].set_yticks([0, 1, 2])
axs[1].set_yticklabels(["Left", "Center", "Right"])
axs[1].set_ylabel("Gaze")
axs[1].legend()
axs[1].grid(True)

# Confidence / Engagement / Nervousness / Authenticity
axs[2].plot(df["Time (s)"], df["Confidence_num"], label="Confidence", color="green")
axs[2].plot(df["Time (s)"], df["Engagement_num"], label="Engagement", color="blue")
axs[2].plot(df["Time (s)"], df["Nervousness_num"], label="Nervousness", color="red")
axs[2].plot(df["Time (s)"], df["Authenticity_num"], label="Authenticity", color="black")
axs[2].set_yticks([0, 0.5, 1])
axs[2].set_yticklabels(["Low", "?", "High"])
axs[2].set_ylabel("Emotion Score")
axs[2].legend()
axs[2].grid(True)

# Final plot formatting
axs[2].set_xlabel("Time (s)")
plt.tight_layout()
plt.show()
