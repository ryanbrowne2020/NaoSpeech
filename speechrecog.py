# -*- encoding: UTF-8 -*-

import speech_recognition as sr
import socket
import time
from os import system
from naoqi import ALBroker, ALModule, ALProxy
from colorama import init, Fore, Back, Style
import random


tts = audio = None

r = None
m = None
response = None
robot_IP = "192.168.11.7" #LL IP
robot_PORT = 9559

tts = ALProxy("ALTextToSpeech", robot_IP, 9559)
lights = ALProxy("ALLeds", robot_IP, 9559)

def init():
    # Create a TCP / IP socket
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Testing internet...."
    hostname = "google.com"
    global response
    #response = system("ping " + hostname)
    response = 0
    if response == 0:
        print "I can reach internet, I'm going to use Google TTS API"
    else:
        print "I can't reach internet"
    global r, m
    r = sr.Recognizer()  # obtain audio from the laptop microphone
    r.dynamic_energy_threshold = False # デフォルトだと True だが、音声が長めになりがちなので False にしている
    r.energy_threshold = 270  # minimum audio energy to consider for recording (300) 170 worked okay. 570 is background talking
    r.phrase_threshold = 0.10 # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
    r.pause_threshold = 1.2 # seconds of non-speaking audio before a phrase is considered complete
    r.non_speaking_duration = 0.5 # seconds of non-speaking audio to keep on both sides of the recording

    m = sr.Microphone()

def calibrate():
    with m as source:
        print("Please wait 2s. Calibrating microphone...")
        # listen for 2 seconds and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=2)

def listen():
    while True:
        with m as source:
            lights.on("FaceLeds")
            audio = r.listen(source, phrase_time_limit=6)
            lights.off("FaceLeds")
            try:
                if response == 0:
                    speech = r.recognize_google(audio, None, "ja-JP")
                    print "ユーザー：　'" + Fore.GREEN +speech + "'"
                    print Style.RESET_ALL
                    return speech
            except sr.UnknownValueError:
                print("NAOが待っています。なにも聞こえなかった")

def main():
    init()
    calibrate()
    listen()


if __name__ == '__main__':
    main()
