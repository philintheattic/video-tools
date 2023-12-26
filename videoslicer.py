import subprocess
import cv2
import random

print("This Script takes an input video and slices it up vertically.")
print("Those slices are then reassembled back together randomly.")

# Variablen abfragen/deklarieren
input_file = input("Input File: ")
slices_amount = input("Amount of slices: ")
output_file = input("Output File: ")
frame_width = int(cv2.VideoCapture(input_file).get(cv2.CAP_PROP_FRAME_WIDTH))
slices_width = int(frame_width/int(slices_amount))

# Helferfunktion um easy strings aus arrays zu machen. Verbessert Lesbarkeit im Code
def makeString(array):
    name = "".join(array)
    return name

# Erstellt den Teil des FFmpeg Filterbefehls, der die input streams bennent ([v1][v2][v3]..[vn])
def getVideoInputs():
    print("getting videoinputs")
    video_inputs = []
    for i in range(int(slices_amount)):
        video_input = "[v" + str(i) + "]"   # generate as many ffmpeg inputs as necessary
        video_inputs.append(video_input)    # fill the array with the inputs
    v_string = "".join(video_inputs)        # save the array in a single string
    #print(v_string)
    return v_string, video_inputs           # index 0 returns the inputs as a string, index 1 returns the inputs as array


# Erstellt den crop-Teil des FFmpeg Filterbefehls und passt die Strings dynamisch an den user input an.
def getVideoCrops():
    print("getting videocrops")
    video_crops = []
    for i in range(int(slices_amount)):
        video_crop = "[v" + str(i) + "]crop=" + str(slices_width) + ":ih:" + str(slices_width*i) + ":0[v" + str(i) + "];"
        video_crops.append(video_crop)
    c_string = "".join(video_crops)
    #print(c_string)
    return c_string, video_crops


# Würfelt die Reihenfolge der Slices neu zusammen. Erstellt am Ende einen String für den FFmpeg Befehl
def getStackingOrder():
    random_order = video_inputs[1]          # hier kopiere ich das inputs array in eine neue variable
    random.shuffle(random_order)            # shufflet das kopierte array
    r_order = makeString(random_order)
    #print(r_order)
    return r_order , random_order

# Jede der oberen Funktionen gibt zwei Outputs. Nämlich einen string für ffmpeg und ein array. Damit ich die verwenden kann muss ich den Output erst in einer Variablen speichern und kann dann mit variable[0] oder variable[1] auf den string oder da array zugreifen, wenn ich es brauche (Hauptsächlich wichtig für das randomisieren der Slices aber habe es konsequent auch in die anderen funktionen eingebaut. wer weiß wofür es gut ist)
video_inputs = getVideoInputs()
video_crops = getVideoCrops()
stacking_order = getStackingOrder()


# Array um daraus dann den langen String für den -filter_complex zu erstellen
filter_command = [
    "[0]split=",
    slices_amount,
    video_inputs[0],
    ";",
    video_crops[0],
    stacking_order[0],
    "hstack=inputs=",
    str(slices_amount),
]

# Array für den finalen ffmpeg Befehl
ffmpeg_command = [
    "ffmpeg",
    "-i",
    input_file,
    "-filter_complex",
    makeString(filter_command),
    output_file
]

# Jetzt muss man nur noch den eigentlichen Befehl ausführen und Zackfeddisch.
subprocess.run(ffmpeg_command)

print("Finished!")
input("Press Enter to exit.")


# ffmpeg -i test.mp4 -filter_complex
# "[0]split=4[v1][v2][v3][v4];
# [v1]crop=iw/4:ih:(iw/4)*0:0[v1];
# [v2]crop=iw/4:ih:(iw/4)*1:0[v2];
# [v3]crop=iw/4:ih:(iw/4)*2:0[v3];
# [v4]crop=iw/4:ih:(iw/4)*3:0[v4];
# [v4][v2][v1][v3]hstack=inputs=4" out.mp4

# ffmpeg -i test.mp4 -filter_complex "[0]split=4[v1][v2][v3][v4];[v1]crop=iw/4:ih:(iw/4)*0:0[v1];[v2]crop=iw/4:ih:(iw/4)*1:0[v2];[v3]crop=iw/4:ih:(iw/4)*2:0[v3];[v4]crop=iw/4:ih:(iw/4)*3:0[v4];[v4][v2][v1][v3]hstack=inputs=4" out.mp4