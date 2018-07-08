#!/usr/bin/python
import cv2

class VideoApp(object):
	"""
	This is a base class for an application that uses an OpenCV window to display data from a webcam,
	and manipulates each frame of data as defined in `processFrame`.
	This class was written for the OpenCV module info session on Nov. 16, 2013, for 15-112 at CMU.
	You may use it for your term project but you must cite it appropriately.
	"""
	def __init__(self, title="Video", delay_ms=100):
		self.title = title
		self.delay = delay_ms
		self.done = False
	def _initWrapper(self):
		cv2.namedWindow(self.title, cv2.CV_WINDOW_AUTOSIZE)
		cv2.setMouseCallback(self.title,self._mouseEvent)
		self.cap = self.getCapture()
		self.init()
	def run(self):
		self._initWrapper()
		try:
			while self.cap.isOpened():
				ret, frame = self.cap.read()
				if frame is not None:
					img = self.processFrame(frame)
					cv2.imshow(self.title, img)
				k = cv2.waitKey(self.delay) & 0xFF
				if k != (~0 & 0xFF): # All 1s
					self._keyPressedWrapper(k)
				if self.done:
					break
		finally:
			cv2.destroyAllWindows()
			self.cap.release()
	def _mouseEvent(self, event, x, y, flags, param):
		"""Relays a mouse event to the method corresponding to its event code."""
		if event == cv2.EVENT_LBUTTONDOWN:
			self.mouseLeftDown(x, y, flags, param)
		elif event == cv2.EVENT_LBUTTONUP:
			self.mouseLeftUp(x, y, flags, param)
		elif event == cv2.EVENT_RBUTTONDOWN:
			self.mouseRightDown(x, y, flags, param)
		elif event == cv2.EVENT_RBUTTONUP:
			self.mouseRightUp(x, y, flags, param)
		elif event == cv2.EVENT_MOUSEMOVE:
			self.mouseMove(x, y, flags, param)
	def _keyPressedWrapper(self, k):
		if k == 27: # Esc
			self.done = True
		self.keyPressed(k) 
	def init(self):
		pass
	def keyPressed(self, k):
		pass
	def processFrame(self, frame):
		return frame
	def mouseLeftDown(self, x, y, flags, param):
		pass
	def mouseLeftUp(self, x, y, flags, param):
		pass
	def mouseRightDown(self, x, y, flags, param):
		pass
	def mouseRightUp(self, x, y, flags, param):
		pass
	def mouseMove(self, x, y, flags, param):
		pass
        
class WebcamApp(VideoApp):
	def __init__(self, title="Webcam", delay_ms=100, camera=0):
		self.camera = camera
		super(WebcamApp, self).__init__(title, delay_ms)
	def getCapture(self):
		return cv2.VideoCapture(self.camera)

class VideoFileApp(VideoApp):
	def __init__(self, title="Video File", delay_ms=20, filename=''):
		if not filename:
			raise ValueError("VideoFileApp requires a valid file path.")
		self.filename = filename
		super(VideoFileApp, self).__init__(title, delay_ms)
	def getCapture(self):
		return cv2.VideoCapture(self.filename)

app = WebcamApp("My awesome app", 1000, 0)
app.run()
