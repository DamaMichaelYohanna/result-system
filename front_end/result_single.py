from PySide6.QtWidgets import QDialog


class ResultSingle(QDialog):
    def __init__(self, parent, database_handle):
        super(ResultSingle, self).__init__(parent)
        self.database_handle = database_handle
        self.setFixedWidth(320)
        self.setWindowTitle("Result Page")
        self.setStyleSheet("QDialog{background:white;}")