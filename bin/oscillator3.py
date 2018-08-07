from matplotlib import pyplot as plt
from scipy import signal as sg
import math, time


def oscillator(cycle_length, frequency=1, range_in=[-1,1], range_out=[-1,1], type='sin'):
    timecounter = 0
    while True:
        timecounter += 1
        value = math.sin(2 * math.pi * frequency * timecounter / cycle_length)
        if type=='square':
            value = range_out[0] + ((range_out[1] - range_out[0]) / 2) + sg.square(2 * math.pi * frequency * timecounter / cycle_length) * ((range_out[1] - range_out[0]) / 2)
        elif type=='saw':
            value = sg.sawtooth(2 * math.pi * frequency * timecounter / cycle_length)
        yield round(value,2)

def remap(value, range_in, range_out):
    return range_out[0] + (range_out[1] - range_out[0]) * ((value - range_in[0]) / (range_in[1] - range_in[0]))



cycle = oscillator(50, frequency=1, range_out=[3,3], type="square")
plot_list = []
for i in range(100):
    plot_list.append(int(cycle.next()))

print plot_list
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
