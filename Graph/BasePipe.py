from PyQt5.QtCore import pyqtSignal, QPointF, QLineF, QRectF, Qt
from PyQt5.QtGui import QPen, QCursor
import math
from enum import Enum
from PyQt5.QtWidgets import QGraphicsObject
import uuid
import copy
class BasePipe(QGraphicsObject):
    positionChanged = pyqtSignal()
    
    def __init__(self, start_connection):
        super().__init__()
        self.uuid = str(uuid.uuid4())  # Generate a unique identifier
        self.start_connection = start_connection

    def clone(self):
        # Create a deep copy of the PipeManager instance
        return copy.deepcopy(self)
    def serialize(self):
        # Convert the pipe to a dictionary
        return {
            'uuid': self.uuid,
        }
