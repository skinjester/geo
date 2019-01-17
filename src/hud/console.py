from data import viewsize, FONT, WHITE, GREEN
import data
import numpy as np, cv2

def counter(func):
    def wrapper(*args, **kwargs):
        wrapper.counter +=1
        return func(*args, **kwargs)
    wrapper.counter=0
    return wrapper

def log_value(key, new_value):
    hud_log[key][1] = hud_log[key][0]
    hud_log[key][0] = new_value

def draw(image):
    clearscreen = cv2.rectangle(screen, (0, 0), (viewsize[0], viewsize[1]), (0, 0, 0), -1)
    cv2.putText(screen, hud_log['detect'][0], (x[0], 40), FONT, 1.0, (0, 255, 0))
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
    layout('eq_clip')
    layout('eq_grid')
    layout('timeloop')
    layout('widetime')

    layout.counter=0
    return cv2.addWeighted(screen, opacity, image, 1 - opacity, 0, image)

@counter
def layout(key):
    color = WHITE
    row = y[0] + layout.counter * y[1]
    if hud_log[key][0] != hud_log[key][1]:
        color = GREEN
        hud_log[key][1] = hud_log[key][0]
    cv2.putText(screen, key, (x[0], row), FONT, opacity, color)
    cv2.putText(screen, '{}'.format(hud_log[key][0]), (x[1], row), FONT, opacity, color)

# -------
# INITIALIZE
# -------
screen = np.zeros((viewsize[1], viewsize[0], 3), np.uint8)
opacity = 0.5
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
    'gamma': [None, None],
    'eq_clip': [None, None],
    'eq_grid': [None, None],
    'timeloop': [None, None],
    'widetime': [None, None],
}
x = (40, 180) # col1, col2
y = (150, 20) # row, row height
row = None

# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.CRITICAL)
