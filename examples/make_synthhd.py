from windfreak import SynthHD

synth = SynthHD('/dev/ttyACM0')
synth.init()

# Set channel 0 power and frequency
synth[0].power = -10.
synth[0].frequency = 2.e9

# Enable channel 0 output
synth[0].enable = True