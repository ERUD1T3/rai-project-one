import config
import time
import math
import almath

try:
    import pylab as pyl
    HAS_PYLAB = True
except ImportError:
    print "Matplotlib not found. this example will not plot data"
    HAS_PYLAB = False


def main():
    ''' robot Position: Small example to know how to deal
                        with robotPosition and getFootSteps
    '''
    motionProxy = config.loadProxy("ALMotion")


        # Set NAO in stiffness On
    config.StiffnessOn(motionProxy)
    config.PoseInit(motionProxy, 0.2)

    # Initialize the walk
    motionProxy.walkInit()

    # First call of walk API
    # with post prefix to not be bloquing here.
    motionProxy.post.walkTo(0.3, 0.0, 0.5)

    # wait that the walk process start running
    time.sleep(0.1)

    # get robotPosition and nextRobotPosition
    robotPosition     = almath.Pose2D(almath.vectorFloat(motionProxy.getRobotPosition(False)))
    nextRobotPosition = almath.Pose2D(almath.vectorFloat(motionProxy.getNextRobotPosition(False)))

    # get the first foot steps vector
    # (footPosition, unChangeable and changeable steps)
    footSteps1 = motionProxy.getFootSteps()

    # Second call of walk API
    motionProxy.post.walkTo(0.3, 0.0, -0.5)

    # get the second foot steps vector
    footSteps2 = motionProxy.getFootSteps()

    # here we wait until the walk process is over
    motionProxy.waitUntilWalkIsFinished()
    # then we get the final robot position
    robotPositionFinal = almath.Pose2D(almath.vectorFloat(motionProxy.getRobotPosition(False)))

    # compute robot Move with the second call of walk API
    # so between nextRobotPosition and robotPositionFinal
    robotMove = almath.pose2DInverse(nextRobotPosition)*robotPositionFinal
    print "Robot Move :", robotMove

    if (HAS_PYLAB):
        #################
        # Plot the data #
        #################
        pyl.figure()
        printRobotPosition(robotPosition, 'black')
        printRobotPosition(nextRobotPosition, 'blue')
        printFootSteps(footSteps1, 'green', 'red')

        pyl.figure()
        printRobotPosition(robotPosition, 'black')
        printRobotPosition(nextRobotPosition, 'blue')
        printFootSteps(footSteps2, 'blue', 'orange')

        pyl.show()