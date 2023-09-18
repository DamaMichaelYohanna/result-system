from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox

from PySide6.QtGui import Qt
from PySide6 import QtCore

# user import
from draw_line import QHSeparationLine, QVSeparationLine
from new_student import RegisterUI
from back_end.database import DatabaseOps


class Result(QFrame):

    def __init__(self):
        super(Result, self).__init__()
        main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        class_filter = QLabel("Class Filter")
        class_filter.setStyleSheet("padding:4px;font-size:15px;")
        class_filter_input = QComboBox()
        self.database_handle = DatabaseOps()
        classes = self.database_handle.fetch_class().fetchall()
        for item in classes:
            class_filter_input.addItem(item[0])
        class_filter_input.setStyleSheet("padding:4px;font-size:15px;")
        class_filter_input.setMinimumWidth(200)

        subject_filter = QLabel("Subject Filter")
        subject_filter.setStyleSheet("padding:4px;font-size:15px;")
        subject_filter_input = QComboBox()
        classes = self.database_handle.fetch_class().fetchall()
        for item in classes:
            subject_filter_input.addItem(item[0])
        subject_filter_input.setStyleSheet("padding:4px;font-size:15px;")
        subject_filter_input.setMinimumWidth(200)
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
        menu_layout.addWidget(class_filter_input)
        menu_layout.addWidget(subject_filter)
        menu_layout.addWidget(subject_filter_input)
        menu_layout.addWidget(QVSeparationLine())
        menu_layout.addWidget(self.search_input)
        menu_layout.addWidget(search_button)
        menu_layout.addWidget(QVSeparationLine())
        # menu_layout.addWidget(add_button)
        # menu_layout.addWidget()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setRowCount(5)
        # table.setColumnWidth(0)
        self.table.setHorizontalHeaderLabels(["Name", "Class", "First CA", "Second CA", "Assignment", "Exams"])
        self.table.setStyleSheet(
            "QTableWidget::item {font-size:18px;selection-background-color:#f5f5f5;selection-color:black;}"
            "QHeaderView {font-size:18px;}")
        # table.horizontalHeader().setStyleSheet("QHeaderView {font-size:40px};")
        self.table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        student = [["Dama Michael Yohanna ", "jss1", "20", "20", "20", "90"],
                   ["dama", "jss1", "20", "kaduna", "jamaa", "100"],
                   ["dama", "jss1", "20", "kaduna", "jamaa", "100"],
                   ["dama", "jss1", "20", "kaduna", "jamaa", "100"],
                   ["dama", "jss1", "20", "kaduna", "jamaa", "100"]]
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        start = 0
        for index, value in enumerate(student):
            item1 = QTableWidgetItem(student[index][0])
            item1.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(index, 0, item1)
            self.table.setItem(index, 1, QTableWidgetItem(student[index][1]))
            self.table.setItem(index, 2, QTableWidgetItem(student[index][2]))
            self.table.setItem(index, 3, QTableWidgetItem(student[index][3]))
            self.table.setItem(index, 4, QTableWidgetItem(student[index][4]))
            self.table.setItem(index, 4, QTableWidgetItem(student[index][5]))

        action_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_btn_callback)
        finish_btn = QPushButton("Save Record")
        finish_btn.clicked.connect(self.finish_btn_callback)
        action_layout.addWidget(clear_btn)
        action_layout.addWidget(finish_btn)
        # arrange widget to main layout
        main_layout.addLayout(menu_layout)
        main_layout.addWidget(QHSeparationLine())
        main_layout.addWidget(self.table)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)

    def finish_btn_callback(self):
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

    def delete_student_callback(self):
        me = QMessageBox.question(self, "Warning", "Are you sure you want to delete this student?"
                                                   " You will lose all the student result after this"
                                                   " action. You can Hide instead", )
        print("i was clicked")

    def update_student_callback(self):
        pass

    def search_student_callback(self):
        keyword = self.search_input.text()
        if not keyword:
            QMessageBox.information(self, "Empty!", "No search word entered")
        else:
            self.student = self.database_handle.search_record(keyword).fetchall()
            # self.populate_table()
