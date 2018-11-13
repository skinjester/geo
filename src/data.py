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
viewsize = (1280, 720)

# capturesize = (1280, 720)
# viewsize = (720, 1280)

# capturesize = (1920, 1080)
# viewsize = (1080, 1920)

# outreach
username = "dev"  # can be overriden w commandline

# monitor coordinates for window placement
MONITOR_MAIN = (0, 0)
MONITOR_SECOND = (2560, 0)
MONITOR_TV = (0, 0)
MONITOR_PROJECTOR = (0, 0)

# motion detector
floor_adjust = 5000  # default step size for motion floor adjustment

# async playback?
playback = np.zeros((viewsize[1], viewsize[0], 3),np.uint8)

# store paused image for photo mode
pause_img = np.zeros((viewsize[1], viewsize[0], 3),np.uint8)

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


layers_googlenet = [
    {
        'name': 'pool1/3x3_s2',
        'features': range(-1,64)
    },
    {
        'name': 'conv1/7x7_s2',
        'features': range(-1,64)
    },
    {
        'name': 'conv2/3x3_reduce',
        'features': range(-1,64)
    },
    {
        'name': 'conv2/3x3',
        'features': range(-1,192)
    },
    {
        'name': 'pool2/3x3_s2',
        'features': range(-1,192)
    },
    {
        'name': 'conv2/norm2',
        'features': range(-1,192)
    },

    {
        'name': 'inception_3a/1x1',
        'features': range(-1,64)
    },
    {
        'name': 'inception_3a/3x3_reduce',
        'features': range(-1,96)
    },
    {
        'name': 'inception_3a/3x3',
        'features': range(-1,128)
    },
    {
        'name': 'inception_3a/5x5',
        'features': range(-1,32)
    },
    {
        'name': 'inception_3a/pool',
        'features': range(-1,192)
    },
    {
        'name': 'inception_3a/pool_proj',
        'features': range(-1,32)
    },
    {
        'name': 'inception_3a/output',
        'features': range(-1,256)
    },
    {
        'name': 'inception_3b/1x1',
        'features': range(-1,128)
    },
    {
        'name': 'inception_3b/3x3_reduce',
        'features': range(-1,128)
    },
    {
        'name': 'inception_3b/3x3',
        'features': range(-1,192)
    },
    {
        'name': 'inception_3b/5x5_reduce',
        'features': range(-1,32)
    },
    {
        'name': 'inception_3b/5x5',
        'features': range(-1,96)
    },
    {
        'name': 'inception_3b/pool',
        'features': range(-1,256)
    },
    {
        'name': 'inception_3b/pool_proj',
        'features': range(-1,64)
    },
    {
        'name': 'inception_3b/output',
        'features': range(-1,480)
    },
    {
        'name': 'inception_4a/1x1',
        'features': range(-1,192)
    },
    {
        'name': 'inception_4a/3x3_reduce',
        'features': range(-1,96)
    },
    {
        'name': 'inception_4a/3x3',
        'features': range(-1,208)
    },
    {
        'name': 'inception_4a/5x5_reduce',
        'features': range(-1,16)
    },
    {
        'name': 'inception_4a/5x5',
        'features': range(-1,48)
    },
    {
        'name': 'inception_4a/pool',
        'features': range(-1,480)
    },
    {
        'name': 'inception_4a/pool_proj',
        'features': range(-1,64)
    },
    {
        'name': 'inception_4a/output',
        'features': range(-1,512)
    },

    {
        'name': 'inception_4b/1x1',
        'features': range(-1,160)
    },
    {
        'name': 'inception_4b/3x3_reduce',
        'features': range(-1,112)
    },
    {
        'name': 'inception_4b/3x3',
        'features': range(-1,224)
    },
    {
        'name': 'inception_4b/5x5_reduce',
        'features': range(-1,24)
    },
    {
        'name': 'inception_4b/output',
        'features': range(-1,512)
    },
    {
        'name': 'inception_4b/pool',
        'features': range(-1,512)
    },
    {
        'name': 'inception_4b/pool_proj',
        'features': range(-1,64)
    },
    {
        'name': 'inception_4c/1x1',
        'features': range(-1,128)
    },
    {
        'name': 'inception_4c/3x3',
        'features': range(-1,256)
    },
    {
        'name': 'inception_4c/3x3_reduce',
        'features': range(-1,128)
    },
    {
        'name': 'inception_4c/5x5',
        'features': range(-1,64)
    },
    {
        'name': 'inception_4c/5x5_reduce',
        'features': range(-1,24)
    },
    {
        'name': 'inception_4c/output',
        'features': range(-1,512)
    },
    {
        'name': 'inception_4c/pool',
        'features': range(-1,512)
    },
    {
        'name': 'inception_4d/3x3',
        'features': range(-1,288)
    },
    {
        'name': 'inception_4d/5x5',
        'features': range(-1,64)
    },
    {
        'name': 'inception_4d/5x5_reduce',
        'features': range(-1,32)
    },
    {
        'name': 'inception_4d/output',
        'features': range(-1,528)
    },
    {
        'name': 'inception_4d/pool',
        'features': range(-1,512)
    },
    {
        'name': 'inception_4e/1x1',
        'features': range(-1,256)
    },
    {
        'name': 'inception_4e/3x3',
        'features': range(-1,320)
    },
    {
        'name': 'inception_4c/5x5_reduce',
        'features': range(-1,24)
    },
    {
        'name': 'inception_4c/output',
        'features': range(-1,512)
    },
    {
        'name': 'inception_4c/pool',
        'features': range(-1,512)
    },
    {
        'name': 'inception_4d/3x3',
        'features': range(-1,288)
    },
    {
        'name': 'inception_4d/5x5',
        'features': range(-1,64)
    },
    {
        'name': 'inception_4d/output',
        'features': range(-1,528)
    },
    {
        'name': 'inception_4d/pool',
        'features': range(-1,512)
    },
    {
        'name': 'inception_4e/1x1',
        'features': range(-1,256)
    },
    {
        'name': 'inception_4e/3x3',
        'features': range(-1,320)
    },
    {
        'name': 'inception_4e/3x3_reduce',
        'features': range(-1,160)
    },
    {
        'name': 'inception_4e/5x5',
        'features': range(-1,128)
    },
    {
        'name': 'inception_4e/5x5_reduce',
        'features': range(-1,32)
    },
    {
        'name': 'inception_4e/output',
        'features': range(-1,832)
    },
    {
        'name': 'inception_4e/pool',
        'features': range(-1,528)
    },
    {
        'name': 'inception_4e/pool_proj',
        'features': range(-1,128)
    },
    {
        'name': 'inception_5a/1x1',
        'features': range(-1,256)
    },
    {
        'name': 'inception_5a/3x3',
        'features': range(-1,320)
    },
    {
        'name': 'inception_5a/3x3_reduce',
        'features': range(-1,160)
    },
    {
        'name': 'inception_5a/5x5',
        'features': range(-1,128)
    },
    {
        'name': 'inception_5a/5x5_reduce',
        'features': range(-1,32)
    },
    {
        'name': 'inception_5a/output',
        'features': range(-1,832)
    },
    {
        'name': 'inception_5a/pool',
        'features': range(-1,832)
    },
    {
        'name': 'inception_5b/1x1',
        'features': range(-1,384)
    },
    {
        'name': 'inception_5b/3x3',
        'features': range(-1,384)
    },
    {
        'name': 'inception_5b/3x3_reduce',
        'features': range(-1,192)
    },
    {
        'name': 'inception_5b/5x5',
        'features': range(-1,128)
    },
    {
        'name': 'inception_5b/5x5_reduce',
        'features': range(-1,48)
    },
    {
        'name': 'inception_5b/output',
        'features': range(-1,1024)
    },
    {
        'name': 'inception_5b/pool',
        'features': range(-1,832)
    },
    {
        'name': 'inception_5b/pool_proj',
        'features': range(-1,128)
    },
]

