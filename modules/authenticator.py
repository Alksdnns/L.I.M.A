from pathlib import Path
import sounddevice as sd
import scipy.io.wavfile as wav

def record_and_save_user_voice(duration=5):
    print("🎙️ Recording your voice sample for 5 seconds...")
    fs = 16000
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    user_folder = Path("user_voices")
    user_folder.mkdir(exist_ok=True)

    # Find next available user file number
    existing_files = list(user_folder.glob("user_*.wav"))
    next_num = len(existing_files) + 1
    filename = user_folder / f"user_{next_num}.wav"

    wav.write(str(filename), fs, recording)
    print(f"✅ Voice recorded and saved as {filename}")
    return filename
