import cv2 as cv
import numpy as np
import pagePreprocessing as pagpre
import lineSolver as lisol
from scipy.stats import mode
from skimage.measure import regionprops
from matplotlib import pyplot as plt
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

    print('Debug stop')