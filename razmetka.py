import PIL
import PIL.ImageOps

from pytesseract import pytesseract
import cv2
from PIL import Image, ImageEnhance, ImageOps

# для работы тессеракта
path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract
# стартовая строка и кадр
start = 2
saved_frame = 1
all = 12910
# кратность увеличения
x = 3
factor = 3  # increase contrast
step = 10  # шаг кадров
config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789,.'
import matplotlib.pyplot as plt

# цикл по строкам
for i in range(start, 2001):
    print(i)
    flag = 0
    # цикл по кадрам начиная с кадра , с которого взяли предыдущий кадр
    for frame in range(saved_frame, 17480, +step):
        # image = cv2.imread("test.png")
        # или вы можете использовать подушку
        image = Image.open(f"frames/{frame}.png")

        enhancer = ImageEnhance.Contrast(image)
        # image = image.convert('1')
        image = enhancer.enhance(factor)
        # print(frame)
        # определяем высоту и ширину
        width = image.size[0]
        hight = image.size[1]

        # обрезка изображения по первому столбцу
        image.crop((1, 300, 32, hight)).save('1.png', quality=100)
        # передаем обрезанное изображение с cv
        id = cv2.imread("1.png")
        id = cv2.resize(id, None, fx=x, fy=x)  # Увеличение изображения в x раз
        # нормализуем изображение
        thresh = cv2.threshold(id, 150, 255, cv2.THRESH_BINARY_INV)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        id = 255 - close

        # config = 'digits'

        # Распознавание

        check = pytesseract.image_to_string(id, config=config)
        data = pytesseract.image_to_data(id, config=config, output_type=pytesseract.Output.DICT)
        # разбиваем данные на строки
        check = [''.join(check)]
        check = check[0].split("\n")
        print(check)

        # проверка каждой строки в кажре
        for a in range(len(check)):
            # print(a)
            # если текущий и предыдущими совпали с искомыми
            if (str(i) == check[a]) & (str(i - 1) == check[a - 1]):
                top = str(i - 1)
                down = str(i)
                # получить все вхождения нужного слова
                word_occurences = [i for i, word in enumerate(data['text']) if word.lower() == top]
                for occ in word_occurences:
                    # извлекаем верхнюю обнаруженного слова
                    t1 = data["top"][occ] // x
                    break
                word_occurences = [i for i, word in enumerate(data['text']) if word.lower() == down]
                for occ in word_occurences:
                    # извлекаем верхнюю обнаруженного слова
                    t2 = data["top"][occ] // x
                    break
                if frame >= saved_frame:
                    image = Image.open(f"frames/{frame}.png")
                    # сохранение строки, вырезая из текущего кадра по координатам и задаем флаг
                    image_name = str(i - 1) + '.png'
                    image.crop((0, t1 + 295, width, t2 + 290)).save('strings/' + image_name, quality=100)
                    flag = 1
                    saved_frame = frame
                    print("saved " + str(saved_frame) + " frame")
                break
        # выход по флаг
        if flag == 1:
            break
