import numpy as np
import cv2 as cv
from math import *
import time

max_size = 345  # indicate the size of the output picture
method = 1  # (1,2,3) different method to make picture clearer.
reverse = 0  # (0,1) you can choose either reverse the color of the picture or not

# Hexadecimal digits
alphabet = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

# All the unicode representations of braille characters
Unicodes = [[u'\u2800',u'\u2801',u'\u2802',u'\u2803',u'\u2804',u'\u2805',u'\u2806',u'\u2807',u'\u2808',u'\u2809',u'\u280a',u'\u280b',u'\u280c',u'\u280d',u'\u280e',u'\u280f'],
[u'\u2810',u'\u2811',u'\u2812',u'\u2813',u'\u2814',u'\u2815',u'\u2816',u'\u2817',u'\u2818',u'\u2819',u'\u281a',u'\u281b',u'\u281c',u'\u281d',u'\u281e',u'\u281f'],
[u'\u2820',u'\u2821',u'\u2822',u'\u2823',u'\u2824',u'\u2825',u'\u2826',u'\u2827',u'\u2828',u'\u2829',u'\u282a',u'\u282b',u'\u282c',u'\u282d',u'\u282e',u'\u282f'],
[u'\u2830',u'\u2831',u'\u2832',u'\u2833',u'\u2834',u'\u2835',u'\u2836',u'\u2837',u'\u2838',u'\u2839',u'\u283a',u'\u283b',u'\u283c',u'\u283d',u'\u283e',u'\u283f'],
[u'\u2840',u'\u2841',u'\u2842',u'\u2843',u'\u2844',u'\u2845',u'\u2846',u'\u2847',u'\u2848',u'\u2849',u'\u284a',u'\u284b',u'\u284c',u'\u284d',u'\u284e',u'\u284f'],
[u'\u2850',u'\u2851',u'\u2852',u'\u2853',u'\u2854',u'\u2855',u'\u2856',u'\u2857',u'\u2858',u'\u2859',u'\u285a',u'\u285b',u'\u285c',u'\u285d',u'\u285e',u'\u285f'],
[u'\u2860',u'\u2861',u'\u2862',u'\u2863',u'\u2864',u'\u2865',u'\u2866',u'\u2867',u'\u2868',u'\u2869',u'\u286a',u'\u286b',u'\u286c',u'\u286d',u'\u286e',u'\u286f'],
[u'\u2870',u'\u2871',u'\u2872',u'\u2873',u'\u2874',u'\u2875',u'\u2876',u'\u2877',u'\u2878',u'\u2879',u'\u287a',u'\u287b',u'\u287c',u'\u287d',u'\u287e',u'\u287f'],
[u'\u2880',u'\u2881',u'\u2882',u'\u2883',u'\u2884',u'\u2885',u'\u2886',u'\u2887',u'\u2888',u'\u2889',u'\u288a',u'\u288b',u'\u288c',u'\u288d',u'\u288e',u'\u288f'],
[u'\u2890',u'\u2891',u'\u2892',u'\u2893',u'\u2894',u'\u2895',u'\u2896',u'\u2897',u'\u2898',u'\u2899',u'\u289a',u'\u289b',u'\u289c',u'\u289d',u'\u289e',u'\u289f'],
[u'\u28a0',u'\u28a1',u'\u28a2',u'\u28a3',u'\u28a4',u'\u28a5',u'\u28a6',u'\u28a7',u'\u28a8',u'\u28a9',u'\u28aa',u'\u28ab',u'\u28ac',u'\u28ad',u'\u28ae',u'\u28af'],
[u'\u28b0',u'\u28b1',u'\u28b2',u'\u28b3',u'\u28b4',u'\u28b5',u'\u28b6',u'\u28b7',u'\u28b8',u'\u28b9',u'\u28ba',u'\u28bb',u'\u28bc',u'\u28bd',u'\u28be',u'\u28bf'],
[u'\u28c0',u'\u28c1',u'\u28c2',u'\u28c3',u'\u28c4',u'\u28c5',u'\u28c6',u'\u28c7',u'\u28c8',u'\u28c9',u'\u28ca',u'\u28cb',u'\u28cc',u'\u28cd',u'\u28ce',u'\u28cf'],
[u'\u28d0',u'\u28d1',u'\u28d2',u'\u28d3',u'\u28d4',u'\u28d5',u'\u28d6',u'\u28d7',u'\u28d8',u'\u28d9',u'\u28da',u'\u28db',u'\u28dc',u'\u28dd',u'\u28de',u'\u28df'],
[u'\u28e0',u'\u28e1',u'\u28e2',u'\u28e3',u'\u28e4',u'\u28e5',u'\u28e6',u'\u28e7',u'\u28e8',u'\u28e9',u'\u28ea',u'\u28eb',u'\u28ec',u'\u28ed',u'\u28ee',u'\u28ef'],
[u'\u28f0',u'\u28f1',u'\u28f2',u'\u28f3',u'\u28f4',u'\u28f5',u'\u28f6',u'\u28f7',u'\u28f8',u'\u28f9',u'\u28fa',u'\u28fb',u'\u28fc',u'\u28fd',u'\u28fe',u'\u28ff']]

