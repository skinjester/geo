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
        'range_out':[1.1,1.3],
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

bilateral_filter_default = {
    'name': 'bilateral_filter',
    'radius': {
        'cycle_length': 10,
        'frequency': 1,
        'range_out':[3.0,7.0],
        'wavetype': 'square',
        'dutycycle': 0.5
    },
    'sigma-color': {
        'cycle_length': 100,
        'frequency': 1,
        'range_out':[10,10],
        'wavetype': 'saw',
        'dutycycle': 0.5
    },
    'sigma-xy': {
        'cycle_length': 1000,
        'frequency': 10,
        'range_out':[1,200],
        'wavetype': 'square',
        'dutycycle': 0.5
    },
}

slowshutter_default = {
    'name': 'slowshutter',
    'samplesize': {
        'cycle_length': 10000,
        'frequency': 2,
        'range_out':[10,10],
        'wavetype': 'sin',
        'dutycycle': 0.5
    },
    'interval': {
        'cycle_length': 10000,
        'frequency': 1,
        'range_out':[1,1],
        'wavetype': 'sin',
        'dutycycle': 0.5
    },
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



program = []

# program.append({
#     'name': 'peyoteworld-v6',
#     'iterations': 2,
#     'step_size': 1.1,
#     'octaves': 5,
#     'octave_cutoff': 5,
#     'octave_scale': 1.8,
#     'iteration_mult': 0.0,
#     'step_mult': 0.0,
#     'model': 'vgg19',
#     'layers': [
#         {
#             'name':'conv3_1',
#             'features':range(-1,255)
#         },
#     ],
#     'cyclefx': [
#         inception_xform_default
#     ],
#     'stepfx': [
#         slowshutter_default
#     ]
# })

program.append({
    'name': 'Rivendell-1',
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
            'features': [101]
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
        {
            'name': 'featuremap',
            'index': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[101,101],
                'wavetype': 'square',
                'dutycycle': 0.5
            }
        },
        slowshutter_default
    ]
})

program.append({
    'name': 'basic-1',
    'iterations': 20,
    'step_size': 1.0001,
    'octaves': 5,
    'octave_cutoff': 5,
    'octave_scale': 1.2,
    'iteration_mult': 0.5,
    'step_mult': 0.0,
    'model': 'googlenet',
    'layers': [
        {
            'name':'inception_4b/output',
            'features':range(-1,64),
        },
        {
            'name':'inception_5b/output',
            'features':range(-1,64),
        },
        {
            'name':'inception_5b/5x5_reduce',
            'features':range(-1,64),
        },
        {
            'name':'inception_5b/5x5',
            'features':range(-1,64),
        },
        {
            'name':'inception_5b/3x3',
            'features':range(-1,64),
        },
    ],
    'cyclefx': [
        octave_scaler_default,
        inception_xform_default
    ],
    'stepfx': [
        bilateral_filter_default,
        slowshutter_default
    ]
})

