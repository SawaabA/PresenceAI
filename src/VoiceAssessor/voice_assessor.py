# voice_assessor.py
"""
Voice Assessor ‒ prototype implementation
========================================

Given an **audio file** (WAV/MP3/OGG … or the audio track you have extracted from a video),
this script analyses the speech signal and produces a JSON‑serialisable dictionary with the
following high‑level ratings:

- pronunciation_score
- fluency_score
- vocabulary_score
- emotion_profile  (probability distribution over basic emotions)
- melody_score
- anxiety_score
- confidence_score
- filler_word_ratio
- speech_pace_wpm
- pause_stats        (count / total_pause_time / longest_pause)
- overall_score

The code relies entirely on **open‑source libraries** so that you can run it locally for free
in a hackathon setting:

* `whisper`             – ASR + optional word‑level timestamps
* `opensmile`           – prosodic & voice‑quality features (pitch, jitter, shimmer, loudness)
* `webrtcvad`           – robust voice‑activity detection for pause analysis
* `speechbrain`         – lightweight pre‑trained emotion‑recognition model
* `nltk` / `textstat`   – lexical‑richness metrics
* `numpy`, `pandas`, `scipy` – numeric helpers
* `soundfile`, `torchaudio`  – audio I/O

Install dependencies with (example):

```bash
pip install openai-whisper opensmile webrtcvad speechbrain soundfile torchaudio nltk textstat numpy pandas scipy rapidfuzz
```

For first‑time NLTK use you may also have to download tokenisers:

```python
import nltk; nltk.download('punkt')
```

Usage (CLI):

```bash
python voice_assessor.py /path/to/audio.wav --json-out metrics.json
```

or import as a module:

```python
from voice_assessor import assess_voice
metrics = assess_voice("audio.wav")
print(metrics)
```

The scoring formulas are intentionally **simple and transparent** so you can tweak weights
during your hackathon.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, List

import librosa
import numpy as np
import opensmile
import soundfile as sf
import torch
import webrtcvad
from rapidfuzz import fuzz  # lightweight string fuzzy‑matching for filler detection

# Whisper ASR
import whisper

# SpeechBrain emotion recognition
from speechbrain.pretrained import EncoderClassifier

# Text / lexical metrics
import nltk
from nltk.tokenize import word_tokenize
from textstat import lexicon_count

FILLER_WORDS = {"um", "uh", "erm", "hmm", "like", "you know", "so", "actually", "basically"}

def transcribe_audio(path: Path, model_name: str = "base") -> Dict:
    """Run Whisper ASR and return transcription + word‑level timing info."""
    model = whisper.load_model(model_name)
    result = model.transcribe(str(path), word_timestamps=True, verbose=False)
    return result  # dict with keys: text, segments


def extract_prosody(path: Path) -> Dict[str, float]:
    """Call openSMILE to compute core prosodic features (pitch, jitter, shimmer, loudness)."""
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.ComParE_2016,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    features = smile.process_file(str(path))

    # Select representative statistics
    def safe_mean(col):
        return float(features[col].iloc[0]) if col in features else float("nan")

    return {
        "pitch_mean": safe_mean("F0_sma3nz_flatten_median") + 1e-9,
        "pitch_std": safe_mean("F0_sma3nz_flatten_stddev") + 1e-9,
        "jitter_abs": safe_mean("jitterLocal_sma3nz_flatten_median"),
        "shimmer_abs": safe_mean("shimmerLocal_sma3nz_flatten_median"),
        "loudness_mean": safe_mean("pcm_LOGenergy_sma_flatten_median"),
    }


def detect_pauses(path: Path, frame_duration_ms: int = 30, vad_aggressiveness: int = 2) -> Dict[str, float]:
    """Use webrtcvad to compute pause statistics (count, total, longest)."""
    wf = sf.SoundFile(str(path))
    audio, sr = sf.read(str(path))

    vad = webrtcvad.Vad(vad_aggressiveness)
    num_samples_per_frame = int(sr * frame_duration_ms / 1000)

    # If stereo convert to mono
    if audio.ndim == 2:
        audio = audio.mean(axis=1)

    # Convert to 16‑bit PCM as bytes (required by webrtcvad)
    int16 = np.int16(audio / np.max(np.abs(audio)) * 32767)
    bytes_audio = int16.tobytes()

    n_frames = len(int16) // num_samples_per_frame
    voiced = []
    for i in range(n_frames):
        start = i * num_samples_per_frame * 2  # 2 bytes per sample
        end = start + num_samples_per_frame * 2
        frame = bytes_audio[start:end]
        voiced.append(vad.is_speech(frame, sample_rate=sr))

    pauses = []
    current = 0
    for v in voiced:
        if not v:
            current += 1
        elif current > 0:
            pauses.append(current)
            current = 0
    if current > 0:
        pauses.append(current)

    pause_durations_sec = [p * frame_duration_ms / 1000 for p in pauses]

    if not pause_durations_sec:
        return {"pause_count": 0, "total_pause": 0.0, "longest_pause": 0.0}

    return {
        "pause_count": len(pause_durations_sec),
        "total_pause": float(sum(pause_durations_sec)),
        "longest_pause": float(max(pause_durations_sec)),
    }


def analyse_emotion(path: Path, device: str = "cpu") -> Dict[str, float]:
    """Predict emotion probabilities using SpeechBrain's SEMD model."""
    classifier = EncoderClassifier.from_hparams(
        source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
        savedir="pretrained_models/sb_emotion",
        run_opts={"device": device},
    )
    signal, sr = librosa.load(str(path), sr=16000)
    # speechbrain expects tensor [batch, time]
    with torch.no_grad():
        prediction = classifier.classify_batch(torch.tensor(signal).unsqueeze(0))
    probs = torch.softmax(prediction[0], dim=-1)[0]
    labels = classifier.hparams.label_encoder.decode_ndim(torch.arange(len(probs))).tolist()
    return {label: float(prob) for label, prob in zip(labels, probs)}


