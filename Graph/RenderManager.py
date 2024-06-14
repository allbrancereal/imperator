from PyQt5.QtWidgets import QGraphicsView, QGraphicsRectItem, QGraphicsSceneMouseEvent,QGraphicsItem
from PyQt5.QtCore import QRectF, QPointF, Qt, pyqtSignal
from PyQt5.QtGui import QPen, QBrush, QColor
from Graph.AddNodeContextMenu import AddNodeContextMenu
from Graph.RenderWidgets import BezierConnection, DraggableNode, InputHandle, OutputHandle

class RenderManager(QGraphicsView):
    # Define a custom signal. For example, nodeAdded, which passes a reference to the added node
    nodeAdded = pyqtSignal(object)

    def __init__(self, scene, graph_widget):
        super().__init__()
        self.scene = scene
        self.setScene(scene)
        self.graph_widget = graph_widget
        self.setGeometry(graph_widget.geometry()) 
        self.draggingItem = None

        
    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item is None:
            context_menu = AddNodeContextMenu(self.graph_widget, self.graph_widget.graph_core.node_manager, self)
            global_pos = self.mapToGlobal(event.pos())
            context_menu.exec_(global_pos)

    def addNode(self, node):
        try:
            # Create the graphical representation of the node
            rect_item = QGraphicsRectItem(QRectF(node.position.x(), node.position.y(), 100, 50))
            rect_item.setBrush(QBrush(QColor(200, 200, 250)))
            rect_item.setPen(QPen(QColor(0, 0, 0)))
            rect_item.setFlags(QGraphicsItem.ItemIsSelectable)
            self.scene.addItem(rect_item)
        
            # Link the graphical representation with the node instance
            node.setGraphicsItem(rect_item)
        
            # Add handles or other graphical elements related to the node
            self.addHandles(node)
        
            # Connect signals for node movement or other interactions
            node.graphicsItem.nodeMoved.connect(self.onNodeMoved)
        except AttributeError as e:
            print(f"Error adding node: {e}")
    def onNodeMoved(self, newPos):
        # Handle node movement, such as updating connections
        print(f"Node moved to {newPos}")
        # Add logic to update connections here
    def removeNode(self, node):
        # Assuming each node has a graphical representation (QGraphicsItem) stored in it
        if node.graphicsItem:
            self.scene.removeItem(node.graphicsItem)
            node.graphicsItem = None

    def hideHandles(self, node):
        # Assuming node handles are stored in a list within the node
        for handle in node.handles:
            handle.setVisible(False)

    def showHandles(self, node):
        for handle in node.handles:
            handle.setVisible(True)
            
    def addHandles(self, node):
        for input in node.inputs:
            handle = InputHandle(node.position, input)
            self.scene.addItem(handle)
            # Connect the InputHandle's signals
            handle.connectionDragStarted.connect(self.handleConnectionDragStarted)
            handle.connectionDropped.connect(self.handleConnectionDropped)
            handle.connectionMade.connect(self.handleConnectionMade)

        for output in node.outputs:
            handle = OutputHandle(node.position, output)
            self.scene.addItem(handle)
            # Connect the OutputHandle's signals
            handle.connectionDragStarted.connect(self.handleConnectionDragStarted)
            handle.connectionDropped.connect(self.handleConnectionDropped)
            handle.connectionMade.connect(self.handleConnectionMade)

    def onNodeAdded(self, node):
        # Implement the logic that should occur when a node is added
        print(f"Node added: {node}")
        
    def handleConnectionMade(self, output_handle, input_handle):
        self.connectNodes(output_handle, input_handle)
    def handleConnectionDragStarted(self, output_handle):
        # Placeholder for logic to handle the start of a connection drag
        print(f"Connection drag started from {output_handle}")
    def handleConnectionDropped(self, output_handle, input_handle):
        self.disconnectNodes(output_handle, input_handle)
    def connectNodes(self, output_handle, input_handle):
        # Create a new BezierConnection
        connection = BezierConnection(output_handle.pos(), input_handle.pos())
        self.scene.addItem(connection)
    
        # Update handles and nodes with the new connection
        output_handle.connections.append(connection)
        input_handle.connection = connection
        output_handle.node.output_connections.append(connection)  # Assuming nodes have a list to store connections
        input_handle.node.input_connections.append(connection)
    
        # Connect signals for updating the connection when nodes move
        output_handle.node.nodeMoved.connect(connection.updateStartPoint)
        input_handle.node.nodeMoved.connect(connection.updateEndPoint)
    
        # Emit signal indicating a connection has been made
        input_handle.connectionMade.emit(output_handle, input_handle)
        output_handle.connectionMade.emit(output_handle, input_handle)


    def disconnectNodes(self, output_handle, input_handle):
        connection = input_handle.connection
        if connection and connection in output_handle.connections:
            output_handle.connections.remove(connection)
            input_handle.connection = None
            self.scene.removeItem(connection)
            
    def handleMousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.handleRightClick(event)
        elif event.button() == Qt.LeftButton:
            self.handleLeftClick(event)
        super().mousePressEvent(event)

    def handleRightClick(self, event):
        item = self.itemAt(event.pos())
        if item is None:
            context_menu = AddNodeContextMenu(self.graph_widget, self.graph_widget.graph_core.node_registry, self)
            global_pos = self.mapToGlobal(event.pos())
            context_menu.exec_(global_pos)

    def handleLeftClick(self, event):
        item = self.itemAt(event.pos())
        if isinstance(item, (InputHandle, OutputHandle, BezierConnection)):
            self.draggingItem = item
            self.draggingItemType = type(item)
            self.lastMousePosition = event.pos()

    def handleMouseMoveEvent(self, event):
        if self.draggingItem:
            scenePos = self.mapToScene(event.pos())
            if isinstance(self.draggingItem, BezierConnection):
                # Assuming BezierConnection has methods to update start/end points
                if self.draggingItemType == OutputHandle:  # Dragging from output
                    self.draggingItem.updateStartPoint(scenePos)
                elif self.draggingItemType == InputHandle:  # Dragging from input
                    self.draggingItem.updateEndPoint(scenePos)
            elif isinstance(self.draggingItem, (InputHandle, OutputHandle)):
                # Move the handle to the new position
                self.draggingItem.setPos(scenePos)
            self.scene.update()  # Refresh the scene to reflect changes
        super().mouseMoveEvent(event)

    def handleMouseReleaseEvent(self, event):
        if self.draggingItem:
            scenePos = self.mapToScene(event.pos())
            targetItem = self.scene.itemAt(scenePos, self.transform())
            if isinstance(self.draggingItem, BezierConnection):
                # Check if we're releasing on a valid handle to connect
                if isinstance(targetItem, InputHandle) and self.draggingItemType == OutputHandle:
                    self.connectNodes(self.draggingItem.outputHandle, targetItem)
                elif isinstance(targetItem, OutputHandle) and self.draggingItemType == InputHandle:
                    self.connectNodes(targetItem, self.draggingItem.inputHandle)
            elif isinstance(self.draggingItem, (InputHandle, OutputHandle)):
                # For handles, check if they should be connected to a node or another handle
                if isinstance(targetItem, (InputHandle, OutputHandle)):
                    # Implement logic to connect handles if applicable
                    pass
            # Reset dragging state
            self.draggingItem = None
            self.draggingItemType = None
        super().mouseReleaseEvent(event)

        
    def reconnect_connection(self, connection, old_start_node, new_start_node, old_end_node, new_end_node):
        # Validate the new connection
        if not self.validate_connection(new_start_node, new_end_node):
            print("Invalid connection. Reconnection not performed.")
            return  # Exit if the connection is not valid
        # Disconnect from old nodes if the connection was previously established
        if connection in old_start_node.output_connections:
            old_start_node.remove_connection(connection)
        if connection in old_end_node.input_connections:
            old_end_node.remove_connection(connection)
    
        # Connect to new nodes
        new_start_node.add_connection(connection, output=True)
        new_end_node.add_connection(connection, output=False)
    
        # Update the connection's start and end points
        connection.set_start_point(new_start_node.position)
        connection.set_end_point(new_end_node.position)
            

    def validate_connection(self, new_start_node, new_end_node):
        # Check if either new_start_node or new_end_node is None
        if new_start_node is None or new_end_node is None:
            return False
        # Check if new_start_node and new_end_node are the same
        if new_start_node == new_end_node:
            return False
        # Add more validation rules as needed
        return True
