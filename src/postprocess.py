import data, time
import scipy.ndimage as nd, PIL.Image, cv2
import hud.console as console

def inception_xform(image, scale):
    h = image.shape[0]
    w = image.shape[1]
    image = nd.affine_transform(image, [1 - scale, 1 - scale, 1],
        [h * scale / 2, w * scale / 2, 0], order=1)
    return image

def octave_scaler(Model):
    Model.octave_scale = Model.pool.next()
    console.log_value('scale', Model.octave_scale)


# STEPFX
def median_blur(image, kernel_shape, interval):
    # if interval == 0:
    #     image = cv2.medianBlur(image, kernel_shape)
    #     return image
    # if (int(time.time()) % interval):
    image = cv2.medianBlur(image, kernel_shape)
    return image

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


# class FX(object):
#     def __init__(self):

#     def xform_array(self, image, amplitude, wavelength):

#         # def shiftfunc(n):
#         #     return int(amplitude*np.sin(n/wavelength))
#         # for n in range(image.shape[1]): # number of rows in the image
#         #     image[:, n] = np.roll(image[:, n], 3*shiftfunc(n))
#         print '****'
#         return image

#     # def test_args(self, model=neuralnet.Model, step=0.05, min_scale=1.2, max_scale=1.6):
#     #     print 'model: ', model
#     #     print 'step: ', step
#     #     print 'min_scale: ', min_scale
#     #     print 'max_scale: ', max_scale




#     def bilateral_filter(self, image, radius, sigma_color, sigma_xy):
#         return cv2.bilateralFilter(image, radius, sigma_color, sigma_xy)

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
