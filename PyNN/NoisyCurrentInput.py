"""
Simple test of injecting noisy current into a cell

"""
import sys
from pyNN.utility import get_script_args, normalized_filename

simulator_name = get_script_args(1)[0]
exec("from pyNN.%s import *" % simulator_name)

setup()
cell = create(IF_curr_exp(v_thresh=-55.0, tau_refrac=5.0))

noise = NoisyCurrentSource(mean=0.5, stdev=0.1, start=50.0, stop=450.0, dt=1.0)
cell.inject(noise)

filename = normalized_filename("Results", "StepCurrentSource", "pkl", simulator_name)
record('v', cell, filename, annotations={'script_name': __file__})
run(500.0)

if not '-nogui' in sys.argv:
    
    import matplotlib.pyplot as plt
    plt.ion()
    data = cell.get_data()
    signal_names = [s.name for s in data.segments[0].analogsignalarrays]
    vm = data.segments[0].analogsignalarrays[signal_names.index('v')]
    plt.plot(vm.times, vm)
    plt.xlabel("time (ms)")
    plt.ylabel("Vm (mV)")

    plt.legend()

    plt.show()


end()
