import cv2, numpy as np, math, random, time, PIL.Image
import scipy.ndimage as nd
from scipy import signal as sg
import data, hud.console as console

class Buffer(object):
    def __init__(self, buffer_size, width, height):
        self.width = width
        self.height = height
        self.storage = np.empty((buffer_size, self.width, self.height, 3), np.dtype('uint8'))
        self.widetime_storage = np.empty((5, self.width, self.height, 3), np.dtype('uint8'))
        self.playback_counter = counter(buffer_size-1)
        self.playback_index = 0
        self.widetime_accumulated = np.zeros((self.width, self.height, 3), np.uint8)
        self.accumulated = np.zeros((self.width, self.height, 3), np.uint8)
        self.start_time = 0.0
        (self.rAvg, self.gAvg, self.bAvg) = (None, None, None)
        self.total = 0
        self.frame = counter()
        self.locked = False
        self.frame_repeat_count = 0
        self.total_frames = 0
        self.osc1 = oscillator(
                        cycle_length = 100,
                        frequency = 1,
                        range_out = [-3.0,3.0],
                        wavetype = 'sin',
                        dutycycle = 0.5
                        )
        self.osc2 = oscillator(
                        cycle_length = 100,
                        frequency = 1.2,
                        range_out = [-3.0,3.0],
                        wavetype = 'sin',
                        dutycycle = 0.5
                        )

        self.osc3 = oscillator(
                        cycle_length = 100,
                        frequency = 1.5,
                        range_out = [3.0,-3.0],
                        wavetype = 'sin',
                        dutycycle = 0.5
                        )

    def write(self, img):
        if not self.locked:
            # input resized to match viewport dimensions
            img = cv2.resize(img,(data.viewsize[0], data.viewsize[1]),interpolation=cv2.INTER_LINEAR)
            previous_img = self.storage[0].copy()
            self.storage=np.roll(self.storage,1,axis=0)
            self.storage[0] = self.mix(img, previous_img, 0.5, gamma=1.0)
            self.total_frames += 1
            log.debug('frames added:{}'.format(self.total_frames))

    def widetime_write(self, img):
        if not self.locked:
            # input resized to match viewport dimensions
            img = cv2.resize(img,(data.viewsize[0], data.viewsize[1]),interpolation=cv2.INTER_LINEAR)
            previous_img = self.widetime_storage[0].copy()
            self.widetime_storage=np.roll(self.widetime_storage,1,axis=0)
            self.widetime_storage[0] = self.mix(img, previous_img, 0.5, gamma=1.0)
            self.total_frames += 1
            log.debug('frames added:{}'.format(self.total_frames))

    def cycle(self,repeat):
        self.frame_repeat_count += 1
        if self.frame_repeat_count >= repeat:
            self.playback_index = -1 * self.playback_counter.next()
            self.frame_repeat_count = 0
            self.locked = False
        else:
            self.locked = True
        return self.storage[self.playback_index]

    def mix(self, image_front, image_back, front_opacity, gamma):
        return cv2.addWeighted(
            image_front,
            front_opacity,  #
            image_back,
            1 - front_opacity,
            gamma,
        )

    def widetime(self, index, interval):
        if index % interval == 0:
            alpha = 0.25
            beta = 1 - alpha
            gamma = 1.0
            img = self.widetime_storage[0]
            self.widetime_accumulated = cv2.addWeighted(img, alpha, self.widetime_accumulated, beta, gamma)
        return self.widetime_accumulated

    def slowshutter(self,img,samplesize,interval):
        if self.frame.next() % int(interval) != 0:
            return self.accumulated
        log.debug('samplesize:{} interval:{}'.format(samplesize,interval))
        (B, G, R) = cv2.split(img.astype("float"))
        if self.rAvg is None:
            self.rAvg = R
            self.bAvg = B
            self.gAvg = G
        else:
                self.rAvg = ((samplesize * self.rAvg) + (2 * R)) / (samplesize + 2.0)
                self.gAvg = ((samplesize * self.gAvg) + (2 * G)) / (samplesize + 2.0)
                self.bAvg = ((samplesize * self.bAvg) + (2 * B)) / (samplesize + 2.0)
        self.accumulated = cv2.merge([self.bAvg, self.gAvg, self.rAvg]).astype("uint8")
        return self.accumulated

def inception_xform(image, scale):
    h = image.shape[0]
    w = image.shape[1]
    image = nd.affine_transform(image, [1 - scale, 1-scale, 1],
        [h * scale / 2, w * scale / 2, 0], order=1)
    return image

def octave_scaler(osc):
    return osc.next()

# STEPFX
def median_blur(image, osc):
    blur = int(osc.next())
    log.warning('median_blur: {}'.format(blur))
    if blur == 0:
        return image
    return cv2.medianBlur(image, blur)

def bilateral_filter(image, osc1, osc2, osc3):
    radius = int(osc1.next())
    sigma_color = osc2.next()
    sigma_xy = osc3.next()
    log.debug('radius:{} sigma_color:{} sigma_xy:{}'.format(radius, sigma_color, sigma_xy))
    return cv2.bilateralFilter(image, radius, sigma_color, sigma_xy)

def nd_gaussian(image, osc):
    sigma = osc.next()
    log.debug('sigma:{}'.format(sigma))
    image[0] = nd.filters.gaussian_filter(image[0], sigma, order=0)
    image[1] = nd.filters.gaussian_filter(image[1], sigma, order=0)
    image[2] = nd.filters.gaussian_filter(image[2], sigma, order=0)
    return image

def step_mixer(osc):
    return osc.next()

def equalize(img, clipLimit=4, tileGridSize=(8,8)):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.uint8(np.clip(gray, 0, 255))
    clahe = cv2.createCLAHE(clipLimit, tileGridSize)
    equalized = clahe.apply(gray)
    img = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
    return img

def grayscale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

def counter(maxvalue=9999999):
    value = 0
    yield value
    while True:
        value += 1
        if value > maxvalue:
            value = 0
        yield value

def feature_release_counter(maxvalue=9999999):
    value = 0
    yield value
    while True:
        value += 1
        if value > maxvalue:
            value = 0
        yield value


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

def update_feature():
    counter = release.next()
    throttle = counter % 10
    if throttle == 0:
        data.Model.next_feature()

def adjust_eq_clip(b_increase=True):
    if b_increase:
        data.eq_clip += 1
    else:
        data.eq_clip -= 1

def adjust_eq_grid(b_increase=True):
    increment = -1
    if b_increase:
        increment = 1
    grid_x = data.eq_grid[0]
    grid_y = data.eq_grid[1]
    if grid_x + increment > 0 and grid_y + increment > 0:
        data.eq_grid = (grid_x + increment, grid_y + increment)



# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.CRITICAL)

# DEBUG
release = feature_release_counter()