layers_vgg19 = [
    {
        'name': 'conv1_1',
        'features': range(-1,64)
    },
    {
        'name': 'conv1_2',
        'features': range(-1,64)
    },
    {
        'name': 'pool1',
        'features': range(-1,64)
    },
    {
        'name': 'conv2_1',
        'features': range(-1,128)
    },
    {
        'name': 'conv2_2',
        'features': range(-1,128)
    },
    {
        'name': 'pool2',
        'features': range(-1,128)
    },
    {
        'name': 'conv3_1',
        'features': range(-1,256)
    },
    {
        'name': 'conv3_2',
        'features': range(-1,256)
    },
    {
        'name': 'conv3_3',
        'features': range(-1,256)
    },
    {
        'name': 'conv3_4',
        'features': range(-1,256)
    },
    {
        'name': 'pool3',
        'features': range(-1,256)
    },
    {
        'name': 'conv4_1',
        'features': range(-1,512)
    },
    {
        'name': 'conv4_2',
        'features': range(-1,512)
    },
    {
        'name': 'conv4_3',
        'features': range(-1,512)
    },
    {
        'name': 'conv4_4',
        'features': range(-1,512)
    },
    {
        'name': 'pool4',
        'features': range(-1,512)
    },
    {
        'name': 'conv5_1',
        'features': range(-1,512)
    },
    {
        'name': 'conv5_2',
        'features': range(-1,512)
    },
    {
        'name': 'conv5_2',
        'features': range(-1,512)
    },
    {
        'name': 'conv5_3',
        'features': range(-1,512)
    },
    {
        'name': 'conv5_4',
        'features': range(-1,512)
    },
    {
        'name': 'pool5',
        'features': range(-1,512)
    },
]

