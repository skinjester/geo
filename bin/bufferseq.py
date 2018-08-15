import cv2, data, numpy as np, math, random
from scipy import signal as sg
from itertools import cycle
data.FONT = cv2.FONT_HERSHEY_SIMPLEX
BUFFERSIZE = 100

def dcounter(func):
    def wrapper(*args, **kwargs):
        wrapper.counter +=1
        return func(*args, **kwargs)
    wrapper.counter=0
    return wrapper

def counter(maxvalue=10):
    value = 0
    yield value
    while True:
        value += 1
        if value >= maxvalue:
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
    def __init__(self, ramp, buffer_size, width, height):
        self.buffer_size = buffer_size
        self.width = width
        self.height = height
        self.storage = np.empty((self.buffer_size, self.width, self.height, 3), np.dtype('uint8'))
        self.viewport = self.storage
        self.range = 0
        self.playback_index = 0
        self.test = 0
        self.ramp = ramp

    def write(self, img):
        self.range += 1
        if self.range == self.buffer_size:
            self.range = 0
        self.storage=np.roll(self.storage,1,axis=0)
        self.storage[0] = img
        self.viewport = self.storage[0:self.range,:,:,:]
        self.counter = counter(self.range)
        self.ramp = oscillator(
                    cycle_length = BUFFERSIZE,
                    frequency = 1,
                    range_out = [0.0,50.0],
                    wavetype = 'saw',
                    dutycycle = 0.5)
        self.playback_index = 0
        log.critical('range:{} {}'.format(self.range,'.' * self.range))

    def show(self):
        if self.range<=1:
            return self.storage[0]
        rampvalue = int(self.ramp.next())
        self.playback_index = self.counter.next() - rampvalue
        log.critical('viewport shape:{} playback: {}'.format(self.viewport.shape, self.playback_index))
        self.viewport = np.roll(self.viewport,-1 * rampvalue,axis=0)
        return self.viewport[0]

def main(counter, ramp):
    framebuffer = Buffer(ramp,buffer_size=BUFFERSIZE,width=1280,height=720 )
    cv2.namedWindow('webcam',cv2.WINDOW_NORMAL)
    cv2.namedWindow('playback',cv2.WINDOW_NORMAL)
    frame = 0
    rampvalue = 0
    cameras = []
    cameras.append(cv2.VideoCapture(0))
    for index,camera in enumerate(cameras):
        camera.set(3,framebuffer.width)
        camera.set(4,framebuffer.height)

    while True:
        for index,camera in enumerate(cameras):
            frame = counter.next()
            rampvalue = int(ramp.next())
            log.critical('frame: {} ramp: {}'.format(frame, rampvalue))

            # image capture
            ret, img = camera.read()
            img = portrait(img)

            # if frame % (1 + rampvalue) == 0:
            #     framebuffer.write(img)

            if random.randint(1,1001) > 900:
                framebuffer.write(img)


            # image show - webcam
            cv2.putText(img,'camera: {} | frame: {}'.format(index, frame),(10,20), data.FONT, 0.51, (0,255,0), 1, cv2.LINE_AA)
            cv2.imshow('webcam', img)

            viewport = framebuffer.show()
            cv2.putText(viewport,'playback: {}'.format(framebuffer.playback_index),(10,20), data.FONT, 0.51, (0,255,0), 1, cv2.LINE_AA)
            cv2.imshow('playback', viewport)

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
    _count = counter(BUFFERSIZE)
    _ramp = oscillator(
                    cycle_length = 100,
                    frequency = 10,
                    range_out = [0.0,10.0],
                    wavetype = 'sin',
                    dutycycle = 0.5
                )
    # _ramp = cycle([0,15,30,45,60,75,90])
    main(counter=_count, ramp=_ramp)


# max 2304 x 1536
# 1920 x 1080
# 1600 x 896
# 1280 x 720
# 960 x 720
# 864 x 480
# 800 x 600
# 640 x 480
# 640 x 360
# 352 x 288
# 320 x 240
# 320 x 180


# horizontal = cv2.flip( img, 0 )
# vertical = cv2.flip( img, 1 )
# horizontal + vertical = cv2.flip( img, -1 )
