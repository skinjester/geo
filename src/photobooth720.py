import data, postprocess

# defaults provided as a convenience
xform_array_default = {
    'name': 'xform_array',
    'params': {'amplitude': 20, 'wavelength': 50}
}


octave_scaler_default = {
    'name': 'octave_scaler',
    'params': {
        'cycle_length': 10,
        'frequency': 1,
        'range_out':[1.2,1.9],
        'wavetype': 'sin',
        'dutycycle': 0.5
    }
}
inception_xform_default = {
    'name': 'inception_xform',
    'params': {'scale': 0.1}
}

inception_xform_small = {
    'name': 'inception_xform',
    'params': {'scale': 0.01}
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

median_filter_default = {
    'name': 'median_blur',
    'params': {
        'cycle_length': 100,
        'frequency': 2,
        'range_out':[3.0,3.0],
        'wavetype': 'square',
        'dutycycle': 0.5
    }
},

bilateral_filter_default = {
    'name': 'bilateral_filter',
    'radius': {
        'cycle_length': 100,
        'frequency': 1,
        'range_out':[3.0,3.0],
        'wavetype': 'square',
        'dutycycle': 0.5
    },
    'sigma-color': {
        'cycle_length': 100,
        'frequency': 1,
        'range_out':[10,10],
        'wavetype': 'square',
        'dutycycle': 0.5
    },
    'sigma-xy': {
        'cycle_length': 250,
        'frequency': 1,
        'range_out':[50,50],
        'wavetype': 'square',
        'dutycycle': 0.5
    },
}

slowshutter_default = {
    'name': 'slowshutter',
    'samplesize': {
        'cycle_length': 1000,
        'frequency': 2,
        'range_out':[1,30],
        'wavetype': 'sin',
        'dutycycle': 0.5
    },
    'interval': {
        'cycle_length': 1000,
        'frequency': 1,
        'range_out':[1,1],
        'wavetype': 'sin',
        'dutycycle': 0.5
    },
}

nd_gaussian_filter_default = {
    'name': 'gaussian',
    'sigma': {
        'cycle_length': 100,
        'frequency': 5,
        'range_out':[0.1,0.5],
        'wavetype': 'sin',
        'dutycycle': 0.5
    }
}


step_opacity_default = {
    'name': 'step_opacity',
    'params': {'opacity': 0.1}
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



program = []

program.append({
    'name': 'Places',
    'autofeature': True,
    'iterations': 5,
    'step_size': 2,
    'octaves': 5,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.1,
    'model': 'places365',
    'layers': [
        {
            'name': 'inception_4a/5x5_reduce',
            'features': range(-1,15)
        },
        {
            'name': 'inception_4a/5x5',
            'features': range(-1,47)
        },
        {
            'name': 'inception_4a/pool',
            'features': range(-1,479)
        },
        {
            'name': 'inception_4a/pool_proj',
            'features': range(-1,63)
        },
        {
            'name': 'inception_4a/output',
            'features': range(-1,511)
        },

        {
            'name': 'inception_4b/1x1',
            'features': range(-1,159)
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
            'features': range(-1,23)
        },
        {
            'name': 'inception_4b/output',
            'features': range(-1,511)
        },
        {
            'name': 'inception_4b/pool',
            'features': range(-1,511)
        },
        {
            'name': 'inception_4b/pool_proj',
            'features': range(-1,63)
        },
        {
            'name': 'inception_4c/1x1',
            'features': range(-1,127)
        },
        {
            'name': 'inception_4c/3x3',
            'features': range(-1,255)
        },
        {
            'name': 'inception_4c/3x3_reduce',
            'features': range(-1,127)
        },
        {
            'name': 'inception_4c/5x5',
            'features': range(-1,63)
        },
        {
            'name': 'inception_4c/5x5_reduce',
            'features': range(-1,23)
        },
        {
            'name': 'inception_4c/output',
            'features': range(-1,511)
        },
        {
            'name': 'inception_4c/pool',
            'features': range(-1,511)
        },
        {
            'name': 'inception_4d/3x3',
            'features': range(-1,288)
        },
        {
            'name': 'inception_4d/5x5',
            'features': range(-1,63)
        },
        {
            'name': 'inception_4d/5x5_reduce',
            'features': range(-1,31)
        },
        {
            'name': 'inception_4d/output',
            'features': range(-1,527)
        },
        {
            'name': 'inception_4d/pool',
            'features': range(-1,511)
        },
        {
            'name': 'inception_4e/1x1',
            'features': range(-1,255)
        },
        {
            'name': 'inception_4e/3x3',
            'features': range(-1,319)
        },
        {
            'name': 'inception_4c/5x5_reduce',
            'features': range(-1,23)
        },
        {
            'name': 'inception_4c/output',
            'features': range(-1,511)
        },
        {
            'name': 'inception_4c/pool',
            'features': range(-1,511)
        },
        {
            'name': 'inception_4d/3x3',
            'features': range(-1,288)
        },
        {
            'name': 'inception_4d/5x5',
            'features': range(-1,63)
        },
        {
            'name': 'inception_4d/output',
            'features': range(-1,528)
        },
        {
            'name': 'inception_4d/pool',
            'features': range(-1,511)
        },
        {
            'name': 'inception_4e/1x1',
            'features': range(-1,255)
        },
        {
            'name': 'inception_4e/3x3',
            'features': range(-1,319)
        },
        {
            'name': 'inception_4e/3x3_reduce',
            'features': range(-1,159)
        },
        {
            'name': 'inception_4e/5x5',
            'features': range(-1,127)
        },
        {
            'name': 'inception_4e/5x5_reduce',
            'features': range(-1,32)
        },
        {
            'name': 'inception_4e/output',
            'features': range(-1,831)
        },
        {
            'name': 'inception_4e/pool',
            'features': range(-1,527)
        },
        {
            'name': 'inception_4e/pool_proj',
            'features': range(-1,127)
        },
        {
            'name': 'inception_5a/1x1',
            'features': range(-1,255)
        },
        {
            'name': 'inception_5a/3x3',
            'features': range(-1,319)
        },
        {
            'name': 'inception_5a/3x3_reduce',
            'features': range(-1,159)
        },
        {
            'name': 'inception_5a/5x5',
            'features': range(-1,127)
        },
        {
            'name': 'inception_5a/5x5_reduce',
            'features': range(-1,31)
        },
        {
            'name': 'inception_5a/output',
            'features': range(-1,831)
        },
        {
            'name': 'inception_5a/pool',
            'features': range(-1,831)
        },
        {
            'name': 'inception_5b/1x1',
            'features': range(-1,383)
        },
        {
            'name': 'inception_5b/3x3',
            'features': range(-1,383)
        },
        {
            'name': 'inception_5b/3x3_reduce',
            'features': range(-1,191)
        },
        {
            'name': 'inception_5b/5x5',
            'features': range(-1,127)
        },
        {
            'name': 'inception_5b/5x5_reduce',
            'features': range(-1,47)
        },
        {
            'name': 'inception_5b/output',
            'features': range(-1,1023)
        },
        {
            'name': 'inception_5b/pool',
            'features': range(-1,831)
        },
        {
            'name': 'inception_5b/pool_proj',
            'features': range(-1,127)
        },
    ],
    'cyclefx': [
        octave_scaler_default,
        inception_xform_default
    ],
    'stepfx': [
        # bilateral_filter_default,
        # slowshutter_default,
    ]
})

program.append({
    'name': 'GoogLeNet w Stylized Motion',
    'autofeature': False,
    'iterations': 20,
    'step_size': 1,
    'octaves': 5,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.1,
    'model': 'googlenet',
    'layers': data.layers_googlenet,
    'cyclefx': [
        octave_scaler_default,
        inception_xform_default
    ],
    'stepfx': [
        bilateral_filter_default,
        slowshutter_default,
    ]
})

program.append({
    'name': 'magicmirror-1',
    'autofeature': True,
    'iterations': 20,
    'step_size': 2,
    'octaves': 5,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.1,
    'step_mult': 0.0,
    'model': 'googlenet',
    'layers': [
        {
            'name': 'inception_4c/pool',
            'features': range(-1,511)
        },
    ],
    'cyclefx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 10,
                'frequency': 1,
                'range_out':[1.6,1.9],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        }
    ],
    'stepfx': [
        {
            'name': 'median_blur',
            'params': {
                'cycle_length': 1000,
                'frequency': 250,
                'range_out':[0.0,3],
                'wavetype': 'square',
                'dutycycle': 0.5
            }
        },
        slowshutter_default,
    ]
})

