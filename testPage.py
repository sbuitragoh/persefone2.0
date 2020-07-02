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
    lisol.lineCleaner(pageCut, lineInterval)

    # WORD BOXES

    #Graph
    # linePath = './lines/line_1.png'
    # line = cv.imread(linePath)
    # fig, ax = plt.subplots(1)
    # ax.imshow(line)
    #
    # m, n = np.shape(wordBox)
    # for pos in range(m):
    #     x0 = wordBox[pos][1]
    #     y0 = wordBox[pos][0]
    #     dx = wordBox[pos][3] - wordBox[pos][1]
    #     dy = wordBox[pos][2] - wordBox[pos][0]
    #     rect = pch.Rectangle((x0, y0), dx, dy, facecolor='None', edgecolor='r', linewidth='1')
    #     ax.add_patch(rect)
    print('Debug stop')