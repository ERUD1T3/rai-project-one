from matplotlib.figure import figaspect
import almath as m # python's wrapping of almath
import sys
import time
from naoqi import ALProxy
from nao_conf import *
import matplotlib.pyplot as plt
from rai_sonar import read_sonar
import csv



def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def write_to_csv(time_arr, x_array, r_x_array, r_y_array):
    '''
    Write the data to a csv file
    '''
    filename = '../../../data/sonar_data_{}.csv'.format(time.time())
    with open(filename, 'w') as csvfile:
        # write the header
        fieldnames = ['time', 'sonar', 'robot_x', 'robot_y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # write the data
        for i in range(len(time_arr)):
            writer.writerow({
                'time': time_arr[i], 
                'sonar': x_array[i], 
                'robot_x': r_x_array[i], 
                'robot_y': r_y_array[i]})
        


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

    # vX = 0
    # vY = 0.1
    wTheta = 0
    x_array = []
    time_arr = []
    r_x_array = []
    r_y_array = []

    # minimum distance to the wall
    min_dist = .5
    # maximum distance to the wall
    max_dist = .8

    time_start = time.time()
    time_now = 0

    # 20 second window
    while time_now < 40:
        print(time_now)
        
        #read sonar
        sonar_readings = read_sonar(20)
        time_now = time.time() - time_start
        time_arr.append(time_now)
        # print(sonar_readings)
        x_array.append(sonar_readings)
        
        if sonar_readings < min_dist:
            # move away from the wall
            # motionProxy.post.move(0, 0.1, 0)
            motionProxy.post.move(-.1, .1, wTheta)
        elif sonar_readings > max_dist:
            # move towards the wall
            # motionProxy.post.move(0, -0.1, 0)
            motionProxy.post.move(.1, .1, wTheta)
        else:
            # stay put
            motionProxy.post.move(0, 0.1, wTheta)

        # wait is useful because with post moveTo is not blocking function
        #motionProxy.waitUntilMoveIsFinished()
        # get robot position after move
        endRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))
        robotMove = m.pose2DInverse(initRobotPosition)*endRobotPosition

        print("Robot Move :", robotMove)
        r_x_array.append(robotMove.x)
        r_y_array.append(robotMove.y)

    motionProxy.post.stopMove()

    # write the data to a csv file
    write_to_csv(time_arr, x_array, r_x_array, r_y_array)

    # plot the sonar readings, and the robot's position in subplot
    fig, ax1 = plt.subplots()
    ax1.plot(time_arr, x_array)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('sonar readings', color='b')
    ax1.tick_params('y', colors='b')

    # plot the robot's position y with respect to x in subplot
    ax2 = ax1.twinx()
    ax2.plot(r_x_array, r_y_array, 'r-')
    ax2.set_ylabel('robot position', color='r')
    ax2.tick_params('y', colors='r')



    
    fig.tight_layout()
    fig.savefig('../../../data/plot_{}.png'.format(time.time()))

    # save plot
    fig.savefig(f'../../../data/sonar_data_{time.time()}.png')

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