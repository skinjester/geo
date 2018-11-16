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
import hud.console as console
import render.deepdream as dreamer
import neuralnet
import postprocess
from listener import listener
from composer import Composer
from viewport import Viewport
from data import rgb2caffe
from camerautils import WebcamVideoStream, Cameras

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
    Composer.start()
    Webcam.get().start()
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
    data.playback = initial_image  # initial camera image for starting

    while True:
        log.warning('new cycle')
        _Deepdreamer.set_cycle_start_time(time.time())

        if Model.cyclefx is not None:
            for fx in Model.cyclefx:
                if fx['name'] == 'octave_scaler':
                    Model.octave_scale = round(postprocess.octave_scaler(fx['osc']),4)
                    log.critical('octave_scale: {}'.format(Model.octave_scale))
                if fx['name'] == 'xform_array':
                    postprocess.xform_array(Composer.dreambuffer, **fx['params'])
                if fx['name'] == 'inception_xform':
                    data.playback = postprocess.inception_xform(data.playback, **fx['params'])

        # new rem sleep test
        _Deepdreamer.paint(
            Model=Model,
            base_image=data.playback,
            iteration_max = Model.iterations,
            iteration_mult = Model.iteration_mult,
            octave_n = Model.octave_n,
            octave_cutoff = Model.octave_cutoff,
            octave_scale= Model.octave_scale,
            end = Model.end,
            objective = dreamer.objective_L2,
            stepsize_base = Model.stepsize_base,
            step_mult = Model.step_mult,
            feature = Model.current_feature,
            stepfx = Model.stepfx,
            Webcam=Webcam,
            Composer=Composer,
            Framebuffer = data.Framebuffer
            )

        # logging
        later = time.time()
        duration_msg = '{:.2f}s'.format(later - now)
        now = time.time()  # the new now
        console.log_value('cycle_time',duration_msg)
        log.critical('cycle time: {}\n{}'.format(duration_msg, '-' * 80))

# -------
# INITIALIZE
# -------

osc1 = postprocess.oscillator(
            cycle_length = 100,
            frequency = 3,
            range_out = [1,30],
            wavetype = 'sin',
            dutycycle = 0.5
            )
osc2 = postprocess.oscillator(
            cycle_length = 100,
            frequency = 1.2,
            range_out = [-3.0,3.0],
            wavetype = 'sin',
            dutycycle = 0.5
            )

osc3 = postprocess.oscillator(
            cycle_length = 100,
            frequency = 1.5,
            range_out = [3.0,-3.0],
            wavetype = 'sin',
            dutycycle = 0.5
            )

osc4 = postprocess.oscillator(
            cycle_length = 100,
            frequency = 2,
            range_out = [0.0,0.5],
            wavetype = 'sin',
            dutycycle = 0.5
            )

if __name__ == "__main__":
    log = data.logging.getLogger('mainlog')
    log.setLevel(data.logging.WARNING)  # CRITICAL ERROR WARNING INFO DEBUG
    threadlog = data.logging.getLogger('threadlog')
    threadlog.setLevel(data.logging.CRITICAL)
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='twitter userid for sharing')
    args = parser.parse_args()
    if args.username:
        data.username = args.username
    width, height = data.capturesize
    data.Framebuffer = postprocess.Buffer(10,width,height)
    camera=[]
    camera.append(
        WebcamVideoStream(
            0,
            width=width,
            height=height,
            portrait_alignment=False,
            Viewport=Viewport,
            Framebuffer=data.Framebuffer,
            flip_h=False,
            flip_v=False,
            gamma=0.5,
            floor=5000,
            threshold_filter=8))
    Webcam = Cameras(source=camera, current_camera=0)
    _Deepdreamer = dreamer.Artist('test', Framebuffer=data.Framebuffer)
    Model = neuralnet.Model(program_duration=-1, current_program=0, Renderer=_Deepdreamer)
    Viewport = Viewport(window_name='deepdreamvisionquest', monitor=data.MONITOR_MAIN, fullscreen=True, listener=listener)
    Composer = Composer()

    # new idea, so objects have common pointers
    data.vis = np.zeros((data.viewsize[1], data.viewsize[0], 3), np.uint8)
    data.Model=Model
    data.Webcam=Webcam
    data.Viewport=Viewport
    data.Renderer=_Deepdreamer
    data.Composer = Composer

    main()


