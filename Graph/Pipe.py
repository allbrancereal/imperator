from PyQt5.QtCore import pyqtSignal, QPointF, QLineF, QRectF
from PyQt5.QtGui import  QPen,  QCursor
from PyQt5.QtCore import Qt
import math
from enum import Enum
from PyQt5.QtWidgets import QGraphicsObject
from Graph import BasePipe
import copy 

class PhantomPipe(BasePipe):
    def __init__(self, input):
        super().__init__(input)

        self.dragging = False
        self.cursor_pos = QPointF()

    def clone(self):
        # Create a deep copy of the PipeManager instance
        return copy.deepcopy(self)
    def hoverEnterEvent(self, event):
        self.node.tab.app.setOverrideCursor(QCursor(Qt.OpenHandCursor))

    def hoverLeaveEvent(self, event):
        self.node.tab.app.restoreOverrideCursor()

    def update_cursor_position(self, pos):
        # Update the cursor position and redraw the pipe
        self.cursor_pos = pos
        self.update_position()  # Assuming update_position redraws the pipe based on input and cursor_pos




class Pipe(BasePipe):
    def __init__(self, input, output,node_manager):
        super().__init__(input, output,)
        self.end_connection = output
        self.input.connect(self)
        self.output.connect(self)
        self.input.node.signals.positionChanged.connect(self.update_position)
        self.output.node.signals.positionChanged.connect(self.update_position)
        self.node_manager = node_manager
    def clone(self):
        # Create a deep copy of the PipeManager instance
        return copy.deepcopy(self)
    def hoverEnterEvent(self, event):
        self.node.tab.app.setOverrideCursor(QCursor(Qt.OpenHandCursor))

    def hoverLeaveEvent(self, event):
        self.node.tab.app.restoreOverrideCursor()
        
    def disconnect(self):
        super().disconnect()
        if self.input:
            self.input.pipe = None
            self.input = None
        if self.output:
            self.output.pipe = None
            self.output = None
        if self.scene():
            self.scene().removeItem(self)
            
            
    def serialize(self):
        # Convert the pipe to a dictionary
        return {
            'uuid': self.uuid,
            'start_connection_uuid': self.start_connection.uuid,
            'end_connection_uuid': self.end_connection.uuid,
        }
    

    def set_start_position(self, new_start_pos):
        self.start_pos = new_start_pos
        # Update any graphical representation as needed

    def set_end_position(self, new_end_pos):
        self.end_pos = new_end_pos
        # Update any graphical representation as needed

    def resolve_connection(connection_uuid, node_manager):
        for node in node_manager.nodes.values():
            for connection in node.connections:  # Assuming each node has a list of connections
                if connection.uuid == connection_uuid:
                    return connection
        return None

    @classmethod
    def deserialize(cls, data):
        # Assuming you have a way to resolve connections by UUID
        start_connection = self.resolve_connection(data['start_connection_uuid'])
        end_connection = self.resolve_connection(data['end_connection_uuid'])
        
        # Create a new instance of Pipe
        pipe = cls(start_connection, end_connection)
        pipe.uuid = data['uuid']  # Set the UUID to match the serialized data
        
        return pipe