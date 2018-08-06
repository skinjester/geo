from matplotlib import pyplot as plt
from scipy import signal as sg
import math, time


def oscillator(cycle_length, frequency=1, out_minmax=[1,10], type='sin'):
    timecounter = 0
    while True:
        timecounter += 1
        value = math.sin(2 * math.pi * frequency * timecounter / cycle_length)
        if type=='square':
            value = sg.square(2 * math.pi * frequency * timecounter / cycle_length)
        elif type=='saw':
            value = sg.sawtooth(2 * math.pi * frequency * timecounter / cycle_length)
        yield remap(value, out_minmax)

def remap(in_value, in_minmax=[-1,1], out_minmax=[-1,1]):
    return (
            in_value - in_minmax[0]
        ) / (
            in_minmax[1] - in_minmax[0]
        ) * (
            out_minmax[1] - out_minmax[0]
        ) + out_minmax[0]

cycle = oscillator(50, out_minmax=[0,5])
plot_list = []
for i in range(100):
    plot_list.append(cycle.next())

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
