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
This script takes an input file and compresses it via ffmpeg with a quality setting of `-crf 67` which is the worst possible setting in ffmpeg. This generates a highly compressed videofile with lots of compression artifacts. This compressed videofile is then used as a new input file and will be further compressed and so on. The file will get more and more "destroyed" in the process creating lots of interesting (and sometimes creepy) visuals. You can specify the number of iterations.

Example images of the input file, after the first compression, the 10th and the 50th:

<img width="200" alt="input file" src="https://github.com/philintheattic/video-tools/assets/154841043/d3dbab2c-37a6-4e1d-a87a-d1b43523e465">
<img width="200" alt="after first compression" src="https://github.com/philintheattic/video-tools/assets/154841043/45419e36-8556-4017-a7d4-dd1379cb35e4">
<img width="200" alt="after 10th compression" src="https://github.com/philintheattic/video-tools/assets/154841043/744d951c-80ef-4c05-8481-80e861777d45">
<img width="200" alt="after 50th compression" src="https://github.com/philintheattic/video-tools/assets/154841043/aa061c6a-148d-40b6-b587-8bcc309368fb">

### videoslicer
This script takes an input file and slices it up vertically in a number of stripes. Those slices are then shuffled and reassembled back into a new video file. The number of slices can be specified by the user.

Example image, 25 slices:

<img width="400" alt="input video" src="https://github.com/philintheattic/video-tools/assets/154841043/1f5fd741-cfe5-4af0-a9bc-cce59abbfd3a">
<img width="400" alt="25 slices" src="https://github.com/philintheattic/video-tools/assets/154841043/91e20c9b-010d-4082-836e-61e62afb906e">

