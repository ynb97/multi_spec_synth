from matplotlib import pyplot as plt
import json

import numpy as np
import wave
import sys


spf = wave.open("out.wav", "r")

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, np.int16)
plt.figure(figsize = (10,7))


# If Stereo
if spf.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)

# plt.figure(1)
plt.title("Signal Wave...")
ymax = max(signal)
plt.plot(signal)


with open("segments.json", 'rb') as f:
   segments = json.loads(f.read())


# plot segment identifed as speech
for segment in segments:
    if segment['is_speech']:
        print(segment)
        plt.plot([ segment['start'], segment['stop'] - 1], [ymax * 1.1, ymax * 1.1], color = 'orange')

plt.xlabel('sample')
plt.grid()

plt.show()