#This is the main file that will run the voting app. It imports the logic and executes the app.
#CSCI-1620: Final Project Part 1
#Written By: Yusuf Hussain, 12/5/2025

from voting_logic import *


def main():
    """
    Creates a window with a fixed size and executes the voting app within it.
    :return: None
    """
    application = QApplication([])
    window = Logic() #creates a window using the Logic class within voting_logic
    window.setFixedSize(420, 500) #makes the window non-resizeable
    window.show()
    application.exec()


#Run the program
if __name__ == '__main__':
    main()
