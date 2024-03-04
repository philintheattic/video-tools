# video-tools
## Installation
### For Windows
If you don't want to bother with python and all that code you can download the windows executables from the [latest release](https://github.com/philintheattic/video-tools/releases)

### Python
Copy the script you want to use into the folder that contains the videofile that you want to process. Run the script and follow the prompts. For the script to work you need an installation of ffmpeg that is added to PATH. Depending on the script you may also need:
+ opencv
```
pip install opencv-python
```
+ Pillow
```
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
```
+ NumPy
```
pip install numpy
```
## Description
I was looking for ways to manipulate videofiles with code to use the output in an artistic way. These tools are a way of learning (to code) and automating processes that would be very time consuming if done in software like After Effects or Fusion. The project is basically just tailored around my needs although I try to keep it as reusable and user-friendly as possible. 
## The tools
### videobreaker
This script takes an input video and compresses it via ffmpeg with a quality setting of `-crf 67` which is the worst possible setting in ffmpeg. This generates a highly compressed videofile with lots of compression artifacts. This compressed videofile is then used as a new input file and will be further compressed and so on. The file will get more and more "destroyed" in the process creating lots of interesting (and sometimes creepy) visuals. You can specify the number of iterations.

Example images of the input file, after the first compression, the 10th and the 50th:

<img width="200" alt="input file" src="https://github.com/philintheattic/video-tools/assets/154841043/d3dbab2c-37a6-4e1d-a87a-d1b43523e465">
<img width="200" alt="after first compression" src="https://github.com/philintheattic/video-tools/assets/154841043/45419e36-8556-4017-a7d4-dd1379cb35e4">
<img width="200" alt="after 10th compression" src="https://github.com/philintheattic/video-tools/assets/154841043/744d951c-80ef-4c05-8481-80e861777d45">
<img width="200" alt="after 50th compression" src="https://github.com/philintheattic/video-tools/assets/154841043/aa061c6a-148d-40b6-b587-8bcc309368fb">

### videoslicer
This script takes an input video and slices it up vertically in a number of stripes. Those slices are then shuffled and reassembled back into a new video file. The number of slices can be specified by the user.

Example image, 25 slices:

<img width="400" alt="input video" src="https://github.com/philintheattic/video-tools/assets/154841043/1f5fd741-cfe5-4af0-a9bc-cce59abbfd3a">
<img width="400" alt="25 slices" src="https://github.com/philintheattic/video-tools/assets/154841043/91e20c9b-010d-4082-836e-61e62afb906e">

### videotunneler
This script takes an input video, scales it down and overlays it on top of itself creating a sort of tunnel effect. You can specify the number of copies and also provide a value for rotation. Rotation happens over time by multiplying the input value with the the t variable in the FFmpeg rotation filter.

Example image of the input file, n=4:no rotation, n=10,rotation=0.01

<img width="200" alt="input video" src="https://github.com/philintheattic/video-tools/assets/154841043/c36a8581-f6ce-44c5-a10e-4ec4371f31a3">
<img width="200" alt="copies:4, no rotation" src="https://github.com/philintheattic/video-tools/assets/154841043/e7cb83c3-d1a6-43d8-ad32-665c208d817e">
<img width="200" alt="copies:10, rotation:0.01" src="https://github.com/philintheattic/video-tools/assets/154841043/2fa133cb-3922-4340-b5a9-8568988c9d6d">

### videoslitscan
A slitscan effect that works by slicing the input video into a lot of horizontal stripes and then offsetting each slice in time. The slices are then reassembled back together.

Example video: Slice width=10

https://github.com/philintheattic/video-tools/assets/154841043/3ea48a28-9af6-4eae-bd1e-81fccc452cce

