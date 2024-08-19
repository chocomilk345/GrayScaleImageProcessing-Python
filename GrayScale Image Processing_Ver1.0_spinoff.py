from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter.simpledialog import *
import os.path
import math
import sys
import matplotlib.pyplot as plt

### 함수부
#***********************
# 공통 함수부
#***********************
def malloc2D(h, w, initValue=0) :
    memory = [ [initValue for _ in range(w)] for _ in range(h)]
    return memory

def openImage() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    fullname = askopenfilename(parent=window, filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')))
    # 중요! 입력 이미지 크기를 결정
    fsize = os.path.getsize(fullname) # 파일 크기(Byte)
    inH = inW = int(math.sqrt(fsize))
    # 메모리 할당
    inImage = malloc2D(inH, inW)
    # 파일 --> 메모리
    rfp = open(fullname, 'rb')
    for i in range(inH) :
        for k in range(inW) :
            inImage[i][k] = ord(rfp.read(1))
    rfp.close()
    equalImage()

def saveImage() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    if (outImage == None or len(outImage)==0) : # 영상처리를 한적이 없다면...
        return
    wfp = asksaveasfile(parent=window, mode='wb', defaultextension='*.raw',
                        filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')))
    import struct
    for i in range(outH) :
        for k in range(outW) :
            wfp.write( struct.pack('B', outImage[i][k]))
    wfp.close()
    messagebox.showinfo('성공', wfp.name + ' 저장완료!')

def accumImage() : # 효과누적 : 현재의 outImage를 inImage로..
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    #  inW와 outW가 다르면 in을 다시 잡음.
    if (inW != outW) :
        inH = outH
        inW = outW
        inImage = malloc2D(inH, inW)

    for i in range(outH) :
        for k in range(outW) :
            inImage[i][k] = outImage[i][k]

 #   messagebox.showinfo('성공', wfp.name + ' 완료!')

def exit() : # 종료
    sys.exit()

def displayImage() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    ## 기존에 이미지를 오픈한적이 있으면, 캔버스 뜯어내기
    if(canvas != None) :
        canvas.destroy()
    ## 벽, 캔버스, 종이 설정
    window.geometry(str(outH)+'x'+str(outW)) # "512x512"
    canvas = Canvas(window, height=outH, width=outW, bg='yellow')  # 칠판
    paper = PhotoImage(height=outH, width=outW)  # 종이
    canvas.create_image((outH // 2, outW // 2), image=paper, state='normal')
    ## 메모리-->화면
    # for i in range(outH):
    #    for k in range(outW):
    #        r = g = b = outImage[i][k]
    #        paper.put('#%02x%02x%02x' % (r, g, b), (k, i))
    # 더블 버퍼링... 비슷한 기법 (모두다 메모리상에 출력형태로 생성한 후에, 한방에 출력)
    rgbString = "" # 전체에 대한 16진수 문자열
    for i in range(outH) :
        oneString = "" # 한줄에 대한 16진수 문자열
        for k in range(outW) :
            r = g = b = outImage[i][k]
            oneString += '#%02x%02x%02x ' % (r, g, b)
        rgbString += '{' + oneString + '} '
    paper.put(rgbString)
    canvas.pack()

    # plt.hist(outImage)
    # plt.show()

#***********************
# 영상처리 함수부
#***********************
def equalImage() : # 동일 이미지
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = inImage[i][k]
    ##########################
    displayImage()

# 화소점 처리
def addImage() : # 밝게 / 어둡게
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # 중요! 출력 영상 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 메모리 할당
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    value = askinteger('정수입력', '-255~255 입력', maxvalue=255, minvalue=-255)
    for i in range(inH) :
        for k in range(inW) :
            px = inImage[i][k] + value
            if(px > 255):
                px = 255
            if(px < 0) :
                px = 0
            outImage[i][k] = px
    ##########################
    displayImage()
def mulImage() : # 화소 값 상수 곱셈
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    val = askfloat('실수입력', '0.1에서 3사이의 실수값', maxvalue=3, minvalue=0.1)

    ## 입력배열 --> 출력배열
    for i in range(inH) :
        for k in range(inW) :
            px = int(inImage[i][k] * val)
            if (px > 255) :
                outImage[i][k] = 255
            elif(px < 0) :
                outImage[i][k] = 0
            else :
                outImage[i][k] = px
    displayImage()

def divImage() : # 화소 값 상수 나눗셈
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
#    val = float(input("0.1에서 10사이의 실수값-->"))
    val = askfloat('실수입력', '0.1~10 입력', maxvalue=10, minvalue=0.1)
    print("val = ", val)
    ## 입력배열 --> 출력배열
    for i in range(outH) :
        for k in range(outW) :
            px = int(inImage[i][k] / val)
            if (px > 255) :
                outImage[i][k] = 255
            elif (px < 0) :
                outImage[i][k] = 0
            else :
                outImage[i][k] = px
    displayImage()

def andImage() : # AND Operation
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    val = askinteger('정수입력', '0~255 입력', maxvalue=255, minvalue=0)
    print("val = ", val)
    ## 입력배열 --> 출력배열
    for i in range(outH) :
        for k in range(outW) :
            px = inImage[i][k] & val
            if (px > 255) :
                outImage[i][k] = 255
            elif (px < 0) :
                outImage[i][k] = 0
            else :
                outImage[i][k] = px
    displayImage()
def orImage() : # OR Operation
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    val = askinteger('정수입력', '0~255 입력', maxvalue=255, minvalue=0)
    print("val = ", val)
    ## 입력배열 --> 출력배열
    for i in range(outH) :
        for k in range(outW) :
            px = inImage[i][k] | val
            if (px > 255) :
                outImage[i][k] = 255
            elif (px < 0) :
                outImage[i][k] = 0
            else :
                outImage[i][k] = px
    displayImage()

def xorImage() : # XOR Operation
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    val = askinteger('정수입력', '0~255 입력', maxvalue=255, minvalue=0)
    print("val = ", val)
    ## 입력배열 --> 출력배열
    for i in range(outH) :
        for k in range(outW) :
            px = inImage[i][k] ^ val
            if (px > 255) :
                outImage[i][k] = 255
            elif (px < 0) :
                outImage[i][k] = 0
            else :
                outImage[i][k] = px
    displayImage()

def reverseImage() : # 반전 알고리즘 0->255, 1->254 ..... 255->0
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    ## 입력배열 --> 출력배열
    for i in range(outH) :
        for k in range(outW) :
            outImage[i][k] = 255 - inImage[i][k]
    displayImage()

def bwImage() : # 흑백 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    ## 입력배열 --> 출력배열
    for i in range(inH) :
        for k in range(inW) :
            if (inImage[i][k] > 127) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = 0
    displayImage()

def bwAvgImage() : # 흑백(평균값)
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    sum, avg = [0] * 2
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH):
        for k in range(inW):
            sum += inImage[i][k]
    avg = sum / (outW * outH)

    for i in range(outH):
        for k in range(outW):
            if (inImage[i][k] < avg):
                outImage[i][k] = 0
            else:
                outImage[i][k] = 255
    print("흑백(평균값) ", avg)
    displayImage()

def bwMedImage() : # 흑백(중앙값)
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    array = []
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH):
        for k in range(inW):
            array.append(inImage[i][k])
    array.sort()
    median = array[int(inH * inW / 2)]
    print("흑백(중앙값) = ", median)
    for i in range(outH):
        for k in range(outW):
            if (inImage[i][k] < median):
                outImage[i][k] = 0
            else:
                outImage[i][k] = 255
    displayImage()

def gammaImage() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW#
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    val = askfloat('실수입력', '감마값(0.2~1.8)', maxvalue=1.8, minvalue=0.2)
 #   print("감마 = ", val)

    ## 진짜 영상처리 알고리즘 ##
    for i in range(outH):
        for k in range(outW):
            px = inImage[i][k]
            outImage[i][k] = int(255.0 * (px / 255.0) ** (val))
    displayImage()

def paraImage() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW#
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    ## 밝은 곳 입체형 (CAP)
    for i in range(outH):
        for k in range(outW):
            px = inImage[i][k]
            val = 255.0 - 255.0 * pow((px / 128.0 - 1.0), 2)
            if (val > 255.0) :
                val = 255.0
            elif (val < 0.0) :
                val = 0.0
            outImage[i][k] = int(val)
    displayImage()

def paraImage2() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW#
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    ## 어두운 곳 입체형 (CUP)
    for i in range(outH):
        for k in range(outW):
            px = inImage[i][k]
            val = 255.0 * pow((px / 128.0 - 1.0), 2)
            if (val > 255.0) :
                val = 255.0
            elif (val < 0.0) :
                val = 0.0
            outImage[i][k] = int(val)
    displayImage()

def postImage() : # 포스터라이징
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW#
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    val = askinteger('단계입력', '1~10 입력', maxvalue=10, minvalue=1)
    interval = int(255/val)
    ## 진짜 영상처리 알고리즘 ##
    for i in range(inH):
        for k in range(inW):
            if (inImage[i][k] < interval) : # 값이 제일 낮은 영역 0으로 할당
                outImage[i][k] = 0
            if(inImage[i][k] < interval*(val-1)) : # 값이 제일 큰 영역 255로 할당
                outImage[i][k] = 255

    for i in range(val-1):  # 영역 입력값에 비례하여 할당
        for j in range(inH):
            for k in range(inW):
                if (inImage[j][k] > (interval * i) and inImage[j][k] < interval * (i + 1)):
                    outImage[j][k] = interval * (i+1)
    displayImage()

def stressImage() : #  Stress Operation
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    start = askinteger('정수', '시작값 0~255 입력', maxvalue=255, minvalue=0)
    end = askinteger('정수', '종료값 0~255 입력', maxvalue=255, minvalue=0)
    if(start > end) :
        temp = start
        start = end
        end = temp
 #   if(start != end and start >= 0 and end <= 255) :
 #       return

    ## 입력배열 --> 출력배열
    for i in range(inH) :
        for k in range(inW) :
            px = inImage[i][k]
            if (px >= start and px <= end) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = px
    displayImage()

def move() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    moveX = askinteger('정수', 'X좌표 0~100 입력', maxvalue=100, minvalue=0) # 추후 수정 요망
    moveY = askinteger('정수', 'Y좌표 0~100 입력', maxvalue=100, minvalue=0)

    ## 입력배열 --> 출력배열
    for i in range(inH) :
        for k in range(inW) :
            x = k - moveX
            y = i - moveY
            if (x >= 0 and x < inW and y>=0 and y<inH) :
                outImage[i][k] = inImage[y][x]
            else :
                outImage[i][k] = 0 # 배경색 검정
    displayImage()

def mirrorHor() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 입력배열 --> 출력배열
    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = inImage[i][outW - 1 - k]
    displayImage()

def mirrorVer() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 입력배열 --> 출력배열
    for i in range(inH) :
        for k in range(inW) :
            outImage[i][k] = inImage[inH - 1 - i][k]
    displayImage()

def zoomIn() : # 확대 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    scale = askinteger('정수입력', '1~5 입력', maxvalue=5, minvalue=1)
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH * scale
    outW = inW * scale
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 입력배열 --> 출력배열
    for i in range(inH) :
        for k in range(inW) :
            outImage[i*scale][k*scale] = inImage[i][k]
            outImage[i*scale+1][k*scale+1] = inImage[i][k]
    displayImage()

def zoomIn2() : # 확대 백워딩
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    scale = askinteger('정수입력', '1~5 입력', maxvalue=5, minvalue=1)
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH * scale
    outW = inW * scale
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 입력배열 --> 출력배열
    for i in range(outH) :
        for k in range(outW) :
            outImage[i][k] = inImage[int(i/scale)][int(k/scale)]
    displayImage()

def zoomIn3() : # 확대 (양선형 보간)
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    ZoomRate = askfloat('실수입력', '0.1에서 3사이의 실수값', maxvalue=3, minvalue=0.1)

    point, i_H, i_W = [0] * 3
    r_H, r_W, s_H, s_W, C1, C2, C3, C4 = [0.0] * 8

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = int(inH * ZoomRate)
    outW = int(inW * ZoomRate)
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    tempImage = malloc2D(inH, inW, 0.0)

    for i in range(inH) :
        for k in range(inW) :
            tempImage[i][k] = float(inImage[i][k])

    ## 입력배열 --> 출력배열
    for i in range(outH) :
        for k in range(outW) :
            r_H = i / ZoomRate
            r_W = k / ZoomRate

            i_H = int(math.floor(r_H))
            i_W = int(math.floor(r_W))

            s_H = r_H - i_H
            s_W = r_W - i_W

            if (i_H < 0 or i_H >= (inH - 1) or i_W < 0 or i_W >= (inW - 1)) :
                outImage[i][k] = 255
            else : # 소수점 값 보간하기
                C1 = float(tempImage[i_H][i_W])
                C2 = float(tempImage[i_H][i_W + 1])
                C3 = float(tempImage[i_H + 1][i_W + 1])
                C4 = float(tempImage[i_H + 1][i_W])

                newValue = int(C1 * (1 - s_H) * (1 - s_W) + C2 * s_W * (1 - s_H) + C3 * s_W * s_H + C4 * (1 - s_W) * s_H)
                outImage[i][k] = newValue
    displayImage()

def zoomOut() : # 축소 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    scale = askinteger('정수입력', '1~5 입력', maxvalue=5, minvalue=1)
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = int(inH / scale)
    outW = int(inW / scale)
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 입력배열 --> 출력배열
    for i in range(inH) :
        for k in range(inW) :
            outImage[int(i/scale)][int(k/scale)] = inImage[i][k]
    displayImage()

def zoomOutAvg() : # 축소 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    scale = askinteger('정수입력', '1~5 입력', maxvalue=5, minvalue=1)
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = int(inH / scale)
    outW = int(inW / scale)
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 입력배열 --> 출력배열, 3축소 오류, 1.5배 축소 고민해서 해보자
    for i in range(0, inH, scale) :
        for k in range(0, inW, scale) :
            sum, avg = [0] * 2
            for x in range(scale):
                for y in range(scale):
                    sum += inImage[i+x][k+y]
            avg = int(sum/(scale*scale))
            outImage[int(i/scale)][int(k/scale)] = avg
    displayImage()

# def zoomOutMed() : # 축소 알고리즘
#     global window, canvas, paper, fullname
#     global inImage, outImage, inH, inW, outH, outW
#
#     scale = askinteger('정수입력', '1~5 입력', maxvalue=5, minvalue=1)
#     # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
#     outH = int(inH / scale)
#     outW = int(inW / scale)
#     # 출력 이미지 메모리 확보
#     outImage = malloc2D(outH, outW)
#
#     array = [0]*scale*scale
#     ## 진짜 영상처리 알고리즘 ##
#
#     for i in range(0, inH, scale) :
#         for k in range(0, inW, scale) :
#
#             number = 0
#             for x in range(scale):
#                 for y in range(scale):
#                     array[number] = inImage[i+x][k+y]
#                     number += 1
#             array.sort()
#             med = array[int(scale*scale/2)]
#             outImage[int(i/scale)][int(k/scale)] = med
#     displayImage()

# def zoomOutMed() : # 축소 알고리즘
#     global window, canvas, paper, fullname
#     global inImage, outImage, inH, inW, outH, outW
#
#     scale = askinteger('정수입력', '1~5 입력', maxvalue=5, minvalue=1)
#     # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
#     outH = int(inH / scale)
#     outW = int(inW / scale)
#     # 출력 이미지 메모리 확보
#     outImage = malloc2D(outH, outW)
#
#     ## 진짜 영상처리 알고리즘 ##
#     for i in range(0, inH, scale) :
#         for k in range(0, inW, scale) :
#             array = [0] * scale * scale
#             number = 0
#             for x in range(i, i+scale):
#                 for y in range(k, k+scale):
#                     array[number] = inImage[x][y]
#                     number += 1
#             array.sort()
#             med = array[int(scale*scale/2)]
#             if(med > 255) :
#                 outImage[int(i / scale)][int(k / scale)] = 255
#             elif(med < 0) :
#                 outImage[int(i / scale)][int(k / scale)] = 0
#             else :
#                 outImage[int(i/scale)][int(k/scale)] = med
#     displayImage()
def zoomOutMed() : # 축소 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    scale = askinteger('정수입력', '1~5 입력', maxvalue=5, minvalue=1)
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = int(inH / scale)
    outW = int(inW / scale)
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    for i in range(0, inH, scale) :
        for k in range(0, inW, scale) :
            array = [0] * scale * scale
            number = 0
            for x in range(i, i+scale):
                for y in range(k, k+scale):
                    array[number] = inImage[x][y]
                    number += 1
            array.sort()
            med = array[int(scale*scale/2)]
            if(med > 255) :
                outImage[int(i / scale)][int(k / scale)] = 255
            elif(med < 0) :
                outImage[int(i / scale)][int(k / scale)] = 0
            else :
                outImage[int(i/scale)][int(k/scale)] = med
    displayImage()
def rotate() : # 회전 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    degree = askinteger('정수입력', '각도입력 0~90 입력', maxvalue=90, minvalue=0)
    radian = degree * math.pi / 180.0
    ## xd = cos * xs - sin * ys
    ## yd = sin * xs + cos * ys

    ## 진짜 영상처리 알고리즘 ##
    for i in range(outH) :
        for k in range(outW) :
            xs = i
            ys = k
            xd = (int)(math.cos(radian) * xs - math.sin(radian) * ys)
            yd = (int)(math.sin(radian) * xs + math.cos(radian) * ys)

            if ((0 <= xd and xd < outH) and (0 <= yd and yd < outW)) :
                outImage[xd][yd] = inImage[xs][ys]
    displayImage()

def rotate2() : # 회전 알고리즘 + 중앙/백워딩
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    degree = askinteger('정수입력', '각도입력 0~90 입력', maxvalue=90, minvalue=0)
    radian = degree * math.pi / 180.0
    ## xd = cos * xs - sin * ys
    ## yd = sin * xs + cos * ys

    ## 진짜 영상처리 알고리즘 ##
    cx = int(inH / 2)
    cy = int(inW / 2)

    for i in range(outH) : # TODO
        for k in range(outW) :

            xd = i
            yd = k
            xs = int(math.cos(radian) * (xd - cx) + math.sin(radian) * (yd - cy))
            ys = int(-math.sin(radian) * (xd - cx) + math.cos(radian) * (yd - cy))
            xs += cx
            ys += cy

            if ((0 <= xs and xs < outH) and (0 <= ys and ys < outW)) :
                outImage[xd][yd] = inImage[xs][ys]
            else :
                outImage[xd][yd] = 0
    displayImage()

def rotate3() : # 회전 알고리즘 + 중앙/백워딩 + 출력크기 재조정
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    degree = askinteger('정수입력', '각도입력 0~90 입력', maxvalue=90, minvalue=0)
    radian = degree * math.pi / 180.0
    radian2 = (90 - degree) * math.pi / 180.0
    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = int(inH * math.cos(radian2) + inW * math.cos(radian))
    outW = int(inH * math.cos(radian) + inW * math.cos(radian2))
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## xd = cos * xs - sin * ys
    ## yd = sin * xs + cos * ys

    ## 진짜 영상처리 알고리즘 ##
    cx = int(inH / 2)
    cy = int(inW / 2)
    centerX = int(outH / 2)
    centerY = int(outW / 2)

    # 입력 배열 --> 출력 배열
    for i in range(outH) :
        for k in range(outW) :

            xd = i
            yd = k
            xs = int(math.cos(radian) * (xd - centerX) + math.sin(radian) * (yd - centerY))
            ys = int(-math.sin(radian) * (xd - centerX) + math.cos(radian) * (yd - centerY))
            xs += cx
            ys += cy

            if ((0 <= xs and xs < inH) and (0 <= ys and ys < inW)) :
                outImage[xd][yd] = inImage[xs][ys]
            else :
                outImage[xd][yd] = 0
    displayImage()

def morph() : # 모핑
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    fullnameMor = askopenfilename(parent=window, filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')))
    morRate = askinteger('정수입력', '모핑비율 1~9 입력', maxvalue=9, minvalue=1)

    # 중요! 입력 이미지 크기를 결정
    fsize = os.path.getsize(fullnameMor) # 파일 크기(Byte)
    morH, morW, inX, inY, morX, morY = [0] * 6

    morH = morW = int(math.sqrt(fsize))
    # 메모리 할당
    morImage = malloc2D(morH, morW)
    # 파일 --> 메모리
    rfp = open(fullnameMor, 'rb')
    for i in range(morH) :
        for k in range(morW) :
            morImage[i][k] = ord(rfp.read(1))
    rfp.close()

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    if (morH <= inH and morW <= inW) :
        outH = inH
        outW = inW
        morX = int((inH - morH) / 2.)
        morY = int((inW - morW) / 2.)
    else : # inImage가 작으면
        outH = morH
        outW = morW
        inX = int((morH - inH) / 2.)
        inY = int((morW - inW) / 2.)

    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    # 영상처리 -> 어두워지는 문제를 해결할것
    if (morH <= inH) : # inImage가 더 크거나 같음
        for i in range(outH) :
            for k in range(outW) :
                if (i >= morX and k >= morY and i < morX + morH and k < morY + morW) :
                    outImage[i][k] = int((inImage[i][k] * (10. - morRate) / 10.))
                else :
                    outImage[i][k] = inImage[i][k]
        for i in range(morH) :
            for k in range(morW) :
                outImage[i + morX][k + morY] += int((morImage[i][k] * (morRate) / 10.))
    else : # inImage가 작음
        for i in range(outH):
            for k in range(outW):
                if (i >= inX and k >= inY and i < inX + inH and k < inY + inW) :
                    outImage[i][k] = int((morImage[i][k] * (morRate) / 10.))
                else :
                    outImage[i][k] = morImage[i][k]
        for i in range(inH):
            for k in range(inW):
                outImage[i + inX][k + inY] += int((inImage[i][k] * (10-morRate) / 10.))

    displayImage()

def histoStretch() : # 히스토그램 스트래칭 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    high = inImage[0][0]
    low = inImage[0][0]

    for i in range(inH):
        for k in range(inW):
            if (inImage[i][k] > high) :
                high = inImage[i][k]
            if (inImage[i][k] < low) :
                low = inImage[i][k]
    old, new = [0] * 2
    for i in range(inH):
        for k in range(inW):
            old = inImage[i][k]
            new = int(float(old - low) / float(high - low) * 255.0)
            if (new > 255) :
                new = 255
            elif (new < 0) :
                new = 0
            outImage[i][k] = new
    displayImage()

def endIn() : # 엔드인 탐색 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    # high = (old-low) / (high-low) * 255.0
    high = inImage[0][0]
    low = inImage[0][0]

    for i in range(inH):
        for k in range(inW):
            if (inImage[i][k] > high) :
                high = inImage[i][k]
            if (inImage[i][k] < low) :
                low = inImage[i][k]
    high -= 50
    low += 50
    for i in range(inH):
        for k in range(inW):
            old = inImage[i][k]
            new = int(float(old - low) / float(high - low) * 255.0)
            if (new > 255) :
                new = 255
            elif (new < 0) :
                new = 0
            outImage[i][k] = new
    displayImage()

def histoEqual() : # 히스토그램 평활화 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 진짜 영상처리 알고리즘 ##
    # 1단계 : 빈도수 세기 (=히스토그램)
    histo = [0 for _ in range(256)]
    for i in range(inH):
        for k in range(inW):
            histo[inImage[i][k]] += 1

    # 2단계 : 누적히스토그램 생성
    sumHisto = [0 for _ in range(256)]
    sumHisto[0] = histo[0]
    for i in range (256) :
        sumHisto[i] = sumHisto[i - 1] + histo[i]

    # 3단계 : 정규화된 히스토그램 생성 normalHisto = sumHisto * (1.0/(inH*inW)) * 255.0
    normalHisto = [1.0 for _ in range(256)]
    for i in range(256):
        normalHisto[i] = sumHisto[i] * (1.0 / (inH * inW)) * 255.0

    # 4단계 : inImage를 정규화된 값으로 치환
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = int(normalHisto[inImage[i][k]])

    displayImage()

def emboss() : # 화소영역 처리: 엠보싱 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[-1.0, 0.0, 0.0], # 엠보싱 마스크
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+2, inW+2, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+1][k+1] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(3x3)와 한점을 중심으로 한 3x3을 곱하기
            S = 0.0 # 마스크 9개와 입력값 9개를 각각 곱해서 합한 값.
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S

    # 후처리 (마스크 값의 합계에 따라서...)
    for i in range(outH) :
        for k in range(outW) :
            tmpOutImage[i][k] += 127.0

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def blur() : # 화소영역 처리: 블러링 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[1./9, 1./9, 1./9], # 블러링 마스크
            [1./9, 1./9, 1./9],
            [1./9, 1./9, 1./9]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+2, inW+2, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+1][k+1] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(3x3)와 한점을 중심으로 한 3x3을 곱하기
            S = 0.0 # 마스크 9개와 입력값 9개를 각각 곱해서 합한 값.
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S;

    # 후처리 (마스크 값의 합계에 따라서...)
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImage[i][k] += 127.0

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def blur2() : # 화소영역 처리: 블러링 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81],   # 블러링 마스크
            [1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81],
            [1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81],
            [1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81],
            [1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81],
            [1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81],
            [1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81],
            [1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81],
            [1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81, 1./81]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+8, inW+8, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH+8):
        for k in range(inW+8):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+4][k+4] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(9x9)와 한점을 중심으로 한 9x9 곱하기
            S = 0.0 # 마스크 81개와 입력값 81개를 각각 곱해서 합한 값.
            for m in range(9):
                for n in range(9):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S

    # 후처리 (마스크 값의 합계에 따라서...)
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImage[i][k] += 127.0

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def sharp() : # 화소영역 처리: 샤프닝 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[-1., -1., -1.], # 샤프닝 마스크
            [-1., 9., -1.],
            [-1., -1., -1.]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+2, inW+2, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+1][k+1] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(3x3)와 한점을 중심으로 한 3x3 곱하기
            S = 0.0 # 마스크 9개와 입력값 9개를 각각 곱해서 합한 값.
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S

    # 후처리 (마스크 값의 합계에 따라서...)
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImage[i][k] += 127.0

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def sharpHpf() : # 화소영역 처리: 고주파 샤프닝 알고리즘
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[-1./9., -1./9., -1./9.], # 샤프닝 마스크
            [-1./9., 8./9., -1./9.],
            [-1./9., -1./9., -1./9.]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+2, inW+2, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+1][k+1] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(3x3)와 한점을 중심으로 한 3x3 곱하기
            S = 0.0 # 마스크 9개와 입력값 9개를 각각 곱해서 합한 값.
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S

    # 후처리 (마스크 값의 합계에 따라서...)
    for i in range(outH) :
        for k in range(outW) :
            tmpOutImage[i][k] += inImage[i][k]

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def edge1() : # 경계선검출: 수직 에지 검출 마스크
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[0.0, 0.0, 0.0], # 수직 에지 검출 마스크
           [-1.0, 1.0, 0.0],
           [0.0,  0.0, 0.0]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+2, inW+2, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+1][k+1] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(3x3)와 한점을 중심으로 한 3x3 곱하기
            S = 0.0 # 마스크 9개와 입력값 9개를 각각 곱해서 합한 값.
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S

    # 후처리 (마스크 값의 합계에 따라서...)
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImage[i][k] += 127.0

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def edgeHomo() : # 경계선검출: 유사 연산자 에지 검출
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+2, inW+2, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+1][k+1] = float(inImage[i][k])

    for i in range(inH) :
        for k in range(inW) :
            max = 0.0 # 블록이 이동할 때마다 최대값 초기화
            for m in range(3):
                for n in range(3):
                    if (math.fabs(tmpInImage[i + 1][k + 1] - tmpInImage[i + n][k + m]) >= max) :
                        max = math.fabs(tmpInImage[i + 1][k + 1] - tmpInImage[i + n][k + m])
            tmpOutImage[i][k] = max

    # 입력 배열 --> 출력 배열
    for i in range(inH) :
        for k in range(inW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def edgeSub() : # 경계선검출: 차연산자 에지 검출
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+2, inW+2, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)
    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+1][k+1] = float(inImage[i][k])

    for i in range(inH) :
        for k in range(inW) :
            max = 0.0 # 블록이 이동할 때마다 최대값 초기화
            temp = math.fabs(tmpInImage[i][k] - tmpInImage[i + 2][k + 2])
            if (temp >= max) :
                max = temp
            temp = math.fabs(tmpInImage[i][k + 1] - tmpInImage[i + 2][k + 1])
            if (temp >= max) :
                max = temp
            temp = math.fabs(tmpInImage[i][k + 2] - tmpInImage[i + 2][k])
            if (temp >= max) :
                max = temp
            temp = math.fabs(tmpInImage[i + 1][k] - tmpInImage[i + 1][k + 1])
            if (temp >= max) :
                max = temp
            tmpOutImage[i][k] = max

    # 입력 배열 --> 출력 배열
    for i in range(inH) :
        for k in range(inW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def robert() : # 경계선검출: 1차 미분 회선
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[-1.0, 0.0, 0.0], # 로버츠 행 검출 마스크
            [0.0,  1.0, 0.0],
            [0.0,  0.0, 0.0]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+2, inW+2, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+1][k+1] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(3x3)와 한점을 중심으로 한 3x3 곱하기             # 마스크 9개와 입력값 9개를 각각 곱해서 합한 값.
            S = 0.0
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S

    # 후처리 (마스크 값의 합계에 따라서...)
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImage[i][k] += 127.0

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def sobel() : # 경계선검출: 1차 미분 회선
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[-1.0, -2.0,-1.0], # 소벨 행 검출 마스크
             [0.0,  0.0, 0.0],
             [1.0,  2.0, 1.0]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+2, inW+2, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+1][k+1] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(3x3)와 한점을 중심으로 한 3x3 곱하기
            S = 0.0 # 마스크 9개와 입력값 9개를 각각 곱해서 합한 값.
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S

    # 후처리 (마스크 값의 합계에 따라서...)
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImage[i][k] += 127.0

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def lapla() : # 경계선검출: 라플라시안
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[-1.0, -1.0, -1.0], # 라플라시안 마스크
            [-1.0,  8.0, -1.0],
            [-1.0, -1.0, -1.0]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+2, inW+2, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+1][k+1] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(3x3)와 한점을 중심으로 한 3x3 곱하기
            S = 0.0 # 마스크 9개와 입력값 9개를 각각 곱해서 합한 값.
            for m in range(3):
                for n in range(3):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S

    # 후처리 (마스크 값의 합계에 따라서...)
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImage[i][k] += 127.0

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def loG() : # 경계선검출: LoG(가우시안)
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[0.0,  0.0, -1.0, 0.0, 0.0],  # LoG 마스크
            [0.0, -1.0, -2.0,-1.0, 0.0],
            [-1.0,-2.0, 16.0,-2.0,-1.0],
            [0.0, -1.0, -2.0,-1.0, 0.0],
            [0.0,  0.0, -1.0, 0.0, 0.0]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+4, inW+4, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH+4):
        for k in range(inW+4):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+2][k+2] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(5x5)와 한점을 중심으로 한 5x5 곱하기
            S = 0.0 # 마스크 25개와 입력값 25개를 각각 곱해서 합한 값.
            for m in range(5):
                for n in range(5):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S

    # 후처리 (마스크 값의 합계에 따라서...)
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImage[i][k] += 127.0

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()

