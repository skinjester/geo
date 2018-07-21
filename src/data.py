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

# a list of programs
program = []

# defaults provided as a convenience
xform_array_default = {
    'name': 'xform_array',
    'params': {'amplitude': 20, 'wavelength': 50}
}

octave_scaler_default = {
    'name': 'octave_scaler',
    'params': {'step': 0.01, 'min_scale': 1.6, 'max_scale': 1.7}
}

inception_xform_default = {
    'name': 'inception_xform',
    'params': {'scale': 0.075}
}

cyclefx_default = [
    xform_array_default,
    octave_scaler_default,
    inception_xform_default,
]

median_blur_default = {
    'name': 'median_blur',
    'params': {'kernel_shape': 3}
}

bilateral_filter_default = {
    'name': 'bilateral_filter',
    'params': {'radius': 5, 'sigma_color': 30, 'sigma_xy': 30}
}

nd_gaussian_filter_default = {
    'name': 'nd_gaussian',
    'params': {'sigma': 0.6, 'order': 0}
}

step_opacity_default = {
    'name': 'step_opacity',
    'params': {'opacity': 1.0}
}

duration_cutoff_default = {
    'name': 'duration_cutoff',
    'params': {'duration': 2.0}
}

stepfx_default = [
    # median_blur_default,
    bilateral_filter_default,
    # nd_gaussian_filter_default,
    # step_opacity_default,
    # duration_cutoff_default
]

program.append({
    'name': 'basic',
    'iterations': 20,
    'step_size': 1.4,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.6,
    'iteration_mult': 0.0,
    'step_mult': 0.0,
    'model': 'places365',
    'layers': [
        'inception_4c/output',
        'inception_4c/pool',
        'inception_4d/3x3',
        'inception_4d/5x5',
        'inception_4d/5x5_reduce',
        'inception_4d/output',
        'inception_4d/pool',
        'inception_4e/1x1',
        'inception_4e/3x3',
        'inception_4e/3x3_reduce',
        'inception_4e/5x5',
        'inception_4e/5x5_reduce',
        'inception_4e/output',
        'inception_4e/pool',
        'inception_4e/pool_proj',
    ],
    'features': range(-1, 128),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.2}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.1, 'min_scale': 1.5, 'max_scale': 2.0}
        },
    ],
    'stepfx': [
        {
            'name': 'nd_gaussian',
            'params': {'sigma': 0.7, 'order': 0}
        },
    ]
})

program.append({
    'name': 'kwisatzhaderach',
    'iterations': 5,
    'step_size': 3,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.002,
    'model': 'vgg19',
    'layers': [
        'conv5_1',
        'conv3_1',
        'conv3_2',
        'conv3_3',
        'conv3_4',
        'conv4_1',
        'conv4_2',
        'conv4_3',
        'conv4_4',
        'conv5_3',
    ],
    'features': range(90, 512),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.2}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.1, 'min_scale': 1.5, 'max_scale': 2.0}
        },
    ],
    'stepfx': [
        {
            'name': 'nd_gaussian',
            'params': {'sigma': 0.7, 'order': 0}
        },
    ]
})

program.append({
    'name': 'PIKHAL',
    'iterations': 5,
    'step_size': 3,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.0,
    'model': 'vgg19',
    'layers': [
        'conv5_1',
        'conv3_1',
        'conv3_2',
        'conv3_3',
        'conv3_4',
        'conv4_1',
        'conv4_2',
        'conv4_3',
        'conv4_4',
        'conv5_3',
    ],
    'features': range(-1, 512),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.2}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.1, 'min_scale': 1.5, 'max_scale': 2.0}
        },
    ],
    'stepfx': []
})

program.append({
    'name': 'metamachine',
    'iterations': 10,
    'step_size': 1.8,
    'octaves': 6,
    'octave_cutoff': 6,
    'octave_scale': 1.8,
    'iteration_mult': 0.2,
    'step_mult': 0.0,
    'model': 'vgg19',
    'layers': [
        'conv5_1',
        'conv3_1',
        'conv3_2',
        'conv3_3',
        'conv3_4',
        'conv4_1',
        'conv4_2',
        'conv4_3',
        'conv4_4',
        'conv5_3',
    ],
    'features': range(-1, 512),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': -0.5}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.1, 'min_scale': 1.5, 'max_scale': 2.0}
        },
    ],
    'stepfx': [

        {
            'name': 'nd_gaussian',
            'params': {'sigma': 0.3, 'order': 0}
        },
        # {
        #     'name': 'octave_scaler',
        #     'params': {'step': 0.001, 'min_scale': 1.2, 'max_scale': 1.8}
        # },
    ]
})

