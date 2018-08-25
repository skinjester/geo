import math
import itertools
from matplotlib import pyplot as plt

class Sine:
    '''A sine wave oscillator.'''

    sr = 44100
    ksmps = 1000

    def __init__(self, amp=1.0, freq=440, phase=20.0):
        self.amp = amp
        self.freq = float(freq)
        self.phase = phase

    def __iter__(self):
        self.index = 0
        return self

    def next(self):
        if self.index >= self.ksmps:
            raise StopIteration

        self.index += 1
        v = math.sin(self.phase * 2 * math.pi)
        self.phase += self.freq / self.sr
        return v * self.amp

if __name__ == "__main__":
    a1 = Sine(1, 4410, 0.25)
    # a2 = Sine(0.5, 8820)
    # amix = (i + j for i, j in itertools.izip(a1, a2))

    list_of_generated_values = []
    for i in a1:
        list_of_generated_values.append(i)

    plt.plot(list_of_generated_values)
    plt.show()
