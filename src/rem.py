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
# from model import Model

class Model(object):
    def __init__(self, current_layer=0, program_duration=30):
        self.net = None
        self.net_fn = None
        self.param_fn = None
        self.caffemodel = None
        self.end = None
        self.models = data.models
        self.guides = data.guides
        self.guide_features = self.guides[0]

        self.features = None
        self.current_feature = 0

        self.current_guide = 0
        self.current_layer = current_layer
        self.layers = data.layers
        self.first_time_through = True

        self.program = data.program
        self.current_program = 0
        self.program_duration = program_duration
        self.program_running = True
        self.program_start_time = time.time()
        self.installation_startup = time.time()  # keep track of runtime

        # amplification
        self.iterations = None
        self.iteration_max = None
        self.stepsize = None
        self.stepsize_base = None
        self.step_size_base = None
        self.octaves = None
        self.octave_n = None
        self.octave_cutoff = None
        self.octave_scale = None
        self.iteration_mult = None
        self.step_mult = None
        self.jitter = 320
        self.clip = True

        # FX
        self.package_name = None
        self.cyclefx = None  # contains cyclefx list for current program
        self.stepfx = None  # contains stepfx list for current program

        # objective
        self.objective = dreamer.objective_L2

    def set_program(self, index):
        Viewport.refresh()
        self.package_name = data.program[index]['name']
        self.iterations = data.program[index]['iterations']
        self.iteration_max = data.program[index]['iterations']
        self.stepsize_base = data.program[index]['step_size']
        self.step_size_base = data.program[index]['step_size']
        self.octaves = data.program[index]['octaves']
        self.octave_n = data.program[index]['octaves']
        self.octave_cutoff = data.program[index]['octave_cutoff']
        self.octave_scale = data.program[index]['octave_scale']
        self.iteration_mult = data.program[index]['iteration_mult']
        self.step_mult = data.program[index]['step_mult']
        self.layers = data.program[index]['layers']
        self.features = data.program[index]['features']
        self.current_feature = 0;
        self.model = data.program[index]['model']
        self.choose_model(self.model)
        self.set_endlayer(self.layers[0])
        self.cyclefx = data.program[index]['cyclefx']
        self.stepfx = data.program[index]['stepfx']
        self.program_start_time = time.time()
        log.warning('program:{} started:{}'.format(
            self.program[self.current_program]['name'],
            self.program_start_time))

    def choose_model(self, key):
        self.net_fn = '{}/{}/{}'.format(self.models['path'],
            self.models[key][0], self.models[key][1])
        self.param_fn = '{}/{}/{}'.format(self.models['path'],
            self.models[key][0], self.models[key][2])
        self.caffemodel = self.models[key][2]

        # Patch model to be able to compute gradients
        # load the empty protobuf model
        model = caffe.io.caffe_pb2.NetParameter()

        # load the prototxt and place it in the empty model
        text_format.Merge(open(self.net_fn).read(), model)

        # add the force backward: true value
        model.force_backward = True

        # save it to a new file called tmp.prototxt
        open('tmp.prototxt', 'w').write(str(model))

        # the neural network model
        self.net = caffe.Classifier('tmp.prototxt',
            self.param_fn, mean=np.float32([104.0, 116.0, 122.0]),
            channel_swap=(2, 1, 0))
        # self.param_fn, mean=np.float32([20.0, 10.0,190.0]), channel_swap=(2, 1, 0))

        console_log('model', self.caffemodel)

    def show_network_details(self):
        # outputs layer details to console
        print self.net.blobs.keys()
        print 'current layer:{} ({}) current feature:{}'.format(
            self.end,
            self.net.blobs[self.end].data.shape[1],
            self.features[self.current_feature]
        )

    def set_endlayer(self, end):
        self.end = end
        Viewport.refresh()
        log.warning('layer: {} ({})'.format(self.end, self.net.blobs[self.end].data.shape[1]))
        console_log('layer','{} ({})'.format(self.end, self.net.blobs[self.end].data.shape[1]))

    def prev_layer(self):
        self.current_layer -= 1
        if self.current_layer < 0:
            self.current_layer = len(self.layers) - 1
        self.set_endlayer(self.layers[self.current_layer])

    def next_layer(self):
        self.current_layer += 1
        if self.current_layer > len(self.layers) - 1:
            self.current_layer = 0
        self.set_endlayer(self.layers[self.current_layer])

    def set_featuremap(self):
        log.warning('featuremap:{}'.format(self.features[self.current_feature]))
        console_log('featuremap', self.features[self.current_feature])
        Viewport.refresh()

    def prev_feature(self):
        max_feature_index = self.net.blobs[self.end].data.shape[1]
        self.current_feature -= 1
        if self.current_feature < 0:
            self.current_feature = max_feature_index - 1
        self.set_featuremap()

    def next_feature(self):
        max_feature_index = self.net.blobs[self.end].data.shape[1]
        self.current_feature += 1
        if self.current_feature > max_feature_index - 1:
            self.current_feature = -1
        self.set_featuremap()

    def reset_feature(self):
        pass

    def prev_program(self):
        self.current_program -= 1
        if self.current_program < 0:
            self.current_program = len(self.program) - 1
        self.set_program(self.current_program)

    def next_program(self):
        self.current_program += 1
        if self.current_program > len(self.program) - 1:
            self.current_program = 0
        self.set_program(self.current_program)

    def toggle_program_cycle(self):
        self.program_running = not self.program_running
        if self.program_running:
            self.next_program()

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
            _deepdreamer.request_new()

        if motion.peak < motion.floor:
            self.opacity -= 0.1
            if self.opacity <= 0.1:
                self.opacity = 0.0
        else:
            self.opacity = data.remapValuetoRange(
                motion.delta_history,
                [0.0, 100000.0],
                [0.0, 1.0]
            )

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

    def test_args(self, model=Model, step=0.05, min_scale=1.2, max_scale=1.6):
        print 'model: ', model
        print 'step: ', step
        print 'min_scale: ', min_scale
        print 'max_scale: ', max_scale

    def octave_scaler(self, model=Model, step=0.05, min_scale=1.2,
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

# a couple of utility functions for converting to and from Caffe's input image layout
def rgb2caffe(net, image):
    return np.float32(np.rollaxis(image, 2)[::-1]) - net.transformer.mean[
        'data']

def caffe2rgb(net, image):
    return np.dstack((image + net.transformer.mean['data'])[::-1])


def postprocess_step(net, net_data_blob):
    # takes neural net data blob and converts to RGB
    # then after processing, takes the RGB image and converts back to caffe
    image = caffe2rgb(net, net_data_blob)

    #  apply any defined stepFX
    if Model.stepfx is not None:
        for fx in Model.stepfx:
            if fx['name'] == 'median_blur':
                image = FX.median_blur(image, **fx['params'])

            if fx['name'] == 'bilateral_filter':
                image = FX.bilateral_filter(image, **fx['params'])

            if fx['name'] == 'nd_gaussian':
                # image = net_data_blob

                image = FX.nd_gaussian(net_data_blob, **fx['params'])
                image = caffe2rgb(net, net_data_blob)

            if fx['name'] == 'step_opacity':
                FX.step_mixer(**fx['params'])

            if fx['name'] == 'duration_cutoff':
                FX.duration_cutoff(**fx['params'])

            if fx['name'] == 'octave_scaler':
                FX.octave_scaler(model=Model, **fx['params'])

    # image = cv2.addWeighted(image, FX.stepfx_opacity, image, 1.0-FX.stepfx_opacity, 0, image)
    return rgb2caffe(Model.net, image)


def make_step(net, step_size=1.5, end='inception_4c/output', jitter=32,
    clip=False, feature=-1, objective=dreamer.objective_L2):
    log.info(
        'step_size:{} feature:{} end:{}\n{}'.format(step_size, feature, end,
            '-' * 10))
    src = net.blobs['data']
    dst = net.blobs[end]

    ox, oy = np.random.randint(-jitter, jitter + 1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2)
    net.forward(end=end)

    if feature == -1:
        objective(dst)
    else:
        dst.diff.fill(0.0)
        dst.diff[0, feature, :] = dst.data[0, feature, :]

    net.backward(start=end)
    g = src.diff[0]
    src.data[:] += step_size / np.abs(g).mean() * g
    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2)

    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 200 - bias)

    src.data[0] = postprocess_step(net, src.data[0])

    # program sequencer. don't run if program_duration is -1 though
    elapsed = time.time() - Model.program_start_time
    if Model.program_running:
        if elapsed > Model.program_duration:
            Model.next_program()