def doG() : # 경계선검출: DoG(가우시안)
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW

    # (중요!) 출력 이미지 크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ##***********************
    ## 화소 영역 처리
    ##***********************
    mask = [[0.0,  0.0, -1.0, -1.0, -1.0,  0.0,  0.0],  # DoG 마스크
            [0.0, -2.0, -3.0, -3.0, -3.0, -2.0,  0.0],
            [-1.0,-3.0,  5.0,  5.0,  5.0, -3.0, -1.0],
            [-1.0,-3.0,  5.0, 16.0,  5.0, -3.0, -1.0],
            [-1.0,-3.0,  5.0,  5.0,  5.0, -3.0, -1.0],
            [0.0, -2.0, -3.0, -3.0, -3.0, -2.0,  0.0],
            [0.0,  0.0, -1.0, -1.0, -1.0,  0.0,  0.0]]

    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH+6, inW+6, 0.0)
    tmpOutImage = malloc2D(outH, outW, 0.0)

    # 임시 입력 메모리를 초기화(127) : 필요시 평균값
    for i in range(inH+6):
        for k in range(inW+6):
            tmpInImage[i][k] = 127

    # 입력 이미지 --> 임시 입력 이미지
    for i in range(inH) :
        for k in range(inW) :
            tmpInImage[i+3][k+3] = inImage[i][k]

    # ** 회선 연산 **
    for i in range(inH) :
        for k in range(inW) :
            # 마스크(7x7)와 한점을 중심으로 한 7x7 곱하기
            S = 0.0 # 마스크 81개와 입력값 81개를 각각 곱해서 합한 값.
            for m in range(7):
                for n in range(7):
                    S += tmpInImage[i + m][k + n] * mask[m][n]
            tmpOutImage[i][k] = S

    # 후처리 (마스크 값의 합계에 따라서...)
    # for i in range(outH) :
    #     for k in range(outW) :
    #         tmpOutImage[i][k] += 127.0

    # 임시 출력 영상 --> 출력 영상
    for i in range(outH) :
        for k in range(outW) :
            if (tmpOutImage[i][k] < 0.0) :
                outImage[i][k] = 0
            elif (tmpOutImage[i][k] > 255.0) :
                outImage[i][k] = 255
            else :
                outImage[i][k] = int(tmpOutImage[i][k])

    displayImage()


