# read measurements from the robot and print them to the console
# -*- encoding: UTF-8 -*-
# Before running this command please check your PYTHONPATH is set correctly to the folder of your pynaoqi sdk.
from naoqi import ALProxy 
from nao_conf import *

# Set the IP address of your NAO.
ip = IP

# Connect to ALSonar module.
sonarProxy = ALProxy("ALSonar", ip, 9559)

# Subscribe to sonars, this will launch sonars (at hardware level) and start data acquisition.
sonarProxy.subscribe("myApplication")

#Now you can retrieve sonar data from ALMemory.
memoryProxy = ALProxy("ALMemory", ip, 9559)

def read_sonar(n_samples = 20, n_cleanups=1):
    '''Read sonar values print them to the console.'''

    left_sonar_echos = [
        "Device/SubDeviceList/US/Left/Sensor/Value",
        # "Device/SubDeviceList/US/Left/Sensor/Value1",
        # "Device/SubDeviceList/US/Left/Sensor/Value2",
        # "Device/SubDeviceList/US/Left/Sensor/Value3",
        # "Device/SubDeviceList/US/Left/Sensor/Value4",
        # "Device/SubDeviceList/US/Left/Sensor/Value5",
        # "Device/SubDeviceList/US/Left/Sensor/Value6",
        # "Device/SubDeviceList/US/Left/Sensor/Value7",
        # "Device/SubDeviceList/US/Left/Sensor/Value8",
        # "Device/SubDeviceList/US/Left/Sensor/Value9",
    ]

    right_sonar_echos = [
        "Device/SubDeviceList/US/Right/Sensor/Value",
        # "Device/SubDeviceList/US/Right/Sensor/Value1",
        # "Device/SubDeviceList/US/Right/Sensor/Value2",
        # "Device/SubDeviceList/US/Right/Sensor/Value3",
        # "Device/SubDeviceList/US/Right/Sensor/Value4",
        # "Device/SubDeviceList/US/Right/Sensor/Value5",
        # "Device/SubDeviceList/US/Right/Sensor/Value6",
        # "Device/SubDeviceList/US/Right/Sensor/Value7",
        # "Device/SubDeviceList/US/Right/Sensor/Value8",
        # "Device/SubDeviceList/US/Right/Sensor/Value9",
    ]

    left_sonar_values = []
    right_sonar_values = []

    # read n samples
    for _ in range(n_samples):
        # read raw sonar values
        left_sonar_values.append(memoryProxy.getData(left_sonar_echos[0]))
        right_sonar_values.append(memoryProxy.getData(right_sonar_echos[0]))

    # remove outliers 
    # for _ in range(n_cleanups):
    #     # find mean of all sonar echos for left and right
    #     left_sonar_mean = sum(left_sonar_values) / len(left_sonar_values)
    #     right_sonar_mean = sum(right_sonar_values) / len(right_sonar_values)
    #     # find standard deviation of all sonar echos for left and right
    #     left_sonar_std = (sum([(value - left_sonar_mean) ** 2 for value in left_sonar_values]) / len(left_sonar_values)) ** 0.5
    #     right_sonar_std = (sum([(value - right_sonar_mean) ** 2 for value in right_sonar_values]) / len(right_sonar_values)) ** 0.5
    #     # remove outliers
    #     left_sonar_values = [value for value in left_sonar_values if abs(value - left_sonar_mean) < left_sonar_std]
    #     right_sonar_values = [value for value in right_sonar_values if abs(value - right_sonar_mean) < right_sonar_std]

    # calculate mean of all sonar echos for left and right
    left_sonar_mean = sum(left_sonar_values) / len(left_sonar_values)
    right_sonar_mean = sum(right_sonar_values) / len(right_sonar_values)

    # print sonar values
    # print("Left:", left_sonar_mean)
    # print("Right:", right_sonar_mean, "\n")
    
    return (left_sonar_mean + right_sonar_mean) / 2.0


# def plot_sonar():
#     '''Plot sonar values in a graph.'''

#     fig = plt.figure()
#     ax1 = fig.add_subplot(1,1,1)

#     def animate(i):
#         left_sonar_mean, right_sonar_mean = read_sonar()
#         ax1.clear()
#         ax1.plot([left_sonar_mean, right_sonar_mean])
#         ax1.set_ylim([0, 1.5])

#     ani = animation.FuncAnimation(fig, animate, interval=1000)
#     plt.show()

# def write_csv(data, path):
#     '''Write sonar, imu, data to csv values to a csv file.
#     data: list of tuples (
#         timestep, distance along wall, 
#         left sonar, right sonar, rotation angle, 
#         measured x, measured y, measured theta)
#     path: path to csv file
#     '''

#     with open(path, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',')
#         writer.writerow(['t', 'y', 'x', 'r_x', 'r_y'])
#         for row in data:
#             writer.writerow(row)


# def gather_date():
#     '''Gather sonar, imu, data to csv values to a csv file.'''
#     pass


# while True:
#     # Get sonar left first echo (distance in meters to the first obstacle).
#     sonar_reading = read_sonar(n_samples=20)
#     # print sonar values
#     print("Sonar reading:", sonar_reading, "\n")

