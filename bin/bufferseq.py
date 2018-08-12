import cv2, data, numpy as np, math
from scipy import signal as sg
from itertools import cycle
data.FONT = cv2.FONT_HERSHEY_SIMPLEX
frameCount = 100  # zero-indexed
frameWidth = 800
frameHeight = 600


def counter(frameCount):
    value = 0
    yield value
    while True:
        value += 1
        if value > frameCount - 1:
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
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2,2))
    equalized = clahe.apply(gray)
    img = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
    return img

def portrait(img):
     return cv2.flip(cv2.transpose(img),0)

def main(timeline, ramp):
    buf = np.empty((frameCount, frameWidth, frameHeight, 3), np.dtype('uint8'))

    cv2.namedWindow('webcam',cv2.WINDOW_NORMAL)
    cv2.namedWindow('playback',cv2.WINDOW_NORMAL)

    cameras = []
    cameras.append(cv2.VideoCapture(0))
    frame=0
    rampvalue = 0

    for index,camera in enumerate(cameras):
        camera.set(3,frameWidth)
        camera.set(4,frameHeight)

    while True:
        for index,camera in enumerate(cameras):
            frame = timeline.next()

            # image capture
            ret, img = camera.read()
            img = equalize(portrait(img))

            # buffer write
            buf=np.roll(buf,1,axis=0)
            buf[0] = img

            # image write - webcam
            cv2.putText(img,'camera {}'.format(index),(10,20), data.FONT, 0.51, (0,255,0), 1, cv2.LINE_AA)
            cv2.imshow('webcam', img)

            # image write - buffer
            if frame % 2 == 0:
                rampvalue = int(ramp.next())
            cv2.imshow('playback', buf[rampvalue])

            log.debug('timeline:{} ramp:{}'.format(frame, rampvalue))

        key = cv2.waitKey(10) & 0xFF
        if key == 27: # ESC
            cv2.destroyAllWindows()
            for camera in cameras:
                camera.release()
            break



if __name__ == '__main__':
    # CRITICAL ERROR WARNING INFO DEBUG
    log = data.logging.getLogger('mainlog')
    log.setLevel(data.logging.DEBUG)
    _count = counter(frameCount)
    # _ramp = oscillator(
    #                 cycle_length = 30,
    #                 frequency = 1,
    #                 range_out = [30.0,60.0],
    #                 wavetype = 'square',
    #                 dutycycle = 0.5
    #             )
    _ramp = cycle([0,15,30,45,60,75,90])
    main(timeline=_count, ramp=_ramp)


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
