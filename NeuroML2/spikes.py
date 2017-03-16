
import numpy as np
import sys

files = ['regular.spikes','random.spikes','poisson.spikes','pynn.spikes','pois.syn.fire','trans.pois.syn.fire']

tstop = 20000.0
expected_avg_rate = 50
expected_std_isi = 20

check_syns = True
if "jNeuroML_NEURON" in sys.argv:
    check_syns = False

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
    
    avg_rate = len(spikes)*1000.0/tstop
    std_isi = np.std(isis)
    print("Num spikes: %s; avg rate: %s Hz; avg isi: %s ms; std isi: %s ms"%(len(spikes),avg_rate,np.average(isis),std_isi))
    if not '-info' in sys.argv:
        print("   Checking %s; check_syns: %s"%(fn,check_syns))
        if not 'syn' in fn or check_syns:
            assert abs(avg_rate-expected_avg_rate) <= 3
            if 'pois' in fn or 'pynn' in fn:
                assert abs(std_isi-expected_std_isi) <= 3
        