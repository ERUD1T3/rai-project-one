import almath as m # python's wrapping of almath
import sys
import time
from naoqi import ALProxy
from nao_conf import *
import matplotlib.pyplot as plt
from rai_sonar import read_sonar



def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def main(robotIP):
    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
        
    except Exception as e:
        print("Could not create proxy to ALMotion")
        print("Error was: ", e)


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

    # Fix head position
    motionProxy.setAngles("HeadYaw", 0, 0.6)
    motionProxy.setAngles("HeadPitch", 0, 0.6)

    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION",False]])
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    # position of the robot before the move
    initRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))

    X = 0
    Y = 0.1
    Theta = 0
    x_array = []
    time_arr = []
    r_x_array = []
    r_y_array = []

    time_start = time.time()
    time_now = 0

    # 20 second window
    while time_now < 50:


        print(time_now)
        motionProxy.post.move(X, Y, Theta)
        #read sonar
        sonar_readings = read_sonar()
        time_now = time.time() - time_start
        time_arr.append(time_now)
        # print(sonar_readings)
        x_array.append(sonar_readings)
        # wait is useful because with post moveTo is not blocking function
        #motionProxy.waitUntilMoveIsFinished()
        # get robot position after move
        endRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))
        robotMove = m.pose2DInverse(initRobotPosition)*endRobotPosition
        print("Robot Move :", robotMove)
        r_x_array.append(robotMove.x)
        r_y_array.append(robotMove.y)

    motionProxy.post.stopMove()

    # plot the sonar readings, and the robot's position in subplot
    fig, ax1 = plt.subplots()
    ax1.plot(time_arr, x_array)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('sonar readings', color='b')
    ax1.tick_params('y', colors='b')

    # ax2 = ax1.twinx()
    # ax2.plot(time_arr, r_x_array, 'r-')
    # ax2.plot(time_arr, r_y_array, 'g-')
    # ax2.set_ylabel('robot position', color='r')
    # ax2.tick_params('y', colors='r')

    fig.tight_layout()
    plt.show()

    # plt.plot(time_arr, x_array)
    # plt.plot(time_arr, r_x_array)
    # plt.plot(time_arr, r_y_array)
    # plt.show() 

if __name__ == "__main__":
    robotIp = "127.0.0.1"

    if len(sys.argv) <= 1:
        print("Usage python motion_moveTo.py robotIP (optional default: 127.0.0.1)")
    else:
        robotIp = sys.argv[1]

    main(IP)