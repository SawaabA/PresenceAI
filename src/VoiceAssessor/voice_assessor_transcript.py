#!/usr/bin/env python3
import argparse
import subprocess
import tempfile
import json
import os
import sys
import wave
import re
from pathlib import Path


def extract_audio(video_path: Path) -> Path:
    """Extract audio from video into mono 16kHz WAV using ffmpeg"""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav_path = Path(tmp.name)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-ac",
        "1",
        "-ar",
        "16000",
        str(wav_path),
    ]
    try:
        subprocess.run(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
    except FileNotFoundError:
        print(
            "Error: ffmpeg not found. Please install ffmpeg and ensure it's on PATH.",
            file=sys.stderr,
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e}", file=sys.stderr)
        sys.exit(1)
    return wav_path


def get_audio_duration(wav_path: Path) -> float:
    """Return duration in seconds of WAV file"""
    try:
        with wave.open(str(wav_path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / rate
    except Exception:
        return 0.0


def transcribe_audio(
    wav_path: Path, model_name: str = "small", cache_dir: str = None
) -> str:
    """Transcribe WAV to text using Whisper"""
    try:
        import whisper
    except ImportError:
        print(
            "Error: whisper library not installed. Install with `pip install openai-whisper`.",
            file=sys.stderr,
        )
        sys.exit(1)
    if cache_dir:
        os.environ["WHISPER_CACHE"] = cache_dir
    try:
        model = whisper.load_model(model_name)
    except Exception as e:
        print(f"Error loading Whisper model '{model_name}': {e}", file=sys.stderr)
        sys.exit(1)
    try:
        result = model.transcribe(str(wav_path), language="en")
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        sys.exit(1)
    return result.get("text", "").strip()


def compute_wpm(transcript: str, duration_sec: float) -> float:
    """Compute words per minute from transcript and audio duration"""
    words = re.findall(r"\b\w+\b", transcript)
    word_count = len(words)
    minutes = duration_sec / 60.0 if duration_sec > 0 else 1e-6
    return word_count / minutes


def compute_filler_stats(transcript: str) -> dict:
    """Compute filler ratio (%) and most common filler"""
    words = [w.lower() for w in re.findall(r"\b\w+\b", transcript)]
    fillers = {
        "um",
        "uh",
        "er",
        "ah",
        "like",
        "you know",
        "so",
        "actually",
        "basically",
        "right",
    }
    # Count occurrences; for multi-word filler 'you know', handle separately
    count = 0
    freq = {}
    # First handle 'you know' sequences
    joined = transcript.lower()
    youknow_count = len(re.findall(r"\byou know\b", joined))
    if youknow_count:
        count += youknow_count
        freq["you know"] = youknow_count
    # Remove occurrences of 'you know' from word list for single-word counting
    words_single = []
    skip_next = False
    wlist = transcript.lower().split()
    for i, w in enumerate(wlist):
        if skip_next:
            skip_next = False
            continue
        if w == "you" and i + 1 < len(wlist) and wlist[i + 1] == "know":
            skip_next = True
            continue
        words_single.append(w)
    # Count single-word fillers
    for w in words_single:
        if w in fillers:
            count += 1
            freq[w] = freq.get(w, 0) + 1
    total_words = len(words)
    ratio = (count / total_words * 100) if total_words > 0 else 0.0
    most_common = None
    if freq:
        most_common = max(freq.items(), key=lambda x: x[1])[0]
    return {"filler_ratio": round(ratio, 1), "most_common_filler": most_common}


def main():
    parser = argparse.ArgumentParser(
        description="Extract transcript, WPM, and filler stats from MP4 video using Whisper."
    )
    parser.add_argument("video", help="Path to input MP4 file")
    parser.add_argument(
        "--json", default="output.json", help="Path to output JSON file"
    )
    parser.add_argument(
        "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size",
    )
    parser.add_argument("--cache-dir", help="Custom Whisper cache directory")
    args = parser.parse_args()

    video_path = Path(args.video)
    if not video_path.exists():
        print(f"Error: File not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    wav_path = extract_audio(video_path)
    duration = get_audio_duration(wav_path)
    transcript = transcribe_audio(
        wav_path, model_name=args.model, cache_dir=args.cache_dir
    )
    try:
        os.remove(wav_path)
    except Exception:
        pass

    wpm = compute_wpm(transcript, duration)
    filler_stats = compute_filler_stats(transcript)
    output = {
        "transcript": transcript,
        "wpm": round(wpm, 1),
        "filler_ratio": filler_stats.get("filler_ratio"),
        "most_common_filler": filler_stats.get("most_common_filler"),
    }
    try:
        with open(args.json, "w") as f:
            json.dump(output, f, indent=2)
    except Exception as e:
        print(f"Error writing JSON output: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
