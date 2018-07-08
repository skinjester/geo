import numpy as np
import cv2

# processing resolution
capture_w = 1280
capture_h = 720

# crashy
# capture_w = 1920
# capture_h = 1080

# capture_w = 960
# capture_h = 720

# 4K camera doesn't support this display size
# capture_w = 864
# capture_h = 480

# capture_w = 640
# capture_h = 360

# capture_w = 1280
# capture_h = 800


now = 0  # timing reference updated each rem cycle
counter = 0  # has to do with the hud laout. sort of a hack

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

models = {
    'path': '../models',
    'cars': ('cars', 'deploy.prototxt', 'googlenet_finetune_web_car_iter_10000.caffemodel'),
    'googlenet': ('bvlc_googlenet', 'deploy.prototxt', 'bvlc_googlenet.caffemodel'),
    'places': ('googlenet_places205', 'deploy.prototxt', 'places205_train_iter_2400000.caffemodel'),
    'places365': ('googlenet_places365', 'deploy.prototxt', 'googlenet_places365.caffemodel'),
    'vgg19': ('VGG_ILSVRC_19', 'deploy.prototxt', 'VGG_ILSVRC_19_layers.caffemodel')
}

layers = [
    'inception_4d/5x5_reduce',
    'conv2/3x3',
    'conv2/3x3_reduce',
    'conv2/norm2',
    'inception_3a/1x1',
    'inception_3a/3x3',
    'inception_3b/5x5',
    'inception_3b/output',
    'inception_3b/pool',
    'inception_4a/1x1',
    'inception_4a/3x3',
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
    'inception_5a/1x1',
    'inception_5a/3x3',
    'inception_5a/3x3_reduce',
    'inception_5a/5x5',
    'inception_5a/5x5_reduce',
    'inception_5a/output',
    'inception_5a/pool',
    'inception_5b/1x1',
    'inception_5b/3x3',
    'inception_5b/3x3_reduce',
    'inception_5b/5x5',
    'inception_5b/5x5_reduce',
    'inception_5b/output',
    'inception_5b/pool',
    'inception_5b/pool_proj'
]

vgg19_layers = [
    'conv3_1',
    'conv3_2',
    'conv3_3',
    'conv3_4',
    'conv4_1',
    'conv4_2',
    'conv4_3',
    'conv4_4',
    'conv5_1',
    'conv5_2',
    'conv5_3',
    'conv5_4'
]

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
    'name': 'kwisatzhaderach',
    'iterations': 30,
    'step_size': 3,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.5,
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
    'iterations': 5,
    'step_size': 1.2,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.8,
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
    'features': range(87, 512),
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': -0.2}
        },
        {
            'name': 'octave_scaler',
            'params': {'step': 0.1, 'min_scale': 1.5, 'max_scale': 2.0}
        },
    ],
    'stepfx': []
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
        'inception_4c/pool',
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
        # 	'name': 'bilateral_filter',
        # 	'params': {'radius': 3, 'sigma_color':10, 'sigma_xy': 23}
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
        # 	'name': 'step_opacity',
        # 	'params': {'opacity':0.5}
        # },
        # {
        # 	'name': 'bilateral_filter',
        # 	'params': {'radius': 3, 'sigma_color':5, 'sigma_xy': 10}
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
        # 	'name': 'step_opacity',
        # 	'params': {'opacity':0.5}
        # },
        # {
        # 	'name': 'bilateral_filter',
        # 	'params': {'radius': 3, 'sigma_color':5, 'sigma_xy': 10}
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
        # 	'name': 'octave_scaler',
        # 	'params': {'step':0.1, 'min_scale':1.3, 'max_scale':1.8}
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
        # {
        # 	'name': 'nd_gaussian',
        # 	'params': {'sigma': 0.4, 'order':0}
        # },
        {
            'name': 'bilateral_filter',
            'params': {'radius': 7, 'sigma_color': 16, 'sigma_xy': 60}
        }
    ]
})


# --------
#
# --------

hud_log = {
    'octave': [None, None],
    'width': [None, None],
    'height': [None, None],
    'guide': [None, None],
    'layer': [None, None],
    'last': [None, None],
    'now': [None, None],
    'iteration': [None, None],
    'step_size': [None, None],
    'settings': [None, None],
    'threshold': [None, None],
    'detect': [None, None],
    'cycle_time': [None, None],
    'featuremap': [None, None],
    'model': [None, None],
    'username': [None, None],
    'scale': [None, None],
    'program': [None, None],
    'interval': [None, None],
    'runtime': [None, None],
    'floor': [None, None],
    'gamma': [None, None]
}

# opencv font and color
FONT = cv2.FONT_HERSHEY_SIMPLEX
WHITE = (255, 255, 255)
GREEN = (0,255,0)
RED = (255,0,0)