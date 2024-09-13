from openpyxl import load_workbook
from pytesseract import pytesseract
import cv2
import matplotlib.pyplot as plt

from PIL import Image, ImageEnhance
from numpy import ndarray
import numpy as np

path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe" #директория с тессерактом
pytesseract.tesseract_cmd = path_to_tesseract

x = 5
factor = 0.55# increase contrast
fn = 'table.xlsx'
wb = load_workbook(fn)
ws = wb['1']

for i in range(1, 2000):
    image = cv2.imread(f"strings\\{i}.png")
    #обработка изображения
    image = cv2.resize(image, None, fx=x, fy=x)
    height, width, channel = image.shape


    # нормализуем изображение
    '''thresh = cv2.threshold(image, 180, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3 ))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    image = 255 - close'''

    # Create custom kernel
    # Threshold to obtain binary image
    thresh = cv2.threshold(image, 208, 255, cv2.THRESH_BINARY)[1]

    # Create custom kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    # Perform closing (dilation followed by erosion)
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Invert image to use for Tesseract
    img = 255 - close
    image= cv2.GaussianBlur(img, (1, 1), 0)
    # image = Image.open(f"strings\\{i}.png")
    # enhancer = ImageEnhance.Contrast(image)
    # image = image.convert('1')
    # image = enhancer.enhance(factor)
    '''cv2.imshow('original', image)
    cv2.waitKey(0)'''

    # image=image.resize( [int(x * s) for s in image.size] )


    # image=image.convert('1')
    # image.save(f'{i}.png')

    # print(height)

    y=0

    #обрезка изображения

    column1 = image[y:height,35*x:130*x]
    column2 = image[y:height,132 * x:195 * x]
    column3 = image[y:height,195 * x: 350 * x]
    column4 = image[y:height,350 * x: 660 * x]
    column5 = image[y:height,660 * x:  865 * x]
    column6 = image[y:height,865 * x: 950 * x]
    column7 = image[y:height,950 * x: 1060 * x]
    column8 = image[y:height,1060 * x: 1190 * x]
    column9 = image[y:height,1210 * x: 1340 * x]
    column10 = image[y:height,1353 * x:1455 * x]
    column11 = image[y:height,1470 * x: 1570 * x]
    column12 = image[y:height,1570 * x: 1780 * x]

    config = r'--oem 3 --psm 6'
    #детекция текста

    c1 = pytesseract.image_to_string(column1, lang="rus+eng", config=config)
    c2 = pytesseract.image_to_string(column2, lang="rus+eng", config=config)
    c3 = pytesseract.image_to_string(column3, lang="rus+eng", config=config)
    c4 = pytesseract.image_to_string(column4, lang="rus+eng", config=config)
    c5 = pytesseract.image_to_string(column5, lang="rus+eng", config=config)
    c6 = pytesseract.image_to_string(column6, lang="rus+eng", config=config)
    c7 = pytesseract.image_to_string(column7, lang="rus+eng", config=config)
    c8 = pytesseract.image_to_string(column8, config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,.')
    c9 = pytesseract.image_to_string(column9, config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,.')
    c10 = pytesseract.image_to_string(column10, config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,.')
    c11 = pytesseract.image_to_string(column11,config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,.')
    c12 = pytesseract.image_to_string(column12, lang='eng', config=config)
    #исключения
    ''' if '?' in с1:
        c1='?'
    if '?' in с2:
        c2='?'
    if len (c10)<3:
        c10=" "'''

    #внесение в таблицу

    ws.append([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12])
    wb.save(fn)
    wb.close()
    print(f'string {i} is saved')
