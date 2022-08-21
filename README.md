# Parking-Lot-Detection
A naive computer vision solution to detect empty parking space using normal thresholding (otsu). Adaptive thresholding can be used in place of otsu thresholding to make the algorithm more robust.

This solution is a proof of concept and shows that it possible to solve computer vision problems without using deep learning. Note that the method only works due to having ideal scenario of a top-down aerial view with little changes in lighting. A prerecorded video is used for the purpose of this project, but can be easily swapped to live video input.

# The idea
1. Carpark lots positions are first manually selected using parkingSpacePicker.py
2. At each frame, image preprocessing and thresholding is done when main.py is run
3. The thresholding values of each parking position is then calculated 
4. A higher thresholding values suggests that the lot is likely full and vice versa
