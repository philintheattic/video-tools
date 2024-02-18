# Wrap this ffmpeg command into a python script.
# input a video, run the command and output a new video
# Takes long to render
# ‍ffmpeg -i song_viz.mp4 -filter_complex "format=rgba,geq='p(mod((2*W/(2*PI))*(PI+atan2(0.5*H-Y,X-W/2)),W), H-2*hypot(0.5*H-Y,X-W/2))'" -pix_fmt yuv420p song_viz_circle.mp4

import subprocess

input_file = input("Input Video: ")
output_file = input_file[:-4] + "_circulated.mp4"

ffmpeg_command = [
    "ffmpeg",
    "-i",
    input_file,
    "-filter_complex",
    "format=rgba,geq='p(mod((2*W/(2*PI))*(PI+atan2(0.5*H-Y,X-W/2)),W), H-2*hypot(0.5*H-Y,X-W/2))'",
    output_file
]

subprocess.call(ffmpeg_command)

