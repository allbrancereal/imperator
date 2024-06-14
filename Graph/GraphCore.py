
from Graph.NodeManager import NodeManager
from Graph.PipeManager import PipeManager
from Graph.Node import NodeRegistry, register_nodes

class GraphCore:
    def __init__(self, library_registry, render_manager=None):
        self.library_registry = library_registry
        self.render_manager = render_manager
        self.node_registry = NodeRegistry()
        register_nodes(self.node_registry)
        self.node_manager = NodeManager(self.render_manager.scene,self.node_registry,self.render_manager)
        self.pipe_manager = PipeManager(self.node_manager)
