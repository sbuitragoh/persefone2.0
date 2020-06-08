import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from skimage.measure import regionprops
from matplotlib import patches as pch

def lineSet(pageCut):

    htTerms = cv.reduce(pageCut, 1, cv.REDUCE_AVG).reshape(-1)
    thresh = 30

    for el in range(len(htTerms)):
        if htTerms[el] < thresh:
            htTerms[el] = 0
        if htTerms[el] >= thresh:
            htTerms[el] = 1

    lineInterval = []
    for i in range(len(htTerms)-1):
        if (htTerms[i] == 0 and htTerms[i+1] == 1) or (htTerms[i] == 1 and htTerms[i+1] == 0):
            lineInterval.append(i)

    lineInterval = np.array(np.reshape(lineInterval, (-1, 2)))
    lineInterval = np.c_[lineInterval, lineInterval[:, 1] - lineInterval[:, 0]]
    lineInterval = lineInterval[lineInterval[:, 2] >= 40]
    lines, _ = np.shape(lineInterval)

    lineInterval[0][0] = 0
    return lineInterval, lines

def elementColoring(lb):
    label_hue = np.uint8(179 * lb / np.max(lb))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv.cvtColor(labeled_img, cv.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue == 0] = 0

    cv.imshow('labeled.png', labeled_img)
    cv.waitKey()

def lineCleaner(pageCut, lineInterval):
    pageCopy = pageCut.copy()

    for i in range(0, len(lineInterval) - 1):
        if i == 0:
            lineSection = pageCopy[0:lineInterval[i + 1][0], :]
        else:
            lineSection = pageCopy[lineInterval[i - 1][1]:lineInterval[i + 1][0]+20, :]

        lineCopy = lineSection.copy()
        output = cv.connectedComponentsWithStats(lineCopy)
        prop = regionprops(output[1])
        limitSet = int((lineInterval[i + 1][0] - lineInterval[i][1]) / 4)

        for x in range(0, len(prop)):
            py, px = prop[x].centroid

            if i == 0:
                limitLine = lineInterval[i][1] + limitSet
            else:
                limitLine = lineInterval[i][1] + limitSet - lineInterval[i - 1][1]

            if py >= limitLine:
                lineCopy[prop[x].bbox[0]:prop[x].bbox[2], prop[x].bbox[1]:prop[x].bbox[3]] = 0

        if i == 0:
            pageCopy[0:lineInterval[1, 0], :] = cv.bitwise_xor(pageCopy[0:lineInterval[1, 0], :], lineCopy)
        else:
            pageCopy[lineInterval[i - 1][1]:lineInterval[i + 1, 0]+20, :] = cv.bitwise_xor(
                pageCopy[lineInterval[i - 1][1]:lineInterval[i + 1, 0]+20, :], lineCopy)

        linePath = './lines/line_' + str(i + 1) + '.png'
        cv.imwrite(linePath, lineCopy)