import streamlit as st
import os
import json
from TTS.api import TTS
from google.cloud import translate_v2 as translate
import torch
import matplotlib.pyplot as plt
# import sounddevice as sd
import wavio
from datetime import datetime


device = "cuda" if torch.cuda.is_available() else "cpu"
translate_language_code_mapping = {
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Hindi": "hi",
    "Italian": "it",
    "Japanese": "ja",
    "Korean": "ko",
    "Polish": "pl",
    "Portuguese": "pt",  # This is for all Portuguese varieties (excluding Brazilian Portuguese)
    "Portuguese (Brazil)": "pt-BR",
    "Russian": "ru",
    "Turkish": "tr",
    "Chinese Simplified": "zh-CN"
}

tts_language_code_mapping = {
  "English": "en-US",  # You can choose other English variations like "en-GB"
  "German": "de-DE",
  "French": "fr-FR",
  "Spanish": "es-ES",
  "Hindi": "hi-IN",
  "Italian": "it-IT",
  "Japanese": "ja-JP",
  "Korean": "ko-KR",
  "Polish": "pl-PL",
  "Portuguese": "pt-PT",  # European Portuguese
  "Portuguese (Brazil)": "pt-BR",
  "Russian": "ru-RU",
  "Turkish": "tr-TR",
  "Chinese Simplified": "zh-CN",
}

output_audio = os.path.join("data", "generated_audio", "output.mp3")
options = list(translate_language_code_mapping.keys())

def generate_audio(input_text, language):

    # google_tts(input_text, "English", os.path.join("data", "generated_audio", "output.mp3"))
    
    local_tts(input_text, language=language)


def play_audio(file_path=None):
    print("Playing audio...*****")
    if not file_path:
        file_path = os.path.join("data", "generated_audio", "output.wav")
    try:
        # Placeholder for audio data (replace with your audio processing logic)
        audio_data = open(file_path, 'rb')
        if audio_data:
            # Implement your audio playback functionality here
            # audio_file = open(os.path.join('data', 'Piotr Hummel - Mainland.mp3.mp3'), 'rb')
            audio_bytes = audio_data.read()

            st.audio(audio_bytes, format='audio/wav')
            st.success("Audio playback started!")
        else:
            st.warning("No audio data available to play.")
    except FileNotFoundError:
        audio_data = None
        st.info("No audio file to play yet")
    except IsADirectoryError:
        audio_data = None
        st.info("No audio")

# Options for the dropdown selector


def save_file(uploaded_file, filename):
  """Saves uploaded file to the specified location."""
  with open(os.path.join("data", "uploads", filename), "wb") as f:
    f.write(uploaded_file.read())
  st.success(f"File '{filename}' saved successfully!")


def google_translate(text, language="German"):

    # Your Google Cloud project ID
    project_id = "casst2"

    # Create a translation client object
    client = translate.Client()

    # Text to translate
    # text = "Hello, how are you?"

    # Destination language
    destination_language = translate_language_code_mapping[language]  # French

    # Translation with Cloud Translation API
    translation = client.translate(text, target_language=destination_language)

    # Print translated text
    print(translation)
    return translation["translatedText"]
    # print(translation["text"])


def google_tts(text, language=None, file_path=None):
  """
  Synthesizes speech from the provided text and saves it to the specified file.

  Args:
      text: The text to be synthesized.
      language_code: The language code of the text (e.g. "en-US").
      filename: The path to save the synthesized audio file.
  """

  if not language:
      raise Exception("Please provide language for generating audio !")
  if not file_path:
      raise Exception("Please provide a path to store the generated audio file !")
  
  # Create a Text-to-Speech client object
  client = texttospeech.TextToSpeechClient()

  # Set the text input to be synthesized
  synthesis_input = texttospeech.SynthesisInput(text=text)

  # Set the voice configuration
  voice = texttospeech.VoiceSelectionParams(
      language_code=tts_language_code_mapping[language],
      name="en-US-Wavenet-A"  # You can choose a different voice here (see list of voices)
  )

  # Set the audio format for the synthesized speech
  audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

  # Build the request object
  request = texttospeech.SynthesizeSpeechRequest(
      input=synthesis_input, voice=voice, audio_config=audio_config
  )

  # Synthesize speech and save it to the specified file
  response = client.synthesize_speech(request=request)
  with open(file_path, "wb") as out:
      out.write(response.audio_content)
      print(f'Text converted to speech and saved to: {file_path}')


