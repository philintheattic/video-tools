#TODO tidy up this messy formatted code lol

from PIL import Image
import numpy as np
import random
import os
import subprocess
import shutil

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

def makeFrames():
     cmd = f"ffmpeg -i {input_file} in/%01d.png"
     return cmd
    
subprocess.run(makeFrames())

# Get infos for the progressbar
file_count = 0
file_count_2 = 0
for files in os.listdir(input_directory):
     file_count += 1
progress_bar(0,file_count)

# Loop through each frame in that folder and shuffle the pixel arrays
# save a new image from the shuffled pixelarray
# combine all the new images back into a movie



# Öffnet Bild und gibt ein geshuffeltes pixelarray zurück
def shuffle_pixels(image):
    image = Image.open(f"in/{image}")
    array = np.array(image, dtype=np.uint8)
    random.shuffle(array)
    return array

# wandelt das numpy array in ein bild um und speichert es ab
def save_shuffled_image(image):
    new_image = Image.fromarray(shuffle_pixels(image))
    new_image.save(f"out/{image}")

# MAIN LOOP
for files in os.listdir(input_directory):

    save_shuffled_image(files)
   
    progress_bar(file_count_2+1,file_count)
    file_count_2 += 1


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
