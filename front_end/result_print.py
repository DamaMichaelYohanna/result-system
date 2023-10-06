import sys

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QTableWidget, QHeaderView, QVBoxLayout, \
    QLabel, QHBoxLayout, QComboBox, QLineEdit, QWidget

from front_end.draw_line import QVSeparationLine, QHSeparationLine


class PrintResult(QWidget):
    """Tab view for printing of result"""

    def __init__(self, database_handle):
        super().__init__()
        self.database_handle = database_handle
        page_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        class_filter = QLabel("Select Class")
        class_filter.setStyleSheet("padding:4px;font-size:15px;")
        self.class_filter_input = QComboBox()
        classes = self.database_handle.fetch_class().fetchall()
        for item in classes:
            self.class_filter_input.addItem(item[0])
        self.class_filter_input.setStyleSheet("padding:4px;font-size:15px;")
        self.class_filter_input.setMinimumWidth(200)
        self.class_filter_input.currentTextChanged.connect(lambda text: self.populate_subject(text))

        subject_filter = QLabel("Select Subject")
        subject_filter.setStyleSheet("padding:4px;font-size:15px;")
        self.subject_filter_input = QComboBox()
        # subject_filter_input.currentTextChanged.connect(lambda text: self.)
        self.subject_filter_input.setStyleSheet("padding:4px;font-size:15px;")
        self.subject_filter_input.setMinimumWidth(200)
        # filter_input.currentTextChanged.connect("me")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Find A Student")
        self.search_input.setStyleSheet("padding:4px;font-size:15px;")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student_callback)
        search_button.setStyleSheet("padding:8px;border-radius:0px;background:rgb(14, 180, 166);")
        # add_button = QPushButton("New Student")
        # add_button.clicked.connect(self.add_student_callback)
        # add_button.setStyleSheet("padding:8px;border-radius:0px;"
        #                          "background:rgb(14, 180, 166);color:white;font-weight:bold;")

        menu_layout.addWidget(class_filter)
        menu_layout.addWidget(self.class_filter_input)
        menu_layout.addWidget(subject_filter)
        menu_layout.addWidget(self.subject_filter_input)
        menu_layout.addWidget(QVSeparationLine())
        menu_layout.addWidget(self.search_input)
        menu_layout.addWidget(search_button)
        menu_layout.addWidget(QVSeparationLine())

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        # table.setColumnWidth(0)
        self.table.setHorizontalHeaderLabels(["Name", "Class", "First CA", "Second CA", "Exams"])
        self.table.setStyleSheet(
            "QTableWidget::item {font-size:18px;selection-background-color:#f5f5f5;selection-color:black;}"
            "QHeaderView {font-size:18px;}")
        self.table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.student = self.database_handle.fetch_record("all").fetchall()
        self.table.setRowCount(len(self.student))
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        # load student into table
        self.populate_table()

        action_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_btn_callback)
        finish_btn = QPushButton("Save Record")
        finish_btn.clicked.connect(self.finish_btn_callback)
        action_layout.addWidget(clear_btn)
        action_layout.addWidget(finish_btn)
        # arrange widget to page layout
        page_layout.addLayout(menu_layout)
        page_layout.addWidget(QHSeparationLine())
        page_layout.addWidget(self.table)
        page_layout.addLayout(action_layout)
        # page_layout.addWidget(self.result_tabs)

        self.setLayout(page_layout)

    def populate_table(self):
        """function to populated table based on request"""
        if not self.student:
            QMessageBox.information(self, 'No Record!', "Record not found for entry made!")
            self.table.clearContents()
            self.table.setRowCount(0)
            self.subject_filter_input.clear()
        else:
            self.table.setRowCount(len(self.student))
            for index, value in enumerate(self.student):
                name = QTableWidgetItem(self.student[index][0])
                name.setFlags(Qt.ItemIsEnabled)
                class_ = QTableWidgetItem(self.student[index][2])
                class_.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(index, 0, name)
                self.table.setItem(index, 1, class_)
                # self.table.setItem(index, 2, QTableWidgetItem(self.student[index][2]))
                # self.table.setItem(index, 3, QTableWidgetItem(str(self.student[index][3])))
                # self.table.setItem(index, 4, QTableWidgetItem(self.student[index][4]))
                # self.table.setItem(index, 5, QTableWidgetItem(self.student[index][5]))

    def populate_subject(self, key):
        classes = self.database_handle.fetch_subject_per_class(key).fetchall()
        self.student = self.database_handle.fetch_record(key).fetchall()
        for item in classes:
            self.subject_filter_input.addItem(item[0])
        self.populate_table()

    def finish_btn_callback(self):
        """function save data into database after finished editing"""
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                value = self.table.item(row, column)
                if value:
                    print(value.text(), end=" ")
                else:
                    continue
            print()

    def clear_btn_callback(self):
        """call back function to clear the entries """
        accept = QMessageBox.question(self, "Warning", "Are you sure you want to clear? "
                                                       "Scores will be gone")
        if accept == 16384:
            for row in range(self.table.rowCount()):
                for column in range(2, self.table.columnCount()):
                    value = self.table.item(row, column)
                    if value:
                        value.setText("")
                    else:
                        continue

    def search_student_callback(self):
        keyword = self.search_input.text()
        if not keyword:
            QMessageBox.information(self, "Empty!", "No Search Word Entered")
        else:
            self.student = self.database_handle.search_record(keyword).fetchall()
            # self.populate_table()


from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QFileDialog
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QTextCursor, QPageSize, QPageLayout, QAction


class A4Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('A4 Window Printer')

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.createActions()
        self.createMenus()

    def createActions(self):
        self.printAction = QAction('Print', self)
        self.printAction.setShortcut('Ctrl+P')
        self.printAction.triggered.connect(self.printDialog)

        self.openAction = QAction('Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.triggered.connect(self.openFile)

    def createMenus(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(self.printAction)
        fileMenu.addAction(self.openAction)

    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)', options=options)

        if file_name:
            with open(file_name, 'r') as file:
                text = file.read()
                self.text_edit.setPlainText(text)

    def printDialog(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPageSize.A4)

        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.text_edit.print_(printer)

def main():
    app = QApplication(sys.argv)
    window = A4Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
