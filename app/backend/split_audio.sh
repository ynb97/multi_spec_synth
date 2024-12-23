rm ./split_files/*.mp3
sox $1 ${2:-./split_files/s.mp3} silence 1 0.2 0.6% 1 0.2 0.6% : newfile : restart
