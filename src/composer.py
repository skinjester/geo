import data, postprocess, time, threading
import hud.console as console
import cv2, numpy as np

class Composer(object):
    def __init__(self):
        emptybuffer = np.zeros((data.viewsize[1], data.viewsize[0], 3), np.uint8)
        self.buffer = []
        self.buffer.append(emptybuffer)
        self.buffer.append(emptybuffer)
        self.mixbuffer = emptybuffer
        self.dreambuffer = emptybuffer
        self.opacity = 0
        self.stopped = False
        self.counter = 0

    def start(self):
        threadlog.critical('start composer thread')
        composer_thread = threading.Thread(target=self.update, name='composer')
        composer_thread.setDaemon(True)
        composer_thread.start()
        return self

    def stop(self):
        self.stopped = True
        threadlog.critical('stop composer thread')

    def update(self):
        while True:
            if self.stopped:
                return
            motion = data.Webcam.get().motiondetector
            motion.peak_last = motion.peak
            motion.peak = motion.delta_history_peak

            self.opacity = 0.5
            if not data.Webcam.get().motiondetector.is_paused:
                if motion.delta > motion.delta_trigger:
                    data.Renderer.request_wakeup()
                    if data.Model.autofeature:
                        data.Model.next_feature()
                    self.counter = 0
                    self.opacity -= 0.1
                    if self.opacity < 0:
                        self.opacity = 0
                else:
                    if self.counter < 10:
                        self.counter += 0.5
                    if self.counter > 10:
                        self.counter = 10
                    if self.counter == 10:
                        self.opacity += 0.1
                        if self.opacity > 1.0:
                            self.opacity = 1.0
                camera_img = data.Webcam.get().read()


            self.send(0, data.vis)
            self.send(1, camera_img)
            self.dreambuffer = self.mix(self.buffer[0], self.buffer[1], self.opacity, gamma=1.0)
            data.playback = self.dreambuffer
            # data.playback = postprocess.equalize(self.dreambuffer)
            if data.Model.stepfx is not None:
                for fx in data.Model.stepfx:
                    if fx['name'] == 'slowshutter':
                        data.playback = data.Framebuffer.slowshutter(
                            data.playback ,
                            samplesize=fx['osc1'].next(),
                            interval=fx['osc2'].next()
                            )
                    if fx['name'] == 'featuremap':
                        data.Model.set_featuremap(index=fx['osc1'].next())
            data.Viewport.show(data.playback)

            console.log_value('runtime', '{:0>2}'.format(round(time.time() - data.Model.installation_startup, 2)))
            console.log_value('interval', '{:01.2f}/{:01.2f}'.format(round(time.time() - data.Model.program_start_time, 2), data.Model.program_duration))

            # program sequencer. don't run if program_duration is -1 though
            if data.Model.program_running and data.Model.program_duration > 0:
                if time.time() - data.Model.program_start_time > data.Model.program_duration:
                    data.Model.next_program()

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

    def request_message(self):
        pass

    def was_message_requested():
        pass

    def clear_message_request():
        pass

# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.CRITICAL)
threadlog = data.logging.getLogger('threadlog')
threadlog.setLevel(data.logging.CRITICAL)

osc = postprocess.oscillator(
            cycle_length = 100,
            frequency = 1,
            range_out = [0.0, 0.5],
            wavetype = 'sin',
            dutycycle = 0.5
            )
