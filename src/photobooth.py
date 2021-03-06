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
        'range_out':[1.4,1.9],
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
        'range_out':[5.0,5.0],
        'wavetype': 'square',
        'dutycycle': 0.5
    },
    'sigma-color': {
        'cycle_length': 100,
        'frequency': 1,
        'range_out':[20,20],
        'wavetype': 'saw',
        'dutycycle': 0.5
    },
    'sigma-xy': {
        'cycle_length': 100,
        'frequency': 1,
        'range_out':[5,5],
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

program.append({
    'name': 'demo-1',
    'autofeature': True,
    'iterations': 10,
    'step_size': 0.5,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.1,
    'model': 'places365',
    'layers': data.layers_googlenet[18:19],
    'cyclefx': [
        octave_scaler_default
    ],
    'stepfx': [
        bilateral_filter_default,
        slowshutter_default,
    ]
})

program.append({
    'name': 'demo',
    'autofeature': True,
    'iterations': 2,
    'step_size': 2.4,
    'octaves': 4,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.0,
    'model': 'vgg19',
    'layers': data.layers_vgg19,
    'cyclefx': [
        {
            'name': 'inception_xform',
            'params': {'scale': 0.01}
        },
    ],
    'stepfx': [],
})



program.append({
    'name': 'demo-2',
    'autofeature': True,
    'iterations': 40,
    'step_size': 0.1,
    'octaves': 5,
    'octave_cutoff': 5,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.2,
    'model': 'googlenet',
    'layers': [
        {
            'name': 'inception_4d/5x5',
            'features': range(-1,64)
        }
    ],
    'cyclefx': [
        octave_scaler_default
    ],
    'stepfx': [
        bilateral_filter_default,
        {
            'name': 'slowshutter',
            'samplesize': {
                'cycle_length': 10000,
                'frequency': 2,
                'range_out':[15,15],
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
    ]
})

program.append({
    'name': 'Pixels to Semantics',
    'autofeature': True,
    'iterations': 10,
    'step_size': 0.5,
    'octaves': 5,
    'octave_cutoff': 4,
    'octave_scale': 1.8,
    'iteration_mult': 0.0,
    'step_mult': 0.1,
    'model': 'places365',
    'layers': [
        {
            'name': 'inception_4d/3x3',
            'features': range(-1,280)
        },

    ],
    'cyclefx': [
        octave_scaler_default
    ],
    'stepfx': [
        # bilateral_filter_default,
        slowshutter_default,
    ]
})

googlenet_layers = [
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


]
