import cv2 as cv
import numpy as np
import pagePreprocessing as pagpre
import lineSolver as lisol
from scipy.stats import mode
from skimage.measure import regionprops
from matplotlib import pyplot as plt
from matplotlib import patches as pch
import scipy as sc


if __name__ == "__main__":
    pagePath = './testImag/out_4.jpg'

    # PAGE ADQUISITION
    pageOriginal, pageHSV, pageGrey = pagpre.pageImport(pagePath)
    processed = pagpre.pageProcessing(pageOriginal, pageHSV, pageGrey)
    pageCut, limit = pagpre.limitExtract(processed)
    originalCut = pageOriginal[limit[1][0]:limit[1][1], limit[0][0]:limit[0][1]]
    print ('Image Pre-processed!')

    # LINE FINDING

    lineInterval, lines = lisol.lineSet(pageCut)
    boundingBox = lisol.lineCleaner(pageCut, lineInterval)

    # WORD BOXES
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
    #Graph
    linePath = './lines/line_1.png'
    line = cv.imread(linePath)
    fig, ax = plt.subplots(1)
    ax.imshow(line)

    m, n = np.shape(wordBox)
    for pos in range(m):
        x0 = wordBox[pos][1]
        y0 = wordBox[pos][0]
        dx = wordBox[pos][3] - wordBox[pos][1]
        dy = wordBox[pos][2] - wordBox[pos][0]
        rect = pch.Rectangle((x0, y0), dx, dy, facecolor='None', edgecolor='r', linewidth='1')
        ax.add_patch(rect)
    print('Debug stop')