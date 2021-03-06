from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import cv2
import numpy as np
import time

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.cpt=cv2.VideoCapture(0)
        self.fps=60
        self.sens=300
        _, self.img_O = self.cpt.read()
        self.img_O= cv2.cvtColor(self.img_O, cv2.COLOR_RGB2GRAY)
        cv2.imwrite('img_O.jpg',self.img_O)

        self.frame=QLabel(self) # 얼굴 표출 화면
        self.frame.resize(640,480)
        self.frame.setScaledContents(True)
        self.frame.move(5,5)
        
        self.btn_on=QPushButton("켜기",self)
        self.btn_on.resize(100,25)
        self.btn_on.move(5,490)
        self.btn_on.clicked.connect(self.start)

        self.btn_off=QPushButton("끄기",self)
        self.btn_off.resize(100,25)
        self.btn_off.move(110,490)
        self.btn_off.clicked.connect(self.stop)

        self.prt=QLabel(self)
        self.prt.resize(200,25)
        self.prt.move(215,490)

        self.sldr=QSlider(Qt.Horizontal,self)
        self.sldr.resize(100,25)
        self.sldr.move(415,490)
        self.sldr.setMinimum(1)
        self.sldr.setMaximum(60)
        self.sldr.setValue(24)
        self.sldr.valueChanged.connect(self.setFps)

        self.sldr1=QSlider(Qt.Horizontal,self)
        self.sldr1.resize(100,25)
        self.sldr1.move(520,490)
        self.sldr1.setMinimum(50)
        self.sldr1.setMaximum(500)
        self.sldr1.setValue(300)
        self.sldr1.valueChanged.connect(self.setSens)

        self.setGeometry(150,150,650,540)
        self.setWindowTitle("Cam_exam")
        self.show()

    
    def setFps(self):
        self.fps=self.sldr.value() 
        self.prt.setText("FPS "+str(self.fps)+"로 조정!")
        self.timer.stop() #타이머를 껏다가 다시킴
        self.timer.start(1000 / self.fps)

    def setSens(self):
        self.sens=self.sldr1.value()
        self.prt.setText("감도 "+str(self.sens)+"로 조정!")
    
    def start(self):
        self.timer=QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000 /self.fps) #24분의 1초마다 반복

    def nextFrameSlot(self):
        _, cam = self.cpt.read()
        cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)
        # cam = cv2.flip(cam,0) //영상 상하반전
        self .img_p=cv2.cvtColor(cam,cv2.COLOR_RGB2GRAY)
        cv2.imwrite('img_p.jpg',self.img_p)
        self.compare(self.img_O,self.img_p)
        self.img_O=self.img_p.copy()
        img=QImage(cam, cam.shape[1], cam.shape[0], QImage.Format_RGB888)#이미지객체만들어줌
        pix=QPixmap.fromImage(img) #픽스맵객체 만듬
        self.frame.setPixmap(pix)

    def compare(self,img_O,img_p):
        err=np.sum((img_O.astype("float") - img_p.astype("float")) ** 2)
        err /= float(img_O.shape[0] * img_p.shape[1])
        if(err >= self.sens):
            t=time.localtime()
            self.prt.setText("{}-{}-{} {}:{}:{} 움직임 감지!".format(t.tm_year, t.tm_mon,
             t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec))

    def stop(self):
        self.frame.setPixmap(QPixmap.fromImage(QImage()))#영상을 비우고 
        self.timer.stop()   #타임을 끔
    

    
if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())
