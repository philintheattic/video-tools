#TODO ##### STEP 1 ##### user inputs a video file
#TODO ##### STEP 2 ##### ffmpeg extracts individual frames to a temp folder
#TODO ##### STEP 3 ##### python script iterates over these images and turns them into asci art
#TODO ##### STEP 4 ##### ffmpeg concatenates all the images back to a video

from PIL import Image, ImageDraw, ImageFont
import subprocess
import os
import shutil
import math

# Header
print("")
print("Video 2 ASCII. Philipp Wachowitz 2023")
print("Takes a video and turns it into ASCII Art")
print("-----------------------------------------")
print("")

# Funktion für Fortschrittsbalken
def progress_bar(progress, total):
    percent = 100 * (progress/ float(total))
    bar = "█" * int(percent) + "-" * (100 - int(percent))
    print(f"\r|{bar}| Frame: {progress}/{total}", end="\r")


##### STEP 1 - User inputs a video file #####


input_file = input("Input File: ")
output_file = input("Output File: ")

# Creating temp directories
input_directory = "in"
if os.path.isdir(input_directory) == False: 
	os.mkdir(input_directory)
     
output_directory = "out"
if os.path.isdir(output_directory) == False: 
	os.mkdir(output_directory)


##### STEP 2 - Extract individial frames with FFmpeg #####

print("Extracting frames...")

def makeFrames():
     cmd = f"ffmpeg -i {input_file} in/%01d.png"
     return cmd
    
subprocess.run(makeFrames())


##### STEP 3 - The main act #####


# Read the ASCII Characters from external file. This makes changing it easy for the enduser
with open("assets/chars.txt") as f:
    chars = f.read()
    f.close()

charArray = list(chars)
# Uncomment to reverse "colors"
# charArray.reverse()
charLength = len(charArray)
mapping = charLength/256
scaleFactor = 0.1        # can be changed depending on the input size. take care of later

def getChar(input_pixel):
    return charArray[math.floor(input_pixel*mapping)]

print("Turning frames into ASCII Art...")

# Get infos for the progressbar
file_count = 0
file_count_2 = 0
for files in os.listdir(input_directory):
     file_count += 1
progress_bar(0,file_count)


# Loop through all files in the input folder, turn them into ASCII Art and save them in the output folder
for files in os.listdir(input_directory):
    image_file = f"in/{files}"
    image = Image.open(image_file)

    oneCharWidth = 10
    oneCharHeight = 10

    font = ImageFont.truetype("assets/Cour.ttf", 10)

    # Resize Image to make processing faster
    width, height = image.size
    image = image.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
    width, height = image.size
    pixels = image.load()

    # Create a new output image and prepare it for drawing
    outputImage = Image.new("RGB", (int(oneCharWidth * width),int(oneCharHeight * height)), color = (0, 0, 0))
    d = ImageDraw.Draw(outputImage)

    # check every pixel for color value, turn that into a brightness value and assign a char from the character array to it based on the brightness
    for i in range(height):
        for j in range(width):
            r, g, b = pixels[j, i]
            brightness = int((r + g + b)/3)
            pixels[j, i] = brightness
            d.text((j * oneCharWidth, i * oneCharHeight), getChar(brightness), font = font, fill = (255, 255, 255))

    # save to file
    outputImage.save(f"out/{files}")

    # Move the progress bar forward
    progress_bar(file_count_2+1,file_count)
    file_count_2 += 1

##### STEP 4 - Reassemble the new frames into a video file #####

print("")
print("Making Movie...")

def makeMovie():
     cmd = f"ffmpeg -i out/%01d.png {output_file}"
     return cmd

subprocess.run(makeMovie())

print("Finished compiling movie!")

# ask the user to remove all temp files
delete_prompt = input("Delete all temp files? [y/n] ")
if (delete_prompt == "y"):
    shutil.rmtree(input_directory)
    shutil.rmtree(output_directory)
    input("Files deleted! You are all set! Press enter to exit and enjoy your ASCII video...")
else:
    print("Finished! Press enter to exit and enjoy your ASCII video...")    