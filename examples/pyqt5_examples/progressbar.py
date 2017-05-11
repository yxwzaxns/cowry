import sys,time, threading
from PyQt5.QtWidgets import (QWidget, QProgressBar,
    QPushButton, QApplication)
from PyQt5.QtCore import QBasicTimer, pyqtSignal, QObject

class Signal(QObject):
    # def __init__(self):
    #     super(UploadSignal, self).__init__()
    q = pyqtSignal(int)

class Pregress(threading.Thread):
    """docstring for Pregress."""
    def __init__(self):
        super(Pregress, self).__init__()
        self.step = 0

    def run(self):
        while True:
            time.sleep(0.1)
            self.step += 1
            if self.step <= 99:
                self.f.q.emit(self.step)
            else:
                break

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.pregress = Pregress()
        self.pregress.f = Signal()
        self.pregress.f.q.connect(self.change)
        self.initUI()

    def initUI(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 50)
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QProgressBar')

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.pregress.start)

        self.step = 0
        self.token = 1

        self.show()

    def change(self, p):
        self.pbar.setValue(p)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
