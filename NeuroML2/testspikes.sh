set -e

jnml LEMS_Inputs.xml -nogui

python spikes.py

jnml LEMS_Inputs.xml -neuron -run -nogui

#python spikes.py

