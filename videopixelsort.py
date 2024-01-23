import numpy as np
from typing import Callable
from PIL import Image
import subprocess
import os
import shutil

# Header
print("")
print("Video Pixel Sort. Philipp Wachowitz 2024")
print("Takes a video and sorts Pixel frame by frame")
print("Original sorting script by u/GregTJ")
print("--------------------------------------------")
print("")

##### STEP 1 #####

input_file = input("Input File: ")
output_file = input("Output File: ")
# Funktion für Fortschrittsbalken
def progress_bar(progress, total):
    percent = 100 * (progress/ float(total))
    bar = "█" * int(percent) + "-" * (100 - int(percent))
    print(f"\r|{bar}| Frame: {progress}/{total}", end="\r")

# Creating temp directories
input_directory = "in"
if os.path.isdir(input_directory) == False: 
	os.mkdir(input_directory)
     
output_directory = "out"
if os.path.isdir(output_directory) == False: 
	os.mkdir(output_directory)

#TODO ##### STEP 1 ##### user inputs a video file
#TODO ##### STEP 2 ##### ffmpeg extracts individual frames to a temp folder
#TODO ##### STEP 3 ##### python script iterates over these images and turns them into asci art
#TODO ##### STEP 4 ##### ffmpeg concatenates all the images back to a video

##### STEP 2 #####

def makeFrames():
     cmd = f"ffmpeg -i {input_file} in/%01d.png"
     return cmd
    
subprocess.run(makeFrames())

# PIXEL SORT FUNCTION - found on r/pixelsorting - Thx to u/GregTJ
def sort_pixels(image: Image, value: Callable, condition: Callable, rotation: int = 0) -> Image:
    pixels = np.rot90(np.array(image), rotation)
    values = value(pixels)
    edges = np.apply_along_axis(lambda row: np.convolve(row, [-1, 1], 'same'), 0, condition(values))
    intervals = [np.flatnonzero(row) for row in edges]

    for row, key in enumerate(values):
        order = np.split(key, intervals[row])
        for index, interval in enumerate(order[1:]):
            order[index + 1] = np.argsort(interval) + intervals[row][index]
        order[0] = range(order[0].size)
        order = np.concatenate(order)

        for channel in range(3):
            pixels[row, :, channel] = pixels[row, order.astype('uint32'), channel]

    return Image.fromarray(np.rot90(pixels, -rotation))

# Get infos for the progressbar
file_count = 0
file_count_2 = 0
for files in os.listdir(input_directory):
     file_count += 1
progress_bar(0,file_count)


# MAIN LOOP
for files in os.listdir(input_directory):

    # credits for this block also belong to u/GregTJ
    sort_pixels(Image.open(f"in/{files}"),
                lambda pixels: np.average(pixels, axis=2) / 255,
                lambda lum: (lum > 2 / 6) & (lum < 4 / 6), 1).save(f"out/{files}")
    
    progress_bar(file_count_2+1,file_count)
    file_count_2 += 1

##### STEP 4 #####

def makeMovie():
     cmd = f"ffmpeg -i out/%01d.png {output_file}"
     return cmd

subprocess.run(makeMovie())


# ask the user to remove all temp files
delete_prompt = input("delete all temp files? [y/n] ")
if (delete_prompt == "y"):
    shutil.rmtree(input_directory)
    shutil.rmtree(output_directory)
    print("finished and files deleted")
else:
    print("finished!") 