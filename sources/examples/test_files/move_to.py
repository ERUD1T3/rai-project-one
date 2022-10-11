import math
from turtle import distance
import almath as m # python's wrapping of almath
import sys
import time
from naoqi import ALProxy
from nao_conf import *
import matplotlib.pyplot as plt



def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def main(robotIP):
    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
        
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e


    # Set NAO in stiffness On
    StiffnessOn(motionProxy)
    sonarProxy = ALProxy("ALSonar", robotIP, 9559)
    sonarProxy.subscribe("myApplication")
    memoryProxy = ALProxy("ALMemory", robotIP, 9559)
    postureProxy = ALProxy("ALRobotPosture", IP, 9559)
    postureProxy.goToPosture("Stand", 0.8)

    #####################
    ## Enable arms control by move algorithm
    #####################
    motionProxy.setWalkArmsEnabled(True, True)
    #~ motionProxy.setWalkArmsEnabled(False, False)

    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",False]])
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    #####################
    ## get robot position before move
    #####################
    initRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))

    X = 0
    Y = 0.2
    Theta = 0
    left = []
    right = []
    time_arr = []
    time_start = time.time()
    time_now = 0

    #while memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value") > 0.1 and memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value") > 0.1:

    while time_now < 20:
        print(time_now)
        motionProxy.post.move(X, Y, Theta)
        time.sleep(0.25)
        #print("Left:",memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value"))
        left.append(memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value"))
        #print("Right:", memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value"), "\n")
        right.append(memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value"))
        time_now = time.time() - time_start
        time_arr.append(time_now)
        # wait is useful because with post moveTo is not blocking function
        #motionProxy.waitUntilMoveIsFinished()
    motionProxy.post.stopMove()

    #####################
    ## get robot position after move
    #####################
    endRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))

    #####################
    ## compute and print the robot motion
    #####################
    robotMove = m.pose2DInverse(initRobotPosition)*endRobotPosition
    print "Robot Move :", robotMove
    plt.plot(time_arr, right)
    plt.plot(time_arr, left)
    #plt.set_ylabel('Sonar Distance')
    #plt.set_xlabel('Distance Traveled')
    plt.legend()
    plt.show() 

if __name__ == "__main__":
    robotIp = "127.0.0.1"

    if len(sys.argv) <= 1:
        print "Usage python motion_moveTo.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(IP)