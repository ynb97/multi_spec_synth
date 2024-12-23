import os
import ffmpeg
import json


def perform_vad():
  import torch

  torch.set_num_threads(1)
  model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad')
  (get_speech_timestamps, _, read_audio, _, _) = utils

  wav = read_audio('out.wav', sampling_rate=16000)
  speech_timestamps = get_speech_timestamps(
    wav, 
    model, 
    sampling_rate=16000, 
    visualize_probs=False, 
    return_seconds=True,
    min_speech_duration_ms=126,
    window_size_samples=8,
    threshold=0.151
  )

  with open("speech_timestamps", 'w') as f:
    json.dump(speech_timestamps, f)

def split_audio():
  from decimal import Decimal, getcontext

  OUT_DIR = "split_audio"
  filelist = [ f for f in os.listdir(os.path.join(os.path.abspath(os.path.curdir), OUT_DIR)) ]
  for f in filelist:
    os.remove(os.path.join(os.path.abspath(os.path.curdir), OUT_DIR, f))
  
  speakers = {}
  with open("annotations.txt", 'r') as f:
    for i, line in enumerate(f.readlines()):
      line = line.split()
      speaker = line[-3]

      # getcontext().prec = 3
      start, end = Decimal(line[3]), Decimal(line[4])
      duration = float(end - start)
      if duration != 0.0:
        # if speaker not in speakers.keys():
        #   speakers.update({speaker: {"start":}})
      # print(start, end)

      # for i, item in enumerate(speech_timestamps):
        # open a file, from `ss`, for duration `t`
        print(os.path.join(os.path.abspath(os.path.curdir), "audio", line[1] + ".mkv.wav"))
        stream = ffmpeg.input(os.path.join(os.path.abspath(os.path.curdir), "audio", line[1] + ".mkv.wav"), ss=start, t=duration)
        # output to named file
        stream = ffmpeg.output(stream, os.path.join(os.path.abspath(os.path.curdir), OUT_DIR, f"{line[1]}_{speaker}_{str(i).zfill(3)}.wav")).overwrite_output()
        # this was to make trial and error easier
        # stream = ffmpeg.overwrite_output(stream)

        # and actually run
        ffmpeg.run(stream, cmd='/usr/local/bin/ffmpeg')

if __name__ == "__main__":
  import sys
  import os

  available_options = ["--run-vad", "--split-files"]
  args = sys.argv[1:]

  option_args = [item for item in args if "--" in item]

  for option in option_args:
      if option not in available_options:
          nl = '\n'
          raise Exception(
              f"{nl}Invalid option: {option}{nl}"
              f"Available options are: {', '.join(available_options)}"
          )
  
  if len(args) >= 1:
    if "--run-vad" in args:
      perform_vad()
    elif "--split-files" in args:
      split_audio()
    else:
      for option in option_args:
        if option not in available_options:
            nl = '\n'
            raise Exception(
                f"{nl}Invalid option: {option}{nl}"
                f"Available options are: {', '.join(available_options)}"
            )