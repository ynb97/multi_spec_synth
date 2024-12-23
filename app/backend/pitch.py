from pydub import AudioSegment
import librosa

def extract_pitch(audio_filepath):
  """
  Extracts pitch data (fundamental frequency) from an audio file.

  Args:
      audio_filepath (str): Path to the audio file.

  Returns:
      tuple: (time_stamps, pitches)
          time_stamps (np.ndarray): Array of time stamps for each pitch value.
          pitches (np.ndarray): Array of extracted pitch values in Hz.
  """
  # Load audio
  y, sr = librosa.load(audio_filepath)

  # Extract pitch using yp tracking algorithm (adjust parameters if needed)
  pitches, _ = librosa.core.yp_harmonic(y, sr=sr, n_fft=2048, hop_length=512)

  # Filter out potential tracking errors (adjust threshold if necessary)
  pitches = pitches[pitches > 0]

  # Get time stamps for each pitch
  time_stamps = librosa.core.frames_to_time(np.arange(len(pitches)), sr=sr, hop_length=512)

  return time_stamps, pitches


# Convert MP3 to WAV
# Replace with your MP3 file path

mp3_file = "Hindi_Female_1.mp3"
sound = AudioSegment.from_mp3(mp3_file)
wav_file = mp3_file.replace(".mp3", ".wav")
sound.export(wav_file, format="wav")

print(f"MP3 converted to WAV: {wav_file}")


# Example usage
audio_file = "Hindi_Female_1.wav"  # Replace with your audio file path

time_stamps, pitches = extract_pitch(audio_file)

print("Time Stamps (seconds):", time_stamps)
print("Pitches (Hz):", pitches)
