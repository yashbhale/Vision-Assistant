import math
import cv2
import pyttsx3
import threading
import speech_recognition as sr
import datetime as dt
import os
from gtts import gTTS
import subprocess


thres = 0.6
ip_cam_url = "http://192.168.189.213:8080/video"
cap = cv2.VideoCapture(ip_cam_url)
cap.set(3, 648)  # Width
cap.set(4, 480)  # Height

r = sr.Recognizer()

classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')


configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(328, 328)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


engine = pyttsx3.init()
engine.setProperty('rate', 150)

detected_objects = set()

FOCAL_LENGTH = 700

KNOWN_FACE_WIDTH = 0.15

countable = ["how many", "many", "how much", "count", "counts", "counting", "number of", "number", "numbers", "there", "distinct", "what"]
Distance = ["distance", "between", "distance between", "far"]
specifiable = ["peoples", "people", "face", "faces", "person","objects", "persons","bottle","bottles","car","cell Phone","chair","tv","moniter","table","mouse","remote","keyboard",]

fcountable = False
fdistance = False
fSpecifiable = [False, ""]
start = False
question = False

object_distance = {}

def search(str):
    global fcountable, fdistance, fSpecifiable, start, prev, question

    words = str.split()
    que = "how"
    que1="is"
    print(words)
    if words[0]==que1:
        question=True
    for tar in words:
        if tar == "they" or tar == "their":
            prev = True
        if tar == "hello" or tar == "hi":
            start = True

        for val in countable:
            if tar == val:
                fcountable = True
                break
        for val in Distance:
            if tar == val:
                fdistance = True
                break
        for val in specifiable:
            if tar == val:
                fSpecifiable[0] = True
                fSpecifiable[1] = tar
                break

def calculate_distance(knownWidth, focalLength, perWidth):
    # Distance from camera to object
    return (knownWidth * focalLength) / perWidth

