import time
from data import program

class Model(object):
    def __init__(self, current_layer=0, program_duration=30):
        self.net = None
        self.net_fn = None
        self.param_fn = None
        self.caffemodel = None
        self.end = None
        self.models = models
        self.guides = guides
        self.guide_features = self.guides[0]
        self.current_guide = 0
        self.features = None
        self.current_feature = 0
        self.layers = layers
        self.current_layer = current_layer
        self.first_time_through = True

        self.program = program
        self.current_program = 0
        self.program_duration = program_duration
        self.program_running = True
        self.program_start_time = time.time()
        self.installation_startup = time.time()  # keep track of runtime

        # amplification
        self.iterations = None
        self.stepsize = None
        self.stepsize_base = None
        self.octaves = None
        self.octave_cutoff = None
        self.octave_scale = None
        self.iteration_mult = None
        self.step_mult = None
        self.jitter = 320

        # FX
        self.package_name = None
        self.cyclefx = None  # contains cyclefx list for current program
        self.stepfx = None  # contains stepfx list for current program

    def set_program(self, index):
        Viewport.refresh()
        self.package_name = data.program[index]['name']
        self.iterations = data.program[index]['iterations']
        self.stepsize_base = data.program[index]['step_size']
        self.octaves = data.program[index]['octaves']
        self.octave_cutoff = data.program[index]['octave_cutoff']
        self.octave_scale = data.program[index]['octave_scale']
        self.iteration_mult = data.program[index]['iteration_mult']
        self.step_mult = data.program[index]['step_mult']
        self.layers = data.program[index]['layers']
        self.features = data.program[index]['features']
        self.current_feature = 0;
        self.model = data.program[index]['model']
        self.choose_model(self.model)
        self.set_endlayer(self.layers[0])
        self.cyclefx = data.program[index]['cyclefx']
        self.stepfx = data.program[index]['stepfx']
        self.program_start_time = time.time()
        log.warning('program:{} started:{}'.format(
            self.program[self.current_program]['name'],
            self.program_start_time))

    def choose_model(self, key):
        self.net_fn = '{}/{}/{}'.format(self.models['path'],
            self.models[key][0], self.models[key][1])
        self.param_fn = '{}/{}/{}'.format(self.models['path'],
            self.models[key][0], self.models[key][2])
        self.caffemodel = self.models[key][2]

        # Patch model to be able to compute gradients
        # load the empty protobuf model
        model = caffe.io.caffe_pb2.NetParameter()

        # load the prototxt and place it in the empty model
        text_format.Merge(open(self.net_fn).read(), model)

        # add the force backward: true value
        model.force_backward = True

        # save it to a new file called tmp.prototxt
        open('tmp.prototxt', 'w').write(str(model))

        # the neural network model
        self.net = caffe.Classifier('tmp.prototxt',
            self.param_fn, mean=np.float32([104.0, 116.0, 122.0]),
            channel_swap=(2, 1, 0))
        # self.param_fn, mean=np.float32([20.0, 10.0,190.0]), channel_swap=(2, 1, 0))

        console_log('model', self.caffemodel)

    def show_network_details(self):
        # outputs layer details to console
        print self.net.blobs.keys()
        print 'current layer:{} ({}) current feature:{}'.format(
            self.end,
            self.net.blobs[self.end].data.shape[1],
            self.features[self.current_feature]
        )

    def set_endlayer(self, end):
        self.end = end
        Viewport.refresh()
        log.warning('layer: {} ({})'.format(self.end, self.net.blobs[self.end].data.shape[1]))
        console_log('layer','{} ({})'.format(self.end, self.net.blobs[self.end].data.shape[1]))

    def prev_layer(self):
        self.current_layer -= 1
        if self.current_layer < 0:
            self.current_layer = len(self.layers) - 1
        self.set_endlayer(self.layers[self.current_layer])

    def next_layer(self):
        self.current_layer += 1
        if self.current_layer > len(self.layers) - 1:
            self.current_layer = 0
        self.set_endlayer(self.layers[self.current_layer])

    def set_featuremap(self):
        log.warning('featuremap:{}'.format(self.features[self.current_feature]))
        console_log('featuremap', self.features[self.current_feature])
        Viewport.refresh()

    def prev_feature(self):
        max_feature_index = self.net.blobs[self.end].data.shape[1]
        self.current_feature -= 1
        if self.current_feature < 0:
            self.current_feature = max_feature_index - 1
        self.set_featuremap()

    def next_feature(self):
        max_feature_index = self.net.blobs[self.end].data.shape[1]
        self.current_feature += 1
        if self.current_feature > max_feature_index - 1:
            self.current_feature = -1
        self.set_featuremap()

    def reset_feature(self):
        pass

    def prev_program(self):
        self.current_program -= 1
        if self.current_program < 0:
            self.current_program = len(self.program) - 1
        self.set_program(self.current_program)

    def next_program(self):
        self.current_program += 1
        if self.current_program > len(self.program) - 1:
            self.current_program = 0
        self.set_program(self.current_program)

    def toggle_program_cycle(self):
        self.program_running = not self.program_running
        if self.program_running:
            self.next_program()

models = {
    'path': '../models',
    'cars': [
        'cars',
        'deploy.prototxt',
        'googlenet_finetune_web_car_iter_10000.caffemodel'
    ],
    'googlenet': [
        'bvlc_googlenet',
        'deploy.prototxt',
        'bvlc_googlenet.caffemodel'
    ],
    'places': [
        'googlenet_places205',
        'deploy.prototxt',
        'places205_train_iter_2400000.caffemodel'
    ],
    'places365': [
        'googlenet_places365',
        'deploy.prototxt',
        'googlenet_places365.caffemodel'
    ],
    'vgg19': [
        'VGG_ILSVRC_19',
        'deploy.prototxt',
        'VGG_ILSVRC_19_layers.caffemodel'
    ]
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

guides = [
    'gaudi1.jpg',
    'gaudi2.jpg',
    'house1.jpg',
    'eagle1.jpg',
    'tiger.jpg',
    'cat.jpg',
    'sax2.jpg',
    'bono.jpg',
    'rabbit2.jpg',
    'eyeballs.jpg',
]
