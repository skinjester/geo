import numpy as np
import cv2

# logging
import logging
import logging.config
import logsettings

logging.config.dictConfig(logsettings.LOGGING_CONFIG)

now = 0  # timing reference updated each rem cycle

guides = []
guides.append('./img/gaudi1.jpg')
guides.append('./img/gaudi2.jpg')
guides.append('./img/house1.jpg')
guides.append('./img/eagle1.jpg')
guides.append('./img/tiger.jpg')
guides.append('./img/cat.jpg')
guides.append('./img/sax2.jpg')
guides.append('./img/bono.jpg')
guides.append('./img/rabbit2.jpg')
guides.append('./img/eyeballs.jpg')

# this is written to by rem.py at runtime so that it points to Composer.buffer1
# I'm using it like a scratchpad, but initializes to None
data_img = None

# opencv font and color
FONT = cv2.FONT_HERSHEY_SIMPLEX
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# image I/O
capturesize = (1280, 720)
viewsize = (720, 1280)

# outreach
username = "dev"  # can be overriden w commandline

# monitor coordinates for window placement
MONITOR_MAIN = (0, 0)
MONITOR_SECOND = (2560, 0)
MONITOR_TV = (0, 0)
MONITOR_PROJECTOR = (0, 0)

# motion detector
floor_adjust = 5000  # default step size for motion floor adjustment


# utility functions
def rgb2caffe(net, image):
    return np.float32(np.rollaxis(image, 2)[::-1]) - net.transformer.mean[
        'data']


def caffe2rgb(net, image):
    return np.dstack((image + net.transformer.mean['data'])[::-1])

# deprecated
def remapValuetoRange(val, src, dst):
    # src [min,max] old range
    # dst [min,max] new range
    remapped_Value = ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + \
                     dst[0]
    return clamp(remapped_Value, [0.0, 1.0])

def remap(in_value, in_minmax=[-1,1], out_minmax=[-1,1]):
    return (
            in_value - in_minmax[0]
        ) / (
            in_minmax[1] - in_minmax[0]
        ) * (
            out_minmax[1] - out_minmax[0]
        ) + out_minmax[0]

# clamps provided value between provided range
def clamp(value, range):
    return max(range[0], min(value, range[1]))