### 전역 변수부
window, canvas, paper = None, None, None
inImage, outImage = [], []
inH, inW, outH, outW = [0]*4
fullname = ''

### 메인 코드부
window = Tk() # 벽
window.geometry("500x500")
window.resizable(width=False, height=False)
window.title("영상처리(RC 1)")

# 메뉴 만들기
mainMenu = Menu(window) # 메뉴의 틀
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu, tearoff=0)  # 상위 메뉴 (파일)
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=openImage)
fileMenu.add_command(label='저장', command=saveImage)
fileMenu.add_separator()
fileMenu.add_command(label='효과누적', command=accumImage)
fileMenu.add_separator()
fileMenu.add_command(label='종료', command=exit)

pixelMenu = Menu(mainMenu, tearoff=0)  # 상위 메뉴 (화소점처리)
mainMenu.add_cascade(label='화소점 처리', menu=pixelMenu)
pixelMenu.add_command(label='동일 이미지', command=equalImage)
pixelMenu.add_command(label='밝게/어둡게', command=addImage)
pixelMenu.add_separator()
pixelMenu.add_command(label='곱셈', command=mulImage)
pixelMenu.add_command(label='나눗셈', command=divImage)
pixelMenu.add_command(label='AND', command=andImage)
pixelMenu.add_command(label='OR', command=orImage)
pixelMenu.add_command(label='XOR', command=xorImage)
pixelMenu.add_command(label='반전', command=reverseImage)
pixelMenu.add_separator()
pixelMenu.add_command(label='흑백', command=bwImage)
pixelMenu.add_command(label='흑백(평균값)', command=bwAvgImage)
pixelMenu.add_command(label='흑백(중앙값)', command=bwMedImage)
pixelMenu.add_separator()
pixelMenu.add_command(label='감마', command=gammaImage)
pixelMenu.add_command(label='파라볼라 CAP', command=paraImage)
pixelMenu.add_command(label='파라볼라 CUP', command=paraImage2)
pixelMenu.add_command(label='포스터라이징', command=postImage)
pixelMenu.add_command(label='강조', command=stressImage)

