import subprocess
import cv2
import os

# Header
print("")
print("Video Tunnel Generator. Philipp Wachowitz 2023")
print("Takes an input video, scales it down and overlays it on itself repeatedly")
print("Overlays can rotate over time if value is set between 0 and 1. 0.01 works")
print("-------------------------------------------------------------------------")
print("")

# Variablen
input_file = input("Input File: ")
video_width = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_HEIGHT))
n_copies = input("Number of copies: ")
scale_factor = 1 / int(n_copies)
rotation_factor = input("Rotation value (Float between 0 and 1. 0 = no rotation):")

# if left empty defaults to 0, no rotation
if rotation_factor == "":
    rotation_factor = 0

output_file = input_file + "-tunnel.mp4"
overlay_x = int(int(video_width/int(n_copies))/2)
overlay_y = int(int(video_height/int(n_copies))/2)

# set to true if you need to keep the cmd.txt for debugging
keep_cmd_file = False

# Helferfunktion um easy strings aus arrays zu machen. Verbessert Lesbarkeit im Code
def makeString(array):
    name = "".join(array)
    return name

# Schreibt den Part für den split Filter
def getSplits():
    splits_cmd = f"[0]split={int(n_copies)}"
    for i in range(int(n_copies)):
        splits_cmd += f"[v{i}]"
    return splits_cmd

# Schreibt den Part für den scale Filter
def getScales():
    scales_cmd = ";"
    for i in range(1, int(n_copies)):
        scales_cmd += f"[v{i}]scale=iw*{scale_factor*(int(n_copies)-i)}:ih*{scale_factor*(int(n_copies)-i)}+1,rotate={i*float(rotation_factor)}*PI*t:fillcolor=none[v{i}];"
    return scales_cmd

# Schreibt den Part für den overlay Filter
def getOverlays():
    overlays_cmd = ""
    for i in range(1,int(n_copies)):
        if i != (int(n_copies)-1):
            overlays_cmd += f"[v{i-1}][v{i}]overlay={i*int(overlay_x)}:{i*int(overlay_y)}[v{i}];"
        else:
            overlays_cmd += f"[v{i-1}][v{i}]overlay={i*int(overlay_x)}:{i*int(overlay_y)}"
    return overlays_cmd

# Array um daraus dann den langen String für den -filter_complex zu erstellen
filter_command = [
    getSplits(),
    getScales(),
    getOverlays()
]

# Weil der Befehl bei bestimmten Werten sehr lang werden kann wird er in eine Textdatei outgesourced und ffmpeg liest dann den Filtergraph aus der Datei
with open("cmd.txt", "w") as file:
    file.write(makeString(filter_command))

# Array für den finalen ffmpeg Befehl
ffmpeg_command = [
    "ffmpeg",
    "-i",
    input_file,
    "-filter_complex_script",
    "cmd.txt",
    "-map",
    "v",
    output_file
]

# Jetzt muss man nur noch den eigentlichen Befehl ausführen und Zackfeddisch.
subprocess.run(ffmpeg_command)

# Löscht die temporäre cmd Datei
if os.path.exists("cmd.txt") and not keep_cmd_file :
  os.remove("cmd.txt")
else:
    print("Couldn't delete cmd.txt file. It was either removed or you wanted to keep it.")

# Wartet auf input damit sich das Fenster nicht automatisch schließt
print("Finished!")
input("Press Enter to exit.")

# Leftovers
# ffmpeg -i clip.mp4 -filter_complex "[0]split=4[v1][v2][v3][v4];
# [v1]hue=12*t[v1];
# [v2]hue=24*t,scale=iw*0.75:ih*0.75[v2];
# [v3]hue=48*t,scale=iw*0.5:ih*0.5[v3];
# [v4]hue=96*t,scale=iw*0.25:ih*0.25[v4];
# [v1][v2]overlay=main_w*0.125:main_h*0.125[v2];
# [v2][v3]overlay=main_w*0.25:main_h*0.25[v3];
# [v3][v4]overlay=main_w*0.375:main_h*0.375"
# out.mp4

# ffmpeg -i clip.mp4 -filter_complex "[0]split=5[v1][v2][v3][v4][v5];[v1]hue=12*t[v1];[v2]hue=24*t,scale=iw*0.8:ih*0.8[v2];[v3]hue=48*t,scale=iw*0.6:ih*0.6[v3];[v4]hue=96*t,scale=iw*0.4:ih*0.4[v4];[v5]hue=192*t,scale=iw*0.2:ih*0.2[v5];[v1][v2]overlay=384:216[v2];[v2][v3]overlay=768:432[v3];[v3][v4]overlay=1152:648[v4];[v4][v5]overlay=1536:864" out.mp4

# ffmpeg -i clip.mp4 -filter_complex "[0]split=5[v1][v2][v3][v4][v5];[v1]hue=12*t[v1];[v2]hue=24*t,scale=iw*0.75:ih*0.75[v2];[v3]hue=48*t,scale=iw*0.5:ih*0.5[v3];[v4]hue=96*t,scale=iw*0.25:ih*0.25[v4];[v5]scale=iw[v5];[v1][v2]overlay=main_w*0.125:main_h*0.125[v2];[v2][v3]overlay=main_w*0.25:main_h*0.25[v3];[v3][v4]overlay=main_w*0.375:main_h*0.375" out.mp4