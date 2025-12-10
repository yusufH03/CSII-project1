#This file contains the logic to run the voting app. It will allow the user to vote for one of 5 candidates on the ballot. In order to do so, the user must enter a valid voter ID, and choose a candidate. They can then view the election results. Another voter can return to the ballot afterward and cast their vote. Votes are tracked in a CSV file, and voter IDs are tracked in a text file. This program imports the auto-generated GUI file, created via Qt Designer.
#CSCI-1620: Final Project-Part 1
#Written By: Yusuf Hussain, 12/9/2025

#import everything that is needed (PyQt6, the GUI file, CSV module, and Regular Expressions module)
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
    def enable_submit(self):
        """
        Enables submit button
        :return: None
        """
        self.submit_button.setEnabled(True)

    # clear and reset ballot
    def clear(self):
        """
        Resets the voting window (clears voter ID, candidate checkboxes)
        :return: None
        """
        self.id_input.clear()
        self.error_label.setText("")
        self.candidate1_checkBox.setChecked(False)
        self.candidate2_checkBox.setChecked(False)
        self.candidate3_checkBox.setChecked(False)
        self.candidate4_checkBox.setChecked(False)
        self.candidate5_checkBox.setChecked(False)

    # checks the validity of the ballot and adds the vote to the data file
    def check_ballot(self):
        """
        This method checks a ballot to see if a candidate has been voted for. It also ensures the voter ID is valid.
        :return: None
        """
        self.clear() # reset the ballot
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
            self.error_label.setText(f"Error. {e}")
        else:
            self.submit(voted_for, voter_id)
            self.id_list.append(voter_id)

    def submit(self, vote: int = None, voter_id: int = 0):
        """
        Method that increments the chosen candidate's vote in a CSV file, and appends the voter ID to a text file.
        :param vote: number of the candidate that was voted for
        :param voter_id: voter ID
        :return: None
        """
        #candidates on the ballot
        candidates = ["candidate1", "candidate2", "candidate3", "candidate4", "candidate5"]
        #set the candidate that was voted for
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
        for row in range(2, len(data)): #skip the header
                if data[row][0] == self.candidate: # find the candidate that was voted for
                    temp = data[row][1].strip() # temporarily store the current vote as a string
                    data[row][1] = int(temp)+1 # cast it to an int, add 1, and put the new vote count in data
                    data[row][1] = f"\t\t\t\t{data[row][1]}" # add back formatting
                elif data[row][0] == "Total Votes Casted:":
                    temp = data[row][1] # temporarily store the total
                    data[row][1] = int(temp)+1 # cast it to an int, add 1, and put the new total in data
                else:
                    pass

        # overwrite the file with updated data
        with open("data.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)

    #display the results of the election
    def results(self):
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
        self.election_results_label.setText("\n".join(display_text))

        self.stackedWidget.setCurrentIndex(1) # go to the results page

    #go back to the voting page from the results
    def home(self):
        """
        Returns to the voting window.
        :return: None
        """
        self.clear()
        self.stackedWidget.setCurrentIndex(0)
