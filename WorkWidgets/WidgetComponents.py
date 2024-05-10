from PyQt6 import QtWidgets, QtCore, QtGui


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()

        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.setFont(QtGui.QFont("Arial", pointSize=font_size, weight=500))
        self.setText(content)

class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", length=10, width=200, font_size=16):
        super().__init__()
        self.setMaxLength(length)
        self.setText(default_content)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("Arial", font_size))
        self.setStyleSheet("background-color: white;") 

    def setReadOnly(self, read_only):
        super().setReadOnly(read_only)
        if read_only:
            self.setStyleSheet("background-color: gray;")
        else:
            self.setStyleSheet("background-color: white;") 

class NumberLineEditComponent(LineEditComponent):
    def __init__(self, default_content="", length=10, width=200, font_size=16, min_value=0, max_value=100):
        super().__init__(default_content, length, width, font_size)
        
        validator = QtGui.QIntValidator(min_value, max_value, self)
        self.setValidator(validator)

class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("Arial", font_size))
