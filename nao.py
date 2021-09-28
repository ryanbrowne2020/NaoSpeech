# -*- encoding: UTF-8 -*-

import argparse
import time
import math
from naoqi import ALBroker, ALModule, ALProxy

nao = None
FRAME_TORSO = 0
FRAME_ROBOT = 2


class Nao(ALModule):
    """Basic class for interaction to NAO Robot"""

    def __init__(self, ip, port, name="nao"):
        self.my_broker = ALBroker(
            "myBroker",
            "0.0.0.0",  # listen to anyone
            0,  # find a free port and use it
            ip,  # parent broker IP
            port)  # parent broker port
        ALModule.__init__(self, name)
        self.name = name
        self.hand_full_threshold = 0.20
        self.tts = ALProxy("ALTextToSpeech")
        self.memory_service = ALProxy("ALMemory")
        self.motionProxy = ALProxy("ALMotion")
    	self.audio = ALProxy("ALAudioDevice")
    	self.aup = ALProxy("ALAudioPlayer")
        self.not_touched = True
        self.not_detected = True

    def playOnNao(self, AudioName):
    	global tts, audio, aup
    	record_path = AudioName
    	fileID = self.aup.playFile(record_path, 0.7, 0)

    def get_posture(self):
        """Get current NAO posture"""
        posture_service = ALProxy("ALRobotPosture")
        posture = posture_service.getPostureFamily()
        print posture
        return posture

    def go_to_posture(self, posture_name):
        """Make NAO assume a desired posture"""
        posture_service = ALProxy("ALRobotPosture")
        result = posture_service.goToPosture(posture_name, 0.5)
        return result

    def nod(self): #not working
        self.motionProxy.setStiffnesses("Head", 1.0)
        names            = "HeadPitch"
        angles           = 0.52
        fractionMaxSpeed = 0.5
        self.motionProxy.setAngles(names,angles,fractionMaxSpeed)
        time.sleep(0.2)
        self.motionProxy.setStiffnesses("Head", 0.0)
        #go back
        angles           = 0.00
        self.motionProxy.setAngles(names,angles,fractionMaxSpeed)
        self.motionProxy.setStiffnesses("Head", 0.0)


# Callback

    def hand_touched(self, event_name, value):
        """Callback method for HandRightBackTouched event"""
        print "Event raised: " + event_name + " " + str(value)
        self.memory_service.unsubscribeToEvent("HandRightBackTouched",
                                               self.name)
        self.not_touched = False

    def disconnect(self):
        self.my_broker.shutdown()
        print "Disconnecting...."


def main():
    """A simple main"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="monami03.local",
                        help="Robot IP address. On robot or Local Naoqi: use '192.168.11.3'.")
    parser.add_argument(
        "--port", type=int, default=9559, help="Naoqi port number")
    args = parser.parse_args()
    global nao
    nao = Nao(args.ip, args.port)
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print
        print "Interrupted by user"
        print "Stopping..."
    finally:
        nao.disconnect()


if __name__ == "__main__":
    main()
