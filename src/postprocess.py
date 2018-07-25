import data
import scipy.ndimage as nd, PIL.Image, cv2

direction = 1
stepfx_opacity = 1.0

def inception_xform(image, scale):
    h = image.shape[0]
    w = image.shape[1]
    image = nd.affine_transform(image, [1 - scale, 1 - scale, 1],
        [h * scale / 2, w * scale / 2, 0], order=1)
    return image

def octave_scaler(model, step, min_scale, max_scale=1.6):
    pass
    # octave scaling cycle each rem cycle, maybe
    # if (int(time.time()) % 2):
    # model.octave_scale += step * direction
    # if model.octave_scale > max_scale or model.octave_scale <= min_scale:
    #     direction = -1 * direction
    # console.log_value('scale', model.octave_scale)
    # log.debug('octave_scale: {}'.format(model.octave_scale))

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



#     def median_blur(self, image, kernel_shape, interval):
#         if interval == 0:
#             image = cv2.medianBlur(image, kernel_shape)
#             return image
#         if (int(time.time()) % interval):
#             image = cv2.medianBlur(image, kernel_shape)
#         return image

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
log.critical('postprocess init')

