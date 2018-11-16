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
# Name:        Video File classes
#              
# Purpose:     Classes which utilize the multi processing environment to
#              read and write video avi files 
#
# Author:      Dani Thomas
#
# Requires:    OpenCV
# Based on: 
#-------------------------------------------------------------------------
import miaConfig
from datetime import datetime
import os
import cv2
import signal
from miaMultiProcEnv import ReceiveProcess, SendProcess, MiaEnv

class ReadVideofile(SendProcess):
    terminate=False
    
    def quitGracefully(self,signum, frame):
        self.terminate=True
        
    def __init__(self,videoFile):
      # If control c is pressed should quit everything gracefully
      signal.signal(signal.SIGINT, self.quitGracefully)
      self.cap = cv2.VideoCapture(videoFile)
      self.fps=self.GetFramesPerSecond(self.cap)
              
    def run(self):
      self.SendConn.send(self.fps) # Send the frames per second down the pipe
      while(self.cap.isOpened() and not(self.terminate)):
        ret, frame = self.cap.read()
        if ret:
          self.SendConn.send(frame)
        else:
          break
      self.SendConn.send(None) # Sending None will terminate the other processes
      self.cap.release()
      return
    
    # frames per second can be retrieved from file
    def GetFramesPerSecond(self,video):
      (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
      if int(major_ver)  < 3 :
        return video.get(cv2.cv.CV_CAP_PROP_FPS)
      else :
        return video.get(cv2.CAP_PROP_FPS)
      
class WriteVideofile(ReceiveProcess):
    fps = 15.0  # Temporary frames per second
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    filming=False
    videoFullPath=None
    
    # Can be initialized either by a filename and pic size from initializing or otherwise
    # uses config values and datestamp
    def __init__(self,videoFullPath=None,camWidth=None, camHeight=None):
        config=miaConfig.miaConfig()
        if (videoFullPath is None):
          self.videoDir=str(config.GetConfig('VIDEO_ROOT') + config.GetConfig('VIDEO_DIR'))
          self.videoName=str(config.GetConfig('VIDEO_NAME'))
        else:
          self.videoFullPath=videoFullPath
        if (camWidth is None):
          self.camWidth=int(config.GetConfig('SMALL_CAMERA_WIDTH'))
        else:
          self.camWidth=camWidth
        if (camHeight is None):
          self.camHeight=int(config.GetConfig('SMALL_CAMERA_HEIGHT'))
        else:
          self.camHeight=camHeight
    
    # closes up video file
    def closeup(self,video):
        if self.filming:
          self.filming=False
          video.release
         
    def run(self):
        video=None
        while True:
          pItem=self.ReceiveConn.recv()
          if (pItem is None): break # terminate if item is none
          elif type(pItem)==str:    # if receiving closeup we close file without terminating
              if (pItem=="<closeup>"):
                self.closeup(video)
                video=None
          elif type(pItem)==float:
              self.fps=pItem
          else:
              if not(self.filming):
                video=self.openVideoFile()
                self.filming=True  
              video.write(pItem)
        
        self.closeup(video)
    
    # opens a new video file                 
    def openVideoFile(self):
        # if the filename isn't passed in init use config and datestamp
        if self.videoFullPath is None:
          start=datetime.now()
          videoPath=str.format(self.videoDir, start.strftime("%Y-%m-%d"))
          videoName=str.format(self.videoName,start.strftime("%H-%M-%S-%f"))
          videoFullPath=os.path.join(videoPath,videoName)
          if not os.path.exists(videoPath):
              os.makedirs(videoPath)
        else:
          videoFullPath=self.videoFullPath
        video=cv2.VideoWriter(videoFullPath, self.fourcc, self.fps, (self.camWidth,self.camHeight))
        return video
        
if __name__ == '__main__':        
    rdVid=ReadVideofile('./Video12-09-52-175806.avi')
    writeVideo=WriteVideofile('./temp.avi')
    bsPrs=MiaEnv([rdVid, writeVideo])