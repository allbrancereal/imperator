from PyQt5.QtCore import QObject, pyqtSignal
from Graph import Pipe, PhantomPipe
import json
import copy
class PipeManager:
    inputConnected = pyqtSignal(str, str)  # Emits input UUID and pipe UUID
    inputDisconnected = pyqtSignal(str)  # Emits input UUID
    outputConnected = pyqtSignal(str, str)  # Emits output UUID and pipe UUID
    outputDisconnected = pyqtSignal(str)  # Emits output UUID
    def __init__(self, node_manager, category="default"):
        self.pipes = {}
        self.node_manager = node_manager
        node_manager.pipe_manager = self;
        self.category = category  # New category attribute
    def clone(self):
        # Create a deep copy of the PipeManager instance
        return copy.deepcopy(self)
    
    def find_pipes_by_node_uuid(self, node_uuid):
        # Initialize an empty list to hold the connected pipes
        connected_pipes = []
        # Iterate over all pipes managed by PipeManager
        for pipe in self.pipes.values():
            # Check if the current pipe is connected to the node
            if pipe.start_node_uuid == node_uuid or pipe.end_node_uuid == node_uuid:
                # If so, add it to the list of connected pipes
                connected_pipes.append(pipe)
        # Return the list of connected pipes
        return connected_pipes
    
    def remove_pipe(self, pipe):
        if pipe.uuid in self.pipes:
            # Emit signals before removing the pipe
            self.inputDisconnected.emit(pipe.start_connection.uuid)
            self.outputDisconnected.emit(pipe.end_connection.uuid)
            del self.pipes[pipe.uuid]

    def create_temporary_pipe(self, start_connection):
        # This method creates a PhantomPipe or a similar temporary visual representation
        # It doesn't add the pipe to the pipes dictionary since it's not a confirmed connection yet
        temp_pipe = PhantomPipe(start_connection)
        return temp_pipe

    def create_pipe(self, output, input):
        # Check if the input already has a connection
        if input.connected_pipe:
            # Optionally, disconnect the existing pipe
            self.disconnect_pipe(input.connected_pipe)
        # Create the new pipe and connect it
        new_pipe = Pipe(output, input)
        self.render_manager.render_pipe(output.node, input.node)
        input.connected_pipe = new_pipe
        output.connected_pipes.append(new_pipe)
        # Additional logic to add the pipe to the scene, etc.

    def disconnect_pipe(self, pipe):
        # Disconnect the pipe from its input and output
        if pipe.input.connected_pipe == pipe:
            pipe.input.connected_pipe = None
        if pipe in pipe.output.connected_pipes:
            pipe.output.connected_pipes.remove(pipe)
        # Additional logic to remove the pipe from the scene, etc.
    def add_pipe(self, pipe):
        self.pipes[pipe.uuid] = pipe
        # Emit signals based on the pipe's connections
        self.inputConnected.emit(pipe.start_connection.uuid, pipe.uuid)
        self.outputConnected.emit(pipe.end_connection.uuid, pipe.uuid)

    def convert_pipe(self, uuid, target_pipe_class):
        if uuid in self.pipes and issubclass(target_pipe_class, Pipe):
            original_pipe = self.pipes[uuid]
            # Create a new instance of the target pipe class with the attributes of the original pipe
            new_pipe = target_pipe_class(original_pipe.start_connection, original_pipe.end_connection)
            new_pipe.uuid = uuid  # Preserve the original UUID
            # Replace the original pipe with the new one
            self.pipes[uuid] = new_pipe

    def serialize(self):
        serialized_pipes = {uuid: pipe.serialize() for uuid, pipe in self.pipes.items()}
        return json.dumps(serialized_pipes)

    def deserialize(self, data):
        deserialized_pipes = json.loads(data)
        for uuid, pipe_data in deserialized_pipes.items():
            pipe = Pipe.deserialize(pipe_data)
            self.add_pipe(pipe)
            
    def on_input_connected(self, input_uuid, pipe_uuid):
        # Assuming each node has a method to handle being connected to a pipe
        if input_uuid in self.node_manager.nodes:
            node = self.node_manager.nodes[input_uuid]
            node.on_pipe_connected(pipe_uuid)
        print(f"Input {input_uuid} connected to pipe {pipe_uuid}")

    def on_output_connected(self, output_uuid, pipe_uuid):
        # Similarly for output connections
        if output_uuid in self.node_manager.nodes:
            node = self.node_manager.nodes[output_uuid]
            node.on_pipe_connected(pipe_uuid)
        print(f"Output {output_uuid} connected to pipe {pipe_uuid}")

    def on_input_disconnected(self, input_uuid):
        # Handle an input connection being removed
        if input_uuid in self.node_manager.nodes:
            node = self.node_manager.nodes[input_uuid]
            node.on_pipe_disconnected()
        print(f"Input {input_uuid} disconnected")
        
    def on_output_disconnected(self, output_uuid):
        # Notify the affected node
        if output_uuid in self.node_manager.nodes:
            node = self.node_manager.nodes[output_uuid]
            node.on_pipe_disconnected()
            print(f"Output {output_uuid} disconnected")
        else:
            print(f"Warning: Node for output {output_uuid} not found.")

        # Emit a signal to notify other parts of the application
        self.outputDisconnected.emit(output_uuid)
    def update_connected_pipes_positions(self, node_uuid):
        # Find all pipes connected to the node that has moved
        connected_pipes = self.find_pipes_by_node_uuid(node_uuid)

        for pipe in connected_pipes:
            # Assuming the Pipe class has methods to set start and end positions
            if pipe.start_node_uuid == node_uuid:
                new_start_pos = self.node_manager.find_new_connection_point(pipe.start_connection)
                pipe.set_start_position(new_start_pos)
            elif pipe.end_node_uuid == node_uuid:
                new_end_pos = self.node_manager.find_new_connection_point(pipe.end_connection)
                pipe.set_end_position(new_end_pos)

            # Redraw the pipe to reflect its new position
            pipe.update_position()
    def deserialize(self, data):
        deserialized_data = json.loads(data)
        self.category = deserialized_data.get('category', 'default')  # Restore the category

        for uuid, pipe_data in deserialized_data.get('pipes', {}).items():
            pipe_class = self.get_pipe_class(pipe_data['type'])
            if pipe_class:
                pipe = pipe_class.deserialize(pipe_data, self.node_manager)
                pipe.uuid = uuid
                self.add_pipe(pipe)

                # Explicitly set the pipe's UUID to match the saved state
                pipe.uuid = uuid

                # Assuming deserialize method sets up connections, but if not:
                # start_connection = self.find_connection_by_uuid(pipe_data['start_connection_uuid'])
                # end_connection = self.find_connection_by_uuid(pipe_data['end_connection_uuid'])
                # pipe.start_connection = start_connection
                # pipe.end_connection = end_connection

                # Now add the pipe to the manager
                self.add_pipe(pipe)
    @staticmethod
    def get_pipe_class(pipe_type):
        # Define mappings from string identifiers to pipe classes
        pipe_class_map = {
            "Pipe": Pipe,
            "PhantomPipe": PhantomPipe,
            # Add other pipe types here
        }
        return pipe_class_map.get(pipe_type, None)