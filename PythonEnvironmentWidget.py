
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QTextBrowser, QPushButton
from PyQt5.QtCore import pyqtSlot
from contextlib import redirect_stdout, redirect_stderr
import io

class PythonEnvironmentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.python_env = QPlainTextEdit(self)
        self.layout.addWidget(self.python_env)

        self.output = QTextBrowser(self)
        self.layout.addWidget(self.output)

        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run_code)
        self.layout.addWidget(self.run_button)

    @pyqtSlot()
    def run_code(self):
        code = self.python_env.toPlainText()

        # Redirect stdout and stderr to the output widget
        stdout = io.StringIO()
        stderr = io.StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exec(code)
            except Exception as e:
                print(str(e))

        self.output.setPlainText(stdout.getvalue() + stderr.getvalue())
