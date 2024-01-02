# video-tools
## Installation
Copy the script you want to use into the folder that contains the videofile that you want to process. Run the script and follow the prompts. For the script to work you need an installation of ffmpeg that is added to PATH. Depending on the script you may also need opencv which you can install by running:
```
pip install opencv-python
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

### tbp_makeimage
I took the [timebased photography](https://github.com/hbajohr/time-based-photography) script by Hannes Bajohr and modified it so that it only outputs 1 Frame. Check out his [github](https://github.com/hbajohr) for more information on what timebased photography is and how it works.





