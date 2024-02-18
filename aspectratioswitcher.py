# ffmpeg -i moin.mp4 -vf scale=ih:iw,setsar=1 moin_scaled.mp4

import subprocess

input_file = input("Input File: ")
output_file = input_file[:-4] + "_switched.mp4"

ffmpeg_command = [
    "ffmpeg",
    "-i",
    input_file,
    "-vf",
    "scale=ih:iw,setsar=1",
    output_file
]

subprocess.call(ffmpeg_command)