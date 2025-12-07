#main logic file

#This program will allow the user to vote or exit. If voting, the user may choose one of 3 candidates. Poll results are displayed at the end.

#Main function - keeps track of the user's votes, displaying the final output
def main():
    #set votes for all candidates to 0
    isabella_votes = 0
    genji_votes = 0
    hannah_votes = 0
    total_votes = 0

    # run vote menu until user is done voting
    while True:
        choice = vote_menu()
        if choice == 'x':
            break
        #run candidate menu if the user wants to vote
        elif choice == 'v':
            u_vote = candidate_menu()
            if u_vote == 1:
                isabella_votes += 1
            elif u_vote == 2:
                genji_votes += 1
            else:
                hannah_votes += 1
        total_votes += 1
    print('----------------------------------------------')
    print(f'Isabella - {isabella_votes}, Genji - {genji_votes}, Hannah - {hannah_votes}, Total - {total_votes}')
    print('----------------------------------------------')

#Display the vote menu and return the user's response to the main function
def vote_menu():
    print('------------------------')
    print('VOTE MENU')
    print('------------------------')

    #ask user if they want to vote or exit
    u_choice = input('v: Vote\nx: Exit\nOption: ').strip().lower()
    while u_choice != 'v' and u_choice != 'x':
        u_choice = input('Invalid (v/x): ').strip().lower()
    return u_choice

#Display the candidate menu. Return the user's response to the main function
def candidate_menu():
    print('------------------------')
    print('CANDIDATE MENU')
    print('------------------------\n1: Isabella\n2: Genji\n3: Hannah')

    while True:
        u_vote = input('Candidate: ').strip()
        if u_vote == '1':
            print('Voted Isabella')
            break
        elif u_vote == '2':
            print('Voted Genji')
            break
        elif u_vote == '3':
            print('Voted Hannah')
            break
        else:
            u_vote = input('Invalid (1/2/3): ').strip()
    return int(u_vote)

#Run the program
if __name__ == '__main__':
    main()