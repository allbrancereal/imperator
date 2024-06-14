from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget,QMainWindow, QMenu, QAction
from PyQt5.QtCore import pyqtSignal, QPoint, Qt
from CustomTabBar import CustomTabBar
class DetachableTabWidget(QTabWidget):
    def __init__(self, node_app , tabBar, parent=None):
        super().__init__(parent)

        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)
        self.app = node_app;
        self.tabBar = tabBar  # Assign the tabBar attribute to the CustomTabBar instance
        self.setTabBar(self.tabBar)

        # Connect the tabDetachSignal to the detach_tab method
        self.tabBar.tabDetachSignal.connect(self.detach_tab)

        self._dragStartPos = None
        self.detached_tabs = []  # Keep track of the detached tabs
        # Connect the destroyed signal to the reorder_tab_bars method of the parent window
        self.destroyed.connect(self.app.reorder_tab_bars)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragStartPos = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self._dragStartPos).manhattanLength() < QApplication.startDragDistance():
            return

        index = self.tabBar.tabAt(self._dragStartPos)
        if index >= 0:
            self.tabBar.tabDetachSignal.emit(index, event.pos())
       


    def removeTab(self, index):
        super().removeTab(index)

        # If there are no more tabs left, schedule this widget for deletion
        if self.count() == 0:
            self.deleteLater()

    def detach_tab(self, index, point):
        # Get the original widget
        original_widget = self.widget(index)
        title = self.tabText(index)

        # Clone the widget if it has a clone method, otherwise create a new instance of its class
        if hasattr(original_widget, 'clone'):
            cloned_widget = original_widget.clone()
        else:
            cloned_widget = original_widget.__class__(self)  # Pass self as the parent

        # Remove the tab from the original DetachableTabWidget
        self.removeTab(index)
        
        # Create a new CustomTabBar for the detached tab
        new_tab_bar = CustomTabBar(self.app, self)

        # Create a new DetachableTabWidget for the detached tab
        new_widget = DetachableTabWidget(self.app, new_tab_bar, self)
        new_widget.addTab(cloned_widget, title)
        # Create a new window and set the new DetachableTabWidget as its central widget
        new_window = self.parent().__class__(self.parent().app)
        new_window.setCentralWidget(new_widget)

        # Show the new window
        new_window.show()

        # Add the detached tab to the list of detached tabs
        self.detached_tabs.append(new_window)

        # Close the original window if there are no more tabs left
        if self.count() == 0:
            self.parent().deleteLater()


    def serialize_tabs(self):
        serialized_data = []
        for i in range(self.count()):
            widget = self.widget(i)
            label = self.tabText(i)
            serialized_data.append({
                'label': label,
                'widget_state': widget.serialize()  # Assumes each widget has a serialize method
            })
        return serialized_data
    def remove_detached_window(self, _):
        # Remove the window from the list of detached tabs
        for window in self.detached_tabs:
            if window is self.sender():
                self.detached_tabs.remove(window)
                print(f"Removed window. Number of detached tabs: {len(self.detached_tabs)}")  # Add this line
                break
    # ...
    def clone(self):
        # Create a new DetachableTabWidget
        new_widget = DetachableTabWidget(self.tabBar, self.parent())

        # Copy the tabs from this widget to the new widget
        for i in range(self.count()):
            widget = self.widget(i)
            new_widget.addTab(widget, self.tabText(i))

        return new_widget
