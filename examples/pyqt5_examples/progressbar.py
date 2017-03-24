import sys,time
from PyQt5.QtWidgets import (QWidget, QProgressBar,
    QPushButton, QApplication)
from PyQt5.QtCore import QBasicTimer, pyqtSignal

class Down(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.f = pyqtSignal()

    def initUI(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 50)
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QProgressBar')

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.change)
        self.step = 0

        self.show()
    def change(self):
        self.pbar.setValue(self.step)
        self.step += 5
        if self.step == 100:
            self.f.emit()





if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
