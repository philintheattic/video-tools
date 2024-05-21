from PIL import Image
import numpy as np
import random
import os
import subprocess
import shutil

# Header
print("")
print("Shuffle Pixel Rows. Philipp Wachowitz 2024")
print("Shuffles the rows/lines of a video by shuffling the first dimension of the pixel array")
print("--------------------------------------------------------------------------------------")
print("")

# Function for the progressbar
def progress_bar(progress, total):
    percent = 100 * (progress/ float(total))
    bar = "█" * int(percent) + "-" * (100 - int(percent))
    print(f"\r|{bar}| Frame: {progress}/{total}", end="\r")


##### STEP 1 - User inputs a video file #####

# Get user input and specifiy an output filename
input_file = input("Input File: ")
output_file = input("Output File: ")

# Creating temp directories
input_directory = "in"
if os.path.isdir(input_directory) == False: 
	os.mkdir(input_directory)
     
output_directory = "out"
if os.path.isdir(output_directory) == False: 
	os.mkdir(output_directory)

##### STEP 2 - Extract individual frames with FFmpeg #####

print("Extracting frames...")

def makeFrames():
     cmd = f"ffmpeg -i {input_file} in/%01d.png"
     return cmd
    
subprocess.run(makeFrames())

##### STEP 3 - The main act #####

# Get infos for the progressbar
file_count = 0
file_count_2 = 0
for files in os.listdir(input_directory):
     file_count += 1
progress_bar(0,file_count)

# Opens an image, turns pixel values into numpy array, shuffles said array and then returns it
def shuffle_pixels(image):
    image = Image.open(f"in/{image}")
    array = np.array(image, dtype=np.uint8)
    random.shuffle(array)
    return array

# saves the shuffled array back into an image
def save_shuffled_image(image):
    new_image = Image.fromarray(shuffle_pixels(image))
    new_image.save(f"out/{image}")

print("Shuffling pixel rows...")
print("")

# MAIN LOOP
# Iterates over every frame in the input directory
for files in os.listdir(input_directory):

    save_shuffled_image(files)

    # Move progress bar forward
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

# Ask the user to remove all temp files
delete_prompt = input("delete all temp files? [y/n] ")
if (delete_prompt == "y"):
    shutil.rmtree(input_directory)
    shutil.rmtree(output_directory)
    print("finished and files deleted")
else:
    print("finished!") 