geoMenu = Menu(mainMenu, tearoff=0)  # 상위 메뉴 (기하학처리)
mainMenu.add_cascade(label='기하학 처리', menu=geoMenu)
geoMenu.add_command(label='이동', command=move)
geoMenu.add_command(label='좌우대칭', command=mirrorHor)
geoMenu.add_command(label='상하대칭', command=mirrorVer)
geoMenu.add_separator()
geoMenu.add_command(label='확대(포워딩)', command=zoomIn)
geoMenu.add_command(label='확대(백워딩)', command=zoomIn2)
geoMenu.add_command(label='확대(양선형 보간)', command=zoomIn3)
geoMenu.add_separator()
geoMenu.add_command(label='축소', command=zoomOut)
geoMenu.add_command(label='축소(평균값)', command=zoomOutAvg)
geoMenu.add_command(label='축소(중앙값)', command=zoomOutMed)
geoMenu.add_separator()
geoMenu.add_command(label='회전', command=rotate)
geoMenu.add_command(label='회전(중앙,백워딩)', command=rotate2)
geoMenu.add_command(label='회전(확대)', command=rotate3)
# geoMenu.add_command(label='회전(확대,양선형)', command=None)
geoMenu.add_separator()
geoMenu.add_command(label='모핑', command=morph)

