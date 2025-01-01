# TODO: Add functionalty to change FPS

import subprocess

print("")
print("Noise Overlay Generator. Philipp Wachowitz 2025")
print("Renders a gray video with noise so you can use that")
print("as an overlay in your favorite NLE.")
print("---------------------------------------------------")
print("")

duration = input("Duration (in seconds): ")
size = input("Video Resolution (must be in format widthxheight): ")
noise = input("Amount of Noise: ")
output_file = input("Name your output file: ")

ffmpeg_command = [
  "ffmpeg",
  "-t",
  duration,
  "-f",
  "lavfi",
  "-i",
  f"color=c=gray:s={size}",
  "-c:v",
  "libx265",
  "-vf",
  f"noise=c0s={int(noise)}:c0f=t+u",
  output_file
]

subprocess.run(ffmpeg_command) 

print("Finished!")
input("Press Enter to exit.")


# ffmpeg -i test.mp4 -vf noise=c0s=60:c0f=t+u noise.mp4

# ffmpeg -t 5 -f lavfi -i color=c=gray:s=1280x720 -c:v libx265 gray.mp4

# this one works! it generates noise on a middle grey bg.
# ffmpeg -t 5 -f lavfi -i color=c=gray:s=1280x720 -c:v libx265 -vf "noise=c0s=60:c0f=t+u" noise_overlay.mp4