# SerializationManager.py
import json
import copy

class SerializationManager:
    def __init__(self, graph_widget,node_manager, pipe_manager):
        self.node_manager = node_manager
        self.pipe_manager = pipe_manager
        self.graph_widget = graph_widget
    def clone(self):
        # Create a deep copy of the PipeManager instance
        return copy.deepcopy(self)

    def serialize(self):
        # Serialize nodes
        # Serialize nodes using their own serialize method
        nodes_serialized = [node.serialize() for node in self.node_manager.nodes.values()]
        
        # Serialize pipes
        # Assuming PipeManager has a method to serialize all pipes or pipes are directly accessible
        pipes_serialized = [pipe.serialize() for pipe in self.pipe_manager.pipes.values()]
        
        # Wrap in widget state
        widget_state = {
            "type": "graph_widget",
            "nodes": nodes_serialized,
            "pipes": pipes_serialized  # Include serialized pipes in the widget state
        }


        # Wrap in tab state
        tab_state = [{
            "label": "Default Tab",
            "widget_state": widget_state
        }]

        # Convert to JSON string
        import json
        return json.dumps(tab_state, indent=4)
    
    def deserialize(self, data, ):
        # Parse the JSON string
        tab_states = json.loads(data)

        for tab_state in tab_states:
            widget_state = tab_state.get('widget_state', {})
        
            # Dictionary to log connections
            connection_dict = {}
            if widget_state.get('type') == 'graph_widget':
                # Clear existing nodes and pipes before deserializing new ones
                self.node_manager.clear_nodes()
                self.pipe_manager.clear_pipes()
                
                for node_data in widget_state.get('nodes', []):
                    # Assuming 'identifier' is now an object with a 'name' property
                    identifier_obj = node_data.get('identifier', {})  # Fetch the identifier object
                    identifier_name = identifier_obj.get('name', 'default')  # Extract the 'name' property
    
                    x = node_data.get('x', 0)
                    y = node_data.get('y', 0)
                    width = node_data.get('width', 100)
                    height = node_data.get('height', 50)
                    name = node_data.get('name')
                    library_identifier = node_data.get('library', 'default')  # Use 'default' if not specified
    
                    # Fetch the library instance from the library registry
                    library_instance = self.graph_manager.library_registry.get_library(library_identifier)
    
                    # Pass the library instance to the create_node method
                    node = self.graph_widget.create_node(identifier_name, x, y, width, height, name, library=library_instance, tab=None)
                    # Assuming each node has a unique UUID and connections are accessible
                    connection_dict[node.uuid] = node.connections


                # Assuming 'pipes' are included in the widget_state
                if 'pipes' in widget_state:
                    for pipe_data in widget_state['pipes']:
                        start_connection_uuid = pipe_data['start_connection_uuid']
                        end_connection_uuid = pipe_data['end_connection_uuid']
                        # Resolve connections
                        start_connection = connection_dict.get(start_connection_uuid)
                        end_connection = connection_dict.get(end_connection_uuid)
                        if start_connection and end_connection:
                            # Assuming PipeManager has a method create_pipe that takes start and end connections
                            self.pipe_manager.create_pipe(start_connection, end_connection)
                        else:
                            # Log an error if connections cannot be resolved
                            print(f"Error: Connections for pipe could not be found. Start UUID: {start_connection_uuid}, End UUID: {end_connection_uuid}")