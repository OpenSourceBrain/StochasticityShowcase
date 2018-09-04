from __future__ import print_function
import numpy as np
import sys

files = ['regular.spikes','random.spikes','poisson.spikes','refpoisson.spikes','pynn.spikes','pois.syn.spikes','trans.pois.syn.spikes']

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
    print("Num spikes: %s; avg rate: %s Hz"%(len(spikes),avg_rate), end="")
    if len(isis)>0:
        print("; avg isi: %s ms; std isi: %s ms; max: %s ms; min: %s ms"%(np.average(isis),std_isi, np.max(isis), np.min(isis)))
    if not '-info' in sys.argv:
        print("   Checking %s; check_syns: %s"%(fn,check_syns))
        if not 'syn' in fn or check_syns:
            assert abs(avg_rate-expected_avg_rate) <= 3
            if ('pois' in fn and not 'ref' in fn) or 'pynn' in fn:
                assert abs(std_isi-expected_std_isi) <= 1.6
                
if not '-info' in sys.argv:                
    print("********************************\n*\n* All passed with inputs of %sHz!\n*\n********************************"%expected_avg_rate)
        
