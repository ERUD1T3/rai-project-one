from matplotlib.figure import figaspect
import almath as m # python's wrapping of almath
import sys
import time
from naoqi import ALProxy
from nao_conf import *
import matplotlib.pyplot as plt
from rai_sonar import read_sonar
import csv

import numpy as np
from math import factorial




def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
   
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

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
    while time_now < 40:

        print(time_now)
        motionProxy.post.move(X, Y, Theta)
        #read sonar
        sonar_readings = read_sonar(20)
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

    # write the data to a csv file
    write_to_csv(time_arr, x_array, r_x_array, r_y_array)

    # plot the sonar readings, and the robot's position in subplot
    fig, ax1 = plt.subplots()
    ysg = savitzky_golay(np.array(x_array), window_size=31, order=4)

    ax1.plot(time_arr, ysg)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('sonar readings', color='b')
    ax1.tick_params('y', colors='b')

    # ax2 = ax1.twinx()
    # ax2.plot(time_arr, r_x_array, 'r-')
    # ax2.plot(time_arr, r_y_array, 'g-')
    # ax2.set_ylabel('robot position', color='r')
    # ax2.tick_params('y', colors='r')

    
    fig.tight_layout()
    fig.savefig('../../../data/plot_{}.png'.format(time.time()))

    # save plot
    fig.savefig('../../../data/sonar_data_{}.png'.format(time.time()))

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