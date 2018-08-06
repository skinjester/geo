import data, postprocess

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


program = []


program.append({
    'name': 'basic',
    'iterations': 10,
    'step_size': 2.0,
    'octaves': 5,
    'octave_cutoff': 5,
    'octave_scale': 1.5,
    'iteration_mult': 0.0,
    'step_mult': 0.0,
    'model': 'milesdeep',
    'layers': [
        'eltwise_stage2_block2',
        'conv_stage2_block3_branch2a',
        'conv_stage2_block3_branch2b',
        'conv_stage2_block3_branch2c',
        'eltwise_stage2_block3',
    ],
    'features': range(-1, 128),
    'cyclefx': [
        {
            'name': 'octave_scaler',
            'params': {'step': 5, 'min_scale': 1.6, 'max_scale': 2.0}
        },
        {
            'name': 'inception_xform',
            'params': {'scale': 0.2}
        },
    ],
    'stepfx': [
        {
            'name': 'median_blur',
            'params': {
                'cycle_length': 50,
                'frequency': 1,
                'out_minmax':[-1,1],
                'wavetype': 'sin'
            }
        }
    ]
})

'''
program.append({
    'name': 'basic',
    'step_size': 2.0,

    'octaves': (10,10,10,10),   # 4 octaves, 10 iterations each octave
    'octaves': (10,10,5,2),     # 4 octaves, variable iterations per octave
    'octaves': (10,10,5,5,0),   # 5 octaves, cutoff after octave 4
    'octaves': (10,-1,5,5]      # 5 octaves, skip octave 2

    'octave_scale': 1.5,
    'step_mult': -0.1,
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
            'params': {'scale': 0.05}
        },
    ],
    'stepfx': []
})
'''

# program.append({
#     'name': 'kwisatzhaderach',
#     'iterations': 5,
#     'step_size': 3,
#     'octaves': 4,
#     'octave_cutoff': 4,
#     'octave_scale': 1.8,
#     'iteration_mult': 0.0,
#     'step_mult': 0.002,
#     'model': 'vgg19',
#     'layers': [
#         'conv5_1',
#         'conv3_1',
#         'conv3_2',
#         'conv3_3',
#         'conv3_4',
#         'conv4_1',
#         'conv4_2',
#         'conv4_3',
#         'conv4_4',
#         'conv5_3',
#     ],
#     'features': range(90, 100),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': 0.2}
#         },
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 5, 'min_scale': 1.1, 'max_scale': 2.0}
#         },
#     ],
#     'stepfx': [
#         {
#             'name': 'nd_gaussian',
#             'params': {'sigma': 0.7, 'order': 0}
#         },
#     ]
# })

# program.append({
#     'name': 'PIKHAL',
#     'iterations': 5,
#     'step_size': 3,
#     'octaves': 4,
#     'octave_cutoff': 4,
#     'octave_scale': 1.8,
#     'iteration_mult': 0.0,
#     'step_mult': 0.0,
#     'model': 'vgg19',
#     'layers': [
#         'conv5_1',
#         'conv3_1',
#         'conv3_2',
#         'conv3_3',
#         'conv3_4',
#         'conv4_1',
#         'conv4_2',
#         'conv4_3',
#         'conv4_4',
#         'conv5_3',
#     ],
#     'features': range(-1,10),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': 0.2}
#         },
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 0.1, 'min_scale': 1.5, 'max_scale': 2.0}
#         },
#     ],
#     'stepfx': []
# })

# program.append({
#     'name': 'metamachine',
#     'iterations': 10,
#     'step_size': 1.8,
#     'octaves': 6,
#     'octave_cutoff': 6,
#     'octave_scale': 1.8,
#     'iteration_mult': 0.2,
#     'step_mult': 0.0,
#     'model': 'vgg19',
#     'layers': [
#         'conv5_1',
#         'conv3_1',
#         'conv3_2',
#         'conv3_3',
#         'conv3_4',
#         'conv4_1',
#         'conv4_2',
#         'conv4_3',
#         'conv4_4',
#         'conv5_3',
#     ],
#     'features': range(-1, 512),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': -0.5}
#         },
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 0.1, 'min_scale': 1.5, 'max_scale': 2.0}
#         },
#     ],
#     'stepfx': [

#         {
#             'name': 'nd_gaussian',
#             'params': {'sigma': 0.3, 'order': 0}
#         },
#         # {
#         #     'name': 'octave_scaler',
#         #     'params': {'step': 0.001, 'min_scale': 1.2, 'max_scale': 1.8}
#         # },
#     ]
# })

# program.append({
#     'name': 'cambrian-implosion',
#     'iterations': 10,
#     'step_size': 10.,
#     'octaves': 4,
#     'octave_cutoff': 4,
#     'octave_scale': 1.8,
#     'iteration_mult': 0.25,
#     'step_mult': -0.01,
#     'model': 'googlenet',
#     'layers': [
#         'inception_4b/5x5',
#         'inception_4b/pool',
#         'inception_4c/pool',
#         'inception_4b/3x3_reduce',
#         'inception_4b/5x5',
#         'inception_4b/5x5_reduce',
#         'inception_4b/output',
#         'inception_4b/pool_proj',
#         'inception_4c/1x1',
#         'inception_4c/3x3',
#         'inception_4c/3x3_reduce',
#         'inception_5a/output',
#         'inception_5a/pool',
#         'inception_5b/1x1',
#         'inception_5b/3x3',
#         'inception_5b/3x3_reduce',
#     ],
#     'features': range(-1, 256),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': 0.02}
#         },
#     ],
#     'stepfx': [

#         {
#             'name': 'nd_gaussian',
#             'params': {'sigma': 0.7, 'order': 0}
#         },
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 0.001, 'min_scale': 1.2, 'max_scale': 1.8}
#         },
#     ]
# })

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
#     'name': 'Rivendell',
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
#     'features': range(127, 256),
#     'cyclefx': [
#         {
#             'name': 'inception_xform',
#             'params': {'scale': 0.2}
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

# program.append({
#     'name': 'JOI.02',
#     'iterations': 20,
#     'step_size': 1.2,
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
#     'features': range(15, 256),
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
#     'name': 'neomorph-neo',
#     'iterations': 10,
#     'step_size': 2,
#     'octaves': 5,
#     'octave_cutoff': 3,
#     'octave_scale': 1.5,
#     'iteration_mult': 0.0,
#     'step_mult': 0.01,
#     'model': 'googlenet',
#     'layers': [
#         'inception_4c/5x5',
#         'inception_4c/5x5_reduce',
#         'inception_4c/output',
#         'inception_4c/pool',
#         'inception_4d/3x3',
#         'inception_4d/5x5'
#     ],
#     'features': range(64),
#     'cyclefx': [
#         inception_xform_default
#     ],
#     'stepfx': [
#         {
#             'name': 'octave_scaler',
#             'params': {'step': 0.01, 'min_scale': 1.4, 'max_scale': 1.7}
#         },
#         {
#             'name': 'bilateral_filter',
#             'params': {'radius': 7, 'sigma_color': 16, 'sigma_xy': 60}
#         }
#     ]
# })
