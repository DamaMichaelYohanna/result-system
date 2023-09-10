from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem,QMessageBox

from PySide6.QtGui import QIcon

from draw_line import QHSeparationLine, QVSeparationLine
from new_student import RegisterUI


class Result(QFrame):

    def __init__(self):
        super(Result, self).__init__()
        main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        filter_label = QLabel("Filter By Class")
        filter_label.setStyleSheet("padding:4px;font-size:15px;")
        filter_input = QComboBox()
        text_list = ["All", "JSS 1", "JSS 2", "JSS 3", "SSS 1"]
        filter_input.addItems(text_list)
        filter_input.setStyleSheet("padding:4px;font-size:15px;")
        filter_input.setMinimumWidth(200)
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

        menu_layout.addWidget(filter_label)
        menu_layout.addWidget(filter_input)
        menu_layout.addWidget(self.search_input)
        menu_layout.addWidget(search_button)
        menu_layout.addWidget(QVSeparationLine())
        # menu_layout.addWidget(add_button)
        # menu_layout.addWidget()

        table = QTableWidget()
        table.setColumnCount(6)
        table.setRowCount(2)
        # table.setColumnWidth(0)
        table.setHorizontalHeaderLabels(["Name", "Class", "First CA", "Second CA", "Assignment", "Exams"])
        table.setStyleSheet("QTableWidget::item {border: 10px; padding: 5px;color:red;font-style:bolder;}")
        student = [["Dama Michael Yohanna ", "jss1", "20", "20", "20", "90"],
                   ["dama", "jss1", "20", "kaduna", "jamaa", "100"],
                   ["dama", "jss1", "20", "kaduna", "jamaa", "100"],
                   ["dama", "jss1", "20", "kaduna", "jamaa", "100"],
                   ["dama", "jss1", "20", "kaduna", "jamaa", "100"]]
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        start = 0
        for index, value in enumerate(student):
            table.setItem(index, 0, QTableWidgetItem(student[index][0]))
            table.setItem(index, 1, QTableWidgetItem(student[index][1]))
            table.setItem(index, 2, QTableWidgetItem(student[index][2]))
            table.setItem(index, 3, QTableWidgetItem(student[index][3]))
            table.setItem(index, 4, QTableWidgetItem(student[index][4]))
            table.setItem(index, 4, QTableWidgetItem(student[index][5]))

        main_layout.addLayout(menu_layout)
        main_layout.addWidget(QHSeparationLine())
        main_layout.addWidget(table)

        # main_layout.addStretch()

        self.setLayout(main_layout)

    def add_student_callback(self):
        print("hello")
        app = RegisterUI(self)
        app.show()

    def delete_student_callback(self):
        me = QMessageBox.question(self, "Warning", "Are you sure you want to delete this student?"
                                    " You will lose all the student result after this"
                                    " action. You can Hide instead",)
        print("i was clicked")

    def update_student_callback(self):
        pass

    def search_student_callback(self):
        keyword = self.search_input.text()
        if not keyword:
            pass
        else:
            print(keyword)