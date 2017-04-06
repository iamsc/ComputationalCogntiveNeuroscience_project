#Setup the environment
import matplotlib.pyplot as plt
import random
import math
import nengo                
from nengo import spa

# Number of dimensions for the Semantic Pointers
dimensions = 16

# Make a model with the SPA network
model = spa.SPA(label='Task')
with model:
    # Creating a input and working memory element 
    model.iA = spa.State(dimensions=dimensions)
    model.iB = spa.State(dimensions=dimensions)
    model.iC = spa.State(dimensions=dimensions)
    model.pro = spa.State(dimensions=dimensions)
    model.state = spa.State(dimensions=dimensions)
    model.memory = spa.State(dimensions=dimensions, feedback=1)

    # Compare with the difference loadings of working memory. (more inputs)
    # model.iD = spa.State(dimensions=dimensions)
    # model.iE = spa.State(dimensions=dimensions)
    # model.iF = spa.State(dimensions=dimensions)
    
    
    
    # Specifying the action mappings
    actions = spa.Actions(
        'state = iA + iB + iC', # 3 inputs
        #'state = iA + iB + iC + iD', # 4 inputs
        #'state = iA + iB + iC + iD + iE', # 6 inputs
        'memory = state'
    )
    
    # Creating the cortical components
    model.cortical = spa.Cortical(actions=actions)
    
    # Stimulus dataset
    sequence = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    # the order of stimulus for each input
    test1 = [0, 2, 5, 3]
    test2 = [1, 3, 7, 1]
    test3 = [2, 1, 3, 5]
    test4 = [5, 4, 6, 3]
    test5 = [4, 5, 2, 7]
    test6 = [6, 0, 4, 2]
    test7 = [7, 0, 0, 4]
    ind = 0

    # Function that provides the model with an initial input semantic pointer.
    # input iA
    def start1(t):
        ind = test1[int(math.floor(t%4))]
        if math.floor((t*10)%10) < 3:
            return sequence[ind]
        else:
            return '0'
            
    # input iB
    def start2(t):
        ind = test2[int(math.floor(t%4))]
        if math.floor((t*10)%10) < 3:
            return sequence[ind]
        else:
            return '0'
    
    # input iC
    def start3(t):
        ind = test3[int(math.floor(t%4))]
        if math.floor((t*10)%10) < 3:
            return sequence[ind]
        else:
            return '0'
    
    # input iD
    def start4(t):
        ind = test4[int(math.floor(t%4))]
        if math.floor((t*10)%10) < 3:
            return sequence[ind]
        else:
            return '0'
            
    # input iE
    def start5(t):
        ind = test5[int(math.floor(t%4))]
        if math.floor((t*10)%10) < 3:
            return sequence[ind]
        else:
            return '0'
            
    # input iE
    def start6(t):
        ind = test6[int(math.floor(t%4))]
        if math.floor((t*10)%10) < 3:
            return sequence[ind]
        else:
            return '0'

    # probe
    def pro_stimuli(t):
        ind = test7[int(math.floor(t%4))]
        if (math.floor((t*10)%10) > 6) and (math.floor((t*10)%10) < 8):
            print(ind)
            return sequence[ind]
        elif math.floor((t*10)%10) >= 8:
            return '0'
        else:
            return '0'
        
    # Input
    model.input = spa.Input(iA=start1, iB=start2, iC=start3, pro=pro_stimuli)
    #model.input = spa.Input(iA=start1, iB=start2, iC=start3, iD=start4, pro=pro_stimuli)
    #model.input = spa.Input(iA=start1, iB=start2, iC=start3, iD=start4, iE=start5, pro=pro_stimuli)
    #model.input = spa.Input(iA=start1, iB=start2, iC=start3, iD=start4, iE=start5, iF=start6, pro=pro_stimuli)

import nengo_gui
nengo_gui.GUI(__file__).start()