program.append({
    'name': 'cambrian-implosion',
    'iterations': 10,
    'step_size': 10.,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.25,
    'step_mult': -0.01,
    'model': 'googlenet',
    'layers': [
        'inception_4b/5x5',
        'inception_4b/pool',
        'inception_4c/pool',
        'inception_4b/3x3_reduce',
        'inception_4b/5x5',
        'inception_4b/5x5_reduce',
        'inception_4b/output',
        'inception_4b/pool_proj',
        'inception_4c/1x1',
        'inception_4c/3x3',
        'inception_4c/3x3_reduce',
        'inception_5a/output',
        'inception_5a/pool',
        'inception_5b/1x1',
        'inception_5b/3x3',
        'inception_5b/3x3_reduce',
    ],
    'features': range(-1, 256),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.02}
        },
    ],
    'stepfx': [

        {
            'name': 'nd_gaussian',
            'params': {'sigma': 0.7, 'order': 0}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.001, 'min_scale': 1.2, 'max_scale': 1.8}
        },
    ]
})

program.append({
    'name': 'cambrian-candidate-googlenet',
    'iterations': 30,
    'step_size': 2.2,
    'octaves': 5,
    'octave_cutoff': 5,
    'octave_scale': 1.5,
    'iteration_mult': 0.5,
    'step_mult': 0.05,
    'model': 'googlenet',
    'layers': [
        'inception_4b/output',
        'inception_4b/pool',
        'inception_4c/pool',
        'inception_4b/3x3_reduce',
        'inception_4b/5x5',
        'inception_4b/5x5_reduce',
        'inception_4b/pool_proj',
        'inception_4c/1x1',
        'inception_4c/3x3',
        'inception_4c/3x3_reduce',
        'inception_4c/5x5',
        'inception_4c/5x5_reduce',
        'inception_4c/output',
        'inception_3a/1x1',
        'inception_3a/3x3',
        'inception_3b/5x5',
        'inception_3b/output',
        'inception_3b/pool',
    ],
    'features': range(-1, 256),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.05}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.1, 'min_scale': 1.4, 'max_scale': 2.0}
        },

    ],
    'stepfx': [
        # {
        #   'name': 'bilateral_filter',
        #   'params': {'radius': 3, 'sigma_color':10, 'sigma_xy': 23}
        # },
        {
            'name': 'median_blur',
            'params': {'kernel_shape': 3, 'interval': 3}
        }

    ]
})

program.append({
    'name': 'Wintermute',
    'iterations': 10,
    'step_size': 3.,
    'octaves': 6,
    'octave_cutoff': 5,
    'octave_scale': 1.5,
    'iteration_mult': 0.0,
    'step_mult': 0.03,
    'model': 'places365',
    'layers': [
        'inception_4c/output',
        'inception_4c/pool',
        'inception_4b/3x3_reduce',
        'inception_4b/5x5',
        'inception_4b/5x5_reduce',
        'inception_4b/output',
        'inception_4b/pool',
        'inception_4b/pool_proj',
        'inception_4c/1x1',
        'inception_4c/3x3',
        'inception_4c/3x3_reduce',
        'inception_4c/5x5',
        'inception_4c/5x5_reduce',
    ],
    'features': range(-1, 256),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': -0.025}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.33, 'min_scale': 1.24, 'max_scale': 2.1}
        },
    ],
    'stepfx': [
        {
            'name': 'bilateral_filter',
            'params': {'radius': -1, 'sigma_color': 24, 'sigma_xy': 3}
        },
    ]
})

program.append({
    'name': 'Geologist',
    'iterations': 30,
    'step_size': 3.5,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.25,
    'step_mult': -0.01,
    'model': 'places365',
    'layers': [
        'inception_4c/1x1',
        'inception_4c/3x3',
    ],
    'features': range(93, 127),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.25}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.13, 'min_scale': 1.5, 'max_scale': 2.0}
        },
    ],
    'stepfx': [
        # {
        #   'name': 'step_opacity',
        #   'params': {'opacity':0.5}
        # },
        # {
        #   'name': 'bilateral_filter',
        #   'params': {'radius': 3, 'sigma_color':5, 'sigma_xy': 10}
        # },
    ]
})

program.append({
    'name': 'Rivendell',
    'iterations': 30,
    'step_size': 3.5,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.25,
    'step_mult': -0.01,
    'model': 'places365',
    'layers': [
        'inception_4c/1x1',
        'inception_4c/3x3',
    ],
    'features': range(127, 256),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.2}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.13, 'min_scale': 1.5, 'max_scale': 2.0}
        },
    ],
    'stepfx': [
        # {
        #   'name': 'step_opacity',
        #   'params': {'opacity':0.5}
        # },
        # {
        #   'name': 'bilateral_filter',
        #   'params': {'radius': 3, 'sigma_color':5, 'sigma_xy': 10}
        # },
    ]
})

