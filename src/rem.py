# rem.py

# system
import os, os.path, argparse, sys, errno, time, warnings
from threading import Thread
warnings.filterwarnings('ignore', '.*output shape of zoom.*') # hide scipy console msg

# image processing
import scipy.ndimage as nd, PIL.Image, cv2

# maths
import math, numpy as np
from random import randint

# neural network
os.environ[
    'GLOG_minloglevel'] = '2'  # suppress verbose caffe logging before caffe import
import caffe
from google.protobuf import text_format

# program modules
import data
from data import rgb2caffe
from camerautils import WebcamVideoStream, Cameras
from listener import listener
from hud.console import console_log, console_draw
import render.deepdream as dreamer
import neuralnet

class Viewport(object):

    def __init__(self, window_name, monitor, fullscreen, listener):
        self.window_name = '{}-{}'.format(window_name, data.username)
        self.b_show_HUD = False
        self.b_show_monitor = False
        self.imagesavepath = '/home/gary/Pictures/{}'.format(data.username)
        self.listener = listener
        self.force_refresh = True
        self.fullscreen = fullscreen
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        if self.fullscreen:
            cv2.setWindowProperty(self.window_name, 0, 1)
        cv2.moveWindow(self.window_name, monitor[0], monitor[1])

    def show(self, image):
        if self.b_show_HUD:
            image = console_draw(image)
        cv2.imshow(self.window_name, image)
        self.monitor()
        self.listener(Model, Webcam, Viewport, log, console_log)

    def export(self, image):
        make_sure_path_exists(self.imagesavepath)
        log.warning('{}:{}'.format('export image', self.imagesavepath))
        export_path = '{}/{}.jpg'.format(
            self.imagesavepath,
            time.strftime('%m-%d-%H-%M-%s')
        )
        savefile = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        PIL.Image.fromarray(np.uint8(savefile)).save(export_path)
        # tweet(export_path)

    # forces new cycle with new camera image
    def refresh(self):
        self.force_refresh = True

    def monitor(self):
        if self.b_show_monitor:
            msg = Webcam.get().motiondetector.monitor_msg
            image = Webcam.get().buffer_t
            cv2.putText(image, msg, (20, 20), data.FONT, 0.5, data.WHITE)
            cv2.imshow('delta', image)

    def toggle_HUD(self):
        self.b_show_HUD = not self.b_show_HUD

    def toggle_monitor(self):
        self.b_show_monitor = not self.b_show_monitor
        if self.b_show_monitor:
            cv2.namedWindow('delta', cv2.WINDOW_AUTOSIZE)
        else:
            cv2.destroyWindow('delta')


    def shutdown(self):
        cv2.destroyAllWindows()
        for cam in Camera:
            cam.stop()
        sys.exit()

class Composer(object):
    def __init__(self):
        self.isDreaming = False
        self.xform_scale = 0.05
        self.emptybuffer = np.zeros((data.viewsize[1], data.viewsize[0], 3),
            np.uint8)
        self.buffer = []
        self.buffer.append(
            Webcam.get().read())  # uses camera capture dimensions
        self.buffer.append(
            Webcam.get().read())  # uses camera capture dimensions
        self.mixbuffer = self.emptybuffer
        self.dreambuffer = self.emptybuffer
        self.opacity = 0
        self.opacity_step = 0.1
        self.buffer3_opacity = 1.0

    def send(self, channel, image):
        self.buffer[channel] = image

        # input resized to match viewport dimensions
        self.buffer[channel] = cv2.resize(self.buffer[channel],
            (data.viewsize[0], data.viewsize[1]),
            interpolation=cv2.INTER_LINEAR)

        # convert and clip any floating point values into RGB bounds as integers
        self.buffer[channel] = np.uint8(np.clip(self.buffer[channel], 0, 255))

    def get(self, channel):
        return self.buffer[channel]

    def mix(self, image_back, image_front, mix_opacity):
        cv2.addWeighted(
            image_front,
            mix_opacity,  #
            image_back,
            1 - mix_opacity,
            0,
            self.mixbuffer
        )

        return self.mixbuffer

    def update(self, vis, Webcam):

        # motion detection
        motion = Webcam.get().motiondetector
        motion.peak_last = motion.peak
        motion.peak = motion.delta_history_peak


        if motion.delta > motion.delta_trigger:
            log.critical('starting new dream')
            _deepdreamer.request_wakeup()

        if motion.peak < motion.floor:
            self.opacity -= 0.1
            if self.opacity < 0.0:
                self.opacity = 0.0
        else:
            if (self.opacity + self.opacity_step < 0.0) or (self.opacity + self.opacity_step > 1.0):
                self.opacity_step = -1.0 * self.opacity_step
            self.opacity += self.opacity_step

        log.critical(
            'count:{:>06} trigger:{:>06} peak:{:>06} opacity:{:03.2}'
                .format(
                motion.delta,
                motion.delta_trigger,
                motion.delta_history_peak,
                Composer.opacity
            )
        )

        # compositing
        self.send(0, vis)
        self.send(1, Webcam.get().read())
        comp1 = Composer.mix(Composer.buffer[0], Composer.buffer[1], Composer.opacity)
        Viewport.show(comp1)

        # for fx in Model.cyclefx:
        #     if fx['name'] == 'inception_xform':
        #         image = FX.inception_xform(image, **fx['params'])
        # return image

