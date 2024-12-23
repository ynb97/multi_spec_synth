import pykakasi

kks = pykakasi.kakasi()

with open("input.txt", 'r') as f:
    for line in f.readlines():
        print(line)
        result = kks.convert(line)
        print(result)
        for item in result:
            print(f"{item['hepburn']}", end=" ")