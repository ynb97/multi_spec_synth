import torch
from diarizers import SegmentationModel
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
"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"


"""
PEAKER aisvi 1 0.200000 15.360000 <NA> <NA> spk00 <NA> <NA>
SPEAKER aisvi 1 185.760000 14.840000 <NA> <NA> spk00 <NA> <NA>
SPEAKER aisvi 1 201.560000 10.680000 <NA> <NA> spk00 <NA> <NA>
SPEAKER aisvi 1 212.680000 8.400000 <NA> <NA> spk00 <NA> <NA>
SPEAKER aisvi 1 249.680000 9.960000 <NA> <NA> spk00 <NA> <NA>
SPEAKER aisvi 1 329.600000 6.720000 <NA> <NA> spk00 <NA> <NA>
SPEAKER aisvi 1 395.840000 12.520000 <NA> <NA> spk00 <NA> <NA>
SPEAKER aisvi 1 465.440000 2.920000 <NA> <NA> spk00 <NA> <NA>
SPEAKER aisvi 1 102.560000 6.400000 <NA> <NA> spk01 <NA> <NA>
SPEAKER aisvi 1 115.240000 1.600000 <NA> <NA> spk02 <NA> <NA>
SPEAKER aisvi 1 118.120000 3.120000 <NA> <NA> spk02 <NA> <NA>
SPEAKER aisvi 1 21.480000 9.960000 <NA> <NA> spk00 <NA> <NA>
SPEAKER aisvi 1 121.960000 0.480000 <NA> <NA> spk02 <NA> <NA>
SPEAKER aisvi 1 123.080000 2.920000 <NA> <NA> spk02 <NA> <NA>
SPEAKER aisvi 1 126.640000 2.600000 <NA> <NA> spk02 <NA> <NA>
SPEAKER aisvi 1 39.560000 1.080000 <NA> <NA> spk03 <NA> <NA>
SPEAKER aisvi 1 59.280000 1.400000 <NA> <NA> spk03 <NA> <NA>
"""
# segmentation_model = SegmentationModel().from_pretrained('diarizers-community/speaker-segmentation-fine-tuned-callhome-jpn')
segmentation_model = SegmentationModel().from_pretrained('/home/model-server/model-store/finetuned')

pipeline = Pipeline.from_pretrained("pyannote_local_config.yml")


segmentation_model = segmentation_model.to_pyannote_model()
pipeline._segmentation.model = segmentation_model

# send pipeline to GPU (when available)
pipeline.to(torch.device("cuda"))

with ProgressHook() as hook:
    # apply pretrained pipeline
    diarization = pipeline("out.wav", hook=hook, num_speakers=5)

# print the result
with open("out.txt", 'a') as f:
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        f.write(f"{turn.start:.1f} {turn.end:.1f} {speaker.split('_')[1]}"+"\n")
        # print(f"{turn.start:.1f} {turn.end:.1f} {speaker.split('_')[1]}")