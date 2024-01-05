# Methodology
![image](https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/f57a3c9c-a7b4-4581-b6a5-c79eaabab209)
The OCR application is integrated as an external module, establishing communication with the Claim form system via a web API. Upon uploading an image to the Claim form system, it promptly forwards the image as input to the OCR application through the API. Subsequently, the OCR application initiates a sequence of intricate processes, encompassing image processing, text detection, post-processing, and classification utilising machine learning algorithms. Once these processes are successfully executed, the OCR application generates a well-organised list of structured data, which is promptly transmitted back to the Claim form system through the API. In this return journey, the structured data seamlessly facilitates the autofill process for the claim form, ensuring a streamlined and efficient experience for the user.

-	Design system architecture
The high level architecture of the OCR Application to be deployed. The standalone system will consist of the backend system, for servicing and processing external requests. 
-	Input and output of OCR application
    -	Input: Image of invoice sent from Claims module
    -	Output: Detected words/figures from Image sent, with the ability to determine if multiple words/figures are meant to be linked together, e.g. name, address.
-	Web API: 
The OCR Application will be deployed as a Web API to serve users’ requests when an image or document is uploaded on the Claims module.
-	OCR Application
    -	Image processing: 
    Pre-processing steps to improve the quality of the input image.
    -	OCR engine design: 
    The OCR engine’s technology and model design.
    -	Algorithm for merging words: 
    Mechanism to merge words which are meant to be interpreted collectively.
    - Detected fields classifier: 
    Mechanism to convert unstructured data from output of OCR application to structured data.
-	Integrate with Claim form system for autofill capability

# System Architecture
![image](https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/f6a1e886-b7db-4f05-b4f0-c4ea3a0904f9)

The proposed system adopts a client-server architecture to facilitate communication and interaction between system components. At the core of this architecture, the backend server encompasses the OCR application responsible for processing uploaded images, performing image processing, OCR, text merging algorithm, and classification using machine learning technique. The web API is implemented to handle client request and communication with the server, it serves as the interface through which the frontend application can interact with. The frontend application, serving as the client, allows users to upload image attachments of invoices onto the system.
When an image is uploaded, the frontend application makes a request to the web API, triggering the OCR application to process the image and generates structured data representing the labelled detected fields. This structured data is then sent back to the claim module through the web API, and utilised to facilitate the autofill process on the frontend application.

# Image Processing
## Normalisation
<p align="center">
  <img src=https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/89e59ec0-dd88-4eca-aac5-a85d093bf821" />
</p>

The image normalisation technique employed in the proposed system is min-max normalisation, a widely used method in image processing. The goal of image normalisation is to scale the pixel values of an image to a specific range, making it easier to process and analyse the image data. The cv2.normalize() function is utilised for the implementation, which takes the input image and transforms it pixel values to fit within the range of 0 to 255.
Through apply min-max normalisation, the entire pixel intensity range of the image is stretched or compressed to match the desired range. In the cv2.normalize() function, the parameters 0 and 255 represent the minimum and maximum values of the new range, respectively. The method ensures that the minimum pixel value in the original image is mapped to 0, and the maximum pixel value in the original image is mapped to 255, while the other pixel values are linearly interpolated in between.

## Denoise
<p align="center">
  <img src=https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/21634b39-7e40-48fa-bb14-7c8fecaa6cf2" />
</p>

The image denoise technique employed in the proposed system is the non-local means (NLM) algorithm which reduces noise and enhancing the quality of images. The cv2.fastNlMeansDenoisingColored() function is utilised for the implementation, specifically designed to handle coloured images with additive Gaussian noise.

## Grayscale
The grayscale conversion method utilised in the proposed system is the luminosity method, implemented using cv2.COLOR_BGR2GRAY. This method involves assigning weights to each colour channel for the conversion from RGB colour space to a grayscale representation.

## Thresholding
![image](https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/07ebd009-9b6c-4fc9-abda-eb4f43e74f16)

The image thresholding technique utilised in the proposed system is the Otsu’s thresholding method, implemented using cv2.THRESH_OTSU. This method calculates an optimal threshold value that separates the foreground and background pixels by maximising the between-class variance of the pixel intensities. 

## Skew Correction
![image](https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/f54acdea-0851-405d-aa6b-5cda149724b1)

The image skew correction technique utilised in the proposed system employs the cv2.minAreaRect function, which drew inspiration from another relevant implementation. While this method is not specifically designed for skew angle detection, the function calculates the minimum bounding rectangle for a given contour or a set of points within the image. As the bounding rectangle is oriented at an angle that corresponds to the principal axis, an estimate of the skew angle can be derived from the algorithm. can be derived from the algorithm
![image](https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/daa2e8d2-7753-4dac-80a3-2ce1ada561b2)

