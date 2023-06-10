import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtCore import QTimer, Qt

class NotificationWindow(QWidget):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Bildirim")
        self.setGeometry(100, 100, 300, 100)

        self.label = QLabel(self)
        self.label.setText(message)
        self.label.setAlignment(Qt.AlignCenter)

        self.timer = QTimer()
        self.timer.setInterval(5000)  # 5 saniye
        self.timer.timeout.connect(self.hide_message)

    def showEvent(self, event):
        self.timer.start()
        super().showEvent(event)

    def hide_message(self):
        self.label.hide()
        self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    username = "doğru_kullanıcı_adı"
    entered_username = "yanlış_kullanıcı_adı"

    if entered_username != username:
        window = NotificationWindow("Kullanıcı adı yanlış!")
        window.show()

    sys.exit(app.exec_())