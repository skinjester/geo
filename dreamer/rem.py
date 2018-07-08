# rem.py

# file handling
import os
import os.path
import argparse
import sys
import errno

# image processing
import scipy.ndimage as nd
import PIL.Image
import cv2

# math
import math
import numpy as np
from random import randint

# communication
import tweepy # was used to post the framebuffer to twitter

# neural network stuff
os.environ['GLOG_minloglevel'] = '2' # suppress verbose caffe logging before caffe import
import caffe
from google.protobuf import text_format

# logging
import logging
import logging.config
sys.path.append('../bin') #  point to directory containing LogSettings
import LogSettings # global log settings templ

# system
from threading import Thread
import time

# program modules
import data
from camerautils import WebcamVideoStream
from camerautils import Cameras


# using this to index some values with dot notation in their own namespace
# perhaps misguided, but needing expediency at the moment
class Display(object):
    def __init__(self, width, height, camera):
        self.width = width
        self.height = height

        # swap width, height when in portrait alignment
        if camera.portrait_alignment:
            self.width = height
            self.height = width

        self.screensize = [self.width, self.height]


class Model(object):
    def __init__(self, current_layer=0, program_duration=-1):
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
        self.program_start_time = time.time()
        self.installation_startup = time.time() # keep track of runtime

        # amplification
        self.iterations = None
        self.stepsize = None
        self.stepsize_base = None
        self.octaves = None
        self.octave_cutoff = None
        self.octave_scale = None
        self.iteration_mult = None
        self.step_mult = None
        self.jitter = 320
        self.package_name = None

        self.choose_model(data.program[self.current_program]['model'])
        self.cyclefx = None # contains cyclefx list for current program
        self.stepfx = None # contains stepfx list for current program


    def choose_model(self, key):
        self.net_fn = '{}/{}/{}'.format(self.models['path'], self.models[key][0], self.models[key][1])
        self.param_fn = '{}/{}/{}'.format(self.models['path'], self.models[key][0], self.models[key][2])
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
            self.param_fn, mean=np.float32([104.0, 116.0, 122.0]), channel_swap=(2, 1, 0))
            # self.param_fn, mean=np.float32([20.0, 10.0,190.0]), channel_swap=(2, 1, 0))

        update_HUD_log('model',self.caffemodel)

    def show_network_details(self):
        # outputs layer details to console
        print self.net.blobs.keys()
        print 'current layer:{} ({}) current feature:{}'.format(
            self.end,
            self.net.blobs[self.end].data.shape[1],
            self.features[self.current_feature]
            )

    def set_program(self, index):
        self.package_name = data.program[index]['name']
        self.iterations = data.program[index]['iterations']
        self.stepsize_base = data.program[index]['step_size']
        self.octaves = data.program[index]['octaves']
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
        self.set_featuremap()
        self.cyclefx = data.program[index]['cyclefx']
        self.stepfx = data.program[index]['stepfx']
        self.program_start_time = time.time()
        log.warning('program:{} started:{}'.format(self.program[self.current_program]['name'], self.program_start_time))


    def set_endlayer(self,end):
        self.end = end
        Viewport.refresh()
        log.warning('layer: {} ({})'.format(self.end,self.net.blobs[self.end].data.shape[1]))
        update_HUD_log('layer','{} ({})'.format(self.end,self.net.blobs[self.end].data.shape[1]))

    def prev_layer(self):
        self.current_layer -= 1
        if self.current_layer < 0:
            self.current_layer = len(self.layers)-1
        self.set_endlayer(self.layers[self.current_layer])

    def next_layer(self):
        self.current_layer += 1
        if self.current_layer > len(self.layers)-1:
            self.current_layer = 0
        self.set_endlayer(self.layers[self.current_layer])

    def set_featuremap(self):
        Viewport.refresh()
        # featuremap = self.features[self.current_feature]
        log.warning('featuremap:{}'.format(self.features[self.current_feature]))
        update_HUD_log('featuremap',self.features[self.current_feature])

    def prev_feature(self):
        max_feature_index = self.net.blobs[self.end].data.shape[1]
        self.current_feature -= 1
        if self.current_feature < 0:
            self.current_feature = len(self.features)-1
        self.set_featuremap()

    def next_feature(self):
        max_feature_index = self.net.blobs[self.end].data.shape[1]
        self.current_feature += 1

        if self.current_feature > len(self.features)-1:
            self.current_feature = 0
        if self.current_feature > max_feature_index-1:
            self.current_feature = -1
        self.set_featuremap()

    def reset_feature(self):
        pass

    def prev_program(self):
        self.current_program -= 1
        if self.current_program < 0:
            self.current_program = len(self.program)-1
        self.set_program(self.current_program)

    def next_program(self):
        self.current_program += 1
        if self.current_program > len(self.program)-1:
            self.current_program = 0
        self.set_program(self.current_program)

