from matplotlib import pyplot as plt
from scipy import signal as sg
import math, time

def oscillator(cycle_length, frequency=1, type='sin'):
    timecounter = 0
    while True:
        timecounter += 1
        value = math.sin(2 * math.pi * frequency * timecounter / cycle_length)
        if type=='square':
            value = sg.square(2 * math.pi * frequency * timecounter / cycle_length)
        elif type=='saw':
            value = sg.sawtooth(2 * math.pi * frequency * timecounter / cycle_length)
        yield value

def remap(input_value, input_minmax, output_minmax):
    return (
            input_value - input_minmax[0]
        ) / (
            input_minmax[1] - input_minmax[0]
        ) * (
            output_minmax[1] - output_minmax[0]
        ) + output_minmax[0]

cycle = oscillator(50,frequency=1.2)
plot_list = []
for i in range(100):
    value = remap(cycle.next(), [-1,1], [1.1, 1.8])
    plot_list.append(value)

plt.plot(plot_list)
plt.show()


####### sine wave ###########
# y = 100*np.sin(2 * np.pi * f * x / Fs)

####### square wave ##########
# y = 100* sg.square(2 *np.pi * f *x / Fs )

####### square wave with Duty Cycle ##########
# y = 100* sg.square(2 *np.pi * f *x / Fs , duty = 0.8)

####### Sawtooth wave ########
# y = 100* sg.sawtooth(2 *np.pi * f *x / Fs )
