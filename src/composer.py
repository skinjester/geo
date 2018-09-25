import data, postprocess, time
import hud.console as console
import cv2, numpy as np

class Composer(object):
    def __init__(self, Viewport):
        self.isDreaming = False
        self.xform_scale = 0.05
        self.emptybuffer = np.zeros((data.viewsize[1], data.viewsize[0], 3),
            np.uint8)
        self.buffer = []
        self.buffer.append(self.emptybuffer)
        self.buffer.append(self.emptybuffer)
        self.mixbuffer = self.emptybuffer
        self.dreambuffer = self.emptybuffer
        self.opacity = 0
        self.opacity_step = 0.1
        self.buffer3_opacity = 1.0
        self.running = True
        self.Viewport = Viewport

    def send(self, channel, image):
        self.buffer[channel] = image
        self.buffer[channel] = cv2.resize(self.buffer[channel],
            (data.viewsize[0], data.viewsize[1]),
            interpolation=cv2.INTER_LINEAR)
        self.buffer[channel] = np.uint8(np.clip(self.buffer[channel], 0, 255))

    def get(self, channel):
        return self.buffer[channel]

    def mix(self, image_back, image_front, mix_opacity, gamma):
        cv2.addWeighted(
            image_front,
            mix_opacity,  #
            image_back,
            1 - mix_opacity,
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
            if self.running == False:
                self.opacity += 0.1
            if self.opacity > 0.1:
                self.opacity =1.0
                self.running  = True
            else:
                self.opacity = osc.next()

        if motion.peak < motion.floor:
            self.opacity -= 0.05
            if self.opacity < 0.0:
                self.opacity = 0.0
                self.running = False
        else:
            Renderer.request_wakeup()
            self.opacity += 0.1
            if self.opacity > 1.0:
                self.opacity = 1.0
                self.running  = True

        # compositing
        camera_img = Webcam.get().read()
        self.send(0, vis)
        self.send(1, camera_img)
        data.playback = self.mix(self.buffer[0], self.buffer[1], self.opacity, gamma=1.0)
        # data.playback = postprocess.equalize(data.playback)
        if Model.stepfx is not None:
            for fx in Model.stepfx:
                if fx['name'] == 'slowshutter':
                    data.playback = data.Framebuffer.slowshutter(
                        data.playback,
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
            cycle_length = 100,
            frequency = 10,
            range_out = [-0.2,1.2],
            wavetype = 'sin',
            dutycycle = 0.5
            )
