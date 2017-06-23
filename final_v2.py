#Setup the environment
import matplotlib.pyplot as plt
import random
import math
import nengo                
from nengo import spa
import numpy as np
# Number of dimensions for the SPs
dimensions = 128

# Make a model object with the SPA network
model = spa.SPA(label='Task')

vocab = spa.Vocabulary(dimensions=dimensions)
#vocab.add('A', vocab.parse('1.2 * Areg'))
#vocab.add('E', vocab.parse('1.2 * Ereg'))
#vocab.add('I', vocab.parse('1.2 * Ireg'))
#vocab.add('O', vocab.parse('1.2 * Oreg'))
#vocab.add('U', vocab.parse('1.2 * Ureg'))

vocab.add('Bdecay', vocab.parse('0.8 * B'))
vocab.add('Cdecay', vocab.parse('0.8 * C'))
vocab.add('Ddecay', vocab.parse('0.8 * D'))
vocab.add('Fdecay', vocab.parse('0.8 * F'))
vocab.add('Gdecay', vocab.parse('0.8 * G'))

Threshold = 1.35

with model:
    # Initial the three visual perceptual memory component and one working memory component.
    model.vision1 = spa.State(dimensions=dimensions, neurons_per_dimension=100, feedback=0.7, vocab = vocab)
    model.vision2 = spa.State(dimensions=dimensions, neurons_per_dimension=100, feedback=0.7, vocab = vocab)
    model.cue = spa.State(dimensions=dimensions, neurons_per_dimension=100, feedback=0.7, vocab = vocab)
    model.target = spa.State(dimensions=dimensions, neurons_per_dimension=100, feedback=0.7, vocab = vocab)
    model.representation = spa.Memory(dimensions=dimensions, neurons_per_dimension=100, vocab = vocab)
    model.awake = spa.Memory(dimensions=dimensions, neurons_per_dimension=100, vocab = vocab)
    model.similar = spa.Compare(dimensions=dimensions, vocab = vocab)
    model.output = spa.Buffer(dimensions=dimensions, neurons_per_dimension=100)
    model.state = spa.Buffer(dimensions=dimensions, neurons_per_dimension=100)
    # Specify the action mapping and attention function
    actions = spa.Actions(
        #'dot(cue, LEFT) --> vision1=vision1*2',
        #'dot(cue, RIGHT) --> vision2=vision2*2',
        #'dot(cue, HIGH) --> output = LOW'
        #'dot(cue, LOW) --> output = LOW'
        'similar --> output = Match',
        '1.5 - similar --> output = NotMatch',
        '1.4 --> output = IDK',
        '3 * dot(state, Wait) --> output = IDK'
        )
    cortical_actions = spa.Actions(
        'representation=vision1 * L + vision2 * R',
        'awake=representation * ~cue',
        'similar_A = awake',
        'similar_B = target'
        )

    model.bg = spa.BasalGanglia(actions=actions)
    model.thal = spa.Thalamus(model.bg)
    model.cortical = spa.Cortical(actions=cortical_actions)

# Stimulus dataset
# input visual1
np.random.seed(0)
arr = np.arange(100)
np.random.shuffle(arr)

#threaten :A E I O U
#normal: B C D F G
Con1qASet = 'A C A B F'.split()
Con1qBSet = 'B I G U E'.split()
Con1cuSet = 'L R L R R'.split()
Con1tgSet = 'A I A U E' .split()
Con1random = np.arange(101)
np.random.shuffle(Con1random)

Con2qASet = 'B O E G G'.split()
Con2qBSet = 'A B F U I'.split()
Con2cuSet = 'R L L R R'.split()
Con2tgSet = 'C G F D D'.split()
Con2random = np.arange(101)
np.random.shuffle(Con2random)

Con3qASet = 'U C B F I'.split()
Con3qBSet = 'G A E O G'.split()
Con3cuSet = 'R L L L R'.split()
Con3tgSet = 'G C B F G'.split()
Con3random = np.arange(101)
np.random.shuffle(Con3random)

Con4qASet = 'I O C D B'.split()
Con4qBSet = 'F G E A I'.split()
Con4cuSet = 'R R L L L'.split()
Con4tgSet = 'C A D C U'.split()
Con4random = np.arange(101)
np.random.shuffle(Con4random)


simTime = 200

vision1List = ['a'] * (simTime / 2)
vision2List = ['a'] * (simTime / 2)
cueList = ['a'] * (simTime / 2)
targetList = ['a'] * (simTime / 2)
conditionList = [-1] * (simTime / 2)

