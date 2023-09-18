from PySide6 import QtWidgets as widget
from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox

import draw_line
from front_end.extra import states


class RegisterUI(widget.QDialog):
    def __init__(self, parent, database_handle):
        super(RegisterUI, self).__init__(parent)
        self.setFixedWidth(620)
        self.setWindowTitle("New Student")
        self.database_handle = database_handle
        with open("student.qss") as file:
            style = file.read()
        self.setStyleSheet(style)
        self.build_ui()

    def clear_btn_callback(self):
            answer = QMessageBox.question(self, "Clear Fields?", 'Are you sure you want to clear entries?')
            if answer == 16384:
                self.name_entry.setText("")
                self.class_entry.setCurrentText("")
                self.age_entry.setText("")
                self.state_entry.setCurrentText("")
                self.lga_entry.setCurrentText("")

    def save_button_callback(self):
        name = self.name_entry.text()
        class_ = self.class_entry.currentText()
        age = self.age_entry.text()
        state = self.state_entry.currentText()
        lga = self.lga_entry.currentText()
        if not name or not class_ or not age or not lga or not state:
            QMessageBox.information(self, "Failure", 'Fields cannot be empty!')
        else:
            sql_statement = f"""INSERT INTO Student (name, age, sex, class_, state, lga) 
            VALUES ('{name}', '{age}', 'male','{class_}', '{state}', '{lga}');"""
            response = self.database_handle.insert_record(sql_statement)
            if not response == "error":
                QMessageBox.information(self, "Success!", "Record added successfully")
                self.clear_btn_callback()
            else:
                QMessageBox.critical(self, "Database error!", "Something happened! Record Not added.")

    def load_lga(self, text):
        """function to load lga based on selected state"""
        self.lga_entry.clear()
        self.lga_entry.addItems(states[text])

    def build_ui(self):
        """function to build the UI"""
        layout = widget.QVBoxLayout()
        inner_frame = widget.QFrame()
        inner_frame.setObjectName("add_student_frame")
        inner_layout = widget.QVBoxLayout()
        inner_frame.setFixedWidth(600)
        # ------------------------ content goes here
        self.name_label = widget.QLabel("Student Name")
        self.name_label.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.name_entry = widget.QLineEdit()
        self.name_entry.setObjectName("entry")
        class_label = widget.QLabel("Student Class")
        class_label.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.class_entry = widget.QComboBox()
        self.class_entry.setPlaceholderText("Select class")
        classes = self.database_handle.run_sql().fetchall()
        for item in classes:
            self.class_entry.addItem(item[0])
        self.class_entry.setObjectName("entry")
        age_label = widget.QLabel("Student Age")
        age_label.setStyleSheet("""margin-top:10px;font-size:15px;padding-left:0px;""")
        self.age_entry = widget.QLineEdit()
        self.age_entry.setObjectName("entry")
        state_label = widget.QLabel("Student's State")
        state_label.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.state_entry = widget.QComboBox()
        self.state_entry.addItems(states.keys())
        self.state_entry.currentTextChanged.connect(lambda text: self.load_lga(text))
        self.state_entry.setObjectName("entry")

        lga_label = widget.QLabel("Student's LGA")
        lga_label.setStyleSheet("""margin-top:10px;font-size:15px;""")

        self.lga_entry = widget.QComboBox()
        self.lga_entry.setObjectName("entry")
        action_layout = widget.QHBoxLayout()  # create new layout for button
        clear_btn = widget.QPushButton("Clear Fields")
        clear_btn.setObjectName("action_button")
        clear_btn.clicked.connect(self.clear_btn_callback)

        submit_btn = widget.QPushButton("Add Student")
        submit_btn.setObjectName("action_button")
        submit_btn.setFixedWidth(300)
        submit_btn.clicked.connect(self.save_button_callback)

        action_layout.addWidget(clear_btn)
        action_layout.addWidget(submit_btn)
        # --------------------------- A add widget to layout
        header = widget.QLabel("Student Information Form")
        # header.setAlignment(QtCore.Qt.AlignCenter)
        header.setStyleSheet("padding:20px;color:rgb(14, 180, 166);font-size:25px;font-family:helvetica;")
        inner_layout.addWidget(header)
        inner_layout.addWidget(draw_line.QHSeparationLine())
        inner_layout.addWidget(self.name_label)
        inner_layout.addWidget(self.name_entry)
        inner_layout.addWidget(class_label)
        inner_layout.addWidget(self.class_entry)
        inner_layout.addWidget(age_label)
        inner_layout.addWidget(self.age_entry)
        inner_layout.addWidget(state_label)
        inner_layout.addWidget(self.state_entry)
        inner_layout.addWidget(lga_label)
        inner_layout.addWidget(self.lga_entry)
        inner_layout.addLayout(action_layout)
        # inner_layout.addWidget(submit_btn)
        # inner_layout.addWidget(submit_btn)
        inner_layout.addStretch(5)
        inner_layout.setAlignment(QtCore.Qt.AlignCenter)

        # header = widget.QLabel("Enter Student Information Below")
        # header.setAlignment(QtCore.Qt.AlignCenter)
        # header.setStyleSheet("padding:20px;color:rgb(14, 180, 166);font-size:25px;font-family:helvetica;")

        # layout.addWidget(header)
        # layout.addWidget(draw_line.QHSeparationLine())
        # layout
        inner_frame.setLayout(inner_layout)
        layout.addWidget(inner_frame)
        self.setLayout(layout)
        # layout.addLayout(inner_layout)
