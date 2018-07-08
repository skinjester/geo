import cv2

#capture from camera at location 0
cameraID = 0
cap = cv2.VideoCapture(cameraID)

#set the width and height
cap.set(3,1920)
cap.set(4,1080)

def show(img, portrait_alignment=False, flip_h=False, flip_v=False):
    if portrait_alignment: 
        img = cv2.transpose(img)
    if flip_v:
        img = cv2.flip(img, 0)
    if flip_h:
        img = cv2.flip(img, 1)

    cv2.imshow("camera:{}  portrait_alignment:{}  flip_h:{}  flip_v:{}"
        .format(cameraID, portrait_alignment, flip_h, flip_v),
        img)

    return img

while True:
    ret, img = cap.read()
    img = show(img, portrait_alignment=True, flip_h=False, flip_v=True)

    key = cv2.waitKey(10) & 0xEFFFFF
    print "camera: {} keyboard input: {} img shape: {}".format(cameraID, key, img.shape)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows() 