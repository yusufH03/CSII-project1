#This file contains the logic to run the voting app. It will allow the user to vote for one of 5 candidates on the ballot. In order to do so, the user must enter a valid voter ID, and choose a candidate. They can then view the election results. Another voter can return to the ballot afterward and cast their vote. Votes are tracked in a CSV file, and voter IDs are tracked in a text file. This program imports the auto-generated GUI file, created via Qt Designer.
#CSCI-1620: Final Project-Part 1
#Written By: Yusuf Hussain, 12/9/2025
#import everything that is needed (PyQt6, the GUI file, CSV module, and Regular Expressions module)
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from gui import *
import csv
import re


class Logic(QMainWindow, Ui_voting_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # class variables to store the current candidate being voted for and all the voter IDs
        self.candidate = "candidate"
        self.id_list = []

        # only allow a ballot to be submitted if a candidate is voted for
        self.candidate1_checkBox.clicked.connect(lambda: self.enable_submit())
        self.candidate2_checkBox.clicked.connect(lambda: self.enable_submit())
        self.candidate3_checkBox.clicked.connect(lambda: self.enable_submit())
        self.candidate4_checkBox.clicked.connect(lambda: self.enable_submit())
        self.candidate5_checkBox.clicked.connect(lambda: self.enable_submit())
        # connect button presses to respective methods
        self.submit_button.clicked.connect(lambda: self.check_ballot())
        self.results_button.clicked.connect(lambda: self.results())
        self.back_button.clicked.connect(lambda: self.home())

    # allow the user to click submit
    def enable_submit(self) -> None:
        """
        Enables submit button
        :return: None
        """
        self.submit_button.setVisible(True)
        self.results_button.setVisible(True)

    # clear and reset ballot
    def clear(self) -> None:
        """
        Resets the voting window (clears voter ID, candidate checkboxes)
        :return: None
        """
        self.id_input.clear()
        self.error_label.setText("")
        self.candidate_group.setExclusive(False)
        self.candidate1_checkBox.setChecked(False)
        self.candidate2_checkBox.setChecked(False)
        self.candidate3_checkBox.setChecked(False)
        self.candidate4_checkBox.setChecked(False)
        self.candidate5_checkBox.setChecked(False)
        self.candidate_group.setExclusive(True)

    def check_ballot(self):
        """
        This method checks a ballot to see if a candidate has been voted for. It also ensures the voter ID is valid. If it is, the vote is added to the CSV file and the ID is added to the text file. Otherwise, an error message is displayed.
        :return: None
        """
        # check who the candidate voted for
        if self.candidate1_checkBox.isChecked():
            voted_for = 1
        elif self.candidate2_checkBox.isChecked():
            voted_for = 2
        elif self.candidate3_checkBox.isChecked():
            voted_for = 3
        elif self.candidate4_checkBox.isChecked():
            voted_for = 4
        elif self.candidate5_checkBox.isChecked():
            voted_for = 5

        # voter id must be unique, numerical, and 9 digits long
        try:
            voter_id = self.id_input.text().strip()
            if voter_id == "":
                raise ValueError("Enter a 9-digit voter ID")
            # must be a unique id
            elif voter_id in self.id_list:
                raise ValueError("You have already voted")
            # numbers only
            elif not voter_id.isdigit():
                raise ValueError("Please enter a numerical voter ID")
            # must not be shorter or longer than 9 numbers
            elif not re.fullmatch('[0-9]{9}', voter_id):
                raise ValueError(f"{voter_id} is invalid. Please enter a 9-digit voter ID")
        # display any errors
        except ValueError as e:
            self.clear()
            self.submit_button.setVisible(False) #voter cannot vote with an invalid ID
            self.results_button.setVisible(False) #voter cannot view results unless they have voted
            self.error_label.setText(f"Error. {e}")
        else:
            self.submit(voted_for, voter_id)
            self.id_list.append(voter_id)

    def submit(self, vote: int = None, voter_id: int = 0) -> None:
        """
        Method that increments the chosen candidate's vote in a CSV file, and appends the voter ID to a text file.
        :param vote: number of the candidate that was voted for
        :param voter_id: voter ID
        :return: None
        """
        self.clear()
        # candidates on the ballot
        candidates = ["A.W. Turing", "Mr. Syed", "Jimothy Jones", "Dr. Seuss", "Capt. Bail"]
        # set the candidate that was voted for
        self.candidate = candidates[vote - 1]

        # write ID to a text file
        id_file = open("ids.txt", "a")
        id_file.write(f"\n{voter_id}")
        id_file.close()

        # read the file and store it to a 2-D array
        with open("data.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            data = []
            for row in reader:
                data.append(row)

        # find the right candidate and add 1 to their votes as well as the total.
        for row in range(1, len(data)): #skip the header
                if data[row][0].startswith("-"): #skip separating rows
                    continue
                elif data[row][0] == self.candidate: # find the candidate that was voted for
                    data[row][1] = int(data[row][1].strip()) + 1 #cast the current vote to an int and add 1
                    data[row][1] = str(data[row][1]) #cast it back to a string and put the new vote count in data
                elif data[row][0] == "Total Votes Casted:":
                    data[row][1] = int(data[row][1]) + 1 #cast the total to an int and add 1
                    data[row][1] = str(data[row][1])  #cast back to a string and store new total in data
                else:
                    continue

        # overwrite the file with updated data
        with open("data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)

    def results(self) -> None:
        """
        Displays the results of the election.
        :return: None
        """
        self.clear()
        # print the text as it appears in the CSV file
        with open("data.csv", "r") as file:
            reader = csv.reader(file)
            display_text = []
            for row in reader:
                display_text.append(" ".join(row)) # add each row to be displayed
        self.election_results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.election_results_label.setText("\n".join(display_text))
        self.stackedWidget.setCurrentIndex(1) # go to the results page

    def home(self):
        """
        Returns back to the voting window with the ballot reset.
        :return: None
        """
        self.stackedWidget.setCurrentIndex(0)
        self.clear()


#NOTE: These lines need to be added to the gui file programmatically if it is regenerated using the designer.:
#self.voting_label.setGeometry(QtCore.QRect(0, 20, 400, 25))
#font = QtGui.QFont()
#font.setPointSize(15)
#font.setBold(True)
#font.setWeight(800)
#self.results_label.setGeometry(QtCore.QRect(0, 25, 400, 25))
#font = QtGui.QFont()
#font.setPointSize(20)
#font.setBold(True)
#font.setWeight(800)
#self.submit_button.setVisible(False)
#self.results_button.setVisible(False)