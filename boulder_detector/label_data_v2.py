import cv2 as cv
from os import walk
import pandas as pd
import numpy as np


def isolate_ROI(target):
    '''Isolate the regions of interest
    '''
    image = cv.imread("data/frames/{0}".format(target))
        
    # convert the image to hsv format (hue, saturation, value)
    image_hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # regions of interest in white, background in black
    _, thresh = cv.threshold(image_hsv[:,:,0], 0, 255, 
        cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    
    # bitwise and the image and the regions of interest
    ROI = cv.bitwise_and(image, image, mask=thresh)
    # cv.imwrite("../data/image_boulders/{0}".format(target), ROI)

    # convert the regions of interest into black and white
    grey = cv.cvtColor(ROI, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(grey,25,255, cv.THRESH_BINARY)[1]

    return image, thresh



def calculate_ROI(target, ROI, image):
    '''Add bounding boxes for each region of interest
    '''
    bounding_boxes = []
    contours = cv.findContours(ROI, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for cntr in contours:
        # calculate the bounding box based on the contours
        x,y,w,h = cv.boundingRect(cntr)
        cv.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 1)
        
        bounding_boxes.append([x, y, w, h])

    cv.imwrite("data/truths_v2/{0}".format(target), image)

    return bounding_boxes



def label_ROI():
    '''Label regions of interest
    '''
    _, _, filenames = next(walk("data/frames"))
    data = []

    for i, f in enumerate(filenames):
        # isolate the regions of interest
        image, ROI = isolate_ROI(f)

        # apply bounding boxes around contours
        boxes = calculate_ROI(f, ROI, image)

        # append bounding boxes in csv format
        for b in boxes:
            data.append([f, b])
        
        print("{0}/{1} {2} labelled".format(i, len(filenames)-1, f))
    df = pd.DataFrame(data, columns=['image_id', 'bbox'])
    
    # add bounding boxes to csv
    df.to_csv('data/bboxes.csv')
        
if __name__ == "__main__":
    label_ROI()