class Viewport(object):

    def __init__(self, window_name, username, listener):
        self.window_name = '{}/{}'.format(window_name, username)
        self.username = username
        self.b_show_HUD = False
        self.keypress_mult = 3 # accelerate value changes when key held
        self.b_show_stats = True
        self.motiondetect_log_enabled = False
        self.blend_ratio = 0.0
        self.imagesavepath = '/home/gary/Pictures/'+self.username
        self.listener = listener
        self.force_refresh = True
        self.image = None
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def show(self, image):
        if self.b_show_HUD: # HUD overlay
            image = draw_HUD(image)

        # temp support to show debug messaging  in main window
        motiondetector = Webcam.get().motiondetector
        # cv2.putText(image, 'count', (20, 20), data.FONT, 0.5, data.WHITE)
        # cv2.putText(image, '{:>10}'.format(motiondetector.delta_count), (80, 20), data.FONT, 0.5, data.WHITE)

        # cv2.putText(image, 'trigger', (20, 40), data.FONT, 0.5, data.WHITE)
        # cv2.putText(image, '{:>10}'.format(motiondetector.delta_trigger), (80, 40), data.FONT, 0.5, data.WHITE)

        # cv2.putText(image, 'peak', (20, 60), data.FONT, 0.5, data.WHITE)
        # cv2.putText(image, '{:>10}'.format(motiondetector.delta_count_history_peak), (80, 60), data.FONT, 0.5, data.WHITE)

        # cv2.putText(image, 'history', (20, 80), data.FONT, 0.5, data.WHITE)
        # cv2.putText(image, '{:>10}'.format(motiondetector.delta_count_history), (80, 80), data.FONT, 0.5, data.WHITE)

        # cv2.putText(image, 'dreaming', (20, 100), data.FONT, 0.5, data.WHITE)
        # cv2.putText(image, '{:>10}'.format(Composer.isDreaming), (80, 100), data.FONT, 0.5, data.WHITE)

        # cv2.putText(image, 'direction', (20, 120), data.FONT, 0.5, data.WHITE)
        # cv2.putText(image, '{}'.format(motiondetector.peak_statusmsg), (120, 120), data.FONT, 0.5, data.WHITE)


        cv2.imshow(self.window_name, image) # draw to window

        self.monitor() # handle motion detection viewport
        self.listener() # listen for keyboard events


    def export(self,image):
        make_sure_path_exists(self.imagesavepath)
        log.warning('{}:{}'.format('export image',self.imagesavepath))
        export_path = '{}/{}.jpg'.format(
            self.imagesavepath,
            time.strftime('%m-%d-%H-%M-%s')
            )
        savefile = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        PIL.Image.fromarray(np.uint8(savefile)).save(export_path)
        #tweet(export_path)

    # forces new cycle with new camera image
    def refresh(self):
        self.force_refresh = True

    def monitor(self):
        if self.motiondetect_log_enabled:
            msg = Webcam.get().motiondetector.monitor_msg
            image = Webcam.get().t_delta_framebuffer
            cv2.putText(image, msg, (20, 20), data.FONT, 0.5, data.WHITE)
            cv2.imshow('delta', image)

    def shutdown(self):
        cv2.destroyAllWindows()
        for cam in Camera:
            cam.stop()
        sys.exit()

