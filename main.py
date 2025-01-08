from logging import exception

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

loaded_data = None #global variable for the loaded data

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
    filename = input("\n CASE SENSITIVE do not worry about adding .csv in the end \n Enter a .CSV file name: ")
    global loaded_data
    try:
        loaded_data = pd.read_csv(f"{filename}.csv")
        print(f"{loaded_data.head()}")
        input("Press ENTER to continue...")
        return
    except FileNotFoundError:
        print("File not found")
        input("Press ENTER to continue...")
        return
    except Exception as e:
        print(f"unexpected error: {e}")
        input("Press ENTER to continue...")
        return

def process_data():
    print("\nProcessing data...")


def visualise_data():
    print("")
    #conducting some small experiments of making bar chart.
    '''category_sums = loaded_data.groupby("ProductCategory")['Quantity'].sum()
    plt.bar(category_sums.index, category_sums.values)
    plt.show()'''
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



