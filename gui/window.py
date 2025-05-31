from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QListWidget, QLineEdit, QPushButton,
                              QCheckBox, QListWidgetItem, QMessageBox)
from PySide6.QtCore import Qt

from db.db import AbstractDb
from tasks.task import Task

class Window(QMainWindow):
    def __init__(self, db: AbstractDb):
        super().__init__()
        # Set up our abstract DB
        self.db = db

        self.setWindowTitle("Todo List")
        self.setGeometry(100, 100, 500, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout
        self.layout = QVBoxLayout(self.central_widget)

        # Create input section
        self.create_input_section()

        # Create list section
        self.create_list_section()

        # Bottom buttons section
        self.create_bottom_buttons()

        # Display previously saved data
        self.init_from_db()

    def init_from_db(self):
        items = self.db.read_all()["tasks"]
        for task in items:
            self.add_task_to_ui(task["value"], task["done"])

    def create_input_section(self):
        """Create the input area with a text field and add button"""
        input_layout = QHBoxLayout()

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.task_input.returnPressed.connect(self.add_task)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)

        input_layout.addWidget(self.task_input, 4)
        input_layout.addWidget(self.add_button, 1)

        self.layout.addLayout(input_layout)

    def create_list_section(self):
        """Create the task list area"""
        self.task_list = QListWidget()
        self.task_list.setAlternatingRowColors(True)
        self.layout.addWidget(self.task_list)

    def create_bottom_buttons(self):
        """Create buttons for deleting and clearing tasks"""
        button_layout = QHBoxLayout()

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_selected_task)

        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all_tasks)

        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)

        self.layout.addLayout(button_layout)

    def add_task(self):
        """Add a new task to the list"""
        task_text = self.task_input.text().strip()
        if task_text:
            self.add_task_to_ui(task_text, False)
            # Write to the database
            self.db.write({"done": False, "value": task_text})
        else:
            QMessageBox.warning(self, "Empty Task", "Please enter a task first!")

    def delete_selected_task(self):
        """Delete the selected task from the list"""
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "No Selection", "Please select a task to delete.")
            return

        for item in selected_items:
            row = self.task_list.row(item)

            # Remove from GUI
            self.task_list.takeItem(row)

            # Remove from DB
            self.db.remove(row)

    def clear_all_tasks(self):
        """Clear all tasks from the list"""
        confirm = QMessageBox.question(
            self, "Confirm Clear All",
            "Are you sure you want to clear all tasks?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.task_list.clear()
            self.db.clear()

    def task_state_changed(self, state: int):
        """Handle when a task is checked or unchecked"""
        checkbox = self.sender()

        # Set strikethrough text style for completed tasks
        font = checkbox.font()
        font.setStrikeOut(state == Qt.CheckState.Checked.value)
        checkbox.setFont(font)

        # Set value to DB
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            item_widget = self.task_list.itemWidget(item)

            if item_widget == checkbox:
                self.db.set_checked(i, state == Qt.CheckState.Checked.value)

    def add_task_to_ui(self, value: str, status: bool):
        # Create list item with checkbox
        item = QListWidgetItem()
        self.task_list.addItem(item)

        # Create checkbox widget
        checkbox = QCheckBox(value)
        checkbox.stateChanged.connect(self.task_state_changed)
        checkbox.setChecked(status)

        # Set item widget
        self.task_list.setItemWidget(item, checkbox)

        # Clear the input field
        self.task_input.clear()
        self.task_input.setFocus()

