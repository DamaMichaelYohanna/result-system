from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QWidget

from PySide6.QtGui import Qt
from PySide6 import QtCore

# user import
from draw_line import QHSeparationLine, QVSeparationLine
from new_student import RegisterUI
from back_end.database import DatabaseOps


class Result(QFrame):
    """UI page for result section"""

    def __init__(self, database_handle):
        super(Result, self).__init__()
        self.database_handle = database_handle
        self.result_tabs = QTabWidget()

        self.result_tabs.addTab(PreviewResult(), "Preview Result")
        self.result_tabs.addTab(AddResult(), "New Entry")
        self.result_tabs.addTab(PrintResult(), "Print Result")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.result_tabs)
        self.setLayout(main_layout)


class AddResult(QWidget):
    """Tab view for adding of result"""

    def __init__(self):
        super().__init__()

        page_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        class_filter = QLabel("Select Class")
        class_filter.setStyleSheet("padding:4px;font-size:15px;")
        self.class_filter_input = QComboBox()
        self.database_handle = DatabaseOps()
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

    def add_student_callback(self):
        print("hello")
        app = RegisterUI(self)
        app.show()

    def search_student_callback(self):
        keyword = self.search_input.text()
        if not keyword:
            QMessageBox.information(self, "Empty!", "No Search Word Entered")
        else:
            self.student = self.database_handle.search_record(keyword).fetchall()
            # self.populate_table()


class PrintResult(QWidget):
    """Tab view for printing of result"""

    def __init__(self):
        super().__init__()

        page_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        class_filter = QLabel("Select Class")
        class_filter.setStyleSheet("padding:4px;font-size:15px;")
        self.class_filter_input = QComboBox()
        self.database_handle = DatabaseOps()
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


class PreviewResult(QWidget):
    """Tab view for adding of result"""

    def __init__(self):
        super().__init__()

        page_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        class_filter = QLabel("Select Class")
        class_filter.setStyleSheet("padding:4px;font-size:15px;")
        self.class_filter_input = QComboBox()
        self.database_handle = DatabaseOps()
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
