import data, postprocess, time
import hud.console as console
import cv2, numpy as np

class Composer(object):
    def __init__(self, Viewport):
        emptybuffer = np.zeros((data.viewsize[1], data.viewsize[0], 3), np.uint8)
        self.buffer = []
        self.buffer.append(emptybuffer)
        self.buffer.append(emptybuffer)
        self.mixbuffer = emptybuffer
        self.dreambuffer = emptybuffer
        self.opacity = 0
        self.Viewport = Viewport

    def send(self, channel, image):
        self.buffer[channel] = image
        self.buffer[channel] = cv2.resize(self.buffer[channel],
            (data.viewsize[0], data.viewsize[1]),
            interpolation=cv2.INTER_LINEAR)
        self.buffer[channel] = np.uint8(np.clip(self.buffer[channel], 0, 255))

    def get(self, channel):
        return self.buffer[channel]

    def mix(self, image_front, image_back, front_opacity, gamma):
        cv2.addWeighted(
            image_front,
            front_opacity,  #
            image_back,
            1 - front_opacity,
            gamma,
            self.mixbuffer
        )
        return self.mixbuffer

    def update(self, vis, Webcam, Model, Renderer):
        motion = Webcam.get().motiondetector
        motion.peak_last = motion.peak
        motion.peak = motion.delta_history_peak

        if motion.delta > motion.delta_trigger:
            Renderer.request_wakeup()
            Model.next_feature()
            self.opacity = 0.0
        else:
            self.opacity = osc.next()

        # compositing
        camera_img = Webcam.get().read()
        self.send(0, vis)
        self.send(1, camera_img)
        self.dreambuffer = self.mix(self.buffer[0], self.buffer[1], self.opacity, gamma=1.0)
        if Model.stepfx is not None:
            for fx in Model.stepfx:
                if fx['name'] == 'slowshutter':
                    data.playback = data.Framebuffer.slowshutter(
                        self.dreambuffer ,
                        samplesize=fx['osc1'].next(),
                        interval=fx['osc2'].next()
                        )
                    # self.send(0,img_avg)
                if fx['name'] == 'featuremap':
                    Model.set_featuremap(index=fx['osc1'].next())


        self.Viewport.show(data.playback)


        console.log_value('runtime', '{:0>2}'.format(round(time.time() - Model.installation_startup, 2)))
        console.log_value('interval', '{:01.2f}/{:01.2f}'.format(round(time.time() - Model.program_start_time, 2), Model.program_duration))

        # program sequencer. don't run if program_duration is -1 though
        if Model.program_running and Model.program_duration > 0:
            if time.time() - Model.program_start_time > Model.program_duration:
                Model.next_program()

# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.CRITICAL)

osc = postprocess.oscillator(
            cycle_length = 10,
            frequency = 1,
            range_out = [-0.1, 1.5],
            wavetype = 'square',
            dutycycle = 0.5
            )
