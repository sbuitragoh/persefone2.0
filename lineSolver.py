import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from skimage.measure import regionprops
from matplotlib import patches as pch
import os

def lineSet(pageCut):

    htTerms = cv.reduce(pageCut, 1, cv.REDUCE_AVG).reshape(-1)
    thresh = 25
    lineInterval = []

    for el in range(len(htTerms)):
        htTerms[el] = 0 if htTerms[el] < thresh else 1
        #if htTerms[el] < thresh: htTerms[el] = 0
        #if htTerms[el] >= thresh: htTerms[el] = 1

    for i in range(len(htTerms)-1):
        if (htTerms[i] == 0 and htTerms[i+1] == 1) or (htTerms[i] == 1 and htTerms[i+1] == 0):
            lineInterval.append(i)

    if len(lineInterval) % 2 != 0:
        lineInterval.insert(0,0)

    lineInterval = np.array(np.reshape(lineInterval, (-1, 2)))
    lineInterval[0][0] = 0
    lineInterval[-1][1] = np.shape(pageCut)[0]
    lineInterval = np.c_[lineInterval, lineInterval[:, 1] - lineInterval[:, 0]]
    lineInterval = lineInterval[lineInterval[:, 2] >= 35]
    lineInterval[0][0] = 0

    if np.where(lineInterval[:-1,2]>200)[0].size != 0:
        for space in np.where(lineInterval[:-1,2]>200):
            a,b,_ = lineInterval[space][0]
            rangeInt = int((b-a)/2)

            lineInterval = np.insert(lineInterval, space+1, [a+rangeInt+7, b, b-(a+rangeInt+7)], axis=0)
            lineInterval = np.insert(lineInterval, space + 1, [a, a + rangeInt - 7, rangeInt - 7], axis=0)
            lineInterval = np.delete(lineInterval, space, axis=0)

    lines, _ = np.shape(lineInterval)

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

def lineCleaner(pageCut, lineInterval, numberPage):
    pageCopy = pageCut.copy()

    for i in range(0, len(lineInterval)):
        if i == 0:
            lineSection = pageCopy[lineInterval[0][0]:lineInterval[i+1][0], :]
        elif i == len(lineInterval)-1:
            lineSection = pageCopy[lineInterval[-2][1]:lineInterval[-1][1], :]
        else:
            lineSection = pageCopy[lineInterval[i - 1][1]:lineInterval[i + 1][0] + 15, :]
        #if i == 0:
        #    lineSection = pageCopy[0:lineInterval[i + 1][0], :]
        #else:
        #    lineSection = pageCopy[lineInterval[i - 1][1]:lineInterval[i + 1][0]+20, :]

        lineCopy = lineSection.copy()
        output = cv.connectedComponentsWithStats(lineCopy)
        prop = regionprops(output[1])
        if i < len(lineInterval)-1:
            limitSet = int((lineInterval[i + 1][0] - lineInterval[i][1]) / 4)
        else:
            limitSet = int((lineInterval[i][0]-lineInterval[i][1])/4)
        boundingBox = []

        for x in range(0, len(prop)):
            py, px = prop[x].centroid

            limitLine = lineInterval[i][1] + limitSet if not i else \
                lineInterval[i][1] + limitSet - lineInterval[i - 1][1]

            #if i == 0:
            #    limitLine = lineInterval[i][1] + limitSet
            #else:
            #    limitLine = lineInterval[i][1] + limitSet - lineInterval[i - 1][1]

            if py >= limitLine:
                currentSection = lineCopy[prop[x].bbox[0]:prop[x].bbox[2], prop[x].bbox[1]:prop[x].bbox[3]]
                convexHull = prop[x].convex_image
                X, Y = convexHull.shape
                for m in range(X):
                    for n in range(Y):
                        if convexHull[m][n] == 1:
                            currentSection[m][n] = 0
            else:
                boundingBox.append(prop[x].bbox)

        if i == 0:
            pageCopy[0:lineInterval[1, 0], :] = cv.bitwise_xor(pageCopy[0:lineInterval[1, 0], :], lineCopy)
        elif i == len(lineInterval)-1:
            pageCopy[lineInterval[i - 1, 1]:lineInterval[i, 1], :] = cv.bitwise_xor(
                pageCopy[lineInterval[i - 1, 1]:lineInterval[i, 1], :], lineCopy)
        else:
            pageCopy[lineInterval[i - 1][1]:lineInterval[i + 1, 0] + 15, :] = cv.bitwise_xor(
                pageCopy[lineInterval[i - 1][1]:lineInterval[i + 1, 0] + 15, :], lineCopy)

        #Setting words inside the line
        wordInLine(boundingBox, lineCopy, i, numberPage)

        #Write in folder, all lines in page
        linePath = './lines/line_' + str(i + 1) + '.png'
        cv.imwrite(linePath, lineCopy)

def wordInLine(boundingBox, currentLine,lineNumber, numberPage):
    def xPos(elem):
        return elem[1]

    boundingBox.sort(key = xPos) # boxes sorted through x1
    boundingBox = np.asarray(boundingBox)
    box,_ = np.shape(boundingBox)
    wordBox = []
    for b in range(box-1):
        if boundingBox[b+1][0] >= boundingBox[b][0] and boundingBox[b+1][0] <= boundingBox[b][2]:
            if boundingBox[b+1][1] >= boundingBox[b][1] and boundingBox[b+1][1] <= boundingBox[b][3]:
                boundingBox[b+1][0] = boundingBox[b][0]
                boundingBox[b+1][1] = boundingBox[b][1]
                boundingBox[b+1][2] = np.maximum(boundingBox[b+1][2], boundingBox[b][2])
                boundingBox[b+1][3] = np.maximum(boundingBox[b+1][3], boundingBox[b][3])
    #Clean values
    for word in range(box-1):
        if boundingBox[word+1][0] == boundingBox[word][0]:
            if boundingBox[word + 1][1] == boundingBox[word][1]:
                pass
        else:
            wordBox.append(boundingBox[word])
    wordBox.append(boundingBox[-1])

    words, coord = np.shape(wordBox)
    for savedWord in range(words):

        currentWord = wordBox[savedWord]
        word2Save = currentLine[currentWord[0]:currentWord[2], currentWord[1]:currentWord[3]]
        xW, yW = np.shape(word2Save)
        if xW > 15 and yW > 15:
            wordLinePath = './words/page_'+str(numberPage)+'_line_' + str(lineNumber + 1) + '_word_' + str(savedWord+1) + '.png'
            cv.imwrite(wordLinePath, word2Save)