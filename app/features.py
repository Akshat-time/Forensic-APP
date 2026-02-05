import numpy as np
import librosa
import scipy.stats

def extract_features(audio_io):
    """
    Extracts acoustic features from an audio stream using Librosa.
    """
    # Load audio (sr=None preserves native sampling rate)
    # OPTIMIZATION: Limit to first 10 seconds to prevent "Request Timeout" on free CPU instances.
    try:
        y, sr = librosa.load(audio_io, sr=None, duration=10)
    except Exception as e:
        # Fallback for empty or corrupted audio
        print(f"Error loading audio: {e}")
        return _get_fallback_features()

    # 1. Fundamental Frequency (F0) Extraction
    # fmin/fmax range for human speech
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr)
    
    # Filter out unvoiced parts (where f0 is NaN)
    f0_clean = f0[~np.isnan(f0)]

    # 2. RMS Energy for Amplitude/Pause analysis
    rms = librosa.feature.rms(y=y)[0]
    
    # --- Feature Calculations ---

    # Jitter: Cycle-to-cycle variation in pitch
    if len(f0_clean) > 1:
        jitter = np.mean(np.abs(np.diff(f0_clean))) / np.mean(f0_clean)
    else:
        jitter = 0.0

    # Shimmer: Cycle-to-cycle variation in amplitude
    # (Approximated using RMS frames instead of individual periods)
    if len(rms) > 1:
        # Avoid division by zero
        mean_rms = np.mean(rms)
        if mean_rms > 0:
            shimmer = np.mean(np.abs(np.diff(rms))) / mean_rms
        else:
            shimmer = 0.0
    else:
        shimmer = 0.0

    # Prosody Drift: Standard deviation of pitch over time
    if len(f0_clean) > 0:
        prosody_drift = np.std(f0_clean) / np.mean(f0_clean)
    else:
        prosody_drift = 0.0

    # Pause Entropy: Randomness of silence durations
    # Define silence as audio below a threshold (e.g., -40dB relative to peak)
    silence_thresh = 1e-4 # Simple absolute threshold approx
    is_silent = rms < silence_thresh
    
    # Find durations of continuous silence
    silence_durations = []
    current_duration = 0
    for silent in is_silent:
        if silent:
            current_duration += 1
        else:
            if current_duration > 0:
                silence_durations.append(current_duration)
                current_duration = 0
    if current_duration > 0: # Catch trailing silence
        silence_durations.append(current_duration)

    if silence_durations:
        # Convert frames to seconds (hop_length default is 512)
        durations_sec = np.array(silence_durations) * 512 / sr
        # Calculate entropy of the distribution of pause lengths
        prob_dist = durations_sec / np.sum(durations_sec)
        pause_entropy = scipy.stats.entropy(prob_dist)
    else:
        pause_entropy = 0.0

    # Noise Variance: Signal variance in silent regions
    # Create a mask for the raw audio samples corresponding to silent frames
    # Expanding the low-res RMS mask to audio usage is tricky, simpler to assume
    # low energy frames represent background.
    # We'll take the variance of the raw signal y where the corresponding RMS frame was silent.
    # Note: rms has fewer frames than y. We need to expand the mask.
    noise_variance = 0.0
    if np.any(is_silent):
        # Repeat each boolean flag 512 times (hop_length)
        # Handle edge case where length might not match exactly due to padding
        y_silent_mask = np.repeat(is_silent, 512)[:len(y)]
        if len(y_silent_mask) < len(y):
             # Pad with False if short
             y_silent_mask = np.pad(y_silent_mask, (0, len(y) - len(y_silent_mask)), 'constant')
        
        silent_samples = y[y_silent_mask]
        if len(silent_samples) > 0:
            noise_variance = np.var(silent_samples)
    
    # Amplitude Variance: Global amplitude consistency
    amplitude_variance = np.var(np.abs(y))

    # Sanitize inputs (numpy types to python float)
    return {
        "pause_entropy": float(pause_entropy),
        "jitter": float(jitter),
        "shimmer": float(shimmer),
        "noise_variance": float(noise_variance),
        "prosody_drift": float(prosody_drift),
        "amplitude_variance": float(amplitude_variance),
    }

def _get_fallback_features():
    """Returns safe default values if analysis fails."""
    return {
        "pause_entropy": 0.0,
        "jitter": 0.0,
        "shimmer": 0.0,
        "noise_variance": 0.0,
        "prosody_drift": 0.0,
        "amplitude_variance": 1.0, # Default high to avoid false positive AI
    }
