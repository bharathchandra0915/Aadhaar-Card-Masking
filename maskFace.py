import cv2 as cv
faceCascade = cv.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

def detectFace(img):
    gray_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=4,minSize=(200,200))
    # print(faces)
    return faces

def drawBox(img, faceBox):
    pt1 = (faceBox[0], faceBox[1])
    pt2 = (faceBox[0] + faceBox[2], faceBox[1] + faceBox[3])
    cv.rectangle(img, pt1, pt2, (0, 0, 255), 1)
    # print('drawn')

def putBlur(img, roi):
    x,y,w,h = roi
    imgROI = img[y-20:y+h+20, x-20:x+w+20]
    blurImg = cv.blur(imgROI,(50,50))
    img[y-20:y+h+20, x-20:x+w+20] = blurImg
    return img

def maskFace(img):
    input = img.copy()
    face = detectFace(input)
    if len(face) == 0:
        return img
    else:
        masked = putBlur(input,face[0])
        return  masked

