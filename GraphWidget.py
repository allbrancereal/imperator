from PyQt5.QtCore import QObject, pyqtSignal
from Graph.Node import Node, NodeRegistry
from Graph.RenderManager import RenderManager
from Graph.SerializationManager import SerializationManager
from Graph.EventManager import EventManager
from PyQt5.QtWidgets import QWidget
class GraphWidget(QWidget):
    nodeAddedSignal = pyqtSignal(Node)
    nodeRemovedSignal = pyqtSignal(Node)

    def __init__(self,app,library_manager, render_manager, graph_core):
        super().__init__()
        

    def real_init(self, app, library_manager, render_manager, graph_core):
        self.library_registry = library_manager
        self.graph_core = graph_core
        self.render_manager = render_manager
        self.event_manager = EventManager(self.render_manager.scene, self)
        self.serialization_manager = SerializationManager(self,self.graph_core.node_manager, self.graph_core.pipe_manager)
        # Assuming graphWidgetInstance is an instance of GraphWidget
        # and renderManagerInstance is an instance of RenderManager

        self.nodeAddedSignal.connect(self.render_manager.onNodeAdded)

    def mousePressEvent(self, event):
        if self.render_manager:
            self.render_manager.handleMousePressEvent(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.render_manager:
            self.render_manager.handleMouseMoveEvent(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.render_manager:
            self.render_manager.handleMouseReleaseEvent(event)
        super().mouseReleaseEvent(event)
        
    def create_node(self, node_identifier, x, y, width, height, name, library_identifier, tab, event_manager):
        # Instantiate the node using the registry
        NodeClass = self.graph_core.node_registry.get_node(node_identifier)
        if not NodeClass:
            print(f"Node class for identifier '{node_identifier}' not found.")
            return
        
        # Create an instance of the node with position (x, y) and size (100, 50)
        node = NodeClass(x=x, y=y, width=100, height=50, name=name, library=library_identifier, tab=tab, event_manager=event_manager)
        node.setup_default_io()  # Set up default inputs and outputs


        # Add the node to the graph
        self.add_node_object(node)
    def add_node_object(self, node):
        # Directly add the node object to the graph
        # Assuming there's a method or a way to add the node object in your graph_core.node_manager
        self.graph_core.node_manager.add_node_object(node)
        self.nodeAddedSignal.emit(node)
    def add_node(self, node_identifier, position):
        # Use GraphCore to add a node
        node = self.graph_core.node_manager.add_node(node_identifier, position)
        if node:
            self.nodeAddedSignal.emit(node)

    def remove_node(self, node):
        # Use GraphCore to remove a node
        self.graph_core.node_manager.remove_node(node)
        self.nodeRemovedSignal.emit(node)

    def get_nodes(self):
        # Access nodes through GraphCore
        return self.graph_core.node_manager.nodes

    