### videointerpolater
Uses the FFmpeg filter `minterpolate` to stretch a video with some sort of optical flow. Inspired by this [Blogpost](https://www.hellocatfood.com/misusing-ffmpegs-motion-interpolation-options/) from Antonio Roberts. Best used on a very short clip that contains only single frames of images in quick succesion. If you then use high stretch factor values you get interesting motion interpolation artifacts

Example:

Input file in original speed:

https://github.com/philintheattic/video-tools/assets/154841043/907e6830-c2c3-4bcf-a30f-eef4c1259d8f

Output file. Stretch factor = 40

https://github.com/philintheattic/video-tools/assets/154841043/f5615b80-466b-47f1-9dd8-6f017f7e45d9

### videoeraserpolater
Takes an input video and extracts 1 frame per second. The resulting video is then stretched back to its original length with the `minterpolate` filter applied. The result is a wildly interpolated version of the original clip. A bit hard to describe I guess so here is an example:

Input file:

https://github.com/philintheattic/video-tools/assets/154841043/6e85e60a-10d0-4c60-b5cb-702106c010c8

Output file:

https://github.com/philintheattic/video-tools/assets/154841043/7497b490-09fb-4bd1-a898-9f4b331d5211

### video2ascii
Converts any video into ASCII art. This works by first extracting all the frames from the input video and then converting them one by one into ASCII. The code for the ASCII conversion is based upon a [youtube tutorial by Raphson](https://youtu.be/2fZBLPk-T2Y?si=btfsYBQzULswSW4Z). If all images are processed they are concatenated with ffmpeg. You lose the audio in the process but this is no big deal since you can easily just use the audio track from the original clip in your video editor of choice. WARNING: Since every frame needs to be calculated it could take a lot of time depending on the length (and thus frame count) of the input video.

You can also specify the "Level of Detail" (LOD) of the ASCII conversion.

Example:

https://github.com/philintheattic/video-tools/assets/154841043/784ddced-5514-44ff-9de7-0c9ec8c8c777

### videomvextractor
This script uses the ffmpeg `codecview` filter option that superimposes motion vector data upon the image. The cool thing is that it is coupled with a `blend` filter that effectively cancels out the original footage so that only the motion vector visualization is visible in the final output. 

Example:

https://github.com/philintheattic/video-tools/assets/154841043/b9e0a6a6-3c6b-4107-afe6-791924e4916a

### videopixelsort
Works like the video2ascii script but performs a pixel sorting algorithm on the individual frames. The code for the pixel sorting stuff comes from [Gregory Johnson](https://gist.github.com/GregTJ/097d7829048c6bf27bc5008a8d153825). WARNING: Since every frame needs to be calculated it could take a lot of time depending on the length (and thus frame count) of the input video.

Example:

https://github.com/philintheattic/video-tools/assets/154841043/794d7404-5374-4e42-b9d5-a3438e5c9b94

### videocirculator
Uses the ffmpeg `geq` (generic equation) filter option to bend the pixels around a half-sphere that is mirrored along the horizontal axis. This ffmpeg command was originally used to spice up [waveform visualizations](https://www.splashmusic.com/post/audio-visualisation-with-ffmpeg) (also done with ffmpeg) and bend them around in a circle but can of course be used on any footage with interesting results.

Example:

https://github.com/philintheattic/video-tools/assets/154841043/1295c892-65e8-479f-864a-f77c9061fedf

### aspectratioswitcher
When the client wants vertical video for reels...
This is just a joke. It switches the videos orientation (it flips width with height and vice versa) without preserving the original aspect ratio. The result is a stretched video. A fun idea would be to write a program that automatically rips reels off instagram, flips the aspect ratio and displays the new videos somewhere else. Maybe in an art gallery. (as if there was a satirical commentary on viewing habits in the 21st century hidden in there...)

Example:

https://github.com/philintheattic/video-tools/assets/154841043/71b56ddb-735d-49e4-b19e-3960e9f084a1

### videotripper
Makes videos "trippy". I tried to learn the opencv library and found out that you can just multiply the values of a pixel array with an arbitrary number and it results in crazy colors. This script takes an input video and a multiplication factor and outputs a new video with multiplied color values resulting in a colorful "trippy" look. The higher the number the more "noisy" it looks. You lose the audio in the process but you can always add it back using the original video in the video editor of your choice. In fact the result works great if you overlay it on top of your original clip and play around with blending modes.
As a bonus, this script actually shows a preview of the resulting image while it is encoding so you can quickly check the intensity of the effect and abort (using the Enter key while the preview window is in focus) the process if you need to adjust the value.

Example:

https://github.com/philintheattic/video-tools/assets/154841043/4a6baada-a553-4941-ac83-ab4815636212


### tbp_makeimage
I took the [timebased photography](https://github.com/hbajohr/time-based-photography) script by Hannes Bajohr and modified it so that it only outputs 1 Frame. Check out his [github](https://github.com/hbajohr) for more information on what timebased photography is and how it works.







