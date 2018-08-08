import data, time, math
import scipy.ndimage as nd
from scipy import signal as sg
import PIL.Image
import cv2
import numpy as np
import hud.console as console

def inception_xform(image, scale):
    h = image.shape[0]
    w = image.shape[1]
    image = nd.affine_transform(image, [1 - scale, 1 - scale, 1],
        [h * scale / 2, w * scale / 2, 0], order=1)
    return image

def octave_scaler(osc):
    return osc.next()

# STEPFX
def median_blur(image, osc):
    blur = int(osc.next())
    log.critical('{}'.format(blur))
    if blur == 0:
        return image
    return cv2.medianBlur(image, blur)

def bilateral_filter(image, osc1, osc2, osc3):
    radius = int(osc1.next())
    sigma_color = osc2.next()
    sigma_xy = osc3.next()
    log.critical('radius:{} sigma_color:{} sigma_xy:{}'.format(radius, sigma_color, sigma_xy))
    return cv2.bilateralFilter(image, radius, sigma_color, sigma_xy)

def oscillator(cycle_length, frequency=1, range_in=[-1,1], range_out=[-1,1], wavetype='sin', dutycycle=0.5):
    timecounter = 0
    while True:
        timecounter += 1
        if wavetype=='square':
            value = range_out[0] + ((range_out[1] - range_out[0]) / 2) + sg.square(2 * math.pi * frequency * timecounter / cycle_length, duty=dutycycle) * ((range_out[1] - range_out[0]) / 2)
        elif wavetype=='saw':
            value = range_out[0] + ((range_out[1] - range_out[0]) / 2) + sg.sawtooth(2 * math.pi * frequency * timecounter / cycle_length) * ((range_out[1] - range_out[0]) / 2)
        else:
            value = range_out[0] + ((range_out[1] - range_out[0]) / 2) + math.sin(2 * math.pi * frequency * timecounter / cycle_length) * ((range_out[1] - range_out[0]) / 2)
        yield value

def remap(value, range_in, range_out):
    return range_out[0] + (range_out[1] - range_out[0]) * ((value - range_in[0]) / (range_in[1] - range_in[0]))


# class FX(object):
#     def __init__(self):

#     def xform_array(self, image, amplitude, wavelength):

#         # def shiftfunc(n):
#         #     return int(amplitude*np.sin(n/wavelength))
#         # for n in range(image.shape[1]): # number of rows in the image
#         #     image[:, n] = np.roll(image[:, n], 3*shiftfunc(n))
#         print '****'
#         return image


#     def nd_gaussian(self, image, sigma, order):
#         image[0] = nd.filters.gaussian_filter(image[0], sigma, order=0)
#         image[1] = nd.filters.gaussian_filter(image[1], sigma, order=0)
#         image[2] = nd.filters.gaussian_filter(image[2], sigma, order=0)
#         # image = nd.filters.gaussian_filter(image, sigma, order=0)
#         return image

#     def step_mixer(self, opacity):
#         self.stepfx_opacity = opacity

#     def duration_cutoff(self, duration):
#         elapsed = time.time() - self.cycle_start_time
#         if elapsed >= duration:
#             Viewport.refresh()
#         log.warning('cycle_start_time:{} duration:{} elapsed:{}'.format(
#             self.cycle_start_time, duration, elapsed))



# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.CRITICAL)
