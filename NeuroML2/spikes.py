
import numpy as np

files = ['regular.spikes','random.spikes','poisson.spikes']

tstop = 5000.0

for fn in files:
    f = open(fn)
    spikes = []
    isis = []
    lastSpike =None
    for line in f:
        words = line.split()
        if len(words)==2:
            t = float(words[1])*1000 # ms
            spikes.append(t)
            if lastSpike:
                isis.append(t-lastSpike)
            lastSpike = t
        
    print('\n--- Analysing: %s'%fn)
    #print(spikes)
    #print(isis)
    print("Num spikes: %s; avg rate: %s Hz; avg isi: %s ms; std isi: %s ms"%(len(spikes),1000/(tstop/len(spikes)),np.average(isis),np.std(isis)))