class Composer(object):
    # both self.buffer1 and self.buffer2 look to data.capture_size for their dimensions
    # this happens on init
    def __init__(self):
        self.isDreaming = False
        self.xform_scale = 0.05
        self.buffer = []
        self.buffer.append( Webcam.get().read() ) # uses camera capture dimensions
        self.buffer.append( Webcam.get().read() ) # uses camera capture dimensions
        self.buffer.append( Webcam.get().read() ) # uses camera capture dimensions
        self.mixbuffer = np.zeros((Display.height, Display.width ,3), np.uint8)
        self.dreambuffer = np.zeros((Display.height, Display.width ,3), np.uint8)
        self.opacity = 0
        self.buffer3_opacity = 1.0
        self.cycle_count = 0

    def send(self, channel, image):
        self.buffer[channel] = image

        ### any input is resized to match viewport dimensions
        self.buffer[channel] = cv2.resize(self.buffer[channel], (Display.width, Display.height), interpolation = cv2.INTER_LINEAR)

        # convert and clip any floating point values into RGB bounds as integers
        self.buffer[channel] = np.uint8(np.clip(self.buffer[channel], 0, 255))

    def mix(self, image_back, image_front, mix_opacity):
        cv2.addWeighted(
            image_front,
            mix_opacity,#
            image_back,
            1-mix_opacity,
            0,
            self.mixbuffer
            )

        return self.mixbuffer

    def update(self, image):
        for fx in Model.cyclefx:
            if fx['name'] == 'inception_xform':
                image = FX.inception_xform(image, **fx['params'])
        return image

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

    def octave_scaler(self, model=Model, step=0.05, min_scale=1.2, max_scale=1.6):
        # octave scaling cycle each rem cycle, maybe
        # if (int(time.time()) % 2):
        model.octave_scale += step * self.direction
        # prevents values from getting stuck above or beneath min/max
        if model.octave_scale > max_scale or model.octave_scale <= min_scale:
            self.direction = -1 * self.direction
        update_HUD_log('scale',model.octave_scale)
        log.debug('octave_scale: {}'.format(model.octave_scale))

    def inception_xform(self, image, scale):
        h = image.shape[0]
        w = image.shape[1]
        image = nd.affine_transform(image, [1-scale,1-scale,1], [h*scale/2,w*scale/2,0], order=1)
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

    def step_mixer(self,opacity):
        self.stepfx_opacity = opacity

    def duration_cutoff(self, duration):
        elapsed = time.time() - self.cycle_start_time
        if elapsed >= duration:
            Webcam.get().motiondetector.force_detection()
            Viewport.refresh()
        log.warning('cycle_start_time:{} duration:{} elapsed:{}'.format(self.cycle_start_time, duration, elapsed))

    # called by main() at start of each cycle
    def set_cycle_start_time(self, start_time):
        self.cycle_start_time = start_time

def vignette(image,param):
    rows,cols = image.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols,param)
    kernel_y = cv2.getGaussianKernel(rows,param)
    kernel = kernel_y * kernel_x.T
    mask = 22 * kernel / np.linalg.norm(kernel)
    output = np.copy(image)
    for i in range(1):
        output[:,:,i] = np.uint8(np.clip((output[:,:,i] * mask ), 0, 512))
    return output


