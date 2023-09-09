from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem,QMessageBox

from PySide6.QtGui import QIcon

from draw_line import QHSeparationLine, QVSeparationLine
from new_student import RegisterUI


class SessionAndTerm(QFrame):
    def btn_click(self):
        print("hello")

    def __init__(self):
        super(SessionAndTerm, self).__init__()
        main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        session_label = QLabel("Current Session")
        session_label.setStyleSheet("padding:4px;font-size:15px;")
        session_text = QLabel("2023/2023")
        session_text.setStyleSheet("padding:4px;font-size:15px;font-weight:bold;")
        # filter_input.currentTextChanged.connect("me")
        term_label = QLabel("Current Term")
        term_label.setStyleSheet("padding:4px;font-size:15px;")
        term_text = QLabel("First Term")
        term_text.setStyleSheet("padding:4px;font-size:15px;font-weight:bold;")
        update_button = QPushButton("Update Session")
        update_button.clicked.connect(self.add_student_callback)
        update_button.setStyleSheet("padding:8px;border-radius:0px;"
                                 "background:rgb(14, 180, 166);color:white;font-weight:bold;")
        add_button = QPushButton("New Session")
        add_button.clicked.connect(self.add_student_callback)
        add_button.setStyleSheet("padding:8px;border-radius:0px;"
                                 "background:rgb(14, 180, 166);color:white;font-weight:bold;")

        menu_layout.addWidget(session_label)
        menu_layout.addWidget(session_text)
        menu_layout.addWidget(QVSeparationLine())
        menu_layout.addWidget(term_label)
        menu_layout.addWidget(term_text)
        menu_layout.addWidget(update_button)
        menu_layout.addWidget(add_button)
        # menu_layout.addWidget()

        table = QTableWidget()
        table.setColumnCount(1)
        table.setRowCount(6)
        # table.setColumnWidth(0)
        table.setHorizontalHeaderLabels(["Previous Sessions", "Class", "Age", "State", "lga", "Action", ""])
        table.setStyleSheet("QTableWidget::item {border: 0px; padding: 5px;}")
        student = [["2019", "jss1", "20", "kaduna", "jamaa"],
                   ["2020", "jss1", "20", "kaduna", "jamaa"],
                   ["2021", "jss1", "20", "kaduna", "jamaa"],
                   ["2022", "jss1", "20", "kaduna", "jamaa"],
                   ["2023", "jss1", "20", "kaduna", "jamaa"]]
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