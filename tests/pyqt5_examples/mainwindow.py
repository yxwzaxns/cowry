import sys, time
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QObject, QTimer
from PyQt5 import QtWidgets
from progressbar import Down
from PyQt5.QtWidgets import QApplication , QMainWindow, QWidget, QPushButton, QLabel, QProgressBar


class Example(QMainWindow):
    """docstring for Example."""
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()


    def initUI(self):

        btn = QPushButton('ok', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        btn.clicked.connect(self.on_btn_ok)

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('Absolute')
        self.show()

    def on_btn_ok(self):
        self.s = QtWidgets.QDialog()
        self.s.setGeometry(800, 300, 300, 200)
        self.s.setWindowTitle('QProgressBar')
        self.s.pbar = QProgressBar(self.s)
        self.s.pbar.setGeometry(50, 50, 100, 50)
        self.s.pbar.show()
        self.s.show()

        self.w = Worker()
        # self.connect(self.w, SIGNAL("finished()"), self.done)
        # print(self.w.s)
        self.w.s.connect(self.s.pbar.setValue)
        self.w.run()

        # w.start()
    def done(self):
        print('get SIGNAL')

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()

    def on_btn_t(self):
        s = self.sender()
        print(s.text())


class Worker(QThread):
    s = pyqtSignal(int)
    """docstring for Worker."""
    def __init__(self):
        QThread.__init__(self)
        self.step = 0
        # self.s = pyqtSignal(str)
        # QObject.__init__(self)
        # self.down = down
        # self.s.connect(self.do)

    def run(self):
        self.timer = QTimer()
        # for i in range(100):

        self.timer.timeout.connect(self.do)
        self.timer.start(1000)
            # self.s.emit(i)
        # self.exec_()
    def do(self):
        self.step += 1
        if self.step == 101:
            self.timer.stop()
        self.s.emit(self.step)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


    # w = QWidget()
    # w.resize(550, 350)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    #
    # def on_btn_func():
    #     s.show()
    #
    # def on_btn_close():
    #     w.close()
    #
    # btn = QPushButton('ok', w)
    # btn.setToolTip('This is a <b>QPushButton</b> widget')
    # btn.resize(btn.sizeHint())
    # btn.move(50, 50)
    # btn.clicked.connect(on_btn_func)
    #
    # btn1 = QPushButton('Cancel', w)
    # btn1.setToolTip('This is a <b>QPushButton</b> widget')
    # btn1.resize(btn.sizeHint())
    # btn1.move(50, 100)
    # btn1.clicked.connect(on_btn_close)
    #
    # label = QLabel('hello', w)
    # label.move(100, 150)
    #
    # s = QWidget()
    # s.resize(550, 350)
    # s.move(400, 400)
    # s.setWindowTitle('S')
    #
    # def son_btn_close():
    #     s.close()
    # def son_btn():
    #     label.setText('sss')
    #
    # sbtn1 = QPushButton('ok', s)
    # sbtn1.setToolTip('This is a <b>QPushButton</b> widget')
    # sbtn1.resize(btn.sizeHint())
    # sbtn1.move(50, 150)
    # sbtn1.clicked.connect(son_btn)
    #
    # sbtn = QPushButton('close', s)
    # sbtn.setToolTip('This is a <b>QPushButton</b> widget')
    # sbtn.resize(btn.sizeHint())
    # sbtn.move(50, 50)
    # sbtn.clicked.connect(son_btn_close)
    #
    # w.show()