def list_voices():
    """Lists the available voices."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()


    available_voices = []
    for voice in voices.voices:
        # Display the voice's name. Example: tpc-vocoded
        print(f"Name: {voice.name}")

        # Display the supported language codes for this voice. Example: "en-US"
        languages = []
        for language_code in voice.language_codes:
            languages.append(language_code)
            # print(f"Supported language: {language_code}")

        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

        # Display the SSML Voice Gender
        # print(f"SSML Voice Gender: {ssml_gender.name}")

        # Display the natural sample rate hertz for this voice. Example: 24000
        # print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

        available_voices.append({
            "name": voice.name,
            "supported_language": languages,
            "ssml_voice_gender": ssml_gender.name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz
            })
        
    with open("data/available_voices.json", "w") as f:
        json.dump(available_voices, f)


def log_error(*params):
    with open("errors.txt", "a") as f:
        f.write(str(datetime.now())+str(params)+'\n')


def local_tts(input_text, speaker_audio=None, language=None, output_file=None, model_name=None):

    # List available 🐸TTS models
    # print(TTS().list_models())
    try:
        if not language:
            language = "en"
        else:
            language = translate_language_code_mapping[language].lower()
        if not output_file:
            output_file = os.path.join("data", "generated_audio", "output.wav")
        else:
            output_file = os.path.join("data", "generated_audio", output_file)
        if not model_name:
            model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        if not speaker_audio:
            speaker_audio = "recording.wav"

        # Init TTS
        # tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", model_path="/tmp/tts_models").to(device)
        # tts = TTS("tts_models/multilingual/multi-dataset/xtts_v1.1", model_path="/tmp/tts_models").to(device)
        # tts = TTS("tts_models/multilingual/multi-dataset/your_tts", model_path="/tmp/tts_models").to(device)
        # tts = TTS("tts_models/multilingual/multi-dataset/bark", model_path="/tmp/tts_models").to(device)
        print("here")
        tts = TTS(model_name).to(device)

        # Run TTS
        # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
        # Text to speech list of amplitude values as output
        # wav = tts.tts(text="Hello world!", speaker_wav="my/cloning/audio.wav", language="en")
        # Text to speech to a file

        print("here")

        tts.tts_to_file(
            text=input_text,
            speaker_wav=speaker_audio, 
            language=language, 
            file_path=output_file
        )
    except Exception as e:
        log_error(e)


# Function to create graphs
def create_graph(model_names, metric_name, metric_values):
    plt.figure(figsize=(8, 5))
    plt.bar(model_names, metric_values, color='skyblue')
    plt.xlabel("Model Name")
    plt.ylabel(metric_name)
    plt.title(f"{metric_name} Comparison")
    plt.grid(axis='y')
    st.pyplot()

def record_audio():
    # Recording parameters
    duration = 60  # seconds
    fs = 44100  # sampling rate
    channels = 2  # stereo

    # Start recording
    print("Recording...")
    # recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    # sd.wait()
    recording = None
    print("Recording finished!")

    # Save recording to a file
    filename = "recording.wav"
    wavio.write(filename, recording, fs, sampwidth=2)

    print(f"Recording saved as: {filename}")


def translate_text(text, region="us-central1", source_language="en", target_language="es"):
  """
  Translates text using Google Translate API with error handling.

  Args:
      text (str): Text to be translated.
      project_id (str): Google Cloud Project ID with Translate API enabled.
      region (str, optional): Google Cloud region where the API is hosted (defaults to "us-central1").
      source_language (str, optional): Source language code (defaults to "en" for English).
      target_language (str, optional): Destination language code (defaults to "es" for Spanish).

  Returns:
      str: Translated text or None if an error occurs.
  """

  target_language = translate_language_code_mapping[target_language]
  # Authenticate using your Google Cloud project credentials
  try:
      project_id = "casst2"
      translate_client = translate.Client(project_id=project_id)
  except Exception as e:
      print(f"An error occurred during authentication: {e}")
      return None

  # Prepare translation request
  text = text.encode("utf-8")  # Ensure text is encoded properly
  try:
      translation = translate_client.translate(
          input_=text,
          source_language=source_language,
          target_language=target_language
      )
  except Exception as e:
      print(f"An error occurred during translation: {e}")
      return None

  return translation["translatedText"]


if __name__ == "__main__":
    # translated_text = google_translate("Hello, how are you ?", language="German")
    # print(translated_text)

    # language = "German"
    # filename = "output.mp3"

    # synthesize_speech(text, language=language, file_path=output_audio)

    # list_voices()

    # for key, value in [("English", "en")]:
    #     local_tts(
    #         google_translate("This is an AI generated speech audio with the voice cloned from a given audio sample.", key), 
    #         key,
    #         f"output0_{value}.wav"
    #     )
    #     local_tts(
    #         google_translate("The boy was there when the sun rose.", key), 
    #         key,
    #         f"output1_{value}.wav"
    #     )
    #     local_tts(
    #         google_translate("A rod is used to catch pink salmon.", key), 
    #         key,
    #         f"output2_{value}.wav"
    #     )
    #     local_tts(
    #         google_translate("The source of the huge river is the clear spring.", key), 
    #         key,
    #         f"output3_{value}.wav"
    #     )
    #     local_tts(
    #         google_translate("Kick the ball straight and follow through.", key), 
    #         key,
    #         f"output4_{value}.wav"
    #     )
    #     local_tts(
    #         google_translate("Help the woman get back to her feet.", key), 
    #         key,
    #         f"output5_{value}.wav"
    #     )
    #     local_tts(
    #         google_translate("A pot of tea helps to pass the evening.", key), 
    #         key,
    #         f"output6_{value}.wav"
    #     )
    #     local_tts(
    #         google_translate("Smoky fires lack flame and heat.", key), 
    #         key,
    #         f"output7_{value}.wav"
    #     )
    #     local_tts(
    #         google_translate("The soft cushion broke the man's fall.", key), 
    #         key,
    #         f"output8_{value}.wav"
    #     )
    #     local_tts(
    #         google_translate("The salt breeze came across from the sea.", key), 
    #         key,
    #         f"output9_{value}.wav"
    #     )
    with open("data.txt") as f:
        for i, line in enumerate(f.readlines()):
            if line.strip():
                local_tts(
                    line,
                    speaker_audio=["trimmed_audio_en.mp3", "trimmed_audio_en1.mp3", "trimmed_audio_en2.mp3"], 
                    language="English",
                    output_file=f"output_{i}.wav"
                )
    # for item in TTS().list_models():
    # print(TTS().list_models().list_tts_models())
    # record_audio()
    pass