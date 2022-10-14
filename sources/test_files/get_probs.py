# get probabilities of the sonar readings
import csv

# read the data from the csv file
def read_from_csv(path, n_samples=60):
    time_arr = []
    z_array = []
    a_array = []
    with open(path, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        # skip the first line
        next(plots)
        # read the data and stop at n_samples
        for row in plots:
            # print(row)
            
            # get the time
            time_arr.append(True if row[0] == 'True' else False)
            # get the sonar reading
            z_array.append(True if row[1] == 'True' else False)
            # get the sonar reading
            a_array.append(True if row[2] == 'True' else False)
            # check if we have read enough samples
            if len(time_arr) >= n_samples:
                break

    return time_arr, z_array, a_array

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
    count = 0.0
    for x in x_array:
        if x: count += 1
    return count/len(x_array)

# generate cpts based on samples
def generate_cpts(samples):
    # generate cpts based on samples
    # sample is 3D array
    # first dimension is the number of samples
    # second dimension is the number of time steps
    # third dimension is the number of variables
    # return cpts based on trues

    # get the number of samples
    num_samples = len(samples)
    print("number of samples: {}".format( num_samples))
    # get the number of time steps
    num_time_steps = len(samples[0][0])
    print("number of time steps: {}".format( num_time_steps))
    # get the number of variables
    num_vars = len(samples[0])
    print("number of variables: {}".format( num_vars))

    # find probabilities for each variable at the given time step
    z_cpts = {}
    a_cpts = {}

    # print the samples
    print(samples)

    # for each time step
    for t in range(num_time_steps):
        # for each variable skip the first one
        for var in range(1, num_vars):
            # get the array of values for the variable at the given time step
            x_array = []
            for sample in samples:
                # print length of sample
                # print(len(sample))
                # print(len(sample[0]))
                # print var and t
                # print("var: {}".format( var))
                # print("t: {}".format( t))
                # print sample at var and t
                # print("sample at {}{} =  {}".format(var, t, sample[var][t]))
                x_array.append(sample[var][t])
            # get the probabilities of the sonar readings based on the check function
            bools = x_array
            print(bools)
            # computer probabilities based on count
            prob = compute_prob(bools)
            # add the probability to the cpts
            if var == 1:
                z_cpts[('z', t)] = prob
                # print cpt with 3 decimal places
                print("cpt[('z', {})] = {:.3f}".format(t, prob))
                
            else:
                a_cpts[('a', t)] = prob
                # print cpt with 3 decimal places
                print("cpt[('a', {})] = {:.3f}".format(t, prob))

    return z_cpts, a_cpts





# generate cpts based on samples
def generate_cpts_comp(samples, check_fn):
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
        # for each variable skip the first one
        for var in range(1, num_vars):
            # get the array of values for the variable at the given time step
            x_array = []
            for sample in samples:
                x_array.append(sample[t][var])
            # get the probabilities of the sonar readings based on the check function
            bools = get_bool(x_array, check_fn)
            # computer probabilities based on count
            prob = compute_prob(bools)
            # add the probability to the cpts
            if var == 1:
                cpts[('z', t)] = prob
            else:
                cpts[('a', t)] = prob
            

    return cpts
        

