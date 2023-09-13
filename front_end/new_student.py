from PySide6 import QtWidgets as widget
from PySide6 import QtCore
from PySide6.QtWidgets import QMessageBox

import draw_line


class RegisterUI(widget.QDialog):
    def __init__(self, parent):
        super(RegisterUI, self).__init__(parent)
        self.setFixedWidth(620)
        self.setWindowTitle("New Student")
        self.build_ui()

    def clear_btn_callback(self):
        self.name_entry.setText("")
        self.class_entry.setText("")
        self.age_entry.setText("")
        self.lga_entry.setText("")
        self.lga_entry.setText("")

    def save_button_callback(self):
        name = self.name_entry.text()
        class_ = self.class_entry.text()
        age = self.age_entry.text()
        lga = self.lga_entry.text()
        state = self.lga_entry.text()
        if not name or not class_ or not age or not lga or not state:
            QMessageBox.information(self, "Failure", 'Fields cannot be empty!')
        else:
            print(name, class_, age, lga, state)

    def build_ui(self):
        def extract_info():
            name = self.name_entry.text()
            class_ = self.class_entry.text()
            age = self.age_entry.text()
            state = self.state_entry.text()
            lga = self.lga_entry.text()
            print(name, class_, age, state, lga)
            print("nothing is going on")

        layout = widget.QVBoxLayout()
        inner_frame = widget.QFrame()
        inner_frame.setStyleSheet("background:white;")
        inner_frame.setObjectName("add_student_frame")
        inner_layout = widget.QVBoxLayout()
        inner_frame.setFixedWidth(600)
        # ------------------------ content goes here
        self.name_label = widget.QLabel("Student Name")
        self.name_label.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.name_entry = widget.QLineEdit()
        self.name_entry.setStyleSheet(
            """
            padding:3px;font-size:15px;
            color:gray;margin-top:10px;
            border-radius:1px;border:1px solid grey;
            """)
        class_label = widget.QLabel("Student Class")
        class_label.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.class_entry = widget.QLineEdit()
        self.class_entry.setStyleSheet(
            """
            padding:3px;font-size:15px;
            color:gray;margin-top:10px;
            border-radius:1px;border:1px solid grey;""")
        age_label = widget.QLabel("Student Age")
        age_label.setStyleSheet("""margin-top:10px;font-size:15px;padding-left:0px;""")
        self.age_entry = widget.QLineEdit()
        self.age_entry.setStyleSheet(
            """
            padding:3px;font-size:15px;
            color:gray;margin-top:10px;
            border-radius:1px;border:1px solid grey;
            """)
        state_label = widget.QLabel("Student's State")
        state_label.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.state_entry = widget.QLineEdit()
        self.state_entry.setStyleSheet(
            """
            padding:3px;font-size:15px;
            color:gray;margin-top:10px;
            border-radius:1px;border:1px solid grey;""")
        lga_label = widget.QLabel("Student's LGA")
        lga_label.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.lga_entry = widget.QLineEdit()
        self.lga_entry.setStyleSheet(
            """
            padding:3px;font-size:15px;
            color:gray;margin-top:10px;
            border-radius:1px;border:1px solid grey;""")
        action_layout = widget.QHBoxLayout()
        clear_btn = widget.QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_btn_callback)
        submit_btn = widget.QPushButton("Add Student")
        submit_btn.setStyleSheet("background:rgb(14, 180, 166);margin-top:20px;padding:10px;border-radius:5px")
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

