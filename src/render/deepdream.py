import data
import sys
import hud.console as console
import scipy.ndimage as nd
import cv2
import math, numpy as np
from random import randint
import postprocess
import thread


# def objective_guide(dst):
#     x = dst.data[0].copy()
#     y = Model.guide_features
#     ch = x.shape[0]
#     x = x.reshape(ch, -1)
#     y = y.reshape(ch, -1)
#     A = x.T.dot(y)  # compute the matrix of dot produts with guide features
#     dst.diff[0].reshape(ch, -1)[:] = y[:,
#     A.argmax(1)]  # select one that matches best



def objective_L2(dst):
    dst.diff[:] = dst.data

# unimplemented guideed dreaming
def objective_guide(dst):
    x = dst.data[0].copy()
    y = Model.guide_features
    ch = x.shape[0]
    x = x.reshape(ch, -1)
    y = y.reshape(ch, -1)
    A = x.T.dot(y)
    dst.diff[0].reshape(ch, -1)[:] = y[:,
    A.argmax(1)]

class Artist(object):
    def __init__(self, id, webcam):
        self.id = id
        self.b_wakeup = True
        self.b_capture_now = False
        self.cycle_start_time = 0
        self.repeat = 0
        self.new_cycle = True
        self.webcam = webcam

    def paint(self,
        Model,
        base_image,
        iteration_max,
        iteration_mult,
        octave_n,
        octave_cutoff,
        octave_scale,
        end,
        objective,
        stepsize_base,
        step_mult,
        feature,
        stepfx,
        Webcam,
        Composer,
        clip=False
        ):


        # # SETUP OCTAVES
        src = Model.net.blobs['data']
        octaves = [data.rgb2caffe(Model.net, base_image)]
        log.warning('octave_n: {}'.format(octave_n))

        if Model.cyclefx is not None:
         for fx in Model.cyclefx:
             if fx['name'] == 'octave_scaler':
                 Model.octave_scale = round(postprocess.octave_scaler(fx['osc']),4)
                 log.warning('octave_scale: {}'.format(Model.octave_scale))

        for i in xrange(octave_n - 1):
            octaves.append(nd.zoom(octaves[-1], (1, round((1.0 / octave_scale), 2), round((1.0 / octave_scale), 2)), order=1))
        detail = np.zeros_like(octaves[-1])

        step_size=stepsize_base
        for octave, octave_current in enumerate(octaves[::-1]):
            h, w = octave_current.shape[-2:]
            h1, w1 = detail.shape[-2:]
            detail = nd.zoom(detail, (1, 1.0 * h / h1, 1.0 * w / w1), order=0)
            src.reshape(1, 3, h, w)
            src.data[0] = octave_current + detail

            # OCTAVE CYCLE
            i = 1
            while i <= iteration_max:
                if self.was_wakeup_requested():
                    self.clear_request()
                    # data.img_wakeup = Webcam.get().read()
                    return

                self.make_step(Model=Model,
                    step_size=step_size,
                    end=end,
                    feature=feature,
                    objective=objective,
                    stepfx=stepfx,
                    jitter=200)

                if octave > 1:
                    self.new_cycle = False

                console.log_value('octave', '{}/{}({})'.format(octave+1, octave_n, octave_cutoff))
                console.log_value('iteration', '{:0>3}:{:0>3} x{}'.format(i, iteration_max, iteration_mult))
                console.log_value('step_size','{:02.3f} x{:02.3f}'.format(step_size, step_mult))
                console.log_value('width', w)
                console.log_value('height', h)
                console.log_value('scale', octave_scale)

                log.critical('{}/{}({}) {}/{}'.format(octave+1, octave_n, octave_cutoff,i,iteration_max))

                data.vis = data.caffe2rgb(Model.net,src.data[0])
                data.vis = data.vis * (255.0 / np.percentile(data.vis, 99.98))
                step_size += stepsize_base * step_mult
                if step_size < 0.1:
                    step_size = 0.1
                i += 1
                detail = src.data[0] - octave_current
                if octave > octave_cutoff:
                    break
            iteration_max = int(iteration_max - (iteration_max * iteration_mult))

        if self.was_photo_requested():
            self.clear_photo_request()
            data.Viewport.export()
        return

    def make_step(self, Model, step_size, end, feature, objective, stepfx, jitter):
        src = Model.net.blobs['data']
        dst = Model.net.blobs[end]
        ox, oy = np.random.randint(-jitter, jitter + 1, 2)
        src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2)
        try:
            Model.net.forward(end=end)
        except:
            log.critical('MISSING LAYER')

        try:
            if feature == -1:
                objective(dst)
            else:
                dst.diff.fill(0.0)
                dst.diff[0, feature, :] = dst.data[0, feature, :]
            Model.net.backward(start=end)
            g = src.diff[0]
            if np.abs(g).mean() * g.any() != 0:
                src.data[:] += step_size / np.abs(g).mean() * g
                src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2)
                bias = Model.net.transformer.mean['data']
                src.data[:] = np.clip(src.data, -bias, 255 - bias)
                src.data[0] = self.postprocess_step(Model, src.data[0], stepfx)
        except KeyboardInterrupt:
            sys.exit()
        except:
            log.critical('RENDERINGERROR')


    def postprocess_step(self, Model, src, stepfx):
        rgb = data.caffe2rgb(Model.net, src)
        rgb_out = rgb.copy()
        opacity = 1.0
        for fx in stepfx:
            if fx['name'] == 'median_blur':
                rgb = postprocess.median_blur(rgb, fx['osc'])
            if fx['name'] == 'bilateral_filter':
                rgb = postprocess.bilateral_filter(rgb, fx['osc1'], fx['osc2'], fx['osc3'])
            if fx['name'] == 'gaussian':
                rgb = postprocess.nd_gaussian(src, fx['osc'])
                rgb = data.caffe2rgb(Model.net, rgb)

        for fx in stepfx:
            if fx['name'] == 'step_mixer':
                opacity = postprocess.step_mixer(fx['osc'])
        rgb_out = cv2.addWeighted(rgb, opacity, rgb_out, 1.0-opacity, 0.0)
        return data.rgb2caffe(Model.net, rgb_out)

    def request_wakeup(self):
        self.b_wakeup = True
        data.img_wakeup = self.webcam.get().read()
        log.warning('request new')

    def was_wakeup_requested(self):
        return self.b_wakeup

    def clear_request(self):
        self.b_wakeup = False

    def request_photo(self):
        self.b_capture_now = True
        pass

    def was_photo_requested(self):
        return self.b_capture_now
        pass

    def clear_photo_request(self):
        self.b_capture_now = False
        pass

    def set_cycle_start_time(self, start_time):
        self.cycle_start_time = start_time
        self.new_cycle = True
# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.WARNING)
