from neuromllite import Network, Cell, InputSource, Population, Synapse, RectangularRegion, RandomLayout 
from neuromllite import Projection, RandomConnectivity, Input, Simulation
import sys

################################################################################
###   Build new network

net = Network(id='NoisyExample')
net.notes = 'Example with NoisyCurrentSource'
net.parameters = { 'input_amp':       0.9} 

cell = Cell(id='testcell', pynn_cell='IF_cond_alpha')
cell.parameters = { "tau_refrac":5, "i_offset":0 }
net.cells.append(cell)


input_source1 = InputSource(id='i_clamp', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':'input_amp', 'start':200., 'stop':800.})
                           
net.input_sources.append(input_source1)

input_source2 = InputSource(id='noisyCurrentSource0', 
                           lems_source_file='TestNCS.xml', 
                           parameters={'mean':'0.5nA'})
                           
net.input_sources.append(input_source2)

r1 = RectangularRegion(id='region1', x=0,y=0,z=0,width=1000,height=100,depth=1000)
net.regions.append(r1)

p0 = Population(id='pop0', size=1, component=cell.id, properties={'color':'1 0 0'},random_layout = RandomLayout(region=r1.id))
p1 = Population(id='pop1', size=3, component=cell.id, properties={'color':'0 1 0'},random_layout = RandomLayout(region=r1.id))

net.populations.append(p0)
net.populations.append(p1)


net.inputs.append(Input(id='stim0',
                        input_source=input_source1.id,
                        population=p0.id,
                        percentage=100))
                        
net.inputs.append(Input(id='stim1',
                        input_source=input_source2.id,
                        population=p1.id,
                        percentage=100))

print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='SimNoisyExample',
                 network=new_file,
                 duration='1000',
                 dt='0.01',
                 seed=1234,
                 recordTraces={'all':'*'},
                 recordSpikes={'all':'*'})
                 
sim.to_json_file()



################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)

