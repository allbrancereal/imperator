from PyQt5.QtWidgets import QLineEdit, QWidget, QVBoxLayout
from Graph.nodes import Node

class WriteNode(Node):
    identifier = "output.write"
    def __init__(self, x, y, width, height, name=None, library=None, tab=None, event_manager=None):
        super().__init__(x, y, width, height, name, library, tab,  event_manager)

        # Create a QWidget for the QLineEdit
        self.widget = QWidget()

        # Create a QVBoxLayout for the widget
        self.layout = QVBoxLayout(self.widget)
        
        # Create a QLineEdit for the file path
        self.file_path_edit = QLineEdit()

        # Add the QLineEdit to the layout
        self.layout.addWidget(self.file_path_edit)
        self.default_inputs = {"input1"}

    def get_file_path(self):
        return self.file_path_edit.text()

    def set_file_path(self, file_path):
        self.file_path_edit.setText(file_path)

    def write_file(self):
        file_path = self.get_file_path()
        if self.input_connector.connections:
            data = self.input_connector.connections[0].node.get_data()
            with open(file_path, 'w') as f:
                f.write(str(data))

registered_vars = {'WriteNode': WriteNode}