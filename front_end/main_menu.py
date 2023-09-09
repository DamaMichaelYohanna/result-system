import sys
from PySide6 import QtWidgets as widget
from PySide6 import QtGui, QtCore


# user import
import draw_line
import student_info
import dashboard
import session_and_term
from front_end import result


class MainMenu(widget.QWidget):

    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)
        self.setWindowTitle("Main Menu")
        self.setWindowIcon(QtGui.QIcon("images/icon.png"))
        self.setContentsMargins(0, 0, 0, 0)
        # self.showMaximized()
        self.right_window_holder = widget.QStackedWidget()
        self.right_window_holder.addWidget(dashboard.Dashboard())
        self.right_window_holder.addWidget(student_info.StudentInfo())
        self.right_window_holder.addWidget(session_and_term.SessionAndTerm())
        self.right_window_holder.addWidget(result.Result())
        self.right_window_holder.setCurrentIndex(0)
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

        dashboard = widget.QPushButton(text="-> Dashboard")
        dashboard.clicked.connect(lambda: self.switch_page1(0))
        dashboard.setObjectName("menu_button")
        dashboard.setFixedWidth(300)
        #
        # add_student = widget.QPushButton(text="-> View ")
        # add_student.setObjectName("menu_button")
        # add_student.setFixedWidth(300)

        view_student = widget.QPushButton(text="-> View Student")
        view_student.setObjectName("menu_button")
        view_student.clicked.connect(lambda: self.switch_page1(1))
        view_student.setFixedWidth(300)

        session_and_term = widget.QPushButton(text="-> Session And Term")
        session_and_term.clicked.connect(lambda: self.switch_page1(2))
        session_and_term.setObjectName("menu_button")

        add_result = widget.QPushButton(text="-> Result Section")
        add_result.clicked.connect(lambda: self.switch_page1(3))
        add_result.setObjectName("menu_button")

        add_record = widget.QPushButton(text="-> General Settings")
        add_record.setObjectName("menu_button")
        view_record = widget.QPushButton(text="Add new student")

        # add widget to layout
        left_side.addWidget(label)
        left_side.addWidget(draw_line.QHSeparationLine())
        left_side.addWidget(dashboard)
        # left_side.addWidget(add_student)
        left_side.addWidget(view_student)
        left_side.addWidget(session_and_term)
        left_side.addWidget(add_result)
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
        self.setLayout(body_layout)

    def switch_page1(self, value):
        if value == self.right_window_holder.currentIndex():
            pass
            print("i just passed")
        else:
            self.right_window_holder.setCurrentIndex(value)


with open("front_end/style.qss") as file:
    style = file.read()

win = widget.QApplication(sys.argv)
my_app = MainMenu()
my_app.show()
win.setStyleSheet(style)
win.exec()
