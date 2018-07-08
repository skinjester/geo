import cv2

# max 2304 x 1536
# 1920 x 1080
# 1600 x 896
# 1280 x 720
# 960 x 720
# 864 x 480
# 800 x 600
# 640 x 480
# 640 x 360
# 352 x 288
# 320 x 240
# 320 x 180


# horizontal = cv2.flip( img, 0 )
# vertical = cv2.flip( img, 1 )
# horizontal + vertical = cv2.flip( img, -1 )


# create named windows
cv2.namedWindow('webcam0',cv2.WINDOW_NORMAL)
cv2.namedWindow('webcam1',cv2.WINDOW_NORMAL)

# collect camera objects
cap = []
cap.append(cv2.VideoCapture(0))
# disabled for single camera setup
#cap.append(cv2.VideoCapture(1))

font = cv2.FONT_HERSHEY_SIMPLEX


# set the width and height
for index,the_camera in enumerate(cap):
    # the_camera.set(3,1920)
    # the_camera.set(4,1080)

    the_camera.set(3,800)
    the_camera.set(4,540)


while True:
    for camera_index,the_camera in enumerate(cap):
        ret, img = the_camera.read()

        if camera_index == 0:
            # img = cv2.flip(cv2.transpose(img),1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2,2))
            equalized = clahe.apply(gray)
            img = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
            cv2.putText(img,'camera 0',(10,20), font, 0.51, (0,255,0), 1, cv2.LINE_AA)
            cv2.imshow('webcam0', img)
            print img.shape
        else:
            img = cv2.flip(cv2.transpose(img),0)
            cv2.putText(img,'camera 1',(10,20), font, 0.51, (0,255,0), 1, cv2.LINE_AA)
            cv2.imshow('webcam1', img)

    # adaptive contrast filtering
    #img = cv2.transpose(img)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    #equalized = clahe.apply(gray)


    key = cv2.waitKey(10) & 0xFF
    if key == 27: # ESC
        break


cv2.destroyAllWindows() 

for the_camera in cap:
    the_camera.release()