def appendVision1List(t, char):
    print(t, char)
    vision1List.append(char)

def appendVision2List(t, char):
    print(t, char)
    vision2List.append(char)

def appendCueList(t, char):
    print(t, char)
    cueList.append(char)

def appendTargetList(t, char):
    print(t, char)
    targetList.append(char)

def appendConditionList(t, cond):
    print(t, cond)
    conditionList.append(cond)

def input_vision1(t):
    #sequence = 'A 0 0 0 B 0 0 0 C 0 0 0 D 0 0 0'.split()
    returnChar = ''

    index = np.floor(t / 0.5).astype('int')
    if index % 4 == 0:

        if arr[index / 4] % 4 == 0:
        #if (index / 4) % 2:
            returnChar = Con1qASet[Con1random[index / 4] % 5]

        elif arr[index / 4] % 4 == 1:
            returnChar = Con2qASet[Con2random[index / 4] % 5]

        elif arr[index / 4] % 4 == 2:
        #else:
            returnChar = Con3qASet[Con3random[index / 4] % 5]

        elif arr[index / 4] % 4 == 3:
            returnChar = Con4qASet[Con4random[index / 4] % 5]

        if t < simTime:
            listIndex = np.floor(t / 2).astype('int')   
        #try:
            vision1List[listIndex] = returnChar
        #except:
        #    print listIndex
            conditionList[listIndex] = arr[index / 4] % 4
        #if t * 1000 % 2000 == 100:
            #vision1List.append(returnChar)
        #    appendVision1List(t, returnChar)
            #conditionList.append(arr[index / 4] % 4)
        #    appendConditionList(t, arr[index / 4] % 4)

    else:
        returnChar = '0'

    if returnChar in ['B', 'C', 'D', 'F', 'G']:
        return returnChar+'decay'
    return returnChar


# input visual2
def input_vision2(t):

    returnChar = ''

    index = np.floor(t / 0.5).astype('int')
    if index % 4 == 0:
        if arr[index / 4] % 4 == 0:
        #if (index / 4) % 2:
            returnChar = Con1qBSet[Con1random[index / 4] % 5]

        elif arr[index / 4] % 4 == 1:
            returnChar = Con2qBSet[Con2random[index / 4] % 5]

        elif arr[index / 4] % 4 == 2:
        #else:
            returnChar = Con3qBSet[Con3random[index / 4] % 5]

        elif arr[index / 4] % 4 == 3:
            returnChar = Con4qBSet[Con4random[index / 4] % 5]

        if t < simTime:
            listIndex = np.floor(t / 2).astype('int')
            vision2List[listIndex] = returnChar
        #if t * 1000 % 2000 == 100:
        #    #vision2List.append(returnChar)
        #    appendVision2List(t, returnChar)

    else:
        returnChar = '0'

    if returnChar in ['B', 'C', 'D', 'F', 'G']:
        return returnChar+'decay'
    return returnChar

# input cue
def input_cue(t):
    returnChar = ''

    index = np.floor(t / 0.5).astype('int')
    if index % 4 == 1:
        if arr[index / 4] % 4 == 0:
        #if (index / 4) % 2:
            returnChar = Con1cuSet[Con1random[index / 4] % 5]

        elif arr[index / 4] % 4 == 1:
            returnChar = Con2cuSet[Con2random[index / 4] % 5]

        elif arr[index / 4] % 4 == 2:
        #else:
            returnChar = Con3cuSet[Con3random[index / 4] % 5]

        elif arr[index / 4] % 4 == 3:
            returnChar = Con4cuSet[Con4random[index / 4] % 5]

        #if t * 1000 % 2000 == 600:
        #    #cueList.append(returnChar)
        #    appendCueList(t, returnChar)
        if t < simTime:
            listIndex = np.floor(t / 2).astype('int')
            cueList[listIndex] = returnChar

    else:
        returnChar = '0'

    return returnChar

# input target
def input_target(t):
    returnChar = ''

    index = np.floor(t / 0.5).astype('int')
    if index % 4 == 2:
        if arr[index / 4] % 4 == 0:
        #if (index / 4) % 2:
            returnChar = Con1tgSet[Con1random[index / 4] % 5]

        elif arr[index / 4] % 4 == 1:
            returnChar = Con2tgSet[Con2random[index / 4] % 5]

        elif arr[index / 4] % 4 == 2:
        #else:
            returnChar = Con3tgSet[Con3random[index / 4] % 5]

        elif arr[index / 4] % 4 == 3:
            returnChar = Con4tgSet[Con4random[index / 4] % 5]

        #if t * 1000 % 2000 == 1100:
            #targetList.append(returnChar)
            #appendTargetList(t, returnChar)
        if t < simTime:
            listIndex = np.floor(t / 2).astype('int')
            targetList[listIndex] = returnChar

    else:
        returnChar = '0'
    
    return returnChar 

