import cv2, data, numpy as np, math, random, time
from scipy import signal as sg
from itertools import cycle
data.FONT = cv2.FONT_HERSHEY_SIMPLEX
BUFFERSIZE = 30

def dcounter(func):
    def wrapper(*args, **kwargs):
        wrapper.counter +=1
        return func(*args, **kwargs)
    wrapper.counter=0
    return wrapper

def counter(maxvalue=99999):
    value = 0
    yield value
    while True:
        value += 1
        if value > maxvalue:
            value = 0
        yield value

def oscillator(cycle_length, frequency=1, range_in=[-1,1], range_out=[-1,1], wavetype='sin', dutycycle=0.5):
    timecounter = 0
    while True:
        timecounter += 1
        if wavetype=='square':
            value = range_out[0] + ((range_out[1] - range_out[0]) / 2) + sg.square(2 * math.pi * frequency * timecounter / cycle_length, duty=dutycycle) * ((range_out[1] - range_out[0]) / 2)
        elif wavetype=='saw':
            value = range_out[0] + ((range_out[1] - range_out[0]) / 2) + sg.sawtooth(2 * math.pi * frequency * timecounter / cycle_length) * ((range_out[1] - range_out[0]) / 2)
        else:
            value = range_out[0] + ((range_out[1] - range_out[0]) / 2) + math.sin(2 * math.pi * frequency * timecounter / cycle_length) * ((range_out[1] - range_out[0]) / 2)
        yield value

def equalize(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(4,4))
    equalized = clahe.apply(gray)
    img = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
    return img

def portrait(img):
     return cv2.flip(cv2.transpose(img),0)


class Buffer(object):
    def __init__(self, buffer_size, width, height):
        self.width = width
        self.height = height
        self.storage = np.empty((buffer_size, self.width, self.height, 3), np.dtype('uint8'))
        self.playback_counter = counter(buffer_size-1)
        self.playback_index = 0
        self.accumulated = np.zeros((self.width, self.height, 3), np.uint8)
        self.start_time = 0.0
        (self.rAvg, self.gAvg, self.bAvg) = (None, None, None)
        self.total = 0
        self.frame = counter(9999999)
        self.locked = False
        self.frame_repeat_count = 0

    def write(self, img):
        if not self.locked:
            self.storage=np.roll(self.storage,1,axis=0)
            self.storage[0] = img

    def cycle(self,repeat):
        self.frame_repeat_count += 1
        if self.frame_repeat_count >= repeat:
            self.playback_index = self.playback_counter.next()
            self.frame_repeat_count = 0
            self.locked = False
        else:
            self.locked = True
        return self.storage[self.playback_index]

    def widetime(self,delay,interval):
        if delay % interval == 0:
            alpha = 0.1
            beta = 1 - alpha
            gamma = 0.0
            img = self.storage[0]
            self.accumulated = cv2.addWeighted(img, alpha, self.accumulated, beta, gamma)
        return self.accumulated

    def slowshutter(self,img,samplesize=10,interval=1):
        if self.frame.next() % interval != 0:
            return self.accumulated
        (B, G, R) = cv2.split(img.astype("float"))
        if self.rAvg is None:
            self.rAvg = R
            self.bAvg = B
            self.gAvg = G
        else:
                self.rAvg = ((samplesize * self.rAvg) + (1 * R)) / (samplesize + 1.0)
                self.gAvg = ((samplesize * self.gAvg) + (1 * G)) / (samplesize + 1.0)
                self.bAvg = ((samplesize * self.bAvg) + (1 * B)) / (samplesize + 1.0)
        self.accumulated = cv2.merge([self.bAvg, self.gAvg, self.rAvg]).astype("uint8")
        return self.accumulated


def main(counter, ramp):
    framebuffer = Buffer(buffer_size=BUFFERSIZE,width=1280,height=720)
    cv2.namedWindow('webcam',cv2.WINDOW_NORMAL)
    cv2.namedWindow('playback',cv2.WINDOW_NORMAL)
    frame = 0
    rampvalue = 0
    cameras = []
    start_time = time.time()
    img_new = np.zeros((framebuffer.width, framebuffer.height, 3), np.uint8)
    cameras.append(cv2.VideoCapture(0))
    for index,camera in enumerate(cameras):
        camera.set(3,framebuffer.width)
        camera.set(4,framebuffer.height)
    osc = oscillator(
                    cycle_length = 100,
                    frequency = 1,
                    range_out = [1,5.0],
                    wavetype = 'sawtooth',
                    dutycycle = 0.5
                    )
    osc2 = oscillator(
                    cycle_length = 100,
                    frequency = 3,
                    range_out = [5,20],
                    wavetype = 'square',
                    dutycycle = 0.5
                    )

    osc3 = oscillator(
                    cycle_length = 100,
                    frequency = 3,
                    range_out = [0.0,0.3],
                    wavetype = 'sin',
                    dutycycle = 0.5
                    )

    while True:
        for index,camera in enumerate(cameras):
            frame = counter.next()
            rampvalue = ramp.next()

            # image capture
            ret, img = camera.read()
            img = portrait(img)
            cv2.imshow('webcam', img)

            # -------- TEST BLOCK FOR WIDETIME --------
            # log.debug('ramp: {}'.format(rampvalue))
            # if frame % 10 == 0:
            #     log.critical('capture')
            #     framebuffer.write(img)
            # img_new = framebuffer.widetime(delay=frame,interval=4)

            # -------- TEST BLOCK FOR CYCLE --------

            # ---- CYCLICAL FRAME SAMPLING DEMO ----
            # log.debug('ramp: {}'.format(rampvalue))
            # if frame % int(rampvalue) == 0:
            #     framebuffer.write(img)


            # ---- TIME FRAME SAMPLING DEMO ----
            # if time.time() - start_time > 0.3:
            #     framebuffer.write(img)
            #     start_time = time.time()
            #     log.debug('capture')
            # img_new = framebuffer.cycle(delay=1.0)

            # -------- TEST BLOCK FOR LONG EXPOSURE --------
            framebuffer.write(img)
            osc_value = osc.next()
            osc_value2 = osc2.next()
            log.debug('osc1:{} osc2:{}'.format(osc_value,osc_value2))
            img_new = framebuffer.slowshutter(img,samplesize=10,interval=3)


            # ---- RANDOM FRAME SAMPLING DEMO ----
            # if random.randint(1,1001) > 550:
            #     log.critical('capture -----------------------')
            #     framebuffer.write(img_new)
            # img_new = framebuffer.cycle(repeat=3)

            # PLAYBACK
            cv2.imshow('playback', img_new)

        key = cv2.waitKey(10) & 0xFF
        if key == 27: # ESC
            cv2.destroyAllWindows()
            for camera in cameras:
                camera.release()
            break

if __name__ == '__main__':
    # CRITICAL ERROR WARNING INFO DEBUG
    log = data.logging.getLogger('mainlog')
    log.setLevel(data.logging.CRITICAL)
    count = counter(BUFFERSIZE)
    ramp = oscillator(
                    cycle_length = 100,
                    frequency = 10,
                    range_out = [0.0,30.0],
                    wavetype = 'sin',
                    dutycycle = 0.5
                )
    # _ramp = cycle([0,15,30,45,60,75,90])
    main(counter=count, ramp=ramp)
