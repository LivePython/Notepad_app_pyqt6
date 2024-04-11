import sys
from PyQt6.QtWidgets import QInputDialog, QFileDialog, QApplication, QMainWindow, QTextEdit, QMenuBar, QMenu
from PyQt6.QtGui import QAction, QIcon, QTextCursor, QColor
from PyQt6.QtCore import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        # Creating the PyQt window
        self.setWindowTitle("Notepad App")
        self.setGeometry(100, 100, 400, 300)

        # Setting an initial file
        self.current_file = None

        self.edit_field = QTextEdit(self)
        self.setCentralWidget(self.edit_field)

        # Creating a menubar
        menubar = QMenuBar()
        self.setMenuBar(menubar)

        # Creating file menu
        fileMenu = QMenu("File", self)
        menubar.addMenu(fileMenu)

        # Creating actions
        new_action = QAction("New", self)
        fileMenu.addAction(new_action)
        new_action.triggered.connect(self.new_file)

        save_action = QAction("Save", self)
        fileMenu.addAction(save_action)
        save_action.triggered.connect(self.save_file)

        save_as_action = QAction("Save As", self)
        fileMenu.addAction(save_as_action)
        save_as_action.triggered.connect(self.save_as_file)

        open_action = QAction("Open", self)
        fileMenu.addAction(open_action)
        open_action.triggered.connect(self.open_file)

        # Creating the edit menu
        editMenu = QMenu("Edit", self)
        menubar.addMenu(editMenu)

        # Creating the edit menu actions
        cut_action = QAction("Cut", self)
        editMenu.addAction(cut_action)
        cut_action.triggered.connect(self.edit_field.cut)

        undo_action = QAction("Undo", self)
        editMenu.addAction(undo_action)
        undo_action.triggered.connect(self.edit_field.undo)

        redo_action = QAction("Redo", self)
        editMenu.addAction(redo_action)
        redo_action.triggered.connect(self.edit_field.redo)

        copy_action = QAction("Copy", self)
        editMenu.addAction(copy_action)
        copy_action.triggered.connect(self.edit_field.copy)

        paste_action = QAction("Paste", self)
        editMenu.addAction(paste_action)
        paste_action.triggered.connect(self.edit_field.paste)
        menubar.addSeparator()

        find_action = QAction("Find", self)
        editMenu.addAction(find_action)
        find_action.triggered.connect(self.find_text)

    def new_file(self):
        self.edit_field.clear()
        self.current_file = None

    def save_as_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save", "", "All Files(*);; Python File(*.py)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.edit_field.toPlainText())
            self.current_file = file_path

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files(*);; Python File(*.py)")
        with open(file_path, 'r') as file:
            file = file.read()
        self.edit_field.setText(file)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                file.write(self.edit_field.toPlainText())
        else:
            self.save_as_file()

    def find_text(self):
        print("Searching")
        search_text, ok = QInputDialog.getText(self, "Find Text", "Search For")
        if ok:
            all_words = []
            self.edit_field.moveCursor(QTextCursor.MoveOperation.Start)
            highlight_color = QColor(Qt.GlobalColor.red)

            while(self.edit_field.find(search_text)):
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(highlight_color)

                selection.cursor = self.edit_field.textCursor()
                all_words.append(selection)
            self.edit_field.setExtraSelections(all_words)


app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())
