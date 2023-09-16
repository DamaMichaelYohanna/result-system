from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem,QMessageBox

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
        text_list = ["All", "JSS 1", "JSS 2", "JSS 3", "SSS 1"]
        filter_input.addItems(text_list)
        filter_input.setStyleSheet("padding:4px;font-size:15px;")
        filter_input.currentTextChanged.connect(self.filter_class_callback)
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

        table = QTableWidget()
        table.setColumnCount(7)
        table.setRowCount(5)
        # table.setColumnWidth(0)
        table.setHorizontalHeaderLabels(["Name", "Class", "Age", "State", "lga", "Action", ""])
        table.setStyleSheet("QTableWidget::item {border: 0px; padding: 5px;}")
        student = [["dama", "jss1", "20", "kaduna", "jamaa"],
                   ["dama", "jss1", "20", "kaduna", "jamaa"],
                   ["dama", "jss1", "20", "kaduna", "jamaa"],
                   ["dama", "jss1", "20", "kaduna", "jamaa"],
                   ["dama", "jss1", "20", "kaduna", "jamaa"]]
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        start = 0
        for index, value in enumerate(student):
            table.setItem(index, 0, QTableWidgetItem(student[index][0]))
            table.setItem(index, 1, QTableWidgetItem(student[index][1]))
            table.setItem(index, 2, QTableWidgetItem(student[index][2]))
            table.setItem(index, 3, QTableWidgetItem(student[index][3]))
            table.setItem(index, 4, QTableWidgetItem(student[index][4]))

            delete_button = QPushButton("Delete")
            delete_image = QIcon("../images/delete.png")
            delete_button.setIcon(delete_image)
            delete_button.clicked.connect(self.delete_student_callback)
            delete_button.setStyleSheet("background:white;border:none;")

            edit_button = QPushButton("Update")
            edit_button.setToolTip("Update Information")
            edit_image = QIcon("../images/update.png")
            edit_button.setIcon(edit_image)
            edit_button.clicked.connect(self.update_student_callback)
            edit_button.setStyleSheet("background:white;border:none;")

            table.setCellWidget(index, 5, delete_button)
            table.setCellWidget(index, 6, edit_button)
            print()
        add_student = QPushButton("Add Student")

        main_layout.addLayout(menu_layout)
        main_layout.addWidget(QHSeparationLine())
        main_layout.addWidget(table)

        # main_layout.addStretch()

        self.setLayout(main_layout)

    @staticmethod
    def filter_class_callback():
        """Function to filter record based on selected class"""
        print("i was called ")

    def add_student_callback(self):
        """Function to trigger the add new student window"""
        app = RegisterUI(self, self.database_handle)
        app.show()

    def delete_student_callback(self):
        me = QMessageBox.question(self, "Warning", "Are you sure you want to delete this student?"
                                    " You will lose all the student result after this"
                                    " action. You can Hide instead",)
        if me == 16384:
            self.database_handle.run_sql("DELETE FROM Student WHERE name='name'")

    def update_student_callback(self):
        pass

    def search_student_callback(self):
        keyword = self.search_input.text()
        if not keyword:
            QMessageBox.information(self, "Empty!", "No search word entered")
        else:
            print(self.database_handle.search_record(keyword).fetchall())