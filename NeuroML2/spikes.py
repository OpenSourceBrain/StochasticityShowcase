
import numpy as np

files = ['regular.spikes','random.spikes','poisson.spikes','pynn.spikes','pois.syn.fire','trans.pois.syn.fire']

tstop = 20000.0
expected_avg_rate = 50
expected_std_isi = 20

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
    std_isi = np.std(isis)
    print("Num spikes: %s; avg rate: %s Hz; avg isi: %s ms; std isi: %s ms"%(len(spikes),avg_rate,np.average(isis),std_isi))
    assert abs(avg_rate-expected_avg_rate) <= 1
    if 'pois' in fn or 'pynn' in fn:
        assert abs(std_isi-expected_std_isi) <= 1
        