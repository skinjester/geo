from __future__ import division  # so division works like you expect it to
import numpy as np
import cv2
import time
import datetime
from threading import Thread
import sys
sys.path.append('../bin')  # point to directory containing LogSettings
import logging
import logging.config
import LogSettings  # global log settings template


# Camera collection
class Cameras(object):
    def __init__(self, source=[], current_camera=0):
        self.source = source
        self.current_camera = current_camera

    def next(self):
        # returns a pointer to the next available camera object
        if (self.current + 1 >= len(self.source)):
            self.current = 0
        return self.source[self.current]

    def previous(self):
        # returns a pointer to the previous available camera object
        if (self.current - 1 < 0):
            self.current = len(self.source) - 1
        return self.source[self.current]

    def set(self, camera_index):
        # returns a pointer to the specified camera object
        self.current = camera_index
        log.debug('cameraID: {}'.format(self.current))
        return self.source[self.current]

    def get(self):
        # returns a pointer to the current camera object
        log.debug('cameraID: {}'.format(self.current_camera))
        return self.source[self.current_camera]


# camera object
class WebcamVideoStream(object):

    # the camera has to be provided with a basic landscape width, height
    # because the hardware doesn't capture arbitrary window sizes
    def __init__(self,
                 src,
                 capture_width,
                 capture_height,
                 portrait_alignment,
                 log,
                 flip_h=False,
                 flip_v=False,
                 gamma=1.0,
                 floor=1000,
                 threshold_filter=32):

        # set camera dimensions before reading frames
        # requested size is rounded to nearest camera size if non-matching
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3, capture_width)
        self.stream.set(4, capture_height)
        self.width = int(self.stream.get(3))
        self.height = int(self.stream.get(4))
        self.capture_size = [self.width, self.height]

        # image transform and gamma
        self.portrait_alignment = portrait_alignment
        self.flip_h = flip_h
        self.flip_v = flip_v

        #
        self.gamma = gamma
        self.stopped = False

        # generates internal table for gamma correction
        self.table = np.array([((i / 255.0)**(1.0 / self.gamma)) * 255
                               for i in np.arange(0, 256)]).astype("uint8")

        # motion detection
        self.motiondetector = MotionDetector(floor, log)
        self.delta_count = 0  # difference between current frame and previous
        # framebuffer for image differencing operations
        self.t_delta_framebuffer = np.zeros((self.height, self.width, 3),
                                            np.uint8)
        self.threshold_filter = threshold_filter

        # frame buffer housekeeping
        # empty img for initial diff
        self.rawframe = np.zeros((self.height, self.width, 3), np.uint8)
        # initial frame to prime the queue
        (self.grabbed, self.frame) = self.stream.read()
        self.frame = self.transpose(self.frame)  # alignment correction
        ###
        self.t_minus = self.transpose(
            cv2.cvtColor(self.stream.read()[1], cv2.COLOR_RGB2GRAY))
        self.t_now = self.transpose(
            cv2.cvtColor(self.stream.read()[1], cv2.COLOR_RGB2GRAY))
        self.t_plus = self.transpose(
            cv2.cvtColor(self.stream.read()[1], cv2.COLOR_RGB2GRAY))

        # logging
        self.log = log  # this contains reference to hud logging function in rem.py

    def start(self):
        Thread(target=self.update, args=()).start()
        threadlog.critical('started camera thread')
        return self

    def update_gamma(self, gamma):
        # generates internal table for gamma correction
        self.table = np.array([((i / 255.0)**(1.0 / gamma)) * 255
                               for i in np.arange(0, 256)]).astype("uint8")
        threadlog.critical('gamma: {}'.format(gamma))

    def update(self):
        # loop until the thread is stopped
        while True:
            if self.stopped:
                return

            _, img = self.stream.read()

            ###
            # update detection buffer queue
            self.t_minus = self.t_now
            self.t_now = self.t_plus
            self.t_plus = self.transpose(
                cv2.blur(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), (9, 9)))

            self.t_delta_framebuffer = self.diffImg(self.t_minus, self.t_now,
                                                    self.t_plus)
            self.t_delta_framebuffer = cv2.dilate(
                self.t_delta_framebuffer, None, iterations=2)
            _, self.t_delta_framebuffer = cv2.threshold(
                self.t_delta_framebuffer, self.threshold_filter, 255,
                cv2.THRESH_BINARY)
            log.debug('t_delta_framebuffer shape: {}'.format(
                self.t_delta_framebuffer.shape))

            self.delta_count = cv2.countNonZero(self.t_delta_framebuffer)

            # dont process motion detection if paused
            if self.motiondetector.is_paused == False:
                self.motiondetector.process(self.delta_count)

            # update internal buffers w camera frame
            self.rawframe = img  # unprocessed camera img
            self.frame = self.gamma_correct(
                self.transpose(img))  # processed camera img

    def read(self):
        log.debug('camera buffer RGB:{}'.format(self.frame.shape))
        return self.frame

    def transpose(self, img):
        if self.portrait_alignment:
            img = cv2.transpose(img)
        if self.flip_v:
            img = cv2.flip(img, 0)
        if self.flip_h:
            img = cv2.flip(img, 1)
        return img

    def gamma_correct(self, img):
        # # apply gamma correction using the lookup table defined on init
        if self.gamma == 1.0:
            return img
        return cv2.LUT(img, self.table)

    def stop(self):
        self.stopped = True

    def diffImg(self, t0, t1, t2):
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        return cv2.bitwise_and(d1, d2)


