import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os,time,csv
import json, requests

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 200, 400, 300)
        self.setWindowTitle('User Management Delete/create Users')
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

        self.api_name= QLabel('')
        self.pixmap = QPixmap('banner.png')
        self.pixmap3 = QPixmap('banner.png')
        self.labellogo=QLabel(self)
        self.labellogo.setAlignment(Qt.AlignCenter)
        self.labelicon=QLabel(self)
        self.labellogo.setPixmap(self.pixmap)
        self.msgbox = QMessageBox(parent)
        self.msgbox.setIcon(QMessageBox.Critical)
        self.msgbox.setText('Please add UserInfo_URL')
        self.labelicon.setPixmap(self.pixmap3)
        
        # Add tabs
        self.tabsup.addTab(self.tab1,"ADImporter")
        self.tabsup.addTab(self.tab2,"SCIM")

        # Create first tab
        self.tab1.layout = QGridLayout(self)
        self.adprogress = QProgressBar(self)
        self.adprogress.setValue(0)
        self.adprogress.setMaximum(100)
        self.textad=''
        self.adcreateusers = QPushButton("Create Users")
        self.getuserinfourlad = QPushButton("Get UserInfo_URL")
        self.addeleteusers = QPushButton("Delete Users")
        self.adcreategroups = QPushButton("Create Groups")
        self.addeletegroups = QPushButton("Delete Groups")
        self.tab1.layout.addWidget(self.getuserinfourlad,0,0)
        self.tab1.layout.addWidget(self.adcreateusers,1,0)
        self.tab1.layout.addWidget(self.addeleteusers,2,0)
        self.tab1.layout.addWidget(self.adcreategroups,1,1)
        self.tab1.layout.addWidget(self.addeletegroups,2,1)
        self.tab1.layout.addWidget(self.adprogress,4,0)
        self.getuserinfourlad.clicked.connect(self.adgetuserinfourl)
        self.adcreateusers.clicked.connect(self.adcreateuser)
        self.addeleteusers.clicked.connect(self.addeleteuser)
        self.adcreategroups.clicked.connect(self.adcreategroup)
        self.addeletegroups.clicked.connect(self.addeletegroup)
        self.tab1.setLayout(self.tab1.layout)



        # Create Second Tab
        self.tab2.layout = QGridLayout(self)
        self.scimprogress = QProgressBar(self)
        self.scimprogress.setValue(0)
        self.scimprogress.setMaximum(100)
        self.textscim=''
        self.getuserinfourlscim = QPushButton("Get UserInfo_URL")
        self.scimcreateusers = QPushButton("Create Users")
        self.scimdeleteusers = QPushButton("Delete Users")
        self.scimcreategroups = QPushButton("Create Groups")
        self.scimdeletegroups = QPushButton("Delete Groups")
        self.tab2.layout.addWidget(self.scimcreateusers,1,0)
        self.tab2.layout.addWidget(self.getuserinfourlscim,0,0)
        self.tab2.layout.addWidget(self.scimdeleteusers,2,0)
        self.tab2.layout.addWidget(self.scimcreategroups,0,1)
        self.tab2.layout.addWidget(self.scimdeletegroups,1,1)
        self.tab2.layout.addWidget(self.scimprogress,4,0)
        self.getuserinfourlscim.clicked.connect(self.scimgetuserinfourl)
        self.scimdeleteusers.clicked.connect(self.scimdeleteuser)
        self.scimdeletegroups.clicked.connect(self.scimdeletegroup)
        self.tab2.setLayout(self.tab2.layout)


        # Add tabs to widget
        self.layout.addWidget(self.tabsup,1)
 

    def adgetuserinfourl(self):
        self.textad, self.okPressed = QInputDialog.getText(self,"","UserInfo_Url:", QLineEdit.Normal, "")
        if self.okPressed and self.textad != '':
            return self.textad
        else:
            self.msgbox.critical(self, "No text", "Please add UserInfo_URL")

    def scimgetuserinfourl(self):
        self.textscim, self.okPressed = QInputDialog.getText(self,"","UserInfo_Url:", QLineEdit.Normal, "")
        if self.okPressed and self.textscim != '':
            self.bearer, self.okPressed2 = QInputDialog.getText(self,"","Bearer Token:", QLineEdit.Normal, "")
            if self.okPressed2 and self.bearer != '':
                return self.bearer
            return self.textscim
        else:
            self.msgbox.critical(self, "No text", "Please add UserInfo_URL")




    def adcreateuser(self):
        self.fname = QFileDialog.getOpenFileName(None, filter="Json (*.json)")
        if self.fname != '' and self.textad != '':
            with open(self.fname[0]) as self.json_data:
                self.d = json.load(self.json_data)
            self.url = self.textad
            self.adimporter_header = {
            'Content-Type': 'application/json',
            'Accept': 'application/netskope.adsync.v8+json',
            'UserAgent': 'Netskope Adapters -v47.0.0.111',
            }
            self.l=len(self.d["_mapDnUserInfo"])
            self.v=self.l
            for each_item in self.d["_mapDnUserInfo"]:
                each_replace = self.d["_mapDnUserInfo"][each_item]["action"].replace("delete","create")
                self.d["_mapDnUserInfo"][each_item]["action"]=each_replace
                self.json_data = {"users": [self.d["_mapDnUserInfo"][each_item]]}
                self.json_data.update({"schema": []})
                self.json_data.update({"config": {"secureUPN": "0"}})
                self.resp = requests.post(self.url, data=json.dumps(self.json_data), headers=self.adimporter_header)
                if self.resp.status_code == 200:
                    self.v=self.v-1
                    p=int((self.v/self.l)*100)
                    self.adprogress.setValue(100-p)
                app.processEvents()
        else:
            self.msgbox.critical(self, "No text", "Please add UserInfo_URL")

    def adcreategroup(self):
        self.fname = QFileDialog.getOpenFileName(None, filter="Json (*.json)")
        if self.fname != '' and self.textad != '':
            with open(self.fname[0]) as self.json_data:
                self.d = json.load(self.json_data)
            self.url = self.textad
            self.adimporter_header = {
            'Content-Type': 'application/json',
            'Accept': 'application/netskope.adsync.v8+json',
            'UserAgent': 'Netskope Adapters support_tool',
            }
            self.l=len(self.d["_mapGroupInfo"])
            self.v=self.l
            for each_item in self.d["_mapGroupInfo"]:
                each_replace = self.d["_mapGroupInfo"][each_item]["action"].replace("delete","create")
                self.d["_mapGroupInfo"][each_item]["action"]=each_replace
                self.json_data = {"groups": [self.d["_mapGroupInfo"][each_item]]}
                self.json_data.update({"schema": []})
                self.json_data.update({"config": {"secureUPN": "0"}})
                self.resp = requests.post(self.url, data=json.dumps(self.json_data), headers=self.adimporter_header)
                if self.resp.status_code == 200:
                    self.v=self.v-1
                    self.p=int((self.v/self.l)*100)
                self.adprogress.setValue(100-self.p)
                app.processEvents()
        else:
            self.msgbox.critical(self, "No text", "Please add UserInfo_URL")


    def addeletegroup(self):
        self.fname = QFileDialog.getOpenFileName(None, filter="Json (*.json)")
        if self.fname != '' and self.textad != '':
            with open(self.fname[0]) as self.json_data:
                self.d = json.load(self.json_data)
            self.url = self.textad
            self.adimporter_header = {
            'Content-Type': 'application/json',
            'Accept': 'application/netskope.adsync.v8+json',
            'UserAgent': 'Netskope Adapters support_tool',
            }
            self.l=len(self.d["_mapGroupInfo"])
            self.v=self.l
            for each_item in self.d["_mapGroupInfo"]:
                each_replace = self.d["_mapGroupInfo"][each_item]["action"].replace("create","delete")
                self.d["_mapGroupInfo"][each_item]["action"]=each_replace
                self.json_data = {"groups": [self.d["_mapGroupInfo"][each_item]]}
                self.json_data.update({"schema": []})
                self.json_data.update({"config": {"secureUPN": "0"}})
                self.resp = requests.post(self.url, data=json.dumps(self.json_data), headers=self.adimporter_header)
                if self.resp.status_code == 200:
                    self.v=self.v-1
                    self.p=int((self.v/self.l)*100)
                self.adprogress.setValue(100-self.p)
                app.processEvents()
        else:
            self.msgbox.critical(self, "No text", "Please add UserInfo_URL")

    def addeleteuser(self):
        self.fname = QFileDialog.getOpenFileName(None, filter="Json (*.json)")
        if self.fname != '' and self.textad != '':
            with open(self.fname[0]) as self.json_data:
                self.d = json.load(self.json_data)
            self.url = self.textad
            self.adimporter_header = {
            'Content-Type': 'application/json',
            'Accept': 'application/netskope.adsync.v8+json',
            'UserAgent': 'Netskope Adapters -v47.0.0.111',
            }
            self.l=len(self.d["_mapDnUserInfo"])
            self.v=self.l
            for each_item in self.d["_mapDnUserInfo"]:
                each_replace = self.d["_mapDnUserInfo"][each_item]["action"].replace("create","delete")
                self.d["_mapDnUserInfo"][each_item]["action"]=each_replace
                self.json_data = {"users": [self.d["_mapDnUserInfo"][each_item]]}
                self.json_data.update({"schema": []})
                self.json_data.update({"config": {"secureUPN": "0"}})
                self.resp = requests.post(self.url, data=json.dumps(self.json_data), headers=self.adimporter_header)
                if self.resp.status_code == 200:
                    self.v=self.v-1
                    self.p=int((self.v/self.l)*100)
                self.adprogress.setValue(100-self.p)
                app.processEvents()
        else:
            self.msgbox.critical(self, "No text", "Please add UserInfo_URL")

    def scimpulluser(self):
        self.userinfourlscim=self.textscim
        self.getusers=[]
        self.headers = {"Authorization": "Bearer "+self.bearer}
        response = requests.get(self.userinfourlscim+"/scim/Users/", headers=self.headers)
        data=json.loads(response.text)
        for k,r in data.items():
            if k == "Resources":
                for line in r:
                    for k1,v1 in line.items():
                        if k1 == "id":
                            self.getusers.append(v1)

    def scimdeleteuser(self):
        self.scimpulluser()
        length=len(self.getusers)
        count=length
        percent=100
        self.headers = {"Authorization": "Bearer "+self.bearer}
        for userid in self.getusers:
            response = requests.delete(self.userinfourlscim+"/scim/Users/"+userid, headers=self.headers)
            if response.status_code == 204:
                count=count-1
                percent=int((count/length)*100)
                self.scimprogress.setValue(100-percent)
                app.processEvents()

    def scimpullgroup(self):
        self.userinfourlscim=self.textscim
        self.getgroups=[]
        self.headers = {"Authorization": "Bearer "+self.bearer}
        response = requests.get(self.userinfourlscim+"/Groups", headers=self.headers)
        data=json.loads(response.text)
        for k,r in data.items():
            if k == "Resources":
                for line in r:
                    for k1,v1 in line.items():
                        if k1 == "id":
                            self.getgroups.append(v1)


    def scimdeletegroup(self):
        self.scimpullgroup()
        length=len(self.getgroups)
        count=length
        percent=100
        self.headers = {"Authorization": "Bearer "+self.bearer}
        for groupid in self.getgroups:
            response = requests.delete(self.userinfourlscim+"/scim/Groups/"+groupid, headers=self.headers)
            print(response.status_code)
            if response.status_code == 204:
                count=count-1
                percent=int((count/length)*100)
            self.scimprogress.setValue(100-percent)
            app.processEvents()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
