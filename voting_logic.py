from PyQt6.QtWidgets import *
from gui import Ui_voting_window

class Logic(QMainWindow, Ui_voting_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.results_button.clicked.connect(lambda: self.submit())

    def submit(self):
        id = self.id_label.text()
        self.id_label.clear()
        try:
            if self.results_button.checkedButton().text() == "Yes":
                self.labelName.setStyleSheet("color: green")
                self.labelName.setText(f"{id} selected yes")
            else:
                self.labelName.setStyleSheet("color: red")
                self.labelName.setText(f"{id} selected no")
        except AttributeError:
            self.labelName.setStyleSheet("color: blue")
            self.labelName.setText(f"No button selected")