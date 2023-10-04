from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QTableWidget, QHeaderView, QVBoxLayout, \
    QLabel, QHBoxLayout, QComboBox, QLineEdit, QWidget

from front_end.draw_line import QVSeparationLine, QHSeparationLine
from front_end.result_single import ResultSingle


class PreviewResult(QWidget):
    """Tab view for adding of result"""

    def __init__(self, database_handle):
        super().__init__()
        # self.setStyleSheet()
        self.database_handle = database_handle
        page_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        class_filter = QLabel("Select Class")
        class_filter.setStyleSheet("padding:4px;font-size:15px;")
        self.class_filter_input = QComboBox()
        classes = self.database_handle.fetch_class().fetchall()
        for item in classes:
            self.class_filter_input.addItem(item[0])
        self.class_filter_input.setStyleSheet("padding:4px;font-size:15px;")
        self.class_filter_input.setMinimumWidth(200)
        self.class_filter_input.currentTextChanged.connect(lambda text: self.populate_subject(text))

        self.subject_filter_input = QComboBox()
        subject = self.database_handle.fetch_subject_per_class("JSS 1").fetchall()
        for item in subject:
            self.subject_filter_input.addItem(item[0])
        self.subject_filter_input.setPlaceholderText("Select Subject")
        self.subject_filter_input.setStyleSheet("padding:4px;font-size:15px;")
        self.subject_filter_input.setMinimumWidth(200)
        filter_button = QPushButton("Filter Scores")
        filter_button.clicked.connect(self.call_load_data)
        filter_button.setStyleSheet("QPushButton{padding:8px;border-radius:0px;background:rgb(14, 180, 166);color:white;font-weight:bold}"
                                    "QPushButton:hover{background:rgb(49, 194, 189)}")
        # search bar follows here
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Find A Student")
        self.search_input.setStyleSheet("padding:4px;font-size:15px;")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student_callback)
        search_button.setStyleSheet(
            "QPushButton{padding:8px;border-radius:0px;background:rgb(14, 180, 166);color:white;font-weight:bold}"
            "QPushButton:hover{background:rgb(49, 194, 189)}")
        # load widget to menu layout
        menu_layout.addWidget(class_filter)
        menu_layout.addWidget(self.class_filter_input)
        menu_layout.addWidget(QVSeparationLine())
        menu_layout.addWidget(self.subject_filter_input)
        menu_layout.addWidget(filter_button)
        menu_layout.addWidget(QVSeparationLine())
        menu_layout.addWidget(self.search_input)
        menu_layout.addWidget(search_button)
        menu_layout.addWidget(QVSeparationLine())

        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Student Name", "Class", "Subject", "Session", "Term",
                                              "First CA", "Second CA", "Exams", "Total", "Action"])
        self.table.setStyleSheet(
            "QTableWidget::item {font-size:18px;selection-background-color:#f5f5f5;selection-color:black;}"
            "QHeaderView {font-size:18px;background:white}")
        self.table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.student = None

        page_layout.addLayout(menu_layout)
        page_layout.addWidget(QHSeparationLine())
        page_layout.addWidget(self.table)

        self.setLayout(page_layout)

    def populate_table(self):
        """function to populated table based on request"""
        if not self.student:
            QMessageBox.information(self, 'No Record!', "Scores Not Found For Entry Made!")
            self.table.clearContents()
            self.table.setRowCount(0)
        else:
            self.table.setRowCount(len(self.student))
            for index, value in enumerate(self.student):
                name = QTableWidgetItem(self.student[index][0])
                name.setFlags(Qt.ItemIsEnabled)
                subject = QTableWidgetItem(self.student[index][1])
                subject.setFlags(Qt.ItemIsEnabled)
                class_ = QTableWidgetItem(self.student[index][2])
                class_.setFlags(Qt.ItemIsEnabled)
                session = QTableWidgetItem(self.student[index][3])
                session.setFlags(Qt.ItemIsEnabled)
                term = QTableWidgetItem(self.student[index][4])
                term.setFlags(Qt.ItemIsEnabled)
                first_ca = QTableWidgetItem(str(self.student[index][5]))
                first_ca.setFlags(Qt.ItemIsEnabled)
                second_ca = QTableWidgetItem(str(self.student[index][6]))
                second_ca.setFlags(Qt.ItemIsEnabled)
                exam = QTableWidgetItem(str(self.student[index][7]))
                exam.setFlags(Qt.ItemIsEnabled)
                total = QTableWidgetItem(str(self.student[index][8]))
                more = QTableWidgetItem("View More")
                more.setIcon(QIcon("../images/view.png"))
                total.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(index, 0, name)
                self.table.setItem(index, 1, class_)
                self.table.setItem(index, 2, subject)
                self.table.setItem(index, 3, session)
                self.table.setItem(index, 4, term)
                self.table.setItem(index, 5, first_ca)
                self.table.setItem(index, 6, second_ca)
                self.table.setItem(index, 7, exam)
                self.table.setItem(index, 8, total)

                more_button = QPushButton("View More")
                more_button.setToolTip("View Result For A Student")
                edit_image = QIcon("../images/view2.png")
                more_button.setIcon(edit_image)
                more_button.clicked.connect(self.view_more)
                more_button.setStyleSheet("background:white;border:none;")
                self.table.setCellWidget(index, 0, more_button)


    def populate_subject(self, key):
        self.subject_filter_input.clear()
        subject = self.database_handle.fetch_subject_per_class(key).fetchall()
        for item in subject:
            self.subject_filter_input.addItem(item[0])

    def call_load_data(self):
        subject = self.subject_filter_input.currentText()
        class_ = self.class_filter_input.currentText()
        session = self.database_handle.fetch_current_session().fetchone()[0]
        term = self.database_handle.fetch_current_term().fetchone()[0]
        self.student = self.database_handle.fetch_scores(class_, subject, session, term).fetchall()
        self.populate_table()

    def search_student_callback(self):
        keyword = self.search_input.text()
        if not keyword:
            QMessageBox.information(self, "Empty!", "No Search Word Entered")
        else:
            self.student = self.database_handle.search_scores(keyword).fetchall()
            self.populate_table()

    def view_more(self):
        win = ResultSingle(self, self.database_handle)
        win.show()