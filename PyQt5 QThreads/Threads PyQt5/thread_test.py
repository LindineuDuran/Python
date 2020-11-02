from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__()
        self.resize(200, 200)
        self.button = QPushButton("Iniciar loop", self)
        self.button.clicked.connect(self.start_loop)

    def start_loop(self):
        while True:
            print ("Estamos no loop")

root = QApplication([])
app = Window()
app.show()
sys.exit(root.exec_())
