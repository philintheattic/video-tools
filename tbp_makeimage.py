import subprocess
import numpy
from PIL import Image
import cv2

# Funktion für Fortschrittsbalken
def progress_bar(progress, total):
    percent = 100 * (progress/ float(total))
    bar = "█" * int(percent) + "-" * (100 - int(percent))
    print(f"\r|{bar}| Frame: {progress}/{total}", end="\r")

# Header
print("")
print("Time-based photography. Creates an image based on all frames of a video.")
print("Original script written by Hannes Bajohr. https://github.com/hbajohr")
print("Modified to output just one image.")
print("------------------------------------------------------------------------")
print("")

# Variablen
input_file = input("Input file: ")
start_frame = 1
video_height = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_HEIGHT))
video_width = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_WIDTH))
frame_count = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_COUNT))
image_width = int(frame_count)
output_file = input_file + "-out.jpg"

output_image = Image.new("RGB", (image_width,video_height))

print("")
print("Processing...")

# Habe noch nicht genau gecheckt was hier eigentlich passiert.
command = [ 'ffmpeg',
			'-i', input_file, 
			'-f', 'image2pipe',
			'-pix_fmt', 'rgb24',
			'-vcodec', 'rawvideo','-', '-nostats', '-hide_banner', '-loglevel', '0']
pipe = subprocess.Popen(command, stdout = subprocess.PIPE, bufsize=10**8)
#pipe.stdout.flush()

# Fortschrittsbalken initialisieren
progress_bar(0,image_width)

# Jeder Loop ist ein "slice" und wird am Ende zu einem neuen Bild zusammengefügt
for i in range(0,image_width):
    raw_image = pipe.stdout.read(video_height*video_width*3)
    image = numpy.frombuffer(raw_image, dtype="uint8")
    image = image.reshape((video_height,video_width,3))
    im = Image.fromarray(image)
    w,h = im.size
    im = im.crop((start_frame, 0, w-(w-1)+start_frame, h))
    output_image.paste(im,(i*1,0))
    progress_bar(i+1,image_width)

# Speichert das fertige Bild
output_image.save(output_file)

# Wartet auf Input damit sich das Fenster nicht einfach direkt schließt
print("\n\n")
input("Finished! Press enter to exit.")
