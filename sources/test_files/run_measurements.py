from matplotlib.figure import figaspect
import almath as m # python's wrapping of almath
import sys
import time
from naoqi import ALProxy
from nao_conf import *
import matplotlib.pyplot as plt
from rai_sonar import read_sonar, savitzky_golay
import csv
import numpy as np



def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def write_to_csv(time_arr, z_array, a_array):
    '''
    Write the data to a csv file
    '''
    filename = '../../data/sonar_data_{}.csv'.format(time.time())
    with open(filename, 'w') as csvfile:
        # write the header
        fieldnames = ['t', 'z', 'a']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # write the data
        for i in range(len(time_arr)):
            writer.writerow({
                't': time_arr[i], 
                'z': z_array[i], 
                'a': a_array[i], 
            })
        


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
    # wTheta = 0
    x_array = []
    z_array = []
    time_arr = []
    a_array = []
    # action_bool_list = []
    treshhold = .5


    # minimum distance to the wall
    min_dist = treshhold - .2
    # maximum distance to the wall
    max_dist = treshhold + .2 

    time_start = time.time()
    time_now = 0
    
    # 20 second window
    while time_now < 30:
        #action_bool_sublist
        #print(time_now)
        
        #read sonar
        sonar_readings = read_sonar(20)
        time_now = time.time() - time_start
        time_arr.append(time_now)
        # print(sonar_readings)
        x_array.append(sonar_readings)

        filtered_y = savitzky_golay(np.array(x_array), window_size=31, order=4)
        sonar_readings = filtered_y[-1]

        if sonar_readings < .5:
            z_array.append(True)
        else:
            z_array.append(False)

        # 

        print(sonar_readings)
        if sonar_readings < min_dist:
            # move away from the wall
            # motionProxy.post.move(0, 0.1, 0)
            #motionProxy.post.move(-.2, 0, wTheta)
            a_array.append(True)
            motionProxy.post.move(0, .1, 0)
            motionProxy.post.move(-0.1, 0, 0)
            time.sleep(0.05)
        elif sonar_readings > max_dist:
            # move towards the wall
            # motionProxy.post.move(0, -0.1, 0)
            #motionProxy.post.move(.2, 0, wTheta)
            a_array.append(True)
            motionProxy.post.move(0, .1, 0)
            motionProxy.post.move(0.2, 0, 0)
            time.sleep(0.05)
        else:
            # stay put
            a_array.append(False)
            motionProxy.post.move(0, 0.1, 0)
            time.sleep(0.05)

        # wait is useful because with post moveTo is not blocking function
        #motionProxy.waitUntilMoveIsFinished()
        # get robot position after move
        endRobotPosition = m.Pose2D(motionProxy.getRobotPosition(False))
        robotMove = m.pose2DInverse(initRobotPosition)*endRobotPosition

        #print("Robot Move :", robotMove)
        # r_x_array.append(robotMove.x)
        # r_y_array.append(robotMove.y)

    motionProxy.post.stopMove()

    # write the data to a csv file
    filtered_y = savitzky_golay(np.array(x_array), window_size=31, order=4)
    write_to_csv(time_arr, z_array, a_array)

    # plot the sonar readings, and the robot's position in subplot
    fig, ax1 = plt.subplots()
    ax1.plot(time_arr, filtered_y)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('sonar readings', color='b')
    ax1.tick_params('y', colors='b')

    # plot the robot's position y with respect to x in subplot
    # ax2 = ax1.twinx()
    # ax2.plot(r_x_array, r_y_array, 'r-')
    # ax2.set_ylabel('robot position', color='r')
    # ax2.tick_params('y', colors='r')



    
    fig.tight_layout()
    fig.savefig('../../data/plots/plot_{}.png'.format(time.time()))

    # save plot
    fig.savefig('../../data/plots/sonar_data_{}.png'.format(time.time()))

    # plt.plot(time_arr, x_array)
    # plt.plot(time_arr, r_x_array)
    # plt.plot(time_arr, r_y_array)
    # plt.show() 
    # print(action_bool_list)
    # print(len(action_bool_list))
if __name__ == "__main__":
    robotIp = "127.0.0.1"

    if len(sys.argv) <= 1:
        print("Usage python motion_moveTo.py robotIP (optional default: 127.0.0.1)")
    else:
        robotIp = sys.argv[1]

    main(IP)