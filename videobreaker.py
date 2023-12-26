import subprocess

# This script takes an input video and compresses it with the worst quality setting available.
# It then takes that output and compresses it again and again. As often as it is specified in n_repeats

print("This Script compresses your video over and over again with the worst quality setting possible")
input_file = input("Input File: ")
n_repeats = input("Number of iterations: ")

# For this to work the first iteration has to be done by a separate function that runs only once at the beginning
def generateFirstOutput():
    commands_list = [
        "ffmpeg",
        "-i",
        input_file,
        "-crf",
        "63",
        input_file+"-out-0.mp4"
    ]
    return commands_list

# this function creates a ffmpeg prompt in which the input file is replaced with the previously generated output file. this is loopable
def generateNextOutput(count):
    commands_list = [
        "ffmpeg",
        "-i",
        input_file+"-out-"+str(count)+".mp4",
        "-crf",
        "63",
        input_file+"-out-"+str(count+1)+".mp4"
    ]
    return commands_list

# Main loop. Run the first Call once to generate the filename pattern that is loopable and then run the for loop for the number of iterations
subprocess.run(generateFirstOutput())
for i in range(int(n_repeats)-1):
    subprocess.run(generateNextOutput(i))

input("Finished. Have fun with your broken videos! Press Enter to Exit.")
