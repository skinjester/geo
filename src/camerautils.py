from __future__ import division  # so division works like you expect it to
import numpy as np
import cv2
import time
import datetime
from threading import Thread
import sys
import data
from hud.console import console_log, console_draw

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
        device,
        width,
        height,
        portrait_alignment,
        flip_h=False,
        flip_v=False,
        gamma=1.0,
        floor=1000,
        threshold_filter=32
    ):

        # camera
        self.stream = cv2.VideoCapture(device)
        self.stream.set(3, width)
        self.stream.set(4, height)
        self.width = int(self.stream.get(3))
        self.height = int(self.stream.get(4))

        # image transform
        self.portrait_alignment = portrait_alignment
        self.flip_h = flip_h
        self.flip_v = flip_v

        # gamma
        self.gamma = gamma
        self.table = self.set_gamma(gamma)

        # camera thread
        self.stopped = False

        # motion detection
        self.motiondetector = MotionDetector(floor)
        self.delta = 0  # difference between current frame and previous
        self.buffer_t = np.zeros((self.height, self.width, 3),
            np.uint8)
        self.threshold_filter = threshold_filter

        # frame buffer housekeeping
        self.rawframe = np.zeros((self.height, self.width, 3), np.uint8)
        (self.grabbed,
         self.frame) = self.stream.read()  # initial frame to prime the queue
        self.frame = self.transpose(self.frame)
        self.t_minus = self.transpose(
            cv2.cvtColor(self.stream.read()[1], cv2.COLOR_RGB2GRAY))
        self.t_now = self.transpose(
            cv2.cvtColor(self.stream.read()[1], cv2.COLOR_RGB2GRAY))
        self.t_plus = self.transpose(
            cv2.cvtColor(self.stream.read()[1], cv2.COLOR_RGB2GRAY))

    def start(self):
        Thread(target=self.update, args=()).start()
        log.debug('started camera thread')
        return self

    def set_gamma(self, gamma):
        # generates internal table for gamma correction
        log.debug('gamma: {}'.format(gamma))
        return np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in
            np.arange(0, 256)]).astype("uint8")

    def update_gamma(self, gamma):
        self.table = self.set_gamma(gamma)

    def update(self):
        # loop until the thread is stopped
        while True:
            if self.stopped:
                return
            _, img = self.stream.read()
            self.t_minus = self.t_now
            self.t_now = self.t_plus
            self.t_plus = self.transpose(
                cv2.blur(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), (9, 9))
            )
            self.buffer_t = self.diffImg(
                self.t_minus, self.t_now, self.t_plus
            )
            self.buffer_t = cv2.dilate(
                self.buffer_t, None, iterations=2
            )
            _, self.buffer_t = cv2.threshold(
                self.buffer_t, self.threshold_filter, 255, cv2.THRESH_BINARY
            )
            self.delta = cv2.countNonZero(self.buffer_t)

            # dont process motion detection when paused
            if self.motiondetector.is_paused == False:
                self.motiondetector.process(self.delta)

            # update internal buffer w camera frame
            self.frame = self.gamma_correct(self.transpose(img))

    def read(self):
        log.debug('read camera:{} RGB:{}'.format(self.stream, self.frame.shape))
        return self.frame

    def transpose(self, img):
        if self.portrait_alignment: img = cv2.transpose(img)
        if self.flip_v: img = cv2.flip(img, 0)
        if self.flip_h: img = cv2.flip(img, 1)
        return img

    def gamma_correct(self, img):
        return cv2.LUT(img, self.table)

    def stop(self):
        self.stopped = True

    def diffImg(self, t0, t1, t2):
        d1 = cv2.absdiff(t2, t1)
        d2 = cv2.absdiff(t1, t0)
        return cv2.bitwise_and(d1, d2)


class MotionDetector(object):

    def __init__(self, floor):

        self.delta_history = 0
        self.delta_history_peak = 0
        self.delta_trigger = 0
        self.delta = 0

        self.peak = 0
        self.peak_last = 0
        self.peak_avg = 0
        self.peak_statusmsg = 'Peak is static'

        self.is_paused = False
        self.floor = floor
        self.history = []
        self.history_queue_length = 100
        self.monitor_msg = '****'

    def process(self, delta):
        # history
        self.delta = delta

        # scale value to ride peak values & prevent sensitive triggering
        self.delta_trigger = self.add_to_history(self.delta) + self.floor

        lastmsg = '{:0>6}'.format(self.delta_history)
        nowmsg = '{:0>6}'.format(self.delta)
        console_log('last', lastmsg)
        console_log('now', nowmsg)

        #  track delta count history
        self.delta_history = self.delta

        # track peak value
        if self.delta_history > self.delta_history_peak:
            self.delta_history_peak = self.delta_history
        if self.delta < self.floor:
            self.delta_history_peak = 0
        threadlog.warning('history:{}'.format(self.delta_history))

    def add_to_history(self, value):
        self.history.append(self.delta)
        if len(self.history) > self.history_queue_length:
            self.history.pop(0)
        value = int(sum(self.history) / self.history_queue_length)
        return value

    def increase_floor(self):
        self.floor += data.floor_adjust

    def decrease_floor(self):
        if self.floor - data.floor_adjust < 0:
            self.floor = 0
        else:
            self.floor -= data.floor_adjust

    def toggle_pause(self):
        self.is_paused = not self.is_paused


# --------
# INIT.
# --------
# CRITICAL ERROR WARNING INFO DEBUG
log = data.logging.getLogger('mainlog')
log.setLevel(data.logging.CRITICAL)
threadlog = data.logging.getLogger('threadlog')
threadlog.setLevel(data.logging.CRITICAL)
