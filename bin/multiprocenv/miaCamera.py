#! /usr/bin/env python
#--------------------------------------------------------------------------
# Copyright 2018 Cyber-Renegade.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Name:        Video Camera classes
#              
# Purpose:     Classes which utilize the multi processing environment to
#              capture the video and display using OpenCV 
#
# Author:      Dani Thomas
#
# Requires:    OpenCV
# Based on: 
#-------------------------------------------------------------------------
import miaConfig
import cv2
import signal
from miaMultiProcEnv import ReceiveProcess, SendProcess, MiaEnv
import time
from datetime import datetime

class ReadCam(SendProcess):
    SRC=0
    terminate=False
    fps=15.0
    frameType=""
    
    def quitGracefully(self,signum, frame):
        self.terminate=True
        
    def __init__(self,frameType=""):
        config=miaConfig.miaConfig()
        self.frameType=frameType
        # If control c is pressed should quit everything gracefully
        signal.signal(signal.SIGINT, self.quitGracefully)
        
        # Initialize the camera stream  
        self.stream = cv2.VideoCapture(self.SRC)
        self.stream.set(int(config.GetConfig('CAP_PROP_FRAME_WIDTH')), int(config.GetConfig('SMALL_CAMERA_WIDTH')))
        self.stream.set(int(config.GetConfig('CAP_PROP_FRAME_HEIGHT')), int(config.GetConfig('SMALL_CAMERA_HEIGHT')))

    def run(self):
        # Loop reading frames from the camera
        frames=0
        frameUnit=1200
        while not(self.terminate):
          (grabbed, frame) = self.stream.read()
          if grabbed and self.frameType=="jpeg":
            ret, frame = cv2.imencode('.jpg', frame)
          self.SendConn.send(frame) 
          frames=frames+1
          if frames == frameUnit:
            self.startTime=datetime.now()
          elif frames== (frameUnit * 2):
            newfps=frameUnit//(datetime.now()-self.startTime).total_seconds()
            if (newfps<> self.fps):
              self.fps=newfps
              self.SendConn.send(self.fps)
            frames=0    
        self.SendConn.send(None)
        self.stream.release()
        return
      
class DisplayCam(ReceiveProcess):
 
    def run(self):
      while True:
        frame=self.ReceiveConn.recv()
        if frame is None: break
        elif type(frame)==float:continue
        elif type(frame)==str:continue
        cv2.imshow('frame',frame)
        cv2.waitKey(1)
      cv2.destroyAllWindows()
      return  

        
if __name__ == '__main__':

    displayVid = DisplayCam()
    readCam = ReadCam()
    bsPrs=MiaEnv([readCam, displayVid])