class FX(object):
    def __init__(self):
        self.direction = 1
        self.stepfx_opacity = 1.0
        self.cycle_start_time = 0
        self.program_start_time = 0

    def xform_array(self, image, amplitude, wavelength):

        # def shiftfunc(n):
        #     return int(amplitude*np.sin(n/wavelength))
        # for n in range(image.shape[1]): # number of rows in the image
        #     image[:, n] = np.roll(image[:, n], 3*shiftfunc(n))
        print '****'
        return image

    def test_args(self, model=neuralnet.Model, step=0.05, min_scale=1.2, max_scale=1.6):
        print 'model: ', model
        print 'step: ', step
        print 'min_scale: ', min_scale
        print 'max_scale: ', max_scale

    def octave_scaler(self, model=neuralnet.Model, step=0.05, min_scale=1.2,
        max_scale=1.6):
        # octave scaling cycle each rem cycle, maybe
        # if (int(time.time()) % 2):
        model.octave_scale += step * self.direction
        # prevents values from getting stuck above or beneath min/max
        if model.octave_scale > max_scale or model.octave_scale <= min_scale:
            self.direction = -1 * self.direction
        console_log('scale', model.octave_scale)
        log.debug('octave_scale: {}'.format(model.octave_scale))

    def inception_xform(self, image, scale):
        h = image.shape[0]
        w = image.shape[1]
        image = nd.affine_transform(image, [1 - scale, 1 - scale, 1],
            [h * scale / 2, w * scale / 2, 0], order=1)
        return image

    def median_blur(self, image, kernel_shape, interval):
        if interval == 0:
            image = cv2.medianBlur(image, kernel_shape)
            return image
        if (int(time.time()) % interval):
            image = cv2.medianBlur(image, kernel_shape)
        return image

    def bilateral_filter(self, image, radius, sigma_color, sigma_xy):
        return cv2.bilateralFilter(image, radius, sigma_color, sigma_xy)

    def nd_gaussian(self, image, sigma, order):
        image[0] = nd.filters.gaussian_filter(image[0], sigma, order=0)
        image[1] = nd.filters.gaussian_filter(image[1], sigma, order=0)
        image[2] = nd.filters.gaussian_filter(image[2], sigma, order=0)
        # image = nd.filters.gaussian_filter(image, sigma, order=0)
        return image

    def step_mixer(self, opacity):
        self.stepfx_opacity = opacity

    def duration_cutoff(self, duration):
        elapsed = time.time() - self.cycle_start_time
        if elapsed >= duration:
            Viewport.refresh()
        log.warning('cycle_start_time:{} duration:{} elapsed:{}'.format(
            self.cycle_start_time, duration, elapsed))

    # called by main() at start of each cycle
    def set_cycle_start_time(self, start_time):
        self.cycle_start_time = start_time

def vignette(image, param):
    rows, cols = image.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, param)
    kernel_y = cv2.getGaussianKernel(rows, param)
    kernel = kernel_y * kernel_x.T
    mask = 22 * kernel / np.linalg.norm(kernel)
    output = np.copy(image)
    for i in range(1):
        output[:, :, i] = np.uint8(np.clip((output[:, :, i] * mask), 0, 512))
    return output

