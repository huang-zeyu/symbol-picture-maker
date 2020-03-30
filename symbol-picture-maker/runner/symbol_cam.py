from runner.symbol_image import *
import numpy as np
import cv2 as cv
from math import *
import os
import time

# Same function as it is in symbol_image
def img_process(img):


    row = len(img)
    col = len(img[0])
    size_ = max(row,col)
    if(size_>174):
        times=float(size_/174)
        row = int(row / times)
        col = int(col / times)
        img = cv.resize(img, (col, row))

    Row = floor(row/4) #row/5 or row/4
    Col = floor(col/2)
    new_img = np.zeros(shape=(4*Row,2*Col)) #5*row or 4*row
    for i in range(Row*4):    #5*row or 4*row
        for j in range(Col*2):
            new_img[i][j] = round(img[i][j]/255)      #round函数可以改为根据需要设定阈值

    new_img = new_img.astype(np.int16)
    result_img = np.array([['cpp']*Col]*Row)
    for i in range(Row):
        for j in range(Col):
            temp_mat=new_img[i*4:i*4+4,j*2:j*2+2]    #i*5:i*5+4 or i*4:i*4+4
            result_img[i][j] = getpix(temp_mat)
    return result_img

# Same function as it is in symbol_image
def edge_detect(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY, 25, 10)
    return binary

if __name__ == "__main__":
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    cap = cv.VideoCapture(0)

    # Keep reading imagesfrom the camera of your computer
    while True:
        ret, frame = cap.read()
        cv.imshow('frame', frame)
        frame = edge_detect(frame)

        point_mat = img_process(frame)
        for i in range(len(point_mat)):
            for j in range(len(point_mat[0])):
                print(point_mat[i][j], end='')
            print('')
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()