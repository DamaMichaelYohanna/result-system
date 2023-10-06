from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QCheckBox

from PySide6.QtGui import QIcon

from draw_line import QHSeparationLine, QVSeparationLine


class SessionAndTerm(QFrame):

    def __init__(self, database_handle):
        super(SessionAndTerm, self).__init__()
        self.database_handle = database_handle
        main_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        session_label = QLabel("Current Session")
        session_label.setStyleSheet("padding:4px;font-size:15px;")
        # fetch session from the database
        current_session = self.database_handle.run_sql("SELECT name FROM Session WHERE status = 'current'").fetchone()
        if current_session:
            session_text = QLabel(current_session[0])
        else:
            session_text = QLabel(current_session)
        session_text.setStyleSheet("padding:4px;font-size:15px;font-weight:bold;")
        # filter_input.currentTextChanged.connect("me")
        term_label = QLabel("Current Term")
        term_label.setStyleSheet("padding:4px;font-size:15px;")
        current_term = self.database_handle.run_sql("SELECT name FROM Term WHERE status = 'current'").fetchone()[0]
        term_text = QLabel(f"{current_term} Term")
        term_text.setStyleSheet("padding:4px;font-size:15px;font-weight:bold;")
        update_button = QPushButton("Update Term")
        update_button.clicked.connect(self.update_term_callback)
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
        # sessions = [["2019", "Passed", ],
        #            ["2020", "Passed",],
        #            ["2021", "Passed",],
        #            ["2022", "Passed",],
        #            ["2023", "Current",]]
        sessions = self.database_handle.fetch_session().fetchall()
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        start = 0
        for index, value in enumerate(sessions):
            table.setItem(index, 0, QTableWidgetItem(sessions[index][0]))
            # table.setItem(index, 1, QTableWidgetItem(sessions[index][1]))

        main_layout.addLayout(menu_layout)
        main_layout.addWidget(QHSeparationLine())
        main_layout.addWidget(table)

        self.setLayout(main_layout)

    def new_session_callback(self):
        app = NewSession(self, self.database_handle)
        app.open()

    def update_term_callback(self):
        win = UpdateTerm(self, self.database_handle)
        win.open()

    def update_student_callback(self):
        pass


class NewSession(QDialog):
    """Dialog window for adding new session"""
    def __init__(self, parent, database_handle):
        super(NewSession, self).__init__(parent)
        self.database_handle = database_handle
        self.setFixedWidth(320)
        self.setWindowTitle("New Session")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        self.session_entry = QLineEdit()
        self.session_entry.setObjectName('entry')
        self.session_entry.setPlaceholderText("Enter session")
        submit_btn = QPushButton("Submit")
        submit_btn.setObjectName("submit")
        submit_btn.clicked.connect(self.add_session)
        stat_frame = QHBoxLayout()
        label = QLabel("Set As Current")
        label.setStyleSheet("font-size:16px;padding-top:5px;")
        self.is_current = QCheckBox()
        stat_frame.addWidget(label)
        stat_frame.addWidget(self.is_current)
        layout.addWidget(self.session_entry)
        layout.addLayout(stat_frame)
        layout.addWidget(submit_btn)
        self.setLayout(layout)

    def add_session(self):
        session = self.session_entry.text()
        current = self.is_current.isChecked()
        if current:
            sql = f"INSERT INTO Session (name, status) VALUES ('{session}', 'current');"
        else:
            sql = f"INSERT INTO Session (name) VALUES ('{session}');"
        self.database_handle.insert_record(sql)
        QMessageBox.information(self, 'Success', "Session Added Successfully")
        self.destroy()


class UpdateTerm(QDialog):
    """Dialog window for Updating current term"""
    def __init__(self, parent, database_handle):
        super(UpdateTerm, self).__init__(parent)
        self.database_handle = database_handle
        self.setFixedWidth(320)
        self.setWindowTitle("Set Current Term")
        self.setStyleSheet("QDialog{background:white;}")
        # create widget and layout
        layout = QVBoxLayout()
        self.term_entry = QComboBox()
        self.term_entry.addItems(["First", "Second", "Third"])
        self.term_entry.setStyleSheet("padding:3px;font-size:15px;color:gray;"
                                      "margin-top:10px;"
                                      "border-radius:1px;border:1px solid grey;")
        self.term_entry.setPlaceholderText("Set Current Term")
        submit_btn = QPushButton("Submit")
        submit_btn.setObjectName("submit")
        submit_btn.clicked.connect(self.updated_term)
        layout.addWidget(self.term_entry)
        layout.addWidget(submit_btn)
        self.setLayout(layout)

    def updated_term(self):
        term = self.term_entry.currentText()
        sql = f"UPDATE Term SET status = 'current' WHERE name = '{term}';"
        self.database_handle.run_sql(sql)
        QMessageBox.information(self, 'Success', "Term Updated Successfully")
        self.destroy()