def make_sure_path_exists(directoryname):
    try:
        os.makedirs(directoryname)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def tweet(path_to_image):
    consumer_key = '3iSUitN4D5Fi52fgmF5zMQodc'
    consumer_secret = 'Kj9biRwpjCBGQOmYJXd9xV4ni68IO99gZT2HfdHv86HuPhx5Mq'
    access_key = '15870561-2SH025poSRlXyzAGc1YyrL8EDgD5O24docOjlyW5O'
    access_secret = 'qwuc8aa6cpRRKXxMObpaNhtpXAiDm6g2LFfzWhSjv6r8H'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    fn = os.path.abspath('../eagle.jpg')

    # myStatusText = '{} #deepdreamvisionquest #gdc2016'.format(Viewport.username)
    myStatusText = '#deepdreamvisionquest #gdc2016 test'
    api.update_with_media(path_to_image, status=myStatusText)

def show_stats(image):
    log.warning('show stats')
    stats_overlay = image.copy()
    opacity = 1.0
    cv2.putText(stats_overlay, 'show_stats()', (30, 40), data.FONT, 0.5,
        data.RED)
    return cv2.addWeighted(stats_overlay, opacity, image, 1 - opacity, 0, image)

def monitor2():
    pass

# -------
# MAIN
# -------
def main():
    now = time.time()  # start timer
    caffe.set_device(0)
    caffe.set_mode_gpu()
    iterations = Model.iterations
    stepsize = Model.stepsize_base
    octaves = Model.octaves
    octave_scale = Model.octave_scale
    jitter = 300

    # logging
    console_log('model', Model.caffemodel)
    console_log('username', data.username)
    console_log('settings', Model.package_name)

    # the madness begins
    initial_image = Webcam.get().read()
    Composer.send(1, initial_image)
    Composer.dreambuffer = initial_image  # initial camera image for starting

    while True:
        log.debug('new cycle')
        FX.set_cycle_start_time(
            time.time())  # register cycle start for duration_cutoff stepfx

        if Model.cyclefx is not None:
            for fx in Model.cyclefx:
                if fx['name'] == 'octave_scaler':
                    FX.octave_scaler(model=Model, **fx['params'])
                if fx['name'] == 'xform_array':
                    FX.xform_array(Colmposer.dreambuffer, **fx['params'])

        # new rem sleep test
        Composer.dreambuffer = _deepdreamer.paint(
            net=Model.net,
            base_image=Composer.dreambuffer,
            iteration_max = Model.iterations,
            octave_n = Model.octaves,
            octave_scale= Model.octave_scale,
            end = Model.end,
            objective = dreamer.objective_L2,
            step_size_base = Model.stepsize_base,
            step_mult = Model.step_mult,
            feature = Model.features[Model.current_feature],
            Webcam=Webcam,
            Composer=Composer,
            Viewport=Viewport
            )

        for fx in Model.cyclefx:
            if fx['name'] == 'inception_xform':
                Composer.dreambuffer = FX.inception_xform(Composer.dreambuffer, **fx['params'])

        # logging
        later = time.time()
        duration_msg = '{:.2f}s'.format(later - now)
        now = time.time()  # the new now
        console_log('cycle_time', duration_msg)
        log.warning('cycle time: {}\n{}'.format(duration_msg, '-' * 80))


# -------
# INITIALIZE
# -------
if __name__ == "__main__":
    log = data.logging.getLogger('mainlog')
    log.setLevel(data.logging.INFO)  # CRITICAL ERROR WARNING INFO DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='twitter userid for sharing')
    parser.add_argument('--cameraID', help='camera device ID to use as video input')
    args = parser.parse_args()
    if args.username:
        data.username = args.username
    Camera=[]
    Camera.append(WebcamVideoStream(0, width=data.capturesize[0],
        height=data.capturesize[1], portrait_alignment=False,
        flip_h=False, flip_v=False, gamma=0.5, floor=10000,
        threshold_filter=8).start())
    Webcam = Cameras(source=Camera, current_camera=0)
    Viewport = Viewport(window_name='deepdreamvisionquest', monitor=data.MONITOR_MAIN, fullscreen=False, listener=listener)
    Composer = Composer()
    Model = neuralnet.Model(program_duration=45, current_program=0)
    _deepdreamer = dreamer.Artist('test')
    Webcam.get().stop()
    sys.exit()
    # FX = FX()
    # main()