To address the correction of left skewed images, the process involves making two key assumptions to infer the skew direction accurately. Firstly, it assumed that the image is in a portrait orientation, and secondly, that the image is vertically upright. Consequently, the base of the image is expected to be shorter than the sides. By establishing this premise, the skew direction can be determined through comparing the lengths of the base and sides of the image. Specifically, if the left of the base is found to be longer than the sides, the image is identified as left skewed.
To calculate the correct skew angle in such cases, the angle in the opposite quadrant can be calculated, where skew angle = 90 degree - obtained angle.

# OCR Engine
The Optical Character Recognition (OCR) engine deployed in the proposed system is Tesseract OCR. The OCR engine is the core component of the OCR application that performs the actual detection and recognition of the text from the processed input image. 

## Tesseract OCR Implementation
The implementation of Tesseract OCR with Python involves installing the required dependencies, namely the Pytesseract package and the Tesseract binary file. With these dependencies installed, the Tesseract OCR engine can be initiated in Python. The OCR process can then be performed using the pytesseract.image_to_data function, which takes an image as input and performs the optical character recognition on it.

## Text Merging Algorithm
<p align="center">
  <img src=https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/98d1931b-c25a-4050-941d-ec19d902112f" />
</p>

The text merging algorithm is a vital component in the post processing phase after the OCR output has been retrieved. The objective of the text merging algorithm is to combine individual text blocks that are meant to be interpreted as cohesive entity, such as words and phrases.
To accomplish this, the algorithm utilises a proximity-based approach, connecting text blocks on each row based on analysing the white spaces between them. The algorithm takes into account the x and y coordinates, width, and height of the detected text blocks during the segmentation stage to calculate the spatial distance between them. By considering this information, the algorithm can accurately merge adjacent text blocks that form part of the same textual entity, effectively reconstructing the original text layout and structure.
The algorithm first identifies the text blocks on each row and arranges them in the correct order using the x and y coordinates. Subsequently, it calculates the distance between adjacent text block and check if the distance is within the predefined thresholds. Two thresholds were used to define the accepted horizontal difference, x delta, and vertical difference, y delta, with their respective formulas as follow:

<p align="center">
  <img src=https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/0dfc8ab9-8382-4097-be59-6d710ed06006" />
</p>

if both x delta and y delta are within the threshold defined, the algorithm merges the two text blocks into a single entity with the following data structure:

<p align="center">
  <img src=https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/de5abe1d-d980-406c-aa0b-9c1e5d7ac62d" />
</p>

Otherwise, if the text cannot be merged with any existing entity, a new entity will be created and added into the list of merged text entities maintained by the algorithm for the entire document.

# Classifier
The proposed system utilises spaCy’s Name Entity Recognition (NER) in Natural Language Processing (NLP) to classify the OCR output. NER is a subtask of NLP that involves identifying and categorising named entities in text such as person names, organisations, locations, dates, and monetary values, into predefined categories. The classifier accomplishes this by analysing the syntactic and semantic context of the text.

## NER Model Implementation
The implementation of spaCy’s NER model on Python involves installing the required dependencies, namely the spaCy package and its English language model. With these dependencies installed, the model can be loaded to initialise the NER pipeline for classification using spaCy’s nlp function, which takes in a string of texts.

# Autofill and Suggestion list System
A claim form web application is developed to demonstrate the autofill capability of the proposed system. This application serves as a practical demonstration of how the system populates form fields based on the extracted structured data. Additionally, a suggestion system has been integrated into the implementation to enhance the correction process and provide users with probable suggestion.

## Autofill Implementation
![image](https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/c64d52de-4dcd-4150-aff1-88b6e071b268)

The implementation of the autofill system begins with configuring the desired autofilled input element, which involves setting its ‘list’ attribute to the relevant named entities, separated by commas. The ‘list’ attribute establishes the connection between the extracted data and the corresponding input box.
Once the structured data is extracted from the attached invoice and received from the OCR application, a JavaScript function is employed to determine the classes of the named entities to be used for the autofill process. The first element within the classes is then used to populate the respective configured input boxes. Thus, ensures that the relevant information is automatically filled in the corresponding form fields.

## Suggestion List Implementation
![image](https://github.com/leongjinghao/OCR-Claim-Application/assets/73938217/91ef312d-ccb9-4940-865d-8717241c461d)

The implementation of the suggestion list feature is an extension of the autofill implementation. It leverages the same underlying mechanism to generate the datalists based on all the elements within the classes of the named entities. Each configured input box utilises its respective datalist to populate the dropdown box, which is used to provide suggestions extracted from the invoice attachment to the user.
