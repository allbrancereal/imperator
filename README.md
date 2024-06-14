# Imperator Documentation

## Overview

Imperator is a Python application built using PyQt5, designed to provide a graphical interface for creating and managing node-based workflows. It leverages a modular architecture, allowing for the dynamic registration and integration of custom node libraries and tab types. The application is structured around a central window that hosts detachable tabs, each potentially containing a unique graphical widget, such as a node graph editor.

## Features

- **Dynamic Library Registration:** NodeApp can dynamically load and register node libraries from a specified directory, making it easy to extend the application with new node types without modifying the core codebase.
- **Modular Tab System:** The application supports a detachable tab interface, where each tab can host a different type of widget. This system is designed to be extensible, allowing for the registration of custom tab types.
- **Graphical Node Editor:** One of the primary features is the graphical node editor, which allows users to visually create and manage node-based workflows. This includes adding, connecting, and configuring nodes.
- **Customizable UI:** Through the use of PyQt5, the application's user interface is highly customizable, supporting the integration of custom widgets and layouts.

## Limitations

- **Performance:** The application's performance may degrade with a very large number of nodes or complex node graphs. Performance optimizations have not been a primary focus and may require further development.
- **Documentation:** Currently, the application lacks in-depth documentation for extending the core functionality, such as adding new node types or customizing the UI further. Users looking to extend the application will need to read through the source code to understand the extension points.
- **Error Handling:** The application's error handling is basic. More robust error handling and user feedback mechanisms should be implemented, especially for operations like library loading and node graph processing.
- **Testing:** There is a lack of comprehensive unit tests, which may lead to stability issues as the application is extended or modified.
- **Platform Compatibility:** While PyQt5 supports cross-platform development, NodeApp has not been extensively tested across different operating systems. There may be platform-specific issues that need addressing.

## Getting Started

To run Imperator, you will need Python installed on your system along with the PyQt5 library. After cloning the repository, you can start the application by running the `NodeApp.py` script:


## Extending NodeApp

To extend NodeApp with new node types or tab widgets, follow these steps:

1. **Adding New Node Types:** Place your custom node library `.py` files in the `Graph/libraries` directory. Ensure each library file defines a `registered_vars` dictionary that maps unique identifiers to your custom node classes.
2. **Registering New Tab Types:** Implement your custom tab widget class and register it in the `TabTypeRegistry` within the `NodeApp` class's `__init__` method.
# Extending with Custom Nodes

The application supports the extension with custom nodes, allowing users to create specialized nodes for various purposes. This document outlines how to create and integrate a custom node, using `ReadNode` as an example.

## Creating a Custom Node

### Step 1: Define Your Node Class

Create a new Python file for your node class. Your class should inherit from the base `Node` class provided by the application. The `ReadNode` class demonstrates a custom node that includes a QLineEdit widget for inputting a file path.

Example `ReadNode` class:
```
from PyQt5.QtWidgets import QLineEdit, QWidget, QVBoxLayout from Graph.nodes import Node
class ReadNode(Node): identifier = "input.read" def init(self, x, y, width, height, name=None, library=None, tab=None, event_manager=None): super().init(x, y, width, height, name, library, tab, event_manager)
    self.widget = QWidget()
    self.layout = QVBoxLayout(self.widget)
    self.file_path_edit = QLineEdit()
    self.layout.addWidget(self.file_path_edit)
    self.default_outputs = {"output1"}

def get_file_path(self):
    return self.file_path_edit.text()

def set_file_path(self, file_path):
    self.file_path_edit.setText(file_path)
```

### Step 2: Register Your Node

In the same file, define a `registered_vars` dictionary that maps a unique identifier for your node to the node class. This allows the application to dynamically load and recognize your custom node.
```
registered_vars = {'ReadNode': ReadNode}
```
### Step 3: Implement Node Functionality

Implement the necessary functionality within your node class. For `ReadNode`, this includes methods to get and set the file path. Ensure your node handles inputs and outputs appropriately for its intended use.

## Tips for Developing Custom Nodes

- **UI Components**: Utilize PyQt5 widgets to create interactive and user-friendly node interfaces.
- **Error Handling**: Implement comprehensive error handling within your node to manage invalid inputs or processing errors.
- **Performance**: Optimize your node's performance, especially if it performs resource-intensive operations.

## Testing Your Node

After defining and registering your custom node, test it within the application to ensure it behaves as expected. Verify that the node can be added to the graph, interacts correctly with other nodes, and performs its intended function.

## Documentation

Document your custom node's functionality, inputs, and outputs. This can be within the code using docstrings or in a separate documentation file. Good documentation is essential for ensuring that others can effectively use and extend your custom node.


## Contributing

Contributions to NodeApp are welcome! Please feel free to submit pull requests with bug fixes, performance improvements, or new features. For major changes, please open an issue first to discuss what you would like to change.

## License
Please look at License.md for the license information

