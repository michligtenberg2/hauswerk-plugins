from PyQt6.QtWidgets import QWidget

class MypluginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Myplugin")