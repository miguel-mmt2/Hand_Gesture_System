"""
This code was developed by:
    - Miguel Meireles Teixeira, nº 2021217493
    - Damir Ferreira Baspayev Marques, nº 2021218858

Objective: Using th camara to detect colors.

This code was inspired by: https://github.com/computervisioneng/color-detection-opencv/blob/master/LICENSE.md

This code was  available on Github: https://github.com/miguel-mmt2/PL5_Team_1_Repository
"""

# Import all the requiered libraries:
import cv2
import numpy as np

from PIL import Image

Red = [0, 0, 255]
Green = [0, 255, 0]
Blue = [255, 0, 0]
Pink = [203, 192, 255]
Orange = [0, 165, 255]
Yellow = [0, 255, 255]
Purple = [128, 0, 128]
Cyan = [255, 255, 0]
Brown = [19, 69, 139]
Turquoise = [208, 224, 64]
Silver = [192, 192, 192]
Gold = [0, 215, 255]
Lime_Green = [50, 205, 50]
Navy_Blue = [128, 0, 0]
White = [255, 255, 255]
Black = [0, 0, 0]

cap = cv2.VideoCapture(0)

def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit

while True:
        ret, frame = cap.read()
        
        # Convert the image from RGB to HSV
        hsv_Image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get the limits of the yellow color
        lower_yellow, upper_yellow = get_limits(color=Blue)
        
        # Get a mask to all the pixels from one location (color)
        mask = cv2.inRange(hsv_Image, lower_yellow, upper_yellow)
        
        # Shows the mask
        # cv2.imshow('frame', mask)  
        
        # Converting to Pillow and draw a box arround the object
        mask2 = Image.fromarray(mask)
        box = mask2.getbbox()
        print(box)
        
        # Draw the rectangle
        if box is not None:
            x1, y1, x2, y2 = box
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
            
        # Show final result
        cv2.imshow('frame', frame)
            
        
        
        
        # If the key 'q' is pressed than the camara shut down
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
        