def lexical_metrics(transcript: str) -> Dict[str, float]:
    """Compute lexical diversity metrics from transcript text."""
    words = word_tokenize(transcript.lower())
    vocab_size = len(set(words))
    total_words = len(words)
    ttr = vocab_size / (total_words + 1e-9)
    # Use textstat lexicon_count as an alternate vocabulary richness measure
    lex_count = lexicon_count(transcript, removepunct=True)
    return {
        "vocab_size": vocab_size,
        "total_words": total_words,
        "type_token_ratio": ttr,
        "lexicon_count": lex_count,
    }


def filler_stats(words: List[str]) -> Dict[str, float]:
    filler = [w for w in words if any(fuzz.ratio(w, f) > 85 for f in FILLER_WORDS)]
    filler_ratio = len(filler) / (len(words) + 1e-9)
    return {"filler_count": len(filler), "filler_ratio": filler_ratio}


def compute_scores(metrics: Dict[str, float | Dict]) -> Dict[str, float | Dict]:
    """Combine raw metrics into high‑level scores on a 0‑100 scale."""

    # Simple heuristics – tweak weights as needed
    pace_score = 100 - abs(metrics["speech_pace_wpm"] - 150) * 0.5  # ideal ~150 wpm
    pace_score = max(0, min(100, pace_score))

    filler_penalty = metrics["filler_ratio"] * 400  # 0.25 filler ratio => −100
    filler_score = max(0, 100 - filler_penalty)

    pause_penalty = metrics["pause_stats"]["total_pause"] / metrics["audio_duration_sec"] * 200
    pause_score = max(0, 100 - pause_penalty)

    fluency_score = (pace_score * 0.4 + filler_score * 0.3 + pause_score * 0.3)

    vocab_score = min(100, metrics["lexical"]["type_token_ratio"] * 3000)  # TTR 0.05 => 150, capped

    pronunciation_score = 80  # Placeholder – no reference script. Improve with lang‑specific tools.

    melody_score = min(100, metrics["prosody"]["pitch_std"] * 10)  # higher std = more prosodic variation

    anxiety_score = min(100, metrics["prosody"]["jitter_abs"] * 5000)
    confidence_score = 100 - anxiety_score

    # Overall score = weighted average
    overall = (fluency_score * 0.3 + vocab_score * 0.2 + confidence_score * 0.2 + melody_score * 0.1 + pronunciation_score * 0.2)

    return {
        "pronunciation_score": pronunciation_score,
        "fluency_score": round(fluency_score, 1),
        "vocabulary_score": round(vocab_score, 1),
        "melody_score": round(melody_score, 1),
        "anxiety_score": round(anxiety_score, 1),
        "confidence_score": round(confidence_score, 1),
        "overall_score": round(overall, 1),
    }


def assess_voice(audio_path: str | Path, whisper_model: str = "base", device: str = "cpu") -> Dict:
    """Main high‑level function: returns a nested dict of raw metrics + scores."""
    path = Path(audio_path)
    if not path.exists():
        raise FileNotFoundError(path)

    # --- ASR ---
    transcription = transcribe_audio(path, model_name=whisper_model)
    words = []
    total_duration = transcription.get("duration", None)
    if total_duration is None:
        # derive duration via librosa
        total_duration = librosa.get_duration(filename=str(path))

    for seg in transcription["segments"]:
        words.extend([w["text"].strip().lower() for w in seg["words"]])

    speech_pace_wpm = len(words) / (total_duration / 60 + 1e-9)

    # --- Filler words ---
    filler = filler_stats(words)

    # --- Prosody ---
    prosody = extract_prosody(path)

    # --- Pauses ---
    pause_stats = detect_pauses(path)

    # --- Emotion ---
    emotion = analyse_emotion(path, device=device)

    # --- Lexical richness ---
    lexical = lexical_metrics(transcription["text"])

    raw_metrics = {
        "audio_duration_sec": total_duration,
        "speech_pace_wpm": speech_pace_wpm,
        "prosody": prosody,
        "pause_stats": pause_stats,
        "filler_ratio": filler["filler_ratio"],
        "filler_count": filler["filler_count"],
        "emotion_profile": emotion,
        "lexical": lexical,
    }

    scores = compute_scores(raw_metrics)
    return {**raw_metrics, **scores, "transcript": transcription["text"].strip()}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli():
    parser = argparse.ArgumentParser(description="Voice Assessor – analyse speech audio and output metrics JSON")
    parser.add_argument("audio", type=Path, help="Path to audio file (wav/mp3/flac…)")
    parser.add_argument("--json-out", type=Path, default=None, help="Optional path to write JSON metrics")
    parser.add_argument("--model", default="base", help="Which Whisper model to use (tiny, base, small, medium, large)")
    parser.add_argument("--device", default="cpu", help="Torch device for emotion model (cpu or cuda)")

    args = parser.parse_args()
    result = assess_voice(args.audio, whisper_model=args.model, device=args.device)

    print(json.dumps(result, indent=2))
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
            print(f"\nMetrics written to {args.json_out}")


if __name__ == "__main__":
    _cli()
