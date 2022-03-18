from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QAbstractItemView, QMessageBox
from Widget.id import Ui_Idcard
import pyautogui
import sqlite3
import mss
import mss.tools
from PyQt5.QtGui import QPixmap

class AccountPage_ID(QMainWindow, Ui_Idcard):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_photo_btn.clicked.connect(self.openfile)
        self.refresh_btn.clicked.connect(self.refreshitems)
        self.search_btn.clicked.connect(self.serachresults)
        self.register_btn.clicked.connect(self.tablereults)
        self.back_btn.clicked.connect(self.back)
        self.capture.clicked.connect(self.image)
        

    def openfile(self):
        fimg = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\Users\\jahei\\OneDrive\\Bureau\\ID\\Static', 'Image files (*.jpg *.png)')
        img = fimg[0]
        pixmap = QPixmap(img)
        self.add_photo.setPixmap(QPixmap(pixmap))
        self.add_photo.setScaledContents(True)

    def tablereults(self):
        db = sqlite3.connect("userdata.db")
       
        dic = {
            "Prenom":self.prenom_line.text(),
            "Nom": self.nom_line.text(),
            "Sexe": self.comboBox.currentText(),
            "Date":self.dateEdit_combo.text(),
            "img": self.add_photo.text()
        }
        if self.prenom_line.text() == "" or self.nom_line.text() == "":
            QMessageBox.warning(self, "Error", "Veuillez saisir vos infomations")
           

        else:

            cur = db.cursor()
            cur.execute(""" CREATE TABLE IF NOT EXISTS User(
                        Prenom text, 
                        Nom text, 
                        Sexe text, 
                        Date text, 
                        img text
                    )""")

        
            cur.execute("INSERT INTO User VALUES (:Prenom, :Nom, :Sexe, :Date, :img)", dic)
            
            db.commit()
            db.close()

            self.stackedWidget.setCurrentWidget(self.page)
            self.show()
            

    def back(self):
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.show()
    
    
    def refreshitems(self):
        dbs = sqlite3.connect("userdata.db")
        cut = dbs.cursor()
        command =''' SELECT * FROM User ''' 
        res = cut.execute(command)
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(res):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    
    def serachresults(self):
        db = sqlite3.connect("userdata.db")
        cur = db.cursor()
        word = self.search_line.text()

        command = ''' SELECT * FROM User WHERE Prenom=? ''' 
        res = cur.execute(command,[word])
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(res):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def image(self):
        
        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"top": 160, "left": 160, "width": 160, "height": 135}
            output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

            # Grab the data
            sct_img = sct.grab(monitor)

            # Save to the picture file
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            print(output)
    


        
        

    


    # def myscreenshot(self):
    #     myScreenshot = pyautogui.screenshot()
    #     myScreenshot.save(r'C:\Users\jahei\OneDrive\Bureau\ID\Static\screenshot.png')