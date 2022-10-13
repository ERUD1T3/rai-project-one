# get probabilities of the sonar readings

import numpy as np
import matplotlib.pyplot as plt
import csv
import time

# read the data from the csv file
def read_from_csv():
    time_arr = []
    x_array = []
    r_x_array = []
    r_y_array = []
    with open('data.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            time_arr.append(float(row[0]))
            x_array.append(float(row[1]))
            r_x_array.append(float(row[2]))
            r_y_array.append(float(row[3]))
    return time_arr, x_array, r_x_array, r_y_array

# get the probabilities of the sonar readings
def get_bool(x_array, check_fn):
    # get the probabilities of the sonar readings based on the check function
    bools = []
    for x in x_array:
        bools.append(check_fn(x))
    return bools


# compute probability
def compute_prob(x_array):
    # computer probabilities based on count
    # get the number of times true appears in the array
    count = 0
    for x in x_array:
        if x:
            count += 1
    return count/len(x_array)


# generate cpts based on samples
def generate_cpts(samples, check_fn):
    # generate cpts based on samples
    # sample is 3D array
    # first dimension is the number of samples
    # second dimension is the number of time steps
    # third dimension is the number of variables
    # return cpts based on trues

    # get the number of samples
    num_samples = len(samples)
    # get the number of time steps
    num_time_steps = len(samples[0])
    # get the number of variables
    num_vars = len(samples[0][0])

    # find probabilities for each variable at the given time step
    cpts = {}

    # for each time step
    for t in range(num_time_steps):
        # for each variable
        for var in range(num_vars):
            # get the array of values for the variable at the given time step
            x_array = []
            for sample in samples:
                x_array.append(sample[t][var])
            # get the probabilities of the sonar readings based on the check function
            bools = get_bool(x_array, check_fn)
            # computer probabilities based on count
            prob = compute_prob(bools)
            # add the probability to the cpts
            cpts[(t, var)] = prob

    return cpts
        