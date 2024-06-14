from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsLineItem, QGraphicsItem
from PyQt5.QtCore import QRectF, QPointF, QLineF
from PyQt5.QtGui import QPen, QBrush, QColor
import math
import copy
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QPainterPath, QPolygonF    
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsPolygonItem
class BezierConnection(QGraphicsPathItem):
    connectionCreated = pyqtSignal(object)  # Could pass the connection object itself
    connectionDeleted = pyqtSignal(object)
    def __init__(self, start_point, end_point, parent=None):
        super().__init__(parent)
        self.start_point = start_point
        self.end_point = end_point
        self.setPen(QPen(QColor(0, 0, 0), 2))
        self.update_path()

    def update_path(self):
        path = QPainterPath(self.start_point)
        ctrl_point1 = QPointF((self.start_point.x() + self.end_point.x()) / 2, self.start_point.y())
        ctrl_point2 = QPointF((self.start_point.x() + self.end_point.x()) / 2, self.end_point.y())
        path.cubicTo(ctrl_point1, ctrl_point2, self.end_point)
        self.setPath(path)
    def set_start_point(self, new_start_point):
        self.start_point = new_start_point
        self.update_path()

    def set_end_point(self, new_end_point):
        self.end_point = new_end_point
        self.update_path()
class Marquee(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.setPen(QPen(Qt.black, 1, Qt.DashLine))

    def set_rect_from_points(self, point1, point2):
        x = min(point1.x(), point2.x())
        y = min(point1.y(), point2.y())
        width = abs(point1.x() - point2.x())
        height = abs(point1.y() - point2.y())
        self.setRect(x, y, width, height)

class HandleBase(QObject, QGraphicsLineItem):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        QGraphicsLineItem.__init__(self, parent)

        self.setPen(QPen(QColor(255, 0, 0), 2))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor(255, 255, 0), 3))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(QColor(255, 0, 0), 2))
        super().hoverLeaveEvent(event)

class RadialHandle(HandleBase):
    def __init__(self, angle, radius, parent=None):
        super().__init__(parent)
        self.angle = angle
        self.radius = radius
        self.calculate_position()

    def calculate_position(self):
        angle_rad = math.radians(self.angle)
        end_x = self.radius * math.cos(angle_rad)
        end_y = self.radius * math.sin(angle_rad)
        self.setLine(QLineF(QPointF(0, 0), QPointF(end_x, end_y)))

class InputHandle(RadialHandle):
    connectionDragStarted = pyqtSignal(object)  # (outputHandle)
    connectionDropped = pyqtSignal(object, object)  # (outputHandle, inputHandle)
    connectionMade = pyqtSignal(object, object)  # (outputHandle, inputHandle)

    def __init__(self, angle, radius, parent=None):
        super().__init__(angle, radius, parent)
        self.setPen(QPen(QColor(0, 255, 0), 2))
        
class OutputHandle(QGraphicsPolygonItem):
    connectionDragStarted = pyqtSignal(object)  # (outputHandle)
    # Signal for when a connection is successfully made
    connectionDropped = pyqtSignal(object, object)  # (outputHandle, inputHandle)
    connectionMade = pyqtSignal(object, object)  # (outputHandle, inputHandle)
    def __init__(self, angle, radius, parent=None):
        super().__init__(parent)
        self.angle = angle
        self.radius = radius
        self.calculate_position()

    def calculate_position(self):
        angle_rad = math.radians(self.angle)
        end_x = self.radius * math.cos(angle_rad)
        end_y = self.radius * math.sin(angle_rad)

        # Define the arrow shape
        arrow_size = 10  # Size of the arrow
        polygon = QPolygonF()
        polygon.append(QPointF(end_x, end_y))
        polygon.append(QPointF(end_x - arrow_size, end_y - arrow_size))
        polygon.append(QPointF(end_x - arrow_size, end_y + arrow_size))
        polygon.append(QPointF(end_x, end_y))

        self.setPolygon(polygon)
        self.setPen(QPen(QColor(0, 0, 0), 2))
        self.setBrush(QBrush(QColor(0, 0, 0)))  # Fill the arrow with black color

        # Adjust the position of the arrow based on the parent node's position
        if self.parent:
            self.setPos(self.parent.position.x() + 50, self.parent.position.y() + 25)
        
class DraggableNode(QGraphicsRectItem):
    nodeMoved = pyqtSignal(QPointF)  # Emit the new position

    def __init__(self, rect, parent=None):
        super().__init__(rect, parent)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.dragging = False

    def mousePressEvent(self, event):
        self.dragging = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            # Implement logic to update the node's position
            # This could involve updating the model and notifying the RenderManager to redraw connections
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        super().mouseReleaseEvent(event)

    def hoverEnterEvent(self, event):
        # Optionally, change the appearance to indicate hover state
        self.setBrush(QBrush(QColor(220, 220, 255)))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(QColor(200, 200, 250)))
        super().hoverLeaveEvent(event)
