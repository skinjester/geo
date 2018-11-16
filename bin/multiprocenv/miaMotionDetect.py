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
# Name:        New motion detect class and buffer
#              
# Purpose:     Classes which utilize the multi processing environment to
#              check for motion detect and store the context in a buffer 
#
# Author:      Dani Thomas
#
# Requires:    OpenCV
# Based on: 
#-------------------------------------------------------------------------
import miaConfig
import cv2
import signal
from miaMultiProcEnv import TransformProcess, MiaEnv
import Queue
import miaCamera
import miaVideoFile

class miaMotionDetect(TransformProcess):
     changedFrames=0
     staticFrames=0
     delta_thresh = 5
     fps=15.0
     avg=None
     motionDetected=False
     
     def __init__(self):
          config=miaConfig.miaConfig()
          self.framethreshold = int(config.GetConfig('frameThreshold'))
          # The number of non movement frames to count movement has ended
          self.staticthreshold = int(config.GetConfig('staticThreshold'))
          # The minimum size of movement to consider significant
          self.min_area = int(config.GetConfig('min_area'))
          self.MaskedAreas=config.GetConfig('maskedAreas')
          self.CameraWidth=config.GetConfig('SMALL_CAMERA_WIDTH')
          self.checkfps=int(config.GetConfig('checkfps'))
          #if we want to show the motion rectangle or masked area
          self.ShowBlueFrame=config.GetConfig('ShowBlueFrame')
          self.ShowGreenFrame=config.GetConfig('ShowGreenFrame')
          self.calculateCheckRate()
     
     #Calculate how many frames per second to check based on camera fps     
     def calculateCheckRate(self):
          self.checkrate=int(self.fps) // self.checkfps
          if self.checkrate < 1: 
            self.checkrate=1  
                 
     def run(self):
          frames=0
          
          while True:
            pItem=self.ReceiveConn.recv()
            frames=frames+1
            if (pItem is None):break
            if type(pItem)==float:
              self.fps=pItem
              self.calculateCheckRate()
            else:     
              if (frames % self.checkrate == 0):
                  self.checkMotion(pItem)
            self.SendConn.send(pItem)
                  
          self.SendConn.send(None)
          
     def checkMotion(self,frame):
        contours=self.getMotionContours(frame)
        bigMotion,maskedMotion= self.CheckContours(contours,frame)
        if not(self.motionDetected):
            if self.passedMotionThreshold(bigMotion, maskedMotion):
                self.SendConn.send("<release>")
                self.motionDetected=True
        else:
            if self.passedStaticThreshold(bigMotion,maskedMotion):
                self.SendConn.send("<closeup>")
                self.motionDetected=False    
     
     def passedStaticThreshold(self, bigMotion,maskedMotion):
          # Check if motion has finished
          if not(bigMotion or maskedMotion):
            self.staticFrames=self.staticFrames+1
            if self.staticFrames >= self.staticthreshold:
              # Be ready to restart filming if movement starts again
              # Closing file and rewriting a new one uses resources.
              self.changedFrames=self.framethreshold-1
              self.staticFrames=0
              return True
          else:
            self.staticFrames=0
            self.changedFrames=self.changedFrames+1  

     def passedMotionThreshold(self, bigMotion,maskedMotion):
          if maskedMotion or bigMotion:
            self.staticFrames=0
            self.changedFrames=self.changedFrames+1
          elif self.changedFrames > 0:
            self.changedFrames=self.changedFrames - 1
          if bigMotion:
            # Enough to start writing the film
            if self.changedFrames >= self.framethreshold:
              return True
           
     def getMotionContours(self,frame):
        
        # get a monochrome version of frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # blur to fill in small gaps
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if (self.avg is None):
            self.avg = gray.copy().astype("float")
            
        # accumulate the weighted average between the current frame and
        cv2.accumulateWeighted(gray, self.avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta,self.delta_thresh,255,cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        (_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return cnts
        
     def CheckContours(self,cnts,frame):
        bigMotion=False
        maskedMotion=False
        # loop over the contours
        for c in cnts:
 		     # if the contour is too small, ignore it
           cntArea=cv2.contourArea(c)
           if cntArea < self.min_area:
 			        continue
           else:
             (x, y, w, h) = cv2.boundingRect(c)
           # this is to get rid of refresh issues and camera refocussing. If fills the whole frame
           if w>=int(self.CameraWidth)-4:
             continue
           # Totally contained within masked area
           if self.ContainedInMaskAreas(x,y,x + w,y + h,self.MaskedAreas,frame):
             maskedMotion=True
             continue
           if (self.ShowGreenFrame=="on"): 
             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)     
           bigMotion=True
        return (bigMotion,maskedMotion)
     
     # This is part of the Check Motion process
     # Check if the motion is totally contained within a masked area
     def ContainedInMaskAreas(self,x,y,w,h,MaskedAreas,frame):
          for maskedArea in self.MaskedAreas:
             if (self.ShowBlueFrame=="on"):
               cv2.rectangle(frame, (int(maskedArea["x"]), int(maskedArea["y"])), (int(maskedArea["w"]), int(maskedArea["h"])), (255, 0, 0), 1)
             if x < int(maskedArea["x"]):
               continue
             if y < int(maskedArea["y"]):
               continue
             if w > int(maskedArea["w"]):
               continue
             if h > int(maskedArea["h"]):
               continue
             return True
          return False    
     
     
class miaBuffer(TransformProcess):
     fps = 15.0
     release = False
     def __init__(self):
          config=miaConfig.miaConfig()
          self.maxqsize= int(config.GetConfig('maxqsize'))
          self.totalMaxSize = self.fps * self.maxqsize
          self.frameQueue=Queue.Queue()
          
     def run(self):   
          while True:
              if not(self.addItem()):break
              if (self.release):
                  frame=self.frameQueue.get()
                  self.SendConn.send(frame)
              elif self.frameQueue.qsize() > self.totalMaxSize:
                  self.frameQueue.get()
                  
          self.drainQueue()
      
     def addItem(self):
          pItem=self.ReceiveConn.recv()
          if (pItem is None): return False
          elif type(pItem)==float:
              self.fps=pItem
              self.totalMaxSize = self.fps * self.maxqsize
          elif type(pItem)==str:
              if (pItem=="<release>"):
                self.release=True
                self.SendConn.send(self.fps)
              elif (pItem=="<closeup>"):
                self.SendConn.send(pItem)
                self.release=False             
          else:
              self.frameQueue.put(pItem)      
          return True
          
     def drainQueue(self):
          while (self.frameQueue.qsize() > 0):
              frame=self.frameQueue.get()
              if self.release:
                  self.SendConn.send(frame)
          self.release=False
          self.SendConn.send(None)
          
if __name__ == '__main__':
      writeVideo=miaVideoFile.WriteVideofile()
      Buff=miaBuffer()
      redd=miaCamera.ReadCam()
      Motion = miaMotionDetect()
      bsPrs=MiaEnv([redd, Motion, Buff, writeVideo])