program.append({
    'name': 'cambrian-implosion-1',
    'iterations':10,
    'step_size': 1.1,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.0,
    'model': 'places365',
    'layers': [
        {
            'name': 'inception_4d/3x3_reduce',
            'features': range(-1,256),
        },
        {
            'name': 'inception_4d/3x3',
            'features': range(-1,256),
        },
        {
            'name': 'inception_4d/output',
            'features': range(-1,256),
        },
        {
            'name': 'inception_4a/3x3',
            'features': range(-1,256),
        },

    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.02}
        },
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 10,
                'frequency': 1,
                'range_out':[1.1,1.8],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ],
    'stepfx': [

        # {
        #     'name': 'gaussian',
        #     'sigma': {
        #         'cycle_length': 100,
        #         'frequency': 20,
        #         'range_out':[0.1,0.6],
        #         'wavetype': 'sin',
        #         'dutycycle': 0.5
        #     }
        # },

        # {
        #     'name': 'featuremap',
        #     'index': {
        #         'cycle_length': 1000,
        #         'frequency': 1,
        #         'range_out':[0,29],
        #         'wavetype': 'sin',
        #         'dutycycle': 0.5
        #     }
        # },
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10,
                'frequency': 1,
                'range_out':[10,10],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[1,1],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
        # {
        #     'name': 'bilateral_filter',
        #     'radius': {
        #         'cycle_length': 1000,
        #         'frequency': 100,
        #         'range_out':[5.0,5.0],
        #         'wavetype': 'square',
        #         'dutycycle': 0.5
        #     },
        #     'sigma-color': {
        #         'cycle_length': 100,
        #         'frequency': 1,
        #         'range_out':[10,10],
        #         'wavetype': 'saw',
        #         'dutycycle': 0.5
        #     },
        #     'sigma-xy': {
        #         'cycle_length': 1000,
        #         'frequency': 10,
        #         'range_out':[10,200],
        #         'wavetype': 'saw',
        #         'dutycycle': 0.5
        #     },
        # },
        {
            'name': 'step_mixer',
            'opacity': {
                'cycle_length': 10,
                'frequency': 1,
                'range_out':[0.0,1.0],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
    ]
})

program.append({
    'name': 'New Paris',
    'iterations': 10,
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
        # {
        #     'name': 'inception_xform',
        #     'params': {'scale': 0.2}
        # },
        # {
        #     'name': 'octave_scaler',
        #     'params': {
        #         'cycle_length': 10,
        #         'frequency': 1,
        #         'range_out':[1.6,2.2],
        #         'wavetype': 'saw',
        #         'dutycycle': 0.5
        #     }
        # },
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
                'cycle_length': 20000,
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
    'name': 'Paris-v5',
    'iterations': 10,
    'step_size': 2,
    'octaves': 5,
    'octave_cutoff': 3,
    'octave_scale': 1.5,
    'iteration_mult': 0.0,
    'step_mult': 0.01,
    'model': 'places365',
    'layers': [
        {
            'name':'inception_4a/3x3',
            'features':range(-1,200),
        },
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': -0.01}
        },
    ],
    'stepfx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[1.2,1.7],
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
                'frequency': 2,
                'range_out':[60,60],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
        # {
        #     'name': 'featuremap',
        #     'index': {
        #         'cycle_length': 1000,
        #         'frequency': 3,
        #         'range_out':[0,2,3,4,5,6,7],
        #         'wavetype': 'sin',
        #         'dutycycle': 0.5
        #     }
        # },
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 2,
                'range_out':[1,15],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[1,1],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
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
        {
            'name': 'inception_4c/1x1',
            'features': range(127, 256)
        }
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.2}
        },
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 100,
                'frequency': 10,
                'range_out':[1.5,2.0],
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
                'range_out':[10,10],
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
    'name': 'Lobe-v9',
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
    'name': 'Lobe-v6',
    'iterations': 20,
    'step_size': 0.23,
    'octaves': 6,
    'octave_cutoff': 6,
    'octave_scale': 1.7,
    'iteration_mult': 0.5,
    'step_mult': 0.04,
    'model': 'milesdeep',
    'layers': [
        {
            'name':'conv_stage3_block0_branch2b',
            'features': range(-1, 128)
        },
    ],
    'cyclefx': [
        # {
        #     'name': 'octave_scaler',
        #     'params': {
        #         'cycle_length': 100,
        #         'frequency': 10,
        #         'range_out':[1.5,2.0],
        #         'wavetype': 'sin',
        #         'dutycycle': 0.05
        #     }
        # },
        {
            'name': 'inception_xform',
            'params': {'scale': 0.2}
        },
    ],
    'stepfx': [
        {
            'name': 'gaussian',
            'sigma': {
                'cycle_length': 1000,
                'frequency': 100,
                'range_out':[0.0,0.4],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },

        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 299,
                'range_out':[15,15],
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
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[0,1],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ]
})




