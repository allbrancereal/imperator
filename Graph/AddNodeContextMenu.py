# AddNodeContextMenu.py
from PyQt5.QtWidgets import QMenu, QAction, QLineEdit, QWidgetAction

class AddNodeContextMenu(QMenu):
    def __init__(self,graph_widget, node_registry, parent=None):
        super().__init__(parent)
        self.node_registry = node_registry
        self.graph_widget = graph_widget
        self.initUI()

    def initUI(self):
        search_action = QWidgetAction(self)
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search...")
        search_action.setDefaultWidget(search_bar)
        self.addAction(search_action)

        self.addSeparator()

        categories = {}
        for node_name, node_instance in self.node_registry.nodes.items():
            identifier = node_instance.identifier  # Assuming identifier is 'category.name'
            category, name = identifier.split('.')  # Splitting identifier into category and name
            if category not in categories:
                categories[category] = []
            categories[category].append((identifier, name))  # Store both for later use

        # Dynamically add nodes to the menu under their categories
        for category, items in categories.items():
            category_menu = self.addMenu(category.capitalize())
            for identifier, name in items:
                action = QAction(name, self)
                # Bind the current value of identifier using a default argument in the lambda
                action.triggered.connect(lambda checked, id = identifier: self.create_node(id))
                category_menu.addAction(action)

        # Filter actions based on search input
        def filter_actions():
            text = search_bar.text().lower()
            for action in self.actions()[2:]:  # Skip the search bar and separator
                action.setVisible(text in action.text().lower())

        search_bar.textChanged.connect(filter_actions)


    def create_node(self, node_name):
        print(f"create_node called with node_name: {node_name}")  
        # Convert screen position to scene position if necessary
        scene_pos = self.graph_widget.render_manager.mapToScene(self.graph_widget.mapFromGlobal(self.pos()))
        x, y = scene_pos.x(), scene_pos.y()
        
        # Provide default values for missing parameters
        width = 100  # Default width
        height = 50  # Default height
        name = node_name  # Use node_name as the display name
        library_identifier = self.graph_widget.library_registry  # Assuming no specific library is targeted
        tab = self.graph_widget  # Assuming no specific tab is targeted
        event_manager = self.graph_widget.event_manager  # Use the GraphWidget's event manager
        
        # Call create_node with all parameters
        self.graph_widget.create_node(node_name, x, y, width, height, name, library_identifier, tab, event_manager)
