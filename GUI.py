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

#  ---------------  Program  ---------------
class Ui_MainWindow(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow):
        MainWindow.setFixedSize(815, 636)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.table = QtWidgets.QTableView(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(20, 160, 771, 450))
        self.table.horizontalHeader().setHidden(True)
        self.table.verticalHeader().setHidden(True)
        self.table.verticalHeader().setDefaultSectionSize(10)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.model = QtGui.QStandardItemModel(MainWindow)
        self.table.setModel(self.model)
        self.table.setHidden(True)
        self.bSettings = QtWidgets.QPushButton(self.centralwidget)
        self.bSettings.setGeometry(QtCore.QRect(716, 60, 76, 24))
        self.bHelp = QtWidgets.QPushButton(self.centralwidget)
        self.bHelp.setGeometry(QtCore.QRect(716, 30, 76, 24))
        self.bCSV = QtWidgets.QPushButton(self.centralwidget)
        self.bCSV.setGeometry(QtCore.QRect(716, 110, 76, 24))
        self.bStart = QtWidgets.QPushButton(self.centralwidget)
        self.bStart.setGeometry(QtCore.QRect(20, 66, 270, 68))
        self.bFile = QtWidgets.QPushButton(self.centralwidget)
        self.bFile.setGeometry(QtCore.QRect(20, 30, 270, 28))
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(306, 31, 410, 18))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setHidden(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 815, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.label = QtWidgets.QLabel('Select PCAP file to begin', MainWindow)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        fnt = QtGui.QFont('Calibri', 12)
        fnt.setBold(True)
        self.label.setFont(fnt)
        self.label.resize(400, 80)
        self.label.move(300, 50)
        self.label2 = QtWidgets.QLabel('NULL', MainWindow)
        self.label2.resize(200, 30)
        self.label2.move(306, 110)
        self.label2.setHidden(True)
        self.label3 = QtWidgets.QLabel('NULL', MainWindow)
        self.label3.resize(200, 30)
        self.label3.move(22, 132)
        self.label3.setHidden(True)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Network Alert Pipeline"))
        self.bSettings.setText(_translate("MainWindow", "Settings"))
        self.bSettings.clicked.connect(self.openSettings)
        self.bHelp.setText(_translate("MainWindow", "Help"))
        self.bHelp.clicked.connect(self.openHelp)
        self.bStart.setText(_translate("MainWindow", "Start"))
        self.bStart.clicked.connect(self.startProcess)
        self.bFile.setText(_translate("MainWindow", "Select File"))
        self.bFile.clicked.connect(self.openFile)
        self.bCSV.setText(_translate("MainWindow", "Display CSV"))
        self.bCSV.clicked.connect(self.openCSV)

    def openHelp(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("How to use the Network Alert Pipeline")
        dlg.setText("1. Click Select File and choose a valid PCAP file to analyze\n2. Click START\n\nClick Settings to customize various parameters")
        button = dlg.exec()

    def openSettings(self):
        if lock == False:
            print("OPEN SETTINGS MENU")
            SettingsWindow.show()

    def startProcess(self):
        global lock
        global importedfile
        if lock == False:
            if os.path.isfile(importedfile):
                lock=True
                print("STARTING WITH FILE:", importedfile)
                self.label.setText("Analyzing "+str(os.path.basename(importedfile)))
                self.progressBar.setHidden(False)
                
                basename = os.path.basename(importedfile)
                self.label2.setText("Converting PCAP to CSV...")
                output = ptc.convert(basename)
                self.updateBar(50)
                # Parameterization no longer needed
                # self.label2.setText("Parameterizing...")
                # output = param.parameterize(output)
                #self.updateBar(66)
                self.label2.setText("Normalizing...")
                output = norm.digest_file(output)
                self.updateBar(100)
                self.showCSV(output)
                self.label2.setText("SHOWING "+str(os.path.basename(output)))
                self.label.setText("DONE")
                self.progressBar.setProperty("value", 0)
                self.progressBar.setHidden(True)
                lock = False

                #output = MULTICLASS

                #THIS STUFF CAN TRIGGER AFTER PROCESS IS COMPLETE
                #self.progressBar.setHidden(True)
                #self.label.setText("Done!")
                #self.label2.setText(str(os.path.basename(OUTPUT FILE)))
                #self.showCSV(OUTPUT FILE)
            else:
                print("NO FILE SELECTED, cannot start process")

    def openFile(self):
        if lock == False:
            global importedfile
            importedfile = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select a PCAP file',directory=os.getcwd(), filter='PCAP File (*.pcap)')
            importedfile = importedfile[0]
            if os.path.isfile(importedfile):
                print("Imported file:", importedfile)
                self.label.setText("Click start to analyze!")
                self.label2.setText(os.path.basename(importedfile))
                self.label2.setHidden(False)
            else:
                print("No file or invalid file selected")
                self.label.setText("Select PCAP file to begin")
                self.label2.setHidden(True)

    def openCSV(self):
        if lock == False:
            importedCSV = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select a PCAP file',directory=os.getcwd(), filter='PCAP File (*.csv)')
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

class Ui_SettingsWindow(QtWidgets.QMainWindow):

    def setupUi(self, SettingsWindow):
        SettingsWindow.setFixedSize(600, 580)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.bHelp = QtWidgets.QPushButton(SettingsWindow)
        self.bHelp.setGeometry(QtCore.QRect(520, 10, 66, 24))
        self.bTrain = QtWidgets.QPushButton(SettingsWindow)
        self.bTrain.setGeometry(QtCore.QRect(420, 10, 80, 50))
        self.layers = QtWidgets.QSpinBox(SettingsWindow)
        self.layers.setRange(1, 10)
        self.layers.setValue(settings[0])
        self.layers.resize(50, 24)
        self.layers.move(50, 20)
        l = QtWidgets.QLabel('Layers:', SettingsWindow)
        l.resize(38, 24)
        l.move(10, 20)
        self.learn = QtWidgets.QSpinBox(SettingsWindow)
        self.learn.setRange(0, 1)
        self.learn.setValue(settings[7])
        self.learn.resize(50, 24)
        self.learn.move(202, 36)
        l = QtWidgets.QLabel('Learning Rate:', SettingsWindow)
        l.resize(70, 24)
        l.move(128, 36)
        self.type = QtWidgets.QComboBox(SettingsWindow)
        self.type.addItem("Binary")
        self.type.addItem("Multiclass")
        self.type.setCurrentIndex(settings[1])
        self.type.resize(80, 24)
        self.type.move(172, 10)
        l = QtWidgets.QLabel('Type:', SettingsWindow)
        l.resize(31, 24)
        l.move(140, 10)
        self.optimizer = QtWidgets.QComboBox(SettingsWindow)
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
        self.optimizer.resize(80, 24)
        self.optimizer.move(317, 36)
        l = QtWidgets.QLabel('Optimizer:', SettingsWindow)
        l.resize(80, 24)
        l.move(265, 36)
        self.epochs = QtWidgets.QSpinBox(SettingsWindow)
        self.epochs.setRange(10, 10000)
        self.epochs.setValue(settings[2])
        self.epochs.resize(70, 24)
        self.epochs.move(327, 10)
        l = QtWidgets.QLabel('Epochs:', SettingsWindow)
        l.resize(40, 24)
        l.move(286, 10)
        self.s14 = QtWidgets.QSpinBox(SettingsWindow)
        self.s14.setValue(settings[3])
        self.s14.setRange(0, 999999)
        self.s14.resize(68, 24)
        self.s14.move(515, 80)
        l = QtWidgets.QLabel('Input Size:', SettingsWindow)
        l.resize(50, 24)
        l.move(460, 80)

        #CONFIGURABLES FOR LAYERS
        l1 = "Layer Type:"
        l1l = 56
        l1p = 10
        w1 = 4
        w1s = ["Dense", "Flatten", "Conv1D", "MaxPooling1D"]
        w1l = 80
        w1p = 71
        l2 = "Neurons:"
        l2l = 50
        l2p = 175
        w2min = 0
        w2max = 999999
        w2l = 68
        w2p = 222
        l3 = "Activation:"
        l3l = 70
        l3p = 310
        w3 = 2
        w3s = ["ReLU", "Softmax"]
        w3l = 80
        w3p = 364
        #LAYER 1
        self.lt1 = QtWidgets.QLabel("Layer 1", SettingsWindow)
        self.lt1.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt1.resize(570, 16)
        self.lt1.move(10, 62)
        self.s11 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w1):
            self.s11.addItem(w1s[i])
        self.s11.setCurrentIndex(settings[4][0])
        self.s11.resize(w1l, 24)
        self.s11.move(w1p, 80)
        self.l11 = QtWidgets.QLabel(l1, SettingsWindow)
        self.l11.resize(l1l, 24)
        self.l11.move(l1p, 80)
        self.s12 = QtWidgets.QSpinBox(SettingsWindow)
        self.s12.setRange(w2min, w2max)
        self.s12.setValue(settings[5][0])
        self.s12.resize(w2l, 24)
        self.s12.move(w2p, 80)
        self.l12 = QtWidgets.QLabel(l2, SettingsWindow)
        self.l12.resize(l2l, 24)
        self.l12.move(l2p, 80)
        self.s13 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w3):
            self.s13.addItem(w3s[i])
        self.s13.setCurrentIndex(settings[6][0])
        self.s13.resize(w3l, 24)
        self.s13.move(w3p, 80)
        self.l13 = QtWidgets.QLabel(l3, SettingsWindow)
        self.l13.resize(l3l, 24)
        self.l13.move(l3p, 80)
        # LAYER 2
        self.lt2 = QtWidgets.QLabel("Layer 2", SettingsWindow)
        self.lt2.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt2.resize(570, 16)
        self.lt2.move(10, 112)
        self.s21 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w1):
            self.s21.addItem(w1s[i])
        self.s21.setCurrentIndex(settings[4][1])
        self.s21.resize(w1l, 24)
        self.s21.move(w1p, 130)
        self.l21 = QtWidgets.QLabel(l1, SettingsWindow)
        self.l21.resize(l1l, 24)
        self.l21.move(l1p, 130)
        self.s22 = QtWidgets.QSpinBox(SettingsWindow)
        self.s22.setRange(w2min, w2max)
        self.s22.setValue(settings[5][1])
        self.s22.resize(w2l, 24)
        self.s22.move(w2p, 130)
        self.l22 = QtWidgets.QLabel(l2, SettingsWindow)
        self.l22.resize(l2l, 24)
        self.l22.move(l2p, 130)
        self.s23 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w3):
            self.s23.addItem(w3s[i])
        self.s23.setCurrentIndex(settings[6][1])
        self.s23.resize(w3l, 24)
        self.s23.move(w3p, 130)
        self.l23 = QtWidgets.QLabel(l3, SettingsWindow)
        self.l23.resize(l3l, 24)
        self.l23.move(l3p, 130)
        # LAYER 3
        self.lt3 = QtWidgets.QLabel("Layer 3", SettingsWindow)
        self.lt3.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt3.resize(570, 16)
        self.lt3.move(10, 162)
        self.s31 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w1):
            self.s31.addItem(w1s[i])
        self.s31.setCurrentIndex(settings[4][2])
        self.s31.resize(w1l, 24)
        self.s31.move(w1p, 180)
        self.l31 = QtWidgets.QLabel(l1, SettingsWindow)
        self.l31.resize(l1l, 24)
        self.l31.move(l1p, 180)
        self.s32 = QtWidgets.QSpinBox(SettingsWindow)
        self.s32.setRange(w2min, w2max)
        self.s32.setValue(settings[5][2])
        self.s32.resize(w2l, 24)
        self.s32.move(w2p, 180)
        self.l32 = QtWidgets.QLabel(l2, SettingsWindow)
        self.l32.resize(l2l, 24)
        self.l32.move(l2p, 180)
        self.s33 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w3):
            self.s33.addItem(w3s[i])
        self.s33.setCurrentIndex(settings[6][2])
        self.s33.resize(w3l, 24)
        self.s33.move(w3p, 180)
        self.l33 = QtWidgets.QLabel(l3, SettingsWindow)
        self.l33.resize(l3l, 24)
        self.l33.move(l3p, 180)
        # LAYER 4
        self.lt4 = QtWidgets.QLabel("Layer 4", SettingsWindow)
        self.lt4.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt4.resize(570, 16)
        self.lt4.move(10, 212)
        self.s41 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w1):
            self.s41.addItem(w1s[i])
        self.s41.setCurrentIndex(settings[4][3])
        self.s41.resize(w1l, 24)
        self.s41.move(w1p, 230)
        self.l41 = QtWidgets.QLabel(l1, SettingsWindow)
        self.l41.resize(l1l, 24)
        self.l41.move(l1p, 230)
        self.s42 = QtWidgets.QSpinBox(SettingsWindow)
        self.s42.setRange(w2min, w2max)
        self.s42.setValue(settings[5][3])
        self.s42.resize(w2l, 24)
        self.s42.move(w2p, 230)
        self.l42 = QtWidgets.QLabel(l2, SettingsWindow)
        self.l42.resize(l2l, 24)
        self.l42.move(l2p, 230)
        self.s43 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w3):
            self.s43.addItem(w3s[i])
        self.s43.setCurrentIndex(settings[6][3])
        self.s43.resize(w3l, 24)
        self.s43.move(w3p, 230)
        self.l43 = QtWidgets.QLabel(l3, SettingsWindow)
        self.l43.resize(l3l, 24)
        self.l43.move(l3p, 230)
        # LAYER 5
        self.lt5 = QtWidgets.QLabel("Layer 5", SettingsWindow)
        self.lt5.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt5.resize(570, 16)
        self.lt5.move(10, 262)
        self.s51 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w1):
            self.s51.addItem(w1s[i])
        self.s51.setCurrentIndex(settings[4][4])
        self.s51.resize(w1l, 24)
        self.s51.move(w1p, 280)
        self.l51 = QtWidgets.QLabel(l1, SettingsWindow)
        self.l51.resize(l1l, 24)
        self.l51.move(l1p, 280)
        self.s52 = QtWidgets.QSpinBox(SettingsWindow)
        self.s52.setRange(w2min, w2max)
        self.s52.setValue(settings[5][4])
        self.s52.resize(w2l, 24)
        self.s52.move(w2p, 280)
        self.l52 = QtWidgets.QLabel(l2, SettingsWindow)
        self.l52.resize(l2l, 24)
        self.l52.move(l2p, 280)
        self.s53 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w3):
            self.s53.addItem(w3s[i])
        self.s53.setCurrentIndex(settings[6][4])
        self.s53.resize(w3l, 24)
        self.s53.move(w3p, 280)
        self.l53 = QtWidgets.QLabel(l3, SettingsWindow)
        self.l53.resize(l3l, 24)
        self.l53.move(l3p, 280)
        # LAYER 6
        self.lt6 = QtWidgets.QLabel("Layer 6", SettingsWindow)
        self.lt6.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt6.resize(570, 16)
        self.lt6.move(10, 312)
        self.s61 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w1):
            self.s61.addItem(w1s[i])
        self.s61.setCurrentIndex(settings[4][5])
        self.s61.resize(w1l, 24)
        self.s61.move(w1p, 330)
        self.l61 = QtWidgets.QLabel(l1, SettingsWindow)
        self.l61.resize(l1l, 24)
        self.l61.move(l1p, 330)
        self.s62 = QtWidgets.QSpinBox(SettingsWindow)
        self.s62.setRange(w2min, w2max)
        self.s62.setValue(settings[5][5])
        self.s62.resize(w2l, 24)
        self.s62.move(w2p, 330)
        self.l62 = QtWidgets.QLabel(l2, SettingsWindow)
        self.l62.resize(l2l, 24)
        self.l62.move(l2p, 330)
        self.s63 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w3):
            self.s63.addItem(w3s[i])
        self.s63.setCurrentIndex(settings[6][5])
        self.s63.resize(w3l, 24)
        self.s63.move(w3p, 330)
        self.l63 = QtWidgets.QLabel(l3, SettingsWindow)
        self.l63.resize(l3l, 24)
        self.l63.move(l3p, 330)
        # LAYER 7
        self.lt7 = QtWidgets.QLabel("Layer 7", SettingsWindow)
        self.lt7.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt7.resize(570, 16)
        self.lt7.move(10, 362)
        self.s71 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w1):
            self.s71.addItem(w1s[i])
        self.s71.setCurrentIndex(settings[4][6])
        self.s71.resize(w1l, 24)
        self.s71.move(w1p, 380)
        self.l71 = QtWidgets.QLabel(l1, SettingsWindow)
        self.l71.resize(l1l, 24)
        self.l71.move(l1p, 380)
        self.s72 = QtWidgets.QSpinBox(SettingsWindow)
        self.s72.setRange(w2min, w2max)
        self.s72.setValue(settings[5][6])
        self.s72.resize(w2l, 24)
        self.s72.move(w2p, 380)
        self.l72 = QtWidgets.QLabel(l2, SettingsWindow)
        self.l72.resize(l2l, 24)
        self.l72.move(l2p, 380)
        self.s73 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w3):
            self.s73.addItem(w3s[i])
        self.s73.setCurrentIndex(settings[6][6])
        self.s73.resize(w3l, 24)
        self.s73.move(w3p, 380)
        self.l73 = QtWidgets.QLabel(l3, SettingsWindow)
        self.l73.resize(l3l, 24)
        self.l73.move(l3p, 380)
        # LAYER 8
        self.lt8 = QtWidgets.QLabel("Layer 8", SettingsWindow)
        self.lt8.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt8.resize(570, 16)
        self.lt8.move(10, 412)
        self.s81 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w1):
            self.s81.addItem(w1s[i])
        self.s81.setCurrentIndex(settings[4][7])
        self.s81.resize(w1l, 24)
        self.s81.move(w1p, 430)
        self.l81 = QtWidgets.QLabel(l1, SettingsWindow)
        self.l81.resize(l1l, 24)
        self.l81.move(l1p, 430)
        self.s82 = QtWidgets.QSpinBox(SettingsWindow)
        self.s82.setRange(w2min, w2max)
        self.s82.setValue(settings[5][7])
        self.s82.resize(w2l, 24)
        self.s82.move(w2p, 430)
        self.l82 = QtWidgets.QLabel(l2, SettingsWindow)
        self.l82.resize(l2l, 24)
        self.l82.move(l2p, 430)
        self.s83 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w3):
            self.s83.addItem(w3s[i])
        self.s83.setCurrentIndex(settings[6][7])
        self.s83.resize(w3l, 24)
        self.s83.move(w3p, 430)
        self.l83 = QtWidgets.QLabel(l3, SettingsWindow)
        self.l83.resize(l3l, 24)
        self.l83.move(l3p, 430)
        # LAYER 9
        self.lt9 = QtWidgets.QLabel("Layer 9", SettingsWindow)
        self.lt9.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt9.resize(570, 16)
        self.lt9.move(10, 462)
        self.s91 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w1):
            self.s91.addItem(w1s[i])
        self.s91.setCurrentIndex(settings[4][8])
        self.s91.resize(w1l, 24)
        self.s91.move(w1p, 480)
        self.l91 = QtWidgets.QLabel(l1, SettingsWindow)
        self.l91.resize(l1l, 24)
        self.l91.move(l1p, 480)
        self.s92 = QtWidgets.QSpinBox(SettingsWindow)
        self.s92.setRange(w2min, w2max)
        self.s92.setValue(settings[5][8])
        self.s92.resize(w2l, 24)
        self.s92.move(w2p, 480)
        self.l92 = QtWidgets.QLabel(l2, SettingsWindow)
        self.l92.resize(l2l, 24)
        self.l92.move(l2p, 480)
        self.s93 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w3):
            self.s93.addItem(w3s[i])
        self.s93.setCurrentIndex(settings[6][8])
        self.s93.resize(w3l, 24)
        self.s93.move(w3p, 480)
        self.l93 = QtWidgets.QLabel(l3, SettingsWindow)
        self.l93.resize(l3l, 24)
        self.l93.move(l3p, 480)
        # LAYER 10
        self.lt0 = QtWidgets.QLabel("Layer 10", SettingsWindow)
        self.lt0.setStyleSheet("border-top-width: 1px; border-top-style: solid; border-radius: 0px;")
        self.lt0.resize(570, 16)
        self.lt0.move(10, 512)
        self.s01 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w1):
            self.s01.addItem(w1s[i])
        self.s01.setCurrentIndex(settings[4][9])
        self.s01.resize(w1l, 24)
        self.s01.move(w1p, 530)
        self.l01 = QtWidgets.QLabel(l1, SettingsWindow)
        self.l01.resize(l1l, 24)
        self.l01.move(l1p, 530)
        self.s02 = QtWidgets.QSpinBox(SettingsWindow)
        self.s02.setRange(w2min, w2max)
        self.s02.setValue(settings[5][9])
        self.s02.resize(w2l, 24)
        self.s02.move(w2p, 530)
        self.l02 = QtWidgets.QLabel(l2, SettingsWindow)
        self.l02.resize(l2l, 24)
        self.l02.move(l2p, 530)
        self.s03 = QtWidgets.QComboBox(SettingsWindow)
        for i in range(0, w3):
            self.s03.addItem(w3s[i])
        self.s03.setCurrentIndex(settings[6][9])
        self.s03.resize(w3l, 24)
        self.s03.move(w3p, 530)
        self.l03 = QtWidgets.QLabel(l3, SettingsWindow)
        self.l03.resize(l3l, 24)
        self.l03.move(l3p, 530)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, SettingsWindow):
        global settings
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Pipeline Settings"))
        self.revealLayers(settings[0])
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

    def openFile(self):
        if lock == False:
            importedfile1 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select TRAINING data',directory=os.getcwd(), filter='CSV File (*.csv)')
            importedfile2 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select TESTING data',directory=os.getcwd(), filter='CSV File (*.csv)')
            importedfile3 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select VALIDATION data',directory=os.getcwd(), filter='CSV File (*.csv)')
            importedfile1 = importedfile1[0]
            importedfile2 = importedfile2[0]
            importedfile3 = importedfile3[0]
            if os.path.isfile(importedfile):
                print("CREATING TRAINING DATA")
                #CREATE TRAINING DATA FROM importedfile1 2 and 3
            else:
                print("No file(s) or invalid file(s) selected")

    def revealLayers(self, l):
        self.lt2.setHidden(True)
        self.l21.setHidden(True)
        self.l22.setHidden(True)
        self.l23.setHidden(True)
        self.s21.setHidden(True)
        self.s22.setHidden(True)
        self.s23.setHidden(True)
        self.lt3.setHidden(True)
        self.l31.setHidden(True)
        self.l32.setHidden(True)
        self.l33.setHidden(True)
        self.s31.setHidden(True)
        self.s32.setHidden(True)
        self.s33.setHidden(True)
        self.lt4.setHidden(True)
        self.l41.setHidden(True)
        self.l42.setHidden(True)
        self.l43.setHidden(True)
        self.s41.setHidden(True)
        self.s42.setHidden(True)
        self.s43.setHidden(True)
        self.lt5.setHidden(True)
        self.l51.setHidden(True)
        self.l52.setHidden(True)
        self.l53.setHidden(True)
        self.s51.setHidden(True)
        self.s52.setHidden(True)
        self.s53.setHidden(True)
        self.lt6.setHidden(True)
        self.l61.setHidden(True)
        self.l62.setHidden(True)
        self.l63.setHidden(True)
        self.s61.setHidden(True)
        self.s62.setHidden(True)
        self.s63.setHidden(True)
        self.lt7.setHidden(True)
        self.l71.setHidden(True)
        self.l72.setHidden(True)
        self.l73.setHidden(True)
        self.s71.setHidden(True)
        self.s72.setHidden(True)
        self.s73.setHidden(True)
        self.lt8.setHidden(True)
        self.l81.setHidden(True)
        self.l82.setHidden(True)
        self.l83.setHidden(True)
        self.s81.setHidden(True)
        self.s82.setHidden(True)
        self.s83.setHidden(True)
        self.lt9.setHidden(True)
        self.l91.setHidden(True)
        self.l92.setHidden(True)
        self.l93.setHidden(True)
        self.s91.setHidden(True)
        self.s92.setHidden(True)
        self.s93.setHidden(True)
        self.lt0.setHidden(True)
        self.l01.setHidden(True)
        self.l02.setHidden(True)
        self.l03.setHidden(True)
        self.s01.setHidden(True)
        self.s02.setHidden(True)
        self.s03.setHidden(True)
        if l>=2:
            self.lt2.setHidden(False)
            self.l21.setHidden(False)
            self.l22.setHidden(False)
            self.l23.setHidden(False)
            self.s21.setHidden(False)
            self.s22.setHidden(False)
            self.s23.setHidden(False)
        if l>=3:
            self.lt3.setHidden(False)
            self.l31.setHidden(False)
            self.l32.setHidden(False)
            self.l33.setHidden(False)
            self.s31.setHidden(False)
            self.s32.setHidden(False)
            self.s33.setHidden(False)
        if l>=4:
            self.lt4.setHidden(False)
            self.l41.setHidden(False)
            self.l42.setHidden(False)
            self.l43.setHidden(False)
            self.s41.setHidden(False)
            self.s42.setHidden(False)
            self.s43.setHidden(False)
        if l>=5:
            self.lt5.setHidden(False)
            self.l51.setHidden(False)
            self.l52.setHidden(False)
            self.l53.setHidden(False)
            self.s51.setHidden(False)
            self.s52.setHidden(False)
            self.s53.setHidden(False)
        if l>=6:
            self.lt6.setHidden(False)
            self.l61.setHidden(False)
            self.l62.setHidden(False)
            self.l63.setHidden(False)
            self.s61.setHidden(False)
            self.s62.setHidden(False)
            self.s63.setHidden(False)
        if l>=7:
            self.lt7.setHidden(False)
            self.l71.setHidden(False)
            self.l72.setHidden(False)
            self.l73.setHidden(False)
            self.s71.setHidden(False)
            self.s72.setHidden(False)
            self.s73.setHidden(False)
        if l>=8:
            self.lt8.setHidden(False)
            self.l81.setHidden(False)
            self.l82.setHidden(False)
            self.l83.setHidden(False)
            self.s81.setHidden(False)
            self.s82.setHidden(False)
            self.s83.setHidden(False)
        if l>=9:
            self.lt9.setHidden(False)
            self.l91.setHidden(False)
            self.l92.setHidden(False)
            self.l93.setHidden(False)
            self.s91.setHidden(False)
            self.s92.setHidden(False)
            self.s93.setHidden(False)
        if l==10:
            self.lt0.setHidden(False)
            self.l01.setHidden(False)
            self.l02.setHidden(False)
            self.l03.setHidden(False)
            self.s01.setHidden(False)
            self.s02.setHidden(False)
            self.s03.setHidden(False)

    def save0(self):
        global settings
        settings[0] = self.layers.value()
        self.revealLayers(settings[0])
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
        dlg.setText("WRITE THIS")           #NEED TO WRITE HELP TEXT
        button = dlg.exec()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    SettingsWindow = QtWidgets.QMainWindow()
    Sui = Ui_SettingsWindow()
    Sui.setupUi(SettingsWindow)
    MainWindow.show()
    sys.exit(app.exec_())