from __future__ import print_function
import numpy as np
import sys

files = ['regularF.spikes','randomF.spikes','poissonF.spikes','refpoissonF.spikes','pynnF.spikes','poisF.syn.spikes','transF.pois.syn.spikes']

tstop = 10000.0
expected_avg_rate = 10000
expected_std_isi = 0.1

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
            print('     Observed avg rate: %s, expected: %s'%(avg_rate,expected_avg_rate))
            assert abs(avg_rate-expected_avg_rate) <= 40
            if ('pois' in fn and not 'ref' in fn) or 'pynn' in fn:
                print('     Observed std isi: %s, expected: %s'%(std_isi,expected_std_isi))
                assert abs(std_isi-expected_std_isi) <= 0.005
                
if not '-info' in sys.argv:      
    print("********************************\n*\n* All passed with inputs of %sHz!\n*\n********************************"%expected_avg_rate)
        
