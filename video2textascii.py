# -*- coding: UTF-8 -*-

##### STEP 1 ##### user inputs a video file
##### STEP 2 ##### ffmpeg extracts individual frames to a temp folder
##### STEP 3 ##### python script iterates over these images and turns them into asci art
##### STEP 4 ##### ffmpeg concatenates all the images back to a video
#TODO check for framerate and update the ffmpeg command accordingly. For now it only works with 25fps.

from PIL import Image, ImageDraw, ImageFont
import subprocess
import os
import shutil
import math

# Header
print("")
print("Video 2 Text-ASCII. Philipp Wachowitz 2024")
print("Takes a video and turns it into ASCII Art based on an input text file")
print("---------------------------------------------------------------------")
print("")

# Function for the progressbar
def progress_bar(progress, total):
    percent = 100 * (progress/ float(total))
    bar = "█" * int(percent) + "-" * (100 - int(percent))
    print(f"\r|{bar}| Frame: {progress}/{total}", end="\r")


##### STEP 1 - User inputs a video file #####

# Get user input
input_file = input("Input File: ")
output_file = input("Output File: ")
LOD_input = input("Level of Detail (lower value = more details, default is 1): ")

# If input is left empty, default to 1
if LOD_input == "":
     LOD_input = 1

# Make sure LOD is an integer
LOD = math.floor(int(LOD_input))

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


# Read the ASCII Characters from external file. This makes changing it easy for the user
with open("assets/fulltext.txt") as f:
    fulltext = f.read()
    f.close()

# Turn the ASCII string into an array of characters


scaleFactor = 0.1        # Can be changed depending on the input size. Mess around at your own risk.


print("Turning frames into ASCII Art...")

# Get infos for the progressbar
file_count_total = 0
file_count_value = 0
for files in os.listdir(input_directory):
     file_count_total += 1
progress_bar(0,file_count_total)

# Loop through all files in the input folder, turn them into ASCII Art and save them in the output folder
for files in os.listdir(input_directory):
    # Open image file
    image_file = f"in/{files}"
    image = Image.open(image_file)

    # Set character width and height
    oneCharWidth = int(10 * LOD)
    oneCharHeight = int(10 * LOD)

    # Set font
    font = ImageFont.truetype("assets/Cour.ttf", int(10 * LOD))

    # Resize Image to make processing faster
    width, height = image.size
    image = image.resize((int(scaleFactor*width), int(scaleFactor*height*(oneCharWidth/oneCharHeight))), Image.NEAREST)
    width, height = image.size
    pixels = image.load()

    # Create a new output image and prepare it for drawing
    outputImage = Image.new("RGB", (int(oneCharWidth * width / LOD),int(oneCharHeight * height / LOD)), color = (0, 0, 0))
    d = ImageDraw.Draw(outputImage)

    # init count value for advacing in the string array
    count = 0

    # Check every pixel for color value, turn that into a brightness value and assign this brightness value to the character that is being drawn from the fulltext array
    for i in range(0, height, LOD):
        for j in range(0, width, LOD):
            r, g, b = pixels[j, i]
            brightness = int((r + g + b)/3)
            pixels[j, i] = brightness
            d.text((j * oneCharWidth / LOD, i * oneCharHeight / LOD), fulltext[count], font = font, fill = (brightness, brightness, brightness))
            if (count < (len(fulltext)-1)):
                count += 1
            else:
                count = 0

    # Save to file
    outputImage.save(f"out/{files}")

    # Move the progress bar forward
    progress_bar(file_count_value+1,file_count_total)
    file_count_value += 1


##### STEP 4 - Reassemble the new frames into a video file #####


print("")
print("Making Movie...")

def makeMovie():
     cmd = f"ffmpeg -i out/%01d.png {output_file}"
     return cmd

subprocess.run(makeMovie())

print("Finished compiling movie!")

# Ask the user to remove all temp files
delete_prompt = input("Delete all temp files? [y/n] ")
if (delete_prompt == "y"):
    shutil.rmtree(input_directory)
    shutil.rmtree(output_directory)
    input("Files deleted! You are all set! Press enter to exit and enjoy your video...")
else:
    input("Finished! Press enter to exit and enjoy your video...")    