program.append({
    'name': 'peyoteworld-v5',
    'autofeature': False,
    'iterations': 5,
    'step_size': 2,
    'octaves': 5,
    'octave_cutoff': 3,
    'octave_scale': 1.2,
    'iteration_mult': 0.0,
    'step_mult': 0.1,
    'model': 'vgg19',
    'layers': [
        {
            'name':'conv3_2',
            'features':range(-1, 255)
        },
    ],
    'cyclefx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 10000,
                'frequency': 10,
                'range_out':[1.1,1.5],
                'wavetype': 'square',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'inception_xform',
            'params': {'scale': 0.15}
        },
    ],
    'stepfx': [
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 3,
                'range_out':[10,10],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[3,3],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
        },

    ]
})


program.append({
    'name': 'Rivendell-1',
    'autofeature': False,
    'iterations': 10,
    'step_size': 1.5,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.05,
    'model': 'places365',
    'layers': [
        {
            'name': 'inception_4d/3x3',
            'features': range(-1,101)
        }
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.1}
        },
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 100,
                'frequency': 10,
                'range_out':[1.8,2.2],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ],
    'stepfx': [
        {
            'name': 'bilateral_filter',
            'radius': {
                'cycle_length': 1000,
                'frequency': 100,
                'range_out':[3.0,3.0],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
            'sigma-color': {
                'cycle_length': 1000,
                'frequency': 20,
                'range_out':[50,50],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'sigma-xy': {
                'cycle_length': 1000,
                'frequency': 10,
                'range_out':[30,30],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
        },
        {
            'name': 'step_mixer',
            'opacity': {
                'cycle_length': 1000,
                'frequency': 100,
                'range_out':[0.0,1.0],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
        slowshutter_default
    ]
})

program.append({
    'name': 'New Paris',
    'autofeature': False,
    'iterations': 20,
    'step_size': 1.4,
    'octaves': 5,
    'octave_cutoff': 5,
    'octave_scale': 1.5,
    'iteration_mult': 0.0,
    'step_mult': 0.0,
    'model': 'places365',
    'layers': [
        {
            'name':'inception_4b/pool_proj',
            'features':range(-1,64),
        },
        {
            'name':'inception_4b/pool_proj',
            'features':range(64),
        },
        {
            'name':'inception_4b/pool_proj',
            'features':range(64),
        },
        {
            'name':'inception_4b/pool_proj',
            'features':range(64),
        },
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.2}
        },
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 10,
                'frequency': 1,
                'range_out':[1.6,2.2],
                'wavetype': 'saw',
                'dutycycle': 0.5
            }
        },
    ],
    'stepfx': [
        {
            'name': 'bilateral_filter',
            'radius': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[3.0,3.0],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
            'sigma-color': {
                'cycle_length': 1000,
                'frequency': 100,
                'range_out':[0,0],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
            'sigma-xy': {
                'cycle_length': 1000,
                'frequency': 100,
                'range_out':[5,5],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
        },
        {
            'name': 'featuremap',
            'index': {
                'cycle_length': 100,
                'frequency': 1,
                'range_out':[0,64],
                'wavetype': 'saw',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[10,30],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[3,3],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
    ]
})

program.append({
    'name': 'Lobe-v9',
    'autofeature': False,
    'iterations': 10,
    'step_size': 2.0,
    'octaves': 6,
    'octave_cutoff': 6,
    'octave_scale': 1.5,
    'iteration_mult': 0.0,
    'step_mult': 0.0,
    'model': 'googlenet',
    'layers': [
        {
            'name':'inception_4b/5x5',
            'features': [7,12,7,12,14]
        },
    ],
    'cyclefx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 100,
                'frequency': 10,
                'range_out':[1.3,1.5],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'inception_xform',
            'params': {'scale': 0.1}
        },
    ],
    'stepfx': [
        # {
        #     'name': 'median_blur',
        #     'params': {
        #         'cycle_length': 1000,
        #         'frequency': 250,
        #         'range_out':[0.0,3],
        #         'wavetype': 'square',
        #         'dutycycle': 0.5
        #     }
        # },

        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 299,
                'range_out':[1,5],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[1,1],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
        },
        {
            'name': 'featuremap',
            'index': {
                'cycle_length': 2000,
                'frequency': 2,
                'range_out':[0,4],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'bilateral_filter',
            'radius': {
                'cycle_length': 1000,
                'frequency': 100,
                'range_out':[3.0,3.0],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
            'sigma-color': {
                'cycle_length': 1000,
                'frequency': 20,
                'range_out':[50,50],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'sigma-xy': {
                'cycle_length': 1000,
                'frequency': 10,
                'range_out':[50,50],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
        },
    ]
})

program.append({
    'name': 'neomorph-neo-v5',
    'autofeature': False,
    'iterations': 10,
    'step_size': 2,
    'octaves': 5,
    'octave_cutoff': 3,
    'octave_scale': 1.5,
    'iteration_mult': 0.0,
    'step_mult': 0.01,
    'model': 'googlenet',
    'layers': [
        {
            'name':'inception_4d/5x5',
            'features':range(64),
        },
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.05}
        },
    ],
    'stepfx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[1.4,1.7],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'bilateral_filter',
            'radius': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[7.0,7.0],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
            'sigma-color': {
                'cycle_length': 1000,
                'frequency': 2,
                'range_out':[16,16],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'sigma-xy': {
                'cycle_length': 1000,
                'frequency': 10,
                'range_out':[20,60],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
        },
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 1000,
                'frequency': 3,
                'range_out':[10,10],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[1,3],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
        {
            'name': 'featuremap',
            'index': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[0,10],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ]
})

