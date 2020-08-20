import cv2 as cv
import numpy as np

def pageImport(pagePath):

    pageOriginal = cv.imread(pagePath,-1)[...,::-1]
    pageGrey = cv.imread(pagePath, 0)
    pageHSV = cv.cvtColor(pageOriginal, cv.COLOR_RGB2HSV)

    return pageOriginal, pageHSV, pageGrey

def pageProcessing(pageOriginal, pageHSV, pageGrey):

    blueLow = np.array([int(180 * 0), int(255 * 0), int(255 * 0)])
    blueHigh = np.array([int(180 * 1), int(255 * 1), int(255 * 0.65)])

    maskHSV = cv.inRange(pageHSV, blueLow, blueHigh)

    pageMasked = cv.bitwise_and(pageOriginal, pageOriginal, mask = maskHSV)

    maskedHSV2RGB = cv.cvtColor(pageMasked, cv.COLOR_HSV2RGB)
    grayMasked = cv.cvtColor(maskedHSV2RGB, cv.COLOR_RGB2GRAY)

    grayFiltered = cv.inRange(grayMasked, 40, 80)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))

    morph = cv.morphologyEx(grayFiltered, cv.MORPH_CLOSE, kernel, iterations = 1)

    blur = cv.GaussianBlur(pageGrey, (5, 5), 0)
    _, gth = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    gth = ~gth
    
    processed = cv.bitwise_or(morph, gth)

    return processed

def limitExtract(processed):

    X, Y = np.shape(processed)
    space = [0, 0]
    limit = [[0, 0], [0, 0]]

    space[0] = int(Y // 3)
    space[1] = int(X // 3)

    projectionProV = np.sum(processed, axis=0) / np.sum(processed)
    projectionProH = np.sum(processed, axis=1) / np.sum(processed)

    idxSectionV = np.where((projectionProV >= 7E-5) & (projectionProV <= 1E-4))[0]
    idxSectionH = np.where((projectionProH >= 7E-5) & (projectionProH <= 1E-4))[0]

    for i in range(len(idxSectionV) - 1):
        if idxSectionV[i + 1] - idxSectionV[i] > space[0]:
            limit[0] = [idxSectionV[i] - 20, idxSectionV[i + 1] + 20]

    for j in range(len(idxSectionH) - 1):

        startSet = idxSectionH[0] if idxSectionH[0] <= 300 else 0
        endSet = idxSectionH[-1] if idxSectionH[-1] >= X-300 else X
        #if idxSectionH[0] > 300:
        #    startSet = 0
        #else:
        #    startSet = idxSectionH[0]

        #if idxSectionH[-1] < X - 300:
        #    endSet = X
        #else:
        #    endSet = idxSectionH[-1]

        if not limit[1][0]:
            if idxSectionH[j] - startSet >= 200: limit[1][0] = idxSectionH[j] - 20

        if not limit[1][1]:
            if endSet - idxSectionH[-1-j] >= 200: limit[1][1] = idxSectionH[-1-j] + 20

        if limit[1][0] != 0 and limit[1][1] != 0:
            break

    textCapsule = processed[limit[1][0]:limit[1][1], limit[0][0]:limit[0][1]]

    return textCapsule, limit