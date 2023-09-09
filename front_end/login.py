import sys
from PySide6 import QtWidgets as widget
from PySide6 import QtGui, QtCore


class App(widget.QWidget):
    def __init__(self):
        super(App, self).__init__()
        print(self.windowTitle)
        self.setStyleSheet("background:white;")
        self.setWindowTitle("Result Application")
        self.setWindowIcon(QtGui.QIcon("icon.png"))

        main_layout = widget.QVBoxLayout(self)
        header_layout = widget.QHBoxLayout()
        image = QtGui.QPixmap("images/nsuk.png")
        login_image = QtGui.QPixmap("images/login.jpg")

        text1 = widget.QLabel()
        text1.setPixmap(image)
        text2 = widget.QLabel("RESULT PROCESSING SYSTEM")
        text2.setStyleSheet(
            """
                padding:50px;font-size:20px;
                font-style:bold;""")
        header_layout.addWidget(text1)
        header_layout.addStretch()
        header_layout.addWidget(text2)
        header_layout.addStretch()
        # create layout for both side of the body
        body_layout = widget.QHBoxLayout()
        left_body = widget.QVBoxLayout()
        right_body = widget.QHBoxLayout()

        # left side of the login body
        # ---------------------------------------------------------------
        label1 = widget.QLabel("Username Field")
        label1.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.entry1 = widget.QLineEdit()
        self.entry1.setFixedWidth(400)
        self.entry1.setPlaceholderText("Enter Username")
        self.entry1.setStyleSheet(
            """
            padding:5px;font-size:20px;
            color:brown;margin-top:10px;
            border-radius:5px;border:1px solid grey;""")

        label2 = widget.QLabel("Password Field")
        label2.setStyleSheet("""margin-top:10px;font-size:15px;""")
        self.entry2 = widget.QLineEdit()
        self.entry2.setPlaceholderText("Enter Your Password")
        self.entry2.setEchoMode(widget.QLineEdit.Password)
        self.entry2.setStyleSheet(
            """
            padding:5px;font-size:20px;
            color:gray;margin-top:10px;
            border-radius:5px;border:1px solid grey;""")
        self.entry2.setFixedWidth(400)
        login_btn = widget.QPushButton("Login")
        login_btn.clicked.connect(self.validate_login)
        login_btn.setStyleSheet(
            """
            padding:5px;font-size:15px;
            margin-top:10px;
            border-radius:5px;border:1px solid grey;""")

        left_body.addWidget(label1)
        left_body.addWidget(self.entry1)
        left_body.addWidget(label2)
        left_body.addWidget(self.entry2)
        left_body.addWidget(login_btn)
        left_body.setAlignment(QtCore.Qt.AlignCenter)

        # right part of the login body
        # ------------------------------------------------------------------
        image_label = widget.QLabel()
        image_label.setPixmap(login_image)
        right_body.addWidget(image_label)

        # add head and body layout to the main layout
        body_layout.addStretch()
        body_layout.addLayout(right_body)
        body_layout.addLayout(left_body)
        body_layout.addStretch()

        main_layout.addLayout(header_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(body_layout)
        main_layout.addStretch(2)
        self.setLayout(main_layout)  # set main layout

    def validate_login(self):
        username = self.entry1.text()
        password = self.entry2.text()
        if not username or not password:
            widget.QMessageBox.warning(self, "Error", "Fields can't be empty")
        else:
            print(username, password)



win = widget.QApplication(sys.argv)
my_app = App()
my_app.resize(600, 200)
my_app.show()
win.exec()
