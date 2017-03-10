
import numpy as np

files = ['regular.spikes','random.spikes','poisson.spikes','pynn.spikes']

tstop = 10000.0
expected_avg_rate = 50

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
    
    avg_rate = 1000/(tstop/len(spikes))
    print("Num spikes: %s; avg rate: %s Hz; avg isi: %s ms; std isi: %s ms"%(len(spikes),avg_rate,np.average(isis),np.std(isis)))
    assert abs(avg_rate-expected_avg_rate) < 1