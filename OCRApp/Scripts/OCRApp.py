import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import spacy


def deskewImage(image):
    """
    Apply skew correction to image
    :param image: raw image data
    :return: Deskew image data
    """
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    # print(angle)

    if angle == 90:
        return image
    elif angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated


def preprocessImage(image):
    """
    Preprocess image prior to performing OCR detection
    1. Normalisation
    2. Denoise
    3. Apply Grayscale
    4. Image Thresholding
    5. Skew Correction
    :param image: raw image data
    :return: processed image data
    """
    kernel = np.ones((2, 2), np.uint8)
    normalise_image = np.zeros((image.shape[0], image.shape[1]))

    processed_image = cv2.normalize(image, normalise_image, 0, 255, cv2.NORM_MINMAX)
    processed_image = cv2.fastNlMeansDenoisingColored(processed_image, None, 10, 10, 7, 15)
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.threshold(processed_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    processed_image = deskewImage(processed_image)

    return processed_image


def main():
    # load the English language model (spaCy)
    # python -m spacy download en_core_web_sm
    nlp = spacy.load("en_core_web_sm")

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    filename = "D:\GitHub\OCR-Claim-Application\OCRApp\Scripts\sample_invoice.png"
    img = cv2.imread(filename)

    """
    detect characters using Tesseract OCR
    """
    img = preprocessImage(img)
    data = pytesseract.image_to_data(img, output_type=Output.DICT)

    """
    Output detected words
    """
    n_boxes = len(data['text'])
    linkedWords = [[(0, 0), ""]]
    xThreshold = 5
    yThreshold = 10

    for i in range(n_boxes):
        if data["text"][i] == "":
            continue

        # if int(data['conf'][i]) > 60:
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])

        # link words depending on x and y coordinates
        if abs(linkedWords[-1][0][0] - x) <= xThreshold and abs(linkedWords[-1][0][1] - y) <= yThreshold:
            # update the latest linked words x (with width) and y coordinate
            linkedWords[-1][0] = (x + w, y)
            linkedWords[-1][1] += f' {data["text"][i]}'
        else:
            linkedWords.append([(x + w, y), data["text"][i]])

        # plot detection on image
        # img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.putText(img, data["text"][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    """
    Named Entity Recognition
    """
    # dictionary to store the text with the respective named entities
    docEntity = dict()

    for element in linkedWords:
        linkedWord = element[1]

        # use spaCy's NER to identify named entities
        doc = nlp(linkedWord)

        for entity in doc.ents:
            # print(entity.label_, entity.text)
            if entity.label_ in docEntity:
                docEntity[entity.label_].append(entity.text)
            else:
                docEntity[entity.label_] = [entity.text]

    return(docEntity)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)


if __name__ == "__main__":
    main()