program.append({
    'name': 'metamachine',
    'iterations': 12,
    'step_size': 1.8,
    'octaves': 6,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.75,
    'step_mult': 0.0,
    'model': 'vgg19',
    'layers': [
        {
            'name': 'conv4_1',
            'features': range(-1, 512)
        }
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': -0.2}
        },
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[1.1,1.4],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ],
    'stepfx': [
        {
            'name': 'nd_gaussian',
            'params': {
                'cycle_length': 100,
                'frequency': 1,
                'range_out':[0.1,10.0],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ]
})


program.append({
    'name': 'neomorph-neo-v5',
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



program.append({
    'name': 'peyoteworld-v5',
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
    'name': 'Paris-v7',
    'iterations': 10,
    'step_size': 2,
    'octaves': 5,
    'octave_cutoff': 3,
    'octave_scale': 1.5,
    'iteration_mult': 0.0,
    'step_mult': 0.01,
    'model': 'places365',
    'layers': [
        {
            'name':'inception_4b/pool_proj',
            'features':range(64),
        },
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.1}
        },
    ],
    'stepfx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[1.2,1.7],
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
                'range_out':[1,16],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'sigma-xy': {
                'cycle_length': 1000,
                'frequency': 2,
                'range_out':[12,60],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
        {
            'name': 'featuremap',
            'index': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[0,20],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 2,
                'range_out':[1,60],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[1,1],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
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
        {
            'name': 'conv5_1',
            'features': range(90, 100)
        }
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': -0.05}
        },
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 10000,
                'frequency': 10,
                'range_out':[1.1,2.0],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ],
    'stepfx': [
        {
            'name': 'nd_gaussian',
            'params': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[0.1,3.0],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 10,
                'range_out':[10,10],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 10000,
                'frequency': 2,
                'range_out':[1,3],
                'wavetype': 'saw',
                'dutycycle': 0.5
            },
        },
        {
            'name': 'featuremap',
            'index': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[0,5],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ]
})

program.append({
    'name': 'Lobe-v7',
    'iterations': 20,
    'step_size': 2.0,
    'octaves': 6,
    'octave_cutoff': 6,
    'octave_scale': 1.5,
    'iteration_mult': 0.25,
    'step_mult': 0.04,
    'model': 'places365',
    'layers': [
        {
            'name':'inception_5a/5x5_reduce',
            'features': range(-1,30)
        },
    ],
    'cyclefx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 100,
                'frequency': 10,
                'range_out':[1.1,1.3],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'inception_xform',
            'params': {'scale': 0.2}
        },
    ],
    'stepfx': [
        {
            'name': 'gaussian',
            'sigma': {
                'cycle_length': 1000,
                'frequency': 100,
                'range_out':[0.0,1.4],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },

        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 299,
                'range_out':[15,15],
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
                'cycle_length': 1000,
                'frequency': 50,
                'range_out':[0,12],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ]
})

program.append({
    'name': 'peyoteworld-2',
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
            'name':'conv3_3',
            'features':range(-1, 255)
        }
    ],
    'cyclefx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 10000,
                'frequency': 10,
                'range_out':[1.1,1.3],
                'wavetype': 'square',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'inception_xform',
            'params': {'scale': 0.05}
        },
    ],
    'stepfx': [
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 3,
                'range_out':[10,30],
                'wavetype': 'sin',
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
                'cycle_length': 10000,
                'frequency': 4,
                'range_out':[0,20],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },

    ]
})

