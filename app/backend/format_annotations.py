import os
import pysrt
import pykakasi

kks = pykakasi.kakasi()


DATA_DIR = "custom_data"
files = os.listdir(os.path.join(os.path.abspath(os.curdir), DATA_DIR))


speaker_variations = {
    "okabe": [
        "岡部", "おかべりんたろう", "きょうま", "ほうおういんきょうま", "未来の岡部", "過去の岡部", "ほうおういん"
    ],
    "kurisu": [
        "紅莉栖", "まきせくりす", "まきせ", "くりす", "牧瀬紅莉栖"
    ],
    "mayuri": [
        "まゆり", "しいな"
    ],
    "itaru": [
        "橋田", "はしだいたる", "いたる", "はしだ"
    ],
    "suzuha": [
        "鈴羽", "あまねすずは", "すず", "すずは"
    ],
    "rukako": [
        "るか", "うるしばら", "漆原"
    ],
    "faris": [
        "フェイリス"
    ],
    "moeka": [
        "萌郁", "きりゅうもえか", "もえか", "きりゅう"
    ],
    "mrbraun": [
        "天王寺", "てんのうじゆうご"
    ],
    "drnakabachi": [
        "中鉢博士", "なかばち"
    ],
    "titer": [
        "タイター"
    ],
    "attackers": [
        "ヴァイラルアタッカーズ１", "ヴァイラルアタッカーズ２", "ラウンダー３", "ヴァイラルアタッカーズ３"
    ],
    "nae": [
        "なえ"
    ],
    "maid": [
        "メイド"
    ],
    "clerk": [
        "店員"
    ],
    "yanabayashi": [
        "やなばやし"
    ],
    "yuri": [
        "ゆり"
    ],
    "reporter": [
        "レポーター"
    ]


}

sub_count = 0
bad_sub = 0
speakers = []
annotations = ""
for item in files:
    speaker = "nospeaker"
    subs = pysrt.open(os.path.join(os.path.abspath(os.curdir), DATA_DIR, item))
    sub_count = len(subs) + sub_count
    for index, sub in enumerate(subs):
        
        text = sub.text
        if text.find("(") != -1:
            # print(index+1)
            speaker = text[text.find("(")+1:text.rfind(")")]
            if speaker.find("(") != -1:
                pass
            else:
                # print(index+1)
                speakers.append(speaker)
                # result = kks.convert(speaker)
                # for item in result:
                #     print(f"{item['hepburn']}", end=" ")
        elif text.find("（") != -1:
            # print(index+1)
            speaker = text[text.find("（")+1:text.rfind("）")]
            if speaker.find("（") != -1:
                pass
            else:
                speakers.append(speaker)
                # print(index+1)
                # result = kks.convert(speaker)
                # for item in result:
                #     print(f"{item['hepburn']}", end=" ")
                # print()
            # print(text)
            # print()
        total_duration_seconds = sub.duration.hours*3600 + sub.duration.minutes*60 + sub.duration.seconds + sub.duration.milliseconds/1000
        total_start_seconds = sub.start.hours*3600 + sub.start.minutes*60 + sub.start.seconds + sub.start.milliseconds/1000
        total_end_seconds = sub.end.hours*3600 + sub.end.minutes*60 + sub.end.seconds + sub.end.milliseconds/1000
        # print(total_duration_seconds, total_start_seconds, total_end_seconds)
        annotation = f'SPEAKER {item[item.find("GATE.")+5:item.find(".JA")]} 1 {total_start_seconds} {total_end_seconds} <NA> <NA> nospeaker <NA> <NA>' + "\n"
        
        for key in speaker_variations.keys():
            if speaker in speaker_variations[key]:
                annotation = f'SPEAKER {item[item.find("GATE.")+5:item.find(".JA")]} 1 {total_start_seconds} {total_end_seconds} <NA> <NA> {key} <NA> <NA>' + "\n"
                break
        annotations = annotations + annotation
        
    # with open(os.path.join(os.path.abspath(os.curdir), DATA_DIR, item), 'r') as f:
    #     for line in f.readlines():
    #         print(line)
    with open(os.path.join(os.path.abspath(os.curdir), "annotations.txt"), 'w') as f:
        f.write(annotations)

# from collections import Counter

# speakers_counter = Counter(speakers).most_common()

# topn = 0
# for speaker in speakers_counter[:100]:
#     print(speaker)
#     topn += speaker[1]
#     result = kks.convert(speaker[0])
#     for item in result:
#         print(f"{item['hepburn']}", end=" ")
#     print()
# print(topn)
