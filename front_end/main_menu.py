import sys
from PySide6 import QtWidgets as widget
from PySide6 import QtGui, QtCore

# user import
import draw_line
import student_info
import dashboard
import session_and_term
import result_menu
from back_end.database import DatabaseOps


class MainMenu(widget.QWidget):

    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.setWindowTitle("Main Menu")
        self.setWindowIcon(QtGui.QIcon("../images/icon.png"))
        self.setContentsMargins(0, 0, 0, 0)
        # self.showMaximized()
        # create DB instance and pass to different pages
        self.database_handle = DatabaseOps()
        # create instance of other window and arrange in stack
        self.right_window_holder = widget.QStackedWidget()
        self.right_window_holder.addWidget(dashboard.Dashboard(self.database_handle))
        self.right_window_holder.addWidget(student_info.StudentInfo(self.database_handle))
        self.right_window_holder.addWidget(session_and_term.SessionAndTerm(self.database_handle))
        self.right_window_holder.addWidget(result.Result(self.database_handle))
        self.right_window_holder.setCurrentIndex(0)
        self.current = 0
        self.style_active = """
        QPushButton#menu_button{background:rgb(31, 214, 199);color:white;}
        QPushButton#menu_button:hover{
        background:rgb(31, 210, 190);
        color:white;
        }
        """
        self.style_non_active = """
            QPushButton#menu_button{
                background:rgb(31, 214, 199, 0);
                padding:10px;
                border:none;
                font-style:bolder;
                font-size:20px;
                text-align:left;
                color:rgb(31, 214, 199);
                font-family:Consolas Bold;
            }
            QPushButton#menu_button:hover{
                color:rgb(74, 228, 215)
            }
        
        """
        # build the UI
        self.buildUi()

    def buildUi(self):
        body_layout = widget.QHBoxLayout(self)
        body_layout.setContentsMargins(0, 0, 0, 0)
        # --------------------------------------------
        # left  menu goes here
        left_frame = widget.QFrame()
        left_frame.setObjectName("left_frame")
        left_side = widget.QVBoxLayout()
        # -------------------- left side button and text here

        label = widget.QLabel("Administrator")
        # label.setPixmap(QtGui.QPixmap("images/retouch.pngg").scaled(100, 100))
        label.setAlignment(QtCore.Qt.AlignCenter)

        self.dashboard = widget.QPushButton(text="-> Dashboard")
        self.dashboard.clicked.connect(lambda: self.switch_page1(0))
        self.dashboard.setObjectName("menu_button")
        self.dashboard.setFixedWidth(300)
        #
        # add_student = widget.QPushButton(text="-> View ")
        # add_student.setObjectName("menu_button")
        # add_student.setFixedWidth(300)

        self.view_student = widget.QPushButton(text="-> View Student")
        self.view_student.setObjectName("menu_button")
        self.view_student.clicked.connect(lambda: self.switch_page1(1))
        self.view_student.setFixedWidth(300)

        self.session_and_term = widget.QPushButton(text="-> Session And Term")
        self.session_and_term.clicked.connect(lambda: self.switch_page1(2))
        self.session_and_term.setObjectName("menu_button")

        self.add_result = widget.QPushButton(text="-> Result Section")
        self.add_result.clicked.connect(lambda: self.switch_page1(3))
        self.add_result.setObjectName("menu_button")

        add_record = widget.QPushButton(text="-> General Settings")
        add_record.setObjectName("menu_button")
        view_record = widget.QPushButton(text="Add new student")

        # add widget to layout
        left_side.addWidget(label)
        left_side.addWidget(draw_line.QHSeparationLine())
        left_side.addWidget(self.dashboard)
        # left_side.addWidget(add_student)
        left_side.addWidget(self.view_student)
        left_side.addWidget(self.session_and_term)
        left_side.addWidget(self.add_result)
        left_side.addWidget(draw_line.QHSeparationLine())
        left_side.addWidget(add_record)
        # left_side.addWidget(view_record)
        left_side.addStretch()

        # self.right_window_holder.addWidget(student_info.StudentInfo())
        # self.right_window_holder.setCurrentIndex(1)
        right_side = self.right_window_holder
        # right_side.addStretch()

        left_frame.setLayout(left_side)
        body_layout.addWidget(left_frame)
        body_layout.addWidget(right_side)
        # body_layout.addStretch()
        self.update_selection(0)
        self.setLayout(body_layout)

    def switch_page1(self, value):
        if not value == self.right_window_holder.currentIndex():
            self.right_window_holder.setCurrentIndex(value)
            self.update_selection(value=value)

    def update_selection(self, value):
        if value == 0:
            self.dashboard.setStyleSheet(self.style_active)
            self.view_student.setStyleSheet(self.style_non_active)
            self.session_and_term.setStyleSheet(self.style_non_active)
            self.add_result.setStyleSheet(self.style_non_active)
        elif value == 1:
            self.view_student.setStyleSheet(self.style_active)
            self.dashboard.setStyleSheet(self.style_non_active)
            self.session_and_term.setStyleSheet(self.style_non_active)
            self.add_result.setStyleSheet(self.style_non_active)

        elif value == 2:
            self.session_and_term.setStyleSheet(self.style_active)
            self.dashboard.setStyleSheet(self.style_non_active)
            self.view_student.setStyleSheet(self.style_non_active)
            self.add_result.setStyleSheet(self.style_non_active)
        elif value == 3:
            self.add_result.setStyleSheet(self.style_active)
            self.view_student.setStyleSheet(self.style_non_active)
            self.dashboard.setStyleSheet(self.style_non_active)
            self.session_and_term.setStyleSheet(self.style_non_active)


with open("style.qss") as file:
    style = file.read()

win = widget.QApplication(sys.argv)
my_app = MainMenu()
my_app.show()
win.setStyleSheet(style)
win.exec()
