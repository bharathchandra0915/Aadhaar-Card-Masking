import cv2 as cv
import numpy as np
import pytesseract.pytesseract
from pytesseract import  Output
from blurs import  putBlur

import  streamlit as st

# path = "Tesseract-OCR\\tesseract.exe"
path = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


pytesseract.pytesseract.tesseract_cmd = path
psmValue = 12
myConfig = f"--psm {psmValue} --oem 3 "


# Name, Father Name, Gender, DOB, Gender, Aadhar number

##### SHOWS THE DETECTED WORDS BY PYTESSERACT IN A GREEN GREEN COLOURED BELNDING #######

def showDetected(df,scannedCard):
    for x,y,w,h in zip(df['left'],df['top'],df['width'],df['height']):
        blank_image = np.zeros((h,w, 3), np.uint8)
        blank_image[:, :] = (0, 255, 0)
        scannedCard[y:y+h,x:x+w] = cv.addWeighted(scannedCard[y:y+h,x:x+w],0.99,blank_image,0.3,0)


#####  DETECTS AADHAR CARD NUMBER AND ALSO VID NUMBER IF EXISTS  ######

def detectCardNumber(df,scannedCard):
    numericalValues = df[df['text'].str.contains(r'\d+')]  #### the words having digits in them
    # numericalValues = df[df['text']]
    # print(numericalValues)
    aadharNumberIndex = []
    columns = [0,1,2,3,5]
    i = 0
    number = set()
    while i < len(numericalValues)-1:
        strt = numericalValues.iloc[i].top
        # print(i,strt,abs(numericalValues.iloc[i+1].top- strt ))
        if(abs(numericalValues.iloc[i+1].top- strt)<=20):

            number.add(i)
            number.add(i+1)
        else:
            number = set()
            # print('#'*50)
        # print(number)
        aadharNumberIndex.append(number)
        i += 1

    # print(aadharNumberIndex)
    uniqueIndex = []
    for item in aadharNumberIndex:
        if item not in uniqueIndex:
            uniqueIndex.append(item)

    # print(uniqueIndex)
    aadharNumber = []
    vidNumber = []
    dob = []
    for lineIndices in uniqueIndex:
        if len(lineIndices) == 3:
            tempLst = []
            for i in lineIndices:
                tempLst.append(numericalValues.iloc[i, columns].values.tolist())
            aadharNumber.append(tempLst)

        if len(lineIndices) == 4:
            tempLst = []
            for i in lineIndices:
                tempLst.append(numericalValues.iloc[i, columns].values.tolist())
            vidNumber.append(tempLst)

    # print(len(aadharNumber))
    # print(aadharNumber)

    for number in aadharNumber:
        number = sorted(number, key=lambda x: x[0])
        firstBox = number[0]
        secondBox = number[1]
        ###### We are masking only on first 8 digits i.e first word and second word ######

        putBlur(scannedCard,(firstBox[0], firstBox[1], firstBox[2], firstBox[3]))
        putBlur(scannedCard,(secondBox[0], secondBox[1], secondBox[2], secondBox[3]))

    # print(vidNumber)
    if(len(vidNumber)!=0):
        for number in vidNumber:
            number = sorted(number, key=lambda x: x[0])
            firstBox = number[0]
            secondBox = number[1]
            thirdBox = number[2]

            ###### We are masking the first 12 digits in VID #########

            putBlur(scannedCard, (firstBox[0], firstBox[1], firstBox[2], firstBox[3]))
            putBlur(scannedCard, (secondBox[0], secondBox[1], secondBox[2], secondBox[3]))
            putBlur(scannedCard, (thirdBox[0], thirdBox[1], thirdBox[2], thirdBox[3]))

def detectText(img,scannedCard):

    df = pytesseract.image_to_data(img,config=myConfig,output_type=Output.DATAFRAME, lang='eng')
    df = df[df['conf'] > 10]  ### considering the detections whose confidence > 10
    df.to_csv('filtered.csv')
    df = df.dropna(subset=['text'])
    # st.text('After filtering')
    # st.text(df)
    if df.empty:
        st.text("Unable to Detect Characters")
        return

    df = df[['left', 'top', 'width', 'height', 'conf', 'text']]
    detectCardNumber(df,scannedCard)
    showDetected(df,scannedCard)


def mask(img):
    scannedCard = img.copy()
    imgRGB = cv.cvtColor(scannedCard, cv.COLOR_BGR2RGB)
    imgReturn = scannedCard.copy()
    detectText(imgRGB,imgReturn)
    return  imgReturn

