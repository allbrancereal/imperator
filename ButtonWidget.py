from PyQt5.QtWidgets import QPushButton

class ButtonWidget(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
