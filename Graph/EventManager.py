from PyQt5.QtGui import QTransform
from PyQt5.QtCore import Qt, QObject, QPointF, pyqtSignal  # Corrected import here
from PyQt5.QtWidgets import QGraphicsItem
class EventManagerSignals(QObject):
    nodePressed = pyqtSignal(QGraphicsItem, QPointF)
    nodeMoved = pyqtSignal(QGraphicsItem, QPointF)
    nodeReleased = pyqtSignal(QGraphicsItem, QPointF)

class EventManager:
    def __init__(self, scene, graph_widget, Parent=None):
        self.scene = scene
        self.graph_widget = graph_widget  # Store reference to GraphWidget
        self.dragging = False
        self.selected_node_uuid = None  # Track the UUID of the selected node
        self.signals = EventManagerSignals()
        self.nodes = {}  # Initialize nodes as an empty dictionary


    def find_node_by_uuid(self, uuid):
        return self.graph_widget.node_manager.find_node_by_uuid(uuid)
    
    def register_node(self, node):
        # Register the node for event handling
        self.nodes[node.uuid] = node
        # You can also connect node-specific signals to EventManager slots here