def announce_objects():
    global fcountable, fdistance, fSpecifiable, start, prev
    while True:
        with sr.Microphone() as source:
            print("Speak")
            input_audio = r.listen(source)
            try:
                text = r.recognize_google(input_audio)
                search(text.lower())
                if start:
                    start = False
                    now = dt.datetime.now()
                    text = ""
                    if now.strftime("%p").lower() == "am":
                        text += " good morning, now it's "
                    elif now.strftime("%p").lower() == "pm":
                        text += "good afternoon sir, now it's "
                    text += now.strftime("%I") + ":" + now.strftime("%M") + " O'clock tell me what can I help you"

                    language = 'en'
                    tts = gTTS(text=text, lang=language)
                    tts.save("output.mp3")

                    if os.name == 'nt':
                        try:

                            command = [
r"C:\Users\ll010\Downloads\mpg123-1.32.6-static-x86-64\mpg123-1.32.6-static-x86-64\mpg123.exe",
                                "output.mp3"]
                            subprocess.run(command)
                        except FileNotFoundError:
                            print(
                                "Error: mpg123.exe not found. Please install mpg123 and ensure it's in your system path or adjust the path in the script.")
                        except Exception as e:
                            print(f"An error occurred during playback: {e}")

                    else:
                        print(f"Unsupported operating system: {os.name}")

                if question:
                    if fSpecifiable[0]:
                        text = f"No there is no {fSpecifiable[1]} like in front of you "
                        for obj in detected_objects:
                            if fSpecifiable[1] == obj:
                                text = f"Yes I can see {fSpecifiable[1]} in front of you which is at {math.floor(object_distance[obj] * 100 /30)} steps"
                                break

                        language = 'en'
                        tts = gTTS(text=text, lang=language)
                        tts.save("output.mp3")

                        if os.name == 'nt':
                            try:

                                command = [
                                    r"C:\Users\ll010\Downloads\mpg123-1.32.6-static-x86-64\mpg123-1.32.6-static-x86-64\mpg123.exe",
                                    "output.mp3"]
                                subprocess.run(command)
                            except FileNotFoundError:
                                print(
                                    "Error: mpg123.exe not found. Please install mpg123 and ensure it's in your system path or adjust the path in the script.")
                            except Exception as e:
                                print(f"An error occurred during playback: {e}")
                        else:
                            print(f"Unsupported operating system: {os.name}")

                        detected_objects.clear()
                if fcountable and fSpecifiable[0]:
                    fcountable = False
                    fSpecifiable[0] = False
                    text = "I can see "
                    objects = list(detected_objects)
                    count = len(objects)
                    if count == 1:
                        text += f"a {fSpecifiable[1]}"
                    else:
                        text += f"{count} {fSpecifiable[1]}'s in front of you"

                    language = 'en'
                    tts = gTTS(text=text, lang=language)
                    tts.save("output.mp3")

                    if os.name == 'nt':
                        try:

                            command = [
                                r"C:\Users\ll010\Downloads\mpg123-1.32.6-static-x86-64\mpg123-1.32.6-static-x86-64\mpg123.exe",
                                "output.mp3"]
                            subprocess.run(command)
                        except FileNotFoundError:
                            print(
                                "Error: mpg123.exe not found. Please install mpg123 and ensure it's in your system path or adjust the path in the script.")
                        except Exception as e:
                            print(f"An error occurred during playback: {e}")

                    else:
                        print(f"Unsupported operating system: {os.name}")
                    detected_objects.clear()
                if fcountable and fdistance:
                    fcountable = False
                    fdistance = False
                    text = "I think there is a, "
                    for obj in object_distance:
                        text += f"{obj} which is at around {math.floor(object_distance[obj] * 100 / 30)} steps and "
                    text = text[:-5] + "."

                    language = 'en'
                    tts = gTTS(text=text, lang=language)
                    tts.save("output.mp3")

                    if os.name == 'nt':
                        try:

                            command = [
                                r"C:\Users\ll010\Downloads\mpg123-1.32.6-static-x86-64\mpg123-1.32.6-static-x86-64\mpg123.exe",
                                "output.mp3"]
                            subprocess.run(command)
                        except FileNotFoundError:
                            print(
                                "Error: mpg123.exe not found. Please install mpg123 and ensure it's in your system path or adjust the path in the script.")
                        except Exception as e:
                            print(f"An error occurred during playback: {e}")

                    else:
                        print(f"Unsupported operating system: {os.name}")
                    object_distance.clear()

                if fcountable and fSpecifiable[0] and fdistance:
                    text = ""
                    fcountable = False
                    fSpecifiable[0] = False
                    fdistance = False
                    for obj in object_distance:
                        if obj == fSpecifiable[1]:
                            text += f"{obj} which is at around {math.floor(object_distance[obj] * 100 / 30)} steps and "
                            object_distance.pop(fSpecifiable[1])
                    text = text[:-5] + "."
                    language = 'en'
                    tts = gTTS(text=text, lang=language)
                    tts.save("output.mp3")

                    if os.name == 'nt':
                        try:

                            command = [
                                r"C:\Users\ll010\Downloads\mpg123-1.32.6-static-x86-64\mpg123-1.32.6-static-x86-64\mpg123.exe",
                                "output.mp3"]
                            subprocess.run(command)
                        except FileNotFoundError:
                            print(
                                "Error: mpg123.exe not found. Please install mpg123 and ensure it's in your system path or adjust the path in the script.")
                        except Exception as e:
                            print(f"An error occurred during playback: {e}")

                    else:
                        print(f"Unsupported operating system: {os.name}")

            except sr.UnknownValueError:
                print("Sorry, I didn't hear you")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

#new thread launch
threading.Thread(target=announce_objects, daemon=True).start()

while True:
    success, img = cap.read()
    if not success:
        break

    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
            label = f"{classNames[classId - 1]}: {round(confidence * 100, 2)}%"
            cv2.putText(img, label, (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            detected_objects.add(classNames[classId - 1])
            object_width_in_frame = box[2]  # Width of the bounding box
            distance = calculate_distance(KNOWN_FACE_WIDTH, FOCAL_LENGTH, object_width_in_frame)
            distance_label = f"Distance: {round(distance-0.03, 2)} meters"
            cv2.putText(img, distance_label, (box[0] + 10, box[1] + 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            object_distance[classNames[classId - 1]] = round(distance, 2)

    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()