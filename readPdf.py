from pdf2image import convert_from_path
import cv2 as cv
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

popplerPath = 'poppler'

def extractImages(filePath):
    if filePath:
        pages = convert_from_path(filePath, poppler_path=popplerPath)
        images = []
        for page in pages:
            img = cv.cvtColor(np.array(page), cv.COLOR_RGB2BGR)
            images.append(img)
        return images

### courtesy: CHATGPT
def images2pdf(images, output_path):

    c = canvas.Canvas(output_path, pagesize=letter)
    for i, image in enumerate(images):
        h,w,_ = image.shape
        dim_limit = 800
        max_dim = max(image.shape)
        if max_dim > dim_limit:
            resize_scale = dim_limit / max_dim
            image = cv.resize(image, None, fx=resize_scale, fy=resize_scale)
        h, w, _ = image.shape

        image_path = f"image_{i+1}.jpg"
        cv.imwrite(image_path, image)
        c.drawImage(image_path, 10,800-h, width=w, height=h)
        c.showPage()
    c.save()
