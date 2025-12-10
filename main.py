#This is the main file that will run the voting app. It imports the logic, creates a window, and executes the app.
#CSCI-1620: Final Project Part 1
#Written By: Yusuf Hussain, 12/5/2025

from voting_logic import *


def main():
    application = QApplication([])
    window = Logic()
    window.setFixedSize(400, 500)
    window.show()
    application.exec()


#Run the program
if __name__ == '__main__':
    main()