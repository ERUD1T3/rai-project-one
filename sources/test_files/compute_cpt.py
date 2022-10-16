# read samples and compute probabilities
from get_probs import read_from_csv, generate_cpts
import os
import pomegranate as pg

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
    z_cpts, a_cpts = generate_cpts(samples)

    # print the cpts
    print("z_cpts: {}".format(z_cpts))
    print("a_cpts: {}".format(a_cpts))

    # write the z_cpts to a file
    with open('../../data/cpts/z_cpts.txt', 'w') as f:
        # write the cpts key and values
        for cpt in z_cpts:
            f.write("{}: {}\n".format(cpt, z_cpts[cpt]))

    # write the a_cpts to a file
    with open('../../data/cpts/a_cpts.txt', 'w') as f:
        # write the lines and their probabilities
        for cpt in a_cpts:
            f.write("{}: {}\n".format(cpt, a_cpts[cpt]))


    # create the model
    model = pg.BayesianNetwork("Door Model")


    z_nodes = []
    a_nodes = []

    # create the nodes
    for cpt in z_cpts:
        # create the node
        z_node = pg.Node(
            pg.DiscreteDistribution({
                'z{}=True'.format(cpt[1]): z_cpts[cpt],
                'z{}=False'.format(cpt[1]): 1 - z_cpts[cpt]
                })
            )

    # add cpt actions
    for cpt in a_cpts:
        # create the node
        a_node = pg.Node(
            pg.DiscreteDistribution({
                'a{}=True'.format(cpt[1]): a_cpts[cpt],
                'a{}=False'.format(cpt[1]): 1 - a_cpts[cpt]
                })
            )
        # add the node to the list
        z_nodes.append(z_node)
   
    # door nodes
    # door = pg.Node(
    #     pg.DiscreteDistribution({


        

if __name__ == '__main__':
    main()