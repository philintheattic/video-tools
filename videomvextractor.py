import subprocess

print("")
print("Motion Vector Visualizer. Philipp Wachowitz 2024")
print("Renders a video that shows only the motion vectors")
print("--------------------------------------------------")
print("")

input_file = input("Input File: ")
output_file = input_file[:-4] + "-MVextracted.mp4"

ffmpeg_command = [
  "ffmpeg",
  "-flags2",
  "+export_mvs",
  "-i",
  input_file,
  "-vf",
  "split[src],codecview=mv=pf+bf+bb[vex],[vex][src]blend=all_mode=difference128,eq=contrast=7:brightness=-1:gamma=1.5",
  "-c:v",
  "libx264",
  output_file
]

subprocess.run(ffmpeg_command) 

print("Finished!")
input("Press Enter to exit.")

# ffmpeg -flags2 +export_mvs -i vid_in.mp4 -vf "split[src],codecview=mv=pf+bf+bb[vex],[vex][src]blend=all_mode=difference128,eq=contrast=7:brightness=-1:gamma=1.5" -c:v libx264 vid_out.mp4
