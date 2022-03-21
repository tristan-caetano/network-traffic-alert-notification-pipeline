# Network Traffic Alert Notification Pipeline Project MVP
# University of Massachusetts Dartmouth
# Naval Undersea Warfare Center

# Client: Benjamin Drozdenko
# Team Lead: Tristan Caetano
# Scrum Master: Jake Holme
# Vinicius Coelho: Project Coordinator
# Lead Developer: Jason Pinto
# Developer: Tate DeTerra

# Final GUI for interfacing with the pipeline

#  ---------------  Libraries  ---------------
import os
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import math
import csv

#  --------------- Components  ---------------
import pcap_to_csv as ptc
import train_test_creator as ttc
import normalize as norm
import data_trimmer as dt
import parameterizer as param
import parameterize_mal as pmal
import multiclass_classification as multi

#  ---------------  Global Variables  ---------------
importedfile = ""
settings = [1, 0, 1000, 0,
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            0, 0]
# SETTINGS VARIABLE GUIDE:  [(number of layers), (type), (epoch number), (first layer input size),
#                           [(layer type for all 10 layers)],
#                           [(number of neurons for all 10 layers)],
#                           [(activation for all 10 layers)],
#                           (learning rate), (optimizer)]                    all integers, 0-based
lock = False

#  ---------------  CSS Stylesheet  ---------------
style = """
            QPushButton {
                background-color: #AFC1CC;
                border-width: 0px;
                border-radius: 4px;
                }
            QPushButton:hover{
                background-color: #7895A2;
            }
            QPushButton:pressed{
                background-color: #517281;
            }
            QTableView {
                selection-background-color: #517281;
            }
            QScrollBar {
                background-color: #AFC1CC;
            }
            QProgressBar {
                border: solid grey;
                border-radius: 8px;
                color: black;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;
                border-radius: 8px;
            }
            QSpinBox {
                border: 0px;
                border-radius: 4px;
                background-color: #CCD7DF;
            }
            QSpinBox:hover {
                background-color: #AFC1CC;
            }
            QComboBox {
                border: 0px;
                border-radius: 4px;
                background-color: #CCD7DF;
            }
            QComboBox:hover {
                background-color: #AFC1CC;
            }
            QComboBox QAbstractItemView {
                selection-background-color: #517281;
            }
        """

