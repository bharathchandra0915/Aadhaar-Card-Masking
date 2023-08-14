import cv2 as cv
import streamlit as st
import numpy as np
from ocr import mask
from maskFace import maskFace
from grabcut import grabCutScan
from readPdf import extractImages, images2pdf
import  os
import tempfile

@st.cache_data
def scanningAadhar(img,scan):
    if scan.lower() == 'yes':
        scannedCard = grabCutScan(img)
        return scannedCard
    if scan.lower()  == 'no':
        return img

@st.cache_data
def orientation(scannedCard, axis):
    scannedCard = cv.flip(scannedCard,axis)
    return scannedCard

    #### axis = 0 means flip over X-asis
    #### axis = 1 means flip over Y-asis


@st.cache_data
def maskingAadhar (scannedCard):
    maskedCard = mask(scannedCard)
    return maskedCard

@st.cache_data
def displayOnStreamlit(Name,imgShow,faceMask):
    if faceMask:
        imgShow = maskFace(imgShow)
    st.text(Name)
    st.image(imgShow, channels='BGR')

# @st.cache_data
def pdfImages(fileName, maskedCards):
    if not os.path.exists(f'{fileName}_masked'):
        os.mkdir(f'{fileName}_masked')
    pdf_path = f'{fileName}_masked/{fileName}.pdf'
    # pdf_filename = f'{fileName}.pdf'
    images2pdf(maskedCards, pdf_path)

    with open(pdf_path, "rb") as file:
        st.download_button("Download Your Masked Aadhar", file.read(), file_name=f'{fileName}_masked.pdf', mime="application/pdf")


def performTask(images,faceMask):
    maskedCards = []
    for img in images:

        imgShow = np.array(img)
        displayOnStreamlit('Input Card', imgShow, faceMask)

        option = st.sidebar.radio("Do you Need a Scan?", ("Yes", "No"), index=1)
        scannedCard = scanningAadhar(img,option)

        displayOnStreamlit('Scanned Aadhar', scannedCard, faceMask)

        editOrientation = st.sidebar.checkbox('Edit Orientation',value=False)
        if editOrientation:

            flipAlongX = st.checkbox('Flip over X-axis',value = False)
            flipAlongY = st.checkbox('Flip over Y-axis',value = False)
            if flipAlongX:
                scannedCard = cv.flip(scannedCard,0)
            if flipAlongY:
                scannedCard= cv.flip(scannedCard,1)

            displayOnStreamlit('After Orientation',scannedCard , faceMask)


        maskedCard = maskingAadhar(scannedCard)
        displayOnStreamlit('Masked Card', maskedCard, faceMask)

        maskedCards.append(maskedCard)

    return maskedCards


def main():
    st.title('Aadhar Card Masking')
    st.subheader('Mask your Aadhar card Number')
    # Add custom CSS styles
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('bg.jpg');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    filePath = st.file_uploader("Upload Your Aadhar Card", type=['jpg', 'png', 'jpeg','pdf'])
    faceMask = st.sidebar.checkbox('MaskMyFace',value=False)

    if not filePath:
        return None
    else:
        fileName, extension = filePath.name.split('.')

    if extension.lower()  == 'pdf':
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(filePath.read())
            temp_path = temp_file.name
        images = extractImages(temp_path)
        os.remove(temp_path)
        maskedCards = performTask(images, faceMask)
        pdfImages(fileName, maskedCards)


    else:  ### the inputed file is an image file
        file_bytes = np.asarray(bytearray(filePath.read()), dtype=np.uint8)
        img = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
        input = [img]
        maskedCard = performTask(input, faceMask)[0] ### since this returns only one masked card
        image_bytes = cv.imencode(".png", maskedCard)[1].tobytes()
        file_name = f"masked_{fileName}.{extension}"
        mime_type = "image/png"
        st.download_button(label="Download Your Masked Aadhar",
                           data=image_bytes,
                           file_name=file_name,
                           mime=mime_type)

if __name__ == "__main__":
    main()

