#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:54:28 2020

@author: beam
"""
import time
from datetime import datetime
import csv
from comm_unity import UnityCommunication



def simulatorComm():
    
    comm = UnityCommunication() # connect Unity Simulator
    
    return comm

def readConfig(configFlie):
    
    with open(configFlie) as f:
        # read the file and transfer str to dictionary
        configuration = eval(f.read())
            
    return configuration


def getGraph(comm):
    
    s, graph = comm.environment_graph()
    
    return graph

# def getSensorsState(sensorsList, graph):
#     sensorsState = []
    
def initializeState_dict(configuration):
    state_dict = {}
    for unit_init in configuration:
        # if the sensor is active, we write it in state_dict
        if configuration[unit_init]:
            # state_dict is like: {(unit key): ['present state', 'last state']}
            state_dict[unit_init] = ["init", "initbis"] 
        
    return state_dict

    
def writeState(state_dict, graph):
    for unit_key in state_dict:
        pre_id = unit_key[0]
        state = graph['nodes'][pre_id - 1]['states']
        
        # update the present state
        if len(unit_key) == 2: # if this object has only 1 state
            state_dict[unit_key][0] = state[0]
        elif unit_key[2] == 'door':          
            if state[0] == 'OPEN' or 'CLOSED':
                state_dict[unit_key][0] = state[0]
            else:
                state_dict[unit_key][0] = state[1]
        else: # if this is plug's state
            if state[1] == 'ON' or 'OFF':
                state_dict[unit_key][0] = state[1]
            else:
                state_dict[unit_key][0] = state[0]
                
        # check if the state has been changed        
        if state_dict[unit_key][0] != state_dict[unit_key][1]:
            # current date and time
            timestamp = time.time()
            dt_object = datetime.fromtimestamp(timestamp)
            with open('states.csv', mode='a') as states:
                state_writer = csv.writer(states, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                state_writer.writerow([dt_object.strftime('%x'), dt_object.strftime('%X'), pre_id, state_dict[unit_key][0]])
            #print(type(state_dict[unit][0]))
            state_dict[unit_key][1] = state_dict[unit_key][0] # update the last state
    


def main():
    
    comm = simulatorComm()
    
    configuration = readConfig("configuration.txt")
    
    state_dict = initializeState_dict(configuration)
    
    while True:
        
        graph = getGraph(comm)
        
        writeState(state_dict, graph)
        
        time.sleep(1)



if __name__ == "__main__":
    # execute only if run as a script
    main()