import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication , QMainWindow, QWidget, QPushButton, QLabel

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(550, 350)
    w.move(300, 300)
    w.setWindowTitle('Simple')

    def on_btn_func():
        s.show()

    def on_btn_close():
        w.close()

    btn = QPushButton('ok', w)
    btn.setToolTip('This is a <b>QPushButton</b> widget')
    btn.resize(btn.sizeHint())
    btn.move(50, 50)
    btn.clicked.connect(on_btn_func)

    btn1 = QPushButton('Cancel', w)
    btn1.setToolTip('This is a <b>QPushButton</b> widget')
    btn1.resize(btn.sizeHint())
    btn1.move(50, 100)
    btn1.clicked.connect(on_btn_close)

    label = QLabel('hello', w)
    label.move(100, 150)

    s = QWidget()
    s.resize(550, 350)
    s.move(400, 400)
    s.setWindowTitle('S')

    def son_btn_close():
        s.close()
    def son_btn():
        label.setText('sss')

    sbtn1 = QPushButton('ok', s)
    sbtn1.setToolTip('This is a <b>QPushButton</b> widget')
    sbtn1.resize(btn.sizeHint())
    sbtn1.move(50, 150)
    sbtn1.clicked.connect(son_btn)

    sbtn = QPushButton('close', s)
    sbtn.setToolTip('This is a <b>QPushButton</b> widget')
    sbtn.resize(btn.sizeHint())
    sbtn.move(50, 50)
    sbtn.clicked.connect(son_btn_close)

    w.show()



    sys.exit(app.exec_())
