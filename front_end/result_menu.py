from PySide6.QtWidgets import QPushButton, QLabel, \
    QLineEdit, QComboBox, QFrame, QVBoxLayout, QHBoxLayout, \
    QHeaderView, QTableWidget, QTableWidgetItem, QMessageBox, QTabWidget, QWidget, QDialog

from PySide6.QtGui import Qt, QIcon, QPixmap
from PySide6 import QtCore, QtGui

# user import
from draw_line import QHSeparationLine, QVSeparationLine
from front_end.result_preview import PreviewResult
from front_end.result_print import PrintResult
from new_student import RegisterUI
from result_single import ResultSingle

from back_end.database import DatabaseOps
from back_end.middleware import prepare_scores


class Result(QFrame):
    """UI page for result section"""

    def __init__(self, database_handle):
        super(Result, self).__init__()
        self.database_handle = database_handle
        self.result_tabs = QTabWidget()
        self.result_tabs.setStyleSheet("""
                                        QTabBar::tab:selected {
                                            background: white;
                                            padding:8px;
                                        }
                                        QTabWidget::pane { background:white;padding:10px;border-radius:0px}"""
                                       )

        self.result_tabs.addTab(PreviewResult(database_handle),
                                QPixmap("../images/view.png"),
                                "Preview Result",
                                )
        self.result_tabs.addTab(AddResult(),
                                QPixmap("../images/add.png"),
                                "New Entry")
        self.result_tabs.addTab(PrintResult(database_handle),
                                QPixmap("../images/print.png"),
                                "Print Result")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.result_tabs)
        self.setLayout(main_layout)


