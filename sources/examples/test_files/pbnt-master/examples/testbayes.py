import sys
from numpy import *
sys.path.append('../lib')
from pbnt.Graph import *
from pbnt.Distribution import *
from pbnt.Node import *

def bayesnet():
    door = 0
    sensor = 1
    position = 2
    action = 3

    # sensor_2 = 4
    # position_2 = 5
    # action_2 = 6

    # sensor_3 = 7
    # position_3 = 8
    # action_3 = 9

    # sensor_4 = 10
    # position_4 = 11
    # action_4 = 12

    # sensor_5 = 13
    # position_5 = 14
    # action_5 = 15

    # sensor_6 = 16
    # position_6 = 17
    # action_6 = 18

    # sensor_7 = 19
    # position_7 = 20
    # action_7 = 21

    # sensor_8 = 22
    # position_8 = 23
    # action_8 = 24

    # sensor_9 = 25
    # position_9 = 26
    # action_9 = 27

    # sensor_10 = 28
    # position_10 = 29
    # action_10 = 30

    num_mesurements = 5
    sensor_nodes = []
    position_nodes = []
    action_nodes = []
    door_node = BayesNode(0, 2, name="door")
    counter = 1
    for i in range(num_mesurements):
        sensor_nodes.append(BayesNode(counter, name=("sensor_"+i))
        counter += 1
        position_nodes.append(BayesNode(counter, name=("position_"+i))
        counter += 1
        action_nodes.append(BayesNode(counter, name=("action_"+i)))
        counter += 1


    for node in range(num_mesurments):

        sensor_nodes[node].add_child(position_nodes[node])
        position_nodes[node].add_parent(sensor_nodes[node])

        position_nodes[node].add_child(action_node[node])
        action_node[node].add_parent(position_nodes[node])

        action_node[node].add_child(door_node)
        door_node.add_parent(action_node[node])

        if node < num_mesurements-1:
            action_node[node].add_child(position_nodes[node+1])

        if node >= 1:
            position_nodes[node].add_parent(action_node[node-1])
        

