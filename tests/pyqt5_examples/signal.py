import sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QObject
from PyQt5.QtWidgets import (QWidget, QProgressBar,
    QPushButton, QApplication)

class Example(QWidget):
    s = pyqtSignal()
    """docstring for Example."""
    def __init__(self):
        # QThread.__init__(self)
        # QWidget.__init__(self)
        super(Example, self).__init__()

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QProgressBar')

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.done)

    def done(self):
        self.w = QtWidgets.QDialog()
        self.w.setGeometry(800, 300, 300, 200)
        self.w.setWindowTitle('QProgressBar')
        self.w.pbar = QProgressBar(self.w)
        self.w.pbar.setGeometry(50, 50, 100, 50)
        self.w.pbar.show()
        self.w.show()

        self.w = Worker()
        # self.connect(self.w, SIGNAL("finished()"), self.done)
        # print(self.w.s)
        self.w.s.connect(self.done)
        self.w.run()


class Worker(QThread):
    """docstring for Worker."""
    def __init__(self):
        super(Worker, self).__init__()
        # QThread.__init__(self)
        # QWidget.__init__(self)

    def run(self):
        # self.w = QWidget()
        # self.w.setGeometry(300, 300, 280, 170)
        # self.w.setWindowTitle('QProgressBar')
        # self.w.show()
        print('thread start')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
