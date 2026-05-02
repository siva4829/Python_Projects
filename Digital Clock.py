import sys
from PyQt5.QtWidgets import QApplication, QWidget,QVBoxLayout,QLabel
from PyQt5.QtCore import QTimer,QTime,Qt


class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Clock")
        self.setGeometry(300, 300, 500, 150)
        self.time_label = QLabel(self)
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.time_label)
        self.setLayout(vbox)
        self.time_label.setStyleSheet("background-color: black;"
                                      "color:red ;"
                                      "font-size:150px;"
                                      "font-family:Arial")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)

    def updateTime(self):
        currentTime = QTime.currentTime().toString("hh:mm:ss AP")
        self.time_label.setText(currentTime)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DigitalClock()
    window.show()
    sys.exit(app.exec_())
