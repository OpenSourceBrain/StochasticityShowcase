set -e

jnml LEMS_Inputs.xml -nogui

python spikes.py

rm *spikes

jnml LEMS_Inputs.xml -neuron -run -nogui

python spikes.py jNeuroML_NEURON

rm *spikes

jnml LEMS_InputsFast.xml -nogui

python spikesFast.py

rm *spikes

jnml LEMS_InputsFast.xml -neuron -run -nogui

python spikesFast.py jNeuroML_NEURON