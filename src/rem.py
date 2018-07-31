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


# program modules
import data
from data import rgb2caffe
from camerautils import WebcamVideoStream, Cameras
from listener import listener
import hud.console as console
import render.deepdream as dreamer
import neuralnet
import postprocess

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
            image = console.draw(image)
        cv2.imshow(self.window_name, image)
        self.monitor()
        self.listener(Model, Webcam, Viewport, log, console.log_value)

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
        for camera in Webcam.get_camera_list():
            camera.stop()
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
        self.running = False

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
        motion = Webcam.get().motiondetector
        motion.peak_last = motion.peak
        motion.peak = motion.delta_history_peak

        if motion.delta > motion.delta_trigger:
            log.warning('starting new dream')
            _Deepdreamer.request_wakeup()
            self.running = False

        if motion.peak < motion.floor:
            self.opacity -= 0.1
            if self.opacity < 0.0:
                self.opacity = 0.0
                self.running = False
                # _Deepdreamer.request_wakeup()
        else:
            if (self.opacity + self.opacity_step < 0.5) or (self.opacity + self.opacity_step > 1.0):
                self.opacity_step = -1.0 * self.opacity_step
                _Deepdreamer.request_wakeup()
            self.opacity += self.opacity_step

        # compositing
        self.send(0, vis)
        self.send(1, Webcam.get().read())
        comp1 = Composer.mix(Composer.buffer[0], Composer.buffer[1], Composer.opacity)
        Viewport.show(comp1)

        console.log_value('runtime', '{:0>2}'.format(round(time.time() - Model.installation_startup, 2)))
        console.log_value('interval', '{:01.2f}/{:01.2f}'.format(round(time.time() - Model.program_start_time, 2), Model.program_duration))

        # program sequencer. don't run if program_duration is -1 though
        if Model.program_running and Model.program_duration > 0:
            if time.time() - Model.program_start_time > Model.program_duration:
                Model.next_program()


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

    iterations = Model.iterations
    stepsize = Model.stepsize_base
    octave_n = Model.octave_n
    octave_scale = Model.octave_scale
    jitter = 300

    # logging
    console.log_value('username',data.username)
    console.log_value('settings',Model.package_name)

    # the madness begins
    initial_image = Webcam.get().read()
    Composer.send(1, initial_image)
    Composer.dreambuffer = initial_image  # initial camera image for starting

    while True:
        log.debug('new cycle')
        _Deepdreamer.set_cycle_start_time(time.time())

        if Model.cyclefx is not None:
            for fx in Model.cyclefx:
                if fx['name'] == 'octave_scaler':
                    postprocess.octave_scaler(Model=Model)
                if fx['name'] == 'xform_array':
                    postprocess.xform_array(Composer.dreambuffer, **fx['params'])
                if fx['name'] == 'inception_xform':
                    Composer.dreambuffer = postprocess.inception_xform(Composer.dreambuffer, **fx['params'])

        # new rem sleep test
        Composer.dreambuffer = _Deepdreamer.paint(
            Model=Model,
            base_image=Composer.dreambuffer,
            iteration_max = Model.iterations,
            iteration_mult = Model.iteration_mult,
            octave_n = Model.octave_n,
            octave_cutoff = Model.octave_cutoff,
            octave_scale= Model.octave_scale,
            end = Model.end,
            objective = dreamer.objective_L2,
            stepsize_base = Model.stepsize_base,
            step_mult = Model.step_mult,
            feature = Model.features[Model.current_feature],
            stepfx = Model.stepfx,
            Webcam=Webcam,
            Composer=Composer,
            Viewport=Viewport,
            )

        Composer.dreambuffer = cv2.resize(Composer.dreambuffer,
            (data.viewsize[0], data.viewsize[1]),
            interpolation=cv2.INTER_LINEAR)

        # logging
        later = time.time()
        duration_msg = '{:.2f}s'.format(later - now)
        now = time.time()  # the new now
        console.log_value('cycle_time',duration_msg)
        log.critical('cycle time: {}\n{}'.format(duration_msg, '-' * 80))

# -------
# INITIALIZE
# -------
if __name__ == "__main__":
    log = data.logging.getLogger('mainlog')
    log.setLevel(data.logging.CRITICAL)  # CRITICAL ERROR WARNING INFO DEBUG
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='twitter userid for sharing')
    args = parser.parse_args()
    if args.username:
        data.username = args.username
    Viewport = Viewport(window_name='deepdreamvisionquest', monitor=data.MONITOR_MAIN, fullscreen=False, listener=listener)
    camera=[]
    camera.append(WebcamVideoStream(0, width=data.capturesize[0],
        height=data.capturesize[1], portrait_alignment=False,
        flip_h=False, flip_v=False, gamma=0.5, floor=10000,
        threshold_filter=8).start())
    Webcam = Cameras(source=camera, current_camera=0)
    Composer = Composer()
    _Deepdreamer = dreamer.Artist('test')
    Model = neuralnet.Model(program_duration=-1, current_program=1, Renderer=_Deepdreamer)
    main()