def input_state(t):
    index = np.floor(t / 0.5).astype('int')
    if index % 4 != 2:
        return 'Wait'
    else:
        return '0'

# Input the stimulus
with model:
    model.input = spa.Input(vision1=input_vision1, vision2=input_vision2, cue=input_cue, target=input_target, state=input_state)

with model:
    actions = nengo.Probe(model.thal.actions.output, synapse=0.01)
    utility = nengo.Probe(model.bg.input, synapse=0.01)
    

    vision1 = nengo.Probe(model.vision1.input, synapse=0.01)
    vision2 = nengo.Probe(model.vision2.input, synapse=0.01)
    cue = nengo.Probe(model.cue.input, synapse=0.01)
    target = nengo.Probe(model.target.input, synapse=0.01)
    #similar = nengo.Probe(model.similar.state.input, synapse = 0.01)



with nengo.Simulator(model) as sim:
    sim.run(simTime - 0.01)

#import nengo_gui
#nengo_gui.GUI(__file__).start()

#quit()

fig = plt.figure(figsize=(12,8))

p2 = fig.add_subplot(2,1,1)
p2.plot(sim.trange(), sim.data[actions])
p2_legend_txt = [a.effect for a in model.bg.actions.actions]
p2.legend(p2_legend_txt, fontsize='xx-small')
p2.set_ylabel('Action')

p3 = fig.add_subplot(2,1,2)
p3.plot(sim.trange(), sim.data[utility])
p3_legend_txt = [a.condition for a in model.bg.actions.actions]
p3.legend(p3_legend_txt, fontsize='xx-small')
p3.set_ylabel('Utility')

fig2 = plt.figure(figsize=(12, 8))

p1 = fig2.add_subplot(4,1,1)
p1.plot(sim.trange(), model.similarity(sim.data, vision1))
p1.legend(model.get_output_vocab('vision1').keys, fontsize='xx-small')
p1.set_ylabel('Vision1')

p4 = fig2.add_subplot(4,1,2)
p4.plot(sim.trange(), model.similarity(sim.data, vision2))
p4.legend(model.get_output_vocab('vision2').keys, fontsize='xx-small')
p4.set_ylabel('Vision2')

p5 = fig2.add_subplot(4,1,3)
p5.plot(sim.trange(), model.similarity(sim.data, cue))
p5.legend(model.get_output_vocab('cue').keys, fontsize='xx-small')
p5.set_ylabel('Cue')

p6 = fig2.add_subplot(4,1,4)
p6.plot(sim.trange(), model.similarity(sim.data, target))
p6.legend(model.get_output_vocab('target').keys, fontsize='xx-small')
p6.set_ylabel('Target')




plt.show()

print(sim.data[utility].shape)

print(vision1List)
print(vision2List)
print(cueList)
print(targetList)
print(conditionList)

OutputList = np.zeros((2, simTime / 2))
for i in range(simTime / 2):
    tmp = sim.data[utility][i * 2000 + 1000 : (i + 1) * 2000 - 500, 0]
    OutputList[0, i] = np.mean(tmp)
    tmp = sim.data[utility][i * 2000 + 1000 : (i + 1) * 2000 - 500, 1]
    OutputList[1, i] = np.mean(tmp)

print(OutputList)

ConPoint = np.zeros(4)

for i in range(simTime / 2):
    if cueList[i] == 'L': ##Cue = L
        if targetList[i] == vision1List[i]: ##Match
            if OutputList[0, i] > Threshold: ##answer Match
                ConPoint[conditionList[i]] = ConPoint[conditionList[i]] + 1
        elif targetList[i] != vision1List[i]: ##NotMatch
            if OutputList[1, i] > Threshold: ##answer NotMatch
                ConPoint[conditionList[i]] = ConPoint[conditionList[i]] + 1
    elif cueList[i] == 'R': ##Cue = R
        if targetList[i] == vision2List[i]: ##Match
            if OutputList[0, i] > Threshold: ##answer Match
                ConPoint[conditionList[i]] = ConPoint[conditionList[i]] + 1
        elif targetList[i] != vision2List[i]:
            if OutputList[1, i] > Threshold:
                ConPoint[conditionList[i]] = ConPoint[conditionList[i]] + 1

print(ConPoint)