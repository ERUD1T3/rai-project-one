#!/usr/bin/python
import naoqi
from nao_conf import *
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", IP, 9559)
tts.say("Hi! Look at how pretty I am!")