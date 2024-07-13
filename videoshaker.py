import subprocess

# Header
print("")
print("Video Shaker. Philipp Wachowitz 2024")
print("The ChatGPT version of adding camera 'shake'.")
print("Basically shakes every pixel by the chosen factor.")
print("--------------------------------------------------")
print("")

input_file = input("Input File: ")
factor = input("factor: ")
output_file = input_file[:-4] + f"-shaked-{factor}.mp4"

# Array für den finalen ffmpeg Befehl
ffmpeg_command = [
    "ffmpeg",
    "-i",
    input_file,
    "-vf",
    f"geq='lum(X+random(1)*{int(factor)},Y+random(2)*{int(factor)})':'cb(X+random(1)*{int(factor)},Y+random(2)*{int(factor)})': 'cr(X+random(1)*{int(factor)},Y+random(2)*{int(factor)})'",
    "-c:a",
    "copy",
    output_file
]

# Jetzt muss man nur noch den eigentlichen Befehl ausführen und Zackfeddisch.
subprocess.run(ffmpeg_command)

# Wartet auf input damit sich das Fenster nicht automatisch schließt
print("Finished!")
input("Press Enter to exit.")

#ffmpeg -i input.mp4 -vf "geq='lum(X+random(1)*5,Y+random(2)*5)':'cb(X+random(1)*5,Y+random(2)*5)': 'cr(X+random(1)*5,Y+random(2)*5)'" -c:a copy output.mp4