class MotionDetector(object):

    def __init__(self, floor, log):

        self.wasMotionDetected = False
        self.wasMotionDetected = False
        self.delta_count_history = 0
        self.delta_count_history_peak = 0
        self.delta_trigger = 0
        self.delta_count = 0
        self.is_paused = False
        self.floor = floor
        self.update_hud_log = log
        self.history = []
        self.history_queue_length = 50
        self.monitor_msg = '****'
        self.peak = 0
        self.peak_last = 0
        self.peak_avg = 0
        self.peak_statusmsg = 'Peak is static'

        # dataexport
        # self.export = open("motiondata/motiondata-test-11.txt","w+")

        # temp (?)
        self._counter_ = 0
        self.elapsed = 0
        self.now = time.time()
        self.counted = 0

    def process(self, delta_count):
        # history
        self.delta_count = delta_count

        # scale delta trigger to rides peak values & prevent sensitive trigger
        self.delta_trigger = self.add_to_history(self.delta_count) + self.floor

        # for detection monitor window overlay
        self.monitor_msg = 'count:{} trigger:{} peak:{} ___:{}'.format(
            self.delta_count, self.delta_trigger, self.delta_count_history, self.delta_count_history_peak)

        self.elapsed = time.time() - self.now  # elapsed time for logging function
        if self.elapsed > 5 and self.elapsed < 6:
            self.counted += 1

        lastmsg = '{:0>6}'.format(self.delta_count_history)
        nowmsg = '{:0>6}'.format(self.delta_count)
        self.update_hud_log('last', lastmsg)
        self.update_hud_log('now', nowmsg)

        #  keep track of current/prev values
        self.delta_count_history = self.delta_count

        # keep track of peak value
        # if self.delta_count_history > self.delta_count_history_peak:
        #     self.delta_count_history_peak = self.delta_count_history
        self.delta_count_history_peak = max(self.history)

        if self.delta_count < self.floor:
            self.delta_count_history_peak = 0

        log.debug('max history:{} vs peak:{}'.format(
            max(self.history), self.delta_count_history_peak))

    def add_to_history(self, value):
        self.history.append(self.delta_count)
        if len(self.history) > self.history_queue_length:
            self.history.pop(0)
        value = int(sum(self.history) / self.history_queue_length)

        return value

    def force_detection(self):
        self.wasMotionDetected = True

# --------
# INIT.
# --------


# setup system logging facilities
logging.config.dictConfig(LogSettings.LOGGING_CONFIG)
log = logging.getLogger('logtest-debug')
log.setLevel(logging.CRITICAL)
threadlog = logging.getLogger('logtest-debug-thread')
threadlog.setLevel(logging.CRITICAL)

'''
Camera Manager collects any Camera Objects
'''

# log.debug('*debug message!')
# log.info('*info message!')
# log.error('*error message')
# log.warning('warning message')
# log.critical('critical message')
