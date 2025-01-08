import math
from operator import truediv


def start_interface():
    print(f"\nPlease select your option \n 1. Load Data \n 2. process data \n 3. visualise data \n 4. export data \n 5. exit program")
    while True: #will continue to repeat if user continuously fail choosing the correct option.
        try:
            usr_choice = int(input("Enter your choice: "))
            if 1 <= usr_choice <= 5:
                return usr_choice
            else:
                print("Invalid choice, please pick the number between 1 and 5...")
        except ValueError: #catch if any input was not integer.
            print("Invalid input, enter a number with the following options: 1-5...")

def load_data():
    fileName = input("\n CASE SENSITIVE do not worry about adding .csv in the end \n Enter a .CSV file name: ")

def process_data():
    print("")

def visualise_data():
    print("")

def export_data():
    print("")

#user pick the following option
while True: #added a while so that it wouldn't exit the program if user wants to perform more actions in the other options...
    option = start_interface()

    if option == 1:
        load_data()
    if option == 2:
        process_data()
    if option == 3:
        visualise_data()
    if option == 4:
        export_data()
    if option == 5:
        print("Exiting program...")
        exit()



