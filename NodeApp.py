import sys
import threading
from PyQt5.QtWidgets import QApplication,QGraphicsScene
from Window import Window
# Remove the import statement for GraphWidget from here
from PythonEnvironmentWidget import PythonEnvironmentWidget
from DetachableTabWidget import DetachableTabWidget
from library_registry import LibraryRegistry
import os
import importlib
from Graph.RenderManager import RenderManager
from Graph.GraphCore import GraphCore
def register_libraries(library_registry):
    # Get the directory of the current file
    dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Graph','libraries')

    # Iterate over all files in the directory
    for filename in os.listdir(dir_path):
        # Check if the file is a .py file
        if filename.endswith('.py'):
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
                # Register each library in 'registered_vars' in the library registry
                for library_identifier, LibraryClass in module.registered_vars.items():
                    library_registry.register_library(LibraryClass.identifier, LibraryClass)
                    print(f"Registered library: {LibraryClass.identifier}")
                    
class TabTypeRegistry:
    def __init__(self):
        self.tab_types = {}

    def register(self, identifier, TabClass):
        self.tab_types[identifier] = TabClass
        
    def create(self, identifier, *args, **kwargs):
        if identifier in self.tab_types:
            return self.tab_types[identifier](*args, **kwargs)
        else:
            return None
        


    
                    
class NodeApp(QApplication):
    def __init__(self, sys_argv):
        super(NodeApp, self).__init__(sys_argv)
        self.windows = []
        
        self.library_registry = LibraryRegistry()
        # Create a TabTypeRegistry and register the GraphWidget class
        self.tab_type_registry = TabTypeRegistry()
        from GraphWidget import GraphWidget
        self.tab_type_registry.register('graph_widget', GraphWidget)
        
        self.graph_core = GraphCore(self.library_registry, RenderManager)
        # Create the initial window
        self.create_window()
        
    def reorder_tab_bars(self):
        # Code to reorder tab bars goes here
        pass
        
    def create_window(self):
        window = Window(self)
        window.show()

        # Connect the destroyed signal to the remove_window method
        window.destroyed.connect(self.remove_window)
        register_libraries(self.library_registry)
        
        # Assuming you have a method to create and setup the QGraphicsScene...
        scene = QGraphicsScene()
        # Create the DetachableTabWidget and add the default tab
        detachable_tab_widget = DetachableTabWidget(self, window.custom_tab_bar)
        graphWidgetInstance = self.tab_type_registry.create('graph_widget', self, self.library_registry, None, self.graph_core)
    
        if graphWidgetInstance is not None:
            # Now that we have a GraphWidget instance, create RenderManager
            # Update the GraphWidget instance with the newly created RenderManager
            self.render_manager = RenderManager(scene, graphWidgetInstance)
            graphWidgetInstance.real_init( self, self.library_registry, self.render_manager, self.graph_core)
            label = "Default Tab"
            window.add_tab(label, graphWidgetInstance)

            detachable_tab_widget.addTab(graphWidgetInstance, label)
            # Set the DetachableTabWidget as the central widget for the window
            window.set_central_widget(detachable_tab_widget)

        self.windows.append(window)
        
    def remove_window(self, _):
        # Remove the window from the app's list of windows
        for window in self.windows:
            if window is self.sender():
                self.windows.remove(window)
                break
        
if __name__ == "__main__":
    app = NodeApp(sys.argv)  # Pass sys.argv to NodeApp
    sys.exit(app.exec_())