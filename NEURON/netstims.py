# Based on https://www.neuron.yale.edu/phpBB/viewtopic.php?f=2&t=2750

from neuron import *
import numpy as np
import sys

rates = [100,1000,10000,100000]
duration = 10000
dt = 0.001

for r in rates: 

    print('Running simulation of %s with %s Hz input'%(duration, r))
    soma = h.Section()

    soma.push() 
    soma.insert("pas")

    syn = h.ExpSyn (0.5, sec = soma)  

    stimNc = h.NetStim()
    stimNc.noise = 1      
    stimNc.start = 0     
    stimNc.number = 1e9
    stimNc.interval = 1000./r

    vec_nc = h.Vector()


    nc = h.NetCon(stimNc, syn)
    nc.weight[0] = 10

    nc.record(vec_nc)

    vec = {}
    for var in 'v','t':
        vec[var] = h.Vector()

    # record the membrane potentials and
    # synaptic currents
    vec['v'].record(soma(0.5)._ref_v)
    vec ['t'].record(h._ref_t)

    # run the simulation
    h.load_file("stdrun.hoc")
    h.init()
    h.tstop = duration
    h.dt = dt
    h.run()

    spikes = []
    isis = []
    lastSpike =None
    for t in vec_nc:
        spikes.append(t)
        #print(t)
        if lastSpike:
            isis.append(t-lastSpike)
        lastSpike = t

    hz = 1000/(h.tstop/len(spikes))
    print("Num spikes: %s; avg rate: %s Hz; avg isi: %s ms; std isi: %s ms"%(len(spikes),hz,np.average(isis),np.std(isis)))
    assert abs((hz-r)/r)<0.01


    if not '-nogui' in sys.argv:
        import matplotlib.pyplot as plt
        # plot the results
        plt.figure()
        plt.plot(vec['t'],vec['v'])

if not '-nogui' in sys.argv:
    plt.show()