program.append({
    'name': 'GAIA',
    'iterations': 10,
    'step_size': 2.5,
    'octaves': 4,
    'octave_cutoff': 3,
    'octave_scale': 1.8,
    'iteration_mult': 0.25,
    'step_mult': 0.01,
    'model': 'places',
    'layers': [
        'inception_4c/1x1',
        'inception_4c/3x3',
    ],
    'features': range(111, 256),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.15}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.2, 'min_scale': 1.4, 'max_scale': 2.0}
        },
    ],
    'stepfx': [
        {
            'name': 'bilateral_filter',
            'params': {'radius': 3, 'sigma_color': 20, 'sigma_xy': 50}
        },

    ]
})

program.append({
    'name': 'JOI.00',
    'iterations': 20,
    'step_size': 2.2,
    'octaves': 6,
    'octave_cutoff': 5,
    'octave_scale': 1.3,
    'iteration_mult': 0.5,
    'step_mult': 0.02,
    'model': 'vgg19',
    'layers': [
        'conv5_2',
        'conv5_3',
    ],
    'features': range(11, 256),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.1}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.05, 'min_scale': 1.2, 'max_scale': 1.5}
        },
    ],
    'stepfx': [
        {
            'name': 'median_blur',
            'params': {'kernel_shape': 3, 'interval': 3}
        }
    ]
})

program.append({
    'name': 'peyoteworld',
    'iterations': 5,
    'step_size': 2,
    'octaves': 5,
    'octave_cutoff': 3,
    'octave_scale': 1.2,
    'iteration_mult': 0.0,
    'step_mult': 0.1,
    'model': 'vgg19',
    'layers': [
        'conv3_2',
        'conv3_1',
        'conv3_3',
    ],
    'features': range(-1, 255),
    'cyclefx': [
        {
            'name': 'octave_scaler',
            'params': {'step': 0.1, 'min_scale': 1.1, 'max_scale': 1.6}
        }
    ],
    'stepfx': []
})

program.append({
    'name': 'ACCIO',
    'iterations': 10,
    'step_size': 2,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.7,
    'iteration_mult': 0.5,
    'step_mult': 0.01,
    'model': 'vgg19',
    'layers': [
        'conv4_3',
        'conv3_3',
        'conv4_2',
        'conv3_1',
        'conv3_2',
        'conv3_4',
        'conv4_1',
        'conv4_4',
        'conv5_1',
        'conv5_2',
        'conv5_3',
        'conv5_4'
    ],
    'features': range(34, 255),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.025}
        },
        # {
        #   'name': 'octave_scaler',
        #   'params': {'step':0.1, 'min_scale':1.3, 'max_scale':1.8}
        # }
    ],
    'stepfx': [
        {
            'name': 'bilateral_filter',
            'params': {'radius': 3, 'sigma_color': 20, 'sigma_xy': 100}
        },
    ]
})

program.append({
    'name': 'JOI.02',
    'iterations': 20,
    'step_size': 1.2,
    'octaves': 6,
    'octave_cutoff': 5,
    'octave_scale': 1.3,
    'iteration_mult': 0.5,
    'step_mult': 0.02,
    'model': 'vgg19',
    'layers': [
        'conv5_2',
        'conv5_3',
    ],
    'features': range(15, 256),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.1}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.05, 'min_scale': 1.2, 'max_scale': 1.5}
        },
    ],
    'stepfx': [
        {
            'name': 'median_blur',
            'params': {'kernel_shape': 3, 'interval': 3}
        }
    ]
})

program.append({
    'name': 'neomorph-neo',
    'iterations': 10,
    'step_size': 2,
    'octaves': 5,
    'octave_cutoff': 3,
    'octave_scale': 1.5,
    'iteration_mult': 0.0,
    'step_mult': 0.01,
    'model': 'googlenet',
    'layers': [
        'inception_4c/5x5',
        'inception_4c/5x5_reduce',
        'inception_4c/output',
        'inception_4c/pool',
        'inception_4d/3x3',
        'inception_4d/5x5'
    ],
    'features': range(64),
    'cyclefx': [
        inception_xform_default
    ],
    'stepfx': [
        {
            'name': 'octave_scaler',
            'params': {'step': 0.01, 'min_scale': 1.4, 'max_scale': 1.7}
        },
        {
            'name': 'bilateral_filter',
            'params': {'radius': 7, 'sigma_color': 16, 'sigma_xy': 60}
        }
    ]
})

# --------
#
# --------


# opencv font and color
FONT = cv2.FONT_HERSHEY_SIMPLEX
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# image I/O
capturesize = (1280, 720)
viewsize = (1280, 720)

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

def remapValuetoRange(val, src, dst):
    # src [min,max] old range
    # dst [min,max] new range
    remapped_Value = ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + \
                     dst[0]
    return clamp(remapped_Value, [0.0, 1.0])

# clamps provided value between provided range
def clamp(value, range):
    return max(range[0], min(value, range[1]))
