ffmpeg -i $1 -acodec pcm_s16le -ac 1 -ar 16000 /home/yash/projects/text_to_speech/coqui_tts/multi_spec_synth/app/backend/audio/$1.wav