program.append({
    'name': 'Lobe-v5',
    'iterations': 10,
    'step_size': 4.0,
    'octaves': 6,
    'octave_cutoff': 5,
    'octave_scale': 1.5,
    'iteration_mult': 0.2,
    'step_mult': 0.01,
    'model': 'milesdeep',
    'layers': [
        {
            'name':'conv_stage2_block4_branch2b',
            'features': range(-1, 128)
        },
    ],
    'cyclefx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 10000,
                'frequency': 4,
                'range_out':[1.2,1.8],
                'wavetype': 'saw',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'inception_xform',
            'params': {'scale': -0.05}
        },
    ],
    'stepfx': [
        {
            'name': 'median_blur',
            'params': {
                'cycle_length': 1000,
                'frequency': 5,
                'range_out':[0.0,3],
                'wavetype': 'square',
                'dutycycle': 0.5
            }
        },
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
    'name': 'JOI-v5',
    'iterations': 10,
    'step_size': 1.2,
    'octaves': 6,
    'octave_cutoff': 4,
    'octave_scale': 1.3,
    'iteration_mult': 0.5,
    'step_mult': 0.1,
    'model': 'vgg19',
    'layers': [
        {
            'name':'conv5_2',
            'features':range(-1, 256)
        },
        {
            'name':'conv5_3',
            'features':range(-1, 256)
        }
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.05}
        },
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 50,
                'frequency': 10,
                'range_out':[1.2,1.5],
                'wavetype': 'square',
                'dutycycle': 0.5
            }
        },
    ],
    'stepfx': [
        {
            'name': 'median_blur',
            'params': {
                'cycle_length': 60,
                'frequency': 1,
                'range_out':[0.0, 3.0],
                'wavetype': 'square',
                'dutycycle': 0.7
            }
        },
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 100,
                'frequency': 3,
                'range_out':[10,10],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 100,
                'frequency': 1,
                'range_out':[2,2],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
        },
    ],
})

program.append({
    'name': 'Lobe-v8',
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
            'name':'inception_4e/3x3',
            'features': range(-1,300)
        },
    ],
    'cyclefx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 100,
                'frequency': 10,
                'range_out':[1.3,1.8],
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
                'frequency': 1,
                'range_out':[0,120],
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
                'range_out':[10,80],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'sigma-xy': {
                'cycle_length': 1000,
                'frequency': 10,
                'range_out':[90,90],
                'wavetype': 'square',
                'dutycycle': 0.5
            },
        },
    ]
})

program.append({
    'name': 'Windows 2049',
    'iterations': 30,
    'step_size': 2.,
    'octaves': 6,
    'octave_cutoff': 6,
    'octave_scale': 1.5,
    'iteration_mult': 0.25,
    'step_mult': 0.02,
    'model': 'places365',
    'layers': [
        {
            'name': 'inception_3b/output',
            'features': [-1,6,-1,-1]
        },
        {
            'name': 'inception_4b/output',
            'features': range(-1,256)
        }
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.03}
        },
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 10,
                'frequency': 2,
                'range_out':[1.1,1.4],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ],
    'stepfx': [
        # {
        #     'name': 'featuremap',
        #     'index': {
        #         'cycle_length': 10000,
        #         'frequency': 50,
        #         'range_out':[0,2],
        #         'wavetype': 'sin',
        #         'dutycycle': 0.5
        #     }
        # },
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 3,
                'range_out':[5,5],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[2,2],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
    ]
})

program.append({
    'name': 'Paris-v6',
    'iterations': 10,
    'step_size': 2,
    'octaves': 5,
    'octave_cutoff': 3,
    'octave_scale': 1.5,
    'iteration_mult': 0.0,
    'step_mult': 0.01,
    'model': 'places365',
    'layers': [
        {
            'name':'inception_4b/3x3_reduce',
            'features':range(64),
        },
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': -0.01}
        },
    ],
    'stepfx': [
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[1.2,1.7],
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
                'frequency': 2,
                'range_out':[60,60],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
        {
            'name': 'featuremap',
            'index': {
                'cycle_length': 1000,
                'frequency': 1,
                'range_out':[0,20],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 2,
                'range_out':[1,15],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
            'interval': {
                'cycle_length': 10000,
                'frequency': 1,
                'range_out':[1,1],
                'wavetype': 'sin',
                'dutycycle': 0.5
            },
        },
    ]
})

