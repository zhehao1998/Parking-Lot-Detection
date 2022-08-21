import cvzone
import cv2
import numpy as np
import pickle

# CCTV video
vid = cv2.VideoCapture("carPark.mp4")

# Box params
width, height = 104, 41

def checkParkingSpace(image):
    freeSpace = 0
    for pos in posList:
        x, y = pos
        imgCrop = image[y:y+height, x:x+width]
        # Count of non-zero pixels
        count = cv2.countNonZero(imgCrop)

        if count < 700:
            color = (0, 200, 0)
            thickness = 5
            freeSpace += 1
        else:
            color = (0, 0, 200)
            thickness = 2

        # Change color of bounding boxes
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x+5, y+height-5), scale=1, thickness=2,
                           offset=3, colorR=color)

    # Display of carpark status
    cvzone.putTextRect(img, f'Available Lots: {str(freeSpace)}/{len(posList)}', (100, 50), scale=2, thickness=1,
                       offset=6, colorR=(0, 0, 0))

with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)


while True:
    # reset video frame
    if vid.get(cv2.CAP_PROP_POS_FRAMES) == vid.get(cv2.CAP_PROP_FRAME_COUNT):
        vid.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = vid.read()

    # Convert to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Add noise to blur
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    # Convert to binary image
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    # Image dilation
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Check pixel values inside bounding box
    checkParkingSpace(imgDilate)

    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThreshold", imgThreshold)
    # cv2.imshow("ImageMedian", imgMedian)
    # cv2.imshow("ImageDilate", imgDilate)

    # Input lag
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("Exiting ...")
        break

cv2.destroyAllWindows()