def make_sure_path_exists(directoryname):
    try:
        os.makedirs(directoryname)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def tweet(path_to_image):
    consumer_key='3iSUitN4D5Fi52fgmF5zMQodc'
    consumer_secret='Kj9biRwpjCBGQOmYJXd9xV4ni68IO99gZT2HfdHv86HuPhx5Mq'
    access_key='15870561-2SH025poSRlXyzAGc1YyrL8EDgD5O24docOjlyW5O'
    access_secret='qwuc8aa6cpRRKXxMObpaNhtpXAiDm6g2LFfzWhSjv6r8H'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    fn = os.path.abspath('../eagle.jpg')

    #myStatusText = '{} #deepdreamvisionquest #gdc2016'.format(Viewport.username)
    myStatusText = '#deepdreamvisionquest #gdc2016 test'
    api.update_with_media(path_to_image, status=myStatusText )

def update_HUD_log(key,new_value):
    data.hud_log[key][1] = data.hud_log[key][0]
    data.hud_log[key][0] = new_value


def show_stats(image):
    log.warning('show stats')
    stats_overlay = image.copy()
    opacity = 1.0
    cv2.putText(stats_overlay, 'show_stats()', (30, 40), data.FONT, 0.5, data.RED)
    return cv2.addWeighted(stats_overlay, opacity, image, 1-opacity, 0, image)


def draw_HUD(image):
    # rectangle
    overlay = image.copy()
    opacity = 0.5
    cv2.rectangle(overlay,(0,0),(Display.width, Display.height), (0, 0, 0), -1)
    #cv2.rectangle(image_to_draw_on, (x1,y1), (x2,y2), (r,g,b), line_width )

    # list setup
    x,xoff = 40,180
    y,yoff = 150,20

    data.counter = 0
    def write_Text(key):
        color = data.WHITE
        row = y + yoff * data.counter
        if data.hud_log[key][0] != data.hud_log[key][1]:
            #  value has changed since last update
            color = data.GREEN
            data.hud_log[key][1] = data.hud_log[key][0] #  update history
        cv2.putText(overlay, key, (x, row), data.FONT, 0.5, data.WHITE)
        cv2.putText(overlay, '{}'.format(data.hud_log[key][0]), (xoff, row), data.FONT, 0.5, color)

        data.counter += 1

    # write text to overlay
    # col1
    cv2.putText(overlay, data.hud_log['detect'][0], (x, 40), data.FONT, 1.0, (0,255,0))
    cv2.putText(overlay, 'DEEPDREAMVISIONQUEST', (x, 100), data.FONT, 1.0, data.WHITE)
    write_Text('program')
    write_Text('interval')
    write_Text('runtime')
    write_Text('floor')
    write_Text('threshold')
    write_Text('last')
    write_Text('now')
    write_Text('model')
    write_Text('layer')
    write_Text('featuremap')
    write_Text('width')
    write_Text('height')
    write_Text('scale')
    write_Text('octave')
    write_Text('iteration')
    write_Text('step_size')
    write_Text('cycle_time')
    write_Text('gamma')


    # add overlay back to source
    return cv2.addWeighted(overlay, opacity, image, 1-opacity, 0, image)
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

