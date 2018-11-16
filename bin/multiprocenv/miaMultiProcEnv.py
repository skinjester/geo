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
# Name:        MultiProcessing Environment
#              
# Purpose:     System to simply pass data such as images between processes via
#              one way pipesSend process sends data to a transform process which 
#              sends to a receive process see testMultiProcEnv.py for usage.
#
# Author:      Dani Thomas
#
# Requires:    
# Based on: 
#-------------------------------------------------------------------------
import multiprocessing
import signal

class TransformProcess(multiprocessing.Process):
    def __init__(self):
        pass   

    def init(self,ReceiveConn, SendConn):
        super(TransformProcess, self).__init__()
        self.ReceiveConn=ReceiveConn
        self.SendConn=SendConn

class SendProcess(multiprocessing.Process):
    def __init__(self):
        pass

    def init(self,SendConn):
        super(SendProcess, self).__init__()
        self.SendConn=SendConn

class ReceiveProcess(multiprocessing.Process):
    def _init__(self):
        pass

    def init(self,ReceiveConn):
        super(ReceiveProcess,self).__init__()
        self.ReceiveConn=ReceiveConn

class MiaEnv():
  SendConnList=[]
  ReceiveConnList=[]
  ProcessObjectSList=[]
  
  def SetupObject(self, ProcessList, ParentReceiveConn=None):
       ReceiveConn=None
       if not(ProcessList==[]):
           ProcessObject=ProcessList.pop(0)
   
           if type(ProcessObject)==list:
               for SubList in ProcessObject:
                   self.SetupObject(SubList,ParentReceiveConn)
               return
           if (ParentReceiveConn==None):
               ReceiveConn,SendConn = multiprocessing.Pipe(duplex=False)
               self.ReceiveConnList.append(ReceiveConn)
               self.SendConnList.append(SendConn)
               ProcessObject.init(SendConn)
           elif (ProcessList==[]):
               ProcessObject.init(ParentReceiveConn)
           else:
                ReceiveConn,SendConn = multiprocessing.Pipe(duplex=False)
                self.ReceiveConnList.append(ReceiveConn)
                self.SendConnList.append(SendConn)
                ProcessObject.init(ParentReceiveConn,SendConn)
                
           self.ProcessObjectSList.append(ProcessObject)
           ProcessObject.start()
           self.SetupObject(ProcessList,ReceiveConn)
        
  def __init__(self, ProcessList):

        self.SetupObject(ProcessList)

        for ProcessObject in self.ProcessObjectSList:
            ind=self.ProcessObjectSList.index(ProcessObject)
            ProcessObject.join()

        for SendConnObject in self.SendConnList:
            SendConnObject.close

        for ReceiveConnObject in self.ReceiveConnList:
            ReceiveConnObject.close()