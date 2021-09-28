# -*- encoding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import argparse
import time
import traceback
import random
import speechrecog as stt
import qi
from naoqi import ALBroker, ALModule, ALProxy
from nao import Nao
from weather_speak import weatherReport
from colorama import init, Fore, Back, Style


robot_IP = "192.168.11.7" #LL IP
robot_PORT = 9559

tts = ALProxy("ALTextToSpeech", robot_IP, 9559)
lights = ALProxy("ALLeds", robot_IP, 9559)
motionProxy  = ALProxy("ALMotion", robot_IP, 9559)


nao=None

def main():
    """A simple main"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ip",
        type=str,
        default=robot_IP,
        help="Robot IP address. On robot or Local Naoqi: use '192.168.11.3'.")
    parser.add_argument(
        "--port", type=int, default=9559, help="Naoqi port number")
    args = parser.parse_args()
    global nao
    nao = Nao(args.ip, args.port)
    nao.get_posture()
    print Fore.GREEN + "######################"
    print Fore.GREEN + "#####　始まります！　####"
    print Fore.GREEN + "######################"
    print Style.RESET_ALL
    stt.init()

#=============================
#===== ** START UP *** =======
#=============================
def startUP():
    #print("starting General Listen")
    tts.setLanguage("Japanese")
    tts.say("ちょっと話しましょう \\pau=1000\\")
    print "NAO：　'" + Fore.BLUE +"ちょっと話しましょう" + "'"
    print Style.RESET_ALL
    tts.say("話しかけてください")
    print "NAO：　'" + Fore.BLUE +"話しかけてください" + "'"
    print Style.RESET_ALL


#=============================
#===== ** LISTEN *** =========
#=============================
def generalListen():

    health_advice = [
    "毎日　さんぜんぽ　を歩くように目指しましょう",
    "毎日たくさん野菜をとりましょう",
    "毎日、\\pau=300\\ 家でも軽く運動するように目指しましょう",
    "砂糖の摂取　\\pau=300\\ 量を控えるように目指しましょう"
    ]

    brain_advice = [
    "読書やすうどくなどの　\\pau=300\\ パズルをするなどして、毎日脳を刺激しましょう",
    "オメガ3などの　\\pau=300\\ 良質な脂肪を摂るように目指しましょう",
    "質の良い睡眠を　\\pau=300\\ たくさんとるようにしましょう",
    "社会的な活動を続けるようにしましょう。\\pau=300\\ 電話でもいいので、\\pau=300\\ 友人や家族と話してみませんか？"
    ]

    brain_train = [
    "すうどく",
    "\\pau=300\\　かわしま先生の脳トレ",
    "新聞を読むこと",
    "何か　\\pau=300\\ 新しいスキルを習うこと",
    "パズルをすること",
    "計算",
    ]

    exercise_choice = [
    "散歩",
    "ラジオ体操",
    "階段をのぼること"
    ]

    tts.setLanguage("Japanese")
    speech=stt.listen()

    if ("家族" in speech):
        talkFamily()

    elif (("立って" in speech) or ("だって" in speech) or ("たって" in speech)):
        nao.go_to_posture("StandInit")

    elif ("座って" in speech):
        nao.go_to_posture("Sit")

    elif ("ペット" in speech):
        petTalk()

    elif(("どんな話し" in speech) or ("どんな話" in speech) or ("どんなはなし" in speech)):
        askUser()

    elif("違うこと" in speech):
        askUser2()

    elif ("音楽" in speech):
        playMusic()

    elif ("またね" in speech):
        lights.rotateEyes(0x000000FF, 0.5, 1)
        tts.say("少し休憩しますか。またね！")
        print "NAO：　'" + Fore.BLUE +"少し休憩しますか。またね！" + "'"
        print Style.RESET_ALL
        motionProxy.rest()
        return 0

#=======exercise =====
    elif (("健康" in speech) and ("情報" in speech)):
        tts.say("はい、健康な生活に \\pau=300\\ 役立つ情報をお伝えします")
        print "NAO：　'" + Fore.BLUE +"はい、健康な生活に役立つ情報をお伝えします" + "'"
        print Style.RESET_ALL
        tts.say(random.choice(health_advice))
        print "NAO：　'" + Fore.BLUE +"（健康アドバイス言いました）" + "'"
        print Style.RESET_ALL
        tts.say("健康に良いことをしてますか？ はいかいいえと答えてください。")
        print "NAO：　'" + Fore.BLUE +"健康に良いことをしてますか？ はいかいいえと答えてください。" + "'"
        print Style.RESET_ALL
        speech = stt.listen()
        if (
        ("はい" in speech) or
        ("はーい" in speech) or
        ("してます" in speech) or
        ("やって" in speech)
        ):
            tts.say("それは何ですか")
            print "NAO：　'" + Fore.BLUE +"それは何ですか" + "'"
            print Style.RESET_ALL
            stt.listen()
            if speech:
                tts.say("どのくらいしていますか")
                print "NAO：　'" + Fore.BLUE +"どのくらいしていますか" + "'"
                print Style.RESET_ALL
                stt.listen()
                if speech:
                    tts.say("そうかー！がんばってください")
                    print "NAO：　'" + Fore.BLUE +"そうかー！がんばってください" + "'"
                    print Style.RESET_ALL
        else:
            tts.say(random.choice(health_advice))
            print "NAO：　'" + Fore.BLUE +"(健康アドバイス言いました)" + "'"
            print Style.RESET_ALL

    elif (("おすすめ" in speech) and ("運動" in speech)):
        thingtoSay = "おすすめの運動わ" + random.choice(exercise_choice) + "です"
        tts.say(thingtoSay)
        print "NAO：　'" + Fore.BLUE +"(運動アドバイス言いました)" + "'"
        print Style.RESET_ALL


#====== cognitive =======
    elif (
        ("認知症" in speech) and
        ("予防" in speech)
        ):
        tts.say("はい、認知症予防に　\\pau=300\\ 役たつ情報をお伝えします")
        print "NAO：　'" + Fore.BLUE +"はい、認知症予防に役たつ情報をお伝えします" + "'"
        print Style.RESET_ALL
        tts.say(random.choice(brain_advice))
        print "NAO：　'" + Fore.BLUE +"(認知症予防アドバイス言いました)" + "'"
        print Style.RESET_ALL
        time.sleep(2)

    elif (
        ("トレ" in speech) or
        ("脳" in speech)
        ):
        thingtoSay = "おすすめの脳トレわ" + random.choice(brain_train) + "です"
        tts.say(thingtoSay)
        print "NAO：　'" + Fore.BLUE +"(脳トレおすすめ言いました)" + "'"
        print Style.RESET_ALL
        time.sleep(2)

#====== greetings =======

    elif ("おはよう" in speech):
        tts.say("おはようございます。\\pau=1000\\　体調はいかがですか ")
        print "NAO：　'" + Fore.BLUE +"おはようございます。体調はいかがですか" + "'"
        print Style.RESET_ALL
        stt.listen()
        if speech:
            tts.say("なるほどー！今日いちにち元気に過ごせるといいですね。")
            print "NAO：　'" + Fore.BLUE +"なるほどー！今日いちにち元気に過ごせるといいですね。" + "'"
            print Style.RESET_ALL
            time.sleep(2)

    elif ("こんばんは" in speech):
        tts.say("こんばんは。今日はどんな一日でしたか？")
        print "NAO：　'" + Fore.BLUE +"こんばんは。今日はどんな一日でしたか？" + "'"
        print Style.RESET_ALL
        speech = stt.listen()
        if speech:
            tts.say("そうですかー！。お疲れ様です")
            print "NAO：　'" + Fore.BLUE +"そうですかー！お疲れ様です" + "'"
            print Style.RESET_ALL
            time.sleep(2)

    elif ("こんにちは" in speech):
        tts.say("こんにちは！お元気ですか")
        print "NAO：　'" + Fore.BLUE +"こんにちは！お元気ですか" + "'"
        print Style.RESET_ALL
        speech = stt.listen()
        if (
        ("元気です" in speech) or
        ("元気だ" in speech) or
        ("いい" in speech)
        ):
            tts.say("それはなによりです。\\pau=500\\ 今朝はなんじに起きましたか")
            print "NAO：　'" + Fore.BLUE +"それはなによりです。今朝はなんじに起きましたか" + "'"
            print Style.RESET_ALL
            speech=stt.listen()
            if (
                ("3時" in speech) or
                ("4時" in speech) or
                ("5時" in speech) or
                ("6時" in speech) or
                ("7時" in speech) or
                ("8時" in speech)
                ):
                tts.say("早いですね")
                print "NAO：　'" + Fore.BLUE +"早いですね" + "'"
                print Style.RESET_ALL
            elif (
                ("夜" in speech) or
                ("午後" in speech)
                ):
                tts.say("ゆっくりですね")
                print "NAO：　'" + Fore.BLUE +"ゆっくりですね" + "'"
                print Style.RESET_ALL
                time.sleep(2)
            else:
                tts.say("ゆっくりですね")
                print "NAO：　'" + Fore.BLUE +"ゆっくりですね" + "'"
                print Style.RESET_ALL
                time.sleep(2)
        elif speech:
            tts.say("そうかー。\\pau=500\\ 今朝はなんじに起きましたか")
            print "NAO：　'" + Fore.BLUE +"そうかー。今朝はなんじに起きましたか" + "'"
            print Style.RESET_ALL
            speech=stt.listen()
            if (
                ("3時" in speech) or
                ("4時" in speech) or
                ("5時" in speech) or
                ("6時" in speech) or
                ("7時" in speech) or
                ("8時" in speech)
                ):
                tts.say("早いですね")
                print "NAO：　'" + Fore.BLUE +"早いですね" + "'"
                print Style.RESET_ALL
            elif (
                ("夜" in speech) or
                ("午後" in speech)
                ):
                tts.say("ゆっくりですね")
                print "NAO：　'" + Fore.BLUE +"ゆっくりですね" + "'"
                print Style.RESET_ALL
                time.sleep(2)
            else:
                tts.say("ゆっくりですね")
                print "NAO：　'" + Fore.BLUE +"ゆっくりですね" + "'"
                print Style.RESET_ALL
                time.sleep(2)


    elif ("ただいま" in speech):
        tts.say("おかえりなさい。ゆっくり休んでください")
        print "NAO：　'" + Fore.BLUE +"おかえりなさい。ゆっくり休んでください" + "'"
        print Style.RESET_ALL
        time.sleep(2)

    elif ("休みたい" in speech):
        talkTea()

    elif ("天気" in speech):
        getWeather()

    else:
        lights.rotateEyes(0x000000FF, 0.5, 1)
        tts.say("はい")
        print "NAO：　'" + Fore.BLUE +"はい" + "'"
        print Style.RESET_ALL

#====================================
#===== ** OTHER FUNCTIONS *** =======
#====================================

#==========
def talkTea():
    tts.say("お茶いかがですか。はいかいいえと答えてください。")
    speech = stt.listen()

    if (
        ("はい" in speech) or
        ("はーい" in speech) or
        ("お願い" in speech)
        ):
        tts.say("お茶は美味しいですね。")
        ttime.sleep(2)
    elif (
        ("いいえ" in speech) or
        ("いいね" in speech) or
        ("家" in speech) or
        ("大丈夫" in speech)
        ):
        tts.say("そうですか")
    elif ("コーヒー" in speech):
        tts.say("まあ、コーヒーも美味しいね")
        time.sleep(2)
    else:
        tts.say("なるほど")
        time.sleep(2)

#==========
def talkFamily():
    tts.say("私は \\pau=300\\ 50以上の国に5000人の兄弟がいます。あなたは誰と住んでいますか？")
    print "NAO：　'" + Fore.BLUE +"私は50以上の国に5000人の兄弟がいます。あなたは誰と住んでいますか？" + "'"
    print Style.RESET_ALL
    speech = stt.listen()
    if (
        ("お母さん" in speech) or
        ("母" in speech) or
        ("父さん" in speech) or
        ("父" in speech)
        ):
        tts.say("親御さんはお元気ですか。はいかいいえと答えてください。")
        print "NAO：　'" + Fore.BLUE +"親御さんはお元気ですか。はいかいいえと答えてください。" + "'"
        print Style.RESET_ALL
        speech = stt.listen()
        if (
            ("はい" in speech) or
            ("はーい" in speech) or
            ("元気です" in speech) or
            ("元気だ" in speech)
            ):
            tts.say("それは何よりです")
            print "NAO：　'" + Fore.BLUE +"それは何よりです。" + "'"
            print Style.RESET_ALL
        elif (
            ("いいえ" in speech) or
            ("いいね" in speech) or
            ("家" in speech)
            ):
            tts.say("回復してお元気で過ごされることをお願っております")
            print "NAO：　'" + Fore.BLUE +"回復してお元気で過ごされることをお願っております" + "'"
            print Style.RESET_ALL
        else:
            tts.say("すみません、もう一度、家族について話しましょう、と言ってください")
            print "NAO：　'" + Fore.BLUE +"すみません、もう一度、家族について話しましょう、と言ってください" + "'"
            print Style.RESET_ALL
    elif (
        ("奥さん" in speech) or
        ("家内" in speech) or
        ("妻" in speech) or
        ("旦那" in speech) or
        ("夫" in speech)
        ):
        tts.say("いつも一緒に過ごしていますか。はいかいいえと答えてください。")
        print "NAO：　'" + Fore.BLUE +"いつも一緒に過ごしていますか。はいかいいえと答えてください。" + "'"
        print Style.RESET_ALL
        speech = stt.listen()
        if (
            ("はい" in speech) or
            ("はーい" in speech) or
            ("そう" in speech)
            ):
            tts.say("仲がいいですね！最近どこか一緒に出かけてますか")
            print "NAO：　'" + Fore.BLUE +"仲がいいですね！最近どこか一緒に出かけてますか" + "'"
            print Style.RESET_ALL
            stt.listen()
            if speech:
                tts.say("なるほど")
                print "NAO：　'" + Fore.BLUE +"なるほど" + "'"
                print Style.RESET_ALL
                time.sleep(2)
        elif (
            ("いいえ" in speech) or
            ("いいね" in speech) or
            ("家" in speech)
            ):
            tts.say("それぞれの時間も大切ですね！一緒にいる時はなにをしますか")
            print "NAO：　'" + Fore.BLUE +"それぞれの時間も大切ですね！一緒にいる時はなにをしますか" + "'"
            print Style.RESET_ALL
            stt.listen()
            if speech:
                tts.say("なるほど")
                print "NAO：　'" + Fore.BLUE +"なるほど" + "'"
                print Style.RESET_ALL
                time.sleep(2)
        else:
            tts.say("すみません、もう一度、家族について話しましょう、と言ってください")
            print "NAO：　'" + Fore.BLUE +"すみません、もう一度、家族について話しましょう、と言ってください" + "'"
            print Style.RESET_ALL
    elif (
        ("息子" in speech) or
        ("娘" in speech) or
        ("子供" in speech) or
        ("孫" in speech) or
        ("兄弟" in speech) or
        ("兄" in speech) or
        ("姉" in speech) or
        ("妹" in speech) or
        ("弟" in speech)
        ):
        tts.say("休日は一緒にどこかいったりしますか。はいかいいえと答えてください。")
        print "NAO：　'" + Fore.BLUE +"休日は一緒にどこかいったりしますか。はいかいいえと答えてください。" + "'"
        print Style.RESET_ALL
        speech = stt.listen()
        if (
            ("はい" in speech) or
            ("はーい" in speech) or
            ("そう" in speech)
            ):
            tts.say("それは楽しいですね。どこにいっていますか")
            print "NAO：　'" + Fore.BLUE +"それは楽しいですね。どこにいっていますか" + "'"
            print Style.RESET_ALL
            stt.listen()
            if speech:
                tts.say("いいですね")
                print "NAO：　'" + Fore.BLUE +"いいですね" + "'"
                print Style.RESET_ALL
                time.sleep(2)

        elif (
            ("いいえ" in speech) or
            ("いいね" in speech) or
            ("家" in speech) or
            ("あまり" in speech)
            ):
            tts.say("誘ってみたらいかがですか。今度どこに一緒に行きたいですか")
            print "NAO：　'" + Fore.BLUE +"誘ってみたらいかがですか。今度どこに一緒に行きたいですか" + "'"
            print Style.RESET_ALL
            stt.listen()
            if speech:
                tts.say("いいですね")
                print "NAO：　'" + Fore.BLUE +"いいですね" + "'"
                print Style.RESET_ALL
                time.sleep(2)
        else:
            tts.say("すみません、もう一度、家族について話しましょう、と言ってください")
            print "NAO：　'" + Fore.BLUE +"すみません、もう一度、家族について話しましょう、と言ってください" + "'"
            print Style.RESET_ALL
    else:
        tts.say("なるほど")
        print "NAO：　'" + Fore.BLUE +"なるほど" + "'"
        print Style.RESET_ALL
        time.sleep(2)

#==========
def getWeather():
        getweather = weatherReport()

#==========
def petTalk():
    tts.say("ペット飼ってますか。はいかいいえと答えてください。")
    print "NAO：　'" + Fore.BLUE +"ペット飼ってますか。はいかいいえと答えてください。" + "'"
    print Style.RESET_ALL
    speech = stt.listen()
    if (
    ("はい" in speech) or
    ("はーい" in speech) or
    ("買ってます" in speech) or
    ("勝てます" in speech) or
    ("飼ってます" in speech)
    ):
        tts.say("それはなんのペットですか？")
        print "NAO：　'" + Fore.BLUE +"それはなんのペットですか？" + "'"
        print Style.RESET_ALL
        speech = stt.listen()
        if ("犬" in speech):
            tts.say("大きい犬ですか？")
            print "NAO：　'" + Fore.BLUE +"大きい犬ですか？" + "'"
            print Style.RESET_ALL
            speech = stt.listen()
            if (("はい" in speech) or ("大きい" in speech)):
                tts.say("走れる \\pau=100\\ 広いところが必要ですね。いつもどこに散歩していますか？")
                print "NAO：　'" + Fore.BLUE +"走れる広いところが必要ですね。いつもどこに散歩していますか？" + "'"
                print Style.RESET_ALL
                stt.listen()
                if speech:
                    time.sleep(2)
            elif (("小さい" in speech) or ("いいえ" in speech) or ("ううん" in speech)):
                tts.say("小さくて可愛い犬見て見たいな〜。いつもどこに散歩していますか？")
                print "NAO：　'" + Fore.BLUE +"小さくて可愛い犬見て見たいな〜。いつもどこに散歩していますか？" + "'"
                print Style.RESET_ALL
                stt.listen()
                if speech:
                    time.sleep(2)
            else:
                tts.say("すみません、もう一度、ペットについて話しましょう、と言ってください")
                print "NAO：　'" + Fore.BLUE +"すみません、もう一度、ペットについて話しましょう、と言ってください" + "'"
                print Style.RESET_ALL
        elif ("猫" in speech):
            tts.say("猫ですね。\\pau=300\\ 猫ちゃんの名前はなんですか？")
            print "NAO：　'" + Fore.BLUE +"猫ですね。猫ちゃんの名前はなんですか？" + "'"
            print Style.RESET_ALL
            stt.listen()
            if speech:
                tts.say("可愛い名前ですね。")
                print "NAO：　'" + Fore.BLUE +"可愛い名前ですね。" + "'"
                print Style.RESET_ALL
        elif (("犬" not in speech) and ("猫" not in speech)):
            tts.say("飼うの楽しそうですね")
            print "NAO：　'" + Fore.BLUE +"飼うの楽しそうですね" + "'"
            print Style.RESET_ALL
    elif (
        ("いいえ" in speech) or
        ("いいね" in speech) or
        ("家" in speech)
        ):
        tts.say("私もそうです。昔、なにか飼っていましたか？はいかいいえと答えてください。")
        print "NAO：　'" + Fore.BLUE +"私もそうです。昔、なにか飼っていましたか？はいかいいえと答えてください。" + "'"
        print Style.RESET_ALL
        speech = stt.listen()
        if ("はい" in speech):
            tts.say("それはなんのペットですか")
            print "NAO：　'" + Fore.BLUE +"それはなんのペットですか" + "'"
            print Style.RESET_ALL
            speech = stt.listen()
            if ("犬" in speech):
                tts.say("わんわん！なるほど。")
                print "NAO：　'" + Fore.BLUE +"わんわん！なるほど。" + "'"
                print Style.RESET_ALL
            elif ("猫" in speech):
                tts.say("猫ですね。\\pau=1000\\ 猫ちゃんの名前はなんですか？")
                print "NAO：　'" + Fore.BLUE +"猫ですね。\\pau=1000\\ 猫ちゃんの名前はなんですか？" + "'"
                print Style.RESET_ALL
                stt.listen()
                if speech:
                    tts.say("可愛い名前ですね。")
                    print "NAO：　'" + Fore.BLUE +"可愛い名前ですね" + "'"
                    print Style.RESET_ALL
                    time.sleep(2)
            else:
                tts.say("飼うの楽しそうですね")
                print "NAO：　'" + Fore.BLUE +"飼うの楽しそうですね" + "'"
                print Style.RESET_ALL
                time.sleep(2)
        elif (
            ("いいえ" in speech) or
            ("いいね" in speech) or
            ("家" in speech)
            ):
                tts.say("なにか　\\pau=200\\ 飼いたいペットはありますか？")
                print "NAO：　'" + Fore.BLUE +"なにか飼いたいペットはありますか？" + "'"
                print Style.RESET_ALL
                speech = stt.listen()
                if (("ない" in speech) or ("ません" in speech)):
                    tts.say("そうですか。。。")
                    print "NAO：　'" + Fore.BLUE +"そうですか。。。" + "'"
                    print Style.RESET_ALL
                    time.sleep(2)
                else:
                    tts.say("飼うの楽しそうですね")
                    print "NAO：　'" + Fore.BLUE +"飼うの楽しそうですね" + "'"
                    print Style.RESET_ALL
                    time.sleep(2)

#==========
def askUser():
    tts.say("はい！食事、趣味、買い物の話題の中からどれか選んでください")
    print "NAO：　'" + Fore.BLUE +"はい！食事、趣味、買い物の話題の中からどれか選んでください" + "'"
    print Style.RESET_ALL
    speech = stt.listen()
    if ("食事" in speech):
        shokuji()
    elif ("趣味" in speech):
        shumi()
    elif ("買い物" in speech):
        kaimono()

#==========
fun_phrase = [
"最近 \\pau=200\\ 嬉しいことわありましたか？",
"最近 \\pau=200\\ 楽しかったことわありましたか？"
]

def askUser2():
    tts.say(random.choice(fun_phrase))
    speech = stt.listen()
    if (
    ("あった" in speech) or
    ("ありました" in speech)
    ):
        tts.say("どんなことか、\\pau=200\\　聞かせて！")
        stt.listen()
        if speech:
            tts.say("なるほど！\\pau=200\\　いいですね")
            time.sleep(2)
    elif (
    ("ない" in speech) or
    ("特に" in speech)
    ):
        tts.say("そうですか！")
        time.sleep(2)
    else:
        tts.say("そうですか")
        time.sleep(2)

#==========
def shokuji():
    tts.say("食事は作りますか。はいかいいえと答えてください。")
    print "NAO：　'" + Fore.BLUE +"食事は作りますか。はいかいいえと答えてください。" + "'"
    print Style.RESET_ALL
    speech = stt.listen()
    if (
    ("はい" in speech) or
    ("はーい" in speech) or
    ("作ります" in speech) or
    ("作ってます" in speech) or
    ("作っています" in speech)
    ):
        tts.say("どんな料理が得意ですか")
        print "NAO：　'" + Fore.BLUE +"どんな料理が得意ですか" + "'"
        print Style.RESET_ALL
        stt.listen()
        if speech:
            tts.say("美味しそうですね。\\pau=500\\ 食事は誰としますか")
            print "NAO：　'" + Fore.BLUE +"美味しそうですね。食事は誰としますか" + "'"
            print Style.RESET_ALL
            speech = stt.listen()
            if ("一人" in speech
            ):
                tts.say("なるほど。\\pau=500\\ いつか私と食べてみますか")
                print "NAO：　'" + Fore.BLUE +"なるほど。いつか私と食べてみますか" + "'"
                print Style.RESET_ALL
                time.sleep(2)
            else:
                tts.say("いいですね")
                print "NAO：　'" + Fore.BLUE +"いいですね" + "'"
                print Style.RESET_ALL
                time.sleep(2)
    elif (
        ("いいえ" in speech) or
        ("いいね" in speech) or
        ("家" in speech) or
        ("あまり" in speech)
        ):
        tts.say("そうですか。\\pau=1000\\　いつか私と食べてみますか")
        print "NAO：　'" + Fore.BLUE +"そうですか。いつか私と食べてみますか" + "'"
        print Style.RESET_ALL
        time.sleep(2)

#==========
def shumi():
    tts.say("趣味はありますか \\pau=500\\ どんなことやっていますか")
    print "NAO：　'" + Fore.BLUE +"趣味はありますか。どんなことやっていますか" + "'"
    print Style.RESET_ALL
    speech = stt.listen()
    #stt.listen()
    if speech:
        tts.say("楽しそうですね。\\pau=500\\ どのぐらい続けてますか")
        print "NAO：　'" + Fore.BLUE +"楽しそうですね。どのぐらい続けてますか" + "'"
        print Style.RESET_ALL
        stt.listen()
        if speech:
            tts.say("私もしてみたいです")
            print "NAO：　'" + Fore.BLUE +"私もしてみたいです" + "'"
            print Style.RESET_ALL
            time.sleep(2)

#==========
def kaimono():
    tts.say("どこへ買い物に行きますか？")
    print "NAO：　'" + Fore.BLUE +"どこへ買い物に行きますか？" + "'"
    print Style.RESET_ALL
    speech = stt.listen()
    if speech:
        tts.say("誰と行きますか？")
        print "NAO：　'" + Fore.BLUE +"誰と行きますか？" + "'"
        print Style.RESET_ALL
        stt.listen()
        if speech:
            tts.say("私も \\pau=200\\ 一緒にいきたいです！")
            print "NAO：　'" + Fore.BLUE +"私も 一緒にいきたいです！" + "'"
            print Style.RESET_ALL
            time.sleep(2)

#==========
#music
#files are on nao using choreographe - need directory
# problem is cannot ssh to nao without password.
music_selection = [
"./dvorjak_out.mp3",
"./joplin_out.mp3",
"./gershwin_out.mp3",
"./elgar_out.mp3"
]

def playMusic():
    chosenMusic = random.choice(music_selection)
    nao.playOnNao(chosenMusic)


#==========
if __name__ == "__main__":
    while True:
        init()
        main()
        tts.setParameter("speed", 100)
        calib = stt.calibrate()
        lights.rotateEyes(0x000000FF, 0.5, 1)
        nao.go_to_posture("StandInit")
        time.sleep(2)
        motionProxy.setBreathEnabled('Body', True)
        startUP()
        while generalListen() != 0:
                generalListen()
