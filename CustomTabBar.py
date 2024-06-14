from PyQt5.QtWidgets import QTabBar, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtWidgets import QTabBar, QTabWidget, QApplication
class CustomTabBar(QTabBar):
    tabDetachSignal = pyqtSignal(int, QPoint)
    
    def __init__(self, window, parent=None):  # Add a window argument
        super().__init__(parent)
        self.window = window  # Store the window instance
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)
        self._dragStartPos = None
        
        # Add a tab_widget attribute
        self.tab_widget = QTabWidget(self)
        # Remove the creation of the DetachableTabWidget and the addition of the default tab
        # self.tab_widget = DetachableTabWidget(self.window, self)
        # widget = GraphWidget()
        # label = "Default Tab"
        # self.tab_widget.addTab(widget, label)

        
    def __call__(self, widget, label):
        # This method will be called when you use an instance of CustomTabBar like a function.
        # You can put any code you want here. For example, you might want to create a new tab:
        self.tab_widget.addTab(widget, label)
        
    def mouseMoveEvent(self, event):
        if not event.buttons() & Qt.LeftButton:
            return
        if (event.pos() - self._dragStartPos).manhattanLength() < QApplication.startDragDistance():
            return
        self.tabDetachSignal.emit(self.tabAt(self._dragStartPos), event.pos())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragStartPos = event.pos()
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        #context_menu = QMenu(self)

        #split_horizontally_action = QAction("Split Horizontally", self)
        #split_horizontally_action.triggered.connect(self.split_horizontally)
        #context_menu.addAction(split_horizontally_action)

        #split_vertically_action = QAction("Split Vertically", self)
        #split_vertically_action.triggered.connect(self.split_vertically)
        #context_menu.addAction(split_vertically_action)

        #context_menu.exec_(event.globalPos())
        pass;
     


    def split_horizontally(self):
        # Import GraphWidget here
        from GraphWidget import GraphWidget
        # Call split_horizontally on self.window
        self.window.split_horizontally()

    def split_vertically(self):
        # Import GraphWidget here
        from GraphWidget import GraphWidget
        # Call split_vertically on self.window
        self.window.split_vertically()
        
    def show_context_menu(self, point):
        menu = QMenu(self)
        detach_action = QAction("Detach", self)
        menu.addAction(detach_action)
        menu.exec_(self.mapToGlobal(point))


    def detach_tab(self):
        index = self.currentIndex()
        if index >= 0:
            # Get the widget from the tab
            widget = self.tab_widget.widget(index)
            label = self.tab_widget.tabText(index)

            # Remove the tab from the tab widget
            self.tab_widget.removeTab(index)

            # Create a new window
            new_window = self.window.__class__(self.window.app)

            # Add the widget to the new window
            new_window.custom_tab_bar.tab_widget.addTab(widget, label)

            # If there are no more tabs in this CustomTabBar
            if self.tab_widget.count() == 0:
                # Get the parent window
                parent_window = self.window

                # Remove this CustomTabBar from the grid layout
                parent_window.grid_layout.removeWidget(self)
                self.setParent(None)

                # Re-order the remaining CustomTabBar instances
                parent_window.reorder_tab_bars()