# keyboard event handler
def listener():
    key = cv2.waitKey(1) & 0xFF
    # log.critical('key pressed: {}'.format(key))

    # Row A
    # --------------------------------

    if key==10: # ENTER key: save picture
        log.warning('{}:{} {} {}'.format('A1',key,'ENTER','SAVE IMAGE'))
        Viewport.export()
        return

    if key==32: # SPACE
        log.warning('{}:{} {} {}'.format('A2',key,'SPACE','***'))
        return

    if key==80: # HOME
        log.warning('{}:{} {} {}'.format('A3',key,'HOME','***'))
        return

    if key==87: # END
        log.warning('{}:{} {} {}'.format('A4',key,'END','RESET'))
        return

    # Row B
    # --------------------------------

    if key==85: # PAGE UP : increase gamma
        log.warning('{}:{} {} {}'.format('B1',key,'PAGEUP','GAMMA+'))
        Webcam.get().gamma += 0.1
        Webcam.get().update_gamma(Webcam.get().gamma )
        return

    if key==86: # PAGE DOWN decrease gamma
        log.warning('{}:{} {} {}'.format('B2',key,'PAGEDOWN','GAMMA-'))
        Webcam.get().gamma -= 0.1
        Webcam.get().update_gamma(Webcam.get().gamma )
        return

    if key == 81: # left-arrow key: previous program
        log.warning('x{}:{} {} {}'.format('B3',key,'ARROWL','PROGRAM-'))
        Model.prev_program()
        Model.reset_feature()
        return

    if key == 83: # right-arrow key: next program
        log.warning('{}:{} {} {}'.format('B4',key,'ARROWR','PROGRAM+'))
        Model.next_program()
        Model.reset_feature()
        return

    # Row C
    # --------------------------------
    if key==194: # F5
        log.warning('{}:{} {} {}'.format('C1',key,'F5','***'))
        return

    if key==195: # F6
        log.warning('{}:{} {} {}'.format('C2',key,'F6','***'))
        return

    if key == 122: # z key: next network layer
        log.warning('{}:{} {} {}'.format('C3',key,'Z','LAYER-'))
        Model.prev_layer()
        Model.reset_feature()
        return

    if key == 120: # x key: previous network layer
        log.warning('{}:{} {} {}'.format('C4',key,'X','LAYER+'))
        Model.next_layer()
        Model.reset_feature()
        return

    # Row D
    # --------------------------------

    elif key==196: # F7: show network details
        log.warning('{}:{} {} {}'.format('D1',key,'F7','***'))
        # Model.show_network_details()
        # Composer.ramp_start(True)
        return

    elif key==197: # F8
        log.warning('{}:{} {} {}'.format('D2',key,'F8','***'))
        # Composer.ramp_start(False)
        return

    elif key == 44: # , key : previous featuremap
        log.warning('{}:{} {} {}'.format('D3',key,',','Feature-'))
        Model.prev_feature()

    elif key == 46: # . key : next featuremap
        log.warning('{}:{} {} {}'.format('D4',key,'.','Feature+'))
        Model.next_feature()

    # Row E
    # --------------------------------

    if key==91: # [
        log.warning('{}:{} {} {}'.format('E1',key,'[','GAMMA -'))
        Webcam.get().gamma -= 0.1
        Webcam.get().update_gamma(Webcam.get().gamma )
        return

    if key==93: # ]
        log.warning('{}:{} {} {}'.format('E2',key,']','GAMMA +'))
        Webcam.get().gamma += 0.1
        Webcam.get().update_gamma(Webcam.get().gamma )
        return

    if key==86: # PAGE DOWN decrease gamma
        log.warning('{}:{} {} {}'.format('B2',key,'PAGEDOWN','GAMMA-'))

    if key == 45: # _ key (underscore) : decrease detection floor
        Webcam.get().motiondetector.floor -= 5000
        if Webcam.get().motiondetector.floor < 0:
            Webcam.get().motiondetector.floor = 0
        update_HUD_log('floor',Webcam.get().motiondetector.floor)
        log.warning('{}:{} {} {} :{}'.format('E3',key,'-','FLOOR-',Webcam.get().motiondetector.floor))
        return

    if key == 61: # = key (equals): increase detection floor
        Webcam.get().motiondetector.floor += 5000
        update_HUD_log('floor',Webcam.get().motiondetector.floor)
        log.warning('{}:{} {} {} :{}'.format('E4',key,'=','FLOOR+',Webcam.get().motiondetector.floor))
        return

    # Row F
    # --------------------------------

    # dssabled for single camera show
    # if key == 190: # F1 key: Toggle Camera
    #     index = (Webcam.current + 1) % 2 # hardcoded for 2 cameras
    #     Webcam.get().motiondetector.camera = Webcam.set(Device[index])
    #     log.warning('{}:{} {} {}'.format('F1',key,'F1','TOGGLE CAMERA'))
    #     return

    if key == 112: # p key : pause/unpause motion detection
        Webcam.get().motiondetector.is_paused = not Webcam.get().motiondetector.is_paused
        log.warning('{}:{} {} {}:{}'.format('F2',key,'P','PAUSE',Webcam.get().motiondetector.is_paused))
        return

    if key == 96: # `(tilde) key: toggle HUD
        Viewport.b_show_HUD = not Viewport.b_show_HUD
        log.warning('{}:{} {} {}'.format('F3',key,'`','TOGGLE HUD'))
        return

    if key == 49: # 1 key : toggle motion detect window
        Viewport.motiondetect_log_enabled = not Viewport.motiondetect_log_enabled
        if Viewport.motiondetect_log_enabled:
            cv2.namedWindow('delta',cv2.WINDOW_AUTOSIZE)
        else:
            cv2.destroyWindow('delta')
        log.warning('{}:{} {} {}'.format('F4',key,'1','MOTION MONITOR'))
        return

    # --------------------------------

    if key == 27: # ESC: Exit
        log.warning('{}:{} {} {}'.format('**',key,'ESC','SHUTDOWN'))
        Viewport.shutdown()
        Webcam.get().motiondetector.export.close() # close the motion detector data export file
        return

