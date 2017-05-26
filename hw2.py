#Setup the environment
import matplotlib.pyplot as plt
import random
import math
import nengo                
from nengo import spa

# Number of dimensions for the SPs
dimensions = 64

# Make a model object with the SPA network
model = spa.SPA(label='Task')

with model:
    # Initial the three visual perceptual memory component and one working memory component.
    model.vision1 = spa.State(dimensions=dimensions, neurons_per_dimension=100, feedback=0.7)
    model.vision2 = spa.State(dimensions=dimensions, neurons_per_dimension=100, feedback=0.7)
    model.cue = spa.Buffer(dimensions=dimensions, neurons_per_dimension=100)
    model.representation = spa.Memory(dimensions=dimensions, neurons_per_dimension=100)

    # Specify the action mapping and attention function
    actions = spa.Actions(
        'dot(cue, LEFT) --> vision1=vision1*2',
        'dot(cue, RIGHT) --> vision2=vision2*2',)
    cortical_actions = spa.Actions('representation=vision1+vision2',)
    model.bg = spa.BasalGanglia(actions=actions)
    model.thal = spa.Thalamus(model.bg)
    model.cortical = spa.Cortical(actions=cortical_actions)

# Stimulus dataset
# input visual1
def input_vision1(t):
    sequence = 'A 0 0 0 B 0 0 0 C 0 0 0 D 0 0 0'.split()
    index = int(t / 0.5) % len(sequence)
    return sequence[index]

# input visual2
def input_vision2(t):
    sequence = 'B 0 0 0 C 0 0 0 D 0 0 0 A 0 0 0'.split()
    index = int(t / 0.5) % len(sequence)
    return sequence[index]

# input cue
def input_cue(t):
    sequence = '0 LEFT 0 R 0 RIGHT 0 R 0 RIGHT 0 R 0 LEFT 0 R'.split()
    index = int(t / 0.5) % len(sequence)
    return sequence[index]

# Input the stimulus
with model:
    model.input = spa.Input(vision1=input_vision1, vision2=input_vision2, cue=input_cue)

with nengo.Simulator(model) as sim:
    sim.run(1)

import nengo_gui
nengo_gui.GUI(__file__).start()