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
# Name:        Video Streming Server
#              
# Purpose:     Class which utilize the multi processing environment to
#              stream images to the web 
#
# Author:      Dani Thomas
#
# Requires:    OpenCV
# Based on: 
#-------------------------------------------------------------------------
import socket
import cv2
from miaCamera import ReadCam
from miaMultiProcEnv import ReceiveProcess, MiaEnv

class miaWebServer(ReceiveProcess):

    def run(self):
        HOST, PORT = '', 8888
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((HOST, PORT))
        listen_socket.listen(1)

        while True:
            client_connection, client_address = listen_socket.accept()
            request = client_connection.recv(1024)
            fstLine = request.split('\r\n', 1)[0]
            if (fstLine == "GET / HTTP/1.1"):
                http_response = b'\r\nHTTP/1.1 200 OK\r\n\r\n<html><head>' \
                                b'<title>Cyber-Renegade Video Streaming Demonstration</title>' \
                                b'</head><body><h1>Cyber-Renegade Video Streaming Demonstration</h1>' \
                                b'<img id="bg" src="/video_feed">' \
                                b'</body></html>'
                client_connection.sendall(http_response)
                client_connection.close()
            elif (fstLine == "GET /video_feed HTTP/1.1"):
                self.generateStream(client_connection)
                client_connection.close()
                break

    def generateStream(self,client_connection):
        http_response = b'\r\nHTTP/1.1 200 OK\r\n' \
                        b'Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n'
        client_connection.sendall(http_response)
        while True:
            frame=self.ReceiveConn.recv()
            if frame is None: break
            elif type(frame)==float:continue
            elif type(frame)==str:continue
            ret, jpeg = cv2.imencode('.jpg', frame)
            http_response = (b'--frame\r\n' \
                             b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            client_connection.sendall(http_response)
            
if __name__ == '__main__':
    
    mserv= miaWebServer()
    readCam = ReadCam()
    bsPrs=MiaEnv([readCam, mserv])
    