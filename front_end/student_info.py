from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox

from PySide6.QtGui import QIcon

# User defined import
from draw_line import QHSeparationLine, QVSeparationLine
from new_student import RegisterUI
from back_end.database import DatabaseOps


class StudentInfo(QFrame):

    def __init__(self):
        super(StudentInfo, self).__init__()
        self.database_handle = DatabaseOps()  # prepare database operation class
        main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        filter_label = QLabel("Filter Record")
        filter_label.setStyleSheet("padding:4px;font-size:15px;")
        filter_input = QComboBox()
        classes = self.database_handle.fetch_class().fetchall()
        for item in classes:
            filter_input.addItem(item[0])
        filter_input.setStyleSheet("padding:4px;font-size:15px;")
        filter_input.currentTextChanged.connect(lambda text: self.filter_class_callback(text))
        filter_input.setMinimumWidth(200)
        # filter_input.currentTextChanged.connect("me")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Records")
        self.search_input.setStyleSheet("padding:4px;font-size:15px;")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student_callback)
        search_button.setObjectName("action_button")
        add_button = QPushButton("New Student")
        add_button.clicked.connect(self.add_student_callback)
        add_button.setObjectName("action_button")

        menu_layout.addWidget(filter_label)
        menu_layout.addWidget(filter_input)
        menu_layout.addWidget(self.search_input)
        menu_layout.addWidget(search_button)
        menu_layout.addWidget(QVSeparationLine())
        menu_layout.addWidget(add_button)
        # menu_layout.addWidget()

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setRowCount(5)
        # table.setColumnWidth(0)
        self.table.setHorizontalHeaderLabels(["Name", "Gender", "Class", "Age", "State", "lga", "Action", ""])
        self.table.setStyleSheet("QTableWidget::item {border: 0px; padding: 5px;}")
        self.student = self.database_handle.fetch_record("all").fetchall()
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.populate_table()

        main_layout.addLayout(menu_layout)
        main_layout.addWidget(QHSeparationLine())
        main_layout.addWidget(self.table)

        # main_layout.addStretch()

        self.setLayout(main_layout)

    def populate_table(self):
        """function to populated table based on request"""
        if not self.student:
            QMessageBox.information(self, 'No Record!', "Record not found for entry made!")
            self.table.clearContents()
            self.table.setRowCount(0)
        else:
            self.table.setRowCount(len(self.student))
            for index, value in enumerate(self.student):
                self.table.setItem(index, 0, QTableWidgetItem(self.student[index][0]))
                self.table.setItem(index, 1, QTableWidgetItem(self.student[index][1]))
                self.table.setItem(index, 2, QTableWidgetItem(self.student[index][2]))
                self.table.setItem(index, 3, QTableWidgetItem(str(self.student[index][3])))
                self.table.setItem(index, 4, QTableWidgetItem(self.student[index][4]))
                self.table.setItem(index, 5, QTableWidgetItem(self.student[index][5]))

                delete_button = QPushButton("Delete")
                delete_image = QIcon("../images/delete.png")
                delete_button.setIcon(delete_image)
                delete_button.clicked.connect(
                    lambda text="me": self.delete_student_callback(text))
                delete_button.setStyleSheet("background:white;border:none;")

                edit_button = QPushButton("Update")
                edit_button.setToolTip("Update Information")
                edit_image = QIcon("../images/update.png")
                edit_button.setIcon(edit_image)
                edit_button.clicked.connect(self.update_student_callback)
                edit_button.setStyleSheet("background:white;border:none;")

                self.table.setCellWidget(index, 6, delete_button)
                self.table.setCellWidget(index, 7, edit_button)

    def filter_class_callback(self, key):
        """Function to filter record based on selected class"""
        self.student = self.database_handle.fetch_record(key).fetchall()
        self.populate_table()

    def add_student_callback(self):
        """Function to trigger the add new student window"""
        app = RegisterUI(self, self.database_handle)
        app.show()

    def delete_student_callback(self):
        me = QMessageBox.question(self, "Warning", "Are you sure you want to delete this student?"
                                                   " You will lose all the student result after this"
                                                   " action. You can Hide instead", )
        if me == 16384:
            self.database_handle.run_sql("DELETE FROM Student WHERE name='name'")

    def update_student_callback(self):
        pass

    def search_student_callback(self):
        keyword = self.search_input.text()
        if not keyword:
            QMessageBox.information(self, "Empty!", "No search word entered")
        else:
            self.student = self.database_handle.search_record(keyword).fetchall()
            self.populate_table()
