# read samples and compute probabilities
from get_probs import read_from_csv, generate_cpts
import os

def main():

    # read all files in the directory
    files = os.listdir('../../data/csvs')
    print(files)
    # read the data from the csv file
    samples = []
    for file in files:
        # read the data
        time_arr, z_array, a_array = read_from_csv('../../data/csvs/' + file)
        # append the data to the samples
        samples.append([time_arr, z_array, a_array])
    
    print(len(samples))
    print(len(samples[0]))
    print(len(samples[0][0]))
    print(samples[0][0][0])

    # generate cpts
    cpts = generate_cpts(samples)

    # print the cpts
    print(cpts)


if __name__ == '__main__':
    main()