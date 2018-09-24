import imutils
import cv2

class BasicMotionDetector:
    '''
    accumWeight: weighted avg between current frame and previous set of frames. A larger value results in the detector _remembering_ less and quickly forgetting what previous frames look like. A high value is useful if you expect lots of motion in a short time

    deltaThresh: smaller values detect more motion, larger values detect less

    minArea: any region of motion smaller than min Area will be ignored
    '''

    def __init__(self, accumWeight=0.5, deltaThresh=5, minArea=5000):
        self.isv2 = imutils.is_cv2()
        self.accumWeight = accumWeight
        self.deltaThresh = deltaThresh
        self.minArea = minArea

        # initialize the average img for motion detection
        self.avg = None

    def update(self, image):
        # initialize the list of locations containing motion
        locs = []

        # if the avg image is None, initialize it
        if self.avg is None:
            self.avg = image.astype("float")
            return locs

        # otherwise, accumulate the weighted average between
        # the current frame and the previous frames, then compute
        # the pixel-wise differences between the current frame
        # and running average
        cv2.accumulateWeighted(image, self.avg, self.accumWeight)
        frameDelta = cv2.absdiff(image, cv2.convertScaleAbs(self.avg))

        # threshold the delta image and apply a series of dilations
        # to help fill in holes
        thresh = cv2.threshold(frameDelta, self.deltaThresh, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # find contours
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if self.isv2 else cnts[1]
        for c in cnts:
            # only add contour to locations list if it exceed minimum area
            if cv2.contourArea(c) > self.minArea:
                locs.append(c)

        return locs