program.append({
    'name': 'Windows 2050',
    'iterations': 30,
    'step_size': 2.,
    'octaves': 6,
    'octave_cutoff': 6,
    'octave_scale': 1.5,
    'iteration_mult': 0.25,
    'step_mult': 0.02,
    'model': 'places365',
    'layers': [
        {
            'name': 'inception_3b/pool',
            'features': range(-1,256)
        },
        {
            'name': 'inception_4b/output',
            'features': range(-1,256)
        }
    ],
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.03}
        },
        {
            'name': 'octave_scaler',
            'params': {
                'cycle_length': 10,
                'frequency': 2,
                'range_out':[1.1,1.4],
                'wavetype': 'sin',
                'dutycycle': 0.5
            }
        },
    ],
    'stepfx': [
        # {
        #     'name': 'featuremap',
        #     'index': {
        #         'cycle_length': 10000,
        #         'frequency': 50,
        #         'range_out':[0,3],
        #         'wavetype': 'sin',
        #         'dutycycle': 0.5
        #     }
        # },
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 3,
                'range_out':[15,15],
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

















# program.append({
#     'name': 'cambrian-candidate-googlenet',
#     'iterations': 30,
#     'step_size': 2.2,
#     'octaves': 5,
#     'octave_cutoff': 5,
#     'octave_scale': 1.5,
#     'iteration_mult': 0.5,
#     'step_mult': 0.05,
#     'model': 'googlenet',
#     'layers': [
#         'inception_4b/output',
#         'inception_4b/pool',
#         'inception_4c/pool',
#         'inception_4b/3x3_reduce',
#         'inception_4b/5x5',
#         'inception_4b/5x5_reduce',
#         'inception_4b/pool_proj',
#         'inception_4c/1x1',
#         'inception_4c/3x3',
#         'inception_4c/3x3_reduce',
#         'inception_4c/5x5',
#         'inception_4c/5x5_reduce',
#         'inception_4c/output',
#         'inception_3a/1x1',
#         'inception_3a/3x3',
#         'inception_3b/5x5',
#         'inception_3b/output',
#         'inception_3b/pool',
#     ],
#     'features': range(-1, 256),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': 0.05}
#         },
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 0.1, 'min_scale': 1.4, 'max_scale': 2.0}
#         },

#     ],
#     'stepfx': [
#         # {
#         #   'name': 'bilateral_filter',
#         #   'params': {'radius': 3, 'sigma_color':10, 'sigma_xy': 23}
#         # },
#         {
#             'name': 'median_blur',
#             'params': {'kernel_shape': 3, 'interval': 3}
#         }

#     ]
# })

# program.append({
#     'name': 'Wintermute',
#     'iterations': 10,
#     'step_size': 3.,
#     'octaves': 6,
#     'octave_cutoff': 5,
#     'octave_scale': 1.5,
#     'iteration_mult': 0.0,
#     'step_mult': 0.03,
#     'model': 'places365',
#     'layers': [
#         'inception_4c/output',
#         'inception_4c/pool',
#         'inception_4b/3x3_reduce',
#         'inception_4b/5x5',
#         'inception_4b/5x5_reduce',
#         'inception_4b/output',
#         'inception_4b/pool',
#         'inception_4b/pool_proj',
#         'inception_4c/1x1',
#         'inception_4c/3x3',
#         'inception_4c/3x3_reduce',
#         'inception_4c/5x5',
#         'inception_4c/5x5_reduce',
#     ],
#     'features': range(-1, 256),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': -0.025}
#         },
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 0.33, 'min_scale': 1.24, 'max_scale': 2.1}
#         },
#     ],
#     'stepfx': [
#         {
#             'name': 'bilateral_filter',
#             'params': {'radius': -1, 'sigma_color': 24, 'sigma_xy': 3}
#         },
#     ]
# })

