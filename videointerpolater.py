import subprocess

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
