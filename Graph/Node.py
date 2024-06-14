from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem, QMenu, QAction, QGraphicsObject
from PyQt5.QtCore import QRectF, QUuid, QObject, pyqtSignal, QPoint, QPointF
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QSizeF
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QStyle
import os
import importlib.util
from PyQt5.QtGui import QPainterPath, QPainterPathStroker
import math

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
        
class Input:
    def __init__(self, name):
        self.name = name
        self.connected_pipe = None  # Initially, no pipe is connected

        def connect(self, pipe):
            self.connected_pipe = pipe

        def disconnect(self):
            self.connected_pipe = None

class Output:
    def __init__(self, name):
        self.name = name
        self.connected_pipes = []  # An output can have multiple connections

    def connect(self, pipe):
        self.connected_pipes.append(pipe)

    def disconnect(self, pipe):
        self.connected_pipes.remove(pipe)

class Node:
    counter = 0
    identifier = "base.node"
    
    def __init__(self, x, y, width, height, name=None, library=None, tab=None, event_manager=None):
        self.uuid = QUuid.createUuid().toString()[1:-1]
        self.name = name if name else f"Node{Node.counter}"
        Node.counter += 1
        self.tab = tab
        # Assuming tab has a reference to the NodeApp instance as 'app'
        if self.tab and hasattr(self.tab, 'app'):
            self.library = self.tab.app.library_registry.get_library(library)
        else:
            self.library = None
        self.event_manager = event_manager
        self.default_inputs = {}
        self.default_outputs = {}
        self.inputs = {}
        self.outputs = {}
        self.pipes = []
        
        self.position = QPointF(x, y)
        self.graphicsItem = None  # Add this line to initialize the graphicsItem attribute

    def setGraphicsItem(self, item):
        self.graphicsItem = item
    def setup_default_io(self):
        # Setup default inputs
        for input_name in self.default_inputs:
            self.add_input(input_name)

        # Setup default outputs
        for output_name in self.default_outputs:
            self.add_output(output_name)

    def add_input(self, name):
        self.inputs[name] = Input(name)

    def add_output(self, name):
        self.outputs[name] = Output(name)
    def serialize(self):
        return {
            'uuid': self.uuid,
            'x': self.rect.x(),
            'y': self.rect.y(),
            'width': self.width,
            'height': self.height,
            'name': self.name,
            'tab': self.tab,
            'library': self.library if isinstance(self.library, str) else None,  # Assuming library can be serialized directly or is a string
            'position': {'x': self.position.x(), 'y': self.position.y()},
            'default_inputs': self.default_inputs,  # Ensure these are serializable
            'default_outputs': self.default_outputs,  # Ensure these are serializable
            'inputs': self.inputs,  # Ensure these are serializable
            'outputs': self.outputs,  # Ensure these are serializable
            # 'pipes': [pipe.serialize() for pipe in self.pipes],  # Uncomment if pipes can be serialized
            # Add other attributes here as needed
        }
    @classmethod
    def deserialize(cls, data):
        node = cls(
            x=data['x'],
            y=data['y'],
            width=data['width'],
            height=data['height'],
            name=data['name'],
            library=data['library'],  # Make sure to handle library loading if it's not just a string
            tab=data['tab']
        )
        node.position = QPointF(data['position']['x'], data['position']['y'])
        node.default_inputs = data['default_inputs']
        node.default_outputs = data['default_outputs']
        node.inputs = data['inputs']
        node.outputs = data['outputs']
        # Handle 'pipes' if necessary
        # Set other attributes as needed from the serialized data
        return node
    
class NodeRegistry:
    def __init__(self):
        self.nodes = {}

    def register_base_node(self):
        self.nodes['base.node'] = Node


    def register_node(self, name, node):
        self.nodes[name] = node

    def get_node(self, name):
        return self.nodes.get(name)
    
    def create(self, identifier):
        NodeClass = self.get_node(identifier)
        print(f"Creating node with identifier {identifier}: {NodeClass}")  # Print the identifier and the NodeClass
        return NodeClass


        
node_registry = NodeRegistry()
node_registry.register_base_node()

# Get the directory of the current file# Get the directory of the current file
dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nodes')

def register_nodes(registry):
    # Get the directory of the current file
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nodes')

    # Iterate over all files in the directory
    for filename in os.listdir(dir_path):
        # Check if the file is a .py file
        if filename.endswith('.py') and filename != 'Node.py':
            # Get the module name from the filename
            module_name = filename[:-3]

            # Create a module specification
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(dir_path, filename))

            # Create a module from the specification
            module = importlib.util.module_from_spec(spec)

            # Execute the module
            spec.loader.exec_module(module)
            # Check if the module has a 'registered_vars' attribute
            if hasattr(module, 'registered_vars'):
                # Register each node in 'registered_vars' in the node registry
                for node_identifier, NodeClass in module.registered_vars.items():
                    registry.register_node(NodeClass.identifier, NodeClass)
                    print(f"Registered node: {NodeClass.identifier}")