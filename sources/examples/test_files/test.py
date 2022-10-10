#!/usr/bin/python
import naoqi
from nao_conf import *
from naoqi import ALProxy
motionProxy = ALProxy("ALMotion", IP, 9559)
motionProxy.setSmartStiffnessEnabled(False)
tts = ALProxy("ALTextToSpeech", IP, 9559)
tts.say("Hi! Look at how pretty I am!")
postureProxy = ALProxy("ALRobotPosture", IP, 9559)
print(postureProxy.getPostureList())
#motionProxy = ALProxy("ALMotion", IP, 9559)
#motionProxy.setFallManagerEnabled(False)
postureProxy.goToPosture("LyingBelly", 0.2)