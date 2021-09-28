#for python 2
# -*- encoding: UTF-8 -*-
import sys
import time
import json
import requests

from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy


robot_IP = "192.168.11.7" #LL IP

def weatherReport():
    tts = ALProxy("ALTextToSpeech", robot_IP, 9559)
    tts.setLanguage("Japanese")

    #パラメーター
    params={"q":"Sendai","appid":"f727d8c5ef8897b1bd0d263ea977e4d5"}

    url="http://api.openweathermap.org/data/2.5/forecast"
    res=requests.get(url,params=params)
    print(res)

    jsonText=res.json()
    print'都市：Sendai'
    tenki_eng=jsonText["list"][0]["weather"][0]["main"]
    print jsonText["list"][0]
    print tenki_eng
    if tenki_eng == "Clouds":
        tenki_jp= "くもり"
    elif tenki_eng == "Rain":
        tenki_jp= "雨"
    elif tenki_eng == "Clear":
        tenki_jp= "晴れ"
    print tenki_jp

    tenki_speech="\\vct=100\\今日の仙台の天気は" +tenki_jp+ "です。"
    print'tenki_speech'

    tts.say(tenki_speech)
    if tenki_jp == "雨":
        tts.say("傘忘れないでね")

    if tenki_jp == "晴れ":
        tts.say("水飲んでくださいね")
