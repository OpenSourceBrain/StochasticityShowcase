from neuromllite import Network, Cell, InputSource, Population, Synapse
from neuromllite import Projection, RandomConnectivity, OneToOneConnector, Input, Simulation

from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite.sweep.ParameterSweep import *

import sys


def generate():
    ################################################################################
    ###   Build new network

    net = Network(id='RunStims')
    net.notes = 'Example with spike producers'

    net.parameters = { 'rate':       50}

    cell = Cell(id='ifcell', pynn_cell='IF_curr_alpha')



    ssp = Cell(id='ssp', pynn_cell='SpikeSourcePoisson')
    
    ssp.parameters = { 'rate':       'rate',
                             'start':      0,
                             'duration':   1e9}
                             
    net.cells.append(ssp)


    sspPop = Population(id='sspPop', size=1, component=ssp.id, properties={'color':'.5 0 0'})
    

    net.populations.append(sspPop)


    net.synapses.append(Synapse(id='ampa', 
                                pynn_receptor_type='excitatory', 
                                pynn_synapse_type='curr_alpha', 
                                parameters={'tau_syn':0.1}))
    net.synapses.append(Synapse(id='gaba', 
                                pynn_receptor_type='inhibitory', 
                                pynn_synapse_type='curr_alpha', 
                                parameters={'tau_syn':0.1}))


    #print(net)
    #print(net.to_json())
    new_file = net.to_json_file('%s.json'%net.id)


    ################################################################################
    ###   Build Simulation object & save as JSON

    sim = Simulation(id='SimTest',
                     network=new_file,
                     duration='10000',
                     dt='0.025',
                     seed= 123,
                     recordTraces={'xxx':'*'},
                     recordSpikes={'all':'*'})

    sim.to_json_file()
    
    return sim, net



if __name__ == "__main__":

    if '-sweep' in sys.argv:
        
        sim, net = generate()
        
        fixed = {'dt':0.025,'duration':10000}
 
        #
        vary = {'rate':[100,500,1000,5000,10000,20000,40000]}
        vary = {'rate':[100,500,1000,5000,10000]}
        
        vary['seed'] = [i for i in range(30)]
        vary['seed'] = [i for i in range(20)]

        simulator = 'jNeuroML'
        simulator = 'jNeuroML_NEURON'
        simulator = 'PyNN_NEST'
        simulator = 'jNeuroML_NetPyNE'
        simulator = 'jNeuroML'

        nmllr = NeuroMLliteRunner('SimTest.json',
                                  simulator=simulator)

        ps = ParameterSweep(nmllr, 
                            vary, 
                            fixed,
                            num_parallel_runs=16,
                            plot_all=True, 
                            heatmap_all=False,
                            show_plot_already=False,
                            peak_threshold=0)

        report = ps.run()
        ps.print_report()

        #  ps.plotLines('weightInput','average_last_1percent',save_figure_to='average_last_1percent.png')
        #ps.plotLines('weightInput','mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        #ps.plotLines('rate','sspPop[0]/spike:mean_spike_frequency',save_figure_to='mean_spike_frequency.png')
        ps.plotLines('rate','sspPop[0]/spike:mean_spike_frequency',second_param='seed',save_figure_to='mean_spike_frequency.png')

        import matplotlib.pyplot as plt

        plt.show()
    
    else:

        sim, net = generate()

        ################################################################################
        ###   Run in some simulators

        import sys

        check_to_generate_or_run(sys.argv, sim)

