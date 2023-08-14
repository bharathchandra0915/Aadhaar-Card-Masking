import  cv2 as cv
import numpy as np

### mask Function is yet to be developed
def mask(img, roi, bg, pattern):
    x, y, w, h = roi
    if bg == 'white':
        patch = np.ones((h, w, 3), np.uint8) * 255
        color = 0
    elif bg == 'black':
        patch = np.ones((h, w, 3), np.uint8) * 0
        color = 1
    else:
        imgroi = img[y:y+h, x:x+w]
        patch = cv.blur(imgroi,(10,10))
    if pattern == 1:
        ## put pattern on the patch
        img = putPattern(img,)
    else:
        ## just return the patch (with overlaying)
        img[y:y + h, x:x + w] = patch
        return img

def putBlur(img, roi):
    x,y,w,h = roi
    imgROI = img[y:y+h, x:x+w]
    blurImg = cv.blur(imgROI,(50,50))
    img[y:y + h, x:x + w] = blurImg
    return img

def putColor(img, roi,code):
    if code == 0:
        color = 0
    else:
        color = 255
    x,y,w,h = roi
    patch = np.ones((h,w,3),np.uint8)*color
    img[y:y + h, x:x + w] = patch
    return img

def putPattern(img, roi, color):
    x,y,w,h = roi

    if color == 0:
        color = 0
    else:
        color = 255

    font = cv.FONT_HERSHEY_TRIPLEX
    scale = 1
    thickness = 2
    text ='XXXX XXXX'
    size = cv.getTextSize(text,font,scale,thickness)
    print(size)

    pw,ph = size[0]
    pattern = np.ones((ph,pw,3),np.uint8)*200
    originY = ph - (ph-h)//2
    cv.putText(pattern,text,(0,originY),font,scale,(0,0,0),thickness)
    patch = cv.resize(pattern,(w,h))
    img[y:y + h, x:x + w] = patch
    return  img

