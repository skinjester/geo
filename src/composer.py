import data, postprocess, time, threading
import hud.console as console
import cv2, numpy as np

class Composer(object):
    def __init__(self):
        emptybuffer = np.zeros((data.viewsize[1], data.viewsize[0], 3), np.uint8)
        self.buffer = []
        self.buffer.append(emptybuffer)
        self.buffer.append(emptybuffer)
        self.buffer.append(emptybuffer)
        self.mixbuffer = emptybuffer
        self.dreambuffer = emptybuffer
        self.opacity = 0
        self.stopped = False
        self.motion_event_in_progress = False
        self.playback_ready = True


    def start(self):
        threadlog.warning('start composer thread')
        composer_thread = threading.Thread(target=self.update, name='composer')
        composer_thread.setDaemon(True)
        composer_thread.start()
        return self

    def stop(self):
        self.stopped = True
        threadlog.warning('stop composer thread')

    def update(self):
        while True:
            if self.stopped:
                return
            motion = data.Webcam.get().motiondetector
            motion.peak_last = motion.peak
            motion.peak = motion.delta_history_peak

            # not paused
            if not data.Webcam.get().motiondetector.is_paused:
                # only valid if detected when another event not in progress
                if motion.delta > motion.delta_trigger:
                    if not self.motion_event_in_progress:
                        self.motion_event_in_progress = True
                        data.Model.update_feature(release=1)
                # motion event in progress
                if self.motion_event_in_progress:
                    self.opacity -= 1
                    if self.opacity < 0.0:
                        self.opacity = 0.0
                        self.motion_event_in_progress = False
                        data.Renderer.request_wakeup()
                # no motion event in progress
                else:
                    self.opacity += 0.01
                    if self.opacity > 1.0:
                        self.opacity = 1.0

            # paused
            else:
                self.opacity = 1.0

            log.warning('requested:{} in progress: {} opacity: {:3.2f}'.format(data.Renderer.was_wakeup_requested(), self.motion_event_in_progress, self.opacity))

            self.send(0, data.vis)
            self.send(1, data.Webcam.get().read())

            data.Framebuffer.widetime_write(self.buffer[1])
            frame = counter.next()
            self.buffer[1] = data.Framebuffer.widetime(index=frame, interval=3)

            playback_old = data.playback.copy()
            data.playback = self.mix(self.buffer[0], self.buffer[1], self.opacity, gamma=1.0)
            data.playback = postprocess.equalize(data.playback, data.eq_clip, data.eq_grid)
            log.critical('eq clip: {} eq_grid: {}'.format(data.eq_clip, data.eq_grid))

            if data.Model.stepfx is not None:
                for fx in data.Model.stepfx:
                    if fx['name'] == 'slowshutter':
                        data.playback = data.Framebuffer.slowshutter(
                            data.playback ,
                            samplesize=fx['osc1'].next(),
                            interval=fx['osc2'].next()
                            )
                    # if fx['name'] == 'featuremap':
                    #     data.Model.set_featuremap(index=fx['osc1'].next())
                    # if fx['name'] == 'equalize':
                    #     data.playback = postprocess.equalize(self.dreambuffer, 2, (2,2))
                    # if fx['name'] == 'grayscale':
                    #     data.playback = postprocess.grayscale(data.playback)


            # display the update only if previous and current img are different
            # don't do anything if they're identical though
            img=data.playback
            if playback_old.shape == data.playback.shape:
                difference = cv2.subtract(data.playback, playback_old)
                b, g, r = cv2.split(difference)
                if cv2.countNonZero(b) != 0 and cv2.countNonZero(g) != 0 and cv2.countNonZero(r) != 0:
                    # playback "ready" only when new dream cycle completes 1st iteration
                    if self.playback_ready:
                        data.Framebuffer.write(data.playback)
                        # img = data.Framebuffer.cycle(repeat=6)
                # else:
                #     img = data.Framebuffer.cycle(repeat=5)
                data.Viewport.show(img)

            self.playback_ready = not data.Renderer.new_cycle

            # HUD logging
            console.log_value('runtime', '{:0>2}'.format(round(time.time() - data.Model.installation_startup, 2)))
            console.log_value('interval', '{:01.2f}/{:01.2f}'.format(round(time.time() - data.Model.program_start_time, 2), data.Model.program_duration))
            console.log_value('eq_clip', data.eq_clip)
            console.log_value('eq_grid', data.eq_grid)


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
            front_opacity,
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

def _counter(maxvalue=9999999):
    value = 0
    yield value
    while True:
        value += 1
        if value > maxvalue:
            value = 0
        yield value

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

counter = _counter()