histoMenu = Menu(mainMenu, tearoff=0)  # 상위 메뉴 (히스토그램 처리)
mainMenu.add_cascade(label='히스토그램 처리', menu=histoMenu)
histoMenu.add_command(label='히스토그램 스트레칭', command=histoStretch)
histoMenu.add_command(label='앤드-인', command=endIn)
histoMenu.add_command(label='평활화', command=histoEqual)

areaMenu = Menu(mainMenu, tearoff=0)  # 상위 메뉴 (화소 영역 처리)
mainMenu.add_cascade(label='화소 영역 처리', menu=areaMenu)
areaMenu.add_command(label='엠보싱', command=emboss)
areaMenu.add_command(label='블러링', command=blur)
areaMenu.add_command(label='블러링(9x9)', command=blur2)
areaMenu.add_command(label='샤프닝', command=sharp)
areaMenu.add_command(label='고주파샤프닝', command=sharpHpf)

edgeMenu = Menu(mainMenu, tearoff=0)  # 상위 메뉴 (기하학처리)
mainMenu.add_cascade(label='경계선 검출', menu=edgeMenu)
edgeMenu.add_command(label='수직 에지검출', command=edge1)
edgeMenu.add_command(label='에지검출(유사연산)', command=edgeHomo)
edgeMenu.add_command(label='에지검출(차연산)', command=edgeSub)
edgeMenu.add_separator()
edgeMenu.add_command(label='로버츠', command=robert)
edgeMenu.add_command(label='소벨', command=sobel)
edgeMenu.add_separator()
edgeMenu.add_command(label='라플라시안', command=lapla)
edgeMenu.add_command(label='LoG', command=loG)
edgeMenu.add_command(label='DoG', command=doG)

window.mainloop()