#  ---------------  Program  ---------------
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFixedSize(1000, 800)
        self.setStyleSheet(style)
        fnt = QtGui.QFont('Georgia', 14)
        fntb = QtGui.QFont('Georgia', 16)
        fntb.setBold(True)
        self.ddboarder = QtWidgets.QPushButton(self)
        self.ddboarder.setGeometry(QtCore.QRect(20, 20, 820, 156))
        self.ddboarder.setStyleSheet("background-color: white; border: 3px black; border-radius: 10px; border-style: dashed")
        self.bStart = QtWidgets.QPushButton(self)
        self.bStart.setGeometry(QtCore.QRect(439, 120, 1, 1))
        self.bStart.setFont(fntb)
        self.bStart.setStyleSheet("QPushButton {background-color: #ACD2C3;border-width: 0px;border-radius: 4px;}QPushButton:hover{background-color: #89B0A1;}QPushButton:pressed{background-color: #59756A;}")
        self.bStart.setHidden(True)
        self.bFile = QtWidgets.QPushButton(self)
        self.bFile.setGeometry(QtCore.QRect(294, 81, 160, 36))
        self.bFile.setFont(fnt)
        self.bSettings = QtWidgets.QPushButton(self)
        self.bSettings.setGeometry(QtCore.QRect(860, 60, 120, 36))
        self.bSettings.setFont(fnt)
        self.bHelp = QtWidgets.QPushButton(self)
        self.bHelp.setGeometry(QtCore.QRect(860, 20, 120, 36))
        self.bHelp.setFont(fnt)
        self.bCSV = QtWidgets.QPushButton(self)
        self.bCSV.setGeometry(QtCore.QRect(860, 140, 120, 36))
        self.bCSV.setFont(fnt)
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(520, 184, 450, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setFont(QtGui.QFont('Times', 12))
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setHidden(True)
        self.label = QtWidgets.QLabel('NULL', self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.resize(300, 80)
        self.label.move(288, 60)
        self.label.setFont(fntb)
        self.label.setHidden(True)
        self.label2 = QtWidgets.QLabel('or drop it here', self)
        self.label2.resize(200, 30)
        self.label2.move(460, 84)
        self.label2.setFont(fnt)
        self.label3 = QtWidgets.QLabel('NULL', self)
        self.label3.resize(200, 30)
        self.label3.move(22, 180)
        self.label3.setHidden(True)
        self.label3.setFont(fnt)
        self.table = QtWidgets.QTableView(self)
        self.table.setGeometry(QtCore.QRect(20, 210, 960, 570))
        self.table.horizontalHeader().setHidden(True)
        self.table.verticalHeader().setHidden(True)
        self.table.verticalHeader().setDefaultSectionSize(18)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table.setFont(QtGui.QFont('Times', 12))
        self.model = QtGui.QStandardItemModel(self)
        self.table.setModel(self.model)
        self.table.setHidden(True)

        self.anim1 = QtCore.QPropertyAnimation(self.bFile, b"pos")
        self.anim1.setEndValue(QtCore.QPoint(294, 34))
        self.anim1.setDuration(200)
        self.anim1.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.anim2 = QtCore.QPropertyAnimation(self.label2, b"pos")
        self.anim2.setEndValue(QtCore.QPoint(460, 37))
        self.anim2.setDuration(200)
        self.anim2.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.anim3 = QtCore.QPropertyAnimation(self.bStart, b"size")
        self.anim3.setEndValue(QtCore.QSize(270, 80))
        self.anim3.setDuration(200)
        self.anim3.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.anim4 = QtCore.QPropertyAnimation(self.bStart, b"pos")
        self.anim4.setEndValue(QtCore.QPoint(304, 80))
        self.anim4.setDuration(200)
        self.anim4.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.anim5 = QtCore.QPropertyAnimation(self.ddboarder, b"size")
        self.anim5.setEndValue(QtCore.QSize(850, 186))
        self.anim5.setDuration(200)
        self.anim5.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self.anim6 = QtCore.QPropertyAnimation(self.ddboarder, b"pos")
        self.anim6.setEndValue(QtCore.QPoint(5, 5))
        self.anim6.setDuration(200)
        self.anim6.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self.anim7 = QtCore.QPropertyAnimation(self.ddboarder, b"size")
        self.anim7.setEndValue(QtCore.QSize(820, 156))
        self.anim7.setDuration(200)
        self.anim7.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self.anim8 = QtCore.QPropertyAnimation(self.ddboarder, b"pos")
        self.anim8.setEndValue(QtCore.QPoint(20, 20))
        self.anim8.setDuration(200)
        self.anim8.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Network Traffic Alert Notification Pipeline"))
        self.bSettings.setText(_translate("MainWindow", "Settings"))
        self.bSettings.clicked.connect(self.openSettings)
        self.bHelp.setText(_translate("MainWindow", "Help"))
        self.bHelp.clicked.connect(self.openHelp)
        self.bStart.setText(_translate("MainWindow", "Start"))
        self.bStart.clicked.connect(self.startProcess)
        self.bFile.setText(_translate("MainWindow", "Choose PCAP file"))
        self.bFile.clicked.connect(self.openFile)
        self.bCSV.setText(_translate("MainWindow", "Display CSV"))
        self.bCSV.clicked.connect(self.openCSV)

    def openHelp(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("How to use the Network Alert Pipeline")
        dlg.setText("1. Click Select File and choose a valid PCAP file to analyze\n2. Click START\n\nClick Settings to customize various parameters")
        dlg.setStyleSheet("QPushButton {border-radius: 2px; width: 60px; height: 20px;}")
        button = dlg.exec()

    def openSettings(self):
        global lock
        if lock == False:
            lock = True
            print("OPEN SETTINGS MENU")
            SettingsWindow.show(Sui)

    def startProcess(self):
        global lock
        if lock == False:
            if os.path.isfile(importedfile):
                lock=True
                print("STARTING WITH FILE:", importedfile)
                basename = os.path.basename(importedfile)
                self.label2.setHidden(True)
                self.bFile.setHidden(True)
                self.bStart.setHidden(True)
                self.label.setText("Analyzing "+basename)
                self.label.setHidden(False)
                self.progressBar.setHidden(False)

                # Pcap to csv converter
                converted_file = ptc.convert(basename, self)

                # Parameterizer
                # p_converted_file = param.parameterize(converted_file, self)

                # Normalizer
                n_converted_file = norm.digest_file(converted_file, self)

                SettingsWindow.updateMessage(self, 90, "Displaying normalized file.")

                #TRIGGERS AFTER PROCESS IS COMPLETE
                self.progressBar.setHidden(True)
                self.progressBar.setProperty("value", 0)
                self.label2.move(460, 84)
                self.label2.setText("or drop it here")
                self.label2.setHidden(False)
                self.bFile.move(294, 81)
                self.bFile.setHidden(False)
                self.bStart.move(439, 120)
                self.bStart.resize(1, 1)
                self.label.setHidden(True)
                self.showCSV(n_converted_file)

                SettingsWindow.updateMessage(self, 100, "Complete.")

                lock = False
            else:
                print("NO FILE SELECTED, cannot start process")

    def openFile(self):
        if lock == False:
            global importedfile
            importedfileX = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select a PCAP file',directory=os.getcwd(), filter='PCAP File (*.pcap)')
            importedfileX = importedfileX[0]
            if os.path.isfile(importedfileX):
                importedfile = importedfileX
                self.acceptImport()
            else:
                print("No file or invalid file selected")

    def dragEnterEvent(self, event):
        if lock == False:
            data = event.mimeData()
            urls = data.urls()
            if urls and urls[0].scheme() == 'file':
                event.accept()
                self.anim5.start()
                self.anim6.start()
            else:
                event.ignore()

    def dropEvent(self, event):
        if lock == False:
            data = event.mimeData()
            urls = data.urls()
            if urls and urls[0].scheme() == 'file':
                self.anim7.start()
                self.anim8.start()
                importedfileX = str(urls[0].path())[1:]
                if importedfileX[-5:].upper() == ".PCAP":
                    global importedfile
                    importedfile = importedfileX
                    self.acceptImport()
                else:
                    print("Invalid file selected")

    def dragLeaveEvent(self, event):
        self.anim7.start()
        self.anim8.start()

    def acceptImport(self):
        print("Imported file:", importedfile)
        self.bStart.setHidden(False)
        self.label2.setText(os.path.basename(importedfile))
        self.anim1.start()
        self.anim2.start()
        self.anim3.start()
        self.anim4.start()

    def openCSV(self):
        if lock == False:
            importedCSV = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select a CSV file',directory=os.getcwd(), filter='CSV File (*.csv)')
            importedCSV = importedCSV[0]
            if os.path.isfile(importedCSV):
                print("Imported CSV:", importedCSV)
                self.showCSV(importedCSV)
            else:
                print("No file or invalid file selected")

    def updateBar(self, goto):
        cur = self.progressBar.value()
        while cur < goto:
            cur = cur + math.ceil((goto - cur) / 10)
            self.progressBar.setProperty("value", cur)
            time.sleep(0.03)

    def showCSV(self, filename):
        self.model.clear()
        with open(filename, 'r') as f:
            for row in csv.reader(f):
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]
                self.model.appendRow(items)
                self.table.setHidden(False)
                self.label3.setText(os.path.basename(filename)+":")
                self.label3.setHidden(False)

class SettingsWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 840)
        self.setStyleSheet(style)
        fnt = QtGui.QFont('Georgia', 12)
        self.bHelp = QtWidgets.QPushButton(self)
        self.bHelp.setGeometry(QtCore.QRect(660, 20, 120, 36))
        self.bHelp.setFont(fnt)
        self.bTrain = QtWidgets.QPushButton(self)
        self.bTrain.setGeometry(QtCore.QRect(510, 20, 140, 72))
        self.bTrain.setFont(fnt)
        self.layers = QtWidgets.QSpinBox(self)
        self.layers.setRange(1, 10)
        self.layers.setValue(settings[0])
        self.layers.resize(50, 30)
        self.layers.move(80, 62)
        self.layers.setFont(fnt)
        l = QtWidgets.QLabel('Layers:', self)
        l.resize(58, 30)
        l.move(20, 62)
        l.setFont(fnt)
        self.learn = QtWidgets.QSpinBox(self)
        self.learn.setRange(0, 1)
        self.learn.setValue(settings[7])
        self.learn.resize(50, 30)
        self.learn.move(252, 62)
        self.learn.setFont(fnt)
        l = QtWidgets.QLabel('Learning Rate:', self)
        l.resize(108, 30)
        l.move(140, 62)
        l.setFont(fnt)
        self.type = QtWidgets.QComboBox(self)
        self.type.addItem("Binary")
        self.type.addItem("Multiclass")
        self.type.setCurrentIndex(settings[1])
        self.type.resize(100, 30)
        self.type.move(202, 20)
        self.type.setFont(fnt)
        l = QtWidgets.QLabel('Algorithm:', self)
        l.resize(100, 30)
        l.move(118, 20)
        l.setFont(fnt)
        self.optimizer = QtWidgets.QComboBox(self)
        self.optimizer.addItem("Adadelta")
        self.optimizer.addItem("Adagrad")
        self.optimizer.addItem("Adam")
        self.optimizer.addItem("Adamax")
        self.optimizer.addItem("Ftrl")
        self.optimizer.addItem("Nadam")
        self.optimizer.addItem("Optimizer")
        self.optimizer.addItem("RMSprop")
        self.optimizer.addItem("SGD")
        self.optimizer.setCurrentIndex(settings[8])
        self.optimizer.resize(100, 30)
        self.optimizer.move(396, 20)
        self.optimizer.setFont(fnt)
        l = QtWidgets.QLabel('Optimizer:', self)
        l.resize(80, 30)
        l.move(312, 20)
        l.setFont(fnt)
        self.epochs = QtWidgets.QSpinBox(self)
        self.epochs.setRange(10, 10000)
        self.epochs.setValue(settings[2])
        self.epochs.resize(90, 30)
        self.epochs.move(406, 62)
        self.epochs.setFont(fnt)
        l = QtWidgets.QLabel('Epochs:', self)
        l.resize(60, 30)
        l.move(343, 62)
        l.setFont(fnt)
        self.s14 = QtWidgets.QSpinBox(self)
        self.s14.setValue(settings[3])
        self.s14.setRange(0, 999999)
        self.s14.resize(88, 30)
        self.s14.move(692, 130)
        self.s14.setFont(fnt)
        l = QtWidgets.QLabel('Input Size:', self)
        l.resize(80, 30)
        l.move(610, 130)
        l.setFont(fnt)

        #CONFIGURABLES FOR LAYERS
        l1 = "Layer Type:"
        l1l = 94
        l1p = 20
        w1 = 4
        w1s = ["Dense", "Flatten", "Conv1D", "MaxPooling1D"]
        w1l = 130
        w1p = 114
        l2 = "Neurons:"
        l2l = 66
        l2p = 255
        w2min = 0
        w2max = 999999
        w2l = 88
        w2p = 327
        l3 = "Activation:"
        l3l = 90
        l3p = 426
        w3 = 2
        w3s = ["ReLU", "Softmax"]
        w3l = 90
        w3p = 510
        #LAYER 1
        self.lt1 = QtWidgets.QLabel("Layer 1", self)
        self.lt1.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt1.resize(760, 30)
        self.lt1.move(20, 104)
        self.lt1.setFont(QtGui.QFont('Georgia', 10))
        self.s11 = QtWidgets.QComboBox(self)
        for i in range(0, w1):
            self.s11.addItem(w1s[i])
        self.s11.setCurrentIndex(settings[4][0])
        self.s11.resize(w1l, 30)
        self.s11.move(w1p, 130)
        self.s11.setFont(fnt)
        self.l11 = QtWidgets.QLabel(l1, self)
        self.l11.resize(l1l, 30)
        self.l11.move(l1p, 130)
        self.l11.setFont(fnt)
        self.s12 = QtWidgets.QSpinBox(self)
        self.s12.setRange(w2min, w2max)
        self.s12.setValue(settings[5][0])
        self.s12.resize(w2l, 30)
        self.s12.move(w2p, 130)
        self.s12.setFont(fnt)
        self.l12 = QtWidgets.QLabel(l2, self)
        self.l12.resize(l2l, 30)
        self.l12.move(l2p, 130)
        self.l12.setFont(fnt)
        self.s13 = QtWidgets.QComboBox(self)
        for i in range(0, w3):
            self.s13.addItem(w3s[i])
        self.s13.setCurrentIndex(settings[6][0])
        self.s13.resize(w3l, 30)
        self.s13.move(w3p, 130)
        self.s13.setFont(fnt)
        self.l13 = QtWidgets.QLabel(l3, self)
        self.l13.resize(l3l, 30)
        self.l13.move(l3p, 130)
        self.l13.setFont(fnt)
        # LAYER 2
        self.lt2 = QtWidgets.QLabel("Layer 2", self)
        self.lt2.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt2.resize(760, 30)
        self.lt2.move(20, 174)
        self.lt2.setFont(QtGui.QFont('Georgia', 10))
        self.s21 = QtWidgets.QComboBox(self)
        for i in range(0, w1):
            self.s21.addItem(w1s[i])
        self.s21.setCurrentIndex(settings[4][1])
        self.s21.resize(w1l, 30)
        self.s21.move(w1p, 200)
        self.s21.setFont(fnt)
        self.l21 = QtWidgets.QLabel(l1, self)
        self.l21.resize(l1l, 30)
        self.l21.move(l1p, 200)
        self.l21.setFont(fnt)
        self.s22 = QtWidgets.QSpinBox(self)
        self.s22.setRange(w2min, w2max)
        self.s22.setValue(settings[5][1])
        self.s22.resize(w2l, 30)
        self.s22.move(w2p, 200)
        self.s22.setFont(fnt)
        self.l22 = QtWidgets.QLabel(l2, self)
        self.l22.resize(l2l, 30)
        self.l22.move(l2p, 200)
        self.l22.setFont(fnt)
        self.s23 = QtWidgets.QComboBox(self)
        for i in range(0, w3):
            self.s23.addItem(w3s[i])
        self.s23.setCurrentIndex(settings[6][1])
        self.s23.resize(w3l, 30)
        self.s23.move(w3p, 200)
        self.s23.setFont(fnt)
        self.l23 = QtWidgets.QLabel(l3, self)
        self.l23.resize(l3l, 30)
        self.l23.move(l3p, 200)
        self.l23.setFont(fnt)
        # LAYER 3
        self.lt3 = QtWidgets.QLabel("Layer 3", self)
        self.lt3.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt3.resize(760, 30)
        self.lt3.move(20, 244)
        self.lt3.setFont(QtGui.QFont('Georgia', 10))
        self.s31 = QtWidgets.QComboBox(self)
        for i in range(0, w1):
            self.s31.addItem(w1s[i])
        self.s31.setCurrentIndex(settings[4][2])
        self.s31.resize(w1l, 30)
        self.s31.move(w1p, 270)
        self.s31.setFont(fnt)
        self.l31 = QtWidgets.QLabel(l1, self)
        self.l31.resize(l1l, 30)
        self.l31.move(l1p, 270)
        self.l31.setFont(fnt)
        self.s32 = QtWidgets.QSpinBox(self)
        self.s32.setRange(w2min, w2max)
        self.s32.setValue(settings[5][2])
        self.s32.resize(w2l, 30)
        self.s32.move(w2p, 270)
        self.s32.setFont(fnt)
        self.l32 = QtWidgets.QLabel(l2, self)
        self.l32.resize(l2l, 30)
        self.l32.move(l2p, 270)
        self.l32.setFont(fnt)
        self.s33 = QtWidgets.QComboBox(self)
        for i in range(0, w3):
            self.s33.addItem(w3s[i])
        self.s33.setCurrentIndex(settings[6][2])
        self.s33.resize(w3l, 30)
        self.s33.move(w3p, 270)
        self.s33.setFont(fnt)
        self.l33 = QtWidgets.QLabel(l3, self)
        self.l33.resize(l3l, 30)
        self.l33.move(l3p, 270)
        self.l33.setFont(fnt)
        # LAYER 4
        self.lt4 = QtWidgets.QLabel("Layer 4", self)
        self.lt4.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt4.resize(760, 30)
        self.lt4.move(20, 314)
        self.lt4.setFont(QtGui.QFont('Georgia', 10))
        self.s41 = QtWidgets.QComboBox(self)
        for i in range(0, w1):
            self.s41.addItem(w1s[i])
        self.s41.setCurrentIndex(settings[4][3])
        self.s41.resize(w1l, 30)
        self.s41.move(w1p, 340)
        self.s41.setFont(fnt)
        self.l41 = QtWidgets.QLabel(l1, self)
        self.l41.resize(l1l, 30)
        self.l41.move(l1p, 340)
        self.l41.setFont(fnt)
        self.s42 = QtWidgets.QSpinBox(self)
        self.s42.setRange(w2min, w2max)
        self.s42.setValue(settings[5][3])
        self.s42.resize(w2l, 30)
        self.s42.move(w2p, 340)
        self.s42.setFont(fnt)
        self.l42 = QtWidgets.QLabel(l2, self)
        self.l42.resize(l2l, 30)
        self.l42.move(l2p, 340)
        self.l42.setFont(fnt)
        self.s43 = QtWidgets.QComboBox(self)
        for i in range(0, w3):
            self.s43.addItem(w3s[i])
        self.s43.setCurrentIndex(settings[6][3])
        self.s43.resize(w3l, 30)
        self.s43.move(w3p, 340)
        self.s43.setFont(fnt)
        self.l43 = QtWidgets.QLabel(l3, self)
        self.l43.resize(l3l, 30)
        self.l43.move(l3p, 340)
        self.l43.setFont(fnt)
        # LAYER 5
        self.lt5 = QtWidgets.QLabel("Layer 5", self)
        self.lt5.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt5.resize(760, 30)
        self.lt5.move(20, 384)
        self.lt5.setFont(QtGui.QFont('Georgia', 10))
        self.s51 = QtWidgets.QComboBox(self)
        for i in range(0, w1):
            self.s51.addItem(w1s[i])
        self.s51.setCurrentIndex(settings[4][4])
        self.s51.resize(w1l, 30)
        self.s51.move(w1p, 410)
        self.s51.setFont(fnt)
        self.l51 = QtWidgets.QLabel(l1, self)
        self.l51.resize(l1l, 30)
        self.l51.move(l1p, 410)
        self.l51.setFont(fnt)
        self.s52 = QtWidgets.QSpinBox(self)
        self.s52.setRange(w2min, w2max)
        self.s52.setValue(settings[5][4])
        self.s52.resize(w2l, 30)
        self.s52.move(w2p, 410)
        self.s52.setFont(fnt)
        self.l52 = QtWidgets.QLabel(l2, self)
        self.l52.resize(l2l, 30)
        self.l52.move(l2p, 410)
        self.l52.setFont(fnt)
        self.s53 = QtWidgets.QComboBox(self)
        for i in range(0, w3):
            self.s53.addItem(w3s[i])
        self.s53.setCurrentIndex(settings[6][4])
        self.s53.resize(w3l, 30)
        self.s53.move(w3p, 410)
        self.s53.setFont(fnt)
        self.l53 = QtWidgets.QLabel(l3, self)
        self.l53.resize(l3l, 30)
        self.l53.move(l3p, 410)
        self.l53.setFont(fnt)
        # LAYER 6
        self.lt6 = QtWidgets.QLabel("Layer 6", self)
        self.lt6.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt6.resize(760, 30)
        self.lt6.move(20, 454)
        self.lt6.setFont(QtGui.QFont('Georgia', 10))
        self.s61 = QtWidgets.QComboBox(self)
        for i in range(0, w1):
            self.s61.addItem(w1s[i])
        self.s61.setCurrentIndex(settings[4][5])
        self.s61.resize(w1l, 30)
        self.s61.move(w1p, 480)
        self.s61.setFont(fnt)
        self.l61 = QtWidgets.QLabel(l1, self)
        self.l61.resize(l1l, 30)
        self.l61.move(l1p, 480)
        self.l61.setFont(fnt)
        self.s62 = QtWidgets.QSpinBox(self)
        self.s62.setRange(w2min, w2max)
        self.s62.setValue(settings[5][5])
        self.s62.resize(w2l, 30)
        self.s62.move(w2p, 480)
        self.s62.setFont(fnt)
        self.l62 = QtWidgets.QLabel(l2, self)
        self.l62.resize(l2l, 30)
        self.l62.move(l2p, 480)
        self.l62.setFont(fnt)
        self.s63 = QtWidgets.QComboBox(self)
        for i in range(0, w3):
            self.s63.addItem(w3s[i])
        self.s63.setCurrentIndex(settings[6][5])
        self.s63.resize(w3l, 30)
        self.s63.move(w3p, 480)
        self.s63.setFont(fnt)
        self.l63 = QtWidgets.QLabel(l3, self)
        self.l63.resize(l3l, 30)
        self.l63.move(l3p, 480)
        self.l63.setFont(fnt)
        # LAYER 7
        self.lt7 = QtWidgets.QLabel("Layer 7", self)
        self.lt7.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt7.resize(760, 30)
        self.lt7.move(20, 524)
        self.lt7.setFont(QtGui.QFont('Georgia', 10))
        self.s71 = QtWidgets.QComboBox(self)
        for i in range(0, w1):
            self.s71.addItem(w1s[i])
        self.s71.setCurrentIndex(settings[4][6])
        self.s71.resize(w1l, 30)
        self.s71.move(w1p, 550)
        self.s71.setFont(fnt)
        self.l71 = QtWidgets.QLabel(l1, self)
        self.l71.resize(l1l, 30)
        self.l71.move(l1p, 550)
        self.l71.setFont(fnt)
        self.s72 = QtWidgets.QSpinBox(self)
        self.s72.setRange(w2min, w2max)
        self.s72.setValue(settings[5][6])
        self.s72.resize(w2l, 30)
        self.s72.move(w2p, 550)
        self.s72.setFont(fnt)
        self.l72 = QtWidgets.QLabel(l2, self)
        self.l72.resize(l2l, 30)
        self.l72.move(l2p, 550)
        self.l72.setFont(fnt)
        self.s73 = QtWidgets.QComboBox(self)
        for i in range(0, w3):
            self.s73.addItem(w3s[i])
        self.s73.setCurrentIndex(settings[6][6])
        self.s73.resize(w3l, 30)
        self.s73.move(w3p, 550)
        self.s73.setFont(fnt)
        self.l73 = QtWidgets.QLabel(l3, self)
        self.l73.resize(l3l, 30)
        self.l73.move(l3p, 550)
        self.l73.setFont(fnt)
        # LAYER 8
        self.lt8 = QtWidgets.QLabel("Layer 8", self)
        self.lt8.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt8.resize(760, 30)
        self.lt8.move(20, 594)
        self.lt8.setFont(QtGui.QFont('Georgia', 10))
        self.s81 = QtWidgets.QComboBox(self)
        for i in range(0, w1):
            self.s81.addItem(w1s[i])
        self.s81.setCurrentIndex(settings[4][7])
        self.s81.resize(w1l, 30)
        self.s81.move(w1p, 620)
        self.s81.setFont(fnt)
        self.l81 = QtWidgets.QLabel(l1, self)
        self.l81.resize(l1l, 30)
        self.l81.move(l1p, 620)
        self.l81.setFont(fnt)
        self.s82 = QtWidgets.QSpinBox(self)
        self.s82.setRange(w2min, w2max)
        self.s82.setValue(settings[5][7])
        self.s82.resize(w2l, 30)
        self.s82.move(w2p, 620)
        self.s82.setFont(fnt)
        self.l82 = QtWidgets.QLabel(l2, self)
        self.l82.resize(l2l, 30)
        self.l82.move(l2p, 620)
        self.l82.setFont(fnt)
        self.s83 = QtWidgets.QComboBox(self)
        for i in range(0, w3):
            self.s83.addItem(w3s[i])
        self.s83.setCurrentIndex(settings[6][7])
        self.s83.resize(w3l, 30)
        self.s83.move(w3p, 620)
        self.s83.setFont(fnt)
        self.l83 = QtWidgets.QLabel(l3, self)
        self.l83.resize(l3l, 30)
        self.l83.move(l3p, 620)
        self.l83.setFont(fnt)
        # LAYER 9
        self.lt9 = QtWidgets.QLabel("Layer 9", self)
        self.lt9.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt9.resize(760, 30)
        self.lt9.move(20, 664)
        self.lt9.setFont(QtGui.QFont('Georgia', 10))
        self.s91 = QtWidgets.QComboBox(self)
        for i in range(0, w1):
            self.s91.addItem(w1s[i])
        self.s91.setCurrentIndex(settings[4][8])
        self.s91.resize(w1l, 30)
        self.s91.move(w1p, 690)
        self.s91.setFont(fnt)
        self.l91 = QtWidgets.QLabel(l1, self)
        self.l91.resize(l1l, 30)
        self.l91.move(l1p, 690)
        self.l91.setFont(fnt)
        self.s92 = QtWidgets.QSpinBox(self)
        self.s92.setRange(w2min, w2max)
        self.s92.setValue(settings[5][8])
        self.s92.resize(w2l, 30)
        self.s92.move(w2p, 690)
        self.s92.setFont(fnt)
        self.l92 = QtWidgets.QLabel(l2, self)
        self.l92.resize(l2l, 30)
        self.l92.move(l2p, 690)
        self.l92.setFont(fnt)
        self.s93 = QtWidgets.QComboBox(self)
        for i in range(0, w3):
            self.s93.addItem(w3s[i])
        self.s93.setCurrentIndex(settings[6][8])
        self.s93.resize(w3l, 30)
        self.s93.move(w3p, 690)
        self.s93.setFont(fnt)
        self.l93 = QtWidgets.QLabel(l3, self)
        self.l93.resize(l3l, 30)
        self.l93.move(l3p, 690)
        self.l93.setFont(fnt)
        # LAYER 10
        self.lt0 = QtWidgets.QLabel("Layer 10", self)
        self.lt0.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt0.resize(760, 30)
        self.lt0.move(20, 734)
        self.lt0.setFont(QtGui.QFont('Georgia', 10))
        self.s01 = QtWidgets.QComboBox(self)
        for i in range(0, w1):
            self.s01.addItem(w1s[i])
        self.s01.setCurrentIndex(settings[4][9])
        self.s01.resize(w1l, 30)
        self.s01.move(w1p, 760)
        self.s01.setFont(fnt)
        self.l01 = QtWidgets.QLabel(l1, self)
        self.l01.resize(l1l, 30)
        self.l01.move(l1p, 760)
        self.l01.setFont(fnt)
        self.s02 = QtWidgets.QSpinBox(self)
        self.s02.setRange(w2min, w2max)
        self.s02.setValue(settings[5][9])
        self.s02.resize(w2l, 30)
        self.s02.move(w2p, 760)
        self.s02.setFont(fnt)
        self.l02 = QtWidgets.QLabel(l2, self)
        self.l02.resize(l2l, 30)
        self.l02.move(l2p, 760)
        self.l02.setFont(fnt)
        self.s03 = QtWidgets.QComboBox(self)
        for i in range(0, w3):
            self.s03.addItem(w3s[i])
        self.s03.setCurrentIndex(settings[6][9])
        self.s03.resize(w3l, 30)
        self.s03.move(w3p, 760)
        self.s03.setFont(fnt)
        self.l03 = QtWidgets.QLabel(l3, self)
        self.l03.resize(l3l, 30)
        self.l03.move(l3p, 760)
        self.l03.setFont(fnt)
        self.cover = QtWidgets.QPushButton(self)
        self.cover.setGeometry(QtCore.QRect(0, 100+70*self.layers.value(), 800, 650))
        self.cover.setStyleSheet("background-color: #F0F0F0; border: 0px; border-radius: 0px;")

        l = QtWidgets.QLabel('Network Traffic Alert Notification Pipeline - Version: 1.2.0', self)
        l.resize(380, 20)
        l.move(430, 820)
        l.setFont(QtGui.QFont('Georgia', 10))

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        global settings
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SettingsWindow", "Pipeline Settings"))
        self.bHelp.setText(_translate("SettingsWindow", "Help"))
        self.bHelp.clicked.connect(self.openHelp)
        self.bTrain.setText(_translate("SettingsWindow", "Import New\nTraining Data"))
        self.bTrain.clicked.connect(self.openFile)
        self.layers.valueChanged.connect(self.save0)
        self.type.currentIndexChanged.connect(self.saveTop)
        self.epochs.valueChanged.connect(self.saveTop)
        self.learn.valueChanged.connect(self.saveTop)
        self.optimizer.currentIndexChanged.connect(self.saveTop)
        self.s14.valueChanged.connect(self.saveTop)
        self.s11.currentIndexChanged.connect(self.save1)
        self.s12.valueChanged.connect(self.save2)
        self.s13.currentIndexChanged.connect(self.save3)
        self.s21.currentIndexChanged.connect(self.save1)
        self.s22.valueChanged.connect(self.save2)
        self.s23.currentIndexChanged.connect(self.save3)
        self.s31.currentIndexChanged.connect(self.save1)
        self.s32.valueChanged.connect(self.save2)
        self.s33.currentIndexChanged.connect(self.save3)
        self.s41.currentIndexChanged.connect(self.save1)
        self.s42.valueChanged.connect(self.save2)
        self.s43.currentIndexChanged.connect(self.save3)
        self.s51.currentIndexChanged.connect(self.save1)
        self.s52.valueChanged.connect(self.save2)
        self.s53.currentIndexChanged.connect(self.save3)
        self.s61.currentIndexChanged.connect(self.save1)
        self.s62.valueChanged.connect(self.save2)
        self.s63.currentIndexChanged.connect(self.save3)
        self.s71.currentIndexChanged.connect(self.save1)
        self.s72.valueChanged.connect(self.save2)
        self.s73.currentIndexChanged.connect(self.save3)
        self.s81.currentIndexChanged.connect(self.save1)
        self.s82.valueChanged.connect(self.save2)
        self.s83.currentIndexChanged.connect(self.save3)
        self.s91.currentIndexChanged.connect(self.save1)
        self.s92.valueChanged.connect(self.save2)
        self.s93.currentIndexChanged.connect(self.save3)
        self.s01.currentIndexChanged.connect(self.save1)
        self.s02.valueChanged.connect(self.save2)
        self.s03.currentIndexChanged.connect(self.save3)

    def closeEvent(self, event):
        global lock
        lock = False

    def openFile(self):
        importedfile1 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select TRAINING data',directory=os.getcwd(), filter='CSV File (*.csv)')
        importedfile2 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select TESTING data',directory=os.getcwd(), filter='CSV File (*.csv)')
        importedfile3 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select VALIDATION data',directory=os.getcwd(), filter='CSV File (*.csv)')
        importedfile1 = importedfile1[0]
        importedfile2 = importedfile2[0]
        importedfile3 = importedfile3[0]
        if os.path.isfile(importedfile1) & os.path.isfile(importedfile2) & os.path.isfile(importedfile3):
            print("CREATING TRAINING DATA")
            #CREATE TRAINING DATA FROM importedfile1 2 and 3
        else:
            print("No file(s) or invalid file(s) selected")

    def save0(self):
        global settings
        settings[0] = self.layers.value()
        self.showLayers(self.layers.value())
        print("SETTINGS SAVED:", settings)

    def save1(self):
        global settings
        settings[4][0] = self.s11.currentIndex()
        settings[4][1] = self.s21.currentIndex()
        settings[4][2] = self.s31.currentIndex()
        settings[4][3] = self.s41.currentIndex()
        settings[4][4] = self.s51.currentIndex()
        settings[4][5] = self.s61.currentIndex()
        settings[4][6] = self.s71.currentIndex()
        settings[4][7] = self.s81.currentIndex()
        settings[4][8] = self.s91.currentIndex()
        settings[4][9] = self.s01.currentIndex()
        print("SETTINGS SAVED:", settings)

    def save2(self):
        global settings
        settings[5][0] = self.s12.value()
        settings[5][1] = self.s22.value()
        settings[5][2] = self.s32.value()
        settings[5][3] = self.s42.value()
        settings[5][4] = self.s52.value()
        settings[5][5] = self.s62.value()
        settings[5][6] = self.s72.value()
        settings[5][7] = self.s82.value()
        settings[5][8] = self.s92.value()
        settings[5][9] = self.s02.value()
        print("SETTINGS SAVED:", settings)

    def save3(self):
        global settings
        settings[6][0] = self.s13.currentIndex()
        settings[6][1] = self.s23.currentIndex()
        settings[6][2] = self.s33.currentIndex()
        settings[6][3] = self.s43.currentIndex()
        settings[6][4] = self.s53.currentIndex()
        settings[6][5] = self.s63.currentIndex()
        settings[6][6] = self.s73.currentIndex()
        settings[6][7] = self.s83.currentIndex()
        settings[6][8] = self.s93.currentIndex()
        settings[6][9] = self.s03.currentIndex()
        print("SETTINGS SAVED:", settings)

    def saveTop(self):
        global settings
        settings[1] = self.type.currentIndex()
        settings[2] = self.epochs.value()
        settings[3] = self.s14.value()
        settings[7] = self.learn.value()
        settings[8] = self.optimizer.currentIndex()
        print("SETTINGS SAVED:", settings)

    def openHelp(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("Settings Help")
        dlg.setText("WRITE THIS")           ################################################NEED TO WRITE HELP TEXT############################################
        dlg.setStyleSheet("QPushButton {border-radius: 2px; width: 60px; height: 20px;}")
        button = dlg.exec()

    def showLayers(self, count):
        self.anim = QtCore.QPropertyAnimation(self.cover, b"pos")
        self.anim.setEndValue(QtCore.QPoint(0, 100+70*count))
        self.anim.setDuration(120)
        self.anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.anim.start()

    def updateMessage(self, progress, message):

        # Self can be set to 0 for testing modules outside the GUI
        if self != 0:
            self.label.setText(message)
            self.updateBar(progress)
        else: return

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    Sui = SettingsWindow()
    MainWindow.show(ui)
    sys.exit(app.exec_())