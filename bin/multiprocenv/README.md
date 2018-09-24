This is an environment that makes it easy to string various processes together to manipulate video images including streaming to a web page. You create a list of componets in the order you want. Requires OpenCV. It includes the ability to do motion detect from a camera and write to a video file. 

 ==============================

 Display video from the camera.
 
 ==============================
 
 readCam = ReadCam()
 
 displayVid = DisplayCam()
 
 bsPrs=MiaEnv([readCam, displayVid])
 
 ==============================================
 
 Read a video file and write to a separate file
 
 ==============================================
 
 rdVid=ReadVideofile('./Video12-09-52-175806.avi')
 
 writeVideo=WriteVideofile('./temp.avi')
 
 bsPrs=MiaEnv([rdVid, writeVideo])
 
 ==============================
 
 Write motion detect to a file.
 
 ==============================
 
 writeVideo=WriteVideofile()
 
 Buff=miaBuffer()
 
 redd=ReadCam()
 
 Motion = miaMotionDetect()
 
 bsPrs=MiaEnv([redd, Motion, Buff, writeVideo])
 
 =================================================
 
 Display camera to web page. Open page in browser.
 
 =================================================
 
 mserv= miaWebServer()
 
 readCam = ReadCam()
 
 bsPrs=MiaEnv([readCam, mserv])
 
 =======================================================================
 
 Display camera with motion detection to web page. Open page in browser.
 
 =======================================================================
 
 mserv= miaWebServer()
 
 readCam = ReadCam()
 
 Motion = miaMotionDetect()
 
 bsPrs=MiaEnv([readCam, Motion, mserv])
 

For more info visit the blog post http://cyber-renegade.org/2018/04/02/micro-processing-video-image-environment/