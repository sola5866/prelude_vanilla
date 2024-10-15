import os
import glob
import cv2

basedirPath = r"./"
firstList = os.listdir(basedirPath)

for fileName in glob.iglob('*'):
    if '_heightmap.png' in fileName:
        img = cv2.imread(fileName)
        convertImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(fileName, convertImg, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
    elif '_mer.png' in fileName:
        img = cv2.imread(fileName)
        convertImg = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        cv2.imwrite(fileName, convertImg, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])