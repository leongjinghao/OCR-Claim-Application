import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import nltk
import spacy

# download the necessary NLTK data (if not already downloaded)
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')

# load the English language model (spaCy)
# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
filename = "sample_invoice.png"
img = cv2.imread(filename)


def deskewImage(image):
    """
    Apply skew correction to image
    :param image: raw image data
    :return: Deskew image data
    """
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    print(angle)
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
    5. Dilation
    6. Erosion
    7. Morphology Transformation
    8. Canny Edge Detection
    9 . Skew Correction
    :param image: raw image data
    :return: processed image data
    """
    kernel = np.ones((2, 2), np.uint8)
    normalise_image = np.zeros((image.shape[0], image.shape[1]))

    processed_image = cv2.normalize(image, normalise_image, 0, 255, cv2.NORM_MINMAX)
    processed_image = cv2.fastNlMeansDenoisingColored(processed_image, None, 10, 10, 7, 15)
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.threshold(processed_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # processed_image = cv2.dilate(processed_image, kernel, iterations=1)
    # processed_image = cv2.erode(processed_image, kernel, iterations=1)
    # processed_image = cv2.morphologyEx(processed_image, cv2.MORPH_OPEN, kernel)
    # processed_image = cv2.Canny(processed_image, 100, 200)
    # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # processed_image = cv2.filter2D(processed_image, -1, kernel)
    processed_image = deskewImage(processed_image)

    return processed_image


"""
Print detected words
"""
img = preprocessImage(img)
# text = pytesseract.image_to_string(img)
# print(text)
data = pytesseract.image_to_data(img, output_type=Output.DICT)
# print(data.keys())
print(data["text"])

"""
Output detected characters
"""
# h, w = img.shape
# boxes = pytesseract.image_to_boxes(img)
# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
#
# cv2.imshow('img', img)
# cv2.waitKey(0)

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
    img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.putText(img, data["text"][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

"""
Named Entity Recognition
"""
#https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
for element in linkedWords:
    linkedWord = element[1]

    # tokenize the string into words
    tokens = nltk.word_tokenize(linkedWord)

    # use NLTK's NER to identify named entities
    named_entities = nltk.ne_chunk(nltk.pos_tag(tokens))

    # loop through each named entity and print out any that are classified as a person or location (NLTK)
    # for ne in named_entities:
    #     if hasattr(ne, 'label'):
    #         print(ne.label(), ' '.join(c[0] for c in ne))

    # use spaCy's NER to identify named entities
    doc = nlp(linkedWord)
    for entity in doc.ents:
        print(entity.label_, entity.text)

cv2.imshow('img', img)
cv2.waitKey(0)
