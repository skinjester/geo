import time, data, os, os.path, numpy as np
import hud.console as console

# suppress verbose caffe logging before caffe import
os.environ['GLOG_minloglevel'] = '2'
import caffe
from google.protobuf import text_format

class Model(object):
    def __init__(self, program_duration, current_program, Renderer):

        self.net = None
        self.net_fn = None
        self.param_fn = None
        self.end = None
        self.features = None
        self.current_feature = 0
        self.layers =None
        self.current_layer = 0
        self.current_program = current_program
        self.program_duration = program_duration
        self.program_running = True
        self.program_start_time = time.time()
        self.installation_startup = time.time()  # keep track of runtime
        self.iterations = None
        self.iteration_max = None
        self.stepsize = None
        self.stepsize_base = None
        self.octave_n = None
        self.octave_cutoff = None
        self.octave_scale = None
        self.iteration_mult = None
        self.step_mult = None
        self.jitter = 320
        self.clip = True
        self.Renderer = Renderer

        # # FX
        self.package_name = None
        self.cyclefx = None  # contains cyclefx list for current program
        self.stepfx = None  # contains stepfx list for current program
        caffe.set_device(0)
        caffe.set_mode_gpu()

        self.set_program(current_program)

    def set_program(self, current_program):
        program = data.program[current_program]
        self.current_program = current_program
        self.package_name = program['name']
        self.iterations = program['iterations']
        self.iteration_max = program['iterations']
        self.stepsize_base = program['step_size']
        self.octave_n = program['octaves']
        self.octave_cutoff = program['octave_cutoff']
        self.octave_scale = program['octave_scale']
        self.iteration_mult = program['iteration_mult']
        self.step_mult = program['step_mult']
        self.layers = program['layers']
        self.features = program['features']
        self.current_feature = 0;
        self.modelname = program['model']
        self.choose_model(self.modelname)
        self.set_endlayer(self.layers[0])
        self.cyclefx = program['cyclefx']
        self.stepfx = program['stepfx']
        self.program_start_time = time.time()
        log.warning('program:{} started:{}'.format(program['name'], self.program_start_time))
        self.Renderer.request_wakeup()

        console.console_log('program', self.package_name)

    def choose_model(self, modelname):
        self.net_fn = '{}/{}/{}'.format(models['path'], models[modelname][0], models[modelname][1])
        self.param_fn = '{}/{}/{}'.format(models['path'], models[modelname][0], models[modelname][2])

        model = caffe.io.caffe_pb2.NetParameter()
        text_format.Merge(open(self.net_fn).read(), model)
        model.force_backward = True
        open('tmp.prototxt', 'w').write(str(model))

        self.net = caffe.Classifier('tmp.prototxt',
            self.param_fn, mean=np.float32([104.0, 116.0, 122.0]),
            channel_swap=(2, 1, 0))

        console.log_value('model', models[modelname][2])

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
        self.Renderer.request_wakeup()
        log.warning('layer: {} ({})'.format(self.end, self.net.blobs[self.end].data.shape[1]))
        console.log_value('layer','{} ({})'.format(self.end, self.net.blobs[self.end].data.shape[1]))

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
        console.log_value('featuremap', self.features[self.current_feature])
        self.Renderer.request_wakeup()

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
        current_program = self.current_program - 1
        if current_program < 0:
            current_program = len(data.program) - 1
        self.set_program(current_program)

    def next_program(self):
        current_program = self.current_program + 1
        if current_program > len(data.program) - 1:
            current_program = 0
        self.set_program(current_program)

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

# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.CRITICAL)

