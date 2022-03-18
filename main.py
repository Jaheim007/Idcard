import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from Widget.card import AccountPage_ID


 
def main():
    app = QApplication(sys.argv)
    home = AccountPage_ID()
    home.show()
    app.exec_()


if __name__ == '__main__':
    main()
