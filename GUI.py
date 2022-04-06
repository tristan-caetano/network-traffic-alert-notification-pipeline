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
import h5py
import configparser

#  --------------- Components  ---------------
import pcap_to_csv as ptc
# import train_test_creator as ttc
# import normalize as norm
# import data_trimmer as dt
# import parameterizer as param
# import parameterize_mal as pmal
import multiclass_classification as multi

#  ---------------  Global Variables  ---------------
importedfile = ""
importedmodel = ""
settings = 0
lock = False

#  ---------------  User Config  ---------------
config = configparser.ConfigParser()
#If config.ini does not exist, create it
if not os.path.exists('config.ini'):
    config['settings'] = {'type': '0'}
    config.write(open('config.ini', 'w'))
else:
    config.read('config.ini')
    settings = int(config.get('settings', 'type'))

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

        #Initialize buttons, labels, etc
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
        self.label.resize(700, 80)
        self.label.move(88, 60)
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
        self.table.setFont(QtGui.QFont('Times', 12))
        self.model = QtGui.QStandardItemModel(self)
        self.table.setModel(self.model)
        self.table.setHidden(True)

        #Initialize animations
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

        #Finish setting up GUI
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

    #Open help menu
    def openHelp(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("How to use the Network Alert Pipeline")
        dlg.setText("1. Click Select File and choose a valid PCAP file to analyze\n2. Click START\n\nClick Settings to change algorithm type and create new training data")
        dlg.setStyleSheet("QPushButton {border-radius: 2px; width: 60px; height: 20px;}")
        button = dlg.exec()

    #Open settings menu
    def openSettings(self):
        global lock
        if lock == False:
            lock = True
            print("OPEN SETTINGS MENU")
            SettingsWindow.show(Sui)

    #Start main algorithm with importedfile
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

                # PCAP to CSV converter
                converted = ptc.convert(basename, self)
                predicted = multi.saved_weights(converted, 'my_model.h5', self)

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
                self.updateMessage(self, 100, "Displaying CSV in GUI")
                self.showCSV(predicted)
                lock = False
            else:
                print("NO FILE SELECTED, cannot start process")

    #Open file dialog for main PCAP file
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

    #Drag and drop functionality
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

    #Selected PCAP file is accepted as valid
    def acceptImport(self):
        print("Imported file:", importedfile)
        self.bStart.setHidden(False)
        self.label2.setText(os.path.basename(importedfile))
        self.anim1.start()
        self.anim2.start()
        self.anim3.start()
        self.anim4.start()

    #Open file dialog for CSV display
    def openCSV(self):
        if lock == False:
            importedCSV = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select a CSV file',directory=os.getcwd(), filter='CSV File (*.csv)')
            importedCSV = importedCSV[0]
            if os.path.isfile(importedCSV):
                print("Imported CSV:", importedCSV)
                self.showCSV(importedCSV)
            else:
                print("No file or invalid file selected")

    #Updates progress bar with a new value
    def updateBar(self, goto):
        cur = self.progressBar.value()
        while cur < goto:
            cur = cur + math.ceil((goto - cur) / 10)
            self.progressBar.setProperty("value", cur)
            time.sleep(0.03)

    #Display CSV in table
    def showCSV(self, filename):
        self.model.clear()
        with open(filename, 'r') as f:
            try:
                for row in csv.reader(f):
                    items = [
                        QtGui.QStandardItem(field)
                        for field in row
                    ]
            
                    self.model.appendRow(items)
                    self.table.setHidden(False)
                    self.label3.setText(os.path.basename(filename)+":")
                    self.label3.setHidden(False)

                        # TODO: Print to GUI instead of terminal
            except: print("Error")

class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        #Initialize buttons, labels, etc
        self.setFixedSize(400, 170)
        self.setStyleSheet(style)
        fnt = QtGui.QFont('Georgia', 12)
        self.bHelp = QtWidgets.QPushButton(self)
        self.bHelp.setGeometry(QtCore.QRect(280, 10, 100, 36))
        self.bHelp.setFont(fnt)
        self.bTrain = QtWidgets.QPushButton(self)
        self.bTrain.setGeometry(QtCore.QRect(220, 100, 160, 36))
        self.bTrain.setFont(fnt)
        self.bCreate = QtWidgets.QPushButton(self)
        self.bCreate.setGeometry(QtCore.QRect(220, 60, 160, 36))
        self.bCreate.setFont(fnt)
        self.bModel = QtWidgets.QPushButton(self)
        self.bModel.setGeometry(QtCore.QRect(20, 60, 180, 76))
        self.bModel.setFont(fnt)
        self.type = QtWidgets.QComboBox(self)
        self.type.addItem("Binary")
        self.type.addItem("Multiclass")
        self.type.setCurrentIndex(settings)
        self.type.resize(110, 36)
        self.type.move(150, 10)
        self.type.setFont(fnt)
        l = QtWidgets.QLabel('Algorithm Type:', self)
        l.resize(120, 36)
        l.move(20, 10)
        l.setFont(fnt)
        l = QtWidgets.QLabel('Network Traffic Alert Notification Pipeline - Version: 1.2.0', self)
        l.resize(380, 30)
        l.move(20, 146)
        l.setFont(QtGui.QFont('Georgia', 10))

        #Finish setting up GUI
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        global settings
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SettingsWindow", "Pipeline Settings"))
        self.bHelp.setText(_translate("SettingsWindow", "Help"))
        self.bHelp.clicked.connect(self.openHelp)
        self.bCreate.setText(_translate("SettingsWindow", "Create Training Data"))
        self.bCreate.clicked.connect(self.openFile0)
        self.bTrain.setText(_translate("SettingsWindow", "Retrain Algorithm"))
        self.bTrain.clicked.connect(self.openFile)
        self.bModel.setText(_translate("SettingsWindow", "Import Model"))
        self.bModel.clicked.connect(self.openModel)
        self.type.currentIndexChanged.connect(self.save)

    #User closes settings menu
    def closeEvent(self, event):
        global lock
        lock = False

    #Import 3 CSV files to create new training data
    def openFile0(self):
        importedfile1 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select TRAINING Data',directory=os.getcwd(), filter='CSV File (*.csv)')
        importedfile2 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select TESTING Data',directory=os.getcwd(), filter='CSV File (*.csv)')
        importedfile3 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select VALIDATION Data',directory=os.getcwd(), filter='CSV File (*.csv)')
        importedfile1 = importedfile1[0]
        importedfile2 = importedfile2[0]
        importedfile3 = importedfile3[0]
        if os.path.isfile(importedfile1) & os.path.isfile(importedfile2) & os.path.isfile(importedfile3):
            print("RETRAINING ALGORITHM")
                        # TODO: retraining algorithm FROM importedfile1 2 and 3
        else:
            print("No file(s) or invalid file(s) selected")

    #Import a CSV files to retrain algorithm
    def openFile(self):
        importedfile0 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select algorithm model',
                                                              directory=os.getcwd(), filter='CSV File (*.csv)')
        importedfile0 = importedfile0[0]
        if os.path.isfile(importedfile0):
            #Show string input dialog for model name
            modelname, done1 = QtWidgets.QInputDialog.getText(self, 'Set Model Name', 'Enter model name:')
            print("CREATING TRAINING DATA, model name "+modelname)
                        # TODO: CREATE TRAINING DATA from importedfile0
        else:
            print("No file or invalid file selected")

    #Import h5 model file
    def openModel(self):
        importedfile0 = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select unmodified dataset', directory=os.getcwd(), filter='HDF5 File (*.h5)')
        importedfile0 = importedfile0[0]
        if os.path.isfile(importedfile0):
            global importedmodel
            importedmodel = importedfile0
            print("IMPORTED NEW MODEL")
        else:
            print("No file or invalid file selected")

    #Save settings to ini file
    def save(self):
        global settings
        settings = self.type.currentIndex()
        config['settings'] = {'type': str(settings)}
        config.write(open('config.ini', 'w'))
        print("SETTINGS SAVED:", settings)

    #Open help menu
    def openHelp(self):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("Settings Help")
        dlg.setText("-Algorithm type-\nBINARY: Relies on two classes.\nMULTICLASS: Can rely on more than two classes.\n\n-Training Data-\nTo create new training data, click Create Training Data and select csv files for training data, testing data, and validation data.\nTo train the algorithm with new data, click Retrain Algorithm and choose the newly created training data")
        dlg.setStyleSheet("QPushButton {border-radius: 2px; width: 60px; height: 20px;}")
        button = dlg.exec()

    #Update label text
    def updateMessage(self, progress, message):
        self.label.setText(message)
        self.updateBar(progress)

#Driver code
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    Sui = SettingsWindow()
    MainWindow.show(ui)
    sys.exit(app.exec_())