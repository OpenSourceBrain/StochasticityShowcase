set -e


### Test 50Hz inputs on jNeuroML

jnml LEMS_Inputs.xml -nogui

python spikes.py

rm *spikes


### Test 50Hz inputs on jNeuroML_NEURON 

jnml LEMS_Inputs.xml -neuron -run -nogui

python spikes.py jNeuroML_NEURON

rm *spikes


### Test 10000Hz inputs on jNeuroML

jnml LEMS_InputsFast.xml -nogui

python spikesFast.py

rm *spikes

### Test 10000Hz inputs on jNeuroML_NEURON 

jnml LEMS_InputsFast.xml -neuron -run -nogui

python spikesFast.py jNeuroML_NEURON