# a couple of utility functions for converting to and from Caffe's input image layout
def rgb2caffe(net, image):
    return np.float32(np.rollaxis(image, 2)[::-1]) - net.transformer.mean['data']

def caffe2rgb(net, image):
    return np.dstack((image + net.transformer.mean['data'])[::-1])

def objective_L2(dst):
    dst.diff[:] = dst.data

def objective_guide(dst):
    x = dst.data[0].copy()
    y = Model.guide_features
    ch = x.shape[0]
    x = x.reshape(ch,-1)
    y = y.reshape(ch,-1)
    A = x.T.dot(y) # compute the matrix of dot produts with guide features
    dst.diff[0].reshape(ch,-1)[:] = y[:,A.argmax(1)] # select one that matches best

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


def make_step(net, step_size=1.5, end='inception_4c/output', jitter=32, clip=False, feature=-1, objective=objective_L2):

    log.info('step_size:{} feature:{} end:{}\n{}'.format(step_size, feature, end,'-'*10))
    src = net.blobs['data']
    dst = net.blobs[end]

    ox, oy = np.random.randint(-jitter, jitter+1, 2)
    src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2)
    net.forward(end=end)

    if feature == -1:
        objective(dst)
    else:
        dst.diff.fill(0.0)
        dst.diff[0,feature,:] = dst.data[0,feature,:]

    net.backward(start=end)
    g = src.diff[0]
    src.data[:] += step_size/np.abs(g).mean() * g
    src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2)

    if clip:
        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 200-bias)

    src.data[0] = postprocess_step(net, src.data[0])

    # program sequencer. don't run if program_duration is -1 though
    program_elapsed_time = time.time() - Model.program_start_time
    if Model.program_duration != -1:
        if program_elapsed_time > Model.program_duration:
            Model.next_program()

def remapValuetoRange(val, src, dst):
    # src [min,max] old range
    # dst [min,max] new range
    remapped_Value = ((val-src[0])/(src[1]-src[0]))*(dst[1]-dst[0])+dst[0]
    return clamp(remapped_Value, [0.0, 1.0])

# clamps provided value between provided range
def clamp(value, range):
    return max( range[0], min(value, range[1]))

