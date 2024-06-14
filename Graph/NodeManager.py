from Graph import Node,Pipe
import copy
from PyQt5.QtCore import Qt
        
class NodeManager:
    def __init__(self, scene, graph_widget, render_manager=None):
        # Other initializations remain the same
        self.render_manager = render_manager  # Add a reference to RenderManager

        self.nodes = {}
        self.node_io = {}
        self.clipboard = []
        self.dragging = False  # Initialize dragging attribute
        self.temp_pipe = None  # Initialize temp_pipe attribute
        
        self.scene = scene
        self.graph_widget = graph_widget
        self.selected_nodes_and_pipes = []
        # Connect signals from the graph widget if necessary

    def add_node_object(self, node):
        # Add the node to the internal dictionary of nodes
        self.nodes[node.uuid] = node
        # Initialize the node's inputs and outputs in the node_io dictionary
        self.node_io[node.uuid] = {'inputs': [], 'outputs': []}
        # If a RenderManager is available, use it to add the node to the scene

    def find_node_at_position(self, pos):
        # Implement logic to find a node at the given position
        for node in self.nodes.values():
            if node.contains_position(pos):  # Assuming Node has a method to check if a position is within its bounds
                return node
        return None
    
    def clone(self):
        # Create a deep copy of the NodeManager instance
        return copy.deepcopy(self)
    def add_node(self, node):
        self.nodes[node.uuid] = node
        self.node_io[node.uuid] = {'inputs': [], 'outputs': []}
    

    def remove_node(self, node):
        del self.nodes[node.uuid]
        del self.node_io[node.uuid]

    def copy_node(self, node):
        # Assuming Node has a copy method or using copy.deepcopy for a deep copy
        node_copy = copy.deepcopy(node)
        self.clipboard.append(node_copy)
        
    def find_node_by_uuid(self, uuid):
        # Assuming self.nodes is a dictionary mapping UUIDs to node instances
        return self.nodes.get(uuid, None)
    def paste_node(self):
        # This method assumes pasting the last copied node
        if self.clipboard:
            node_to_paste = self.clipboard[-1]
            # Adjust position or other properties as needed
            self.add_node(node_to_paste)
            return node_to_paste
        return None

    def cut_node(self, node):
        self.copy_node(node)
        self.remove_node(node)

    def serialize(self):
        # Convert the current state of nodes to a serializable format
        serialized_nodes = {uuid: node.serialize() for uuid, node in self.nodes.items()}
        return serialized_nodes
    def resolve_connection(self,connection_uuid):
        for node in self.nodes.values():
            for connection in node.connections:  # Assuming each node has a list of connections
                if connection.uuid == connection_uuid:
                    return connection
        return None
    @classmethod
    def deserialize(cls, data, node_manager):
        start_connection = node_manager.resolve_connection(data['start_connection_uuid'], node_manager)
        end_connection = node_manager.resolve_connection(data['end_connection_uuid'], node_manager)
    
        if start_connection is None or end_connection is None:
            raise ValueError("Could not resolve one or more connections.")
    
        pipe = cls(start_connection, end_connection)
        pipe.uuid = data['uuid']
    
        return pipe