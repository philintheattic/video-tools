import subprocess
import cv2
import os

# Header
print("")
print("Slitscan Video Generator. Philipp Wachowitz 2023")
print("Takes an input video and applies a slitscan effect")
print("Play with the strip width value to get different results (default is 2)")
print("-----------------------------------------------------------------------")
print("")

input_file = input("Input File: ")
video_width = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_HEIGHT))
video_fps = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FPS))
strip_width = input("Strip Width: ")
output_file = input_file + "-slitscan.mp4"
offset = 1/video_fps

# default ist 2 wenn kein Wert eingegeben wird
if strip_width == "":
    strip_width = 2

count = int(video_height/int(strip_width))

# Helferfunktion um easy strings aus arrays zu machen. Verbessert Lesbarkeit im Code
def makeString(array):
    name = "".join(array)
    return name

# Schreibt den Part für den Split Filter
def getSplits():
    splits_cmd = f"[0]split={int(count)}"
    for i in range(count):
        splits_cmd += f"[v{i}]"
    return splits_cmd

# Schreibt den Part für den tpad Filter
def getOffset():
    offset_cmd = ""
    for i in range(count):
        offset_cmd += f";[v{i}]tpad=start_mode=clone:start_duration={offset*i},crop={video_width}:{int(strip_width)}:0:{i*int(strip_width)}[v{i}]"
    return offset_cmd

# Schreibt den Part für den vstack Filter
def getStacks():
    stack_cmd = ";"
    for i in range(count):
        stack_cmd += f"[v{i}]"
    stack_cmd += f"vstack=inputs={int(count)}"
    return stack_cmd

# Array um daraus dann den langen String für den -filter_complex zu erstellen
filter_command = [
    getSplits(),
    getOffset(),
    getStacks()
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
    output_file
]

# Jetzt muss man nur noch den eigentlichen Befehl ausführen und Zackfeddisch.
subprocess.run(ffmpeg_command)

# Löscht die temporäre cmd Datei
if os.path.exists("cmd.txt"):
  os.remove("cmd.txt")
else:
  print("Could not find command file.")

# Wartet auf input damit sich das Fenster nicht automatisch schließt
print("Finished!")
input("Press Enter to exit.")