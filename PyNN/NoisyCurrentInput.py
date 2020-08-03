"""
Simple test of injecting noisy current into a cell

"""
import sys
from pyNN.utility import get_script_args, normalized_filename

simulator_name = get_script_args(1)[0]

print("Running example with NoisyCurrentSource using simulator: %s"%simulator_name)

exec("from pyNN.%s import *" % simulator_name)

setup()

filename = normalized_filename("Results", "NoisyCurrentInput", "pkl", simulator_name)

cells = Population(4, IF_curr_exp(v_thresh=-55.0, tau_refrac=5.0))

mean=0.55
stdev=0.1
start=50.0
stop=450.0
noise_dt = [0,1,5,10]

steady = DCSource(amplitude=mean, start=start, stop=stop)
cells[0].inject(steady)

noise1 = NoisyCurrentSource(mean=mean, stdev=stdev, start=start, stop=stop, dt=noise_dt[1])
cells[1].inject(noise1)
noise1.record()

noise2 = NoisyCurrentSource(mean=mean, stdev=stdev, start=start, stop=stop, dt=noise_dt[2])
cells[2].inject(noise2)
noise2.record()

noise3 = NoisyCurrentSource(mean=mean, stdev=stdev, start=start, stop=stop, dt=noise_dt[3])
cells[3].inject(noise3)
noise3.record()

record('v', cells, filename, annotations={'script_name': __file__})

run(500.0)

figure_option = '--plot-figure'

print("Finished")

if figure_option in sys.argv:
    
    print("Plotting...")
    import matplotlib.pyplot as plt
    plt.ion()
    vms = cells.get_data().segments[0].filter(name="v")[0]
    #print(vms, len(vms))
    #print(vms.times, len(vms.times))
    i=0
    for vm in vms.T:
        plt.plot(vms.times, vm, label='Noise dt: %sms'%noise_dt[i] if i!=0 else 'No noise')
        i+=1
    plt.xlabel("time (ms)")
    plt.ylabel("Vm (mV)")
    plt.legend()
    
    plt.figure()
    
    noises = {}
    noises[noise1]='dt: %sms'%noise_dt[1]
    noises[noise2]='dt: %sms'%noise_dt[2]
    noises[noise3]='dt: %sms'%noise_dt[3]
    
    for n in noises:
        plt.plot(vms.times, n.get_data(),label=noises[n])
    
    plt.legend()

    plt.show()
else:
    print('Finished simulation in simulator: %s. To plot the results, run with: %s'%(simulator_name, figure_option))
    
end()
