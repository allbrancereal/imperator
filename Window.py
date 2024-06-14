from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget,QTabWidget
from PyQt5.QtCore import pyqtSlot
from CustomTabBar import CustomTabBar
import uuid
from DetachableTabWidget import DetachableTabWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QWidget,QSplitter
from PyQt5.QtWidgets import QMenu, QAction
import json
from PyQt5.QtWidgets import QFileDialog

class Window(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("NodeApp Window")
        self.setGeometry(100, 100, 800, 600)

        # Create a QSplitter
        self.splitter = QSplitter()

        # Create a CustomTabBar and add it to the QSplitter
        self.custom_tab_bar = CustomTabBar(self)
        self.splitter.addWidget(self.custom_tab_bar)

        # Set the QSplitter as the central widget
        self.setCentralWidget(self.splitter)

        # Add the window to the app's list of windows
        self.app.windows.append(self)



        # Create a dictionary to store buttons by UUID
        self.buttons = {}
        self.tabs = []

        # Connect the tabDetachSignal to the detach_tab method
        
        
        # Connect the destroyed signal to the remove_window method
        self.destroyed.connect(self.app.remove_window)

        # Add the window to the app's list of windows
        self.app.windows.append(self)
        
        # Create a menu bar
        menu_bar = self.menuBar()

        # Create a "File" menu
        file_menu = QMenu("File", self)
        new_action = QAction("New", self)
        save_action = QAction("Save", self)
        load_action = QAction("Load", self)
        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

        # Create an "Edit" menu
        edit_menu = QMenu("Edit", self)
        cut_action = QAction("Cut", self)
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)

        # Add the menus to the menu bar
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)

        # Connect the actions to methods
        new_action.triggered.connect(self.new_file)
        save_action.triggered.connect(self.save_file)
        load_action.triggered.connect(self.load_file)
        cut_action.triggered.connect(self.cut)
        copy_action.triggered.connect(self.copy)
        paste_action.triggered.connect(self.paste)
        
    def add_tab(self, label, widget):
        self.tabs.append((label, widget))
        self.custom_tab_bar.tab_widget.addTab(widget, label)
    def new_file(self):
        # Create a new window
        self.app.create_window()
        
    def save_file(self):
        print("Opening file dialog...")
        file_name, _ = QFileDialog.getSaveFileName(self, "Save file", "", "JSON Files (*.json)")
        if file_name:
            print(f"Saving to file: {file_name}")
            try:
                # Get the DetachableTabWidget instance
                detachable_tab_widget = self.centralWidget()

                # Serialize the tabs in the DetachableTabWidget
                data = detachable_tab_widget.serialize_tabs()

                print(f"Serialized data: {data}")
                with open(file_name, 'w') as f:
                    json.dump(data, f)
                print("File saved.")
            except Exception as e:
                print(f"Error during serialization: {e}")
        else:
            print("No file selected.")
    def load_file(self):
        print("Opening file dialog...")
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", "", "JSON Files (*.json)")
        if file_name:
            print(f"Reading file: {file_name}")
            with open(file_name, 'r') as f:
                data = json.load(f)
            print(f"Read data: {data}")
            if self.custom_tab_bar.tab_widget is not None:
                self.custom_tab_bar.tab_widget.clear()
        
            for tab_data in data:
                # Create the tab
                TabClass = self.app.tab_type_registry.create(tab_data['widget_state']['type'], self.app, self.app.library_registry)

                if TabClass is not None:
                    tab = TabClass(self.app)
                    # Create a DetachableTabWidget and add the tab to it
                    new_tab_bar = CustomTabBar(self.app, self)
                    detachable_tab_widget = DetachableTabWidget(self.app, new_tab_bar, self)
                    detachable_tab_widget.addTab(tab, tab_data['label'])
                    # Add the DetachableTabWidget to the window
                    self.set_central_widget(detachable_tab_widget)
                    # Deserialize the nodes and add them to the tab
                    tab.deserialize(tab_data)
        else:
            print("No file selected.")



    def cut(self):
        # Cut the selected text from the active tab
        self.tabs.currentWidget().cut()

    def copy(self):
        # Copy the selected text from the active tab
        self.tabs.currentWidget().copy()

    def paste(self):
        # Paste the clipboard contents into the active tab
        self.tabs.currentWidget().paste()
    def split_horizontally(self):
        # Create a new CustomTabBar
        new_tab_bar = CustomTabBar(self)

        # Create a new QSplitter
        new_splitter = QSplitter()

        # Check if self.splitter is not None
        if self.splitter is not None:
            # Move the widgets from the old splitter to the new splitter
            while self.splitter.count():
                new_splitter.addWidget(self.splitter.widget(0))

        # Add the new CustomTabBar to the new QSplitter
        new_splitter.addWidget(new_tab_bar)

        # Replace the old splitter with the new splitter
        self.splitter = new_splitter
        self.setCentralWidget(self.splitter)

    def split_vertically(self):
        # Create a new CustomTabBar
        new_tab_bar = CustomTabBar(self)

        # Create a new QSplitter and set its orientation to vertical
        new_splitter = QSplitter()
        new_splitter.setOrientation(Qt.Vertical)

        # Move the widgets from the old splitter to the new splitter
        while self.splitter.count():
            new_splitter.addWidget(self.splitter.widget(0))

        # Add the new CustomTabBar to the new QSplitter
        new_splitter.addWidget(new_tab_bar)

        # Replace the old splitter with the new splitter
        self.splitter.setParent(None)
        self.splitter = new_splitter
        self.setCentralWidget(self.splitter)
            
    def deleteLater(self):
        # Remove the window from the app's list of windows
        if self in self.app.windows:
            self.app.windows.remove(self)

        # Call the deleteLater method of the superclass
        super().deleteLater()
        

    def closeEvent(self, event):
        # Remove the window from the app's list of windows
        if self in self.app.windows:
            self.app.windows.remove(self)

        # Call the deleteLater method and accept the event
        self.deleteLater()
        event.accept()  # Accept the event to ensure the window is closed
        
    @pyqtSlot()
    def add_button(self):
        # Create a new button
        button = QPushButton("Button", self)

        # Assign the button a UUID
        button_uuid = uuid.uuid4()
        self.buttons[button_uuid] = button

        # Add the button to the current tab
        current_tab = self.tab_widget.currentWidget()
        if current_tab is not None:
            current_tab.layout().addWidget(button)
            
    def clone_tab(self):
        # Create a new window
        new_window = Window(self.app)

        # Move the tab to the new window
        if self.custom_tab_bar.tab_widget.count() > 0:
            widget = self.custom_tab_bar.tab_widget.widget(0)
            self.custom_tab_bar.tab_widget.removeTab(0)
            new_window.custom_tab_bar.tab_widget.addTab(widget, widget.windowTitle())

        # If the original window is now empty, close it
        if self.custom_tab_bar.tab_widget.count() == 0:
            self.close()

        # Show the new window
        new_window.show()
            
    def clone_window(self):
        # Create a new window
        new_window = Window(self.app)

        # Copy the state of the original window
        # In this case, we'll just copy the buttons
        for button_uuid, button in self.buttons.items():
            new_button = QPushButton(button.text(), new_window)
            new_window.buttons[button_uuid] = new_button

            # Add the new button to the corresponding tab in the new window
            # This assumes that the tabs in the new window have the same order as in the original window
            tab_index = self.tab_widget.indexOf(button.parent())
            new_tab = new_window.tab_widget.widget(tab_index)
            if new_tab is not None:
                new_tab.layout().addWidget(new_button)

        # Show the new window
        new_window.show()

        

    def remove_window(self):
        # Remove this window from the app's list of windows
        self.app.windows.remove(self)
    def reorder_tab_bars(self):
        # Check if self.custom_tab_bar.tab_widget is None
        if self.custom_tab_bar.tab_widget is not None:
            # Get the current index of the tab bar
            current_index = self.custom_tab_bar.tab_widget.currentIndex()

            # Get the total number of tabs
            total_tabs = self.custom_tab_bar.tab_widget.count()

            # If the current index is not the last one, move it to the end
            if current_index != total_tabs - 1:
                self.custom_tab_bar.tab_widget.tabMove(current_index, total_tabs - 1)

            # Update the current index
            self.custom_tab_bar.tab_widget.setCurrentIndex(total_tabs - 1)
            
    def set_central_widget(self, widget):
        self.setCentralWidget(widget)
    def detach_tab(self, index):
        # Create a new window
        new_window = Window(self.app)

        # Move the tab to the new window
        widget = self.custom_tab_bar.tab_widget.widget(index)
        self.custom_tab_bar.tab_widget.removeTab(index)
        new_window.custom_tab_bar.tab_widget.addTab(widget, widget.windowTitle())

        # Show the new window
        new_window.show()

    def reattach_tab(self, index, window):
        # Move the tab from the other window to this window
        widget = window.custom_tab_bar.tab_widget.widget(index)
        window.custom_tab_bar.tab_widget.removeTab(index)
        self.custom_tab_bar.tab_widget.addTab(widget, widget.windowTitle())

        # If the other window is now empty, close it
        if window.custom_tab_bar.tab_widget.count() == 0:
            window.close()

            
    def add_widget(self, widget_class, tab_title):
        # Create a new widget
        widget = widget_class()

        # Add the widget to a new tab
        self.tab_widget.addTab(widget, tab_title)

    def remove_widget(self, index):
        # Remove the widget at the specified index
        self.tab_widget.removeTab(index)