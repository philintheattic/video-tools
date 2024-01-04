# Framecount auslesen
# frames auf einen prozentsatz reduzieren
# diese restlichen frames random mischen und neu zusammensetzen
# video interpolieren

import subprocess
import cv2
import os

# Header
print("")
print("Video Eraserpolater™. Philipp Wachowitz 2023")
print("Erases frames based on the framerate and then re-interpolates the video")
print("back to it's original length creating abstract shapes and forms.")
print("-----------------------------------------------------------------------")
print("")

input_file = input("Input File: ")
video_width = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_HEIGHT))
video_fps = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FPS))
output_file = input_file + "-eraserpolated.mp4"
reduction_factor = video_fps

# set to true if you need to keep the cmd.txt for debugging
keep_cmd_file = False

# Helferfunktion um easy strings aus arrays zu machen. Verbessert Lesbarkeit im Code
def makeString(array):
    name = "".join(array)
    return name

# Funktion für den FFmpeg Befehl
def getCommand():
    command = f"select=not(mod(n\,{reduction_factor})),setpts=N/{reduction_factor}/TB[short];[short]setpts={reduction_factor}*PTS,minterpolate=fps={reduction_factor}:scd=none:me_mode=bilat:vsbmc=1:search_param=400"
    return command

# Array um daraus dann den langen String für den -filter_complex zu erstellen
filter_command = [
    getCommand(),
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
    "-an", # gets rid of the audio channel. delete if you want to keep audio
    output_file
]

# Jetzt muss man nur noch den eigentlichen Befehl ausführen und Zackfeddisch.
subprocess.run(ffmpeg_command)

# Löscht die temporäre cmd Datei
if os.path.exists("cmd.txt") and not keep_cmd_file:
    os.remove("cmd.txt")
else:
    print("Couldn't delete cmd.txt file. It was either removed or you wanted to keep it.")

# Wartet auf input damit sich das Fenster nicht automatisch schließt
print("Finished!")
input("Press Enter to exit.")

# reduziert video auf bestimmte frameanzahl. über modulo funktion.
# ffmpeg -i clip.MOV -vf select="not(mod(n\,25)),setpts=N/25/TB" -an select-filter-6.mp4

# ffmpeg -i {input_file} -filter_complex "select=not(mod(n\,{reduction_factor})),setpts=N/25/TB[short];[short]setpts={reduction_factor}*PTS,minterpolate=fps=25:scd=none:me_mode=bidir:vsbmc=1:search_param=400" -an out.mp4

# Getest und funktioniert!
# ffmpeg -i clip.MOV -filter_complex select=not(mod(n\,25)),setpts=N/25/TB[short];[short]setpts=25*PTS,minterpolate=fps=25:scd=none:me_mode=bidir:vsbmc=1:search_param=400 -an randomizer-test-out.mp4