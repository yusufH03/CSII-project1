from PyQt6.QtWidgets import *
from gui import Ui_voting_window
import csv
import re

class Logic(QMainWindow, Ui_voting_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.candidate = "candidate"
        self.submit_button.clicked.connect(lambda: self.check_ballot())
        self.results_button.clicked.connect(lambda: self.results())


    # function to clear and reset ballot
    def clear(self):
        self.id_input.clear()
        self.error_label.setText("")
        self.candidate1_checkBox.setChecked(False)
        self.candidate2_checkBox.setChecked(False)
        self.candidate3_checkBox.setChecked(False)
        self.candidate4_checkBox.setChecked(False)
        self.candidate5_checkBox.setChecked(False)



    def submit(self, vote=None, voter_id=0):
        #candidates on the ballot
        candidates = ["candidate1", "candidate2", "candidate3", "candidate4", "candidate5"]
        self.candidate = ""

        #read the file
        with open("data.csv", "r+") as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
            #find out & store number of votes for that candidate
            for row in range(1,len(data)-1):
                if data[row][0] == self.candidate:
                    data[row][1] += 1
                else:
                    pass

        #overwrite the file with updated vote
        with open("data.csv", "w") as file:
            writer = csv.writer(file)
            #start and end values
            start = 0
            end = 1
            for row in file:
                writer.writerow(data[start:end])
                start = end + 1
                end += 1

        #################can files be appended in the middle################
        #with open("data.csv", "w", newline='') as file:
        #    writer = csv.writer(file)
        #    #write the header
        #    writer.writerow(["Candidate", "Number of Votes"])
        #    for line in file:
        #        writer.writerow([candidates[vote], ])


    #checks the validity of the ballot and adds the vote to the data file
    def check_ballot(self):
        #voter id must be 9 digits long and only numerical values
        try:
            voter_id = self.id_input.text().strip()
            if voter_id is None:
                raise ValueError("Enter a 9-digit voter ID")
            #voter id must be numbers only
            elif not voter_id.isdigit():
                raise ValueError("Please enter a numerical voter ID")
            #voter id must not be shorter or longer than 9 numbers
            elif not re.match('^[0-9]{9}', voter_id):
                raise ValueError(f"{voter_id} is invalid. Please enter a 9-digit voter ID")
        #display any errors
        except ValueError as e:
            self.error_label.setText(f"Error. {e}")
        self.submit(voter_id)



    #display the results of the election
    def results(self):
        self.clear()