class AddResult(QWidget):
    """Tab view for adding of result"""

    def __init__(self):
        super().__init__()

        page_layout = QVBoxLayout()
        menu_layout = QHBoxLayout()
        class_filter = QLabel("Select Class")
        class_filter.setStyleSheet("padding:4px;font-size:15px;")
        self.class_filter_input = QComboBox()
        self.database_handle = DatabaseOps()
        classes = self.database_handle.fetch_class().fetchall()
        for item in classes:
            self.class_filter_input.addItem(item[0])
        self.class_filter_input.setStyleSheet("padding:4px;font-size:15px;")
        self.class_filter_input.setMinimumWidth(200)
        self.class_filter_input.currentTextChanged.connect(lambda text: self.populate_subject(text))

        subject_filter = QLabel("Select Subject")
        subject_filter.setStyleSheet("padding:4px;font-size:15px;")
        self.subject_filter_input = QComboBox()
        # subject_filter_input.currentTextChanged.connect(lambda text: self.)
        self.subject_filter_input.setStyleSheet("padding:4px;font-size:15px;")
        self.subject_filter_input.setMinimumWidth(200)
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

        menu_layout.addWidget(class_filter)
        menu_layout.addWidget(self.class_filter_input)
        menu_layout.addWidget(subject_filter)
        menu_layout.addWidget(self.subject_filter_input)
        menu_layout.addWidget(QVSeparationLine())
        menu_layout.addWidget(self.search_input)
        menu_layout.addWidget(search_button)
        menu_layout.addWidget(QVSeparationLine())

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        # table.setColumnWidth(0)
        self.table.setHorizontalHeaderLabels(["Name", "Class", "First CA", "Second CA", "Exams"])
        self.table.setStyleSheet(
            "QTableWidget::item {font-size:18px;selection-background-color:#f5f5f5;selection-color:black;}"
            "QHeaderView {font-size:18px;}")
        self.table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
        # self.student = self.database_handle.fetch_record("all").fetchall()
        # self.table.setRowCount(len(self.student))
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        # load student into table
        action_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_btn_callback)
        finish_btn = QPushButton("Save Record")
        finish_btn.clicked.connect(self.finish_btn_callback)
        action_layout.addWidget(clear_btn)
        action_layout.addWidget(finish_btn)
        # arrange widget to page layout
        page_layout.addLayout(menu_layout)
        page_layout.addWidget(QHSeparationLine())
        page_layout.addWidget(self.table)
        page_layout.addLayout(action_layout)
        # page_layout.addWidget(self.result_tabs)

        self.setLayout(page_layout)

    def populate_table(self):
        """function to populated table based on request"""
        if not self.student:
            QMessageBox.information(self, 'No Record!', "Record not found for entry made!")
            self.table.clearContents()
            self.table.setRowCount(0)
            self.subject_filter_input.clear()
        else:
            self.table.setRowCount(len(self.student))
            for index, value in enumerate(self.student):
                name = QTableWidgetItem(self.student[index][0])
                name.setFlags(Qt.ItemIsEnabled)
                class_ = QTableWidgetItem(self.student[index][2])
                class_.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(index, 0, name)
                self.table.setItem(index, 1, class_)
                # self.table.setItem(index, 2, QTableWidgetItem(self.student[index][2]))
                # self.table.setItem(index, 3, QTableWidgetItem(str(self.student[index][3])))
                # self.table.setItem(index, 4, QTableWidgetItem(self.student[index][4]))
                # self.table.setItem(index, 5, QTableWidgetItem(self.student[index][5]))

    def populate_subject(self, key):
        classes = self.database_handle.fetch_subject_per_class(key).fetchall()
        self.student = self.database_handle.fetch_record(key).fetchall()
        for item in classes:
            self.subject_filter_input.addItem(item[0])
        self.populate_table()

    def finish_btn_callback(self):
        """function collect data into table widget after entry.
            also prepare the data for further processing. set zero in field with not scores."""
        subject = self.subject_filter_input.currentText()
        session = self.database_handle.fetch_current_session().fetchone()[0]
        term = self.database_handle.fetch_current_term().fetchone()[0]
        class_ = self.class_filter_input.currentText()
        if subject:
            score_dict = {}  # create empty dict for later use
            for row in range(self.table.rowCount()):  # loop through table rows.
                score_list = []  # create a temporal list for storage
                for column in range(self.table.columnCount()):  # loop through the columns
                    value = self.table.item(row, column)
                    if value:
                        if value.text():
                            score_list.append(value.text())
                        else:
                            score_list.append('0')
                    else:
                        score_list.append('0')

                score_dict[row] = score_list

            # pass data for further processing
            scores = prepare_scores(score_dict.values(), self.subject_filter_input.currentText())
            # loop through students list and added score.
            return_value = None
            for student in scores[1]:
                return_value = self.database_handle.insert_score(
                    student, class_, subject, session, term,
                    scores[1][student][subject]["first_ca"],
                    scores[1][student][subject]["second_ca"],
                    scores[1][student][subject]["exam"],
                    scores[1][student][subject]["total"],
                )

                if return_value == "error":
                    QMessageBox.warning(self, "Error", "An unexpected error occurred. ")

                else:
                    QMessageBox.information(self, "Success", "Score add successfully")

        else:
            QMessageBox.warning(self, "Error", "No Subject selected! Select A Subject And Try Again. ")

    def validate_data(self):
        stored_score = self.database_handle.fetch_result(self.class_filter_input.currentText(),
                                                         self.subject_filter_input, "2023/2024")
        # for values in scores:
        #     result = self.database_handle.insert_scores(scores)
        pass

    def clear_btn_callback(self):
        """call back function to clear the entries """
        accept = QMessageBox.question(self, "Warning", "Are you sure you want to clear? "
                                                       "Scores will be gone")
        if accept == 16384:
            for row in range(self.table.rowCount()):
                for column in range(2, self.table.columnCount()):
                    value = self.table.item(row, column)
                    if value:
                        value.setText("")
                    else:
                        continue

    def add_student_callback(self):
        print("hello")
        app = RegisterUI(self)
        app.show()

    def search_student_callback(self):
        keyword = self.search_input.text()
        if not keyword:
            QMessageBox.information(self, "Empty!", "No Search Word Entered")
        else:
            self.student = self.database_handle.search_record(keyword).fetchall()
            # self.populate_table()