# Mapping braille character with its unicodes
dict = {}
for i in range(16):
    for j in range(16):
        dict.update({(alphabet[i]+alphabet[j]):Unicodes[i][j]})

# \u2800 is different from space, so we have to improve the alignment
dict.update({'00':Unicodes[0][1]})

# Return the edge of objects in an image
def edge_detect(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    edge_output = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY, 25, 10)
    return edge_output

# Given a four-digit binary number, this function returns the hexadecimal representation. e.g. '1100' -> 'c'
def getc(str):
    temp = hex(int(str,2))
    return temp[2]

# interpret the braille character
def getpix(oct):
    hex1=str(oct[3][1])+str(oct[3][0])+str(oct[2][1])+str(oct[1][1])
    hex2=str(oct[0][1])+str(oct[2][0])+str(oct[1][0])+str(oct[0][0])
    c1=getc(hex1)
    c2=getc(hex2)
    return dict[c1+c2]

def hist(image):
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    dst = cv.equalizeHist(gray)
    return dst

# the main function to process the image
def img_process(path):

    if method == 1:
        img = cv.imread(path, 0)
    elif method == 2:
        img = cv.imread(path)
        img = hist(img)
    else:
        img = cv.imread(path)
        img = edge_detect(img)

    # regulate the size of the image
    row = len(img)
    col = len(img[0])
    size_ = max(row, col)
    if(size_ > max_size):
        times = float(size_/max_size)
        row = int(row / times)
        col = int(col / times)
        img = cv.resize(img, (col, row))

    # every 4*2 pixels get mapped to a braille character
    # you can define a new threshold rather than the 'round' function below to make your symbol image clearer
    Row = int(floor(row/4))
    Col = int(floor(col/2))
    new_img = np.zeros(shape=(4*Row, 2*Col))
    for i in range(Row*4):
        for j in range(Col*2):
            if reverse == 0:
                new_img[i][j] = round(img[i][j]/255)  # not reverse
            else:
                new_img[i][j] = 1 - round(img[i][j]/255)  # reverse

    ## You can check the image here
    # cv.imshow("Precessed Image",np.array(new_img))
    # cv.waitKey()

    # interpret 4*2 pixels into braille characters using getpix()
    new_img = new_img.astype(np.int16)
    result_img = np.array([['cpp']*Col]*Row)
    for i in range(Row):
        for j in range(Col):
            temp_mat=new_img[i*4:i*4+4,j*2:j*2+2]
            result_img[i][j] = getpix(temp_mat)
    return result_img


if __name__ == "__main__":
    time_start = time.time()

    img_path=r"../images/3.jpg"

    # print the symbol image
    point_mat = img_process(img_path)
    for i in range(len(point_mat)):
        for j in range(len(point_mat[0])):
            print(point_mat[i][j], end='')
        print('')

    time_end = time.time()
    print('Time cost:', time_end - time_start, 's')


