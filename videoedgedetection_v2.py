import cv2

print("")
print("Canny Edge Detection. Philipp Wachowitz 2024")
print("OpenCV-based canny edge detection")
print("--------------------------------------------")
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

# Formatting for the name of the output file
output_file = input_file[:-4] + "_cannyedges.mp4"

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

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        canny = cv2.Canny(blur, 10, 70)
        ret, mask = cv2.threshold(canny, 70,255, cv2.THRESH_BINARY)
        out.write(mask)
        cv2.imshow('Preview', mask)
        if cv2.waitKey(1) == 13:
            break

        # Update the progress bar
        progress += 1
        progress_bar(progress, videoframes)

    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("")
print("Finished!")