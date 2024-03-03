import cv2

print("")
print("Video Tripper. Philipp Wachowitz 2024")
print("Multiplies Values in the pixel array. I don't really know what's")
print("exactly happening here but the results look cool, so...")
print("----------------------------------------------------------------")
print("")

# Function for the progressbar
def progress_bar(progress, total):
    percent = 100 * (progress/ float(total))
    bar = "█" * int(percent) + "-" * (100 - int(percent))
    print(f"\r|{bar}| Frame: {progress}/{total}", end="\r")

# Variable for the input file
input_file = input("Input File: ")

# Open the input file with opencv and get some metadata
cap = cv2.VideoCapture(input_file)
videoframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
video_fps = int(cap.get(cv2.CAP_PROP_FPS))
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Display some info about the video file
print("")
print("Videofile found! Here are some infos:")
print(f"Video dimensions:\t {video_width}x{video_height}")
print(f"Video framerate:\t {video_fps}")
print(f"Total number of frames:\t {videoframes}")
print("")

# The higher the number the more "noise"-like the image will be
factor = input("Multiplication factor: ")

# Formatting for the name of the output file
output_file = input_file[:-4] + f"_tripped_{factor}.mp4"

# Prepare the output and the codec, use same fps and size as original video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_file, fourcc, video_fps, (video_width,video_height))

# Set up preview window
cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Preview", int(video_width/4), int(video_height/4))
cv2.setWindowProperty("Preview", cv2.WND_PROP_TOPMOST, 1)

print("")
print("Opening preview window...")
print("Rendering Video...")
print("Press Enter to cancel...")

# Initialize progress bar
progress = 0
progress_bar(progress, videoframes)

# Main loop
while True:
    ret, frame = cap.read()

    # If there is a frame, do something
    if ret:
        # Where the magic happens. Multiplies the pixel values resulting in crazy colors 
        draw = frame * int(factor)

        # Show a preview window to see the effect in action
        cv2.imshow("Preview", draw)

        # Saving to file
        out.write(draw)

        # Pressing Enter breaks out of the loop
        if cv2.waitKey(1) == 13:
            break
        
        # Update the progress bar
        progress += 1
        progress_bar(progress, videoframes)

    # If there is no more frame i.e. the video is finished, break out of the loop
    else:
        break

# Housekeeping
cap.release()
out.release()
cv2.destroyAllWindows()

print("")
print("Finished!")