# -------
# REM CYCLE
# -------
def deepdream(net, base_image, iteration_max=10, octave_n=4, octave_scale=1.4, end='inception_4c/output', clip=True, **step_params):

    motion = Webcam.get().motiondetector

    Composer.cycle_count += 1

    # SETUP OCTAVES
    src = Model.net.blobs['data']
    octaves = [rgb2caffe(Model.net, base_image)]
    for i in xrange(octave_n - 1):
        octaves.append(nd.zoom(octaves[-1], (1, round((1.0 / octave_scale),2), round((1.0 / octave_scale),2)), order=1))
    detail = np.zeros_like(octaves[-1])

    for octave, octave_current in enumerate(octaves[::-1]):
        h, w = octave_current.shape[-2:]
        h1, w1 = detail.shape[-2:]
        detail = nd.zoom(detail, (1, 1.0 * h / h1, 1.0 * w / w1), order=0)
        src.reshape(1,3,h,w)
        src.data[0] = octave_current + detail
        Model.stepsize = Model.stepsize_base # reset step size to default each octave
        step_params['step_size'] = Model.stepsize # modify the **step_params list for makestep

        # OCTAVE CYCLE
        i=0
        while i < iteration_max:
            # handle vieport refresh per iteration
            if Viewport.force_refresh:
                log.warning('**** Viewport Force refresh ****')
                Viewport.force_refresh = False
                return Webcam.get().read()

            make_step(Model.net, end=end, clip=clip, **step_params)

            motion.peak_last = motion.peak
            motion.peak = motion.delta_count_history_peak

            # is peak value increasing or decreasing?
            motion.peak_avg = (motion.peak+motion.peak_last)/2

            if motion.peak > motion.peak_avg:
                motion.peak_statusmsg = '+++++'
            else:
                if motion.peak == motion.peak_avg:
                    motion.peak_statusmsg = '.'
                else:
                    motion.peak_statusmsg = '-----'
                    # if motion.delta_count > motion.delta_trigger:
                    #     Viewport.refresh()

            log.debug(motion.peak_statusmsg)

            if motion.delta_count > motion.delta_trigger:
                Viewport.refresh()

            if motion.peak < motion.floor:
                Composer.opacity -= 0.1
                if Composer.opacity <= 0.1:
                    Composer.opacity = 0.0
            else:
                Composer.opacity = remapValuetoRange(
                    motion.delta_count_history,
                    [0.0, 100000.0],
                    [0.0, 1.0]
                )


            log.debug(
                'count:{:>06} trigger:{:>06} peak:{:>06} opacity:{:03.2}'
                .format(
                    motion.delta_count,
                    motion.delta_trigger,
                    motion.delta_count_history_peak,
                    Composer.opacity
                )
            )

            # update Composer buffers
            Composer.send(0, caffe2rgb(Model.net, src.data[0]))
            Composer.send(1, Webcam.get().read())

            # send the main mix to the viewport
            comp1 = Composer.mix( Composer.buffer[0], Composer.buffer[1], Composer.opacity)


            Viewport.show(comp1)

            # attenuate step size over rem cycle
            x = step_params['step_size']
            step_params['step_size'] += x * Model.step_mult * 1.0

            # set a floor for any cyclefx step modification
            if step_params['step_size'] < 1.1:
                step_params['step_size'] = 1.1

            # increment step
            i += 1

            # LOGGING
            log.warning('{:02d} {:02d} {:02d} peak:{} peak_history:{}'.format(octave, i, iteration_max, motion.peak, motion.peak_last))

            # HUD logging
            octavemsg = '{}/{}({})'.format(octave,octave_n,Model.octave_cutoff)
            guidemsg = '({}/{}) {}'.format(Model.current_guide,len(Model.guides),Model.guides[Model.current_guide])
            iterationmsg = '{:0>3}:{:0>3} x{}'.format(i,iteration_max,Model.iteration_mult)
            stepsizemsg = '{:02.3f} x{:02.3f}'.format(step_params['step_size'],Model.step_mult)
            thresholdmsg = '{:0>6}'.format(motion.delta_trigger)
            floormsg = '{:0>6}'.format(motion.floor)
            gammamsg = '{}'.format(Webcam.get().gamma)
            intervalmsg = '{:01.2f}/{:01.2f}'.format(round(time.time() - Model.program_start_time, 2), Model.program_duration)
            update_HUD_log('octave',octavemsg)
            update_HUD_log('width',w)
            update_HUD_log('height',h)
            update_HUD_log('guide',guidemsg)
            update_HUD_log('iteration',iterationmsg)
            update_HUD_log('step_size',stepsizemsg)
            update_HUD_log('scale',Model.octave_scale)
            update_HUD_log('program',Model.package_name)
            update_HUD_log('threshold',thresholdmsg)
            update_HUD_log('floor',floormsg)
            update_HUD_log('gamma',gammamsg)
            update_HUD_log('interval', intervalmsg)
            update_HUD_log('runtime', round(time.time() - Model.installation_startup, 2))

        # SETUP FOR NEXT OCTAVE
        # extract details produced on the current octave
        detail = src.data[0] - octave_current  # these feed into next octave presumably?

        # calulate iteration count for the next octave
        iteration_max = int(iteration_max - (iteration_max * Model.iteration_mult))

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
    now = time.time() # start timer
    caffe.set_device(0)
    caffe.set_mode_gpu()
    iterations = Model.iterations
    stepsize = Model.stepsize_base
    octaves = Model.octaves
    octave_scale = Model.octave_scale
    jitter = 300

    # logging
    update_HUD_log('model',Model.caffemodel)
    update_HUD_log('username',Viewport.username)
    update_HUD_log('settings',Model.package_name)

    # the madness begins
    initial_image = Webcam.get().read()
    Composer.send(1, initial_image)
    Composer.dreambuffer = initial_image # initial camera image for starting

    while True:
        log.debug('new cycle')
        FX.set_cycle_start_time(time.time()) # register cycle start for duration_cutoff stepfx

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
            objective=objective_L2,
            iteration_max = Model.iterations,
            octave_n = Model.octaves,
            octave_scale = Model.octave_scale,
            step_size = Model.stepsize_base,
            end = Model.end,
            feature = Model.features[Model.current_feature]
            )

        Composer.dreambuffer = Composer.update(Composer.dreambuffer)

        # logging
        later = time.time()
        duration_msg = '{:.2f}s'.format(later - now)
        now = time.time() # the new now
        update_HUD_log('cycle_time',duration_msg)
        log.warning('cycle time: {}\n{}'.format(duration_msg,'-'*80))



