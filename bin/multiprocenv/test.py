import miaConfig
import cv2
import signal
from miaMultiProcEnv import ReceiveProcess, SendProcess, MiaEnv
from miaCamera import DisplayCam, ReadCam
from miaMotionDetect import miaMotionDetect, miaBuffer
import time
from datetime import datetime

       
if __name__ == '__main__':

    displayVid = DisplayCam()
    Buff=miaBuffer()
    readCam = ReadCam()
    Motion = miaMotionDetect()
    bsPrs=MiaEnv([readCam, Motion, Buff, displayVid])