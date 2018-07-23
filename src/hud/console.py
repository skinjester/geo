from data import viewsize, FONT, WHITE, GREEN
import numpy as np, cv2

def counter(func):
    def wrapper(*args, **kwargs):
        wrapper.counter +=1
        return func(*args, **kwargs)
    wrapper.counter=0
    return wrapper

def log_value(key, new_value):
    log[key][1] = log[key][0]
    log[key][0] = new_value

def log_render_values():
    pass

def console_log(key, new_value):
    log[key][1] = log[key][0]
    log[key][0] = new_value

def draw(image):
    clearscreen = cv2.rectangle(screen, (0, 0), (viewsize[0], viewsize[1]), (0, 0, 0), -1)
    cv2.putText(screen, log['detect'][0], (x[0], 40), FONT, 1.0, (0, 255, 0))
    cv2.putText(screen, 'DEEPDREAMVISIONQUEST', (x[0], 100), FONT, 1.0, WHITE)
    layout('program')
    layout('interval')
    layout('runtime')
    layout('floor')
    layout('threshold')
    layout('last')
    layout('now')
    layout('model')
    layout('layer')
    layout('featuremap')
    layout('width')
    layout('height')
    layout('scale')
    layout('octave')
    layout('iteration')
    layout('step_size')
    layout('cycle_time')
    layout('gamma')
    layout.counter=0
    return cv2.addWeighted(screen, opacity, image, 1 - opacity, 0, image)

@counter
def layout(key):
    color = WHITE
    row = y[0] + layout.counter * y[1]
    if log[key][0] != log[key][1]:
        color = GREEN
        log[key][1] = log[key][0]
    cv2.putText(screen, key, (x[0], row), FONT, opacity, color)
    cv2.putText(screen, '{}'.format(log[key][0]), (x[1], row), FONT, opacity, color)

# -------
# INITIALIZE
# -------
screen = np.zeros((viewsize[1], viewsize[0], 3), np.uint8)
opacity = 0.5
log = {
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
x = (40, 180) # col1, col2
y = (150, 20) # row, row height
row = None

'''
octave
i
iteration_max
Model.octave_n
Model.octave_cutoff
Model.current_guide
Model.guides
Model.program_start_time
Model.program_duration
Model.iteration_mult
Webcam.get().delta_trigger
Webcam.get().floor
Webcam.get().gamma
'''

# def post_render_HUD_wrapup(self, i, octave, iteration_max, Model, Webcam):
#     octavemsg = '{}/{}({})'.format(octave, octave_n,
#         Model.octave_cutoff)
#     guidemsg = '({}/{}) {}'.format(
#         Model.current_guide,
#         len(Model.guides),
#         Model.guides[Model.current_guide])
#     iterationmsg = '{:0>3}:{:0>3} x{}'.format(
#         i,
#         iteration_max,
#         Model.iteration_mult)
#     stepsizemsg = '{:02.3f} x{:02.3f}'.format(
#         step_params['step_size'],
#         Model.step_mult)
#     thresholdmsg = '{:0>6}'.format(
#         motion.delta_trigger)
#     floormsg = '{:0>6}'.format(
#         motion.floor)
#     gammamsg = '{}'.format(
#         Webcam.get().gamma)
#     intervalmsg = '{:01.2f}/{:01.2f}'.format(
#         round(time.time() - Model.program_start_time, 2),
#         Model.program_duration)
#     console_log('octave', octavemsg)
#     console_log('width', w)
#     console_log('height', h)
#     console_log('guide', guidemsg)
#     console_log('iteration', iterationmsg)
#     console_log('step_size', stepsizemsg)
#     console_log('scale', Model.octave_scale)
#     console_log('program', Model.package_name)
#     console_log('threshold', thresholdmsg)
#     console_log('floor', floormsg)
#     console_log('gamma', gammamsg)
#     console_log('interval', intervalmsg)
#     console_log('runtime', round(time.time() - Model.installation_startup, 2))

