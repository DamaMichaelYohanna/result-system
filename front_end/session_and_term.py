from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QDialog

from PySide6.QtGui import QIcon

from draw_line import QHSeparationLine, QVSeparationLine


class SessionAndTerm(QFrame):

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
        update_button.clicked.connect(self.update_session_callback)
        update_button.setStyleSheet("padding:8px;border-radius:0px;"
                                    "background:rgb(14, 180, 166);color:white;font-weight:bold;")
        add_button = QPushButton("New Session")
        add_button.clicked.connect(self.new_session_callback)
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
        table.setColumnCount(2)
        table.setRowCount(6)
        # table.setColumnWidth(0)
        table.setHorizontalHeaderLabels(["List Of All Sessions", "Status"])
        table.setStyleSheet("QTableWidget::item {border: 0px; padding: 5px;}")
        sessions = [["2019", "Passed", ],
                   ["2020", "Passed",],
                   ["2021", "Passed",],
                   ["2022", "Passed",],
                   ["2023", "Current",]]
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        start = 0
        for index, value in enumerate(sessions):
            table.setItem(index, 0, QTableWidgetItem(sessions[index][0]))
            table.setItem(index, 1, QTableWidgetItem(sessions[index][1]))

        main_layout.addLayout(menu_layout)
        main_layout.addWidget(QHSeparationLine())
        main_layout.addWidget(table)

        self.setLayout(main_layout)

    def new_session_callback(self):
        print("hello")
        app = NewSession(self)
        app.show()

    def update_session_callback(self):
        me = QMessageBox.question(self, "Warning", "Are you sure you want to delete this student?"
                                                   " You will lose all the student result after this"
                                                   " action. You can Hide instead", )
        print("i was clicked")

    def update_student_callback(self):
        pass


class NewSession(QDialog):
    """Dialog window for adding new session"""
    def __init__(self, parent=None):
        super(NewSession, self).__init__(parent)
        self.setFixedWidth(320)
        self.setWindowTitle("New Session")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        session_entry = QLineEdit()
        session_entry.setObjectName('entry')
        session_entry.setPlaceholderText("Enter session")
        submit_btn = QPushButton("Submit")
        submit_btn.setObjectName("submit")
        layout.addWidget(session_entry)
        layout.addWidget(submit_btn)
        self.setLayout(layout)