# program.append({
#     'name': 'Geologist',
#     'iterations': 30,
#     'step_size': 3.5,
#     'octaves': 4,
#     'octave_cutoff': 4,
#     'octave_scale': 1.8,
#     'iteration_mult': 0.25,
#     'step_mult': -0.01,
#     'model': 'places365',
#     'layers': [
#         'inception_4c/1x1',
#         'inception_4c/3x3',
#     ],
#     'features': range(93, 127),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': 0.25}
#         },
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 0.13, 'min_scale': 1.5, 'max_scale': 2.0}
#         },
#     ],
#     'stepfx': [
#         # {
#         #   'name': 'step_opacity',
#         #   'params': {'opacity':0.5}
#         # },
#         # {
#         #   'name': 'bilateral_filter',
#         #   'params': {'radius': 3, 'sigma_color':5, 'sigma_xy': 10}
#         # },
#     ]
# })



# program.append({
#     'name': 'GAIA',
#     'iterations': 10,
#     'step_size': 2.5,
#     'octaves': 4,
#     'octave_cutoff': 3,
#     'octave_scale': 1.8,
#     'iteration_mult': 0.25,
#     'step_mult': 0.01,
#     'model': 'places',
#     'layers': [
#         'inception_4c/1x1',
#         'inception_4c/3x3',
#     ],
#     'features': range(111, 256),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': 0.15}
#         },
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 0.2, 'min_scale': 1.4, 'max_scale': 2.0}
#         },
#     ],
#     'stepfx': [
#         {
#             'name': 'bilateral_filter',
#             'params': {'radius': 3, 'sigma_color': 20, 'sigma_xy': 50}
#         },

#     ]
# })

# program.append({
#     'name': 'JOI.00',
#     'iterations': 20,
#     'step_size': 2.2,
#     'octaves': 6,
#     'octave_cutoff': 5,
#     'octave_scale': 1.3,
#     'iteration_mult': 0.5,
#     'step_mult': 0.02,
#     'model': 'vgg19',
#     'layers': [
#         'conv5_2',
#         'conv5_3',
#     ],
#     'features': range(11, 256),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': 0.1}
#         },
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 0.05, 'min_scale': 1.2, 'max_scale': 1.5}
#         },
#     ],
#     'stepfx': [
#         {
#             'name': 'median_blur',
#             'params': {'kernel_shape': 3, 'interval': 3}
#         }
#     ]
# })

# program.append({
#     'name': 'peyoteworld',
#     'iterations': 5,
#     'step_size': 2,
#     'octaves': 5,
#     'octave_cutoff': 3,
#     'octave_scale': 1.2,
#     'iteration_mult': 0.0,
#     'step_mult': 0.1,
#     'model': 'vgg19',
#     'layers': [
#         'conv3_2',
#         'conv3_1',
#         'conv3_3',
#     ],
#     'features': range(-1, 255),
#     'cyclefx': [
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 0.1, 'min_scale': 1.1, 'max_scale': 1.6}
#         }
#     ],
#     'stepfx': []
# })

# program.append({
#     'name': 'ACCIO',
#     'iterations': 10,
#     'step_size': 2,
#     'octaves': 4,
#     'octave_cutoff': 4,
#     'octave_scale': 1.7,
#     'iteration_mult': 0.5,
#     'step_mult': 0.01,
#     'model': 'vgg19',
#     'layers': [
#         'conv4_3',
#         'conv3_3',
#         'conv4_2',
#         'conv3_1',
#         'conv3_2',
#         'conv3_4',
#         'conv4_1',
#         'conv4_4',
#         'conv5_1',
#         'conv5_2',
#         'conv5_3',
#         'conv5_4'
#     ],
#     'features': range(34, 255),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': 0.025}
#         },
#         # {
#         #   'name': 'octave_scaler',
#         #   'params': {'step':0.1, 'min_scale':1.3, 'max_scale':1.8}
#         # }
#     ],
#     'stepfx': [
#         {
#             'name': 'bilateral_filter',
#             'params': {'radius': 3, 'sigma_color': 20, 'sigma_xy': 100}
#         },
#     ]
# })



