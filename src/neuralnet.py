import time, data, os, os.path, numpy as np
from itertools import cycle
import hud.console as console
import photobooth720 as performer
import postprocess



# suppress verbose caffe logging before caffe import
os.environ['GLOG_minloglevel'] = '2'
import caffe
from google.protobuf import text_format

class Model(object):
    def __init__(self, program_duration, current_program, Renderer):
        self.program_duration = program_duration
        self.program_running = True
        self.installation_startup = time.time()
        self.Renderer = Renderer
        caffe.set_device(0)
        caffe.set_mode_gpu()
        self.set_program(current_program)

    def set_program(self, current_program):
        program = performer.program[current_program]
        self.package_name = program['name']
        self.program_start_time = time.time()
        self.current_program = current_program
        self.iterations = program['iterations']
        self.iteration_max = program['iterations']
        self.iteration_mult = program['iteration_mult']
        self.stepsize_base = program['step_size']
        self.step_mult = program['step_mult']
        self.octave_n = program['octaves']
        self.octave_cutoff = program['octave_cutoff']
        self.octave_scale = program['octave_scale']
        self.layers = program['layers']
        self.current_layer = 0
        self.features = None # this will be defined in set_end_layer()
        self.current_feature = 0
        self.jitter = 320
        self.clip = True
        self.modelname = program['model']
        self.choose_model(self.modelname)
        self.set_endlayer(self.current_layer)
        self.stepfx = program['stepfx']
        self.autofeature = program['autofeature']
        self.cyclefx = program['cyclefx']
        self.pool = None
        self.release = self.feature_release_counter()
        for fx in self.cyclefx:
            if fx['name'] == 'octave_scaler':
                # self.pool = self.setup_octave_scaler(**value['params'])
                params = fx['params']
                fx['osc'] = postprocess.oscillator(
                    cycle_length = params['cycle_length'],
                    frequency = params['frequency'],
                    range_out = params['range_out'],
                    wavetype = params['wavetype'],
                    dutycycle = params['dutycycle']
                )

        for fx in self.stepfx:
            if fx['name'] == 'median_blur':
                params = fx['params']
                fx['osc'] = postprocess.oscillator(
                    cycle_length = params['cycle_length'],
                    frequency = params['frequency'],
                    range_out = params['range_out'],
                    wavetype = params['wavetype'],
                    dutycycle = params['dutycycle']
                )
            if fx['name'] == 'bilateral_filter':
                params = fx['radius']
                fx['osc1'] = postprocess.oscillator(
                    cycle_length = params['cycle_length'],
                    frequency = params['frequency'],
                    range_out = params['range_out'],
                    wavetype = params['wavetype'],
                    dutycycle = params['dutycycle']
                )
                params = fx['sigma-color']
                fx['osc2'] = postprocess.oscillator(
                    cycle_length = params['cycle_length'],
                    frequency = params['frequency'],
                    range_out = params['range_out'],
                    wavetype = params['wavetype'],
                    dutycycle = params['dutycycle']
                )
                params = fx['sigma-xy']
                fx['osc3'] = postprocess.oscillator(
                    cycle_length = params['cycle_length'],
                    frequency = params['frequency'],
                    range_out = params['range_out'],
                    wavetype = params['wavetype'],
                    dutycycle = params['dutycycle']
                )
            if fx['name'] == 'gaussian':
                params = fx['sigma']
                fx['osc'] = postprocess.oscillator(
                    cycle_length = params['cycle_length'],
                    frequency = params['frequency'],
                    range_out = params['range_out'],
                    wavetype = params['wavetype'],
                    dutycycle = params['dutycycle']
                )
            if fx['name'] == 'step_mixer':
                params = fx['opacity']
                fx['osc'] = postprocess.oscillator(
                    cycle_length = params['cycle_length'],
                    frequency = params['frequency'],
                    range_out = params['range_out'],
                    wavetype = params['wavetype'],
                    dutycycle = params['dutycycle']
                )
            if fx['name'] == 'slowshutter':
                params = fx['samplesize']
                fx['osc1'] = postprocess.oscillator(
                    cycle_length = params['cycle_length'],
                    frequency = params['frequency'],
                    range_out = params['range_out'],
                    wavetype = params['wavetype'],
                    dutycycle = params['dutycycle']
                )
                params = fx['interval']
                fx['osc2'] = postprocess.oscillator(
                    cycle_length = params['cycle_length'],
                    frequency = params['frequency'],
                    range_out = params['range_out'],
                    wavetype = params['wavetype'],
                    dutycycle = params['dutycycle']
                )
            if fx['name'] == 'featuremap':
                params = fx['index']
                fx['osc1'] = postprocess.oscillator(
                    cycle_length = params['cycle_length'],
                    frequency = params['frequency'],
                    range_out = params['range_out'],
                    wavetype = params['wavetype'],
                    dutycycle = params['dutycycle']
                )

        log.warning('program:{} started:{}'.format(program['name'], self.program_start_time))
        console.log_value('program', self.package_name)
        self.Renderer.request_wakeup()

    def setup_octave_scaler(self, step, min_scale, max_scale):
        interval = (max_scale-min_scale)/step
        return cycle(np.arange(min_scale, max_scale, interval).tolist())

    def choose_model(self, modelname):
        self.net_fn = '{}/{}/{}'.format(models['path'], models[modelname][0], models[modelname][1])
        self.param_fn = '{}/{}/{}'.format(models['path'], models[modelname][0], models[modelname][2])

        model = caffe.io.caffe_pb2.NetParameter()
        text_format.Merge(open(self.net_fn).read(), model)
        model.force_backward = True
        open('tmp.prototxt', 'w').write(str(model))

        magic_numbers = [104.0, 116.0, 122.0]

        self.net = caffe.Classifier('tmp.prototxt',
            self.param_fn, mean=np.float32(magic_numbers),
            # self.param_fn, mean=np.float32([64.0, 480.0, -120.0]),
            # self.param_fn, mean=np.float32([364.0, 20.0, -20.0]),
            # self.param_fn, mean=np.float32([128.0, 168.0, 96.0]),
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

    def set_endlayer(self, layer_index):
        self.end = self.layers[layer_index]['name']
        self.features = self.layers[layer_index]['features']
        self.current_feature = self.features[0]
        self.log_featuremap()
        self.Renderer.request_wakeup()
        log.warning('layer: {} ({})'.format(self.end, self.net.blobs[self.end].data.shape[1]))
        console.log_value('layer','{} ({})'.format(self.end, self.net.blobs[self.end].data.shape[1]))

    def prev_layer(self):
        self.current_layer -= 1
        if self.current_layer < 0:
            self.current_layer = len(self.layers) - 1
        self.set_endlayer(self.current_layer)

    def next_layer(self):
        self.current_layer += 1
        if self.current_layer > len(self.layers) - 1:
            self.current_layer = 0
        self.set_endlayer(self.current_layer)

    def log_featuremap(self):
        max_feature_index = self.net.blobs[self.end].data.shape[1]
        log.warning('feature:{}/{}'.format(self.current_feature,max_feature_index))
        console.log_value('featuremap', self.current_feature)
        # self.Renderer.request_wakeup()

    def prev_feature(self):
        max_feature_index = self.net.blobs[self.end].data.shape[1]
        self.current_feature -= 1
        if self.current_feature < -1:
            self.current_feature = max_feature_index - 1
        self.log_featuremap()

    def next_feature(self):
        max_feature_index = self.net.blobs[self.end].data.shape[1]
        self.current_feature += 1
        if self.current_feature > max_feature_index - 1:
            self.current_feature = -1
        self.log_featuremap()

    def reset_feature(self):
        pass

    def update_feature(self, release):
        counter = self.release.next()
        throttle = counter % release
        if throttle == 0:
            self.next_feature()

    def prev_program(self):
        current_program = self.current_program - 1
        if current_program < 0:
            current_program = len(performer.program) - 1
        self.set_program(current_program)

    def next_program(self):
        current_program = self.current_program + 1
        if current_program > len(performer.program) - 1:
            current_program = 0
        self.set_program(current_program)

    def toggle_program_cycle(self):
        self.program_running = not self.program_running
        if self.program_running:
            self.next_program()

    def set_featuremap(self, index):
        index = int(round(index))
        max_feature_index = self.net.blobs[self.end].data.shape[1]
        self.current_feature = index
        if self.current_feature > max_feature_index - 1:
            self.current_feature = -1
        log.debug('index:{}'.format(self.current_feature))
        self.log_featuremap()

    def feature_release_counter(maxvalue=9999999):
        value = 0
        yield value
        while True:
            value += 1
            if value > maxvalue:
                value = 0
            yield value

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
    'vgg16': [
        'VGG_ILSVRC_16',
        'deploy.prototxt',
        'VGG_ILSVRC_16_layers.caffemodel'
    ],
    'vgg19': [
        'VGG_ILSVRC_19',
        'deploy.prototxt',
        'VGG_ILSVRC_19_layers.caffemodel'
    ],

    'milesdeep': [
        'Miles_Deep',
        'deploy.prototxt',
        'Miles_Deep.caffemodel'
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



