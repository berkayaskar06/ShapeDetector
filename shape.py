# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shape.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog
import cv2,imutils
from shapedetector import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(658, 716)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setText("")

        self.label.setPixmap(QtGui.QPixmap())
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.fileOpen = QtWidgets.QPushButton(self.centralwidget)
        self.fileOpen.setObjectName("fileOpen")
        self.gridLayout.addWidget(self.fileOpen, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.fileOpen.clicked.connect(self.loadImage)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Code add

        self.filename = None #Holds image
        self.tmp = None # Holds temporary image for disp

    def loadImage(self):
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*)")[0]
        image = cv2.imread(self.filename)
        ratio = image.shape[1]/5

        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        _ , thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
        contours = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        sd = ShapeDetector()

        for c in contours:
            length = (cv2.arcLength(c, True)) / ratio  # pixel to meter tranformation
            length = round(length, 2)
            shape = sd.detect(c)
            # then draw the contours and the name of the shape on the image
            cv2.drawContours(image, [c], -1, (0, 0, 255), 2)
            cv2.putText(image, shape, (20, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 1)
            cv2.putText(image, "Perimeter: {}".format(length), (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 255), 1)
            image = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)
            self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fileOpen.setText(_translate("MainWindow", "Open File"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

