import subprocess

# Header
print("")
print("Video Interpolater. Philipp Wachowitz 2023")
print("Takes an input video and stretches it in time with optical flow applied")
print("WARNING: Very slow. Use only on short clips. High stretch values produce nice glitches")
print("--------------------------------------------------------------------------------------")
print("")

input_file = input("Input File: ")
stretch_factor = input("Stretch factor: ")
output_file = input_file + "-minterpolate.mp4"

# Array für den finalen ffmpeg Befehl
ffmpeg_command = [
    "ffmpeg",
    "-i",
    input_file,
    "-filter:v",
    f"setpts={int(stretch_factor)}*PTS,minterpolate='fps=25:scd=none:me_mode=bidir:vsbmc=1:search_param=400'",
    output_file
]

# Jetzt muss man nur noch den eigentlichen Befehl ausführen und Zackfeddisch.
subprocess.run(ffmpeg_command)

# Wartet auf input damit sich das Fenster nicht automatisch schließt
print("Finished!")
input("Press Enter to exit.")
