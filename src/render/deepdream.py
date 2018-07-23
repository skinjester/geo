import data
import hud.console as console
import scipy.ndimage as nd
import math, numpy as np
from random import randint


# def objective_guide(dst):
#     x = dst.data[0].copy()
#     y = Model.guide_features
#     ch = x.shape[0]
#     x = x.reshape(ch, -1)
#     y = y.reshape(ch, -1)
#     A = x.T.dot(y)  # compute the matrix of dot produts with guide features
#     dst.diff[0].reshape(ch, -1)[:] = y[:,
#     A.argmax(1)]  # select one that matches best









# def remapValuetoRange(val, src, dst):
#     # src [min,max] old range
#     # dst [min,max] new range
#     remapped_Value = ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + \
#                      dst[0]
#     return clamp(remapped_Value, [0.0, 1.0])

# # clamps provided value between provided range
# def clamp(value, range):
#     return max(range[0], min(value, range[1]))

# def postprocess_step(net, net_data_blob):
#     # takes neural net data blob and converts to RGB
#     # then after processing, takes the RGB image and converts back to caffe
#     image = caffe2rgb(net, net_data_blob)

#     #  apply any defined stepFX
#     if Model.stepfx is not None:
#         for fx in Model.stepfx:
#             if fx['name'] == 'median_blur':
#                 image = FX.median_blur(image, **fx['params'])

#             if fx['name'] == 'bilateral_filter':
#                 image = FX.bilateral_filter(image, **fx['params'])

#             if fx['name'] == 'nd_gaussian':
#                 # image = net_data_blob

#                 image = FX.nd_gaussian(net_data_blob, **fx['params'])
#                 image = caffe2rgb(net, net_data_blob)

#             if fx['name'] == 'step_opacity':
#                 FX.step_mixer(**fx['params'])

#             if fx['name'] == 'duration_cutoff':
#                 FX.duration_cutoff(**fx['params'])

#             if fx['name'] == 'octave_scaler':
#                 FX.octave_scaler(model=Model, **fx['params'])

#     # image = cv2.addWeighted(image, FX.stepfx_opacity, image, 1.0-FX.stepfx_opacity, 0, image)
#     return rgb2caffe(Model.net, image)

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
        log.debug('dreaming with Render instance: {}'.format(self.id))

    def paint(self,
        net,
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
        Webcam,
        Composer,
        Viewport,
        clip=False
        ):

        # # SETUP OCTAVES
        src = net.blobs['data']
        octaves = [data.rgb2caffe(net, base_image)]
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

                self.make_step(net,
                    step_size=step_size,
                    end=end,
                    feature=feature,
                    objective=objective,
                    jitter=32)

                vis = data.caffe2rgb(net,src.data[0])
                vis = vis * (255.0 / np.percentile(vis, 99.98))
                Composer.update(vis, Webcam)

                step_size += stepsize_base * step_mult
                if step_size < 1.1:
                    step_size = 1.1
                i += 1

            detail = src.data[0] - octave_current
            iteration_max = int(iteration_max - (iteration_max * iteration_mult))
            if octave > octave_cutoff - 1:
                log.critical('cutoff at octave: {}'.format(octave))
                break

        log.critical('completed rem cycle')
        return data.caffe2rgb(net, src.data[0])


    def make_step(self, net, step_size, end, feature, objective, jitter):
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

        bias = net.transformer.mean['data']
        src.data[:] = np.clip(src.data, -bias, 255 - bias)

        # src.data[0] = postprocess_step(net, src.data[0])

        # program sequencer. don't run if program_duration is -1 though
        # elapsed = time.time() - Model.program_start_time
        # if Model.program_running:
        #     if elapsed > Model.program_duration:
        #         Model.next_program()


    def request_wakeup(self):
        self.b_wakeup = True
        log.warning('request new')


    def was_wakeup_requested(self):
        return self.b_wakeup


    def clear_request(self):
        self.b_wakeup = False



# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.CRITICAL)
