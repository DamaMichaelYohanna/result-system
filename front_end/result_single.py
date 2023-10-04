from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QTableWidget, QHeaderView, QVBoxLayout, \
    QLabel, QHBoxLayout, QDialog, QComboBox, QLineEdit, QWidget, QGridLayout

from front_end.draw_line import QHSeparationLine


class ResultSingle(QDialog):
    def __init__(self, parent, database_handle):
        super(ResultSingle, self).__init__(parent)
        self.setStyleSheet("""QDialog{background-image: url(../images/result_bg.png);}""")
        self.database_handle = database_handle
        # self.setFixedWidth(320)
        self.setWindowTitle("Result Page")
        # self.setStyleSheet("QDialog{background:white;}")
        main_layout = QVBoxLayout()
        head_layout = QHBoxLayout()
        logo_img_display = QLabel()
        logo_img = QPixmap("../images/view2.png'")
        logo_img_display.setPixmap(logo_img)
        middle_text = QVBoxLayout()
        school_name = QLabel("Sample School Name")
        school_name.setStyleSheet("font-size:25px;color:rgb(14, 180, 166);font-weight:bold")
        school_address = QLabel("Number 65, Adewale street, High court keffi, Nasarawa State")
        middle_text.addWidget(school_name)
        middle_text.addWidget(school_address)
        middle_text.addStretch()

        head_layout.addWidget(logo_img_display)
        head_layout.addLayout(middle_text)
        title = QLabel("Terminal Result Report")
        title.setStyleSheet("background:rgb(14, 180, 166);font-size:25px;"
                            "color:white;font-weight:bold;text-align:center;")
        title.setAlignment(QtCore.Qt.AlignCenter)

        title.setMinimumWidth(800)
        name_label = QLabel("Name")
        name_placement = QLabel("Dama Michael Yohanna")
        age_label = QLabel("Age")
        age_placement = QLabel("12")
        state_label = QLabel("State")
        state_placement = QLabel("Kaduna")
        lga_label = QLabel("LGA")
        lga_placement = QLabel("Daura")
        term_label = QLabel("Term")
        term_placement = QLabel("Second")
        session_label = QLabel("Session")
        session_placement = QLabel("2023/2024")
        student_no_label = QLabel("No of Student")
        student_no_placement = QLabel("20")

        info_section = QGridLayout()
        info_section.addWidget(name_label, 0, 0)
        info_section.addWidget(name_placement, 1, 0)
        info_section.addWidget(age_label, 0, 1)
        info_section.addWidget(age_placement, 1, 1)
        info_section.addWidget(state_label, 0, 2)
        info_section.addWidget(state_placement, 1, 2)
        info_section.addWidget(lga_label, 0, 3)
        info_section.addWidget(lga_placement, 1, 3)
        info_section.addWidget(term_label, 0, 4)
        info_section.addWidget(term_placement, 1, 4)
        info_section.addWidget(session_label, 0, 5)
        info_section.addWidget(session_placement, 1, 5)
        info_section.addWidget(student_no_label, 0, 6)
        info_section.addWidget(student_no_placement, 1, 6)

        main_layout.addLayout(head_layout)
        main_layout.addWidget(title)
        main_layout.addLayout(info_section)
        main_layout.addWidget(QHSeparationLine())
        main_layout.addStretch()
        self.setLayout(main_layout)