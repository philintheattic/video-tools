import cv2

print("")
print("Background Subtraction. Philipp Wachowitz 2024")
print("Uses OpenCV background subtraction and generates a black and white matte")
print("------------------------------------------------------------------------")
print("")

# Function for the progressbar
def progress_bar(progress, total):
    percent = 100 * (progress/ float(total))
    bar = "█" * int(percent) + "-" * (100 - int(percent))
    print(f"\r|{bar}| Frame: {progress}/{total}", end="\r")

# Variable for the input file
input_file = input("Input File: ")

# Initialize the background subtractor
backSub = cv2.createBackgroundSubtractorKNN(500, 512, detectShadows=False)

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

# Formatting for the name of the output file
output_file = input_file[:-4] + "_bg-subtracted.mp4"

# Prepare the output and the codec, use same fps and size as original video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_file, fourcc, video_fps, (video_width,video_height), isColor=False)

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

while True:
    ret, frame = cap.read()
    if frame is None:
        break

    mask = backSub.apply(frame, learningRate=0)

    cv2.imshow("Preview", mask)
    out.write(mask)

    # Pressing Enter breaks out of the loop
    if cv2.waitKey(1) == 13:
        break

    # Update the progress bar
    progress += 1
    progress_bar(progress, videoframes)

# Housekeeping
cap.release()
out.release()
cv2.destroyAllWindows()

print("")
print("Finished!")