# --------
# INIT
# --------

# --- LOGGING ---
logging.config.dictConfig(LogSettings.LOGGING_CONFIG)
log = logging.getLogger('logtest-debug')
log.setLevel(logging.WARNING)


# log.debug('debug message!')
# log.info('info message!')
# log.warning('warning message')
# log.error('error message')
# log.critical('critical message')
# sys.exit(0)





# --- CAMERA ---
Camera = [] # global reference to camera collection


Camera.append(WebcamVideoStream(0, data.capture_w, data.capture_h, portrait_alignment=False, log=update_HUD_log, flip_h=False, flip_v=False, gamma=0.5, floor=10000, threshold_filter=8).start())
Webcam = Cameras(source=Camera, current_camera=0)

# --- DISPLAY ---
Display = Display(width=data.capture_w, height=data.capture_h, camera=Webcam.get())
Viewport = Viewport('deepdreamvisionquest','silent', listener) # no screenshots if username 'silent'
Composer = Composer()

# --- PERFORMANCE SETTINGS AND rFX ---c
Model = Model(program_duration=45) # seconds each program will run, -1 is manual
Model.set_program(0)
FX = FX()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--username',help='twitter userid for sharing')
    parser.add_argument('--cameraID',help='camera device ID to use as video input')
    args = parser.parse_args()
    if args.username:
        Viewport.username = '@{}'.format(args.username)
    # if args.cameraID:


    main()
