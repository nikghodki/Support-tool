import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import clientdebuglibui
import os,time,csv
import pandas._libs.tslibs.base

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(400, 200, 900, 500)
        self.setWindowTitle('Client Debug Tool')
        oImage = QImage("images.jpeg")
        sImage = oImage.scaled(QSize(900,500))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(sImage))                        
        self.setPalette(palette)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    global debugfolder

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QHBoxLayout(self)
        
       
        # Initialize tab screen
        self.tabsup = QTabWidget()
        self.tabsdown = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        #Initializing all variables
        self.tabsdown.resize(10,10)
        self.filepath= None
        self.a= None
        self.b= None
        self.api_output= None
        self.flag=None
        self.api_name= QLabel('')
        self.pixmap = QPixmap('icon.png')
        self.pixmap3 = QPixmap('icon2.png')
        self.labellogo=QLabel(self)
        self.labellogo.setAlignment(Qt.AlignCenter)
        self.labelicon=QLabel(self)
        self.labellogo.setPixmap(self.pixmap)
        self.msgbox = QMessageBox(parent)
        self.msgbox.setIcon(QMessageBox.Critical)
        self.msgbox.setText('Please upload the file')
        self.labelicon.setPixmap(self.pixmap3)
        
        # Add tabs
        self.tabsup.addTab(self.tab1,"Client Details")
        self.tabsdown.addTab(self.tab4,"Main Page")
        self.tabsup.addTab(self.tab2,"Client Issues")
        self.tabsup.addTab(self.tab3,"Client APIs")
        self.tabsdown.setTabPosition(QTabWidget.South)
       
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.button1 = QPushButton("Show Client Specifics")
        self.tab1.layout.addWidget(self.button1)
        self.textEdit1 = QTextEdit(self)
        self.textEdit1.resize(500,500)
        self.tab1.layout.addWidget(self.textEdit1)
        self.tab1.setLayout(self.tab1.layout)



        # Create Second Tab
        self.tab2.layout = QGridLayout(self)
        self.buttonchoosefile= QPushButton("Choose File")
        self.label1=QLabel('Select the client debug package')
        self.buttoncheckerror = QPushButton("Check for errors in logs")
        self.buttonexport = QPushButton("Export")      
        self.tab2.layout.addWidget(self.buttoncheckerror,1,0)
        #self.tab2.layout.addWidget(self.buttonexport,3,0)    
        self.buttonchoosefile.clicked.connect(self.fileupload)
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().setStretchLastSection(True) 
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.tab2.layout.addWidget(self.tableWidget,2,0)
        self.tab2.setLayout(self.tab2.layout)
        self.button1.clicked.connect(self.processfile)
        self.buttoncheckerror.clicked.connect(self.checkerrors)
        #self.buttonexport.clicked.connect(self.export)
        


        # Create 3rd Tab
        self.tab3.layout=QVBoxLayout(self)
        self.tab3.layout1 = QGridLayout(self)
        self.tab3.layout2=QHBoxLayout(self)
        self.buttonapi = QPushButton("Check All APIs")
        self.buttonbranding = QPushButton("Check nsbranding")
        self.buttonexceptions = QPushButton("Check nsexceptions")
        self.buttonbypass = QPushButton("Check nsbypass")
        self.buttonnsuser = QPushButton("Check nsuser")
        self.buttonnssteering = QPushButton("Check nssteering")
        self.labelapi = QLabel("Check the output of all the client\nAPIs if returning expected output")
        self.tab3.layout1.addWidget(self.buttonbranding,1,0)
        self.tab3.layout1.addWidget(self.buttonnssteering,1,1)
        self.tab3.layout1.addWidget(self.buttonexceptions,1,2)
        self.tab3.layout1.addWidget(self.buttonbypass,2,0)
        self.tab3.layout1.addWidget(self.buttonnsuser,2,1)
        self.tab3.layout1.addWidget(self.buttonapi,2,2)
        self.textEdit3 = QTextEdit(self)
        self.textEdit3.resize(100,100)
        self.tab3.layout2.addWidget(self.textEdit3)
        self.tab3.layout.addLayout(self.tab3.layout1)
        self.tab3.layout.addLayout(self.tab3.layout2)
        self.tab3.setLayout(self.tab3.layout)
        self.buttonapi.clicked.connect(self.apioutput)
        self.buttonbranding.clicked.connect(self.apinsbranding)
        self.buttonexceptions.clicked.connect(self.apiexception)
        self.buttonbypass.clicked.connect(self.apinsbypass)
        self.buttonnsuser.clicked.connect(self.apinsuser)
        self.buttonnssteering.clicked.connect(self.apinssteering)






        #Create Tab 4
        self.tab4.layout = QVBoxLayout(self)
        self.labelwelcome=QLabel("Welcome to client Debug tool")
        self.tab4.layout.addWidget(self.labelwelcome,0)
        self.tab4.layout.addWidget(self.labelicon,0)
        self.tab4.layout.addWidget(self.label1,0)
        self.tab4.layout.addWidget(self.buttonchoosefile,0)
        self.tab4.setLayout(self.tab4.layout)



        # Add tabs to widget
        self.layout.addWidget(self.tabsdown)
        self.layout.addWidget(self.tabsup,1)
        
        #self.setLayout(self.layout)

    def fileupload(self):
        fname = QFileDialog.getOpenFileName(None, filter="Zip (*.zip)")
        self.filepath=clientdebuglibui.unzipfolder(fname[0])

    def apioutput(self):
        if self.filepath != None:
            self.textEdit3.setText('')
            self.api_output=clientdebuglibui.apicheck(self.filepath)
            if isinstance(self.api_output,dict):
                for key,value in self.api_output.items():
                    self.textEdit3.append(str(key))
                    self.textEdit3.append(str(value)+'\n\n*********************************************************\n\n')
            else:
                self.textEdit3.append('nsbranding file is not present')

        else:
            self.msgbox.critical(self, "Logs not uploaded", "Please upload client logs")
    def apinsbranding(self):
        if self.filepath != None:
            self.textEdit3.setText(str(clientdebuglibui.apinsbrandingout(self.filepath)))
        else:
            self.msgbox.critical(self, "Logs not uploaded", "Please upload client logs")
    def apinssteering(self):
        if self.filepath != None:
            self.textEdit3.setText(str(clientdebuglibui.apisteeringout(self.filepath)))
        else:
            self.msgbox.critical(self, "Logs not uploaded", "Please upload client logs")
    def apinsbypass(self):
        if self.filepath != None:
            self.textEdit3.setText(str(clientdebuglibui.apibypassout(self.filepath)))
        else:
            self.msgbox.critical(self, "Logs not uploaded", "Please upload client logs")
    def apiexception(self):
        if self.filepath != None:
            self.textEdit3.setText(str(clientdebuglibui.apiexceptionout(self.filepath)))
        else:
            self.msgbox.critical(self, "Logs not uploaded", "Please upload client logs")
    def apinsuser(self):
        if self.filepath != None:
            self.textEdit3.setText(str(clientdebuglibui.apinsuserout(self.filepath)))
        else:
            self.msgbox.critical(self, "Logs not uploaded", "Please upload client logs")


    def checkerrors(self):
        if self.filepath != None:
            self.erroroutput={}
            self.erroroutput=clientdebuglibui.checkerrorlogs(self.filepath)
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(len(self.erroroutput))
            self.columnLabels=["Error Log Line","Error","Remediation"]
            self.tableWidget.setHorizontalHeaderLabels(self.columnLabels)
            i=0
            for k1,v1 in self.erroroutput.items():
                self.tableWidget.setItem(i,0, QTableWidgetItem(str(k1)))
                for k2,v2 in v1.items():
                    self.tableWidget.setItem(i,1, QTableWidgetItem(str(k2)))
                    self.tableWidget.setItem(i,2, QTableWidgetItem(str(v2)))
                    i+=1



                
                
        else:
            self.msgbox.critical(self, "Logs not uploaded", "Please upload client logs")
            
    
    def export(self):
        outerror={}
        temp1=[]
        temp=[]
        if self.filepath != None:
            with open('~/Downloads/errors.csv','w') as f:
                write=csv.writer(f)
                write.writerow(["Error Log Line","Error","Remediation"])
                outerror=clientdebuglibui.checkerrorlogs(self.filepath)
                for k1,v1 in outerror.items():
                    temp.append(str(k1))
                    for k2,v2 in v1.items():
                        temp.append(str(k2))
                        temp.append(str(v2))
                    temp1.append(temp)
                    temp=[]
                for line in temp1:
                    write.writerow(line)
        else:
            self.msgbox.critical(self, "Logs not uploaded", "Please upload client logs")
            


    
    def processfile(self):
        if self.filepath != None:
            self.a=clientdebuglibui.client_specifics(self.filepath)
            self.textEdit1.setText(self.a)
        else:
            self.msgbox.critical(self, "Logs not uploaded", "Please upload client logs")
            
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
