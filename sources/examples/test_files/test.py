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
#postureProxy.goToPosture("Crouch", 0.8)

try:
    motionProxy = ALProxy("ALMotion", IP, 9559)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e

# We use the "Body" name to signify the collection of all joints
pNames = "Body"
pStiffnessLists = 0
pTimeLists = 1
motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)