def remapValuetoRange(val, src, dst):
    # src [min,max] old range
    # dst [min,max] new range
    remapped_Value = ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + \
                     dst[0]
    return clamp(remapped_Value, [0.0, 1.0])


# clamps provided value between provided range
def clamp(value, range):
    return max(range[0], min(value, range[1]))


# -------
# REM CYCLE
# -------
def deepdream(net, base_image, iteration_max=10, octave_n=4, octave_scale=1.4, end='inception_4c/output', clip=True, **step_params):
    motion = Webcam.get().motiondetector

    # SETUP OCTAVES
    src = net.blobs['data']
    octaves = [rgb2caffe(Model.net, base_image)]
    for i in xrange(octave_n - 1):
        octaves.append(
            nd.zoom(octaves[-1], (
            1, round((1.0 / octave_scale), 2), round((1.0 / octave_scale), 2)),
                order=1))
    detail = np.zeros_like(octaves[-1])

    for octave, octave_current in enumerate(octaves[::-1]):
        h, w = octave_current.shape[-2:]
        h1, w1 = detail.shape[-2:]
        detail = nd.zoom(detail, (1, 1.0 * h / h1, 1.0 * w / w1), order=0)
        src.reshape(1, 3, h, w)
        src.data[0] = octave_current + detail
        Model.stepsize = Model.stepsize_base  # reset step size to default each octave

        # OCTAVE CYCLE
        i = 0
        while i < iteration_max:
            # handle vieport refresh per iteration
            if Viewport.force_refresh:
                log.warning('**** Viewport Force refresh ****')
                Viewport.force_refresh = False
                return Webcam.get().read()

            make_step(Model.net, end=end, clip=clip, **step_params)

            motion.peak_last = motion.peak
            motion.peak = motion.delta_history_peak

            if motion.delta > motion.delta_trigger:
                log.critical('new dream')
                Viewport.refresh()

            if motion.peak < motion.floor:
                Composer.opacity -= 0.1
                if Composer.opacity <= 0.1:
                    Composer.opacity = 0.0
            else:
                Composer.opacity = remapValuetoRange(
                    motion.delta_history,
                    [0.0, 100000.0],
                    [0.0, 1.0]
                )

            log.debug(
                'count:{:>06} trigger:{:>06} peak:{:>06} opacity:{:03.2}'
                    .format(
                    motion.delta,
                    motion.delta_trigger,
                    motion.delta_history_peak,
                    Composer.opacity
                )
            )

            # update Composer buffers
            Composer.send(0, caffe2rgb(Model.net, src.data[0]))
            Composer.send(1, Webcam.get().read())

            # send the main mix to the viewport
            comp1 = Composer.mix(Composer.buffer[0], Composer.buffer[1],
                Composer.opacity)

            Viewport.show(comp1)

            # attenuate step size over rem cycle
            step_params['step_size'] += Model.stepsize_base * Model.step_mult

            # set a floor for any cyclefx step modification
            if step_params['step_size'] < 1.1:
                step_params['step_size'] = 1.1

            # increment step
            i += 1

            # LOGGING
            log.warning(
                '{:02d} {:02d} {:02d} peak:{} peak_history:{}'.format(octave, i,
                    iteration_max, motion.peak,
                    motion.peak_last))

            # HUD logging
            octavemsg = '{}/{}({})'.format(
                octave, octave_n,
                Model.octave_cutoff)
            guidemsg = '({}/{}) {}'.format(
                Model.current_guide,
                len(Model.guides),
                Model.guides[Model.current_guide])
            iterationmsg = '{:0>3}:{:0>3} x{}'.format(
                i,
                iteration_max,
                Model.iteration_mult)
            stepsizemsg = '{:02.3f} x{:02.3f}'.format(
                step_params['step_size'],
                Model.step_mult)
            thresholdmsg = '{:0>6}'.format(
                motion.delta_trigger)
            floormsg = '{:0>6}'.format(
                motion.floor)
            gammamsg = '{}'.format(
                Webcam.get().gamma)
            intervalmsg = '{:01.2f}/{:01.2f}'.format(
                round(time.time() - Model.program_start_time, 2),
                Model.program_duration)
            console_log('octave', octavemsg)
            console_log('width', w)
            console_log('height', h)
            console_log('guide', guidemsg)
            console_log('iteration', iterationmsg)
            console_log('step_size', stepsizemsg)
            console_log('scale', Model.octave_scale)
            console_log('program', Model.package_name)
            console_log('threshold', thresholdmsg)
            console_log('floor', floormsg)
            console_log('gamma', gammamsg)
            console_log('interval', intervalmsg)
            console_log('runtime', round(time.time() - Model.installation_startup, 2))

        # SETUP FOR NEXT OCTAVE
        # extract details produced on the current octave
        detail = src.data[
                     0] - octave_current  # these feed into next octave presumably?

        # calulate iteration count for the next octave
        iteration_max = int(
            iteration_max - (iteration_max * Model.iteration_mult))

        # CUTOFF THOUGH?
        # this turned out to be the last octave calculated in the series
        if octave > Model.octave_cutoff:
            log.warning('cutoff at octave: {}'.format(octave))
            break

    log.warning('completed full rem cycle')
    return caffe2rgb(Model.net, src.data[0])


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

        # kicks off rem sleep
        Composer.dreambuffer = deepdream(
            Model.net,
            Composer.dreambuffer,
            iteration_max=Model.iterations,
            octave_n=Model.octaves,
            octave_scale=Model.octave_scale,
            end=Model.end,
            objective=dreamer.objective_L2,
            step_size=Model.stepsize_base,
            feature=Model.features[Model.current_feature]
        )

        # new rem sleep test
        # Composer.dreambuffer = _deepdreamer.paint(
        #     net=Model.net,
        #     base_image=Composer.dreambuffer,
        #     iteration_max = Model.iterations,
        #     octave_n = Model.octaves,
        #     octave_scale= Model.octave_scale,
        #     end = Model.end,
        #     objective = dreamer.objective_L2,
        #     step_size_base = Model.stepsize_base,
        #     step_mult = Model.step_mult,
        #     feature = Model.features[Model.current_feature],
        #     Webcam=Webcam,
        #     Composer=Composer,
        #     Viewport=Viewport
        #     )

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
    Model = Model(program_duration=45)  # program duration (seconds) -1 is manual
    Model.set_program(0)
    _deepdreamer = dreamer.Artist('test')
    FX = FX()
    main()


