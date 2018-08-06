import data
import hud.console as console
import scipy.ndimage as nd
import math, numpy as np
from random import randint
import postprocess


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
    def __init__(self, id):
        self.id = id
        self.b_wakeup = True
        self.cycle_start_time = 0
        log.debug('dreaming with Render instance: {}'.format(self.id))


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
        Viewport,
        clip=False
        ):

        # # SETUP OCTAVES
        src = Model.net.blobs['data']
        octaves = [data.rgb2caffe(Model.net, base_image)]
        log.warning('octave_n: {}'.format(octave_n))
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
            i = 0
            while i < iteration_max:
                if self.was_wakeup_requested():
                    self.clear_request()
                    return Webcam.get().read()

                self.make_step(Model=Model,
                    step_size=step_size,
                    end=end,
                    feature=feature,
                    objective=objective,
                    stepfx=stepfx,
                    jitter=32)

                console.log_value('octave', '{}/{}({})'.format(octave+1, octave_n, octave_cutoff))
                console.log_value('iteration', '{:0>3}:{:0>3} x{}'.format(i, iteration_max, iteration_mult))
                console.log_value('step_size','{:02.3f} x{:02.3f}'.format(step_size, step_mult))
                console.log_value('width', w)
                console.log_value('height', h)
                console.log_value('scale', octave_scale)

                vis = data.caffe2rgb(Model.net,src.data[0])
                vis = vis * (255.0 / np.percentile(vis, 99.98))
                Composer.update(vis, Webcam)
                step_size += stepsize_base * step_mult
                if step_size < 1.1:
                    step_size = 1.1
                i += 1

            detail = src.data[0] - octave_current
            iteration_max = int(iteration_max - (iteration_max * iteration_mult))
            if octave > octave_cutoff - 1:
                break

        return data.caffe2rgb(Model.net, src.data[0])

    def make_step(self, Model, step_size, end, feature, objective, stepfx, jitter):
        src = Model.net.blobs['data']
        dst = Model.net.blobs[end]
        ox, oy = np.random.randint(-jitter, jitter + 1, 2)
        src.data[0] = np.roll(np.roll(src.data[0], ox, -1), oy, -2)
        Model.net.forward(end=end)

        try:
            if feature == -1:
                objective(dst)
            else:
                dst.diff.fill(0.0)
                dst.diff[0, feature, :] = dst.data[0, feature, :]
        except:
            log.critical('ERROR')

        Model.net.backward(start=end)
        g = src.diff[0]
        src.data[:] += step_size / np.abs(g).mean() * g
        src.data[0] = np.roll(np.roll(src.data[0], -ox, -1), -oy, -2)
        bias = Model.net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255 - bias)

        src.data[0] = self.postprocess_step(Model, src.data[0], stepfx)

    def postprocess_step(self, Model, src, stepfx):
        rgb = data.caffe2rgb(Model.net, src)

        for fx in stepfx:
            # log.critical('{}'.format(stepfx))
            if fx['name'] == 'median_blur':
                rgb = postprocess.median_blur(rgb, **fx['params'])
            # if fx['name'] == 'bilateral_filter':
            #     rgb = postprocess.bilateral_filter(rgb, **fx['params'])
            # if fx['name'] == 'nd_gaussian':
            #     rgb = postprocess.nd_gaussian(src, **fx['params'])
            #     rgb = caffe2rgb(Model.net, src)
            # if fx['name'] == 'step_opacity':
            #     postprocess.step_mixer(**fx['params'])
            # if fx['name'] == 'duration_cutoff':
            #     postprocess.duration_cutoff(**fx['params'])
            # if fx['name'] == 'octave_scaler':
            #     postprocess.octave_scaler(model=Model, **fx['params'])

        # rgb = cv2.addWeighted(rgb, FX.stepfx_opacity, rgb, 1.0-FX.stepfx_opacity, 0, rgb)
        return data.rgb2caffe(Model.net, rgb)

    def request_wakeup(self):
        self.b_wakeup = True
        log.warning('request new')


    def was_wakeup_requested(self):
        return self.b_wakeup


    def clear_request(self):
        self.b_wakeup = False

    def set_cycle_start_time(self, start_time):
        self.cycle_start_time = start_time
# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.CRITICAL)
