set -e

jnml LEMS_Inputs.xml -nogui

python spikes.py

rm *spikes

jnml LEMS_Inputs.xml -neuron -run -nogui

python spikes.py jNeuroML_NEURON

#rm *spikes

